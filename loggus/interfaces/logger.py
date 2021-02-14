import sys

from typing import List, Dict
from loggus.interfaces.formatter import IFormatter
from loggus.interfaces.field import IField
from loggus.interfaces.hook import IHook


class ILoggerMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if ILogger not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `loggus.interfaces.ILogger`")
            if "ResolveIn" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `ResolveIn`")
            if "ResolveOut" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `ResolveOut`")
        return type.__new__(cls, name, bases, attrs)


class ILogger:
    out = sys.stdout
    formatter: IFormatter
    fieldKeys: List[IField]
    baseLevel: int
    colorSwitch: bool
    hooks: Dict[str, IHook]

    def IsLevelEnabled(self, level: int) -> bool:
        raise NotImplementedError
