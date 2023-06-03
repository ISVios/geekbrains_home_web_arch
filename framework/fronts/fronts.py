import os.path
from sqlite3 import Connection, connect
from typing import Callable

from framework.error import NoNameSpaceFound
from framework.types import FrontType, SysEnv, ViewEnv, consts
from framework.types.types import ByAnon, ClientControl, Session
from framework.utils.get_data import parse_args_by_method


class DbFront(FrontType):
    db: Connection

    def __init__(self) -> None:
        super().__init__()

    def init(self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds):
        self.db = connect("db.sqlite3")
        Session.new_session(self.db)
        return super().init(sys_env, view_env, config, **kwds)

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        return super().front_action(sys_env, view_env, config, **kwds)


class LoginClient(FrontType):
    def __init__(self) -> None:
        super().__init__()

    def init(self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds):
        view_env.static_vars["__ClientList__"] = {}
        view_env["is_auth"] = False

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        ip = sys_env.get("REMOTE_ADDR")
        client_list = view_env.static_vars["__ClientList__"]
        if not ip in client_list:
            controll = ClientControl(config)
            controll.auth(ByAnon())
            #     authclient = AuthFabric.auth({"ip": ip})
            view_env.static_vars["__ClientList__"][ip] = controll

        client = view_env.static_vars["__ClientList__"][ip]
        view_env["__ClientAuth__"] = client

        view_env["is_auth"] = client.is_auth()

        return super().front_action(sys_env, view_env, config, **kwds)


class NameSpaceList(FrontType):
    namespace_list: dict

    def __init__(self, namespace_list):
        self.namespace_list = namespace_list
        super().__init__()

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        # full_url
        view_env["__IP__"] = sys_env["REMOTE_ADDR"]
        view_env[consts.ViewEnv_CUR_URL] = sys_env["PATH_INFO"]
        view_env[consts.ViewEnv_HOST_URL] = sys_env["HTTP_HOST"]
        view_env[consts.ViewEnv_NAMESPAGEPAGE] = self.namespace_list
        return view_env


class FunctionCalback(FrontType):
    func: Callable
    name: str

    def __init__(self, func: Callable, force_name: "str|None" = None) -> None:
        self.func = func
        self.name = force_name or func.__name__
        super().__init__()

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env[self.name] = self.func
        return view_env


class DebugSysEnv(FrontType):
    def __init__(self) -> None:
        super().__init__()

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env.logger.debug(sys_env.to_dict())
        return super().front_action(sys_env, view_env, config, **kwds)


class DebugViewEnv(FrontType):
    def __init__(self) -> None:
        super().__init__()

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env.logger.debug(view_env.to_dict())
        return super().front_action(sys_env, view_env, config, **kwds)


class BreakPoint(FrontType):
    def __init__(self) -> None:
        super().__init__()

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env["Debug_Mode"] = config[consts.DEBUG]

        def breakpoint_func(sys_env: SysEnv, view_env: ViewEnv, config: dict, func):
            if config.get(consts.DEBUG) and config[consts.DEBUG]:
                func()

        view_env[consts.ViewEnv_BREAKPOINT] = lambda: breakpoint_func(
            sys_env, view_env, config, breakpoint
        )  # add python breakpoint func
        return super().front_action(sys_env, view_env, config, **kwds)


class ParsedEnvArgs(FrontType):
    def __init__(self) -> None:
        super().__init__()

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env[consts.ViewEnv_METHOD] = sys_env.get("REQUEST_METHOD")
        # view_env[consts.ViewEnv_ARGS] = parse_args_by_method(sys_env.to_dict())
        view_env[consts.ViewEnv_URL_PARAM] = parse_args_by_method(sys_env.to_dict())
        # ToDo: add `get args from UrlTree`
        return view_env


class Router(FrontType):
    def __init__(self) -> None:
        super().__init__()

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        def router(url, **kwds):
            """
            conver {{ router ('index') }} to url from namespace_list
            """
            router_dict = view_env[consts.ViewEnv_NAMESPAGEPAGE]
            if not url in router_dict:
                raise NoNameSpaceFound(url)

            url = view_env[consts.ViewEnv_NAMESPAGEPAGE][url]

            sub = ""
            # add kwds
            for k, v in kwds.items():
                sub += f"{k}={v}&"

            sub = sub[:-1]

            # print(sub)

            return url + "?" + sub

        def is_router(url, **kwds):
            """
            test current url with router('url')
            """
            url_without_args = url.split("?")[0]
            router_url = router(url_without_args)
            cur_url = view_env[consts.ViewEnv_CUR_URL]

            return cur_url.split("?")[0] == router_url.split("?")[0]

        FunctionCalback(func=router)(sys_env, view_env, config, **kwds)
        FunctionCalback(func=is_router)(sys_env, view_env, config, **kwds)
        return view_env


class UrlJump(FrontType):
    def __init__(self) -> None:
        super().__init__()

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        def jump_url(url: str, **kwds):
            sys_env["PATH_INFO"] = url

        def jump_namespace(to_namespace: str, **kwds):
            url = view_env[consts.ViewEnv_NAMESPAGEPAGE].get(to_namespace)
            if url:
                sys_env["PATH_INFO"] = url

        return super().front_action(sys_env, view_env, config, **kwds)


class Static(FrontType):
    static_pth: str
    static_flg: str

    def __init__(
        self,
        home_static_path: str,
        static_flg: str = consts.DEFAULT_CNFG_STATIC_MEDIA_FLG_VALUE,
    ) -> None:
        super().__init__()
        self.static_pth = home_static_path
        self.static_flg = static_flg

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        def static(path):
            # return
            # host_url + __static__flag + static_pth(in view) + file
            return os.path.join(
                view_env[consts.ViewEnv_HOST_URL],
                self.static_flg,
                # self.static_pth,
                path,
            )

        # add static func
        view_env[consts.ViewEnv_STATIC] = static

        # parse static file
        url = view_env[consts.ViewEnv_CUR_URL]
        url_splt = url.split(self.static_flg)
        if len(url_splt) > 1:
            view_env["File"] = url_splt[1]
            view_env["MediaStaicFileView"] = True
        return view_env
