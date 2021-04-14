# loggus

This is a structured log library that makes parsing, subsequent processing, analysis, or querying of logs easy and efficient.

Because of the structure, it is very easy to support JSON style output.



> installation mode
> PIP install loggus >= 0.0.21



## `withFieldsAuto`

Automatically find the name of the variable and map the value to Fields as follows:  
The final mapping is: '{"packageName": "Pywss", "packageVersion": "0.0.21"}'  
In this function, functions such as multiple calls and line wrapping are supported
```python
import loggus
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
# output log
# time="2021-04-13 20:56:53.907202" level= INFO MSG ="0.0" packageName= "PyWSS packageText ="0.0.21"
```

## `withFields`
```python
import loggus
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFields({" PackageName ": packageName," PackageVersion ": packageVersion}).info("0.0")
# output log
# time="2021-04-13 20:56:53.907202" level= INFO MSG ="0.0" packageName =" PyWSS packageText ="0.0.21"
```

## Set the log level
* `loggus.SetLevel(loggus.DEBUG)`
* `loggus.SetLevel(loggus.INFO)`
* `loggus.SetLevel(loggus.WARNING)`
* `loggus.SetLevel(loggus.ERROR)`
* `loggus.SetLevel(loggus.PANIC)`

## Customize the output log color
1. Turn off the log color: 'loggus.closecolor ()'  
2, open the log color: 'loggus.opencolor ()'  
In addition, users can customize the output color of the 'field' by 'loggus. Withfield'. There is no uniform color style in the 'JSON' style
```python
import loggus
loggus.withField("Name", "logger", loggus.INFO).info("info color")
loggus.withField("Name", "logger", loggus.WARNING).warning("warn color")
loggus.withField("Name", "logger", loggus.ERROR).error("error color")
loggus.withField("Name", "logger", loggus.PANIC).panic("panic color")
```

## Enables JSON logging output
The default style is' Text ', which can be changed to 'Json' using 'loggus. setFormatter' (loggus. jsonFormatter) '.
* ` Text ` : ` loggus. TextFormatter `
* ` Json ` : ` loggus. JsonFormatter `
```python
import loggus
loggus.SetFormatter(loggus.JsonFormatter)
packageName = "Pywss"
PackageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
# output log
# {" packageName ":" Pywss ", "packageVersion" : "0.0.21", "time", "the 2021-04-13 21:17:17. 644317", "level" : "info", "MSG" : "0.0"}
```

## Match function name, line count, file name automatically  
The default use of 'time', 'level' and 'MSG' is supported, and extensions to 'funcName', 'lineNo' and 'filePath' are also supported
* Open the function name: 'loggus.OpenFieldKeyFunc()'
* open the lines of: ` loggus. OpenFieldKeyLineNo ` ()
* Open the file name: 'loggus.OpenFieldKeyFile()'
```python
import loggus
loggus.OpenFieldKeyFunc()
loggus.OpenFieldKeyLineNo()
loggus.OpenFieldKeyFile()
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
# 日志输出
# time="2021-04-13 21:23:50.113213" level=info msg="0.0" funcName=<module> lineNo=7 filePath=xxx.py packageName=Pywss packageVersion="0.0.21"
```

## Customize output type
The following six types of output are currently included, which can be matched by a free combination of 'loggus.SetFieldKeys'
* 'loggus.FieldKeyTime', time
* 'loggus.FieldKeyLevel', log level
* 'loggus.FieldKeyMsg', log information
* 'loggus.FieldKeyLineNo', number of rows executed
* 'loggus. fieldKeyFunc', the name of the execution function
* 'loggus.FieldKeyFile', the file name of the execution
```python
import loggus
loggus.SetFieldKeys(loggus.FieldKeyMsg, loggus.FieldKeyLineNo)
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
# log output
# msg="0.0" lineNo=5 packageName=Pywss packageVersion="0.0.21"
```

## Log hooks
Currently support 'FileHook', 'RotatingFileHook' two hooks.  
The hook needs to inherit from 'loggus.hook. Ihook'. It is very easy to develop a custom hook.  
You need to implement two functions:
* `GetLevels`
* `Fire`
Here is a simple HTTP hook
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