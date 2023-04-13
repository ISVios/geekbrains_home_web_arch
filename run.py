#!/usr/bin/env python

"""
Main script
"""
import argparse
import datetime


from framework import FrameWork
from framework.utils.render import render
from framework.views.view_type import View

DEF_ADR = "0.0.0.0"
DEF_PORT = 8080


class Contact(View):
    def __call__(self, response) -> tuple[int, str]:
        return 200, render("contact.html", "./simplestyle_8/")


class Index(View):
    def __call__(self, response) -> tuple[int, str]:
        return 200, render("index.html", "./simplestyle_8/")


class Date:
    def __call__(self, response):
        response["date"] = datetime.datetime.now()
        return response


class Urls:
    def __call__(self, response):
        response["urls"] = FrameWork.get_framework().get_register_urls()
        return response


if __name__ == "__main__":
    # add argparse
    framework = FrameWork.get_framework()

    # views
    framework.register_views(Index(), "/")
    framework.register_views(Contact(), "/contact/")

    # fronts
    framework.register_front(Date())
    framework.register_front(Urls())

    FrameWork.run_server(DEF_ADR, DEF_PORT)
