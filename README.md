# loggus
![Project status](https://img.shields.io/badge/version-0.1.1-green.svg)

基于 python 的结构化日志库。利用 python 动态语言的特性，实现了一些独特功能。

## 如何使用
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
