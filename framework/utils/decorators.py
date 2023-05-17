import timeit
from framework import FrameWork
from framework.views.view import FuncView


def to_url(url: str, namespace: str):
    def _func(func):
        framework = FrameWork()
        new_view = FuncView(func)
        framework.register_views(new_view, url, namespace)
        return func

    return _func


# ToDo: conver print to logger
def debug(_func):
    def wrap(*args, **kwds):
        start_tm = timeit.timeit()
        result = _func(*args, **kwds)
        func_time = timeit.timeit() - start_tm
        print(f"{_func.__name__}: {func_time}")
        return result

    return wrap
