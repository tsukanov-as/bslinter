# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import xml.parsers.expat
from enum import EnumMeta
from typing import Optional, Dict, Tuple, List, Any, get_type_hints, get_args, get_origin # type: ignore
from md.visitor import Visitor

class TypeDescription:
    def __init__(self, mt, ls):
        self.meta = mt
        self.list = ls

class XMLData:

    _types: Dict[str, TypeDescription]

    def __init__(self):
        self._path: str = ''
        self._startLine: int = 0
        self._endLine: int = 0
        self._startColumn: int = 0
        self._endColumn: int = 0

    def __getattr__(self, name):
        return None

    def visit(self, visitor: Visitor):
        pass

class XMLFile(XMLData):

    def walk(self, visitor: Visitor):
        self.visit(visitor)

class OrderedXMLData(XMLData):

    pass

class XMLParser:

    def __init__(self, path, meta):

        self.path = path
        self.parser = p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start
        p.EndElementHandler = self.end
        p.CharacterDataHandler = self.chardata
        self.meta = meta
        self.item = meta()
        self.name = ""
        self.stack = []

    def parse(self):

        with open(self.path, 'r', encoding='utf-8-sig') as f:
            src = f.read()
            self.parser.Parse(src)
        # self.parser.ParseFile(open(self.path, mode='rb'))  # быстрее, но подглючивает (вставляет лишние переносы строк)
        return self.item

    def start(self, name, attrs):

        self.stack.append([self.meta, self.item, self.name])

        if self.meta is None:
            return

        if (i := name.find(':')) >= 0:
            name = name[i+1:]

        item = None
        if td := self.meta._types.get(name):
            if td.list:
                items = getattr(self.item, name)
                if items is None:
                    items = []
                    setattr(self.item, name, items)
                if issubclass(td.meta, OrderedXMLData):
                    item = items
                elif issubclass(td.meta, XMLData):
                    item = td.meta()
                    item._path = self.path
                    item._startLine = self.parser.CurrentLineNumber
                    item._startColumn = self.parser.CurrentColumnNumber
                    items.append(item)
            else:
                if issubclass(td.meta, XMLData):
                    item = td.meta()
                    item._path = self.path
                    item._startLine = self.parser.CurrentLineNumber
                    item._startColumn = self.parser.CurrentColumnNumber
                    if issubclass(self.meta, OrderedXMLData):
                        self.item.append(item)
                    else:
                        setattr(self.item, name, item)
                    for key, data in attrs.items():
                        attr = key
                        if (i := attr.find(':')) >= 0:
                            attr = attr[i+1:]
                        if attrtd := td.meta._types.get(attr):
                            if type(attrtd.meta) == EnumMeta:
                                setattr(item, attr, attrtd.meta.get(data))
                            else:
                                setattr(item, attr, attrtd.meta(data))
                            pass
            self.meta = td.meta
        else:
            self.meta = None

        self.item = item
        self.name = name

    def end(self, name):
        if isinstance(self.item, XMLData):
            self.item._endLine = self.parser.CurrentLineNumber
            self.item._endColumn = self.parser.CurrentColumnNumber + len(name) + 3  # </name>
        self.meta, self.item, self.name = self.stack.pop()

    def chardata(self, data):

        if self.meta is None:
            return

        if self.item is None:
            item = self.stack[-1][1]
            if type(self.meta) == EnumMeta:
                value = self.meta.get(data)
            else:
                value = self.meta(data)
            array = getattr(item, self.name)
            if type(array) == list:
                array.append(value)
            else:
                setattr(item, self.name, value)
        elif td := self.meta._types.get('_text'):
            if type(td.meta) == EnumMeta:
                value = td.meta.get(data)
            else:
                value = td.meta(data)
            setattr(self.item, '_text', value)
            pass

def fill_types(ns: dict):
    for cls in ns.values():
        if type(cls) == type and issubclass(cls, XMLData):
            hints = get_type_hints(cls)
            cls._types = {}
            for name, hint in hints.items():
                if name != '_types':
                    args = get_args(hint)
                    orig = get_origin(hint)
                    meta = args[0]
                    cls._types[name] = TypeDescription(meta, orig == list or issubclass(meta, OrderedXMLData))
