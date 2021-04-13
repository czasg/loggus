# loggus

这是一个结构化日志库，使得日志的解析、后续处理、分析或查询变得方便高效。
由于采用结构化，因此可以非常简单的支持JSON样式输出。

> 安装方式
> pip install loggus >= 0.0.21

### `withFieldsAuto`
自动查找变量的名字，并将值映射到fields中，如下：
`packageName`、`packageVersion`两个变量，最终映射为：`{"packageName": "Pywss", "packageVersion": "0.0.21"}`
不支持多次链式调用
```python
import loggus
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
# 输出日志
# time="2021-04-13 20:56:53.907202" level=info msg="0.0" packageName=Pywss packageVersion="0.0.21"
```

### `withFields`
```python
import loggus
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFields({"PackageName": packageName, "PackageVersion": packageVersion}).info("0.0")
# 输出日志
# time="2021-04-13 20:56:53.907202" level=info msg="0.0" PackageName=Pywss PackageVersion="0.0.21"
```

### 设置日志级别
* `loggus.SetLevel(loggus.DEBUG)`
* `loggus.SetLevel(loggus.INFO)`
* `loggus.SetLevel(loggus.WARNING)`
* `loggus.SetLevel(loggus.ERROR)`
* `loggus.SetLevel(loggus.PANIC)`

### 开启JSON日志输出
默认样式为`Text`，可以使用`loggus.SetFormatter(loggus.JsonFormatter)`改变为`Json`样式，目前仅支持两种样式：
* `Text`：`loggus.TextFormatter`
* `Json`：`loggus.JsonFormatter`
```python
import loggus
loggus.SetFormatter(loggus.JsonFormatter)
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
# 输出日志
# {"packageName": "Pywss", "packageVersion": "0.0.21", "time": "2021-04-13 21:17:17.644317", "level": "info", "msg": "0.0"}
```

### 自动匹配函数名、行数、文件名
默认使用`time`、`level`、`msg`三类字段，同样还支持对`funcName`、`lineNo`、`filePath`三类字段的拓展
* 开启函数名：`loggus.OpenFieldKeyFunc()`
* 开启行数：`loggus.OpenFieldKeyLineNo()`
* 开启文件名：`loggus.OpenFieldKeyFile()`
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

### 自定义输出类型
目前包括以下6种输出类型，可以通过`loggus.SetFieldKeys`自由组合匹配
* `loggus.FieldKeyTime`，时间
* `loggus.FieldKeyLevel`，日志级别
* `loggus.FieldKeyMsg`，日志信息
* `loggus.FieldKeyLineNo`，执行行数
* `loggus.FieldKeyFunc`，执行函数名
* `loggus.FieldKeyFile`，执行文件名

```python
import loggus
loggus.SetFieldKeys(loggus.FieldKeyMsg, loggus.FieldKeyLineNo)
packageName = "Pywss"
packageVersion = "0.0.21"
loggus.withFieldsAuto(packageName, packageVersion).info("0.0")
# 日志输出
# msg="0.0" lineNo=5 packageName=Pywss packageVersion="0.0.21"
```

### 日志钩子
目前支持`FileHook`、`RotatingFileHook`两种钩子。

钩子需要从`loggus.hook.IHook`继承，可以非常简单的开发出自定义的钩子。
需要实现两个函数：
* `GetLevels`
* `Fire`
如下为一个简单的http钩子
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

