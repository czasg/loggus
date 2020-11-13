import loggus


def raise_test():
    raise Exception("test exception")


if __name__ == '__main__':
    loggus.SetLevel(loggus.DEBUG)

    try:
        raise_test()
    except Exception as e:
        loggus.withTraceback().WithException(e).error("test exception")

    loggus.withField("Name", "logger", loggus.DEBUG_COLOR).debug("info color")
    loggus.withField("Name", "logger", loggus.INFO_COLOR).info("info color")
    loggus.withField("Name", "logger", loggus.WARNING_COLOR).warning("info color")
    loggus.withField("Name", "logger", loggus.ERROR_COLOR).error("info color")
    loggus.withField("Name", "logger", loggus.PANIC_COLOR).panic("info color")
