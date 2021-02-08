from loggus.interfaces.field import IField

__all__ = "KEY", "FieldLevel"

KEY = "level"


class FieldLevel(IField):

    def GetResolve(self, entry):
        entry.fields[KEY] = entry.fields.get(KEY, "undefined")
        return f'{KEY}={entry.fields[KEY]}'

    def DropResolve(self, entry):
        return f'{KEY}={entry.fields.pop(KEY, "undefined")}'
