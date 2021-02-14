from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "KEY", "FieldLineNo"

KEY = "LineNo"


class FieldLineNo(IField):

    def ResolveIn(self, entry: IEntry):
        entry.fields[KEY] = entry.frame.LineNo
        return f'{KEY}={entry.frame.LineNo}'

    def ResolveOut(self, entry: IEntry):
        return f'{KEY}={entry.fields.pop(KEY, entry.frame.LineNo)}'
