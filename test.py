# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from bsl.parser  import Parser
from bsl.visitor import Plugin, Visitor
import bsl.ast as ast

import xml.etree.ElementTree as ET
import md.conf as cf
import md.forms as fm

import time
import pathlib
import concurrent.futures


class TestPlugin(Plugin):

    def __init__(self, path, src):

        self.path = path
        self.src = src
        self.comments = {}
        self.region_stack = []
        self.errors = []

    def result(self) -> str:
        return '\n'.join(self.errors)

    def beforeVisitModule(self, node: ast.Module):
        self.comments = node.Comments

    def beforeVisitMethodDecl(self, node: ast.MethodDecl):
        line = node.Place.EndLine
        if comment := self.comments.get(line):
            if comment.rstrip() != f' {node.Sign.Name}()':
                self.errors.append(f'[{self.path}] Метод "{node.Sign.Name}()" имеет неправильный замыкающий комментарий в строке {line}')

    def beforeVisitPrepRegionInst(self, node: ast.PrepRegionInst):
        self.region_stack.append(node.Name)

    def beforeVisitPrepEndRegionInst(self, node: ast.PrepEndRegionInst):
        line = node.Place.EndLine
        region_name = self.region_stack.pop()
        if comment := self.comments.get(line):
            if comment.rstrip() != f' {region_name}':
                self.errors.append(f'[{self.path}] Область "{region_name}" имеет неправильный замыкающий комментарий в строке {line}')

def parse(path):
    with open(str(path), 'r', encoding='utf-8-sig') as f:
        s = f.read()
        p = Parser(s)
        try:
            m = p.parse()
            plugins = [TestPlugin(str(path), s)]
            v = Visitor(plugins)
            m.visit(v)
            return plugins[0].result()
        except Exception as e:
            print(path)
            print(e)

def main():

    strt = time.perf_counter()

    mypath = "C:/temp/ERP"
    result = list(pathlib.Path(mypath).rglob("*.[bB][sS][lL]"))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.map(parse, result)

    with open('res.txt', 'w', encoding='utf-8') as f:
        for x in result:
            if x:
                f.write(x)
                f.write('\n')

    print('bsl time: ', time.perf_counter() - strt) # 80 sec

    strt = time.perf_counter()

    result = list(pathlib.Path(mypath).rglob("*.xml"))
    for path in result:
        if path:
            if str(path).endswith('Form.xml'):
                tree = ET.ElementTree(file=str(path))
                root = tree.getroot()
                form = fm.ManagedForm()
                form.unmarshal(root)
            elif not str(path).endswith('Template.xml'):
                tree = ET.ElementTree(file=str(path))
                root = tree.getroot()
                doc = cf.MetaDataObject()
                doc.unmarshal(root)
            pass

    print('metadata time: ', time.perf_counter() - strt) # 60 sec


if __name__ == "__main__":
    main()