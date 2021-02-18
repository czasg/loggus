# coding: utf-8
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

    def Format(self, entry) -> str:
        raise NotImplementedError


class TextFormatter(IFormatter):

    def Format(self, entry) -> str:
        raise NotImplementedError


class JsonFormatter(IFormatter):

    def Format(self, entry) -> str:
        raise NotImplementedError
