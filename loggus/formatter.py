# coding: utf-8
import re

from loggus.level import Level

regex = re.compile("^[a-zA-Z0-9]*$")


def IsIFormatter(formatter) -> bool:
    return formatter.__class__ is IFormatterMetaClass


class IFormatterMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if IFormatter not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `loggus.interfaces.IFormatter`")
            if "Format" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `Format`")
        return type.__new__(cls, name, bases, attrs)


class IFormatter(metaclass=IFormatterMetaClass):

    def Format(self, entry, level, msg) -> str:
        raise NotImplementedError


class TextFormatter(IFormatter):

    def Format(self, entry, level: Level, msg: str) -> str:
        output = " ".join([fieldKey.ResolveOut(entry, level, msg) for fieldKey in entry.fieldKeys])
        for key, value in entry.fields.items():
            if isinstance(value, str):
                if regex.match(value):
                    output += f" {key}={value}"
                else:
                    output += f" {key}=\"{value}\""
            elif isinstance(value, int):
                output += f" {key}={value}"
            else:
                output += f" {key}=\"{value}\""
        return f"{output}\n"


class JsonFormatter(IFormatter):

    def Format(self, entry, level, msg) -> str:
        raise NotImplementedError
