from loggus.interfaces.field import IField

__all__ = "KEY", "FieldFunc"

KEY = "funcName"


class FieldFunc(IField):
    NeedFrame = True

    def GetResolve(self, entry):
        entry.fields[KEY] = entry.frame.co_name
        return f'{KEY}={entry.frame.co_name}'

    def DropResolve(self, entry):
        return f'{KEY}={entry.frame.co_name}'
