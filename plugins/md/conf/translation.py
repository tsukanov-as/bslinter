# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import md.conf as cf
from typing import List, Dict, Optional
from output.issues import Issue, Issues, Kind, Severity, Location, IssueCollector
import os.path

class CheckingDocumentStandardAttributes(IssueCollector):

    def __init__(self):

        self.errors: List[Issue] = []

    def close(self) -> Issues:
        return Issues(self.errors)

    def visit_DocumentProperties(self, node: cf.DocumentProperties):
        cheklist: Dict[str, Optional[cf.StandardAttribute]] = {
            'Number': None,
            'Date': None,
        }
        if node.StandardAttributes:
            if attribs := node.StandardAttributes.StandardAttribute:
                for attrib in attribs:
                    if attrib.name:
                        cheklist[attrib.name] = attrib
        x = cheklist['Number']
        if x and x.Synonym and not x.Synonym.get('en'):
            self.issue('Не задан английский синоним для номера', x.Synonym)
        x = cheklist['Date']
        if x and x.Synonym and not x.Synonym.get('en'):
            self.issue('Не задан английский синоним для даты', x.Synonym)

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
