import loggus


class FileBeat(loggus.IHook):

    def __init__(self):
        self.o = open("cza.log", "a+", encoding="utf-8")

    def GetLevels(self):
        return [loggus.INFO, loggus.ERROR]

    def ProcessMsg(self, msg):
        self.o.write(msg)

    def __del__(self):
        self.o.close()


if __name__ == '__main__':
    loggus.AddHook(FileBeat())
    loggus.info("hello info")
    loggus.warning("hello warning")
    loggus.error("hello error")
    loggus.info("hello info")
    loggus.warning("hello warning")
    loggus.error("hello error")
    loggus.info("hello info")
    loggus.warning("hello warning")
    loggus.error("hello error")
