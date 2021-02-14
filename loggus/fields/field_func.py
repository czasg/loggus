from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "KEY", "FieldFunc"

KEY = "FuncName"


class FieldFunc(IField):

    def ResolveIn(self, entry: IEntry):
        entry.fields[KEY] = entry.frame.FuncName
        return f'{KEY}={entry.frame.FuncName}'

    def ResolveOut(self, entry: IEntry):
        return f'{KEY}={entry.fields.pop(KEY, entry.frame.FuncName)}'
