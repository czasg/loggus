from loggus.interfaces.field import IField

__all__ = "KEY", "FieldMsg"

KEY = "msg"


class FieldMsg(IField):

    def GetResolve(self, entry):
        return f'{KEY}={entry.fields.get(KEY, "undefined")}'

    def DropResolve(self, entry):
        return f'{KEY}={entry.fields.pop(KEY, "undefined")}'
