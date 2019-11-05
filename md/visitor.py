# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from abc import ABC, abstractmethod
from typing import List
from enum import Enum, auto

class Plugin(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def close(self) -> str:
        pass

class ModuleKinds(Enum):
    ObjectModule = auto()
    ManagerModule = auto()
    ManagedFormModule = auto()

class ModuleFile:

    def __init__(self, kind, path, context=None):
        self.kind: ModuleKinds = kind
        self.path: str = path
        self.context = context

    def __repr__(self):
        return f'{self.kind.name}: {self.path}'

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

        self.modules: List[ModuleFile] = []

    def perform(self, func_name, node):
        for hook in self.hooks[func_name]:
            try:
                hook(node)
            except Exception as e:
                print(e)

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

    #endregion forms