import abc
from logging import Logger

from framework.utils.render import render


class TypedDict:
    __typed_dict: dict

    def to_dict(self) -> dict:
        return self.__typed_dict

    def get(self, __name: str, no_key_found=None):
        if not __name in self.__typed_dict:
            return no_key_found
        return self.__typed_dict[__name]

    def __init__(self, base: "dict|None" = None) -> None:
        self.__typed_dict = base or {}

    def __getitem__(self, __name: str):
        return self.__typed_dict[__name]

    def __setitem__(self, __name: str, __value):
        self.__typed_dict[__name] = __value


class SysEnv(TypedDict):
    pass


class ViewEnv(TypedDict):
    @property
    def logger(self) -> "Logger":
        return self["Logger"]


##
class FrontType(abc.ABC):
    def __call__(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        return self.front_action(sys_env, view_env, config, **kwds)

    @abc.abstractmethod
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        raise NotImplemented


##
class ViewResult:
    result: dict
    env: ViewEnv

    def __init__(self, env: ViewEnv) -> None:
        self.env = env
        self.result = {}
        self.result["code"] = -1
        self.result["text"] = ""

    def __call__(self, code: int, text: str):
        self.code = code
        self.text = text

    @property
    def code(self):
        return self.result["code"]

    @code.setter
    def code(self, value: int):
        self.result["code"] = value

    @property
    def text(self):
        return self.result["text"]

    @text.setter
    def text(self, value):
        self.result["text"] = value

    def render_template(
        self,
        template_name: str,
        folder: str,  # by_namespace: "str|None" = None, by_path: "str|None" = None
        code: "int|None" = None,
        # custom_args: "dict|None"=None
    ):
        if code:
            self.code = code
        self.text = render(template_name, folder, **self.env.to_dict())

    def render_with_code(self, code: int, template_name: str, folder: str):
        self.code = code
        self.text = render(template_name, folder, **self.env.to_dict())


##
class ViewType:
    def __call__(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        if hasattr(self, "__meta__"):
            print(getattr(self, "__meta__"))

        else:
            self.view(view_env, config, result, **kwds)

    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass

    def only_get(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass

    def only_head(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass

    def only_post(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass

    def only_put(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass

    def only_options(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass

    def only_pathc(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass

    def only_connect(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass

    def only_delete(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


if __name__ == "__main__":
    # add UnitTest
    pass
