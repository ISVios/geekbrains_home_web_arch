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
from framework.types.types import ViewEnv, ViewResult
from framework.utils.patterns import SingleToneType
from framework.utils.decorators import debug, to_url

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
    sub_category: set | None

    def __init__(self, name, courses):
        self._index = Category.__ID
        Category.__ID += 1
        self.name = name
        self.courses = set()

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, _):
        # Todo: add  error logger
        pass

    def add_subcategory(self, category):
        if not self.sub_category:
            self.sub_category = set()

        self.sub_category.add(category)

    def add_course(self, course):
        self.courses.add(course)

    def count_course(self) -> int:
        return len(self.courses)

    def copy(self):
        return Category(self.name, [])

    def __str__(self) -> str:
        return f"Category[{self._index}]:{self.name}"

    def __repr__(self) -> str:
        return f"Category[{self._index}]:{self.name}"


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

    @abc.abstractmethod
    def course_type(self) -> str:
        return None

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, _):
        # Todo: add  error logger
        pass


class InteractiveCourse(Course):
    def course_type(self) -> str:
        return "Interactive"


class RecordsCourse(Course):
    def course_type(self) -> str:
        return "Record"


class MixCourse(Course):
    def course_type(self) -> str:
        return "Mix"


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
    @debug
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
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


# TEACHER
class TeacherAdd(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


class TeacherEdit(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


class TeacherDelete(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


class TeacherCopy(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


# STUDENT


class StudentAdd(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


class StudentEdit(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


class StudentDelete(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


class StudentCopy(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        pass


# COURSE


class CoursesList(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        view_env["courses"] = SiteApi().courses
        result.render_with_code(200, "courses_list.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class CourseItem(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.render_with_code(200, "courses_item.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class CoursesAdd(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        view_env["SiteLogic"] = SiteApi()
        view_env["category_list"] = SiteApi().category
        result.code = 400
        method = view_env[consts.ViewEnv_METHOD]
        args = view_env[consts.ViewEnv_ARGS]
        if method == "POST":
            course_type = args.get("course_type")
            course_name = args.get("course_name")
            course_category = args.get("category") or []
            course = None
            if course_type == "record":
                course = CourseFabric._create(
                    CourseFabric.Records, course_name, course_category
                )
            elif course_type == "interactive":
                course = CourseFabric._create(
                    CourseFabric.Interactive, course_name, course_category
                )

            if course:
                result.code = 200
                api = SiteApi()

                for category_index in course_category:
                    category = api.get_category_by_id(int(category_index))
                    if category:
                        category.add_course(course)

                SiteApi().courses.append(course)

            result.render_template("admin.html", "./simplestyle_8")
        elif method == "GET":
            result.render_with_code(200, "courses_add.html", "./simplestyle_8")


class CoursesEdit(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.render_with_code(200, "admin.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


class CoursesDelete(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.render_with_code(200, "admin.html", "./simplestyle_8")
        return super().view(view_env, config, result, **kwds)


# class CoursesForm(ViewType):
#     def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
#         result.render_with_code(200, "course_form.html", "./simplestyle_8")
#         return super().view(view_env, config, result, **kwds)


class CoursesCopy(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.render_with_code(200, "admin.html", "./simplestyle_8")


# CATEGORY


class CategoryAdd(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        method = view_env[consts.ViewEnv_METHOD]
        if method == "POST":
            category_name = view_env[consts.ViewEnv_ARGS].get("category_name")
            if category_name:
                category = Category(category_name, [])
                SiteApi().category.append(category)
                result.code = 200
            else:
                result.code = 400
            result.render_template("admin.html", "./simplestyle_8")
        elif method == "GET":
            result.render_with_code(200, "category_add.html", "./simplestyle_8")


class CategoryEdit(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        method = view_env[consts.ViewEnv_METHOD]
        index = int(view_env[consts.ViewEnv_ARGS].get("id") or "-1")
        category_list = SiteApi().category
        category = SiteApi().get_category_by_id(index)

        if method == "POST":
            if view_env.static_vars.get("category"):
                category = view_env.static_vars["category"]
                del view_env.static_vars["category"]

        if not category:
            result.render_with_code(400, "admin.html", "./simplestyle_8")
            return

        if method == "POST":
            category.name = view_env[consts.ViewEnv_ARGS].get("category_name")
            result.render_with_code(200, "admin.html", "./simplestyle_8")
            return
        elif method == "GET":
            view_env["category_name"] = category.name
            view_env.static_vars["category"] = category

            result.render_with_code(200, "category_add.html", "./simplestyle_8")


class CategoryCopy(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        index = int(view_env[consts.ViewEnv_ARGS].get("id"))
        category_list = SiteApi().category
        category = SiteApi().get_category_by_id(index)
        if category:
            copy = category.copy()
            copy.name += " (copy)"
            category_list.append(copy)

        result.render_with_code(200, "admin.html", "./simplestyle_8")


class CategoryDelete(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        index = int(view_env[consts.ViewEnv_ARGS].get("id"))
        category_list = SiteApi().category
        category = SiteApi().get_category_by_id(index)
        if category:
            category_list.remove(category)

        result.render_with_code(200, "admin.html", "./simplestyle_8")


class Contact(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
        result.code = 200
        result.render_template("contact.html", "./simplestyle_8")


@to_url("/test2", "test2")
@debug
def like_flask(view_env: ViewEnv, config: dict, result: ViewResult, **kwds):
    result.code = 200
    result.data = "view 'like' in flask"


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

    # TEACHER
    framework.register_views(TeacherAdd(), "/teachers/add/", "teachers_add")
    framework.register_views(TeacherEdit(), "/teachers/edit/", "teachers_edit")
    framework.register_views(TeacherDelete(), "/teachers/delete/", "teachers_delete")
    framework.register_views(TeacherCopy(), "/teacher/copy/", "teachers_copy")
    # STUDENT
    framework.register_views(StudentAdd(), "/students/add/", "students_add")
    framework.register_views(StudentEdit(), "/students/edit/", "students_edit")
    framework.register_views(StudentDelete(), "/students/delete/", "students_delete")
    framework.register_views(StudentCopy(), "/students/copy/", "students_copy")

    # CATEGORY
    framework.register_views(CategoryAdd(), "/category/add/", "category_add")
    framework.register_views(CategoryEdit(), "/category/edit/", "category_edit")
    framework.register_views(CategoryDelete(), "/category/delete/", "category_delete")
    framework.register_views(CategoryCopy(), "/category/copy/", "category_copy")

    # COURSES
    framework.register_views(CoursesList(), "/courses/", "courses_list")
    framework.register_views(CoursesAdd(), "/courses/add/", "courses_add")
    framework.register_views(CoursesCopy(), "/courses/copy/", "courses_copy")
    framework.register_views(CoursesEdit(), "/courses/edit/", "courses_edit")
    framework.register_views(CoursesDelete(), "/courses/delete/", "courses_delete")
    #
    # fronts
    # framework.register_front(Date())
    # framework.register_front(Urls())
    framework.register_front(SiteLogicFront())

    FrameWork.run_server(DEF_ADR, DEF_PORT)
