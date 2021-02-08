from datetime import datetime
from loggus.interfaces.field import IField

__all__ = "KEY", "FieldTime"

KEY = "time"


class FieldTime(IField):

    def GetResolve(self, entry):
        return f'{KEY}="{entry.fields.get(KEY, datetime.now())}"'

    def DropResolve(self, entry):
        return f'{KEY}="{entry.fields.pop(KEY, datetime.now())}"'
