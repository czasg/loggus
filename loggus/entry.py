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

from loggus.level import *
from loggus.logger import *


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
        self.fields = newFields
        return self

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

    @contextlib.contextmanager
    def withCallback(self, callback: callable = None):
        try:
            yield
        except Exception as e:
            try:
                (callback or (lambda *args: self.withTraceback().error(*args)))(e)
            except Exception as e:
                self.withTraceback().error(e)

    def WithCallback(self, callback: callable = None):
        return self.withCallback(callback)

    def log(self, level: int, *args: Any) -> None:
        try:
            fields = deepcopy(self.fields)
        except:
            fields = {f"{key}": f"{value}" for key, value in self.fields.items()}
        fields.update({
            "time": datetime.now(),
            "level": (COLOR_LEVEL_MAP if self.logger.ColorSwitch else LEVEL_MAP).get(level, "undefined"),
            "msg": " ".join([f"{arg}" for arg in args]),
        })
        self.logger.Format(level, fields)

    def Log(self, level: int, *args: Any):
        if self.logger.IsLevelEnabled(level):
            self.log(level, *args)
            if level >= PANIC:
                sys.exit(PANIC)

    def debug(self, *args: Any) -> None:
        self.Log(DEBUG, *args)

    def Debug(self, *args: Any) -> None:
        self.debug(*args)

    def info(self, *args: Any) -> None:
        self.Log(INFO, *args)

    def Info(self, *args: Any) -> None:
        self.info(*args)

    def warning(self, *args: Any) -> None:
        self.Log(WARNING, *args)

    def Warning(self, *args: Any) -> None:
        self.warning(*args)

    def error(self, *args: Any) -> None:
        self.Log(ERROR, *args)

    def Error(self, *args: Any) -> None:
        self.error(*args)

    def panic(self, *args: Any) -> None:
        self.Log(PANIC, *args)

    def Panic(self, *args: Any) -> None:
        self.panic(*args)
