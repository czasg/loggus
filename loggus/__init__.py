# coding: utf-8
__author__ = "https://github.com/CzaOrz"
__version__ = "0.0.12"

import re
import sys
import json
import logging
import traceback

from typing import Any
from copy import deepcopy
from datetime import datetime

regex = re.compile("[^a-zA-Z0-9]")
TextFormatter: object = object()
JsonFormatter: object = object()
DEBUG: int = logging.DEBUG
INFO: int = logging.INFO
WARNING: int = logging.WARNING
ERROR: int = logging.ERROR
PANIC: int = logging.FATAL
DEBUG_COLOR = "\033[1;37m{}\033[0m"
INFO_COLOR = "\033[1;32m{}\033[0m"
WARNING_COLOR = "\033[1;33m{}\033[0m"
ERROR_COLOR = "\033[1;31m{}\033[0m"
PANIC_COLOR = "\033[1;36m{}\033[0m"
LEVEL_MAP = {
    DEBUG: "debug",
    INFO: "info",
    WARNING: "warning",
    ERROR: "error",
    PANIC: "panic",
}
COLOR_LEVEL_MAP = {
    DEBUG: DEBUG_COLOR.format(LEVEL_MAP[DEBUG]),
    INFO: INFO_COLOR.format(LEVEL_MAP[INFO]),
    WARNING: WARNING_COLOR.format(LEVEL_MAP[WARNING]),
    ERROR: ERROR_COLOR.format(LEVEL_MAP[ERROR]),
    PANIC: PANIC_COLOR.format(LEVEL_MAP[PANIC]),
}

# fix messy code when output color in win32.
if sys.platform == "win32":
    import colorama

    colorama.init(autoreset=True)


# json encoder:
#   1、`datetime`
class PrettyEncoder(json.JSONEncoder):

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return str(obj)
        return super().default(obj)


# json encoder: forced every obj to str.
class ForcedEncoder(json.JSONEncoder):

    def default(self, obj: Any) -> str:
        return f"{obj}"


# interface metaclass, force obj to implement the `property`.
class IHookMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if IHook not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `loggus.IHook`")
            if "GetLevels" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `GetLevels`")
            if "ProcessMsg" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `ProcessMsg`")
        return type.__new__(cls, name, bases, attrs)


class IHook(metaclass=IHookMetaClass):

    def GetLevels(self) -> list:
        raise NotImplementedError

    def ProcessMsg(self, msg: str) -> None:
        raise NotImplementedError


