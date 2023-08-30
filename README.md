# loggus
[![PyPI version](https://badge.fury.io/py/loggus.svg)](https://badge.fury.io/py/loggus)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
loggus 是一个基于 Python 的结构化日志库。与原生的 logging 相比，loggus 提炼了部分关键的结构化字段， 同时简化了结构化日志的使用方式，并改进了日志对象回收机制以确保更优的性能。 此外，loggus 还充分利用了 Python 动态语言的特性，实现了一系列独特的功能。

## 快速开始
```python
import loggus  # pip install loggus


# 日志级别
loggus.debug("debug")
loggus.info("info")
loggus.warning("warning")
loggus.error("error")
loggus.panic("panic")  # 程序退出 sys.exit(50)


# 结构化日志
loggus.update({"name":"log", "func": "test"}).info("info")
loggus.update(name="log", func="test").info("info")


# 变量解析
name = "log"
funcName = "test"
loggus.variables(name, funcName).info("info")


# 异常traceback
try:
    raise
expect:
    loggus.traceback()


# 异常trycache
with loggus.trycache():
    raise 


# 自定义Logger（注意：loggus初始化配置将不生效，配置内容见下）
logger = loggus.GetLogger(__name__)
```

## 基础配置
```python
import loggus


# 开启/关闭日志颜色
loggus.OpenColor()  # 默认
loggus.CloseColor()


# 设置日志级别
loggus.SetLevel(loggus.INFO)  # 默认
loggus.SetLevel(loggus.ERROR)


# 设置日志格式
loggus.SetFormatter(loggus.TextFormatter)  # 默认
loggus.SetFormatter(loggus.JsonFormatter)  # Json格式


# 日志钩子
class LogHook(loggus.IHook):
    def GetLevels(self) -> list:
        return [loggus.DEBUG]
    def Fire(self, entry, level, msg, output) -> None:
        print(entry, level, msg)
loggus.AddHooks(LogHook())
```
