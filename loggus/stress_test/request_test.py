# coding: utf-8
import loggus

from .request import *


def UnitTest_parseRequestInfo(log: loggus.Entry) -> None:
    entry = log.withField("funcName", "parseRequestInfo")
    # test cases.
    samples = [
        {
            "name": str,
            "parameters": [
                {'method': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': "<class 'str'>"}},
                {'url': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': "<class 'str'>"}},
                {'headers': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': "<class 'dict'>"}},
                {'body': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': "<class 'str'>"}},
            ],
            "want": None,
            "wantErr": bool,
        },
        {
            "name": "测试端口解析",
            "parameters": [
                "GET", "localhost:8080", {}, "",
            ],
            "want": ('127.0.0.1', 8080,
                     b'GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: PyStressTest/CzaOrz\r\nAccept: */*\r\n\r\n'),
            "wantErr": False,
        },
    ]
    # perform validation.
    for sample in samples[1:]:
        log = entry.withField("sampleName", sample["name"])
        want = None
        try:
            method, url, headers, body, = sample["parameters"]
            want = parseRequestInfo(method, url, headers, body)
        except:
            log.info("pass") if sample["wantErr"] else log.withTraceback().error("ExceptionErr")
        else:
            if sample["wantErr"]:
                log.error("Want Err But Pass")
            elif want != sample["want"]:
                log.withFields({"want": sample["want"], "actual": want}).error("EqualErr")
            else:
                log.info("pass")


def UnitTest_parseResponse(log: loggus.Entry) -> None:
    entry = log.withField("funcName", "parseResponse")
    # test cases.
    samples = [
        {
            "name": str,
            "parameters": [
                {'response': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': "<class 'bytes'>"}},
            ],
            "want": None,
            "wantErr": bool,
        },
        {
            "name": "测试response解析",
            "parameters": [b"HTTP/1.1 200 ok\r\ntest:test\r\n\r\n"],
            "want": (200, {"test": "test"}, b""),
            "wantErr": False,
        },
    ]
    # perform validation.
    for sample in samples[1:]:
        log = entry.withField("sampleName", sample["name"])
        want = None
        try:
            response, = sample["parameters"]
            want = parseResponse(response)
        except:
            log.info("pass") if sample["wantErr"] else log.withTraceback().error("ExceptionErr")
        else:
            if sample["wantErr"]:
                log.error("Want Err But Pass")
            elif want != sample["want"]:
                log.withFields({"want": sample["want"], "actual": want}).error("EqualErr")
            else:
                log.info("pass")


def UnitTest_parseUrl(log: loggus.Entry) -> None:
    entry = log.withField("funcName", "parseUrl")
    # test cases.
    samples = [
        {
            "name": str,
            "parameters": [
                {'url': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': "<class 'str'>"}},
            ],
            "want": None,
            "wantErr": bool,
        },
        {
            "name": "解析本地host",
            "parameters": ["localhost:8080"],
            "want": ("localhost", "127.0.0.1", 8080, "/"),
            "wantErr": False,
        },
    ]
    # perform validation.
    for sample in samples[1:]:
        log = entry.withField("sampleName", sample["name"])
        try:
            url, = sample["parameters"]
            want = parseUrl(url)
        except:
            log.info("pass") if sample["wantErr"] else log.withTraceback().error("ExceptionErr")
        else:
            if sample["wantErr"]:
                log.error("Want Err But Pass")
            elif want != sample["want"]:
                log.withFields({"want": sample["want"], "actual": want}).error("EqualErr")
            else:
                log.info("pass")


def UnitTest_request(log: loggus.Entry) -> None:
    entry = log.withField("funcName", "request")
    # test cases.
    samples = [
        {
            "name": str,
            "parameters": [
                {'address': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': 'typing.Tuple[str, int]'}},
                {'requestMsg': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': "<class 'bytes'>"}},
                {'timeout': {'kind': 'POSITIONAL_OR_KEYWORD', 'type': "<class 'int'>"}},
            ],
            "want": None,
            "wantErr": bool,
        },
        {
            "name": "测试连接异常",
            "parameters": [
                ("127.0.0.1", 0), b"", 2
            ],
            "want": None,
            "wantErr": True,
        }
    ]
    # perform validation.
    for sample in samples[1:]:
        log = entry.withField("sampleName", sample["name"])
        try:
            address, requestMsg, timeout, = sample["parameters"]
            want = request(address, requestMsg, timeout)
        except:
            log.info("pass") if sample["wantErr"] else log.withTraceback().error("ExceptionErr")
        else:
            if sample["wantErr"]:
                log.error("Want Err But Pass")
            elif want != sample["want"]:
                log.withFields({"want": sample["want"], "actual": want}).error("EqualErr")
            else:
                log.info("pass")
