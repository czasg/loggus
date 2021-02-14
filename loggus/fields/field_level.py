from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "KEY", "FieldLevel"

KEY = "level"


class FieldLevel(IField):

    def ResolveIn(self, entry: IEntry):
        entry.fields[KEY] = entry.fields.get(KEY, "undefined")
        return f'{KEY}={entry.fields[KEY]}'

    def ResolveOut(self, entry: IEntry):
        return f'{KEY}={entry.fields.pop(KEY, "undefined")}'
