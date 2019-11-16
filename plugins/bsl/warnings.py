# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import bsl.ast as ast
from typing import List
from output.issues import Issue, Issues, Kind, Severity, Location, IssueCollector
import os.path

class CheckingUnusedVariables(IssueCollector):

    # TODO: Избавиться от FP (после добавления стека и счетчиков в визитер) и покрыть тестами.
    # TODO: В циклах надо запоминать переменные в условии, т.к. их нужно чекать сразу после цикла и менять состояние.
    # TODO: Указывать на место последнего присваивания переменное.

    def __init__(self, path, src):

        self.path = path
        self.src = src
        self.vars = {}
        self.params = {}
        self.assign_left = None
        self.loop_level = 0
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_AssignStmt(self, node: ast.AssignStmt):
        self.assign_left = node.Left

    def leave_AssignStmt(self, node: ast.AssignStmt):
        if node.Left.Args is not None or len(node.Left.Tail) > 0:
            return
        decl = node.Left.Head.Decl
        if type(decl) is ast.GlobalObject:
            return
        if operation := self.vars.get(decl):
            if operation == "GetInLoop":
                self.vars[decl] = "Get"
            else:
                self.vars[decl] = "Set"
            return
        decl = node.Left.Head.Decl
        if operation := self.params.get(decl):
            if operation == "GetInLoop":
                self.params[decl] = "Get"
            else:
                self.params[decl] = "Set"
        self.assign_left = None

    def visit_WhileStmt(self, node: ast.WhileStmt):
        self.loop_level += 1

    def leave_WhileStmt(self, node: ast.WhileStmt):
        self.loop_level -= 1

    def visit_ForStmt(self, node: ast.ForStmt):
        self.loop_level += 1

    def leave_ForStmt(self, node: ast.ForStmt):
        self.loop_level -= 1

    def visit_ForEachStmt(self, node: ast.ForEachStmt):
        self.loop_level += 1

    def leave_ForEachStmt(self, node: ast.ForEachStmt):
        self.loop_level -= 1

    def visit_IdentExpr(self, node: ast.IdentExpr):
        if len(node.Tail) == 0 and node == self.assign_left:
            return
        if self.loop_level > 0:
            operation = "GetInLoop"
        else:
            operation = "Get"
        decl = node.Head.Decl
        if self.vars.get(decl):
            self.vars[decl] = operation
        elif self.params.get(decl):
            self.params[decl] = operation

    def visit_MethodDecl(self, node: ast.MethodDecl):
        self.vars = {}
        self.params = {}
        for param in node.Sign.Params:
            self.params[param] = "Get"
            #self.params[param] = "Nil" <- чтобы чекать все параметры (в формах адъ)
        for var in node.Vars:
            self.vars[var] = "Set"
        for auto in node.Auto:
            self.vars[auto] = "Set"

    def leave_MethodDecl(self, node: ast.MethodDecl):

        for var, value in self.vars.items():
            if not value.startswith("Get"):
                self.issue(f'Неиспользуемая переменная "{var.Name}"', var)
        for param, value in self.params.items():
            if value == "Nil" or value == "Set" and param.ByVal:
                self.issue(f'Неиспользуемый параметр "{param.Name}"', param)

    def issue(self, msg, node):
        place = node.Place
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