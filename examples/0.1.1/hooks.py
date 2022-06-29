import loggus


class LogHook(loggus.IHook):
    def GetLevels(self) -> list:
        return [loggus.INFO]

    def Fire(self, entry, level, msg, output) -> None:
        print(entry, level, msg)


loggus.AddHooks(LogHook())
loggus.info("11")
