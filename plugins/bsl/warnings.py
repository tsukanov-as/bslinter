# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import bsl.ast as ast
from bsl.enums import Tokens
from typing import List
from output.issues import Issue, Issues, Kind, Severity, Location, IssueCollector
import os.path

class UnusedVariables(IssueCollector):

    # TODO: покрыть тестами

    def __init__(self, path, src):

        self.path = path
        self.src = src
        self.vars = {}
        self.params = {}
        self.assign_left = None
        self.place = {}
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_AssignStmt(self, node: ast.AssignStmt, stack, counters):
        self.assign_left = node.Left

    def leave_AssignStmt(self, node: ast.AssignStmt, stack, counters):
        if node.Left.Args is not None or len(node.Left.Tail) > 0:
            return
        decl = node.Left.Head.Decl
        self.place[decl] = node.Place
        if type(decl) is ast.GlobalObject:
            return
        if op := self.vars.get(decl):
            if op != 'GetInLoop' or self.loop_level(counters) == 0:
                self.vars[decl] = 'Set'
        elif op := self.params.get(decl):
            if op != 'GetInLoop' or self.loop_level(counters) == 0:
                self.params[decl] = 'Set'
        self.assign_left = None

    def visit_IdentExpr(self, node: ast.IdentExpr, stack, counters):
        if len(node.Tail) == 0 and node == self.assign_left:
            return
        decl = node.Head.Decl
        op = self.loop_level(counters) > 0 and 'GetInLoop' or 'Get'
        if self.vars.get(decl):
            self.vars[decl] = op
        elif self.params.get(decl):
            self.params[decl] = op

    def visit_MethodDecl(self, node: ast.MethodDecl, stack, counters):
        self.vars = {}
        self.params = {}
        for param in node.Sign.Params:
            self.params[param] = 'Get'
            #self.params[param] = "Nil" <- чтобы чекать все параметры (в формах адъ)
        for var in node.Vars:
            self.vars[var] = 'Set'
        for auto in node.Auto:
            self.vars[auto] = 'Set'

    def leave_MethodDecl(self, node: ast.MethodDecl, stack, counters):

        for var, value in self.vars.items():
            if not value.startswith('Get'):
                self.issue(f'Переменная "{var.Name}" не используется после присваивания', self.place.get(var) or var.Place)
        for param, value in self.params.items():
            if value == "Nil" or value == 'Set' and param.ByVal:
                self.issue(f'Параметр "{param.Name}" не используется после присваивания', self.place.get(param) or param.Place)

    def loop_level(self, counters):
        return counters[ast.WhileStmt] + counters[ast.ForEachStmt] + counters[ast.ForStmt]

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

class EmptyExcept(IssueCollector):

    def __init__(self, path, src):
        self.path = path
        self.src = src
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_ExceptStmt(self, node: ast.ExceptStmt, stack, counters):
        if len(node.Body) == 0:
            self.issue('Пустой блок Исключение', node.Place)

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

class Concatenation(IssueCollector):

    def __init__(self, path, src):
        self.path = path
        self.src = src
        self.add_count = 0
        self.concat = False
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def leave_Expr(self, node: ast.Expr, stack, counters):
        if self.concat and self.add_count > 1:
            self.issue('Конкатенация неэффективна. Замените на StrTemplate или StrConcat.', node.Place)
        self.add_count = 0
        self.concat = False

    def visit_BinaryExpr(self, node: ast.BinaryExpr, stack, counters):
        if node.Operator == Tokens.ADD:
            self.add_count += 1
            if (type(node.Left) is ast.StringExpr
                or type(node.Right) is ast.StringExpr):
                self.concat = True

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

class StructureConstructor(IssueCollector):

    def __init__(self, path, src):
        self.path = path
        self.src = src
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_NewExpr(self, node: ast.NewExpr, stack, counters):
        if node.Name == 'Structure' and len(node.Args) > 2 and type(node.Args[0]) is ast.StringExpr:
            self.issue('Использование конструкторов структур затрудняет поддержку и доработку кода', node.Place)

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