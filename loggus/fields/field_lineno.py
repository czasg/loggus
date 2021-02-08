from types import CodeType
from loggus.interfaces.field import IField

__all__ = "KEY", "FieldLineNo"

KEY = "lineNo"


class FieldLineNo(IField):
    NeedFrame = True

    def GetResolve(self, fields: dict, frame: CodeType = None):
        fields[KEY] = frame.co_name
        return f'{KEY}={frame.f_lineno}'

    def DropResolve(self, fields: dict, frame: CodeType = None):
        return f'{KEY}={frame.f_lineno}'
