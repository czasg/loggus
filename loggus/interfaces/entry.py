from types import CodeType
from loggus.interfaces.logger import IHook


class IEntry:
    logger: IHook
    fields: dict
    frame: CodeType
