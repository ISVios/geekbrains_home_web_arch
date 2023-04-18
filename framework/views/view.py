from framework.types import ViewType, ViewEnv, ViewResult


class NoFoundPage(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.code = 400
        result.text = "NoFoundPage"


class ErrorMessage(ViewType):
    err_msg: str

    def __init__(self, msg) -> None:
        self.err_msg = msg

    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.code = 400
        result.text = self.err_msg


# return file if Static
class StaticFile(ViewType):
    pass
