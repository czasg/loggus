from datetime import datetime
from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "KEY", "FieldTime"

KEY = "time"


class FieldTime(IField):

    def ResolveIn(self, entry: IEntry):
        return f'{KEY}="{entry.fields.get(KEY, datetime.now())}"'

    def ResolveOut(self, entry: IEntry):
        return f'{KEY}="{entry.fields.pop(KEY, datetime.now())}"'
