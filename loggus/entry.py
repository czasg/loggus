# coding: utf-8
import os
import sys

from copy import deepcopy
from _io import TextIOWrapper
from typing import List, Dict

from loggus.level import *
from loggus.hooks import *
from loggus.fields import *
from loggus.formatter import *

if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else:
    def currentframe():
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


def FindCaller():
    f = currentframe()
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break
    return rv


_srcfile = os.path.normcase(FindCaller.__code__.co_filename)


class Logger:
    out: TextIOWrapper = sys.stdout
    formatter: IFormatter = TextFormatter
    fieldKeys: List[IField] = [FieldKeyTime, FieldKeyLevel, FieldKeyMsg]
    needFrame: bool = False
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

    def SetFieldKeys(self, *fieldKeys):
        fields = []
        for fieldKey in fieldKeys:
            if not IsIField(fieldKey):
                raise Exception(f"undefined Field[{fieldKey}]!")
            fields.append(fieldKey)
        if fields:
            self.fieldKeys = fields
        if {FieldKeyFunc, FieldKeyLineNo, FieldKeyFile} & {*self.fieldKeys}:
            self.needFrame = True
        else:
            self.needFrame = False

    def OpenFieldKeyFunc(self):
        if FieldKeyFunc not in self.fieldKeys:
            self.fieldKeys.append(FieldKeyFunc)
        self.needFrame = True

    def OpenFieldKeyLineNo(self):
        if FieldKeyLineNo not in self.fieldKeys:
            self.fieldKeys.append(FieldKeyLineNo)
        self.needFrame = True

    def OpenFieldKeyFile(self):
        if FieldKeyFile not in self.fieldKeys:
            self.fieldKeys.append(FieldKeyFile)
        self.needFrame = True

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
    frameFuncName = None
    frameLineNo = None
    frameFilePath = None

    def __init__(self, logger: Logger):
        self.logger = logger

    def log(self, level: Level, msg: str):
        entry = NewEntry(self.logger, self.fields)
        if entry.logger.needFrame:
            entry.frameFilePath, entry.frameLineNo, entry.frameFuncName, = FindCaller()
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

if __name__ == '__main__':
    _logger.OpenFieldKeyFile()
    _logger.OpenFieldKeyFunc()
    _logger.OpenFieldKeyLineNo()
    entry = NewEntry(_logger)
    entry.Log(INFO, "hello world")
