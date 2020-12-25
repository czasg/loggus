# coding: utf-8
import re
import time
import json
import signal
import loggus
import threading

from .collector import collector
from .request import parseRequestInfo, request

StressOver = False
regex = re.compile("<(.*?):(.*?)>")


def show():
    loggus.info("Stress Test Start")
    while not StressOver:
        time.sleep(5)
        collector.show()


def worker(
        hostIP, port, requestMsg, timeout,
        equalStatus,
        equalBodyStr,
        equalJson
):
    while not StressOver:
        try:
            status, headers, body, connCreateTime, sendMsgTime, recvMsgTime = \
                request((hostIP, port), requestMsg, timeout)
            if equalJson:
                data = json.loads(body)
                error = False
                for equalRule in equalJson:
                    ruleStr, aim = equalRule.split("==")
                    checkValue = regex.search(aim)
                    if checkValue:
                        typeValue, value = checkValue.groups()
                        if typeValue.startswith("str"):
                            value = value
                        elif typeValue.startswith("int"):
                            value = int(value)
                    else:
                        value = aim
                    for rule in ruleStr.split("."):
                        data = data[rule]
                    if data != value:
                        error = True
                        break
                if error:
                    collector.recordWithErr(connCreateTime, sendMsgTime, recvMsgTime)
                else:
                    collector.record(connCreateTime, sendMsgTime, recvMsgTime)
            elif equalBodyStr is not None and equalBodyStr != body.decode():
                collector.recordWithErr(connCreateTime, sendMsgTime, recvMsgTime)
            elif equalStatus != status:
                collector.recordWithErr(connCreateTime, sendMsgTime, recvMsgTime)
            else:
                collector.record(connCreateTime, sendMsgTime, recvMsgTime)
        except:
            collector.recordWithErr(0, 0, 0)


def stress(
        # Request Params
        method: str, uri: str, headers: list, body: str, timeout: int = 8,
        # Work Params
        concurrent: int = 10,
        duration: int = 60,
        # Valid Response
        equalStatus: int = 200,
        equalBodyStr: str = None,
        equalJson: list = None,  # ["data.msg==ok", "data.error_code==200"]
):
    loggus.withFields({
        "method": method,
        "uri": uri,
        "headers": headers,
        "concurrent": concurrent,
        "duration": duration,
        "equalStatus": equalStatus,
        "equalBodyStr": equalBodyStr,
        "equalJson": equalJson,
    }).info("Get Request Params.")

    _headers = {}
    for header in (headers or []):
        splitRsp = header.split(":")
        if len(splitRsp) != 2:
            loggus.withField("InvalidHeader", header, loggus.ERROR_COLOR).panic("InvalidHeader")
        _headers[splitRsp[0].strip()] = splitRsp[1].strip()

    hostIP, port, requestMsg = parseRequestInfo(method, uri, _headers, body)
    # todo, how to calc & limit throughput.
    threads = [threading.Thread(target=show)]
    for _ in range(concurrent):
        threads.append(threading.Thread(target=worker, args=(
            hostIP, port, requestMsg, timeout,
            equalStatus,
            equalBodyStr,
            equalJson,
        )))
    for thread in threads:
        thread.start()

    with loggus.withCallback():
        time.sleep(duration)
    global StressOver
    StressOver = True
    with loggus.withCallback():
        for thread in threads:
            thread.join()
    loggus.info("stress test over.")
