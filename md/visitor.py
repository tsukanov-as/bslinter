# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from abc import ABC, abstractmethod

class Plugin(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def close(self) -> str:
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

    # LocalStringType

    def visit_LocalStringType(self, node):
        self.perform('visit_LocalStringType', node)

    def leave_LocalStringType(self, node):
        self.perform('leave_LocalStringType', node)

    # LocalStringTypeItem

    def visit_LocalStringTypeItem(self, node):
        self.perform('visit_LocalStringTypeItem', node)