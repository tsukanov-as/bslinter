# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import md.conf as cf
from typing import List, Dict, Optional
from output.issues import Issue, Issues, Kind, Severity, Location, IssueCollector
import os.path

class CheckingDocumentStandardAttributes(IssueCollector):

    # TODO: обработать случай, когда стандартного реквизита вообще нет в xml

    def __init__(self):
        self.languages = {}
        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_LanguageProperties(self, node: cf.LanguageProperties):
        self.languages[node.LanguageCode] = node.Name

    def visit_DocumentProperties(self, node: cf.DocumentProperties):
        if len(self.languages) < 2:
            return
        cheklist: Dict[str, Optional[cf.StandardAttribute]] = {
            'Ref': None,
            'Number': None,
            'Date': None,
            'Posted': None,
            'DeletionMark': None,
        }
        if node.StandardAttributes:
            if attribs := node.StandardAttributes.StandardAttribute:
                for attrib in attribs:
                    if attrib.name:
                        cheklist[attrib.name] = attrib
        for k, v in cheklist.items():
            if v and v.Synonym:
                for lang in self.languages:
                    if not v.Synonym.get(lang):
                        self.issue(f'Не задан синоним стандартного реквизита "{k}" для языка "{lang}"', v.Synonym)

    def issue(self, msg, node):
        self.errors.append(Issue(
            Kind.CODE_SMELL,
            Severity.INFO,
            msg,
            2,
            Location(
                os.path.normpath(node._path),
                node._startLine,
                node._endLine,
                node._startColumn,
                node._endColumn,
            )
        ))
