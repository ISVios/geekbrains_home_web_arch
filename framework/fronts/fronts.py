import abc
import os.path
from typing import Callable
from framework.error import NoNameSpaceFound
from framework.types.types import ViewType

from framework.utils.get_data import parse_args_by_method
from framework.types import SysEnv, ViewEnv, FrontType


class NameSpaceList(FrontType):
    namespace_list: dict

    def __init__(self, namespace_list):
        self.namespace_list = namespace_list

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env["NameSpaceList"] = self.namespace_list
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


class ParsedEnvArgs(FrontType):
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env["Method"] = sys_env.get("REQUEST_METHOD")
        view_env["ParsedEnvArgs"] = parse_args_by_method(sys_env.to_dict())
        return view_env


class Router(FrontType):
    # reg_views: dict[str, ViewType]
    #
    # def __init__(self, reg_views):
    #     self.reg_views = reg_views

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        def router(url):
            router_dict = view_env["NameSpaceList"]
            if not url in router_dict:
                raise NoNameSpaceFound(url)

            return view_env["NameSpaceList"][url]

        FunctionCalback(func=router)(sys_env, view_env, config, **kwds)
        return view_env


class Static(FrontType):
    static_pth: str

    def __init__(self, home_static_path: str) -> None:
        self.static_pth = home_static_path

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        def static(path):
            return os.path.join(self.static_pth, path)

        view_env["static"] = static

        return view_env
