import os.path
from typing import Callable

from framework.error import NoNameSpaceFound
from framework.types import FrontType, SysEnv, ViewEnv, consts
from framework.utils.get_data import parse_args_by_method


class NameSpaceList(FrontType):
    namespace_list: dict

    def __init__(self, namespace_list):
        self.namespace_list = namespace_list

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        # view_env["_"] = sys_env[]
        # full_url
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

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env[self.name] = self.func
        return view_env


# ToDo: connect with config "debug_print_sysenv"
class DebugSysEnv(FrontType):
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env.logger.debug(sys_env.to_dict())
        return super().front_action(sys_env, view_env, config, **kwds)


# ToDo: connect with config "debug_print_viewenv"
class DebugViewEnv(FrontType):
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env.logger.debug(view_env.to_dict())
        return super().front_action(sys_env, view_env, config, **kwds)


class BreakPoint(FrontType):
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        def breakpoint_func(sys_env: SysEnv, view_env: ViewEnv, config: dict, func):
            if config.get(consts.DEBUG) and config[consts.DEBUG]:
                func()

        view_env[consts.ViewEnv_BREAKPOINT] = lambda: breakpoint_func(
            sys_env, view_env, config, breakpoint
        )  # add python breakpoint func
        return super().front_action(sys_env, view_env, config, **kwds)


class ParsedEnvArgs(FrontType):
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env[consts.ViewEnv_METHOD] = sys_env.get("REQUEST_METHOD")
        view_env[consts.ViewEnv_ARGS] = parse_args_by_method(sys_env.to_dict())
        return view_env


class Router(FrontType):
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        def router(url):
            """
            conver {{ router ('index') }} to url from namespace_list
            """
            router_dict = view_env[consts.ViewEnv_NAMESPAGEPAGE]
            if not url in router_dict:
                raise NoNameSpaceFound(url)

            return view_env[consts.ViewEnv_NAMESPAGEPAGE][url]

        def is_router(url):
            """
            test current url with router('url')
            """
            router_url = router(url)
            cur_url = view_env[consts.ViewEnv_CUR_URL]

            return cur_url == router_url

        FunctionCalback(func=router)(sys_env, view_env, config, **kwds)
        FunctionCalback(func=is_router)(sys_env, view_env, config, **kwds)
        return view_env


class Static(FrontType):
    static_pth: str
    static_flg: str

    def __init__(
        self,
        home_static_path: str,
        static_flg: str = consts.DEFAULT_CNFG_STATIC_MEDIA_FLG_VALUE,
    ) -> None:
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
