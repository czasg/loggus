# coding: utf-8
import sys

from copy import deepcopy
from datetime import datetime
from _io import TextIOWrapper
from typing import List, Dict

from loggus.level import *
from loggus.hooks import *
from loggus.fields import *
from loggus.formatter import *


class Logger:
    out: TextIOWrapper = sys.stdout
    formatter: IFormatter = TextFormatter
    fieldKeys: List[IField] = [FieldKeyTime, FieldKeyLevel, FieldKeyMsg]
    baseLevel: Level = INFO
    colorSwitch: bool = True
    hooks: Dict[Level, List[IHook]] = {
        DEBUG: [],
        INFO: [],
        WARNING: [],
        ERROR: [],
        PANIC: [],
    }

    def AddHooks(self, *hooks: List[IHook]) -> None:
        for hook in hooks:  # type: IHook
            if not IsIHook(hook):
                raise Exception(f"undefined Hook[{hook}]!")
            for level in hook.GetLevels():
                if not IsLevel(level):
                    raise Exception(f"undefined Level[{level}]!")
                self.hooks[level].append(hook)

    def FireHooks(self, entry, level, msg, output) -> None:
        for hook in self.hooks[level]:  # type: IHook
            hook.Fire(entry, level, msg, output)

    def IsLevelEnabled(self, level: Level) -> bool:
        return level >= self.baseLevel

    def SetLevel(self, level: Level) -> None:
        if not IsLevel(level):
            raise Exception(f"undefined Level[{level}]!")
        self.baseLevel = level

    def Write(self, output: str) -> None:
        self.out.write(output)
        self.out.flush()

    def NewEntry(self):
        pass

    def Debug(self):
        pass

    def Info(self):
        pass

    def Warning(self):
        pass

    def Error(self):
        pass

    def Panic(self):
        pass


def NewLogger():
    return Logger()


_logger = NewLogger()


class Entry:
    fields = {}

    def __init__(self, logger: Logger):
        self.logger = logger

    def log(self, level: Level, msg: str):
        entry = NewEntry(self.logger, self.fields)
        output = entry.logger.formatter.Format(entry, level, msg)
        entry.logger.FireHooks(entry, level, msg, output)
        entry.logger.Write(output)

    def Log(self, level: Level, msg: str):
        if self.logger.IsLevelEnabled(level):
            self.log(level, msg)
            if level >= PANIC:
                sys.exit(PANIC.value)


def NewEntry(logger: Logger = _logger, fields=None):
    entry = Entry(logger)
    if fields:
        try:
            fields = deepcopy(fields)
        except:
            fields = {f"{key}": f"{value}" for key, value in fields.items()}
        entry.fields = fields
    return entry
