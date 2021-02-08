from types import CodeType
from loggus.interfaces.field import IField

__all__ = "KEY", "FieldMsg"

KEY = "msg"


class FieldMsg(IField):

    def GetResolve(self, fields: dict, frame: CodeType = None):
        return f'{KEY}={fields.get(KEY, "undefined")}'

    def DropResolve(self, fields: dict, frame: CodeType = None):
        return f'{KEY}={fields.pop(KEY, "undefined")}'
