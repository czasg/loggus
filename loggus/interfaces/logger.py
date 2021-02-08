import sys

from typing import List, Dict
from loggus.interfaces.formatter import IFormatter
from loggus.interfaces.field import IField
from loggus.interfaces.hook import IHook


class ILogger:
    out = sys.stdout
    formatter: IFormatter
    fieldKeys: List[IField]
    baseLevel: int
    colorSwitch: bool
    hooks: Dict[str, IHook]
