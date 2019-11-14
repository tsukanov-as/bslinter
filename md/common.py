# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import List, Optional
from decimal import Decimal
import md.enums as enums
from md.base import XMLData, fill_types
from md.visitor import Visitor

Uuid = str
QName = str
MDObjectRef = str

#region types

class NumberQualifiers(XMLData):
    Digits:         Optional[Decimal]
    FractionDigits: Optional[Decimal]
    AllowedSign:    Optional[enums.AllowedSign]

class StringQualifiers(XMLData):
    Length:        Optional[Decimal]
    AllowedLength: Optional[enums.AllowedLength]

class DateQualifiers(XMLData):
    DateFractions: Optional[enums.DateFractions]

class BinaryDataQualifiers(XMLData):
    Length:        Optional[Decimal]
    AllowedLength: Optional[enums.AllowedLength]

class TypeDescription(XMLData):
    Type:                 Optional[QName]
    TypeSet:              Optional[QName]
    TypeId:               Optional[Uuid]
    NumberQualifiers:     Optional[NumberQualifiers]
    StringQualifiers:     Optional[StringQualifiers]
    DateQualifiers:       Optional[DateQualifiers]
    BinaryDataQualifiers: Optional[BinaryDataQualifiers]

#endregion types


class ChoiceParameterLink(XMLData):
    Name:        Optional[str]
    DataPath:    Optional[str]
    ValueChange: Optional[enums.LinkedValueChangeMode]


class ChoiceParameterLinks(XMLData):
    Link: List[ChoiceParameterLink]


class LocalStringTypeItem(XMLData):
    lang:    Optional[str]
    content: Optional[str]

    def visit(self, visitor: Visitor):
        visitor.visit_LocalStringTypeItem(self)


class LocalStringType(XMLData):
    item: List[LocalStringTypeItem]

    def visit(self, visitor: Visitor):
        visitor.visit_LocalStringType(self)
        if self.item is not None:
            for item in self.item:
                item.visit(visitor)
        visitor.leave_LocalStringType(self)

    def get(self, lang: str):
        if not self.item:
            return None
        for value in self.item:
            if value.lang == lang:
                return value.content
        return None