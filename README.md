## loggus

This is a structured log library, you can pay more attention to each fields easy.

> pip install loggus

### Fields
You are free to select fields for stitching.  
default fields are `time`、`level`、`msg`  
```shell script
>>> loggus.info("test")
time="2021-02-20 21:48:23.832815" level=info msg=test
>>> entry = loggus.withFields({"type": "test"})
>>> entry.info("test")
time="2021-02-20 21:48:23.832815" level=info msg=test type=test
>>> entry = entry.withFields({"from": "test"})
>>> entry.info("test")
time="2021-02-20 21:48:23.832815" level=info msg=test type=test from=test
```

### FieldKey
you can also choose other fields of `funcName`、`lineNo`、`filePath`  
those fieldKeys belong `logger`, you can define `logger` with different fiedKeys.
```shell script
>>> loggus.OpenFieldKeyFunc()
>>> loggus.OpenFieldKeyLineNo()
>>> loggus.OpenFieldKeyFile()
>>> loggus.info("test")
time="2021-02-20 22:01:38.558551" level=info msg=test funcName=test lineNo=16 filePath=D:/workplace/loggus/examples/test.py
```
if you want free combination the default fields, use `loggus.SetFieldKeys`
```shell script
>>> loggus.SetFieldKeys(loggus.FieldKeyTime, loggus.FieldKeyLevel, loggus.FieldKeyMsg, loggus.FieldKeyFunc, loggus.FieldKeyLineNo, loggus.FieldKeyFile)
>>> logger = loggus.NewLogger()
>>> logger.SetFieldKeys(loggus.FieldKeyTime, loggus.FieldKeyLevel)
```

### Level
There are five log levels about `DEBUG`、`INFO`、`WARNING`、`ERROR`、`PANIC`  
```shell script
>>> loggus.SetLevel(loggus.DEBUG)
>>> loggus.SetLevel(loggus.INFO)
>>> loggus.SetLevel(loggus.WARNING)
>>> loggus.SetLevel(loggus.ERROR)
>>> loggus.SetLevel(loggus.PANIC)
>>> loggus.GetAllLevels()
[debug, info, warning, error, panic]
```

### Formatter
choose different Formatter to output text/json, default is `TextFormatter`
```shell script
>>> loggus.SetFormatter(loggus.JsonFormatter)
>>> loggus.withFields({"type": "test"}).info("test")
{"type": "test", "time": "2021-02-20 21:39:38.378230", "level": "info", "msg": "test"}
```

### Hook
Hook should inherit from `loggus.hook.IHook`
```shell script
>>> from loggus.hook import FileHook, RotatingFileHook
>>> logger = logger.NewLogger()
>>> logger.AddHook(FileHook("FileHook.log"))
>>> logger.info("test")
>>> logger = logger.NewLogger()
>>> logger.AddHook(RotatingFileHook("RotatingFileHook.log"))
>>> logger.info("test")
```
you can also define a self-hook easy. just implement `GetLevels` and `Fire`  
* GetLevels: trigger level.
* Fire:
    * entry: entry instance.
    * level: loggus.Level.
    * msg: original msg.
    * output: final msg, end of `\n`
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
