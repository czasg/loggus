import loggus


class Test:
    pass


unsupported = {"unsupported", "json", "obj"}

if __name__ == '__main__':
    loggus.SetFormatter(loggus.JsonFormatter)

    entry = loggus.WithFields({
        "class": Test,
        "unsupported": unsupported,
    })
    entry.info("support")
