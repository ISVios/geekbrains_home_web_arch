from abc import ABC, abstractclassmethod


# ToDo: Convert to metaclass
class View(ABC):
    # namespace
    # url
    # method {get. post}
    @abstractclassmethod
    def __call__(self, *args, **kwds) -> tuple[int, str]:
        raise NotImplemented


class NoFoundPage(View):
    def __call__(self, *args, **kwds) -> tuple[int, str]:
        return 400, "Page no found"


# return file if Static
class StaticFile(View):
    raise NotImplemented
