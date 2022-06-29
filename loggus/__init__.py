# coding: utf-8
import threading, contextlib, traceback as _traceback
from copy import deepcopy
from typing import List, Dict
from loggus.level import *
from loggus.hooks import *
from loggus.fields import *
from loggus.formatter import *
from loggus.frame import *

__version__ = "0.1.1"
__index_page__ = "https://github.com/czasg/loggus"
__doc_page__ = "https://github.com/czasg/loggus/README.md"
__author__ = "https://czasg.github.io/docusaurus/author/intro"


class Logger:

    def __init__(self):
        self.stream = sys.stdout
        self.formatter = TextFormatter
        self.fieldKeys = [FieldKeyTime, FieldKeyLevel, FieldKeyMsg]
        self.needFrame: bool = False
        self.baseLevel: Level = INFO
        self.colorSwitch: bool = True
        self.hooks: Dict[Level, List[IHook]] = {
            DEBUG: [],
            INFO: [],
            WARNING: [],
            ERROR: [],
            PANIC: [],
        }

    def AddHooks(self, *hooks: List[IHook]) -> None:
        for hook in hooks:  # type: IHook
            if not IsIHook(hook):
                raise Exception(f"undefined Hook[{hook}]!")
            for level in hook.GetLevels():
                if not IsLevel(level):
                    raise Exception(f"undefined Level[{level}]!")
                self.hooks[level].append(hook)

    def SetLevel(self, level: Level) -> None:
        if not IsLevel(level):
            raise Exception(f"undefined Level[{level}]!")
        self.baseLevel = level

    def SetFormatter(self, formatter: [IFormatter, TextFormatter, JsonFormatter]):
        if not IsIFormatter(formatter):
            raise Exception(f"undefined Formatter[{formatter}]")
        if formatter is JsonFormatter:
            self.colorSwitch = False
        self.formatter = formatter

    def CloseColor(self):
        self.colorSwitch = False

    def OpenColor(self):
        self.colorSwitch = True

    def FireHooks(self, entry, level, msg, output) -> None:
        for hook in self.hooks[level]:  # type: IHook
            hook.Fire(entry, level, msg, output)

    def IsLevelEnabled(self, level: Level) -> bool:
        return level >= self.baseLevel

    def Write(self, output: str) -> None:
        self.stream.write(output)
        self.stream.flush()

    def update(self, _: dict = None, **kwargs):
        return NewEntry(self).update(_, **kwargs)

    def variables(self, *args):
        return NewEntry(self).variables(*args, currentframe=currentframe3)

    def traceback(self):
        NewEntry(self).traceback()

    def trycache(self, callback=None, *args, **kwargs):
        return NewEntry(self).trycache(callback, *args, **kwargs)

    def debug(self, *args):
        NewEntry(self).debug(*args)

    def info(self, *args):
        NewEntry(self).info(*args)

    def warning(self, *args):
        NewEntry(self).warning(*args)

    def error(self, *args):
        NewEntry(self).error(*args)

    def panic(self, *args):
        NewEntry(self).panic(*args)


class Entry:

    def __init__(self, logger: Logger):
        self.logger = logger
        self.fields = {}
        self.frameFuncName = None
        self.frameLineNo = None
        self.frameFilePath = None

    def update(self, _: dict = None, **kwargs):
        fields = _ or {}
        fields.update(kwargs)
        entry = NewEntry(self.logger, self.fields)
        entry.fields.update(fields)
        return entry

    def variables(self, *args, currentframe=currentframe2):
        if not args:
            return self
        code = findCallerVariables(currentframe())
        match = varFieldRegex(code)
        if not match:
            self.warning(f"variables regex not match")
            return self
        return self.update(dict(zip([field.strip() for field in match.group(1).split(",")], args)))

    def traceback(self):
        self.update(error=_traceback.format_exc().strip()).error("traceback")

    @contextlib.contextmanager
    def trycache(self, callback=None, *args, **kwargs):
        try:
            yield self
        except Exception as e:
            if callback:
                try:
                    callback(e, *args, **kwargs)
                except:
                    pass
            self.traceback()

    def _log(self, level: Level, msg: str):
        entry = NewEntry(self.logger, self.fields)
        output = entry.logger.formatter.Format(entry, level, msg)
        entry.logger.FireHooks(entry, level, msg, output)
        entry.logger.Write(output)

    def log(self, level: Level, msg: str):
        self._log(level, msg)
        if level >= PANIC:
            sys.exit(PANIC.value)

    def debug(self, *args):
        if self.logger.IsLevelEnabled(DEBUG):
            self.log(DEBUG, " ".join([f"{arg}" for arg in args]))

    def info(self, *args):
        if self.logger.IsLevelEnabled(INFO):
            self.log(INFO, " ".join([f"{arg}" for arg in args]))

    def warning(self, *args):
        if self.logger.IsLevelEnabled(WARNING):
            self.log(WARNING, " ".join([f"{arg}" for arg in args]))

    def error(self, *args):
        if self.logger.IsLevelEnabled(ERROR):
            self.log(ERROR, " ".join([f"{arg}" for arg in args]))

    def panic(self, *args):
        if self.logger.IsLevelEnabled(PANIC):
            self.log(PANIC, " ".join([f"{arg}" for arg in args]))


# func
NewLogger = lambda: Logger()
AddHooks = lambda *hooks: _logger.AddHooks(*hooks)
SetLevel = lambda level: _logger.SetLevel(level)
SetFormatter = lambda formatter: _logger.SetFormatter(formatter)
CloseColor = lambda: _logger.CloseColor()
OpenColor = lambda: _logger.OpenColor()
# entry
debug = lambda *args: NewEntry().debug(*args)
info = lambda *args: NewEntry().info(*args)
warning = lambda *args: NewEntry().warning(*args)
error = lambda *args: NewEntry().error(*args)
panic = lambda *args: NewEntry().panic(*args)
update = lambda _=None, **kwargs: NewEntry().update(_, **kwargs)
variables = lambda *args: NewEntry().variables(*args, currentframe=currentframe3)
traceback = lambda: NewEntry().traceback()
trycache = lambda callback=None, *args, **kwargs: NewEntry().trycache(callback, *args, **kwargs)
# logger
_logger = NewLogger()
_loggerPool = {None: _logger}
_lock = threading.Lock()


def GetLogger(name: str = None):
    with _lock:
        if name not in _loggerPool:
            _loggerPool[name] = NewLogger()
        return _loggerPool[name]


def NewEntry(logger=_logger, fields=None):
    entry = Entry(logger)
    if fields:
        try:
            fields = deepcopy(fields)
        except:
            fields = {f"{key}": f"{value}" for key, value in fields.items()}
        entry.fields = fields
    return entry
