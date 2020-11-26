# coding: utf-8
import loggus

try:
    from .collector import *
except:
    from collector import *


def UnitTest_record(log: loggus.Entry) -> None:
    entry = log.withField("funcName", "record")
    # test cases.
    samples = [
        {
            "name": str,
            "parameters": [

            ],
            "want": None,
            "wantErr": bool,
        },
        {
            "name": "测试record",
            "parameters": [],
            "want": None,
            "wantErr": False,
        },
    ]
    # perform validation.
    for sample in samples[1:]:
        log = entry.withField("sampleName", sample["name"])
        want = None
        try:

            want = record()
        except:
            log = log.withTraceback()
            log.info("pass") if sample["wantErr"] else log.error("ExceptionErr")
        else:
            if sample["wantErr"]:
                log.error("Want Err But Pass")
            elif want != sample["want"]:
                log.withFields({"want": sample["want"], "actual": want}).error("EqualErr")
            else:
                log.info("pass")


def UnitTest_recordWithErr(log: loggus.Entry) -> None:
    entry = log.withField("funcName", "recordWithErr")
    # test cases.
    samples = [
        {
            "name": str,
            "parameters": [

            ],
            "want": None,
            "wantErr": bool,
        },
        {
            "name": "测试recordWithErr",
            "parameters": [],
            "want": None,
            "wantErr": False,
        },
    ]
    # perform validation.
    for sample in samples[1:]:
        log = entry.withField("sampleName", sample["name"])
        want = None
        try:

            want = recordWithErr()
        except:
            log = log.withTraceback()
            log.info("pass") if sample["wantErr"] else log.error("ExceptionErr")
        else:
            if sample["wantErr"]:
                log.error("Want Err But Pass")
            elif want != sample["want"]:
                log.withFields({"want": sample["want"], "actual": want}).error("EqualErr")
            else:
                log.info("pass")
