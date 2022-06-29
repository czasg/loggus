# coding: utf-8
import loggus

if __name__ == '__main__':
    logger1 = loggus.NewLogger()
    logger1.SetFormatter(loggus.JsonFormatter)
    logger1.info("logger1 output json")

    logger2 = loggus.NewLogger()
    logger2.info("but logger2 is text")

