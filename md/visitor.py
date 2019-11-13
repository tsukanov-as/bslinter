# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from abc import ABC, abstractmethod
from typing import List, Dict, Callable
from enum import Enum, auto
from bsl.glob import scope as global_scope
from bsl.ast import Scope
from plugins import Plugin

class ModuleKinds(Enum):
    ObjectModule = auto()
    ManagerModule = auto()
    ManagedFormModule = auto()
    CommonModule = auto()

class ModuleFile:

    def __init__(self, kind, path, scope=None):
        self.kind: ModuleKinds = kind
        self.path: str = path
        self.scope = scope

    def __repr__(self):
        return f'{self.kind.name}: {self.path}'

class Visitor:

    def __init__(self, plugins: List[Plugin]):

        methods = [func for func in dir(self)
                            if callable(getattr(self, func))
                                and (func.startswith("visit_")
                                     or func.startswith("leave_"))]

        self.hooks: Dict[str, List[Callable]] = {}

        for name in methods:
            hooks: List[Callable] = []
            self.hooks[name] = hooks
            for plugin in plugins:
                if hook := getattr(plugin, name, None):
                    hooks.append(hook)

        self.modules: List[ModuleFile] = []
        self.global_modules: List[ModuleFile] = []

        self.scope: Scope = global_scope

    def perform(self, func_name, node):
        for hook in self.hooks[func_name]:
            try:
                hook(node)
            except Exception as e:
                print(e)

    def open_scope(self) -> Scope:
        scope = Scope(self.scope)
        self.scope = scope
        return scope

    def close_scope(self) -> Scope:
        scope = self.scope.Outer
        assert scope is not None
        self.scope = scope
        return scope

    #region conf

    # Configuration

    def visit_Configuration(self, node):
        self.perform('visit_Configuration', node)

    def leave_Configuration(self, node):
        self.perform('leave_Configuration', node)

    # ConfigurationProperties

    def visit_ConfigurationProperties(self, node):
        self.perform('visit_ConfigurationProperties', node)

    def leave_ConfigurationProperties(self, node):
        self.perform('leave_ConfigurationProperties', node)

    # ConfigurationChildObjects

    def visit_ConfigurationChildObjects(self, node):
        self.perform('visit_ConfigurationChildObjects', node)

    def leave_ConfigurationChildObjects(self, node):
        self.perform('leave_ConfigurationChildObjects', node)

    # CommonModule

    def visit_CommonModule(self, node):
        self.perform('visit_CommonModule', node)

    def leave_CommonModule(self, node):
        self.perform('leave_CommonModule', node)

    # CommonModuleProperties

    def visit_CommonModuleProperties(self, node):
        self.perform('visit_CommonModuleProperties', node)

    def leave_CommonModuleProperties(self, node):
        self.perform('leave_CommonModuleProperties', node)

    # Document

    def visit_Document(self, node):
        self.perform('visit_Document', node)

    def leave_Document(self, node):
        self.perform('leave_Document', node)

    # DocumentChildObjects

    def visit_DocumentChildObjects(self, node):
        self.perform('visit_DocumentChildObjects', node)

    def leave_DocumentChildObjects(self, node):
        self.perform('leave_DocumentChildObjects', node)

    # LocalStringType

    def visit_LocalStringType(self, node):
        self.perform('visit_LocalStringType', node)

    def leave_LocalStringType(self, node):
        self.perform('leave_LocalStringType', node)

    # LocalStringTypeItem

    def visit_LocalStringTypeItem(self, node):
        self.perform('visit_LocalStringTypeItem', node)

    # StandardAttribute

    def visit_StandardAttribute(self, node):
        self.perform('visit_StandardAttribute', node)

    def leave_StandardAttribute(self, node):
        self.perform('leave_StandardAttribute', node)

    # StandardAttributes

    def visit_StandardAttributes(self, node):
        self.perform('visit_StandardAttributes', node)

    def leave_StandardAttributes(self, node):
        self.perform('leave_StandardAttributes', node)

    # Attribute

    def visit_Attribute(self, node):
        self.perform('visit_Attribute', node)

    def leave_Attribute(self, node):
        self.perform('leave_Attribute', node)

    # AttributeProperties

    def visit_AttributeProperties(self, node):
        self.perform('visit_AttributeProperties', node)

    def leave_AttributeProperties(self, node):
        self.perform('leave_AttributeProperties', node)

    # TabularSection

    def visit_TabularSection(self, node):
        self.perform('visit_TabularSection', node)

    def leave_TabularSection(self, node):
        self.perform('leave_TabularSection', node)

    # TabularSectionProperties

    def visit_TabularSectionProperties(self, node):
        self.perform('visit_TabularSectionProperties', node)

    def leave_TabularSectionProperties(self, node):
        self.perform('leave_TabularSectionProperties', node)

    # Form

    def visit_Form(self, node):
        self.perform('visit_Form', node)

    def leave_Form(self, node):
        self.perform('leave_Form', node)

    # FormProperties

    def visit_FormProperties(self, node):
        self.perform('visit_FormProperties', node)

    def leave_FormProperties(self, node):
        self.perform('leave_FormProperties', node)

    #endregion conf

    #region forms

    # ManagedForm

    def visit_ManagedForm(self, node):
        self.perform('visit_ManagedForm', node)

    def leave_ManagedForm(self, node):
        self.perform('leave_ManagedForm', node)

    # FormAttributes

    def visit_FormAttributes(self, node):
        self.perform('visit_FormAttributes', node)

    def leave_FormAttributes(self, node):
        self.perform('leave_FormAttributes', node)

    # FormAttribute

    def visit_FormAttribute(self, node):
        self.perform('visit_FormAttribute', node)

    def leave_FormAttribute(self, node):
        self.perform('leave_FormAttribute', node)

    #endregion forms