# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from abc import abstractmethod

class Plugin:

    # TODO: плагину должны быть известны путь к файлу и путь внутри файла

    def __init__(self, path: str):
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

    # Configuration

    def beforeVisitConfiguration(self, node):
        self.perform('beforeVisitConfiguration', node)

    def afterVisitConfiguration(self, node):
        self.perform('afterVisitConfiguration', node)

    # ConfigurationProperties

    def beforeVisitConfigurationProperties(self, node):
        self.perform('beforeVisitConfigurationProperties', node)

    def afterVisitConfigurationProperties(self, node):
        self.perform('afterVisitConfigurationProperties', node)

    # CommonModule

    def beforeVisitCommonModule(self, node):
        self.perform('beforeVisitCommonModule', node)

    def afterVisitCommonModule(self, node):
        self.perform('afterVisitCommonModule', node)

    # CommonModuleProperties

    def beforeVisitCommonModuleProperties(self, node):
        self.perform('beforeVisitCommonModuleProperties', node)

    def afterVisitCommonModuleProperties(self, node):
        self.perform('afterVisitCommonModuleProperties', node)

    # LocalStringType

    def beforeVisitLocalStringType(self, node):
        self.perform('beforeVisitLocalStringType', node)

    def afterVisitLocalStringType(self, node):
        self.perform('afterVisitLocalStringType', node)

    # LocalStringTypeItem

    def beforeVisitLocalStringTypeItem(self, node):
        self.perform('beforeVisitLocalStringTypeItem', node)