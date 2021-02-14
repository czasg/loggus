from loggus.interfaces.entry import IEntry

__all__ = "IField",


class IFieldMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if IField not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `loggus.interfaces.IField`")
            if "ResolveIn" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `ResolveIn`")
            if "ResolveOut" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `ResolveOut`")
        return type.__new__(cls, name, bases, attrs)


class IField(metaclass=IFieldMetaClass):

    def ResolveIn(self, entry: IEntry):
        raise NotImplementedError

    def ResolveOut(self, entry: IEntry):
        raise NotImplementedError
