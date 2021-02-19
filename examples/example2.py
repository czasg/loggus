import loggus

from loggus.hooks import FileHook, RotatingFileHook

if __name__ == '__main__':
    loggus.CloseColor()
    loggus.AddHook(RotatingFileHook("cza.log"))
    loggus.info("hello info")
    loggus.warning("hello warning")
    loggus.error("hello error")
    loggus.info("hello info")
    loggus.warning("hello warning")
    loggus.error("hello error")
    loggus.info("hello info")
    loggus.warning("hello warning")
    loggus.error("hello error")
