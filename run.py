#!/usr/bin/env python
"""
User script how use framework
"""
import argparse
import datetime

from framework import FrameWork
from framework.utils.render import render
from framework.views.view_type import View

DEF_ADR = "0.0.0.0"
DEF_PORT = 8080


# urls
class Contact(View):
    def __call__(self, response) -> tuple[int, str]:
        return 200, render("contact.html", "./simplestyle_8/", **response)


class Index(View):
    def __call__(self, response) -> tuple[int, str]:
        return 200, render("index.html", "./simplestyle_8/", **response)


class AnotherPage(View):
    def __call__(self, response) -> tuple[int, str]:
        return 200, render("another_page.html", "./simplestyle_8/", **response)


class Examples(View):
    def __call__(self, response) -> tuple[int, str]:
        return 200, render("examples.html", "./simplestyle_8/", **response)


class Page(View):
    def __call__(self, response) -> tuple[int, str]:
        return 200, render("page.html", "./simplestyle_8/", **response)


# fronts
class Date:
    def __call__(self, response):
        response["date"] = datetime.datetime.now()
        return response


class Urls:
    def __call__(self, response):
        response["urls"] = FrameWork.get_framework().get_register_urls()
        return response


if __name__ == "__main__":
    # ToDo: add argparse
    framework = FrameWork.get_framework()

    # config
    framework.config["adr"] = DEF_ADR
    framework.config["port"] = DEF_PORT
    framework.config["static_pth"] = "./simplestyle_8/"

    # views
    framework.register_views(Index(), "/", "main")
    framework.register_views(Contact(), "/contact/", "contact")
    framework.register_views(AnotherPage(), "/another_page/", "another_page")
    framework.register_views(Examples(), "/examples/", "examples")
    framework.register_views(Page(), "/page/", "page")

    # fronts
    framework.register_front(Date())
    framework.register_front(Urls())

    FrameWork.run_server(DEF_ADR, DEF_PORT)
