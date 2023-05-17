import timeit
from framework import FrameWork
from framework.views.view import FuncView


def need_auth(
    redirect_to_url: str | None = None, redirect_to_namespace: str | None = None
):
    def _func(func):
        def wrap(self, view_env, config, result, **kwds):
            if not view_env.user.is_auth():
                if redirect_to_url:
                    result.redirect_to_url(redirect_to_url)
                elif redirect_to_namespace:
                    result.redirect_to_namespace(redirect_to_namespace)
                else:
                    raise NotImplementedError
                    pass  # Think
                return None
            func_res = func(self, view_env, config, result, **kwds)

            return func_res

        return wrap

    return _func


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
