# geekbrains_home_web_arch

Home for web arch

How init server

```python
    from framework import FrameWork

    framework = FrameWork.get_framework()
```

How run server

```python
    framework.run_server(`ip-adress`, `port`) # block function → must be last
```

How create new view

```python
from framework.views.view_type import View

class Index(View):
    def __call__(self, responce) -> tuple[int, str]:
        return 200, "OK"
```

How add new view

```python

    framework = FrameWork.get_framework()
    ...
    framework.register_views(Index(), `urls`, `namespace`)
    # namespace - need for use jinja function `router` {{ router(`namespace`) }}
    ...
    framework.run_server(`ip-adress`, `port`)

```

How create new front

```python
class Index:
    def __call__(self, responce) -> tuple[int, str]:
        return 200, "OK"
```

full example in file 'run.py'
