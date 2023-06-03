"""
ViewEnv struct:
    CurUrl - current url
    HostUrl -  current host url
    ARGS - parsed url args like ?x=1&y=2&z=0
    NextCurUrl - change CurUrl in next loop (one way)
    NextNameSpace - change CurUrl from NameSpace in next loop (one way)
    RouterArgs - args of router func


"""
import datetime
import logging
import re

UrlTreeRe = re.compile(r"^\<(?P<var>[^:]*)(:(?P<type>.*))?\>$")


def Redirect_URL(url: str, wait_sec: int = 0):
    return f"""<meta http-equiv="refresh" content="{wait_sec}; url='{url}'" />"""


# const
CONTENT_TYPE_HTML = "text/html"
CONTENT_TYPE_CSS = "text/css"
CONTENT_TYPE_PNG = "image/png"


# ViewEnv fields
ViewEnv_CUR_URL = "CurUrl"
ViewEnv_HOST_URL = "HostUrl"
ViewEnv_LOGGER = "Logger"
ViewEnv_ARGS = "Args"
ViewEnv_URL_PARAM = "UrlParam"
ViewEnv_NAMESPAGEPAGE = "NameSpace"
ViewEnv_METHOD = "Method"
ViewEnv_StaticVar = "StaticVar"

# ViewEnv Func name
ViewEnv_BREAKPOINT = "breakpoint"
ViewEnv_STATIC = "static"

# SysEnv

# config fields
DEBUG = "debug"
KEY = "__key__"
CNFG_VIEWENV_DEBUG = "debug_print_viewenv"
CNFG_SYSENV_DEBUG = "debug_print_sysenv"
CNFG_LOGGER_LEVEL = "logger_level"
CNFG_CUSTOM_LOGGER = "custom_logger"
CNFG_CUSTOM_USER_MODEL = "custom_client_model"
CNFG_STATIC_PTH = "static_pth"
CNFG_STATIC_MEDIA_FLG = "custom_media_flg"
CNFG_CLIENT_PROBE = "custom_client_probe"

# config value
DEFAULT_CNFG_STATIC_MEDIA_FLG_VALUE = "__static__"
DEFAULT_CNFG_LOGGER_LEVEL = logging.INFO
DEFAULT_CNFG_STATIC_PTH = "./template"
DEFAULT_CNFG_VIEW_TYPE = CONTENT_TYPE_HTML
DEFAULT_CNFG_CLIENT_PROBE = datetime.timedelta(hours=1)
DEFAULT_CNFG_CLIENT_MODEL = None

# urs regex parser
DEFAULT_CNFG_URL_PARSER = re.compile("")
