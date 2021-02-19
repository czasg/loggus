# coding: utf-8
import re

from datetime import datetime

regex = re.compile("^[a-zA-Z0-9]*$")


def IsIField(*fields) -> bool:
    for field in fields:
        if field.__class__ is not IFieldMetaClass:
            return False
    return True


class IFieldMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if IField not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `loggus.interfaces.IField`")
            if attrs.get("Key", None) is None:
                raise Exception(f"please ensure `{name}` implemented the attr of `Key`")
            if "ResolveIn" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `ResolveIn`")
            if "ResolveOut" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `ResolveOut`")
        return type.__new__(cls, name, bases, attrs)


class IField(metaclass=IFieldMetaClass):
    Key = None

    @classmethod
    def ResolveIn(cls, entry, level, msg):
        raise NotImplementedError

    @classmethod
    def ResolveOut(cls, entry, level, msg):
        raise NotImplementedError


class FieldKeyTime(IField):
    Key = "time"

    @classmethod
    def ResolveIn(cls, entry, level, msg):
        entry.fields[cls.Key] = f"{datetime.now()}"

    @classmethod
    def ResolveOut(cls, entry, level, msg):
        entry.fields.pop(cls.Key, None)
        return f"{cls.Key}=\"{datetime.now()}\""


class FieldKeyLevel(IField):
    Key = "level"

    @classmethod
    def ResolveIn(cls, entry, level, msg):
        entry.fields[cls.Key] = level.describe

    @classmethod
    def ResolveOut(cls, entry, level, msg):
        entry.fields.pop(cls.Key, None)
        return f"{cls.Key}={level.color if entry.logger.colorSwitch else level.describe}"


class FieldKeyMsg(IField):
    Key = "msg"

    @classmethod
    def ResolveIn(cls, entry, level, msg):
        entry.fields[cls.Key] = msg

    @classmethod
    def ResolveOut(cls, entry, level, msg):
        entry.fields.pop(cls.Key, None)
        if regex.match(msg):
            return f"{cls.Key}={msg}"
        else:
            return f"{cls.Key}=\"{msg}\""


class FieldKeyLineNo(IField):
    Key = "lineNo"

    @classmethod
    def ResolveIn(cls, entry, level, msg):
        raise NotImplementedError

    @classmethod
    def ResolveOut(cls, entry, level, msg):
        return f"{cls.Key}={entry.frameLineNo}"


class FieldKeyFunc(IField):
    Key = "funcName"

    @classmethod
    def ResolveIn(cls, entry, level, msg):
        raise NotImplementedError

    @classmethod
    def ResolveOut(cls, entry, level, msg):
        return f"{cls.Key}={entry.frameFuncName}"


class FieldKeyFile(IField):
    Key = "filePath"

    @classmethod
    def ResolveIn(cls, entry, level, msg):
        raise NotImplementedError

    @classmethod
    def ResolveOut(cls, entry, level, msg):
        return f"{cls.Key}={entry.frameFilePath}"
