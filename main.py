# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import List, Optional

from md.base import XMLParser
import md.conf as cf
import md.visitor
import bsl.visitor
import bsl.ast as ast
from bsl.parser import Parser

import plugins.bsl.comments as comments
import plugins.bsl.warnings as warnings
import plugins.bsl.errors as errors
from plugins.md.conf.translation import DocumentStandardAttributes
from plugins.md.conf.rights import InteractiveDelete
import reports.sonar as sonar

import time
import concurrent.futures
import os.path

def parse(module):
    if os.path.isfile(module.path):
        with open(module.path, 'r', encoding='utf-8-sig') as f:
            src = f.read()
            parser = Parser(src, module.scope)
            try:
                ast = parser.parse()
                plugins = [
                    comments.ClosingComments(module.path, src),
                    comments.CommentedOutCode(module.path, src),
                    warnings.UnusedVariables(module.path, src),
                    warnings.EmptyExcept(module.path, src),
                    warnings.Concatenation(module.path, src),
                    warnings.StructureConstructor(module.path, src),
                    errors.DuplicateConditions(module.path, src),
                ]
                visitor = bsl.visitor.Visitor(plugins)
                ast.visit(visitor)
                results = [p.close().items for p in plugins]
                return results
            except Exception as e:
                print(module.path)
                print(e)


def main():

    issues = []

    strt = time.perf_counter()

    path = "C:/dev/sonarqube/myprj/src/Configuration.xml"
    plugins = [
        DocumentStandardAttributes(),
        InteractiveDelete(),
    ]
    root = XMLParser(path, cf.Root).parse()
    visitor = md.visitor.Visitor(plugins)
    mdo: Optional[cf.MetaDataObject] = root.MetaDataObject
    if mdo is not None and mdo.Configuration is not None:
        mdo.Configuration.visit(visitor)

    results = [p.close().items for p in plugins]
    for result in results:
        for issue in result:
            issues.append(issue)

    print('md time: ', time.perf_counter() - strt)

    # -------------------------------------------------------------------------

    strt = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results_list = executor.map(parse, visitor.modules)

    with open("C:/dev/sonarqube/myprj/bsl-generic-json.json", 'w', encoding='utf-8') as f:
        for results in results_list:
            if results:
                for result in results:
                    for issue in result:
                        issues.append(issue)
        x = sonar.fromIssues(issues)
        f.write(x.toJSON())

    print('bsl time: ', time.perf_counter() - strt)

    print('issues count: ', len(issues))

if __name__ == "__main__":
    main()