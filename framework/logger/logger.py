import logging
from framework.types import consts

from framework.types.types import FrontType, SysEnv, ViewEnv, ViewResult


class LoggerFront(FrontType):
    logger: logging.Logger

    def __init__(
        self, level: int = logging.DEBUG, custom_logger: "logging.Logger|None" = None
    ) -> None:
        self.logger = custom_logger or logging.getLogger("FrameWork")
        # no config if custom_logger
        if custom_logger:
            return
        logging.root.setLevel(0)
        cli = logging.StreamHandler()
        self.logger.addHandler(cli)
        self.logger.setLevel(level)

    def front_action(
        self, sys_env: SysEnv, view_env: ViewEnv, config: dict, **kwds
    ) -> ViewEnv:
        view_env[consts.ViewEnv_LOGGER] = self.logger
        return view_env
