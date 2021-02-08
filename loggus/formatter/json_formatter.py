import json

from datetime import datetime
from loggus.interfaces.formatter import IFormatter
from loggus.interfaces.field import IField

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

    def Format(self, entry) -> str:
        output = ""
        for fieldKey in entry.logger.fieldKeys:  # type: IField
            fieldKey.GetResolve(entry)

        return output
