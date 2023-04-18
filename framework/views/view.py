import os
import pathlib

from framework.types import ViewEnv, ViewResult, ViewType, consts


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

        if file_pth[0] == "/":
            file_pth = file_pth[1:]

        file_pth = pathlib.Path(config[consts.CNFG_STATIC_PTH]) / file_pth
        # Think: how protect system file
        result.is_text = True
        if not os.path.isfile(file_pth):
            view_env.logger.debug("file no found")
            result.code = 400
            return
        file_type = file_pth.suffix

        if file_type == ".png":
            result.data_type = consts.CONTENT_TYPE_PNG
            result.code = 200
            result.is_text = False
            with open(file_pth, "rb") as data:
                result.data = data.read()
            return

        elif file_type == ".css":
            result.data_type = consts.CONTENT_TYPE_CSS
            result.code = 200
            with open(file_pth, "r", encoding="utf-8") as text:
                result.data = text.read()
            return

        view_env.logger.debug("No support Type File")
        result.code = 400
