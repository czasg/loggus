# coding: utf-8
import socket
from .collector import collector
from .request import parseUrl, parseResponse, parseRequestInfo, request


def stress(method, uri, headers, body, throughput, timeout=8):
    hostIP, port, requestMsg = parseRequestInfo(method, uri, headers, body)
    # todo, how to calc & limit throughput.
    while True:
        response, connCreateTime, sendMsgTime, recvMsgTime = \
            request((hostIP, port), requestMsg, timeout)
        collector.record(connCreateTime, sendMsgTime, recvMsgTime)
