from types import CodeType
from datetime import datetime
from loggus.interfaces.field import IField

__all__ = "KEY", "FieldTime"

KEY = "time"


class FieldTime(IField):

    def GetResolve(self, fields: dict, frame: CodeType = None):
        return f'{KEY}="{fields.get(KEY, datetime.now())}"'

    def DropResolve(self, fields: dict, frame: CodeType = None):
        return f'{KEY}="{fields.pop(KEY, datetime.now())}"'
