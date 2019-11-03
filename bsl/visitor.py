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
                                and (func.startswith("beforeVisit")
                                     or func.startswith("afterVisit"))]

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

    def beforeVisitModule(self, node):
        self.perform('beforeVisitModule', node)

    def afterVisitModule(self, node):
        self.perform('afterVisitModule', node)

    # VarModListDecl

    def beforeVisitVarModListDecl(self, node):
        self.perform('beforeVisitVarModListDecl', node)

    def afterVisitVarModListDecl(self, node):
        self.perform('afterVisitVarModListDecl', node)

    # VarModDecl

    def beforeVisitVarModDecl(self, node):
        self.perform('beforeVisitVarModDecl', node)

    # VarLocDecl

    def beforeVisitVarLocDecl(self, node):
        self.perform('beforeVisitVarLocDecl', node)

    # AutoDecl

    def beforeVisitAutoDecl(self, node):
        self.perform('beforeVisitAutoDecl', node)

    # ParamDecl

    def beforeVisitParamDecl(self, node):
        self.perform('beforeVisitParamDecl', node)

    def afterVisitParamDecl(self, node):
        self.perform('afterVisitParamDecl', node)

    # MethodDecl

    def beforeVisitMethodDecl(self, node):
        self.perform('beforeVisitMethodDecl', node)

    def afterVisitMethodDecl(self, node):
        self.perform('afterVisitMethodDecl', node)

    # ProcSign

    def beforeVisitProcSign(self, node):
        self.perform('beforeVisitProcSign', node)

    def afterVisitProcSign(self, node):
        self.perform('afterVisitProcSign', node)

    # FuncSign

    def beforeVisitFuncSign(self, node):
        self.perform('beforeVisitFuncSign', node)

    def afterVisitFuncSign(self, node):
        self.perform('afterVisitFuncSign', node)

    # BasicLitExpr

    def beforeVisitBasicLitExpr(self, node):
        self.perform('beforeVisitBasicLitExpr', node)

    # FieldExpr

    def beforeVisitFieldExpr(self, node):
        self.perform('beforeVisitFieldExpr', node)

    def afterVisitFieldExpr(self, node):
        self.perform('afterVisitFieldExpr', node)

    # IndexExpr

    def beforeVisitIndexExpr(self, node):
        self.perform('beforeVisitIndexExpr', node)

    def afterVisitIndexExpr(self, node):
        self.perform('afterVisitIndexExpr', node)

    # IdentExpr

    def beforeVisitIdentExpr(self, node):
        self.perform('beforeVisitIdentExpr', node)

    def afterVisitIdentExpr(self, node):
        self.perform('afterVisitIdentExpr', node)

    # UnaryExpr

    def beforeVisitUnaryExpr(self, node):
        self.perform('beforeVisitUnaryExpr', node)

    def afterVisitUnaryExpr(self, node):
        self.perform('afterVisitUnaryExpr', node)

    # BinaryExpr

    def beforeVisitBinaryExpr(self, node):
        self.perform('beforeVisitBinaryExpr', node)

    def afterVisitBinaryExpr(self, node):
        self.perform('afterVisitBinaryExpr', node)

    # NewExpr

    def beforeVisitNewExpr(self, node):
        self.perform('beforeVisitNewExpr', node)

    def afterVisitNewExpr(self, node):
        self.perform('afterVisitNewExpr', node)

    # TernaryExpr

    def beforeVisitTernaryExpr(self, node):
        self.perform('beforeVisitTernaryExpr', node)

    def afterVisitTernaryExpr(self, node):
        self.perform('afterVisitTernaryExpr', node)

    # ParenExpr

    def beforeVisitParenExpr(self, node):
        self.perform('beforeVisitParenExpr', node)

    def afterVisitParenExpr(self, node):
        self.perform('afterVisitParenExpr', node)

    # NotExpr

    def beforeVisitNotExpr(self, node):
        self.perform('beforeVisitNotExpr', node)

    def afterVisitNotExpr(self, node):
        self.perform('afterVisitNotExpr', node)

    # StringExpr

    def beforeVisitStringExpr(self, node):
        self.perform('beforeVisitStringExpr', node)

    def afterVisitStringExpr(self, node):
        self.perform('afterVisitStringExpr', node)

    # AssignStmt

    def beforeVisitAssignStmt(self, node):
        self.perform('beforeVisitAssignStmt', node)

    def afterVisitAssignStmt(self, node):
        self.perform('afterVisitAssignStmt', node)

    # ReturnStmt

    def beforeVisitReturnStmt(self, node):
        self.perform('beforeVisitReturnStmt', node)

    def afterVisitReturnStmt(self, node):
        self.perform('afterVisitReturnStmt', node)

    # BreakStmt

    def beforeVisitBreakStmt(self, node):
        self.perform('beforeVisitBreakStmt', node)

    # ContinueStmt

    def beforeVisitContinueStmt(self, node):
        self.perform('beforeVisitContinueStmt', node)

    # RaiseStmt

    def beforeVisitRaiseStmt(self, node):
        self.perform('beforeVisitRaiseStmt', node)

    def afterVisitRaiseStmt(self, node):
        self.perform('afterVisitRaiseStmt', node)

    # ExecuteStmt

    def beforeVisitExecuteStmt(self, node):
        self.perform('beforeVisitExecuteStmt', node)

    def afterVisitExecuteStmt(self, node):
        self.perform('afterVisitExecuteStmt', node)

    # CallStmt

    def beforeVisitCallStmt(self, node):
        self.perform('beforeVisitCallStmt', node)

    def afterVisitCallStmt(self, node):
        self.perform('afterVisitCallStmt', node)

    # IfStmt

    def beforeVisitIfStmt(self, node):
        self.perform('beforeVisitIfStmt', node)

    def afterVisitIfStmt(self, node):
        self.perform('afterVisitIfStmt', node)

    # ElsIfStmt

    def beforeVisitElsIfStmt(self, node):
        self.perform('beforeVisitElsIfStmt', node)

    def afterVisitElsIfStmt(self, node):
        self.perform('afterVisitElsIfStmt', node)

    # ElseStmt

    def beforeVisitElseStmt(self, node):
        self.perform('beforeVisitElseStmt', node)

    def afterVisitElseStmt(self, node):
        self.perform('afterVisitElseStmt', node)

    # WhileStmt

    def beforeVisitWhileStmt(self, node):
        self.perform('beforeVisitWhileStmt', node)

    def afterVisitWhileStmt(self, node):
        self.perform('afterVisitWhileStmt', node)

    # ForStmt

    def beforeVisitForStmt(self, node):
        self.perform('beforeVisitForStmt', node)

    def afterVisitForStmt(self, node):
        self.perform('afterVisitForStmt', node)

    # ForEachStmt

    def beforeVisitForEachStmt(self, node):
        self.perform('beforeVisitForEachStmt', node)

    def afterVisitForEachStmt(self, node):
        self.perform('afterVisitForEachStmt', node)

    # TryStmt

    def beforeVisitTryStmt(self, node):
        self.perform('beforeVisitTryStmt', node)

    def afterVisitTryStmt(self, node):
        self.perform('afterVisitTryStmt', node)

    # ExceptStmt

    def beforeVisitExceptStmt(self, node):
        self.perform('beforeVisitExceptStmt', node)

    def afterVisitExceptStmt(self, node):
        self.perform('afterVisitExceptStmt', node)

    # GotoStmt

    def beforeVisitGotoStmt(self, node):
        self.perform('beforeVisitGotoStmt', node)

    # LabelStmt

    def beforeVisitLabelStmt(self, node):
        self.perform('beforeVisitLabelStmt', node)

    # PrepIfInst

    def beforeVisitPrepIfInst(self, node):
        self.perform('beforeVisitPrepIfInst', node)

    def afterVisitPrepIfInst(self, node):
        self.perform('afterVisitPrepIfInst', node)

    # PrepElsIfInst

    def beforeVisitPrepElsIfInst(self, node):
        self.perform('beforeVisitPrepElsIfInst', node)

    def afterVisitPrepElsIfInst(self, node):
        self.perform('afterVisitPrepElsIfInst', node)

    # PrepElseInst

    def beforeVisitPrepElseInst(self, node):
        self.perform('beforeVisitPrepElseInst', node)

    # PrepEndIfInst

    def beforeVisitPrepEndIfInst(self, node):
        self.perform('beforeVisitPrepEndIfInst', node)

    # PrepRegionInst

    def beforeVisitPrepRegionInst(self, node):
        self.perform('beforeVisitPrepRegionInst', node)

    # PrepEndRegionInst

    def beforeVisitPrepEndRegionInst(self, node):
        self.perform('beforeVisitPrepEndRegionInst', node)

    # PrepBinaryExpr

    def beforeVisitPrepBinaryExpr(self, node):
        self.perform('beforeVisitPrepBinaryExpr', node)

    def afterVisitPrepBinaryExpr(self, node):
        self.perform('afterVisitPrepBinaryExpr', node)

    # PrepNotExpr

    def beforeVisitPrepNotExpr(self, node):
        self.perform('beforeVisitPrepNotExpr', node)

    def afterVisitPrepNotExpr(self, node):
        self.perform('afterVisitPrepNotExpr', node)

    # PrepSymExpr

    def beforeVisitPrepSymExpr(self, node):
        self.perform('beforeVisitPrepSymExpr', node)

    # PrepParenExpr

    def beforeVisitPrepParenExpr(self, node):
        self.perform('beforeVisitPrepParenExpr', node)

    def afterVisitPrepParenExpr(self, node):
        self.perform('afterVisitPrepParenExpr', node)

