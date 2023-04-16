from typing import Callable
from wsgiref.simple_server import make_server
from framework.error import NoNameSpaceFound
from framework.fronts import (
    NameSpaceList,
    Router,
    ParsedEnvArgs,
    FunctionCalback,
    Static,
)
from framework.types import SysEnv, ViewType, FrontType, ViewEnv, ViewResult

from framework.views import NoFoundPage


class FrameWork:
    __single: "FrameWork|None" = None

    views: dict[str, tuple[ViewType, str]]
    fronts: set
    funcs: dict[str, Callable]
    config: dict

    def __init__(self) -> None:
        self.views = {}
        self.fronts = set()
        self.config = {}

    def register_views(self, view: ViewType, url: str, namespace: str):
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

            view: ViewType = NoFoundPage()
            if url in self.views:
                view = self.views[url][0]

            view_env = ViewEnv()

            # buildin fronts
            buildin_front = [
                ParsedEnvArgs(),
                NameSpaceList(self.get_register_namespace_url()),
                Router(),
                Static(self.config["static_pth"]),
            ]

            for front in buildin_front:
                front(sys_env, view_env, self.config)

            # user fronts
            for front in self.fronts:
                front(sys_env, view_env, self.config)

            args = view_env.get("ParsedEnvArgs") or {}
            if method.upper() == "GET":
                print(f"GET method with {args}")
            elif method.upper() == "POST":
                print(f"POST method with {args}")

            if not view:
                view = NoFoundPage()

            view_result = ViewResult(view_env)
            # sys_env - don`t must be in view_env
            view(view_env, self.config, view_result)

            response(str(view_result.code) + " ", [("Content-Type", "text/html")])
            return [view_result.text.encode("utf-8")]
        except NoNameSpaceFound as err:
            response("400 ", [("Content-Type", "text/html")])
            return [
                f"<h1>NoNameSpaceFound by <b>'{err.namespace}'</b><h1>".encode("utf-8")
            ]

    @classmethod
    def get_framework(cls):
        if cls.__single == None:
            cls.__single = FrameWork()
        return cls.__single

    @classmethod
    def run_server(cls, addr, port):
        with make_server(addr, port, cls.get_framework()) as server:
            # conver to logger
            print(f"Run server {addr}:{port}")
            server.serve_forever()
