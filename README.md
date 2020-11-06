## loggus

This is a log library, you can output json, and pay attention to each fields easy.

### Json && Fields
Here is the passage: 
```text
"hello, my name is cza, 18 years old, i graduated from WUST."
```
so, we can use loggus by this:
```python
import loggus

if __name__ == '__main__':
    loggus.WithFields({
        "name": "cza",
        "age": 18,
        "GraduateSchool": "WUST",
    }).Info("hello")
```
you will get:
```text
time="2020-11-04 14:36:36.768321" level=info msg=hello name=cza age=18 GraduateSchool=WUST
```
if you want to output json, just set formatter like this:
```python
import loggus

if __name__ == '__main__':
    loggus.SetFormatter(loggus.JsonFormatter)  # set json
    loggus.WithFields({
        "name": "cza",
        "age": 18,
        "GraduateSchool": "WUST",
    }).Info("hello")
```
output like this:
```text
{"name": "cza", "age": 18, "GraduateSchool": "WUST", "time": "2020-11-04 14:38:30.002588", "level": "info", "msg": "hello"}
```

### Hook
you can add hook when level event happen like this:
```python
import loggus

class FileBeat(loggus.IHook):

    def __init__(self):
        self.o = open("loggus.log", "a+", encoding="utf-8")

    def GetLevels(self):  # define trigger level of this hook, like debug/info/warning/error
        return [loggus.INFO, loggus.ERROR]

    def ProcessMsg(self, msg):  # you can write msg into file or msg-queue
        self.o.write(msg)
        self.o.flush()

    def __del__(self):
        self.o.close()


if __name__ == '__main__':
    loggus.AddHook(FileBeat())
    loggus.info("hello info")  # write in file
    loggus.warning("hello warning")  # never trigger
    loggus.error("hello error")  # write in file
```
