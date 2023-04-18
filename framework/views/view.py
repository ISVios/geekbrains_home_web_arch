import os
import pathlib

from framework.types import ViewEnv, ViewResult, ViewType
from framework.types.consts import CONTENT_TYPE_CSS, CONTENT_TYPE_PNG


class NoFoundPage(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result(400, "<h1>Page NoFoundPage<h1>")


class ErrorMessage(ViewType):
    err_msg: str

    def __init__(self, msg) -> None:
        self.err_msg = msg

    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result(400, self.err_msg)


# return file if Static
class MediaStaicFileView(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        file_pth = view_env["File"]
        result.is_text = True
        if not os.path.isfile(file_pth):
            result.code = 400
            return

        file_type = pathlib.Path(file_pth).suffix

        if file_type == ".png":
            result.data_type = CONTENT_TYPE_PNG
            result.code = 200
            result.is_text = False
            with open(file_pth, "rb") as data:
                result.data = data.read()
            return

        elif file_type == ".css":
            result.data_type = CONTENT_TYPE_CSS
            result.code = 200
            with open(file_pth, "r", encoding="utf-8") as text:
                result.data = text.read()
            return

        result.code = 400
