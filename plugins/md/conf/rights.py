# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import md.enums as enums
import md.conf as cf
import md.rights as rights
from typing import List, Dict, Optional
from output.issues import Issue, Issues, Kind, Severity, Location, IssueCollector
import os.path

class InteractiveDelete(IssueCollector):

    def __init__(self):
        self.role_name = ''
        self.object_name = ''
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_RoleProperties(self, node: cf.RoleProperties):
        self.role_name = node.Name

    def visit_ObjectRight(self, node: rights.ObjectRight):
        self.object_name = node.name

    def visit_Right(self, node: rights.Right):
        if node.name == 'InteractiveDelete' and node.value == enums.Bool.TRUE:
            self.issue(f'Роль {self.role_name} имеет право интерактивного удаления {self.object_name}', node)

    def issue(self, msg, node):
        self.errors.append(Issue(
            Kind.CODE_SMELL,
            Severity.INFO,
            msg,
            2,
            Location(
                os.path.normpath(node._path),
                node._startLine,
                node._endLine,
                node._startColumn,
                node._endColumn,
            )
        ))
