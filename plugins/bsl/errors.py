# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import bsl.ast as ast
from bsl.enums import Tokens
from typing import List
from output.issues import Issue, Issues, Kind, Severity, Location, IssueCollector
import os.path

class DuplicateConditions(IssueCollector):

    def __init__(self, path, src):
        self.path = path
        self.src = src
        self.conditions = set()
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_IfStmt(self, node: ast.IfStmt, stack, counters):
        cond_place: ast.Place = node.Cond.Place
        text = self.src[cond_place.BegPos:cond_place.EndPos+1]
        self.conditions.add(text)

    def leave_IfStmt(self, node: ast.IfStmt, stack, counters):
        self.conditions.clear()

    def visit_ElsIfStmt(self, node: ast.ElsIfStmt, stack, counters):
        cond_place: ast.Place = node.Cond.Place
        text = self.src[cond_place.BegPos:cond_place.EndPos+1]
        if text in self.conditions:
            self.issue('Условие дублируется', cond_place)
        else:
            self.conditions.add(text)

    def issue(self, msg, place):
        self.errors.append(Issue(
            Kind.CODE_SMELL,
            Severity.INFO,
            msg,
            2,
            Location(
                os.path.normpath(self.path),
                place.BegLine,
                place.EndLine,
                place.BegColumn,
                place.EndColumn,
            )
        ))