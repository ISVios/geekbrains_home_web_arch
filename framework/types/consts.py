import logging

# const
CONTENT_TYPE_HTML = "text/html"
CONTENT_TYPE_CSS = "text/css"
CONTENT_TYPE_PNG = "image/png"


# ViewEnv fields
ViewEnv_CUR_URL = "CurUrl"
ViewEnv_LOGGER = "LOGGER"
ViewEnv_ARGS = "Args"
ViewEnv_NAMESPAGEPAGE = "NameSpace"
ViewEnv_METHOD = "Method"

# ViewEnv Func name
ViewEnv_BREAKPOINT = "breakpoint"
ViewEnv_STATIC = "static"

# SysEnv

# config fields
DEBUG = "debug"
CNFG_LOGGER_LEVEL = "logger_level"
CNFG_CUSTOM_LOGGER = "custom_logger"
CNFG_STATIC_PTH = "static_pth"
CNFG_STATIC_MEDIA_FLG = "custom_media_flg"

# config value
DEFAULT_CNFG_STATIC_MEDIA_FLG_VALUE = "__static__"
DEFAULT_CNFG_LOGGER_LEVEL = logging.INFO
DEFAULT_CNFG_STATIC_FOLDER = "./template"
DEFAULT_CNFG_VIEW_TYPE = CONTENT_TYPE_HTML
