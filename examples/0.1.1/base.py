import loggus


def test(logger: loggus.Logger):
    name = "cza"
    age = 12
    logger.SetLevel(loggus.DEBUG)

    logger.debug("debug pass")
    logger.info("info pass")
    logger.warning("warning pass")
    logger.error("error pass")
    logger.update({"name": name, "age": age}, name=name, age=age).info("update pass")
    logger.variables(name, age).info("variables pass")
    try:
        raise
    except:
        logger.traceback()
    finally:
        logger.info("traceback pass")
    with logger.trycache():
        1 / 0
    logger.info("trycache pass")

    logger.SetFormatter(loggus.JsonFormatter)
    logger.debug("debug pass")
    logger.info("info pass")
    logger.warning("warning pass")
    logger.error("error pass")
    logger.update({"name": name, "age": age}, name=name, age=age).info("update pass")
    logger.variables(name, age).info("variables pass")
    try:
        raise
    except:
        logger.traceback()
    finally:
        logger.info("traceback pass")
    with logger.trycache():
        1 / 0
    logger.info("trycache pass")


test(loggus)
test(loggus.GetLogger(""))
test(loggus.GetLogger(__name__))
