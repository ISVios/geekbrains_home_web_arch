from abc import ABC, abstractclassmethod


class View(ABC):
    @abstractclassmethod
    def __call__(self, *args, **kwds) -> tuple[int, str]:
        raise NotImplemented


class NoFoundPage(View):
    def __call__(self, *args, **kwds) -> tuple[int, str]:
        return 400, "Page no found"


# def as_view()
