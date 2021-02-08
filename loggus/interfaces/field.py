from types import CodeType

__all__ = "IField",


class IFieldMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if IField not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `loggus.interfaces.IField`")
            if "GetResolve" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `Resolve`")
            if "DropResolve" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `Resolve`")
        return type.__new__(cls, name, bases, attrs)


class IField(metaclass=IFieldMetaClass):
    NeedFrame = False

    def GetResolve(self, fields: dict, frame: CodeType = None):
        raise NotImplementedError

    def DropResolve(self, fields: dict, frame: CodeType = None):
        raise NotImplementedError
