from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "KEY", "FieldFile"

KEY = "FilePath"


class FieldFile(IField):

    def ResolveIn(self, entry: IEntry):
        entry.fields[KEY] = entry.frame.FilePath
        return f'{KEY}="{entry.frame.FilePath}"'

    def ResolveOut(self, entry: IEntry):
        return f'{KEY}="{entry.fields.pop(KEY, entry.frame.FilePath)}"'
