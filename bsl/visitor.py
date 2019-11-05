# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from abc import abstractmethod

class Plugin:

    def __init__(self, src):
        pass

    @abstractmethod
    def result(self) -> str:
        pass

class Visitor:

    def __init__(self, plugins):

        methods = [func for func in dir(self)
                            if callable(getattr(self, func))
                                and (func.startswith("visit_")
                                     or func.startswith("leave_"))]

        self.hooks = {}

        for name in methods:
            hooks = []
            self.hooks[name] = hooks
            for plugin in plugins:
                if hook := getattr(plugin, name, None):
                    hooks.append(hook)

    def perform(self, func_name, node):
        for hook in self.hooks[func_name]:
            try:
                hook(node)
            except Exception as e:
                print(e)

    # Module

    def visit_Module(self, node):
        self.perform('visit_Module', node)

    def leave_Module(self, node):
        self.perform('leave_Module', node)

    # VarModListDecl

    def visit_VarModListDecl(self, node):
        self.perform('visit_VarModListDecl', node)

    def leave_VarModListDecl(self, node):
        self.perform('leave_VarModListDecl', node)

    # VarModDecl

    def visit_VarModDecl(self, node):
        self.perform('visit_VarModDecl', node)

    # VarLocDecl

    def visit_VarLocDecl(self, node):
        self.perform('visit_VarLocDecl', node)

    # AutoDecl

    def visit_AutoDecl(self, node):
        self.perform('visit_AutoDecl', node)

    # ParamDecl

    def visit_ParamDecl(self, node):
        self.perform('visit_ParamDecl', node)

    def leave_ParamDecl(self, node):
        self.perform('leave_ParamDecl', node)

    # MethodDecl

    def visit_MethodDecl(self, node):
        self.perform('visit_MethodDecl', node)

    def leave_MethodDecl(self, node):
        self.perform('leave_MethodDecl', node)

    # ProcSign

    def visit_ProcSign(self, node):
        self.perform('visit_ProcSign', node)

    def leave_ProcSign(self, node):
        self.perform('leave_ProcSign', node)

    # FuncSign

    def visit_FuncSign(self, node):
        self.perform('visit_FuncSign', node)

    def leave_FuncSign(self, node):
        self.perform('leave_FuncSign', node)

    # BasicLitExpr

    def visit_BasicLitExpr(self, node):
        self.perform('visit_BasicLitExpr', node)

    # FieldExpr

    def visit_FieldExpr(self, node):
        self.perform('visit_FieldExpr', node)

    def leave_FieldExpr(self, node):
        self.perform('leave_FieldExpr', node)

    # IndexExpr

    def visit_IndexExpr(self, node):
        self.perform('visit_IndexExpr', node)

    def leave_IndexExpr(self, node):
        self.perform('leave_IndexExpr', node)

    # IdentExpr

    def visit_IdentExpr(self, node):
        self.perform('visit_IdentExpr', node)

    def leave_IdentExpr(self, node):
        self.perform('leave_IdentExpr', node)

    # UnaryExpr

    def visit_UnaryExpr(self, node):
        self.perform('visit_UnaryExpr', node)

    def leave_UnaryExpr(self, node):
        self.perform('leave_UnaryExpr', node)

    # BinaryExpr

    def visit_BinaryExpr(self, node):
        self.perform('visit_BinaryExpr', node)

    def leave_BinaryExpr(self, node):
        self.perform('leave_BinaryExpr', node)

    # NewExpr

    def visit_NewExpr(self, node):
        self.perform('visit_NewExpr', node)

    def leave_NewExpr(self, node):
        self.perform('leave_NewExpr', node)

    # TernaryExpr

    def visit_TernaryExpr(self, node):
        self.perform('visit_TernaryExpr', node)

    def leave_TernaryExpr(self, node):
        self.perform('leave_TernaryExpr', node)

    # ParenExpr

    def visit_ParenExpr(self, node):
        self.perform('visit_ParenExpr', node)

    def leave_ParenExpr(self, node):
        self.perform('leave_ParenExpr', node)

    # NotExpr

    def visit_NotExpr(self, node):
        self.perform('visit_NotExpr', node)

    def leave_NotExpr(self, node):
        self.perform('leave_NotExpr', node)

    # StringExpr

    def visit_StringExpr(self, node):
        self.perform('visit_StringExpr', node)

    def leave_StringExpr(self, node):
        self.perform('leave_StringExpr', node)

    # AssignStmt

    def visit_AssignStmt(self, node):
        self.perform('visit_AssignStmt', node)

    def leave_AssignStmt(self, node):
        self.perform('leave_AssignStmt', node)

    # ReturnStmt

    def visit_ReturnStmt(self, node):
        self.perform('visit_ReturnStmt', node)

    def leave_ReturnStmt(self, node):
        self.perform('leave_ReturnStmt', node)

    # BreakStmt

    def visit_BreakStmt(self, node):
        self.perform('visit_BreakStmt', node)

    # ContinueStmt

    def visit_ContinueStmt(self, node):
        self.perform('visit_ContinueStmt', node)

    # RaiseStmt

    def visit_RaiseStmt(self, node):
        self.perform('visit_RaiseStmt', node)

    def leave_RaiseStmt(self, node):
        self.perform('leave_RaiseStmt', node)

    # ExecuteStmt

    def visit_ExecuteStmt(self, node):
        self.perform('visit_ExecuteStmt', node)

    def leave_ExecuteStmt(self, node):
        self.perform('leave_ExecuteStmt', node)

    # CallStmt

    def visit_CallStmt(self, node):
        self.perform('visit_CallStmt', node)

    def leave_CallStmt(self, node):
        self.perform('leave_CallStmt', node)

    # IfStmt

    def visit_IfStmt(self, node):
        self.perform('visit_IfStmt', node)

    def leave_IfStmt(self, node):
        self.perform('leave_IfStmt', node)

    # ElsIfStmt

    def visit_ElsIfStmt(self, node):
        self.perform('visit_ElsIfStmt', node)

    def leave_ElsIfStmt(self, node):
        self.perform('leave_ElsIfStmt', node)

    # ElseStmt

    def visit_ElseStmt(self, node):
        self.perform('visit_ElseStmt', node)

    def leave_ElseStmt(self, node):
        self.perform('leave_ElseStmt', node)

    # WhileStmt

    def visit_WhileStmt(self, node):
        self.perform('visit_WhileStmt', node)

    def leave_WhileStmt(self, node):
        self.perform('leave_WhileStmt', node)

    # ForStmt

    def visit_ForStmt(self, node):
        self.perform('visit_ForStmt', node)

    def leave_ForStmt(self, node):
        self.perform('leave_ForStmt', node)

    # ForEachStmt

    def visit_ForEachStmt(self, node):
        self.perform('visit_ForEachStmt', node)

    def leave_ForEachStmt(self, node):
        self.perform('leave_ForEachStmt', node)

    # TryStmt

    def visit_TryStmt(self, node):
        self.perform('visit_TryStmt', node)

    def leave_TryStmt(self, node):
        self.perform('leave_TryStmt', node)

    # ExceptStmt

    def visit_ExceptStmt(self, node):
        self.perform('visit_ExceptStmt', node)

    def leave_ExceptStmt(self, node):
        self.perform('leave_ExceptStmt', node)

    # GotoStmt

    def visit_GotoStmt(self, node):
        self.perform('visit_GotoStmt', node)

    # LabelStmt

    def visit_LabelStmt(self, node):
        self.perform('visit_LabelStmt', node)

    # PrepIfInst

    def visit_PrepIfInst(self, node):
        self.perform('visit_PrepIfInst', node)

    def leave_PrepIfInst(self, node):
        self.perform('leave_PrepIfInst', node)

    # PrepElsIfInst

    def visit_PrepElsIfInst(self, node):
        self.perform('visit_PrepElsIfInst', node)

    def leave_PrepElsIfInst(self, node):
        self.perform('leave_PrepElsIfInst', node)

    # PrepElseInst

    def visit_PrepElseInst(self, node):
        self.perform('visit_PrepElseInst', node)

    # PrepEndIfInst

    def visit_PrepEndIfInst(self, node):
        self.perform('visit_PrepEndIfInst', node)

    # PrepRegionInst

    def visit_PrepRegionInst(self, node):
        self.perform('visit_PrepRegionInst', node)

    # PrepEndRegionInst

    def visit_PrepEndRegionInst(self, node):
        self.perform('visit_PrepEndRegionInst', node)

    # PrepBinaryExpr

    def visit_PrepBinaryExpr(self, node):
        self.perform('visit_PrepBinaryExpr', node)

    def leave_PrepBinaryExpr(self, node):
        self.perform('leave_PrepBinaryExpr', node)

    # PrepNotExpr

    def visit_PrepNotExpr(self, node):
        self.perform('visit_PrepNotExpr', node)

    def leave_PrepNotExpr(self, node):
        self.perform('leave_PrepNotExpr', node)

    # PrepSymExpr

    def visit_PrepSymExpr(self, node):
        self.perform('visit_PrepSymExpr', node)

    # PrepParenExpr

    def visit_PrepParenExpr(self, node):
        self.perform('visit_PrepParenExpr', node)

    def leave_PrepParenExpr(self, node):
        self.perform('leave_PrepParenExpr', node)

