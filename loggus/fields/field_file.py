from types import CodeType
from loggus.interfaces.field import IField

__all__ = "KEY", "FieldFile"

KEY = "file"


class FieldFile(IField):

    def GetResolve(self, fields: dict, frame: CodeType = None):
        fields[KEY] = frame.co_name
        return f'{KEY}={frame.co_filename}'

    def DropResolve(self, fields: dict, frame: CodeType = None):
        return f'{KEY}={frame.co_filename}'
