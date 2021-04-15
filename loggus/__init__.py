# coding: utf-8
import sys
import inspect
import traceback
import contextlib

from copy import deepcopy
from typing import List, Dict

from loggus.level import *
from loggus.hooks import *
from loggus.fields import *
from loggus.formatter import *

# fix messy code when output color in win32.
if sys.platform == "win32":
    import colorama

    colorama.init(autoreset=True)

if hasattr(sys, '_getframe'):
    currentframe2 = lambda: sys._getframe(2)
    currentframe3 = lambda: sys._getframe(3)
else:
    def currentframe2():
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back.f_back


    def currentframe3():
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back.f_back.f_back


def FindCaller():
    f = currentframe3()
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", "(unknown line)", "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break
    return rv


autoCallerName = "withFieldsAuto"
autoFieldRegex = re.compile(autoCallerName + "\s*\((.*?)(?:$|\))", re.S).search
autoSubRegex = re.compile("[^a-zA-Z0-9.]").sub


# TODO: How to auto parse fields from input， like `withFieldsAuto(self.getName(), self.getAge())`
def FindCallerAuto(frame):
    if inspect.istraceback(frame):
        lineno = frame.tb_lineno
        frame = frame.tb_frame
    else:
        lineno = frame.f_lineno
    if not inspect.isframe(frame):
        raise TypeError('{!r} is not a frame or traceback object'.format(frame))
    start = lineno - 1
    try:
        lines, lnum = inspect.findsource(frame)
    except OSError:
        return ""
    else:
        start = max(0, min(start, len(lines) - 1))
        codes = ""
        for index in range(start, 0, -1):
            line = lines[index]
            codes = line + codes
            if autoCallerName in line:
                break
        return codes


varCallerName = "withVariables"
varFieldRegex = re.compile(varCallerName + "\s*\((.*?)(?:$|\))", re.S).search


def FindCallerVariables(frame):
    if inspect.istraceback(frame):
        lineno = frame.tb_lineno
        frame = frame.tb_frame
    else:
        lineno = frame.f_lineno
    if not inspect.isframe(frame):
        raise TypeError('{!r} is not a frame or traceback object'.format(frame))
    start = lineno - 1
    try:
        lines, lnum = inspect.findsource(frame)
    except OSError:
        return ""
    else:
        start = max(0, min(start, len(lines) - 1))
        codes = ""
        for index in range(start, 0, -1):
            line = lines[index]
            codes = line + codes
            if varCallerName in line:
                break
        return codes


_srcfile = os.path.normcase(FindCaller.__code__.co_filename)


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

    def FireHooks(self, entry, level, msg, output) -> None:
        for hook in self.hooks[level]:  # type: IHook
            hook.Fire(entry, level, msg, output)

    def IsLevelEnabled(self, level: Level) -> bool:
        return level >= self.baseLevel

    def SetLevel(self, level: Level) -> None:
        if not IsLevel(level):
            raise Exception(f"undefined Level[{level}]!")
        self.baseLevel = level

    def SetFormatter(self, formatter: IFormatter):
        if not IsIFormatter(formatter):
            raise Exception(f"undefined Formatter[{formatter}]")
        if formatter is JsonFormatter:
            self.colorSwitch = False
        self.formatter = formatter

    def SetFieldKeys(self, *fieldKeys):
        fields = []
        for fieldKey in fieldKeys:
            if not IsIField(fieldKey):
                raise Exception(f"undefined Field[{fieldKey}]!")
            fields.append(fieldKey)
        if fields:
            self.fieldKeys = fields
        if {FieldKeyFunc, FieldKeyLineNo, FieldKeyFile} & {*self.fieldKeys}:
            self.needFrame = True
        else:
            self.needFrame = False

    def OpenFieldKeyFunc(self):
        if FieldKeyFunc not in self.fieldKeys:
            self.fieldKeys.append(FieldKeyFunc)
        self.needFrame = True

    def OpenFieldKeyLineNo(self):
        if FieldKeyLineNo not in self.fieldKeys:
            self.fieldKeys.append(FieldKeyLineNo)
        self.needFrame = True

    def OpenFieldKeyFile(self):
        if FieldKeyFile not in self.fieldKeys:
            self.fieldKeys.append(FieldKeyFile)
        self.needFrame = True

    def Write(self, output: str) -> None:
        self.stream.write(output)
        self.stream.flush()

    def NewEntry(self):
        return NewEntry(self)

    def withField(self, key, value, colorLevel=None):
        entry = self.NewEntry()
        return entry.withField(key, value, colorLevel)

    def withFields(self, fields: dict):
        entry = self.NewEntry()
        return entry.withFields(fields)

    def withVariables(self, *args):
        entry = self.NewEntry()
        return entry.withVariables(*args)

    def withFieldsAuto(self, *args):
        entry = self.NewEntry()
        return entry.withFieldsAuto(*args)

    def withFieldTrace(self):
        entry = self.NewEntry()
        return entry.withFieldTrace()

    def withTraceback(self, callback=None, *args, **kwargs):
        entry = self.NewEntry()
        return entry.withTraceback(callback, *args, **kwargs)

    def debug(self, *args):
        entry = self.NewEntry()
        entry.debug(*args)

    def info(self, *args):
        entry = self.NewEntry()
        entry.info(*args)

    def warning(self, *args):
        entry = self.NewEntry()
        entry.warning(*args)

    def error(self, *args):
        entry = self.NewEntry()
        entry.error(*args)

    def panic(self, *args):
        entry = self.NewEntry()
        entry.panic(*args)


