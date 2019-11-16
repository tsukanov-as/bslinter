# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import List, Optional
from md.base import XMLData, XMLFile, XMLParser, fill_types

import md.enums as enums
from md.visitor import Visitor

class RestrictionByCondition(XMLData):
    condition: Optional[str]

    def visit(self, visitor: Visitor):
        visitor.visit_RestrictionByCondition(self)

class Right(XMLData):
    name: Optional[str]
    value: Optional[enums.Bool]
    restrictionByCondition: Optional[RestrictionByCondition]

    def visit(self, visitor: Visitor):
        visitor.visit_Right(self)
        if self.restrictionByCondition:
            self.restrictionByCondition.visit(visitor)
        visitor.leave_Right(self)

class ObjectRight(XMLData):
    name: Optional[str]
    right: List[Right]

    def visit(self, visitor: Visitor):
        visitor.visit_ObjectRight(self)
        if self.right:
            for item in self.right:
                item.visit(visitor)
        visitor.leave_ObjectRight(self)

class RestrictionTemplate(XMLData):
    name: Optional[str]
    condition: Optional[str]

    def visit(self, visitor: Visitor):
        visitor.visit_RestrictionTemplate(self)

class Rights(XMLData):
    setForNewObjects: Optional[enums.Bool]
    setForAttributesByDefault: Optional[enums.Bool]
    independentRightsOfChildObjects: Optional[enums.Bool]
    restrictionTemplate: Optional[RestrictionTemplate]
    object: List[ObjectRight]

    def visit(self, visitor: Visitor):
        visitor.visit_Rights(self)
        if self.restrictionTemplate:
            self.restrictionTemplate.visit(visitor)
        if self.object:
            for item in self.object:
                item.visit(visitor)
        visitor.leave_Rights(self)

class Root(XMLFile):
    Rights: Optional[Rights]


fill_types(globals())