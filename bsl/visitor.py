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

    methods = [
        'beforeVisitModule',            'afterVisitModule',
        'beforeVisitVarModListDecl',    'afterVisitVarModListDecl',
        'beforeVisitVarModDecl',        #'afterVisitVarModDecl',
        'beforeVisitVarLocDecl',        #'afterVisitVarLocDecl',
        'beforeVisitAutoDecl',          #'afterVisitAutoDecl',
        'beforeVisitParamDecl',         'afterVisitParamDecl',
        'beforeVisitMethodDecl',        'afterVisitMethodDecl',
        'beforeVisitProcSign',          'afterVisitProcSign',
        'beforeVisitFuncSign',          'afterVisitFuncSign',
        'beforeVisitBasicLitExpr',      #'afterVisitBasicLitExpr',
        'beforeVisitFieldExpr',         'afterVisitFieldExpr',
        'beforeVisitIndexExpr',         'afterVisitIndexExpr',
        'beforeVisitIdentExpr',         'afterVisitIdentExpr',
        'beforeVisitUnaryExpr',         'afterVisitUnaryExpr',
        'beforeVisitBinaryExpr',        'afterVisitBinaryExpr',
        'beforeVisitNewExpr',           'afterVisitNewExpr',
        'beforeVisitTernaryExpr',       'afterVisitTernaryExpr',
        'beforeVisitParenExpr',         'afterVisitParenExpr',
        'beforeVisitNotExpr',           'afterVisitNotExpr',
        'beforeVisitStringExpr',        'afterVisitStringExpr',
        'beforeVisitAssignStmt',        'afterVisitAssignStmt',
        'beforeVisitReturnStmt',        'afterVisitReturnStmt',
        'beforeVisitBreakStmt',         #'afterVisitBreakStmt',
        'beforeVisitContinueStmt',      #'afterVisitContinueStmt',
        'beforeVisitRaiseStmt',         'afterVisitRaiseStmt',
        'beforeVisitExecuteStmt',       'afterVisitExecuteStmt',
        'beforeVisitCallStmt',          'afterVisitCallStmt',
        'beforeVisitIfStmt',            'afterVisitIfStmt',
        'beforeVisitElsIfStmt',         'afterVisitElsIfStmt',
        'beforeVisitElseStmt',          'afterVisitElseStmt',
        'beforeVisitWhileStmt',         'afterVisitWhileStmt',
        'beforeVisitForStmt',           'afterVisitForStmt',
        'beforeVisitForEachStmt',       'afterVisitForEachStmt',
        'beforeVisitTryStmt',           'afterVisitTryStmt',
        'beforeVisitExceptStmt',        'afterVisitExceptStmt',
        'beforeVisitGotoStmt',          #'afterVisitGotoStmt',
        'beforeVisitLabelStmt',         #'afterVisitLabelStmt',
        'beforeVisitPrepIfInst',        'afterVisitPrepIfInst',
        'beforeVisitPrepElsIfInst',     'afterVisitPrepElsIfInst',
        'beforeVisitPrepElseInst',      #'afterVisitPrepElseInst',
        'beforeVisitPrepEndIfInst',     #'afterVisitPrepEndIfInst',
        'beforeVisitPrepRegionInst',    #'afterVisitPrepRegionInst',
        'beforeVisitPrepEndRegionInst', #'afterVisitPrepEndRegionInst',
        'beforeVisitPrepExpr',          'afterVisitPrepExpr',
        'beforeVisitPrepBinaryExpr',    'afterVisitPrepBinaryExpr',
        'beforeVisitPrepNotExpr',       'afterVisitPrepNotExpr',
        'beforeVisitPrepSymExpr',       #'afterVisitPrepSymExpr',
        'beforeVisitPrepParenExpr',     'afterVisitPrepParenExpr',
    ]

    def __init__(self, plugins):

        self.hooks = {}

        for name in self.methods:
            hook = []
            self.hooks[name] = hook
            for plugin in plugins:
                if hasattr(plugin, name):
                    hook.append(plugin)

    def beforeVisitModule(self, node):
        for plugin in self.hooks['beforeVisitModule']:
            try:
                plugin.beforeVisitModule(node)
            except Exception as e:
                print(e)

    def afterVisitModule(self, node):
        for plugin in self.hooks['afterVisitModule']:
            try:
                plugin.afterVisitModule(node)
            except Exception as e:
                print(e)

    def beforeVisitVarModListDecl(self, node):
        for plugin in self.hooks['beforeVisitVarModListDecl']:
            try:
                plugin.beforeVisitVarModListDecl(node)
            except Exception as e:
                print(e)

    def afterVisitVarModListDecl(self, node):
        for plugin in self.hooks['afterVisitVarModListDecl']:
            try:
                plugin.afterVisitVarModListDecl(node)
            except Exception as e:
                print(e)

    def beforeVisitVarModDecl(self, node):
        for plugin in self.hooks['beforeVisitVarModDecl']:
            try:
                plugin.beforeVisitVarModDecl(node)
            except Exception as e:
                print(e)

    # def afterVisitVarModDecl(self, node):
    #     for plugin in self.hooks['afterVisitVarModDecl']:
    #         try:
    #             plugin.afterVisitVarModDecl(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitVarLocDecl(self, node):
        for plugin in self.hooks['beforeVisitVarLocDecl']:
            try:
                plugin.beforeVisitVarLocDecl(node)
            except Exception as e:
                print(e)

    # def afterVisitVarLocDecl(self, node):
    #     for plugin in self.hooks['afterVisitVarLocDecl']:
    #         try:
    #             plugin.afterVisitVarLocDecl(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitAutoDecl(self, node):
        for plugin in self.hooks['beforeVisitAutoDecl']:
            try:
                plugin.beforeVisitAutoDecl(node)
            except Exception as e:
                print(e)

    # def afterVisitAutoDecl(self, node):
    #     for plugin in self.hooks['afterVisitAutoDecl']:
    #         try:
    #             plugin.afterVisitAutoDecl(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitParamDecl(self, node):
        for plugin in self.hooks['beforeVisitParamDecl']:
            try:
                plugin.beforeVisitParamDecl(node)
            except Exception as e:
                print(e)

    def afterVisitParamDecl(self, node):
        for plugin in self.hooks['afterVisitParamDecl']:
            try:
                plugin.afterVisitParamDecl(node)
            except Exception as e:
                print(e)

    def beforeVisitMethodDecl(self, node):
        for plugin in self.hooks['beforeVisitMethodDecl']:
            try:
                plugin.beforeVisitMethodDecl(node)
            except Exception as e:
                print(e)

    def afterVisitMethodDecl(self, node):
        for plugin in self.hooks['afterVisitMethodDecl']:
            try:
                plugin.afterVisitMethodDecl(node)
            except Exception as e:
                print(e)

    def beforeVisitProcSign(self, node):
        for plugin in self.hooks['beforeVisitProcSign']:
            try:
                plugin.beforeVisitProcSign(node)
            except Exception as e:
                print(e)

    def afterVisitProcSign(self, node):
        for plugin in self.hooks['afterVisitProcSign']:
            try:
                plugin.afterVisitProcSign(node)
            except Exception as e:
                print(e)

    def beforeVisitFuncSign(self, node):
        for plugin in self.hooks['beforeVisitFuncSign']:
            try:
                plugin.beforeVisitFuncSign(node)
            except Exception as e:
                print(e)

    def afterVisitFuncSign(self, node):
        for plugin in self.hooks['afterVisitFuncSign']:
            try:
                plugin.afterVisitFuncSign(node)
            except Exception as e:
                print(e)

    def beforeVisitBasicLitExpr(self, node):
        for plugin in self.hooks['beforeVisitBasicLitExpr']:
            try:
                plugin.beforeVisitBasicLitExpr(node)
            except Exception as e:
                print(e)

    # def afterVisitBasicLitExpr(self, node):
    #     for plugin in self.hooks['afterVisitBasicLitExpr']:
    #         try:
    #             plugin.afterVisitBasicLitExpr(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitFieldExpr(self, node):
        for plugin in self.hooks['beforeVisitFieldExpr']:
            try:
                plugin.beforeVisitFieldExpr(node)
            except Exception as e:
                print(e)

    def afterVisitFieldExpr(self, node):
        for plugin in self.hooks['afterVisitFieldExpr']:
            try:
                plugin.afterVisitFieldExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitIndexExpr(self, node):
        for plugin in self.hooks['beforeVisitIndexExpr']:
            try:
                plugin.beforeVisitIndexExpr(node)
            except Exception as e:
                print(e)

    def afterVisitIndexExpr(self, node):
        for plugin in self.hooks['afterVisitIndexExpr']:
            try:
                plugin.afterVisitIndexExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitIdentExpr(self, node):
        for plugin in self.hooks['beforeVisitIdentExpr']:
            try:
                plugin.beforeVisitIdentExpr(node)
            except Exception as e:
                print(e)

    def afterVisitIdentExpr(self, node):
        for plugin in self.hooks['afterVisitIdentExpr']:
            try:
                plugin.afterVisitIdentExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitUnaryExpr(self, node):
        for plugin in self.hooks['beforeVisitUnaryExpr']:
            try:
                plugin.beforeVisitUnaryExpr(node)
            except Exception as e:
                print(e)

    def afterVisitUnaryExpr(self, node):
        for plugin in self.hooks['afterVisitUnaryExpr']:
            try:
                plugin.afterVisitUnaryExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitBinaryExpr(self, node):
        for plugin in self.hooks['beforeVisitBinaryExpr']:
            try:
                plugin.beforeVisitBinaryExpr(node)
            except Exception as e:
                print(e)

    def afterVisitBinaryExpr(self, node):
        for plugin in self.hooks['afterVisitBinaryExpr']:
            try:
                plugin.afterVisitBinaryExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitNewExpr(self, node):
        for plugin in self.hooks['beforeVisitNewExpr']:
            try:
                plugin.beforeVisitNewExpr(node)
            except Exception as e:
                print(e)

    def afterVisitNewExpr(self, node):
        for plugin in self.hooks['afterVisitNewExpr']:
            try:
                plugin.afterVisitNewExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitTernaryExpr(self, node):
        for plugin in self.hooks['beforeVisitTernaryExpr']:
            try:
                plugin.beforeVisitTernaryExpr(node)
            except Exception as e:
                print(e)

    def afterVisitTernaryExpr(self, node):
        for plugin in self.hooks['afterVisitTernaryExpr']:
            try:
                plugin.afterVisitTernaryExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitParenExpr(self, node):
        for plugin in self.hooks['beforeVisitParenExpr']:
            try:
                plugin.beforeVisitParenExpr(node)
            except Exception as e:
                print(e)

    def afterVisitParenExpr(self, node):
        for plugin in self.hooks['afterVisitParenExpr']:
            try:
                plugin.afterVisitParenExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitNotExpr(self, node):
        for plugin in self.hooks['beforeVisitNotExpr']:
            try:
                plugin.beforeVisitNotExpr(node)
            except Exception as e:
                print(e)

    def afterVisitNotExpr(self, node):
        for plugin in self.hooks['afterVisitNotExpr']:
            try:
                plugin.afterVisitNotExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitStringExpr(self, node):
        for plugin in self.hooks['beforeVisitStringExpr']:
            try:
                plugin.beforeVisitStringExpr(node)
            except Exception as e:
                print(e)

    def afterVisitStringExpr(self, node):
        for plugin in self.hooks['afterVisitStringExpr']:
            try:
                plugin.afterVisitStringExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitAssignStmt(self, node):
        for plugin in self.hooks['beforeVisitAssignStmt']:
            try:
                plugin.beforeVisitAssignStmt(node)
            except Exception as e:
                print(e)

    def afterVisitAssignStmt(self, node):
        for plugin in self.hooks['afterVisitAssignStmt']:
            try:
                plugin.afterVisitAssignStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitReturnStmt(self, node):
        for plugin in self.hooks['beforeVisitReturnStmt']:
            try:
                plugin.beforeVisitReturnStmt(node)
            except Exception as e:
                print(e)

    def afterVisitReturnStmt(self, node):
        for plugin in self.hooks['afterVisitReturnStmt']:
            try:
                plugin.afterVisitReturnStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitBreakStmt(self, node):
        for plugin in self.hooks['beforeVisitBreakStmt']:
            try:
                plugin.beforeVisitBreakStmt(node)
            except Exception as e:
                print(e)

    # def afterVisitBreakStmt(self, node):
    #     for plugin in self.hooks['afterVisitBreakStmt']:
    #         try:
    #             plugin.afterVisitBreakStmt(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitContinueStmt(self, node):
        for plugin in self.hooks['beforeVisitContinueStmt']:
            try:
                plugin.beforeVisitContinueStmt(node)
            except Exception as e:
                print(e)

    # def afterVisitContinueStmt(self, node):
    #     for plugin in self.hooks['afterVisitContinueStmt']:
    #         try:
    #             plugin.afterVisitContinueStmt(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitRaiseStmt(self, node):
        for plugin in self.hooks['beforeVisitRaiseStmt']:
            try:
                plugin.beforeVisitRaiseStmt(node)
            except Exception as e:
                print(e)

    def afterVisitRaiseStmt(self, node):
        for plugin in self.hooks['afterVisitRaiseStmt']:
            try:
                plugin.afterVisitRaiseStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitExecuteStmt(self, node):
        for plugin in self.hooks['beforeVisitExecuteStmt']:
            try:
                plugin.beforeVisitExecuteStmt(node)
            except Exception as e:
                print(e)

    def afterVisitExecuteStmt(self, node):
        for plugin in self.hooks['afterVisitExecuteStmt']:
            try:
                plugin.afterVisitExecuteStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitCallStmt(self, node):
        for plugin in self.hooks['beforeVisitCallStmt']:
            try:
                plugin.beforeVisitCallStmt(node)
            except Exception as e:
                print(e)

    def afterVisitCallStmt(self, node):
        for plugin in self.hooks['afterVisitCallStmt']:
            try:
                plugin.afterVisitCallStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitIfStmt(self, node):
        for plugin in self.hooks['beforeVisitIfStmt']:
            try:
                plugin.beforeVisitIfStmt(node)
            except Exception as e:
                print(e)

    def afterVisitIfStmt(self, node):
        for plugin in self.hooks['afterVisitIfStmt']:
            try:
                plugin.afterVisitIfStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitElsIfStmt(self, node):
        for plugin in self.hooks['beforeVisitElsIfStmt']:
            try:
                plugin.beforeVisitElsIfStmt(node)
            except Exception as e:
                print(e)

    def afterVisitElsIfStmt(self, node):
        for plugin in self.hooks['afterVisitElsIfStmt']:
            try:
                plugin.afterVisitElsIfStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitElseStmt(self, node):
        for plugin in self.hooks['beforeVisitElseStmt']:
            try:
                plugin.beforeVisitElseStmt(node)
            except Exception as e:
                print(e)

    def afterVisitElseStmt(self, node):
        for plugin in self.hooks['afterVisitElseStmt']:
            try:
                plugin.afterVisitElseStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitWhileStmt(self, node):
        for plugin in self.hooks['beforeVisitWhileStmt']:
            try:
                plugin.beforeVisitWhileStmt(node)
            except Exception as e:
                print(e)

    def afterVisitWhileStmt(self, node):
        for plugin in self.hooks['afterVisitWhileStmt']:
            try:
                plugin.afterVisitWhileStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitForStmt(self, node):
        for plugin in self.hooks['beforeVisitForStmt']:
            try:
                plugin.beforeVisitForStmt(node)
            except Exception as e:
                print(e)

    def afterVisitForStmt(self, node):
        for plugin in self.hooks['afterVisitForStmt']:
            try:
                plugin.afterVisitForStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitForEachStmt(self, node):
        for plugin in self.hooks['beforeVisitForEachStmt']:
            try:
                plugin.beforeVisitForEachStmt(node)
            except Exception as e:
                print(e)

    def afterVisitForEachStmt(self, node):
        for plugin in self.hooks['afterVisitForEachStmt']:
            try:
                plugin.afterVisitForEachStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitTryStmt(self, node):
        for plugin in self.hooks['beforeVisitTryStmt']:
            try:
                plugin.beforeVisitTryStmt(node)
            except Exception as e:
                print(e)

    def afterVisitTryStmt(self, node):
        for plugin in self.hooks['afterVisitTryStmt']:
            try:
                plugin.afterVisitTryStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitExceptStmt(self, node):
        for plugin in self.hooks['beforeVisitExceptStmt']:
            try:
                plugin.beforeVisitExceptStmt(node)
            except Exception as e:
                print(e)

    def afterVisitExceptStmt(self, node):
        for plugin in self.hooks['afterVisitExceptStmt']:
            try:
                plugin.afterVisitExceptStmt(node)
            except Exception as e:
                print(e)

    def beforeVisitGotoStmt(self, node):
        for plugin in self.hooks['beforeVisitGotoStmt']:
            try:
                plugin.beforeVisitGotoStmt(node)
            except Exception as e:
                print(e)

    # def afterVisitGotoStmt(self, node):
    #     for plugin in self.hooks['afterVisitGotoStmt']:
    #         try:
    #             plugin.afterVisitGotoStmt(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitLabelStmt(self, node):
        for plugin in self.hooks['beforeVisitLabelStmt']:
            try:
                plugin.beforeVisitLabelStmt(node)
            except Exception as e:
                print(e)

    # def afterVisitLabelStmt(self, node):
    #     for plugin in self.hooks['afterVisitLabelStmt']:
    #         try:
    #             plugin.afterVisitLabelStmt(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitPrepIfInst(self, node):
        for plugin in self.hooks['beforeVisitPrepIfInst']:
            try:
                plugin.beforeVisitPrepIfInst(node)
            except Exception as e:
                print(e)

    def afterVisitPrepIfInst(self, node):
        for plugin in self.hooks['afterVisitPrepIfInst']:
            try:
                plugin.afterVisitPrepIfInst(node)
            except Exception as e:
                print(e)

    # PrepElsIfInst

    def beforeVisitPrepElsIfInst(self, node):
        for plugin in self.hooks['beforeVisitPrepElsIfInst']:
            try:
                plugin.beforeVisitPrepElsIfInst(node)
            except Exception as e:
                print(e)

    def afterVisitPrepElsIfInst(self, node):
        for plugin in self.hooks['afterVisitPrepElsIfInst']:
            try:
                plugin.afterVisitPrepElsIfInst(node)
            except Exception as e:
                print(e)

    # PrepElseInst

    def beforeVisitPrepElseInst(self, node):
        for plugin in self.hooks['beforeVisitPrepElseInst']:
            try:
                plugin.beforeVisitPrepElseInst(node)
            except Exception as e:
                print(e)

    # def afterVisitPrepElseInst(self, node):
    #     for plugin in self.hooks['afterVisitPrepElseInst']:
    #         try:
    #             plugin.afterVisitPrepElseInst(node)
    #         except Exception as e:
    #             print(e)

    # PrepEndIfInst

    def beforeVisitPrepEndIfInst(self, node):
        for plugin in self.hooks['beforeVisitPrepEndIfInst']:
            try:
                plugin.beforeVisitPrepEndIfInst(node)
            except Exception as e:
                print(e)

    # def afterVisitPrepEndIfInst(self, node):
    #     for plugin in self.hooks['afterVisitPrepEndIfInst']:
    #         try:
    #             plugin.afterVisitPrepEndIfInst(node)
    #         except Exception as e:
    #             print(e)

    # PrepRegionInst

    def beforeVisitPrepRegionInst(self, node):
        for plugin in self.hooks['beforeVisitPrepRegionInst']:
            try:
                plugin.beforeVisitPrepRegionInst(node)
            except Exception as e:
                print(e)

    # def afterVisitPrepRegionInst(self, node):
    #     for plugin in self.hooks['afterVisitPrepRegionInst']:
    #         try:
    #             plugin.afterVisitPrepRegionInst(node)
    #         except Exception as e:
    #             print(e)

    # PrepEndRegionInst

    def beforeVisitPrepEndRegionInst(self, node):
        for plugin in self.hooks['beforeVisitPrepEndRegionInst']:
            try:
                plugin.beforeVisitPrepEndRegionInst(node)
            except Exception as e:
                print(e)

    # def afterVisitPrepEndRegionInst(self, node):
    #     for plugin in self.hooks['afterVisitPrepEndRegionInst']:
    #         try:
    #             plugin.afterVisitPrepEndRegionInst(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitPrepBinaryExpr(self, node):
        for plugin in self.hooks['beforeVisitPrepBinaryExpr']:
            try:
                plugin.beforeVisitPrepBinaryExpr(node)
            except Exception as e:
                print(e)

    def afterVisitPrepBinaryExpr(self, node):
        for plugin in self.hooks['afterVisitPrepBinaryExpr']:
            try:
                plugin.afterVisitPrepBinaryExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitPrepNotExpr(self, node):
        for plugin in self.hooks['beforeVisitPrepNotExpr']:
            try:
                plugin.beforeVisitPrepNotExpr(node)
            except Exception as e:
                print(e)

    def afterVisitPrepNotExpr(self, node):
        for plugin in self.hooks['afterVisitPrepNotExpr']:
            try:
                plugin.afterVisitPrepNotExpr(node)
            except Exception as e:
                print(e)

    def beforeVisitPrepSymExpr(self, node):
        for plugin in self.hooks['beforeVisitPrepSymExpr']:
            try:
                plugin.beforeVisitPrepSymExpr(node)
            except Exception as e:
                print(e)

    # def afterVisitPrepSymExpr(self, node):
    #     for plugin in self.hooks['afterVisitPrepSymExpr']:
    #         try:
    #             plugin.afterVisitPrepSymExpr(node)
    #         except Exception as e:
    #             print(e)

    def beforeVisitPrepParenExpr(self, node):
        for plugin in self.hooks['beforeVisitPrepParenExpr']:
            try:
                plugin.beforeVisitPrepParenExpr(node)
            except Exception as e:
                print(e)

    def afterVisitPrepParenExpr(self, node):
        for plugin in self.hooks['afterVisitPrepParenExpr']:
            try:
                plugin.afterVisitPrepParenExpr(node)
            except Exception as e:
                print(e)

