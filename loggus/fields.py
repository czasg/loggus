# coding: utf-8
import inspect

from datetime import datetime


# msg field key
class FieldKey:

    def __init__(self, name, default):
        self.name = name
        self.default = default

    def GetDefault(self):
        if inspect.isfunction(self.default):
            return self.default()
        else:
            return self.default

    def GetJsonValue(self):
        return

    def GetTextValue(self, fields: dict):
        value = fields.pop(self.name, None)
        if value is None:
            value = self.GetDefault()
        if regex.search(f"{value}"):
            value = f"\"{value}\""
        return f"{self.name}={value} "


FieldKeyTime: object = FieldKey('time', datetime.now)
FieldKeyLevel: object = FieldKey("level", "undefined")
FieldKeyMsg: object = FieldKey("msg", "undefined")
FieldKeyFuncName: object = FieldKey("funcName", "undefined")
FieldKeyLineNo: object = FieldKey("lineNo", "undefined")
FieldKeyFile: object = FieldKey("file", "undefined")
