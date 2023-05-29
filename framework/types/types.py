import abc
import datetime
from datetime import time
from logging import Logger
from typing import Type

import bcrypt

from threading import local

from jinja2 import clear_caches
from framework.types import consts
from framework.utils.patterns import SingleToneType
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


# ToDo merge with db client
class ClientControl(TypedDict):
    __ID: int = 0

    def __init__(self) -> None:
        super().__init__({}, False)
        self["auth"] = None
        self["prop"] = {}
        # self["db_model"] = None

        self.add_prop("probe", datetime.datetime.now())
        self.add_prop("id", ClientControl.__ID)
        ClientControl.__ID += 1

    @property
    def login(self):
        auth = self["auth"]
        if not auth:
            return " "
        return auth.login

    @property
    def index(self):
        return self.get_prop("id")

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


class MapperRegistry:
    mappers = {}

    @staticmethod
    def get_mapper(obj):
        for _, v in MapperRegistry.mappers.items():
            if isinstance(obj, v["class_type"]):
                return v["mapper"]  # (connection)
        raise ValueError("mapper no found")

    @staticmethod
    def get_current_mapper(name) -> dict:
        return MapperRegistry.mappers[name]  # (connection)


class Session:
    """Unit of Work"""

    local = local()

    cache_obj: dict = {}

    create_obj: list
    change_obj: list
    delete_obj: list

    def __init__(self, connect) -> None:
        self.connect = connect
        self.create_obj = []
        self.change_obj = []
        self.delete_obj = []

    def set_mapper(self, mapper_cls):
        self.mapper = mapper_cls

    def register_new(self, obj):
        self.create_obj.append(obj)

    def register_change(self, obj):
        self.change_obj.append(obj)

    def register_delete(self, obj):
        self.delete_obj.append(obj)

    def commit(self):
        self._create_objs()
        self._change_objs()
        self._delete_objs()

        self.change_obj.clear()
        self.delete_obj.clear()
        self.create_obj.clear()

    def _create_objs(self):
        for obj in self.create_obj:
            mapper = MapperRegistry.get_mapper(obj)
            if not mapper:
                raise NotImplementedError
            mapper.insert(obj)

    def _change_objs(self):
        for obj in self.change_obj:
            mapper = MapperRegistry.get_mapper(obj)
            if not mapper:
                raise NotImplementedError
            mapper.update(obj)

    def _delete_objs(self):
        for obj in self.delete_obj:
            mapper = MapperRegistry.get_mapper(obj)
            if not mapper:
                raise NotImplementedError
            mapper.delete(obj)

    def _drop_all(self, cls):
        class_type_and_mapper_dict = MapperRegistry.get_current_mapper(cls.tablename)
        if not class_type_and_mapper_dict:
            raise NotImplementedError
        class_type_and_mapper_dict["mapper"]._drop_all()

    @staticmethod
    def new_session(connect):
        __class__.set_current(Session(connect))

    @classmethod
    def set_current(cls, session):
        cls.local.session = session

    @classmethod
    def get_current(cls):
        return cls.local.session

    @classmethod
    def add_to_cache(cls, obj):
        typed_cache = cls.cache_obj.get(obj.__class__, {})
        if not obj.id in typed_cache:
            typed_cache[obj.id] = obj

        cls.cache_obj[obj.__class__] = typed_cache

    @classmethod
    def get_from_cache(cls, _class_, id):
        if not _class_ in cls.cache_obj:
            return None
        return cls.change_obj[_class_].get(id, None)

    @classmethod
    def clear_from_cache(cls, obj):
        typed = cls.cache_obj.get(obj.__class__)

        if not typed:
            return

        if typed.get(obj.id):
            del typed[obj.id]

    @classmethod
    def clear_cache_type(cls, _type):
        typed = cls.cache_obj.get(_type)

        if typed:
            del typed


class Mapper:
    def __init__(self, connection, _tablename, cls):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = _tablename
        self.cls = cls
        MapperRegistry.mappers[_tablename] = {"class_type": cls, "mapper": self}

    def all(self, _fields={}):
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        headers = list(map(lambda x: x[0], self.cursor.description))
        for item in self.cursor:
            args = dict((zip(headers, item)))
            instance = self.cls(**args)
            result.append(instance)
            Session.add_to_cache(instance)
        return result

    def find_by_id(self, id, _fields="*"):
        cached_obj = Session.get_from_cache(self.__class__, id)
        if cached_obj:
            return cached_obj

        statement = f"SELECT {_fields} FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return self.cls(*result)
        else:
            return None
            # raise ValueError(f"record with id={id} not found")

    def insert(self, obj, _fields=set()):
        values_palace = ("?," * len(_fields))[:-1]
        statement = f"INSERT INTO {self.tablename} {_fields} VALUES ({values_palace})"
        values = tuple(map(lambda f: getattr(obj, f), _fields))
        self.cursor.execute(statement, values)
        try:
            self.connection.commit()
            # set
            obj.id = self.cursor.lastrowid
            Session.add_to_cache(obj)
        except Exception as e:
            raise ValueError(e.args)

    def update(self, obj, _fields_dict={}):
        update_value = ""

        val = []
        for k, v in _fields_dict.items():
            update_value += f"{k} = ?, "
            val.append(v)

        update_value = update_value[:-2]

        statement = f"UPDATE {self.tablename} SET {update_value} WHERE id=?"

        self.cursor.execute(statement, (*val, obj.id))
        try:
            self.connection.commit()
            Session.add_to_cache(obj)
        except Exception as e:
            raise ValueError(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
            Session.clear_from_cache(obj)
        except Exception as e:
            raise ValueError(e.args)

    def _drop_all(
        self,
    ):
        """Alert"""
        statement = f"DELETE FROM {self.tablename} WHERE id"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
            Session.clear_cache_type(self.cls)
        except Exception as e:
            raise ValueError(e.args)


class DbModel:
    tablename: str = ""

    def mark_new(self):
        Session.get_current().register_new(self)

    def mark_change(self):
        Session.get_current().register_change(self)

    def make_delete(self):
        Session.get_current().register_delete(self)

    @classmethod
    def all(cls):
        return MapperRegistry.get_current_mapper(cls.tablename)["mapper"].all()

    @classmethod
    def by_id(cls, _id: int):
        return MapperRegistry.get_current_mapper(cls.tablename)["mapper"].find_by_id(
            _id
        )

    def __delete__(self):
        self.make_delete()


if __name__ == "__main__":
    # add UnitTest
    pass
