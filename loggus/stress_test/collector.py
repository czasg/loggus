# coding: utf-8
from threading import RLock


class Collector:
    samples = 0  # total samples.
    errSamples = 0  # total error samples.
    connCreateTimeMin = 0
    sendMsgTimeMin = 0
    resMsgTimeMin = 0
    connCreateTimeAvg = 0
    sendMsgTimeAvg = 0
    resMsgTimeAvg = 0
    connCreateTimeMax = 0
    sendMsgTimeMax = 0
    resMsgTimeMax = 0
    connCreateTimeTotal = 0
    sendMsgTimeTotal = 0
    resMsgTimeTotal = 0
    lock = RLock()

    def record(self, connCreateTime: float, sendMsgTime: float, resMsgTime: float) -> None:
        with self.lock:
            self.samples += 1
            self.connCreateTimeTotal += connCreateTime
            self.sendMsgTimeTotal += sendMsgTime
            self.resMsgTimeTotal += resMsgTime
            self.connCreateTimeMin = min(connCreateTime, self.connCreateTimeMin)
            self.sendMsgTimeMin = min(sendMsgTime, self.sendMsgTimeMin)
            self.resMsgTimeMin = min(resMsgTime, self.resMsgTimeMin)
            self.connCreateTimeAvg = self.connCreateTimeTotal / self.samples
            self.sendMsgTimeAvg = self.sendMsgTimeAvg / self.samples
            self.resMsgTimeAvg = self.resMsgTimeAvg / self.samples
            self.connCreateTimeMax = max(connCreateTime, self.connCreateTimeMax)
            self.sendMsgTimeMax = max(sendMsgTime, self.sendMsgTimeMax)
            self.resMsgTimeMax = max(resMsgTime, self.resMsgTimeMax)

    def recordWithErr(self, connCreateTime: float, sendMsgTime: float, resMsgTime: float) -> None:
        with self.lock:
            self.errSamples += 1
            self.record(connCreateTime, sendMsgTime, resMsgTime)


collector = Collector()


# for test
def record():
    collector.record(0, 0, 0)


# for test
def recordWithErr():
    collector.recordWithErr(0, 0, 0)