# this is a storage, to store formatter & level & hooks
# there will be default one instance: `_logger`, so each default entry will bind this and use it's rules.
# if you want to split the rule of logger, you can new one also.
class Logger:

    def __init__(self, out: Any = None, formatter: Any = None, level: int = None):
        self.out = out or sys.stdout
        self.formatter = formatter or TextFormatter
        self.level = level or INFO
        self.color_switch = True
        self.hooks = {
            DEBUG: [],
            INFO: [],
            WARNING: [],
            ERROR: [],
        }

    def NewEntry(self):
        return Entry(self)

    def CloseColor(self) -> None:
        self.color_switch = False

    def OpenColor(self) -> None:
        self.color_switch = True

    @property
    def ColorSwitch(self) -> bool:
        if self.formatter is JsonFormatter:
            return False
        return self.color_switch

    def SetLevel(self, level: int):
        if level in LEVEL_MAP:
            self.level = level
        else:
            self.warning(f"invalid level")

    def IsLevelEnabled(self, level: int) -> bool:
        return level >= self.level

    def Format(self, level: int, fields: dict) -> None:
        if self.formatter is JsonFormatter:
            self.JsonFormat(level, fields)
        else:
            self.TextFormat(level, fields)

    def JsonFormat(self, level: int, fields: dict):
        try:
            out = json.dumps(fields, ensure_ascii=False, cls=PrettyEncoder)
        except:
            out = json.dumps(fields, ensure_ascii=False, cls=ForcedEncoder)
        out = f"{out}\n"
        self.Write(out)
        self.FireHooks(level, out)

    def TextFormat(self, level: int, fields: dict):
        _time = fields.pop("time", datetime.now())
        _level = fields.pop("level", "undefined")
        _msg = f"""{fields.pop("msg", "empty")}"""
        if regex.search(_msg):
            _msg = f"\"{_msg}\""
        out = f"time=\"{_time}\" level={_level} msg={_msg}"
        error = fields.pop("error", None)
        if error is not None:
            out = f"{out} error=\"[####@\n{error}\n@####]\" "
        for key, value in fields.items():
            out += " "
            if isinstance(value, str):
                out += f"{key}=\"{value}\"" if regex.search(value) else f"{key}={value}"
            elif isinstance(value, Exception):
                out += f"{key}=\"[####@ {value} @####]\""
            elif isinstance(value, datetime):
                out += f"{key}=\"{value}\""
            else:
                out += f"{key}={value}"
        out = f"{out}\n"
        self.Write(out)
        self.FireHooks(level, out)

    def Write(self, out: str) -> None:
        self.out.write(out)
        self.out.flush()

    def AddHook(self, hook: object):
        if isinstance(hook, IHook):
            levels = hook.GetLevels()
            for level in levels:
                if level in self.hooks:
                    self.hooks[level].append(hook)
        else:
            self.warning("invalid hook")

    def FireHooks(self, level: int, msg: str):
        for hook in self.hooks.get(level, []):  # type: IHook
            try:
                hook.ProcessMsg(msg)
            except:
                self.Write(f"\nHookErr[{level}:{hook}]: {traceback.format_exc()}\n\n")

    def SetFormatter(self, formatter: TextFormatter or JsonFormatter):
        if formatter in (TextFormatter, JsonFormatter):
            self.formatter = formatter

    def withField(self, key: Any, value: Any, color: str):
        entry = self.NewEntry()
        return entry.withField(key, value, color)

    def WithField(self, key: Any, value: Any, color: str):
        entry = self.NewEntry()
        return entry.WithField(key, value, color)

    def withFields(self, fields: dict):
        entry = self.NewEntry()
        return entry.withFields(fields)

    def WithFields(self, fields: dict):
        entry = self.NewEntry()
        return entry.WithFields(fields)

    def withException(self, exception: Exception):
        entry = self.NewEntry()
        return entry.withException(exception)

    def WithException(self, exception: Exception):
        entry = self.NewEntry()
        return entry.WithException(exception)

    def withTraceback(self):
        entry = self.NewEntry()
        return entry.withTraceback()

    def WithTraceback(self):
        entry = self.NewEntry()
        return entry.WithTraceback()

    def debug(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.debug(msg)

    def Debug(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.Debug(msg)

    def info(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.info(msg)

    def Info(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.Info(msg)

    def warning(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.warning(msg)

    def Warning(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.Warning(msg)

    def error(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.error(msg)

    def Error(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.Error(msg)

    def panic(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.panic(msg)

    def Panic(self, msg: Any) -> None:
        entry = self.NewEntry()
        entry.Panic(msg)


def NewLogger(out: Any = None, formatter: Any = None, level: int = None) -> Logger:
    return Logger(out, formatter, level)


_logger = NewLogger()


# default func for Logger.


def SetLevel(level: int) -> None:
    _logger.SetLevel(level)


def SetFormatter(formatter: TextFormatter or JsonFormatter):
    _logger.SetFormatter(formatter)


def CloseColor():
    _logger.CloseColor()


def OpenColor():
    _logger.OpenColor()


def AddHook(hook: object):
    _logger.AddHook(hook)


# An entry is the final or intermediate logging entry. It contains all the fields,
# It's finally logged when debug/info/warning/error/panic is called on it.
# these objects can be reused and passed around as much as you wish to avoid field duplication.
class Entry:

    def __init__(self, logger: Logger):
        self.logger = logger
        self.fields = dict()

    def withField(self, key: Any, value: Any, color: str = None):
        if color and self.logger.ColorSwitch and \
                color in (DEBUG_COLOR, INFO_COLOR, WARNING_COLOR, ERROR_COLOR, PANIC_COLOR):
            return self.withFields({key: color.format(value)})
        return self.withFields({key: value})

    def WithField(self, key: Any, value: Any, color: str = None):
        return self.withField(key, value, color)

    def withFields(self, fields: dict):
        try:
            newFields = deepcopy(self.fields)
        except:
            newFields = {f"{key}": f"{value}" for key, value in self.fields.items()}
        newFields.update(fields)
        entry = NewEntry(self.logger)
        entry.fields = newFields
        return entry

    def WithFields(self, fields: dict):
        return self.withFields(fields)

    def withException(self, exception: Exception):
        return self.withField("exception", str(exception), ERROR_COLOR)

    def WithException(self, exception: Exception):
        return self.withException(exception)

    def withTraceback(self):
        return self.withField("traceback", traceback.format_exc().strip(), ERROR_COLOR)

    def WithTraceback(self):
        return self.withTraceback()

    def log(self, level: int, msg: Any) -> None:
        try:
            fields = deepcopy(self.fields)
        except:
            fields = {f"{key}": f"{value}" for key, value in self.fields.items()}
        fields.update({
            "time": datetime.now(),
            "level": (COLOR_LEVEL_MAP if self.logger.ColorSwitch else LEVEL_MAP).get(level, "undefined"),
            "msg": msg,
        })
        self.logger.Format(level, fields)

    def Log(self, level: int, msg: Any):
        if self.logger.IsLevelEnabled(level):
            self.log(level, msg)
            if level >= PANIC:
                sys.exit(PANIC)

    def debug(self, msg: Any) -> None:
        self.Log(DEBUG, msg)

    def Debug(self, msg: Any) -> None:
        self.debug(msg)

    def info(self, msg: Any) -> None:
        self.Log(INFO, msg)

    def Info(self, msg: Any) -> None:
        self.info(msg)

    def warning(self, msg: Any) -> None:
        self.Log(WARNING, msg)

    def Warning(self, msg: Any) -> None:
        self.warning(msg)

    def error(self, msg: Any) -> None:
        self.Log(ERROR, msg)

    def Error(self, msg: Any) -> None:
        self.error(msg)

    def panic(self, msg: Any) -> None:
        self.Log(PANIC, msg)

    def Panic(self, msg: Any) -> None:
        self.panic(msg)


def NewEntry(logger: Logger = None) -> Entry:
    return Entry(logger or _logger)


# The default entry should be guaranteed not to be contaminated.
_entry = NewEntry(_logger)


# default func for entry.


def withField(key: Any, value: Any, color: str = None) -> Entry:
    return _entry.withField(key, value, color)


def withFields(fields: dict) -> Entry:
    return _entry.withFields(fields)


def WithField(key: Any, value: Any, color: str = None) -> Entry:
    return _entry.WithField(key, value, color)


def WithFields(fields: dict) -> Entry:
    return _entry.WithFields(fields)


def withException(exception: Exception) -> Entry:
    return _entry.withException(exception)


def WithException(exception: Exception) -> Entry:
    return _entry.WithException(exception)


def withTraceback():
    return _entry.withTraceback()


def WithTraceback():
    return _entry.WithTraceback()


def debug(msg: Any) -> None:
    entry = NewEntry()
    entry.debug(msg)


def info(msg: Any) -> None:
    entry = NewEntry()
    entry.info(msg)


def warning(msg: Any) -> None:
    entry = NewEntry()
    entry.warning(msg)


def error(msg: Any) -> None:
    entry = NewEntry()
    entry.error(msg)


def panic(msg: Any) -> None:
    entry = NewEntry()
    entry.panic(msg)


def Debug(msg: Any) -> None:
    entry = NewEntry()
    entry.Debug(msg)


def Info(msg: Any) -> None:
    entry = NewEntry()
    entry.Info(msg)


def Warning(msg: Any) -> None:
    entry = NewEntry()
    entry.Warning(msg)


def Error(msg: Any) -> None:
    entry = NewEntry()
    entry.Error(msg)


def Panic(msg: Any) -> None:
    entry = NewEntry()
    entry.Panic(msg)


def execute():
    import argparse

    SetLevel(DEBUG)
    entry = WithFields({
        "author": __author__,
        "version": __version__,
    })

    parser = argparse.ArgumentParser(
        prog="loggus",
        description="This is a structured log, and you can output json easy.",
        epilog="you can also add Hook for each output, such like push log to MQ, or write log into file.",
    )

    parser.add_argument("-d", "--debug", action='store_true', help="like debug(msg)")
    parser.add_argument("-i", "--info", action='store_true', help="like info(msg)", default=True)
    parser.add_argument("-w", "--warning", action='store_true', help="like warning(msg)")
    parser.add_argument("-e", "--error", action='store_true', help="like error(msg)")
    parser.add_argument("-p", "--panic", action='store_true', help="like panic(msg), it will exit 50.")
    parser.add_argument("-j", "--json", action='store_true',
                        help="set json formatter, like SetFormatter(JsonFormatter)")
    parser.add_argument("-f", "--field", action='append', type=str, default=[],
                        help="key=value, like WithField(key, value)")
    parser.add_argument("-fs", "--fields", action='append', type=str, default=[],
                        help="json_data, like WithFields(json.loads(json_data))")
    parser.add_argument("msg", nargs="*", help="something you want to output.")

    args = parser.parse_args()

    msg = " ".join(args.msg)

    for field in args.field:
        fields = field.split("=", 1)
        if len(fields) == 2:
            entry = entry.WithField(*fields)
    for fields in args.fields:
        try:
            fields = json.loads(fields)
        except:
            entry.WithField("InvalidJsonData", fields, WARNING_COLOR).WithTraceback().Panic(msg)
            return
        else:
            entry = entry.WithFields(fields)

    if args.json:
        SetFormatter(JsonFormatter)
    if args.debug:
        entry.debug(msg)
    if args.info:
        entry.info(msg)
    if args.warning:
        entry.warning(msg)
    if args.error:
        entry.error(msg)
    if args.panic:
        entry.panic(msg)
