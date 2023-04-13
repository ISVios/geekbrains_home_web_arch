from typing import Callable
import os.path


class InitFront:
    def __call__(self, response: dict, config: dict, **kwds) -> dict:
        # Todo: In future move
        # homeurl
        # namespace
        # router
        # calback
        # static == paths
        # ......
        return response


class NameSpaceList:
    def __call__(self, response: dict, url_dict: dict[str, str]) -> dict:
        response["namespace_list"] = url_dict
        return response


class FunctionCalback:
    func: Callable
    name: str

    def __init__(self, func: Callable, force_name: "str|None" = None) -> None:
        self.func = func
        self.name = force_name or func.__name__

    def __call__(self, response: dict) -> dict:
        response[self.name] = self.func
        return response


class Router:
    def __call__(self, response: dict) -> dict:
        def router(url):
            return response["namespace_list"][url]

        FunctionCalback(router)(response)
        return response


class Static:
    static_pth: str

    def __init__(self, home_static_path: str) -> None:
        self.static_pth = home_static_path

    def __call__(self, response: dict) -> dict:
        def static(path):
            return os.path.join(self.static_pth, path)

        response["static"] = static

        return response
