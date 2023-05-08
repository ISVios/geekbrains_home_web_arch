"""

"""

from os import name
from framework.types import consts

from typing import Any, Type


# class UrlNodeProto:
#     childrens: set["UrlNodeProto"]
#     # url: "Any"
#     # namespace: str | None
#
#     def create(self, url_lst:list[str]):
#
#
#     def add_childern(self, node: "UrlNodeProto"):
#         self.childrens.add(node)
#
#     def get_all_childrens(self) -> list["UrlNodeProto"]:
#         return list(self.childrens)
#
#     def find(self, url_str_lst: list[str]) -> "UrlNodeProto|None":
#         # get url_str_lst[0]
#         # find in childrens
#         # if find return
#         return None
#
#
# class UrlNode(UrlNodeProto):
#
#     def __init__(self, url: str, namespace: str | None = None) -> None:
#         self.url = url
#         self.namespace = namespace
#
#
# class UrlVar(UrlNodeProto):
#     name: str
#     type_: Type
#
#     def __init__(self, var_name: str, var_type: Type = str, namespace: str | None = None) -> None:
#         self.name = var_name
#         self.type_ = var_type
#         self.namespace = namespace
#
#
# class UrlTreeNodeFabric:
#
#     @staticmethod
#     def create(url_elm: str, namespace: str | None = None) -> "UrlNodeProto":
#         re_url = consts.UrlTreeRe.search(url_elm)
#         if not re_url:
#             return UrlNode(url_elm, None)
#
#         re_url = re_url.groupdict()
#
#         return UrlVar(re_url["var"], re_url.get("type", "str"), namespace)
#
#
# class UrlTree:
#     __used_urls: set[str]
#     __namespace: dict[str, UrlNodeProto]
#     childrens: set[UrlNode]
#
#     def __init__(self) -> None:
#         UrlTree.__used_urls = set()
#         UrlTree.__namespace = {}
#
#     def register_views(self, view: ViewType, url: str, namespace: str):
#         # cut param url if exitst
#         url_ = url.split("?")[0]
#
#         url_lst = url.strip().split("/")
#
#         pass
