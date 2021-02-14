import json

from datetime import datetime
from loggus.interfaces.formatter import IFormatter
from loggus.interfaces.field import IField
from loggus.interfaces.entry import IEntry

__all__ = "JsonFormatter",


class PrettyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return super().default(obj)


# json encoder: forced every obj to str.
class ForcedEncoder(json.JSONEncoder):

    def default(self, obj) -> str:
        return f"{obj}"


class JsonFormatter(IFormatter):

    def Format(self, entry: IEntry) -> str:
        for fieldKey in entry.logger.fieldKeys:  # type: IField
            fieldKey.ResolveIn(entry)
        try:
            output = json.dumps(entry.fields, ensure_ascii=False, cls=PrettyEncoder)
        except:
            output = json.dumps(entry.fields, ensure_ascii=False, cls=ForcedEncoder)
        return output
