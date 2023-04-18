#!/usr/bin/env python
"""
User script how use framework
"""
import argparse
import datetime
import logging

from framework import FrameWork, SysEnv, ViewEnv, FrontType, ViewType, ViewResult

DEF_ADR = "0.0.0.0"
DEF_PORT = 8080


# urls
class Index(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        view_env.logger.critical("Hi from logger")
        result.render_with_code(200, "index.html", "./simplestyle_8")


class Contact(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.code = 200
        result.render_template("contact.html", "./simplestyle_8")


class AnotherPage(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.code = 200
        result.render_template("another_page.html", "./simplestyle_8")


class Examples(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.code = 200
        result.render_template("examples.html", "./simplestyle_8")


class Page(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.code = 200
        result.render_template("page.html", "./simplestyle_8")


# fronts
class Date(FrontType):
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env["date"] = datetime.datetime.now()
        return view_env


class Urls(FrontType):
    def front_action(self, sys_env: dict, view_env: dict, config: dict, **kwds) -> dict:
        view_env["urls"] = FrameWork.get_framework().get_register_urls()
        return view_env


if __name__ == "__main__":
    # ToDo: add argparse
    framework = FrameWork.get_framework()

    # config
    framework.config["debug"] = True
    framework.config["adr"] = DEF_ADR
    framework.config["port"] = DEF_PORT
    framework.config["static_pth"] = "./simplestyle_8/"
    framework.config["logger_level"] = logging.INFO

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
