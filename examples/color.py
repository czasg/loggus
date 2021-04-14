# coding: utf-8
import loggus

if __name__ == '__main__':
    loggus.SetLevel(loggus.DEBUG)

    try:
        raise Exception("test exception")
    except Exception as e:
        loggus.withFieldTrace().error("test exception")

    loggus.withField("Name", "logger", loggus.DEBUG).debug("info color")
    loggus.withField("Name", "logger", loggus.INFO).info("info color")
    loggus.withField("Name", "logger", loggus.WARNING).warning("info color")
    loggus.withField("Name", "logger", loggus.ERROR).error("info color")
    loggus.withField("Name", "logger", loggus.PANIC).panic("info color")
