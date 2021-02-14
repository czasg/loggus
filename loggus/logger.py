# coding: utf-8
import re
import sys
import json
import inspect
import logging
import traceback
import contextlib

from typing import Any, List
from copy import deepcopy
from datetime import datetime


# this is a storage, to store formatter & level & hooks
# there will be default one instance: `_logger`, so each default entry will bind this and use it's rules.
# if you want to split the rule of logger, you can new one also.
class Logger:

    def __init__(self, out: Any = None, formatter: Any = None, level: int = None, fields: List[object] = None):
        self.out = out or sys.stdout
        self.formatter = formatter or TextFormatter
        self.fields = fields or [FieldKeyTime, FieldKeyLevel, FieldKeyMsg]
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

    def SetFields(self, fields: list):
        self.fields = fields

    def GetFieldsOutput(self, fields: dict):
        output = ""
        for fieldKey in self.fields:  # type: FieldKey
            output += fieldKey.GetValue(fields)
        return output

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
        out = self.GetFieldsOutput(fields)
        for key, value in fields.items():
            if isinstance(value, str):
                out += f"{key}=\"{value}\"" if regex.search(value) else f"{key}={value}"
            elif isinstance(value, Exception):
                out += f"{key}=\"[####@ {value} @####]\""
            elif isinstance(value, datetime):
                out += f"{key}=\"{value}\""
            else:
                out += f"{key}={value}"
            out += " "
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

    def withCallback(self, callback: callable = None):
        entry = self.NewEntry()
        return entry.withCallback(callback)

    def WithCallback(self, callback: callable = None):
        entry = self.NewEntry()
        return entry.WithCallback(callback)

    def debug(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.debug(*args)

    def Debug(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.Debug(*args)

    def info(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.info(*args)

    def Info(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.Info(*args)

    def warning(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.warning(*args)

    def Warning(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.Warning(*args)

    def error(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.error(*args)

    def Error(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.Error(*args)

    def panic(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.panic(*args)

    def Panic(self, *args: Any) -> None:
        entry = self.NewEntry()
        entry.Panic(*args)

_logger = Logger()
