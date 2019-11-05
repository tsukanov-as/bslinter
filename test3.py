# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import List, Optional

from md.base import XMLParser
import md.conf as cf
from md.visitor import Plugin as mdPlugin, Visitor as mdVisitor
from bsl.visitor import Plugin, Visitor

import bsl.ast as ast
from bsl.parser import Parser

import time
import concurrent.futures

import os.path

class TestPlugin(Plugin):

    def __init__(self, path, src):

        self.path = path
        self.src = src
        self.comments = {}
        self.region_stack = []
        self.errors = []

    def close(self) -> str:
        return '\n'.join(self.errors)

    def visit_Module(self, node: ast.Module):
        self.comments = node.Comments

    def visit_MethodDecl(self, node: ast.MethodDecl):
        line = node.Place.EndLine
        if comment := self.comments.get(line):
            if comment.rstrip() != f' {node.Sign.Name}()':
                self.errors.append(f'[{self.path}] Метод "{node.Sign.Name}()" имеет неправильный замыкающий комментарий в строке {line}')

    def visit_PrepRegionInst(self, node: ast.PrepRegionInst):
        self.region_stack.append(node.Name)

    def visit_PrepEndRegionInst(self, node: ast.PrepEndRegionInst):
        line = node.Place.EndLine
        region_name = self.region_stack.pop()
        if comment := self.comments.get(line):
            if comment.rstrip() != f' {region_name}':
                self.errors.append(f'[{self.path}] Область "{region_name}" имеет неправильный замыкающий комментарий в строке {line}')

def parse(module):
    if os.path.isfile(module.path):
        with open(module.path, 'r', encoding='utf-8-sig') as f:
            s = f.read()
            p = Parser(s)
            try:
                m = p.parse()
                plugins = [TestPlugin(module.path, s)]
                v = Visitor(plugins)
                m.visit(v)
                return plugins[0].close()
            except Exception as e:
                print(module.path)
                print(e)


def main():

    strt = time.perf_counter()

    path = 'C:/temp/ERP/Configuration.xml'
    root = XMLParser(path, cf.Root).parse()
    plugins: List[mdPlugin] = []
    v = mdVisitor(plugins)
    mdo: Optional[cf.MetaDataObject] = root.MetaDataObject
    if mdo is not None and mdo.Configuration is not None:
        mdo.Configuration.visit(v)

    # for module in v.modules:
    #     print(module)

    print('metadata time: ', time.perf_counter() - strt) # 11 sec


    strt = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.map(parse, v.modules)

    with open('res.txt', 'w', encoding='utf-8') as f:
        for x in result:
            if x:
                f.write(x)
                f.write('\n')

    print('bsl time: ', time.perf_counter() - strt) # 12 sec


if __name__ == "__main__":
    main()