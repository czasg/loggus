from loggus.interfaces.formatter import IFormatter
from loggus.interfaces.field import IField

__all__ = "TextFormatter",


class TextFormatter(IFormatter):

    def Format(self, entry) -> str:
        output = ""
        for fieldKey in entry.logger.fieldKeys:  # type: IField
            output += fieldKey.DropResolve(entry)
            output += " "
        for key, value in entry.fields.items():
            output += f"{key}={value}"
        return output
