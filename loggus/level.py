# coding: utf-8
import logging

# level
DEBUG: int = logging.DEBUG
INFO: int = logging.INFO
WARNING: int = logging.WARNING
ERROR: int = logging.ERROR
PANIC: int = logging.FATAL
# level color
DEBUG_COLOR: str = "\033[1;37m{}\033[0m"
INFO_COLOR: str = "\033[1;32m{}\033[0m"
WARNING_COLOR: str = "\033[1;33m{}\033[0m"
ERROR_COLOR: str = "\033[1;31m{}\033[0m"
PANIC_COLOR: str = "\033[1;36m{}\033[0m"
# level map
LEVEL_MAP: dict = {
    DEBUG: "debug",
    INFO: "info",
    WARNING: "warning",
    ERROR: "error",
    PANIC: "panic",
}
# color map
COLOR_LEVEL_MAP: dict = {
    DEBUG: DEBUG_COLOR.format(LEVEL_MAP[DEBUG]),
    INFO: INFO_COLOR.format(LEVEL_MAP[INFO]),
    WARNING: WARNING_COLOR.format(LEVEL_MAP[WARNING]),
    ERROR: ERROR_COLOR.format(LEVEL_MAP[ERROR]),
    PANIC: PANIC_COLOR.format(LEVEL_MAP[PANIC]),
}
