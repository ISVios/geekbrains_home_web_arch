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
from framework.types import ViewType, ViewEnv, ViewResult

class Index(ViewType):
    def view(self, view_env: ViewEnv, config: dict, result: ViewResult):
        """
        view_env
        config
        result
        """
        result.code = 200
        result.text = "OK"
        result.render_template("index.html", "path_to_index.html")
        # In next version will be:  result(200, "OK")
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
from framework import FrontType
class MyFront(FrontType):
    # [fields if need]

    # def __init__(self, ....) # init some fields if need

    def front_action(self, 
        sys_env: SysEnv, # system envaroment 
        view_env:ViewEnv, # envaroment which see views 
        config:dict,      # user custom config 
        **kwds) -> ViewEnv:
            # can use init fields 
            # please don`t mix sys_env with view_type 
            #   like view_type["some_key"] = sys_env 
            return view_env
```

How add new front

```python

    framework = FrameWork.get_framework()
    ...
    framework.register_front(MyFront())
    # namespace - need for use jinja function `router` {{ router(`namespace`) }}
    ...
    framework.run_server(`ip-adress`, `port`)

```

How RUN example file 'run.py'

[use poetry](https://python-poetry.org):

```bash
    poetry run python run.py
```

or

```bash
    poetry shell
    python run.py
```
