# coding: utf-8
__author__ = "https://github.com/CzaOrz"
__version__ = "0.0.2"

import sys
import json
import logging
import traceback

from typing import Any
from queue import Queue
from copy import deepcopy
from datetime import datetime

EntryQueue = Queue(1024)
TextFormatter: object = object()
JsonFormatter: object = object()
DEBUG: int = logging.DEBUG
INFO: int = logging.INFO
WARNING: int = logging.WARNING
ERROR: int = logging.ERROR
PANIC: int = logging.FATAL
LEVEL_MAP = {
    DEBUG: "debug",
    INFO: "info",
    WARNING: "warning",
    ERROR: "error",
    PANIC: "panic",
}


class PrettyEncoder(json.JSONEncoder):

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return str(obj)
        return super().default(obj)


class IHookMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if IHook not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `logor.interface.IHook`")
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


class Logger:

    def __init__(self, out: Any = None, formatter: Any = None, level: int = None):
        self.out = out or sys.stdout
        self.formatter = formatter or TextFormatter
        self.level = level or INFO
        self.hooks = {
            DEBUG: [],
            INFO: [],
            WARNING: [],
            ERROR: [],
        }

    def NewEntry(self):
        try:
            entry = EntryQueue.get_nowait()
        except:
            return Entry(self)
        else:
            entry.logger = self
            return entry

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
            print(traceback.format_exc())
        else:
            out = f"{out}\n"
            self.Write(out)
            self.FireHooks(level, out)

    def TextFormat(self, level: int, fields: dict):
        _time = fields.pop("time", datetime.now())
        _level = fields.pop("level", "undefined")
        _msg = fields.pop("msg", "empty")
        if " " in _msg:
            _msg = f"\"{_msg}\""
        out = f"time=\"{_time}\" level={_level} msg={_msg}"
        error = fields.pop("error", None)
        if error is not None:
            out = f"{out} error=\"[####@\n{error}\n@####]\" "
        for key, value in fields.items():
            out += " "
            if isinstance(value, str):
                out += f"{key}=\"{value}\"" if " " in value else f"{key}={value}"
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
            hook.ProcessMsg(msg)

    def SetFormatter(self, formatter: TextFormatter or JsonFormatter):
        if formatter in (TextFormatter, JsonFormatter):
            self.formatter = formatter

    def WithField(self, key: str, value: Any):
        entry = self.NewEntry()
        return entry.WithField(key, value)

    def WithFields(self, fields: dict):
        entry = self.NewEntry()
        return entry.WithFields(fields)

    def debug(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.debug(msg)

    def Debug(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.Debug(msg)

    def info(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.info(msg)

    def Info(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.Info(msg)

    def warning(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.warning(msg)

    def Warning(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.Warning(msg)

    def error(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.error(msg)

    def Error(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.Error(msg)

    def panic(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.panic(msg)

    def Panic(self, msg: str) -> None:
        entry = self.NewEntry()
        entry.Panic(msg)


def NewLogger(out: Any = None, formatter: Any = None, level: int = None) -> Logger:
    return Logger(out, formatter, level)


_logger = NewLogger()


def SetLevel(level: int) -> None:
    _logger.SetLevel(level)


def SetFormatter(formatter: TextFormatter or JsonFormatter):
    _logger.SetFormatter(formatter)


def AddHook(hook: object):
    _logger.AddHook(hook)


class Entry:

    def __init__(self, logger: Logger):
        self.logger = logger
        self.fields = dict()

    def WithField(self, key: str, value: Any):
        return self.WithFields({key: value})

    def WithFields(self, fields: dict):
        self.fields.update(fields)
        return self

    def WithException(self, exception: Exception) -> None:
        self.fields.update({"error": str(exception)})

    def log(self, level: int, msg: str) -> None:
        fields = deepcopy(self.fields)
        fields.update({
            "time": datetime.now(),
            "level": LEVEL_MAP.get(level, "undefined"),
            "msg": msg,
        })
        self.logger.Format(level, fields)

    def Log(self, level: int, msg: str):
        if self.logger.IsLevelEnabled(level):
            self.log(level, msg)
            if level >= PANIC:
                sys.exit(PANIC)

    def debug(self, msg: str) -> None:
        self.Log(DEBUG, msg)

    def Debug(self, msg: str) -> None:
        self.debug(msg)

    def info(self, msg: str) -> None:
        self.Log(INFO, msg)

    def Info(self, msg: str) -> None:
        self.info(msg)

    def warning(self, msg: str) -> None:
        self.Log(WARNING, msg)

    def Warning(self, msg: str) -> None:
        self.warning(msg)

    def error(self, msg: str) -> None:
        self.Log(ERROR, msg)

    def Error(self, msg: str) -> None:
        self.error(msg)

    def panic(self, msg: str) -> None:
        self.Log(PANIC, msg)

    def Panic(self, msg: str) -> None:
        self.panic(msg)

    def __del__(self):
        self.fields = dict()
        try:
            EntryQueue.put_nowait(self)
        except:
            del self


def NewEntry():
    try:
        entry = EntryQueue.get_nowait()
    except:
        return Entry(_logger)
    else:
        entry.logger = _logger
        return entry


def WithField(key: str, value: Any) -> Entry:
    entry = NewEntry()
    return entry.WithField(key, value)


def WithFields(fields: dict) -> Entry:
    entry = NewEntry()
    return entry.WithFields(fields)


def debug(msg: str) -> None:
    entry = NewEntry()
    entry.debug(msg)


def info(msg: str) -> None:
    entry = NewEntry()
    entry.info(msg)


def warning(msg: str) -> None:
    entry = NewEntry()
    entry.warning(msg)


def error(msg: str) -> None:
    entry = NewEntry()
    entry.error(msg)


def panic(msg: str) -> None:
    entry = NewEntry()
    entry.panic(msg)


def Debug(msg: str) -> None:
    entry = NewEntry()
    entry.Debug(msg)


def Info(msg: str) -> None:
    entry = NewEntry()
    entry.Info(msg)


def Warning(msg: str) -> None:
    entry = NewEntry()
    entry.Warning(msg)


def Error(msg: str) -> None:
    entry = NewEntry()
    entry.Error(msg)


def Panic(msg: str) -> None:
    entry = NewEntry()
    entry.Panic(msg)


def execute():
    args = sys.argv[1:]
    entry = WithFields({
        "author": __author__,
        "version": __version__,
    })
    for index, argv in enumerate(args):
        entry = entry.WithField(f"argv{index + 1}", argv)
    entry.Info("hello loggus")
