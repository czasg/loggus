# coding: utf-8
from loggus.level import GetAllLevels


def IsIHook(hook) -> bool:
    return isinstance(hook, IHook)


class IHookMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if IHook not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `loggus.interfaces.IHook`")
            if "GetLevels" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `GetLevels`")
            if "Fire" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `Fire`")
        return type.__new__(cls, name, bases, attrs)


class IHook(metaclass=IHookMetaClass):

    def GetLevels(self) -> list:
        raise NotImplementedError

    def Fire(self, entry, level, msg, output) -> None:
        raise NotImplementedError


class FileHook(IHook):

    

    def GetLevels(self):
        return GetAllLevels()

    def Fire(self, entry, level, msg, output) -> None:
        raise NotImplementedError
