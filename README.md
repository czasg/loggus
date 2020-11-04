## loggus

This is a log library, you can output json, and pay attention to each fields easy.  

Here is the passage: 
```text
"hello, my name is cza, 18 years old, i graduated from WUST."
```
so, we can use loggrus by this:
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
    loggus.SetFormatter(loggus.JsonFormatter)
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
