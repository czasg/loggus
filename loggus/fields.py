# coding: utf-8
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

    def ResolveIn(self, entry):
        raise NotImplementedError

    def ResolveOut(self, entry):
        raise NotImplementedError


class FieldKeyTime(IField):
    Key = "time"

    def ResolveIn(self, entry):
        raise NotImplementedError

    def ResolveOut(self, entry):
        raise NotImplementedError


class FieldKeyLevel(IField):
    Key = "level"

    def ResolveIn(self, entry):
        raise NotImplementedError

    def ResolveOut(self, entry):
        raise NotImplementedError


class FieldKeyMsg(IField):
    Key = "msg"

    def ResolveIn(self, entry):
        raise NotImplementedError

    def ResolveOut(self, entry):
        raise NotImplementedError


class FieldKeyLineNo(IField):
    Key = "lineNo"

    def ResolveIn(self, entry):
        raise NotImplementedError

    def ResolveOut(self, entry):
        raise NotImplementedError


class FieldKeyFunc(IField):
    Key = "funcName"

    def ResolveIn(self, entry):
        raise NotImplementedError

    def ResolveOut(self, entry):
        raise NotImplementedError


class FieldKeyFile(IField):
    Key = "filePath"

    def ResolveIn(self, entry):
        raise NotImplementedError

    def ResolveOut(self, entry):
        raise NotImplementedError
