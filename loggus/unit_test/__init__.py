# coding: utf-8
import os
import sys
import time
import loggus
import inspect
import colorama
import importlib

from threading import RLock


def TryImportModule(module: str, dir=None):
    try:
        return importlib.import_module(module)
    except:
        if dir is None:
            dir = os.path.dirname(".").replace(".\\", "").replace("\\", "")
    pass


# collect & count all samples.
class Collector:
    allSample = 0
    passSample = 0
    failSample = 0
    lock = RLock()

    def addSample(self):
        with self.lock:
            self.allSample += 1

    def addPassSample(self):
        with self.lock:
            self.passSample += 1
            self.addSample()

    def addFailSample(self):
        with self.lock:
            self.failSample += 1
            self.addSample()

    def show(self):
        print(f"""
 --------------- 

TotalCases: {self.allSample}
pass: {self.passSample}
fail: {self.failSample}

""")
        if self.failSample:
            print(colorama.Fore.RED + f"Test Failed")
            print(colorama.Style.RESET_ALL)
            sys.exit(loggus.PANIC)
        else:
            print(colorama.Fore.GREEN + f"Test Pass")
            print(colorama.Style.RESET_ALL)
            sys.exit(0)


collector = Collector()


# hook for info.
class CollectorPassHook(loggus.IHook):

    def GetLevels(self):
        return [loggus.INFO]

    def ProcessMsg(self, msg):
        collector.addPassSample()


# hook for error.
class CollectorFailHook(loggus.IHook):

    def GetLevels(self):
        return [loggus.ERROR]

    def ProcessMsg(self, msg):
        collector.addFailSample()


# new logger, it is safe for loggus.
logger = loggus.NewLogger()
logger.AddHook(CollectorPassHook())
logger.AddHook(CollectorFailHook())
# bind this logger for entry.
entry = loggus.NewEntry(logger)


# create a py test file.
def create(pyfile: str):
    if not os.path.isfile(pyfile):
        loggus.panic(f"there is not a file: <{pyfile}>.")
    if os.path.dirname(pyfile):
        loggus.panic("can't found file in current dir.")

    pyfile = pyfile.replace(".py", "")
    try:
        module = importlib.import_module(pyfile)
    except:
        loggus.withTraceback().panic("ImportModuleErr")
        return
    template = f"""# coding: utf-8
import loggus

from {pyfile} import *

"""
    for attr in dir(module):
        if attr.startswith(("_", "UnitTest")):
            continue
        attrIns = getattr(module, attr)
        if not inspect.isfunction(attrIns):
            loggus.debug(f"ignore self attr<{attr}>")
            continue
        if hasattr(attrIns, "__module__") and attrIns.__module__ != pyfile:
            loggus.withField("module", attrIns.__module__).warning(f"ignore other module attr<{attr}>")
            continue
        sig = inspect.signature(attrIns)
        parameters = []
        argsKeys = []
        argsValues = []
        for k, v in sig.parameters.items():
            argsKeys.append(k)
            if v.kind == v.POSITIONAL_ONLY:
                argsValues.append(k)
            elif v.kind == v.POSITIONAL_OR_KEYWORD:
                argsValues.append(k)
            elif v.kind == v.VAR_POSITIONAL:
                argsValues.append(f"*{k}")
            elif v.kind == v.KEYWORD_ONLY:
                argsValues.append(f"**{k}")
            elif v.kind == v.VAR_KEYWORD:
                argsValues.append(f"**{k}")
            if v.annotation is sig.empty:
                parameters.append(
                    "                {},".format(
                        {k: {"kind": v.kind.__str__()}}))
            else:
                parameters.append(
                    "                {},".format(
                        {k: {"kind": v.kind.__str__(), "type": f"{v.annotation}"}}))
        argsKeys = ", ".join(argsKeys)
        if argsKeys:
            argsKeys += " = sample[\"parameters\"]"
        argsValues = ", ".join(argsValues)
        parameters = "\n".join(parameters)
        template += f"""
def UnitTest_{attr}(log: loggus.Entry) -> None:
    entry = log.withField("funcName", "{attr}")
    # test cases.
    samples = [
        {{
            "name": str,
            "parameters": [
{parameters}
            ],
            "want": None,
            "wantErr": bool,
        }},
    ]
    # perform validation.
    for sample in samples[1:]:
        log = entry.withField("sampleName", sample["name"])
        want = None
        try:
            {argsKeys}
            want = {attr}({argsValues})
        except:
            log = log.withTraceback()
            log.info("pass") if sample["wantErr"] else log.error("ExceptionErr")
        else:
            if sample["wantErr"]:
                log.error("Want Err But Pass")
            elif want != sample["want"]:
                log.withFields({{"want": sample["want"], "actual": want}}).error("EqualErr")
            else:
                log.info("pass")\n
"""
        loggus.info(f"add attr<{attr}> successful")

    def ensureUnique(src: str) -> None:
        if os.path.exists(src):
            while True:
                dst = f"{src}.{int(time.time())}.bak"
                if os.path.exists(dst):
                    continue
                os.rename(src, dst)
                break

    ensureUnique(f"{pyfile}_test.py")
    with open(f"{pyfile}_test.py", "w", encoding="utf-8") as f:
        f.write(template)
    loggus.info("create unit test file successful~")


# scan all test module in current dir.
def scan():
    for path, dirs, files in os.walk("."):
        for file in files:
            if not file.endswith("_test.py"):
                continue
            actual = os.path.join(path, file)
            print(f">>> found unittest file {actual}:")
            modulePath = os.path.abspath(os.path.dirname(actual))
            sys.path.append(modulePath)
            module = actual. \
                replace(".\\", ""). \
                replace("\\", "."). \
                replace(".py", "")
            log = entry.withField("module", module)
            try:
                module = importlib.import_module(module)
                for attr in dir(module):
                    if attr.startswith("UnitTest_"):
                        getattr(module, attr)(log)
            except:
                log.withTraceback().panic("TestErr")
            sys.path.remove(modulePath)
    collector.show()
