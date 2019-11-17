# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import bsl.ast as ast
from typing import List
from output.issues import Issue, Issues, Kind, Severity, Location, IssueCollector
import os.path

class ClosingComments(IssueCollector):

    # TODO: более конкретные сообщения: "Пропущен пробел", "Не хватает скобок" ...

    def __init__(self, path, src):

        self.path = path
        self.src = src
        self.comments = {}
        self.region_stack = []
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_Module(self, node: ast.Module, stack, counters):
        self.comments = node.Comments

    def visit_MethodDecl(self, node: ast.MethodDecl, stack, counters):
        line = node.Place.EndLine
        if comment := self.comments.get(line):
            if comment.text.rstrip() != f' {node.Sign.Name}()':
                self.issue(f'Метод "{node.Sign.Name}()" имеет неправильный замыкающий комментарий.', comment)

    def visit_PrepRegionInst(self, node: ast.PrepRegionInst, stack, counters):
        self.region_stack.append(node.Name)

    def visit_PrepEndRegionInst(self, node: ast.PrepEndRegionInst, stack, counters):
        line = node.Place.EndLine
        region_name = self.region_stack.pop()
        if comment := self.comments.get(line):
            if comment.text.rstrip() != f' {region_name}':
                self.issue(f'Область "{region_name}" имеет неправильный замыкающий комментарий.', comment)

    def issue(self, msg, comment):
        self.errors.append(Issue(
            Kind.CODE_SMELL,
            Severity.INFO,
            msg,
            2,
            Location(
                os.path.normpath(self.path),
                comment.line,
                comment.line,
                comment.column - 2, # - //
                comment.column + len(comment.text),
            )
        ))
