# coding: utf-8
import re
import time
import socket

from http import client
from typing import Tuple

regex = re.compile("(?:(https?)://)?([^/]*)(.*)")
size = 1024


def parseUrl(url: str) -> Tuple[str, str, int, str]:
    parser = regex.search(url)
    if not parser:
        raise Exception(f"Parser {url} Failure!")
    protocol, host, path = parser.groups()
    port = 443 if protocol == "https" else 80
    if not host:
        raise Exception(f"Parser {url} Failure, Empty Host!")
    if ":" in host:
        host, port = host.split(":", 1)
    port = int(port)
    hostIP = socket.gethostbyname(host)
    path = path or "/"
    return host, hostIP, port, path


def parseResponse(response: bytes) -> Tuple[int, dict, bytes]:
    statusIndex = response.find(b" ") + 1
    statusIndexEnd = statusIndex + 3
    status = int(response[statusIndex:statusIndexEnd])

    headersIndex = response.find(b"\r\n", statusIndexEnd) + 2
    headersEnd = response.find(b"\r\n\r\n", headersIndex)
    bodyIndex = headersEnd + 4
    headersBytes = response[headersIndex:headersEnd]
    body = response[bodyIndex:]

    headers = {}
    for header in headersBytes.decode("utf-8").split("\r\n"):
        kv = header.split(":")
        if len(kv) == 2:
            headers[kv[0].strip()] = kv[1].strip()
    return status, headers, body


def parseRequestInfo(method: str, url: str, headers: dict = None, body: str = None) -> Tuple[str, int, bytes]:
    method = method.upper()
    host, hostIP, port, path = parseUrl(url)
    requestMsg = f"{method} {path} HTTP/1.1\r\n"
    headersBases = {
        "Host": host,
        "User-Agent": "PyStressTest/CzaOrz",
        "Accept": "*/*",
    }
    if body:
        body = body.encode("utf-8")
        headersBases["Content-Length"] = len(body)
        headersBases["Content-Type"] = "application/x-www-form-urlencoded"
    if headers:
        headersBases.update(headers)
    for key, value in headersBases.items():
        requestMsg += f"{key}: {value}\r\n"
    else:
        requestMsg += "\r\n"
    requestMsg = requestMsg.encode("utf-8")
    if body:
        requestMsg = requestMsg + body

    return hostIP, port, requestMsg


def request(address: Tuple[str, int], requestMsg: bytes, timeout: int = None) -> Tuple[bytes, float, float, float]:
    sock = socket.socket()
    sock.settimeout(timeout) if timeout else None
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    start = time.monotonic()
    sock.connect(address)
    connCreateTime = time.monotonic() - start

    start = time.monotonic()
    sock.send(requestMsg)
    sendMsgTime = time.monotonic() - start

    hr = client.HTTPResponse(sock)
    start = time.monotonic()
    hr.begin()
    response = hr.read()
    recvMsgTime = time.monotonic() - start

    hr.close()
    return response, connCreateTime, sendMsgTime, recvMsgTime


if __name__ == '__main__':
    import urllib3

    http = urllib3.PoolManager()
    response = http.request("GET", "http://fanyi.youdao.com")
    print(response.data)

    import requests

    print(requests.get("http://fanyi.youdao.com").content)

    hostIP, port, requestMsg = parseRequestInfo("GET", "http://fanyi.youdao.com", {}, "")
    print(hostIP, port, requestMsg)
    response, connCreateTime, sendMsgTime, recvMsgTime = request((hostIP, port), requestMsg, 60)
    print(response)
