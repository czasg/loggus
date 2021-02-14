# coding: utf-8
from loggus.interfaces.frame import IFrame
from loggus.interfaces.logger import ILogger


class IEntry:
    logger: ILogger
    fields: dict
    frame: IFrame
