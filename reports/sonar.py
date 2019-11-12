# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from dataclasses import dataclass
from typing import List, Optional
import output.issues
import json

class Data:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=False, indent=4, ensure_ascii=False)

@dataclass
class Range(Data):
    startLine: int
    endLine: int
    startColumn: int
    endColumn: int

@dataclass
class Location(Data):
    message: str
    filePath: str
    textRange: Range

@dataclass
class Issue(Data):
    engineId: str
    ruleId: str
    severity: str
    type: str
    primaryLocation: Location
    effortMinutes: int

@dataclass
class GenericIssueData(Data):
    issues: List[Issue]

def fromIssues(issues: List[output.issues.Issue]) -> GenericIssueData:
    data = []
    for item in issues:
        issue = Issue(
            'test',
            'rule42',
            item.severity.name,
            item.kind.name,
            Location(
                item.message,
                item.location.filepath,
                Range(
                    item.location.startLine,
                    item.location.endLine,
                    item.location.startColumn,
                    item.location.endColumn
                )
            ),
            item.effort
        )
        data.append(issue)
    return GenericIssueData(data)