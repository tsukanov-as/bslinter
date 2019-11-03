
from typing import List

import md.conf as cf
from md.visitor import Plugin, Visitor

class TestPlugin(Plugin):

    def __init__(self):

        self.errors: List[str] = []

    def result(self) -> str:
        return '\n'.join(self.errors)

    def beforeVisitLocalStringTypeItem(self, node: cf.LocalStringTypeItem):
        self.errors.append(f'Синоним для языка {node.lang} = {node.content}')



z = cf.Configuration('C:/temp/ERP/Configuration.xml')
plugins = [TestPlugin()]
v = Visitor(plugins)
z.walk(v)
print(plugins[0].result())