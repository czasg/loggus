# loggus

This is a structured log like `logrus`.

But it adds some Python-specific elements, like `withVariables...`

> install
> `pip install loggus`

there are some examples.

## `withVariables`
```python
import loggus
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withVariables(packageName, packageVersion).info("0.0")

loggus.SetFormatter(loggus.JsonFormatter)
loggus.withVariables(packageName, packageVersion).info("0.0")
```
```text
time="2021-04-13 20:56:53.907202" level=info msg="0.0" packageName=Pywss packageVersion="0.0.21"

{"packageName": "Pywss", "packageVersion": "0.0.21", "time": "2021-05-10 20:11:38.349320", "level": "info", "msg": "0.0"}
```

## `withFields`
```python
import loggus
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFields({"PackageName": packageName, "PackageVersion": packageVersion}).info("0.0")
```
```text
time="2021-04-13 20:56:53.907202" level=info msg="0.0" PackageName=Pywss PackageVersion="0.0.21"
```

## loggus.SetLevel
* `loggus.SetLevel(loggus.DEBUG)`
* `loggus.SetLevel(loggus.INFO)`
* `loggus.SetLevel(loggus.WARNING)`
* `loggus.SetLevel(loggus.ERROR)`
* `loggus.SetLevel(loggus.PANIC)`

## Add `FuncName`、`LineNo`、`FilePath`
* Add FuncName：`loggus.OpenFieldKeyFunc()`
* Add LineNo：`loggus.OpenFieldKeyLineNo()`
* Add FilePath：`loggus.OpenFieldKeyFile()`
```python
import loggus
loggus.OpenFieldKeyFunc()
loggus.OpenFieldKeyLineNo()
loggus.OpenFieldKeyFile()
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
```
```text
time="2021-04-13 21:23:50.113213" level=info msg="0.0" funcName=<module> lineNo=7 filePath=xxx.py packageName=Pywss packageVersion="0.0.21"
```

## Fields support free combination
* `loggus.FieldKeyTime`，time
* `loggus.FieldKeyLevel`，level
* `loggus.FieldKeyMsg`，msg
* `loggus.FieldKeyLineNo`，lineNo
* `loggus.FieldKeyFunc`，funcName
* `loggus.FieldKeyFile`，filePath

```python
import loggus
loggus.SetFieldKeys(loggus.FieldKeyMsg, loggus.FieldKeyLineNo)
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
```
```text
msg="0.0" lineNo=5 packageName=Pywss packageVersion="0.0.21"
```

## hook
* `GetLevels`
* `Fire`
```python
import loggus
import requests

from loggus.hooks import IHook

class HttpHook(IHook):

    def GetLevels(self):
        return [loggus.INFO]

    def Fire(self, entry, level, msg, output) -> None:
        requests.post("url", json={"log": output.strip()})


if __name__ == "__main__":
    loggus.AddHook(HttpHook())
    loggus.info("test")
```

#### FileHook
```python
import loggus

from loggus.hooks import FileHook


if __name__ == '__main__':
    loggus.AddHook(FileHook("FileHook.log"))
    for index in range(100):
        loggus.info(index)
```

#### RotatingFileHook
```python
import loggus

from loggus.hooks import RotatingFileHook


if __name__ == '__main__':
    loggus.AddHook(RotatingFileHook("RotatingFileHook.log", maxBytes=1024, backupCount=3))
    for index in range(100):
        loggus.info(index)
```

#### TimedRotatingFileHook
```python
import time
import loggus

from loggus.hooks import TimedRotatingFileHook


if __name__ == '__main__':
    loggus.AddHook(TimedRotatingFileHook("TimedRotatingFileHook.log", when="s", interval=5, backupCount=1))
    for index in range(100):
        time.sleep(0.5)
        loggus.info(index)
```