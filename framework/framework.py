from abc import abstractproperty
from wsgiref.simple_server import make_server

from framework.views import View
from framework.views.view_type import NoFoundPage


class FrameWork:
    __single: "FrameWork|None" = None

    views: dict[str, View]
    fronts: set

    def __init__(self) -> None:
        self.views = {}
        self.fronts = set()

    def register_views(self, view, url: str):
        self.views[url] = view

    def register_front(self, front):
        self.fronts.add(front)

    def get_register_urls(self):
        return self.views.keys()

    def __call__(self, request, response):
        url = request["PATH_INFO"]

        if not url.endswith("/"):
            path = f"{url}/"

        view = None
        if url in self.views:
            view = self.views[url]

        if view == None:
            view = NoFoundPage()
        answer = {}

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
