from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "KEY", "FieldFile"

KEY = "FilePath"


class FieldFile(IField):
    key = "filePath"

    @classmethod
    def ResolveIn(cls, entry: IEntry):
        entry.fields[cls.key] = entry.frame.FilePath
        return f'{cls.key}="{entry.frame.FilePath}"'

    @classmethod
    def ResolveOut(cls, entry: IEntry):
        return f'{cls.key}="{entry.fields.pop(cls.key, entry.frame.FilePath)}"'
