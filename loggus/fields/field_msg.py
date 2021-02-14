from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "KEY", "FieldMsg"

KEY = "msg"


class FieldMsg(IField):

    def ResolveIn(self, entry: IEntry):
        return f'{KEY}={entry.fields.get(KEY, "undefined")}'

    def ResolveOut(self, entry: IEntry):
        return f'{KEY}={entry.fields.pop(KEY, "undefined")}'
