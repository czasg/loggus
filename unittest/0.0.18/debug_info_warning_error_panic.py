import loggus


def test_logger():
    loggus.SetLevel(loggus.DEBUG)
    loggus.debug("test")
    loggus.withFields({"type": "info"}).info("test")
    loggus.withFields({"type": "warning"}).warning("test")
    loggus.error("test")

    logger = loggus.NewLogger()
    logger.colorSwitch = False
    logger.debug("test")
    logger.info("test")
    logger.warning("test")
    logger.error("test")
    logger.withFields({"type": "test"}).info("test")

    logger = loggus.NewLogger()
    logger.SetFormatter(loggus.JsonFormatter)
    logger.debug("test")
    logger.info("test")
    logger.warning("test")
    logger.error("test")
    logger.withFields({"type": "test"}).info("test")


if __name__ == '__main__':
    test_logger()
