# coding: utf-8
import gc

from datetime import datetime
from queue import Queue
from typing import Any

EntryQueue = Queue(1024)

TextFormatter = object()
JsonFormatter = object()


class Logger:

    def __init__(self):
        self.format = ""

    def SetLevel(self):
        pass

    def AddHook(self):
        pass

    def SetFormatter(self):
        pass


_logger = Logger()


def SetLevel():
    pass


def SetFormatter():
    pass


class Entry:

    def __init__(self, logger: Logger):
        self.logger = logger or _logger
        self.fields = dict()
        self.fields_text = ""

    def WithField(self, key: str, value: Any):
        return self.WithFields({key: value})

    def WithFields(self, fields: dict):
        self.fields.update(fields)
        for key, value in self.fields.items():
            if isinstance(value, str):
                self.fields_text += f"{key}=\"{value}\"" if " " in value else f"{key}={value}"
            elif isinstance(value, Exception):
                self.fields_text += f"{key}=\"[####@ {value} @####]\""
            elif isinstance(value, datetime):
                self.fields_text += f"{key}=\"{value}\""
            else:
                self.fields_text += f"{key}={value}"
        return self

    def __del__(self):
        self.fields = dict()
        self.fields_text = "delete"
        try:
            EntryQueue.put_nowait(self)
        except:
            del self


def NewEntry():
    try:
        entry = EntryQueue.get_nowait()
    except:
        return Entry(_logger)
    else:
        return entry


def WithField(key: str, value: Any) -> Entry:
    entry = NewEntry()
    return entry.WithField(key, value)


def WithFields(fields: dict) -> Entry:
    entry = NewEntry()
    return entry.WithFields(fields)
