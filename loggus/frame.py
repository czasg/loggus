# coding: utf-8
import re, sys, inspect, colorama

if sys.platform == "win32":
    colorama.init(autoreset=True)

if hasattr(sys, '_getframe'):
    currentframe2 = lambda: sys._getframe(2)
    currentframe3 = lambda: sys._getframe(3)
else:
    def currentframe2():
        try:
            raise
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back.f_back
    def currentframe3():
        try:
            raise
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back.f_back.f_back

varCallerName = "variables"
varFieldRegex = re.compile(varCallerName + "\s*\((.*?)(?:$|\))", re.S).search


def findCallerVariables(frame):
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
