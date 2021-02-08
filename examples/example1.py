import loggus

if __name__ == '__main__':
    loggus._logger.SetFields([loggus.FieldKeyMsg, loggus.FieldKeyFuncName])

    loggus.info("hello world")
    loggus.WithFields({"name": "cza"}).WithFields({"age": 18}).info("hello world")
    loggus.info("hello world")

    loggus.SetFormatter(loggus.JsonFormatter)
    loggus.info("hello world")
    loggus.WithFields({"name": "cza"}).WithFields({"age": 18}).info("hello world")
    loggus.info("hello world")

    log = loggus.NewLogger()
    log.info("hello world")
    log.WithFields({"name": "cza"}).WithFields({"age": 18}).info("hello world")
    log.info("hello world")
