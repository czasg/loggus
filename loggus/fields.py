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

    def ResolveIn(self, entry, level, msg):
        raise NotImplementedError

    def ResolveOut(self, entry, level, msg):
        raise NotImplementedError


class FieldKeyTime(IField):
    Key = "time"

    def ResolveIn(self, entry, level, msg):
        entry.fields[self.Key] = f"{datetime.now()}"

    def ResolveOut(self, entry, level, msg):
        entry.fields.pop(self.Key, None)
        return f"{self.Key}=\"{datetime.now()}\""


class FieldKeyLevel(IField):
    Key = "level"

    def ResolveIn(self, entry, level, msg):
        entry.fields[self.Key] = level.describe

    def ResolveOut(self, entry, level, msg):
        entry.fields.pop(self.Key, None)
        return f"{self.Key}={level.describe}"


class FieldKeyMsg(IField):
    Key = "msg"

    def ResolveIn(self, entry, level, msg):
        entry.fields[self.Key] = msg

    def ResolveOut(self, entry, level, msg):
        entry.fields.pop(self.Key, None)
        if regex.match(msg):
            return f"{self.Key}={msg}"
        else:
            return f"{self.Key}=\"{msg}\""


class FieldKeyLineNo(IField):
    Key = "lineNo"

    def ResolveIn(self, entry, level, msg):
        raise NotImplementedError

    def ResolveOut(self, entry, level, msg):
        raise NotImplementedError


class FieldKeyFunc(IField):
    Key = "funcName"

    def ResolveIn(self, entry, level, msg):
        raise NotImplementedError

    def ResolveOut(self, entry, level, msg):
        raise NotImplementedError


class FieldKeyFile(IField):
    Key = "filePath"

    def ResolveIn(self, entry, level, msg):
        raise NotImplementedError

    def ResolveOut(self, entry, level, msg):
        raise NotImplementedError
