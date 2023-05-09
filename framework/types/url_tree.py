"""

"""
from re import T
from typing import Type, Any
import unittest
import abc
from framework.types import consts
from framework.types import ViewType, ViewEnv


class UrlNodeProto(abc.ABC):
    _namespace: str | None
    _view: ViewType | None
    _childrens: set["UrlNodeProto"]
    _url: str | None

    def __init__(self):
        self._view = None
        self._namespace = None
        self._url = None

    def add_node(self, node):
        if not hasattr(self, "_childrens"):
            self._childrens = set()

        self._childrens.add(node)

    @property
    def namespace(self) -> str | None:
        return self._namespace

    @namespace.setter
    def namespace(self, value: str):
        if self._namespace:
            raise NotImplementedError("try change exist namespace for url")

        self._namespace = value

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        if self._view:
            raise NotImplementedError("try change exist view for url")

        self._view = value

    def get_childrens(self) -> list["UrlNodeProto"]:
        if not hasattr(self, "_childrens"):
            return []
        return list(self._childrens)

    def get_all_urls(self):

        if not hasattr(self, "_childrens"):
            return []
        return [[ch._url, *ch.get_all_urls()] for ch in self._childrens]


class UrlNode(UrlNodeProto):
    def __repr__(self):
        return f"UrlNode {self._url}:{self._namespace}"


class UrlNodeVar(UrlNodeProto):
    type_: Type

    def __repr__(self):
        return f"UrlVar {self._url} {self.type_}:{self._namespace}"


class UrlNodeStr(UrlNodeVar):
    pass


class UrlNodeInt(UrlNodeVar):
    pass


class UrlNodeBuilder:
    @staticmethod
    def create_node(url_part: str):
        # if var
        url_parse = consts.UrlTreeRe.fullmatch(url_part)
        node = None
        if not url_parse:
            node = UrlNode()
            node._url = url_part
            return node

        url_parse = url_parse.groupdict()

        if url_parse.get("type") == "int":
            node = UrlNodeInt()
            node.type_ = int
        else:
            node = UrlNodeStr()
            node.type_ = str

        node._url = "<" + (url_parse.get("var") or "") + ">"
        return node


class UrlTree:
    __namespaces = {}
    __vars = set()
    _root: UrlNode
    # root_namespace: str

    def __init__(self) -> None:
        self._root = UrlNode()

    def _node_by_url(self, url: str, view_env: ViewEnv):
        return self._go_to_node(url, view_env)

    def _node_by_namespace(self, namespace: str):
        return UrlTree.__namespaces.get(namespace, None)

    def view_by_url(self, url: str, view_env: ViewEnv):
        node = self._node_by_url(url, view_env)
        if node and node.view:
            return node.view

    def view_by_namespace(self, namespace: str):
        node = self._node_by_namespace(namespace)
        if node and node.view:
            return node.view

    def _go_to_node(self, url, view_env: ViewEnv | None, create_node: bool = False) -> UrlNodeProto | None:
        # cut &* (url parm)
        url_ = url.split("&")[0]

        # del first and last /
        if url_[-1] == "/":
            url_ = url_[:-1]

        if len(url_) > 0 and url_[0] == "/":
            url_ = url_[1:]

        url_str_lst = url_.strip().split("/")

        cur_node = self._root

        # only "/" -> root
        if len(url_str_lst) == 1 and url_str_lst[0] == "":
            self._root._url = "/"
            return self._root

        for url_ch in url_str_lst:
            if url_ch == "":
                raise NotImplementedError("dup //")
            # if node if exist
            find_exist = None
            for ch in cur_node.get_childrens():
                ch_type = type(ch)
                if ch_type is UrlNode:
                    if ch._url == url_ch:
                        find_exist = ch
                        break
                elif ch_type is UrlNodeInt:
                    print(ch_type is UrlNodeVar)
                    try:
                        covert = int(url_ch)
                        if view_env:
                            if not ch._url in view_env[consts.ViewEnv_ARGS]:
                                view_env[consts.ViewEnv_ARGS][ch._url] = covert
                                raise NotImplementedError("dup url args name")
                        print(f"add {ch._url} = {url_ch} to URL_ARGS")
                        find_exist = ch
                        break
                    except ValueError as ve:
                        pass
                    except Exception as ex:
                        raise ex
                elif ch_type is UrlNodeStr:
                    print(f"add {ch._url} = {url_ch} to URL_ARGS")
                    if view_env:
                        view_env[consts.ViewEnv_ARGS][ch._url] = url_ch
                    find_exist = ch
                    break

            if not find_exist:
                if create_node:
                    new_node = UrlNodeBuilder.create_node(url_ch)
                    cur_node.add_node(new_node)
                    cur_node = new_node
                else:
                    return None
            else:
                cur_node = find_exist

        return cur_node

    def register_views(self, view: ViewType, url: str, namespace: str):

        # namespace is exist
        if namespace in UrlTree.__namespaces:
            raise NotImplementedError("dup namespace")

        node = self._go_to_node(url, None, True)

        if node:
            node.namespace = namespace
            node.view = view

            UrlTree.__namespaces[namespace] = node

    def urls(self):

        return self._root.get_all_urls()
