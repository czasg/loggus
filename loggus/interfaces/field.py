from loggus.interfaces.entry import IEntry

__all__ = "IField",


class IField:
    NeedFrame: bool

    @property
    def fieldKey(self):
        raise NotImplementedError

    def FillResolve(self, entry: IEntry):
        raise NotImplementedError

    def DropResolve(self, entry: IEntry):
        raise NotImplementedError


class NotNeedFrame(IField):
    NeedFrame = False

    def FillResolve(self, entry: IEntry):
        entry.fields[self.fieldKey] = entry.fields.get(self.fieldKey, "undefined")
        return f""

    def DropResolve(self, entry: IEntry):
        raise NotImplementedError


class NeedFrame(IField):
    NeedFrame = True

    def FillResolve(self, entry: IEntry):
        raise NotImplementedError

    def DropResolve(self, entry: IEntry):
        raise NotImplementedError
