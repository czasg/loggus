# -*- coding: utf-8 -*-

__author__ = 'godliam'

import loggus

if __name__ == '__main__':
    la = loggus.GetLogger("logger_a")
    lb = loggus.GetLogger("logger_b")

    la.AddHooks(RotatingFileHook(filename="./log_a.log"))
    lb.AddHooks(RotatingFileHook(filename="./log_b.log"))

    loggus.SetFieldKeys(
        loggus.FieldKeyTime,
        loggus.FieldKeyLevel,
        loggus.FieldKeyMsg,
        loggus.FieldKeyFunc,
        loggus.FieldKeyLineNo,
        loggus.FieldKeyFile,
    )
    loggus.SetFormatter(loggus.JsonFormatter)

    la.info("this is logger A")
    la.withFields({"name": "logger A"}).info("this is a test for multiple logger.")

    lb.info("this is logger B")
    lb.withFields({"name": "logger B"}).info("this is a test for multiple logger.")
