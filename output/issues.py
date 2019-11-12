# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from enum import Enum, auto
from dataclasses import dataclass
from output.result import Result
from typing import List, Optional

class Severity(Enum):
    BLOCKER = auto()
    CRITICAL = auto()
    MAJOR = auto()
    MINOR = auto()
    INFO = auto()

class Kind(Enum):
    BUG = auto()
    VULNERABILITY = auto()
    CODE_SMELL = auto()

@dataclass
class Location:

    filepath: str
    startLine: int
    endLine: int
    startColumn: int
    endColumn: int

@dataclass
class Issue:

    kind: Kind
    severity: Severity
    message: str
    effort: int
    location: Location

class Issues(Result):

    def __init__(self, items):
        self.items: List[Issue] = items