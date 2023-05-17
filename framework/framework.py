from typing import Callable
from wsgiref.simple_server import make_server
import re

from framework.error import NoNameSpaceFound
from framework.error.error import DuplicateNameSpace, FrameWorkError
from framework.fronts import (
    BreakPoint,
    FunctionCalback,
    NameSpaceList,
    ParsedEnvArgs,
    Router,
    Static,
)
from framework.fronts.fronts import DebugSysEnv, DebugViewEnv, LoginClient
from framework.logger.logger import LoggerFront
from framework.types import FrontType, SysEnv, ViewEnv, ViewResult, ViewType, consts
from framework.types.types import ByLoginPass
from framework.types.url_tree import UrlTree
from framework.views import NoFoundPage, MediaStaicFileView
from framework.utils import SingleToneType


class FrameWork(metaclass=SingleToneType):
    tree: UrlTree
    views: dict[str, tuple[ViewType, str]]
    fronts: set
    funcs: dict[str, Callable]
    config: dict
    static_vars: dict
    client: set
    init: bool

    def __init__(self) -> None:
        self.tree = UrlTree()
        self.views = {}
        self.fronts = set()
        self.config = {}
        self.static_vars = {}

        self.clients = set()
        self.init = False

    def static_var(self, name: str, var):
        self.static_vars[name] = var

    def _register_client(self, login: str, passwd: str):
        client = ByLoginPass(login, passwd, self.config[consts.KEY])
        self.clients.add(client)

    def _get_client(self, by_login: str | None = None, by_index: int | None = None):
        for client in self.clients:
            if by_login:
                if client.index == by_index:
                    return client
            elif by_index:
                if client.login == by_login:
                    return client

    def register_views(self, view: ViewType, url: str, namespace: str):
        self.tree.register_views(view, url, namespace)

        # have url "item/<value:type>"
        all_namespace = self.get_register_namespace_url().keys()

        if namespace in all_namespace:
            raise DuplicateNameSpace(namespace)

        self.views[url] = (view, namespace)

    def register_function(self, calback: Callable, force_name: "str|None" = None):
        clb = FunctionCalback(calback, force_name)

    def register_front(self, front: FrontType):
        self.fronts.add(front)

    def get_register_urls(self):
        return self.views.keys()

    def get_register_namespace_url(self):
        return {value[1]: key for key, value in self.views.items()}

    def __call__(self, sys_env, response):
        try:
            sys_env = SysEnv(sys_env)
            url = sys_env["PATH_INFO"]
            method = sys_env["REQUEST_METHOD"]

            if not url.endswith("/"):
                url = f"{url}/"

            # ToDo: buildin views
            # self.register_views(
            #     MediaStaicFileView(), "/__static__/*", namespace="__static__"
            # )

            # ToDo: switch to Tree
            view_env = ViewEnv()

            node_view = self.tree.view_by_url(url.split("?")[0], view_env)
            view = node_view or NoFoundPage()

            # view: ViewType = NoFoundPage()
            # url_without_args = url.split("?")[0]
            # if url_without_args in self.views:
            #     view = self.views[url_without_args][0]

            # add static_var
            view_env[consts.ViewEnv_StaticVar] = self.static_vars
            view_env["__DB_CLIENT__"] = self.clients

            # buildin fronts
            buildin_front = [
                LoginClient(),
                BreakPoint(),
                LoggerFront(
                    custom_logger=self.config.get(consts.CNFG_CUSTOM_LOGGER)
                    # self.config.get(consts.CNFG_LOGGER_LEVEL),
                ),
                ParsedEnvArgs(),
                NameSpaceList(self.get_register_namespace_url()),
                Router(),
                Static(
                    home_static_path=self.config.get(
                        consts.CNFG_STATIC_PTH, consts.DEFAULT_CNFG_STATIC_PTH
                    ),
                    static_flg=self.config.get(
                        consts.CNFG_STATIC_MEDIA_FLG,
                        consts.DEFAULT_CNFG_STATIC_MEDIA_FLG_VALUE,
                    ),
                ),
            ]

            if self.config.get(consts.CNFG_SYSENV_DEBUG, False):
                buildin_front.append(DebugSysEnv())

            if self.config.get(consts.CNFG_VIEWENV_DEBUG, False):
                buildin_front.append(DebugViewEnv())

            for front in buildin_front:
                if not self.init:
                    front.init(sys_env, view_env, self.config)
                front(sys_env, view_env, self.config)

            self.init = True
            # user fronts
            for front in self.fronts:
                front(sys_env, view_env, self.config)

            # ToDo: conver to buildin_view
            if view_env.get("MediaStaicFileView") and view_env["MediaStaicFileView"]:
                view = MediaStaicFileView()

            # args = view_env.get(consts.ViewEnv_ARGS) or {}
            # if args:
            #     if method.upper() == "GET":
            #         # view_env.logger.debug
            #         print(f"GET method with {args}")
            #     elif method.upper() == "POST":
            #         # view_env.logger.debug
            #         print(f"POST method with {args}")

            view_result = ViewResult(view_env)
            # sys_env - don`t must be in view_env
            view(view_env, self.config, view_result)
            response(
                str(view_result.code) + " ", [("Content-Type", view_result.data_type)]
            )

            if view_result.is_text:
                return [view_result.data.encode("utf-8")]
            else:
                return [view_result.data]
        except NoNameSpaceFound as err:
            # raise err

            response("400 ", [("Content-Type", "text/html")])
            if self.config[consts.DEBUG]:
                return [
                    f"<h1>NoNameSpaceFound by <b>'{err.namespace}'</b><h1>".encode(
                        "utf-8"
                    )
                ]
            else:
                return [""]

        except FrameWorkError as err:
            response("400 ", [("Content-Type", "text/html")])
            if self.config[consts.DEBUG]:
                return [f"<h1>Exception <br>'{err.__str__()}'</br><h1>".encode("utf-8")]
            else:
                return [""]

        except Exception as err:
            raise err
            response("400 ", [("Content-Type", "text/html")])
            if self.config[consts.DEBUG]:
                return [f"<h1>Exception <br>'{err.__str__()}'</br><h1>".encode("utf-8")]
            else:
                return [""]

    # will be deleted
    @classmethod
    def get_framework(cls):
        return FrameWork()

    @classmethod
    def run_server(cls, addr, port):
        with make_server(addr, port, cls.get_framework()) as server:
            print(f"Run server http://{addr}:{port}")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\rServer stop")
