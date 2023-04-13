from abc import abstractproperty
from typing import Callable
from wsgiref.simple_server import make_server
from framework.fronts import NameSpaceList, Router
from framework.fronts.fronts import FunctionCalback, Static

from framework.views import View
from framework.views.view_type import NoFoundPage


class FrameWork:
    __single: "FrameWork|None" = None

    views: dict[str, tuple[View, str]]
    fronts: set
    funcs: dict[str, Callable]
    config: dict

    def __init__(self) -> None:
        self.views = {}
        self.fronts = set()
        self.config = {}

    def register_views(self, view, url: str, namespace: str):
        self.views[url] = (view, namespace)

    # ToDo: make nones name field
    def register_function(self, name: str, calback: Callable):
        clb = FunctionCalback(calback, name)

    def register_front(self, front):
        self.fronts.add(front)

    def get_register_urls(self):
        return self.views.keys()

    def get_register_namespace_url(self):
        return {value[1]: key for key, value in self.views.items()}

    def __call__(self, request, response):
        url = request["PATH_INFO"]

        if not url.endswith("/"):
            url = f"{url}/"

        view = None
        if url in self.views:
            view = self.views[url][0]

        if view == None:
            view = NoFoundPage()
        answer = {}

        # init buildin fronts
        NameSpaceList()(answer, self.get_register_namespace_url())
        Router()(answer)
        Static(self.config["static_pth"])(answer)
        for front in self.fronts:
            front(answer)

        code, body = view(answer)

        response(str(code) + " ", [("Content-Type", "text/html")])
        return [body.encode("utf-8")]

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
