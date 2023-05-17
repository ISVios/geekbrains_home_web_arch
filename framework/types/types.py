import abc
import datetime
from datetime import time
from logging import Logger

import bcrypt

from framework.types import consts
from framework.utils.render import render


class TypedDict:
    __slots__ = ["__typed_dict", "__const"]
    __typed_dict: dict
    __const: bool

    def make_const(self):
        self.__const = True

    def _no_const(self):
        self.__const = False

    def to_dict(self) -> dict:
        return self.__typed_dict

    def __iter__(self):
        return self.__typed_dict.__iter__()

    def get(self, __name: str, no_key_found=None):
        if not __name in self.__typed_dict:
            return no_key_found
        return self.__typed_dict[__name]

    def __init__(self, base: "dict|None" = None, is_const: bool = False) -> None:
        self.__typed_dict = base or {}
        self.__const = is_const

    def __getitem__(self, __name: str):
        return self.__typed_dict[__name]

    def __setitem__(self, __name: str, __value):
        if not self.__const:
            self.__typed_dict[__name] = __value

    def has_key(self, k):
        return k in self.__dict__

    def __str__(self) -> str:
        return "TypedDict"


class SysEnv(TypedDict):
    pass


class ViewEnv(TypedDict):
    @property
    def logger(self) -> "Logger":
        return self[consts.ViewEnv_LOGGER]

    @property
    def static_vars(self) -> dict:
        return self[consts.ViewEnv_StaticVar]

    @property
    def user(self):
        return self["__ClientAuth__"]  # ToDo: make const

    @property
    def users(self):
        return self.static_vars["__ClientList__"]

    @property
    def http_method(self):
        return self[consts.ViewEnv_METHOD]

    @property
    def url_args(self):
        return self[consts.ViewEnv_ARGS]

    @property
    def url_param(self):
        return self[consts.ViewEnv_URL_PARAM]


##
class FrontType(abc.ABC):
    def init(self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds):
        pass

    def __call__(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        return self.front_action(sys_env, view_env, config, **kwds)

    @abc.abstractmethod
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        return view_env


##
class ViewResult:
    result: dict
    env: ViewEnv

    def __init__(self, env: ViewEnv) -> None:
        self.env = env
        self.result = {}
        self.result["code"] = -1  # special
        self.result["data"] = ""
        self.result["data_type"] = consts.DEFAULT_CNFG_VIEW_TYPE
        self.result["text"] = True

    def __call__(self, code: int, data, data_type: str = consts.DEFAULT_CNFG_VIEW_TYPE):
        self.code = code
        self.data = data
        self.data_type = data_type

    @property
    def code(self):
        return self.result["code"]

    @code.setter
    def code(self, value: int):
        self.result["code"] = value

    @property
    def data(self):
        return self.result["data"]

    @data.setter
    def data(self, value):
        self.result["data"] = value

    @property
    def data_type(self):
        return self.result["data_type"]

    @data_type.setter
    def data_type(self, value):
        self.result["data_type"] = value

    @property
    def is_text(self):
        return self.result["text"]

    @is_text.setter
    def is_text(self, value):
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
        self.data = render(template_name, folder, **self.env.to_dict())

    def render_with_code(self, code: int, template_name: str, folder: str):
        self.code = code
        self.data = render(template_name, folder, **self.env.to_dict())

    # ToDo
    def redirect_to_url(self, url: str, wait_sec: int = 0):
        self.code = 200
        self.data = f"""<script>window.location.replace("{url}");</script>"""

    # ToDo
    def redirect_to_namespace(self, namespace, *argv, **kwds):
        url = self.env[consts.ViewEnv_NAMESPAGEPAGE][namespace]
        self.code = 200
        self.data = f"""<script>window.location.replace("{url}");</script>"""


##
# ToDo: add OnlyGetView interface
class ViewType:
    def __call__(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        self.view(view_env, config, result, **kwds)

    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


# AuthType

# No auth type
# None - no init Auth
# Anon - only ip


# auth type
# LoginPass - and login pass(hash)
# Token -> LoginPass  (convert)
# Other -> LoginPass
class AuthBy(metaclass=abc.ABCMeta):
    def probe_over(self):
        return False

    @abc.abstractproperty
    def login(self):
        return " "

    @abc.abstractmethod
    def is_valid(self) -> bool:
        return False

    @abc.abstractmethod
    def is_auth(self) -> bool:
        return False


class ByAnon(AuthBy):
    @property
    def login(self):
        return " "

    def is_valid(self) -> bool:
        return True

    def is_auth(self) -> bool:
        return False


class ByLoginPass(AuthBy):
    time: datetime.datetime

    def __init__(self, login, passwd: str, key="") -> None:
        self.__login = login
        salt = bcrypt.gensalt()
        self.__passwd = bcrypt.hashpw(passwd.encode(), salt)
        super().__init__()

    @property
    def login(self):
        return self.__login

    def is_auth(self) -> bool:
        return True

    def is_valid(self, passwd: str) -> bool:
        return bcrypt.checkpw(passwd.encode(), self.__passwd)

    def probe_over(self):
        return self.time + datetime.timedelta(hours=1) < datetime.datetime.now()


class ClientControl(TypedDict):
    def __init__(self) -> None:
        super().__init__({}, False)
        self["auth"] = None
        self["prop"] = {}

    @property
    def login(self):
        auth = self["auth"]
        if not auth:
            return " "
        return auth.login

    def _update(self):
        # update probe
        pass

    def auth(self, auth_by: AuthBy):
        self["auth"] = auth_by

    def add_prop(self, name: str, value):
        # like email
        # or class have email
        self["prop"][name] = value

    def get_prop(self, name: str):
        return self["prop"][name]

    def is_auth(self):
        if not self["auth"]:
            return False
        return self["auth"].is_auth()

    def __str__(self) -> str:
        return f"ClientControl({self['auth']})"

    def __repr__(self):
        return f"ClientControl({self['auth']})"


if __name__ == "__main__":
    # add UnitTest
    pass