def NewLogger():
    return Logger()


def SetLevel(level: Level) -> None:
    _logger.SetLevel(level)


def SetFormatter(formatter: TextFormatter or JsonFormatter):
    _logger.SetFormatter(formatter)


def OpenFieldKeyFunc():
    _logger.OpenFieldKeyFunc()


def OpenFieldKeyLineNo():
    _logger.OpenFieldKeyLineNo()


def OpenFieldKeyFile():
    _logger.OpenFieldKeyFile()


def SetFieldKeys(*fieldKeys):
    _logger.SetFieldKeys(*fieldKeys)


def CloseColor():
    _logger.colorSwitch = False


def OpenColor():
    _logger.colorSwitch = True


def AddHook(*hooks):
    _logger.AddHooks(*hooks)


_logger = NewLogger()


class Entry:

    def __init__(self, logger: Logger):
        self.logger = logger
        self.fields = {}
        self.frameFuncName = None
        self.frameLineNo = None
        self.frameFilePath = None

    def withField(self, key, value, colorLevel: Level = None):
        if colorLevel and self.logger.colorSwitch:
            value = colorLevel.toColor(value)
        return self.withFields({key: value})

    def withFields(self, fields: dict):
        if not isinstance(fields, dict):
            raise Exception(f"unsupported {type(fields)}")
        entry = NewEntry(self.logger, self.fields)
        entry.fields.update(fields)
        return entry

    def withVariables(self, *args):
        if not args:
            return self
        code = FindCallerVariables(currentframe2())
        match = varFieldRegex(code)
        if not match:
            self.debug(f"{code} [regex not match?]")
            return self
        return self.withFields(dict(zip([field.strip() for field in match.group(1).split(",")], args)))

    def withFieldsAuto(self, *args):
        if not args:
            return self
        code = FindCallerAuto(currentframe2())
        match = autoFieldRegex(code)
        if not match:
            self.debug(f"{code} [regex not match?]")
            return self
        return self.withFields(dict(zip([autoSubRegex("", field) for field in match.group(1).split(",")], args)))

    def withFieldTrace(self):
        return self.withField("traceback", traceback.format_exc().strip(), ERROR)

    @contextlib.contextmanager
    def withTraceback(self, callback=None, *args, **kwargs):
        try:
            yield
        except Exception as e:
            if callback:
                try:
                    callback(e, *args, **kwargs)
                except:
                    pass
            self.withFieldTrace().error("an error occurred.")

    def log(self, level: Level, msg: str):
        entry = NewEntry(self.logger, self.fields)
        if entry.logger.needFrame:
            entry.frameFilePath, entry.frameLineNo, entry.frameFuncName, = FindCaller()
        output = entry.logger.formatter.Format(entry, level, msg)
        entry.logger.FireHooks(entry, level, msg, output)
        entry.logger.Write(output)

    def Log(self, level: Level, msg: str):
        if self.logger.IsLevelEnabled(level):
            self.log(level, msg)
            if level >= PANIC:
                sys.exit(PANIC.value)

    def debug(self, *args):
        self.Log(DEBUG, " ".join([f"{arg}" for arg in args]))

    def info(self, *args):
        self.Log(INFO, " ".join([f"{arg}" for arg in args]))

    def warning(self, *args):
        self.Log(WARNING, " ".join([f"{arg}" for arg in args]))

    def error(self, *args):
        self.Log(ERROR, " ".join([f"{arg}" for arg in args]))

    def panic(self, *args):
        self.Log(PANIC, " ".join([f"{arg}" for arg in args]))


def NewEntry(logger: Logger = _logger, fields=None):
    entry = Entry(logger)
    if fields:
        try:
            fields = deepcopy(fields)
        except:
            fields = {f"{key}": f"{value}" for key, value in fields.items()}
        entry.fields = fields
    return entry


def withField(key, value, color: str = None) -> Entry:
    return NewEntry().withField(key, value, color)


def withFields(fields: dict) -> Entry:
    return NewEntry().withFields(fields)


def withVariables(*args) -> Entry:
    if not args:
        return NewEntry()
    code = FindCallerVariables(currentframe2())
    match = varFieldRegex(code)
    if not match:
        debug(f"{code} [regex not match?]")
        return NewEntry()
    return NewEntry().withFields(dict(zip([field.strip() for field in match.group(1).split(",")], args)))


def withFieldsAuto(*args) -> Entry:
    if not args:
        return NewEntry()
    code = FindCallerAuto(currentframe2())
    match = autoFieldRegex(code)
    if not match:
        debug(f"{code} [regex not match?]")
        return NewEntry()
    return NewEntry().withFields(dict(zip([autoSubRegex("", field) for field in match.group(1).split(",")], args)))


def withFieldTrace():
    return NewEntry().withFieldTrace()


def withTraceback(callback=None, *args, **kwargs):
    return NewEntry().withTraceback(callback, *args, **kwargs)


def debug(*args) -> None:
    entry = NewEntry()
    entry.debug(*args)


def info(*args) -> None:
    entry = NewEntry()
    entry.info(*args)


def warning(*args) -> None:
    entry = NewEntry()
    entry.warning(*args)


def error(*args) -> None:
    entry = NewEntry()
    entry.error(*args)


def panic(*args) -> None:
    entry = NewEntry()
    entry.panic(*args)
