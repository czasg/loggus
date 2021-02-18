# coding: utf-8
import sys
import logging

from _io import TextIOWrapper
from typing import List, Dict
from collections import defaultdict

from loggus.hooks import *
from loggus.fields import *
from loggus.formatter import *

DEBUG: int = logging.DEBUG
INFO: int = logging.INFO
WARNING: int = logging.WARNING
ERROR: int = logging.ERROR
PANIC: int = logging.FATAL
LEVEL_MAP: dict = {
    DEBUG: "debug",
    INFO: "info",
    WARNING: "warning",
    ERROR: "error",
    PANIC: "panic",
}


class Logger:
    out: TextIOWrapper = sys.stdout
    formatter: IFormatter = TextFormatter
    fieldKeys: List[IField] = [FieldKeyTime, FieldKeyLevel, FieldKeyMsg]
    baseLevel: int = INFO
    colorSwitch: bool = True
    hooks: Dict[int, List[IHook]] = defaultdict(list)

    def SetLevel(self, level: int):
        self.baseLevel = level

    def IsLevelEnabled(self, level: int) -> bool:
        return level >= self.baseLevel


def NewLogger():
    return Logger()


class Entry:
    pass


def NewEntry():
    return Entry()
