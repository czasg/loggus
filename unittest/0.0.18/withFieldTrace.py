import loggus


def test():
    def trigger(e):
        print("test ok.")

    try:
        raise Exception("test")
    except:
        loggus.withFieldTrace().error("test error")

    with loggus.withTraceback(trigger):
        raise Exception("test")

    logger = loggus.NewLogger()
    try:
        raise Exception("test")
    except:
        logger.withFieldTrace().error("test error")

    with logger.withTraceback(trigger):
        raise Exception("test")

    logger = loggus.NewLogger()
    logger.SetFormatter(loggus.JsonFormatter)
    try:
        raise Exception("test")
    except:
        logger.withFieldTrace().error("test error")

    with logger.withTraceback(trigger):
        raise Exception("test")

    entry = loggus.withFields({"type": "test"})
    try:
        raise Exception("test")
    except:
        entry.withFieldTrace().error("test error")

    with entry.withTraceback(trigger):
        raise Exception("test")


if __name__ == '__main__':
    test()
