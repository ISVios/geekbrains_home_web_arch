#!/usr/bin/env python
"""
User script how use framework
"""
import abc
import argparse
import datetime
import logging
from copy import deepcopy
from enum import Enum

from framework import FrameWork, FrontType, SysEnv, ViewEnv, ViewResult, ViewType
from framework.types import consts
from framework.utils.patterns import SingleToneType

DEF_ADR = "0.0.0.0"
DEF_PORT = 8080


class User(abc.ABC):
    _first_name: str
    _second_name: str
    _patronymic: "str|None"
    _email: str
    _courses_id: set

    def first_name(self, first_name_: str):
        self._first_name = first_name_
        return self

    def second_name(self, second_name_: str):
        self._second_name = second_name_
        return self

    def patronymic(self, patronymic_: str):
        self._patronymic = patronymic_
        return self

    def email(self, email_: str):
        self._email = email_
        return self


class Student(User):
    course_index: set


class Teacher(User):
    pass


class UserFabric(Enum):
    STUDENT = Student
    TEACHER = Teacher

    @classmethod
    def _create(cls, type: "UserFabric"):
        return type.value()


class Category:
    __ID: int = 0
    _index: int
    name: str
    courses: set

    def __init__(self, name, courses):
        self._index = Category.__ID
        Category.__ID += 1
        self.name = name

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, _):
        # Todo: add  error logger
        pass

    def copy(self):
        return Category(self.name, [])

    def __str__(self) -> str:
        return f"Ctegory[{self._index}]:{self.name}"


class CourseBase:
    def copy(self):
        return deepcopy(self)


class Course(CourseBase, abc.ABC):
    __ID: int = 0
    _index: int
    category: set
    name: str

    def __init__(self, name: str, category: list):
        self._index = Course.__ID
        self.category = set()
        Course.__ID += 1
        self.name = name
        self.category.update(category)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, _):
        # Todo: add  error logger
        pass


class InteractiveCourse(Course):
    pass


class RecordsCourse(Course):
    pass


class MixCourse(Course):
    pass


class CourseFabric(Enum):
    Interactive = InteractiveCourse
    Records = RecordsCourse
    Mix = MixCourse

    @classmethod
    def _create(cls, type_: "CourseFabric", name: str, category: list):
        return type_.value(name, category)


class SiteApi(metaclass=SingleToneType):
    courses: list
    teachers: list
    students: list
    category: list

    def __init__(self) -> None:
        self.courses = []
        self.teachers = []
        self.students = []
        self.category = []

    @staticmethod
    def create_user(type_: UserFabric):
        UserFabric._create(type_)

    @staticmethod
    def create_course(type_: CourseFabric, name, category=[]):
        return CourseFabric._create(type_, name, category)

    @staticmethod
    def create_category(name: str):
        category = Category(name, [])
        return category

    def get_category_by_id(self, index):
        for elm in self.category:
            if elm.index == index:
                return elm
        return None


# urls
class Index(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        view_env.logger.critical("Hi from logger")
        result.render_with_code(200, "index.html", "./simplestyle_8")


class Login(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.render_with_code(200, "login.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class Admin(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        api = SiteApi()
        view_env["courses"] = api.courses
        view_env["categories"] = api.category
        view_env["students"] = api.students
        view_env["teachers"] = api.teachers
        result.render_with_code(200, "admin.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class Courses(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        view_env["courses"] = SiteApi().courses
        result.render_with_code(200, "courses.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class CourseItem(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.render_with_code(200, "course_item.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class CourseForm(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.render_with_code(200, "course_form.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class CoursesCopper(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        return super().view(view_env, config, result, **kwds)


class CategoryForm(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        if view_env[consts.ViewEnv_METHOD] == "POST":
            data = view_env[consts.ViewEnv_ARGS]
            if data:
                if data.get("action") == "create":
                    category = Category(data["category_name"], [])
                    SiteApi().category.append(category)
                elif data.get("action") == "edit":
                    category = SiteApi().get_category_by_id(int(data.get("id", -1)))
                    if category:
                        category.name = view_env[consts.ViewEnv_ARGS].get(
                            "category_name"
                        )

                result.render_with_code(200, "admin.html", "./simplestyle_8")
                return
        elif view_env[consts.ViewEnv_METHOD] == "GET":
            action = view_env[consts.ViewEnv_ARGS].get("action") or "create"
            view_env["action_text"] = action
            view_env[
                "action"
            ] = f"<input type='hidden' name='action' value='{action}' />"
            index = int(view_env[consts.ViewEnv_ARGS].get("id") or -1)
            category = SiteApi().get_category_by_id(index)
            if category:
                view_env["category_name"] = category.name

                view_env[
                    "id"
                ] = f"<input type='hidden' name='id' value='{category.index}' />"

                if view_env[consts.ViewEnv_ARGS].get("action") == "delete":
                    SiteApi().category.remove(category)

                    result.render_with_code(200, "admin.html", "./simplestyle_8")
                    return
                elif view_env[consts.ViewEnv_ARGS].get("action") == "copy":
                    copy_category = category.copy()
                    copy_category.name += " (copy)"
                    SiteApi().category.append(copy_category)
                    result.render_with_code(200, "admin.html", "./simplestyle_8")
                    return

        result.render_with_code(200, "category_form.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class Contact(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.code = 200
        result.render_template("contact.html", "./simplestyle_8")


# fronts


class SiteLogicFront(FrontType):
    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env["SiteLogic"] = SiteApi()
        return super().front_action(sys_env, view_env, config, **kwds)


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
    framework.register_views(Admin(), "/admin/", "admin")

    framework.register_views(Index(), "/", "main")
    framework.register_views(Contact(), "/contact/", "contact")
    framework.register_views(Login(), "/login/", "login")

    framework.register_views(Courses(), "/courses/", "courses")
    framework.register_views(CourseItem(), "/course_item/", "course_item")
    framework.register_views(CourseForm(), "/course_form/", "course_form")

    framework.register_views(CategoryForm(), "/category_form/", "category_form")

    # fronts
    # framework.register_front(Date())
    # framework.register_front(Urls())
    framework.register_front(SiteLogicFront())

    FrameWork.run_server(DEF_ADR, DEF_PORT)
