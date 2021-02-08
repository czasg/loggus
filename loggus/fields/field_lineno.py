from loggus.interfaces.field import IField

__all__ = "KEY", "FieldLineNo"

KEY = "lineNo"


class FieldLineNo(IField):
    NeedFrame = True

    def GetResolve(self, entry):
        entry.fields[KEY] = entry.frame.co_name
        return f'{KEY}={entry.frame.f_lineno}'

    def DropResolve(self, entry):
        return f'{KEY}={entry.frame.f_lineno}'
