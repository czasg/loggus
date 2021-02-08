from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "KEY", "FieldFile"

KEY = "file"


class FieldFile(IField):
    NeedFrame = True

    def GetResolve(self, entry: IEntry):
        entry.fields[KEY] = entry.frame.co_name
        return f'{KEY}={entry.frame.co_filename}'

    def DropResolve(self, entry: IEntry):
        return f'{KEY}={entry.frame.co_filename}'
