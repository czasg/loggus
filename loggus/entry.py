# coding: utf-8
import os
from loggus.utils.level import *
from loggus.logger import *

from loggus.interfaces.frame import IFrame
from loggus.interfaces.logger import ILogger
from loggus.logger import _logger

from loggus.fields.field_level import KEY as LEVEL_KEY
from loggus.fields.field_time import KEY as TIME_KEY
from loggus.fields.field_msg import KEY as MSG_KEY

# from loggus.fields.field_level import KEY
# from loggus.fields.field_level import KEY
# from loggus.fields.field_level import KEY

__all__ = "Entry",

if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else:
    def currentframe():
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back
_srcfile = os.path.normcase(currentframe.__code__.co_filename)

from collections import namedtuple


def findTest():
    f = currentframe()
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)", None
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        sinfo = None
        rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
        break
    return rv


def NewEntry(logger: ILogger = None, fields=None):
    entry = Entry(logger or _logger)
    if fields:
        try:
            fields = deepcopy(fields)
        except:
            fields = {f"{key}": f"{value}" for key, value in fields.items()}
        finally:
            entry.fields = fields
    return entry


# An entry is the final or intermediate logging entry. It contains all the fields,
# It's finally logged when debug/info/warning/error/panic is called on it.
# these objects can be reused and passed around as much as you wish to avoid field duplication.
class Entry:

    def __init__(self, logger: ILogger):
        self.logger = logger
        self.fields = dict()
        self.frame: IFrame  # judge on logger.frame

    def withField(self, key: Any, value: Any, color: str = None):
        if color and self.logger.colorSwitch and \
                color in (DEBUG_COLOR, INFO_COLOR, WARNING_COLOR, ERROR_COLOR, PANIC_COLOR):
            return self.withFields({key: color.format(value)})
        return self.withFields({key: value})

    def WithField(self, key: Any, value: Any, color: str = None):
        return self.withField(key, value, color)

    def withFields(self, fields: dict):
        try:
            newFields = deepcopy(self.fields)
        except:
            newFields = {f"{key}": f"{value}" for key, value in self.fields.items()}
        newFields.update(fields)
        entry = NewEntry(self.logger)
        entry.fields = newFields
        return entry

    def WithFields(self, fields: dict):
        return self.withFields(fields)

    def withException(self, exception: Exception):
        return self.withField("exception", str(exception), ERROR_COLOR)

    def WithException(self, exception: Exception):
        return self.withException(exception)

    def withTraceback(self):
        return self.withField("traceback", traceback.format_exc().strip(), ERROR_COLOR)

    def WithTraceback(self):
        return self.withTraceback()

    @contextlib.contextmanager
    def withCallback(self, callback: callable = None):
        try:
            yield
        except Exception as e:
            try:
                (callback or (lambda *args: self.withTraceback().error(*args)))(e)
            except Exception as e:
                self.withTraceback().error(e)

    def WithCallback(self, callback: callable = None):
        return self.withCallback(callback)

    def log(self, level: int, *args: Any) -> None:
        """
        ensure fields is a Separate Dict Objects
        :param level:
        :param args:
        :return:
        """
        entry = NewEntry(self.logger, self.fields)
        entry.fields.update({
            LEVEL_KEY: level,
            MSG_KEY: " ".join([f"{arg}" for arg in args]),
        })
        output = entry.logger.formatter.Format(entry)
        entry.logger.out.write(output)

    def Log(self, level: int, *args: Any):
        if self.logger.IsLevelEnabled(level):
            self.log(level, *args)
            if level >= PANIC:
                sys.exit(PANIC)

    def debug(self, *args: Any) -> None:
        self.Log(DEBUG, *args)

    def Debug(self, *args: Any) -> None:
        self.debug(*args)

    def info(self, *args: Any) -> None:
        self.Log(INFO, *args)

    def Info(self, *args: Any) -> None:
        self.info(*args)

    def warning(self, *args: Any) -> None:
        self.Log(WARNING, *args)

    def Warning(self, *args: Any) -> None:
        self.warning(*args)

    def error(self, *args: Any) -> None:
        self.Log(ERROR, *args)

    def Error(self, *args: Any) -> None:
        self.error(*args)

    def panic(self, *args: Any) -> None:
        self.Log(PANIC, *args)

    def Panic(self, *args: Any) -> None:
        self.panic(*args)
