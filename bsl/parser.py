# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from decimal import Decimal
from typing import List, Union, Dict, Optional, TypeVar, Tuple
from collections import namedtuple
from bsl.enums import Tokens, Keywords, Directives, PrepInstructions, PrepSymbols
import bsl.ast as ast

tokens_map: Dict[str, Tokens] = {
    '=': Tokens.EQL,
    '+': Tokens.ADD,
    '-': Tokens.SUB,
    '*': Tokens.MUL,
    '%': Tokens.MOD,
    '(': Tokens.LPAREN,
    ')': Tokens.RPAREN,
    '[': Tokens.LBRACK,
    ']': Tokens.RBRACK,
    '?': Tokens.TERNARY,
    ',': Tokens.COMMA,
    '.': Tokens.PERIOD,
    ':': Tokens.COLON,
    ';': Tokens.SEMICOLON,
    '': Tokens.EOF,
}

add_operators = {
    Tokens.ADD,
    Tokens.SUB,
}

mul_operators = {
    Tokens.MUL,
    Tokens.DIV,
    Tokens.MOD,
}

rel_operators = {
    Tokens.EQL,
    Tokens.NEQ,
    Tokens.LSS,
    Tokens.GTR,
    Tokens.LEQ,
    Tokens.GEQ,
}

basic_lit_no_string = {
    Tokens.NUMBER,
    Tokens.DATETIME,
    Keywords.TRUE,
    Keywords.FALSE,
    Keywords.UNDEFINED,
    Keywords.NULL,
}

init_of_expr = {
    Tokens.ADD,
    Tokens.SUB,
    Tokens.IDENT,
    Tokens.LPAREN,
    Tokens.NUMBER,
    Tokens.STRING,
    Tokens.STRINGBEG,
    Tokens.DATETIME,
    Tokens.TERNARY,
    Keywords.NOT,
    Keywords.NEW,
    Keywords.TRUE,
    Keywords.FALSE,
    Keywords.UNDEFINED,
    Keywords.NULL,
}

Error = namedtuple('Error', 'text line pos')

TypeParser = TypeVar('TypeParser', bound='Parser')
class Parser:

    def __init__(self: TypeParser, src: str):

        self.src: str = src

        self.beg_pos: int = -1
        self.cur_pos: int = -1
        self.end_pos: int = -1

        self.cur_line: int = 1
        self.end_line: int = 1

        self.char: str = ""
        self.lit: str = ""
        self.tok: Tokens
        self.val: Union[Decimal, str, bool, None]

        self.scope: ast.Scope = ast.Scope()  # TODO: context
        self.vars: Dict[str, ast.Item] = {}
        self.methods: Dict[str, ast.Item] = {}
        self.unknown: Dict[str, ast.Item] = {}

        self.callsites: Dict[ast.Item, List[ast.Place]] = {}

        self.is_func: bool = False
        self.allow_var: bool = True
        self.directive: Optional[Directives] = None
        self.interface: List[ast.Item] = []

        self.comments: Dict[int, str] = {}

        self.errors: List[Error] = []

        self.scan()

    def next(self: TypeParser) -> str:
        self.cur_pos += 1
        self.char = self.src[self.cur_pos:self.cur_pos+1]
        return self.char

    def scan(self: TypeParser) -> Tokens:

        self.end_pos = self.cur_pos
        self.end_line = self.cur_line

        self.val = None

        if self.lit[-1:] == '\n':
            self.cur_line += 1

        while 1:

            comment = False

            # skip space
            while self.char.isspace():
                if self.char == '\n':
                    self.cur_line += 1
                self.next()

            self.beg_pos = self.cur_pos

            if self.char.isalpha() or self.char == '_':

                # scan ident
                beg = self.cur_pos
                while self.next().isalnum() or self.char == '_':
                    pass
                self.lit = self.src[beg:self.cur_pos]

                # lookup
                tok = Keywords.get(self.lit)
                if tok is not None:
                    if tok is Keywords.TRUE:
                        self.val = True
                    elif tok is Keywords.FALSE:
                        self.val = False
                    elif tok is Keywords.NULL:
                        self.val = None
                    self.tok = tok
                    # TODO: canonical
                else:
                    self.tok = Tokens.IDENT

            elif self.char == '"':

                beg = self.cur_pos

                while self.char == '"':
                    while self.next() not in ['"', '\n', '']:
                        pass
                    if self.char != '':
                        self.next()

                self.lit = self.src[beg:self.cur_pos]
                self.val = self.lit[1:-1].replace('""', '"')

                if self.lit[-1] == '"':
                    self.tok = Tokens.STRING
                else:
                    self.tok = Tokens.STRINGBEG

            elif self.char == '|':

                beg = self.cur_pos

                self.char = '"'  # cheat code
                while self.char == '"':
                    while self.next() not in ['"', '\n', '']:
                        pass
                    if self.char != '':
                        self.next()

                self.lit = self.src[beg:self.cur_pos]
                self.val = self.lit[1:-1].replace('""', '"')

                if self.lit[-1] == '"':
                    self.tok = Tokens.STRINGEND
                else:
                    self.tok = Tokens.STRINGMID

            elif self.char.isdigit():

                beg = self.cur_pos

                while self.next().isdigit():
                    pass
                if self.char == '.':
                    while self.next().isdigit():
                        pass

                self.lit = self.src[beg:self.cur_pos]
                self.val = Decimal(self.lit)
                self.tok = Tokens.NUMBER

            elif self.char == "'":

                beg = self.cur_pos

                while self.next() not in ["'", '\n', '']:
                    pass

                if self.char != '':
                    self.lit = self.src[beg:self.cur_pos]
                    self.val = self.lit
                    self.next()

                self.tok = Tokens.DATETIME

            elif self.char == '/':

                if self.next() == '/':

                    # scan comment
                    beg = self.cur_pos + 1
                    pos = self.src.find('\n', beg)
                    if pos >= 0:
                        self.cur_pos = pos
                        self.char = '\n'
                        self.comments[self.cur_line] = self.src[beg:self.cur_pos]
                    else:
                        self.cur_pos = len(self.src)
                        self.char = ''

                    comment = True

                else:
                    self.tok = Tokens.DIV

            elif self.char == '<':

                self.next()

                if self.char == '>':
                    self.tok = Tokens.NEQ
                    self.next()
                elif self.char == '=':
                    self.tok = Tokens.LEQ
                    self.next()
                else:
                    self.tok = Tokens.LSS

            elif self.char == '>':

                self.next()

                if self.char == '=':
                    self.tok = Tokens.GEQ
                    self.next()
                else:
                    self.tok = Tokens.GTR

            elif self.char == '&':

                self.next()

                if not self.char.isalpha():
                    self.error('Expected directive', self.cur_pos, True)

                # scan ident
                beg = self.cur_pos
                while self.next().isalnum():
                    pass
                self.lit = self.src[beg:self.cur_pos]

                tok = Directives.get(self.lit)
                if tok is not None:
                    self.tok = tok
                else:
                    self.error(f'Unknown directive: "{self.lit}"', self.cur_pos, False)  # TODO: check pos, do not raise?
                    self.tok = Tokens.DIRECTIVE

            elif self.char == '#':

                self.next()

                # skip space
                while self.char.isspace():
                    if self.char == '\n':
                        self.cur_line += 1
                    self.next()

                if not self.char.isalpha():
                    self.error('Expected preprocessor instruction', self.cur_pos, True)

                # scan ident
                beg = self.cur_pos
                while self.next().isalnum():
                    pass
                self.lit = self.src[beg:self.cur_pos]

                tok = PrepInstructions.get(self.lit)
                if tok is not None:
                    self.tok = tok
                else:
                    self.error(f'Unknown preprocessor instruction: "{self.lit}"', self.cur_pos, True)  # TODO: do not raise?

            elif self.char == '~':

                # skip space
                while self.char.isspace():
                    if self.char == '\n':
                        self.cur_line += 1
                    self.next()

                if self.char.isalnum() or self.char == '_':
                    # scan ident
                    beg = self.cur_pos
                    while self.next().isalnum() or self.char == '_':
                        pass
                    self.lit = self.src[beg:self.cur_pos]
                else:
                    self.lit = ''

                self.tok = Tokens.LABEL

            else:

                tok = tokens_map.get(self.char)
                if tok is not None:
                    self.lit = self.char
                    self.tok = tok
                    self.next()
                else:
                    raise Exception('Unknown char!')

            if not comment:
                break

        return self.tok

    def place(self: TypeParser) -> ast.Place:
        return ast.Place(self.beg_pos, self.cur_pos, self.cur_line, self.end_line)

    def marker(self: TypeParser):
        return (self.beg_pos, self.cur_line)

    def place_from(self: TypeParser, marker) -> ast.Place:
        return ast.Place(marker[0], self.end_pos, marker[1], self.end_line)

    def expect(self, tok: Union[Tokens, Keywords]):
        if self.tok != tok:
            self.error(f'expected {tok}', self.beg_pos, True)

    def error(self: TypeParser, text, pos, stop):
        if stop:
            raise Exception(text)
        else:
            print(text, pos)

    def find_item(self: TypeParser, name) -> Optional[ast.Item]:
        item = self.scope.Items.get(name)
        scope = self.scope.Outer
        while item is None and scope is not None:
            item = scope.Items.get(name)
            scope = scope.Outer
        return item

    def open_scope(self: TypeParser) -> ast.Scope:
        scope = ast.Scope(self.scope)
        self.scope = scope
        self.vars = scope.Items
        return scope

    def close_scope(self: TypeParser) -> ast.Scope:
        scope = self.scope.Outer
        assert scope is not None
        self.scope = scope
        self.vars = scope.Items
        return scope

    def parse(self: TypeParser) -> ast.Module:
        self.open_scope()
        self.scan()
        decls = self.parseModDecls()
        statements = self.parseStatements()
        auto = self.scope.Auto.copy()
        module = ast.Module(
            decls,
            auto,
            statements,
            self.interface.copy(),
            self.comments.copy()
        )
        for name in self.unknown:
            places = self.callsites[self.unknown[name]]
            for place in places:
                error = Error(
                    f'Undeclared method "{name}"',
                    place.BegLine,
                    place.BegPos
                )
                self.errors.append(error)
        self.expect(Tokens.EOF)
        return module

    def parseExpression(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        expr = self.parseAndExpr()
        while self.tok == Keywords.OR:
            operator = self.tok
            self.scan()
            expr = ast.BinaryExpr(
                expr,
                operator,
                self.parseAndExpr(),
                self.place_from(marker)
            )
        return expr

    def parseAndExpr(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        expr = self.parseNotExpr()
        while self.tok == Keywords.AND:
            operator = self.tok
            self.scan()
            expr = ast.BinaryExpr(
                expr,
                operator,
                self.parseNotExpr(),
                self.place_from(marker)
            )
        return expr

    def parseNotExpr(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        expr: ast.Expr
        if self.tok == Keywords.NOT:
            self.scan()
            expr = ast.NotExpr(
                self.parseRelExpr(),
                self.place_from(marker)
            )
        else:
            expr = self.parseRelExpr()
        return expr

    def parseRelExpr(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        expr = self.parseAddExpr()
        while self.tok in rel_operators:
            operator = self.tok
            self.scan()
            expr = ast.BinaryExpr(
                expr,
                operator,
                self.parseAddExpr(),
                self.place_from(marker)
            )
        return expr

    def parseAddExpr(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        expr = self.parseMulExpr()
        while self.tok in add_operators:
            operator = self.tok
            self.scan()
            expr = ast.BinaryExpr(
                expr,
                operator,
                self.parseMulExpr(),
                self.place_from(marker)
            )
        return expr

    def parseMulExpr(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        expr = self.parseUnaryExpr()
        while self.tok in mul_operators:
            operator = self.tok
            self.scan()
            expr = ast.BinaryExpr(
                expr,
                operator,
                self.parseUnaryExpr(),
                self.place_from(marker)
            )
        return expr

    def parseUnaryExpr(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        operator = self.tok
        expr: ast.Expr
        if self.tok in add_operators:
            self.scan()
            expr = ast.UnaryExpr(
                operator,
                self.parseOperand(),
                self.place_from(marker)
            )
        else:
            assert self.tok != Tokens.EOF
            expr = self.parseOperand()
        return expr

    def parseOperand(self: TypeParser) -> ast.Expr:
        tok = self.tok
        operand: ast.Expr
        if tok in [Tokens.STRING, Tokens.STRINGBEG]:
            operand = self.parseStringExpr()
        elif tok in basic_lit_no_string:
            operand = ast.BasicLitExpr(
                tok,
                self.val,
                self.place()
            )
            self.scan()
        elif tok == Tokens.IDENT:
            operand, _, _ = self.parseIdentExpr()
        elif tok == Tokens.LPAREN:
            operand = self.parseParenExpr()
        elif tok == Tokens.TERNARY:
            operand = self.parseTernaryExpr()
        elif tok == Keywords.NEW:
            operand = self.parseNewExpr()
        else:
            self.error('Expected operand', self.cur_pos, True)  # TODO: check pos
        return operand

    def parseStringExpr(self: TypeParser) -> ast.StringExpr:
        marker = self.marker()
        expr_list = []
        def append_this():
            expr = ast.BasicLitExpr(
                self.tok,
                self.val,
                self.place()
            )
            expr_list.append(expr)
        while True:
            if self.tok == Tokens.STRING:
                append_this()
                while self.scan() == Tokens.STRING:
                    append_this()
            elif self.tok == Tokens.STRINGBEG:
                append_this()
                while self.scan() == Tokens.STRINGMID:
                    append_this()
                if self.tok != Tokens.STRINGEND:
                    self.error('Expected "', self.cur_pos, True)  # TODO: check pos
                append_this()
                self.scan()
            else:
                break
        expr = ast.StringExpr(
            expr_list,
            self.place_from(marker)
        )
        return expr

    def parseNewExpr(self: TypeParser) -> ast.NewExpr:
        marker = self.marker()
        name: Optional[str] = None
        args: ast.Args
        if self.scan() == Tokens.IDENT:
            name = self.lit
            args = []
            self.scan()
        if self.tok == Tokens.LPAREN:
            if self.scan() != Tokens.RPAREN:
                args = self.parseArguments()
                self.expect(Tokens.RPAREN)
            self.scan()
        if name is None and args is None:
            self.error('Expected constructor', self.end_pos, True)
        expr = ast.NewExpr(
            name,
            args,
            self.place_from(marker)
        )
        return expr

    def parseIdentExpr(self: TypeParser, allow_new_var: bool = False) -> Tuple[ast.IdentExpr, Optional[ast.Item], bool]:
        marker = self.marker()
        name = self.lit
        auto_place = self.place()
        args: Optional[ast.Args] = None
        item: Optional[ast.Item]
        call: bool
        new_var: Optional[ast.Item] = None
        if self.scan() == Tokens.LPAREN:
            if self.scan() == Tokens.RPAREN:
                args = []
            else:
                args = self.parseArguments()
            self.expect(Tokens.RPAREN)
            self.scan()
            item = self.methods.get(name)
            if item is None:
                item = self.unknown.get(name)
                if item is not None:
                    places = self.callsites[item]
                    places.append(auto_place)
                else:
                    item = ast.Item(name)
                    self.unknown[name] = item
                    self.callsites[item] = [auto_place]
            call = True
            tail, call = self.parseTail(call)
        else:
            call = False
            tail, call = self.parseTail(call)
            if len(tail) > 0:
                allow_new_var = False
            item = self.find_item(name.lower())
            if item is None:
                if allow_new_var:
                    item = ast.Item(name, ast.AutoDecl(name, auto_place))
                    new_var = item
                else:
                    item = ast.Item(name)
                    # self.error(f'Undeclared identifier "{name}"', marker[1], False)
        expr = ast.IdentExpr(
            item,
            tail,
            args,
            self.place_from(marker)
        )
        return expr, new_var, call

    def parseTail(self: TypeParser, call: bool = False) -> Tuple[List[ast.TailItemExpr], bool]:
        marker = self.marker()
        expr: ast.TailItemExpr
        tail: List[ast.TailItemExpr] = []
        args: ast.Args
        while True:
            if self.tok == Tokens.PERIOD:
                self.scan()
                if not self.lit[0:1].isalpha() or Keywords.get(self.lit) is None:
                    self.expect(Tokens.IDENT)
                name = self.lit
                if self.scan() == Tokens.LPAREN:
                    if self.scan() == Tokens.RPAREN:
                        args = []
                    else:
                        args = self.parseArguments()
                    self.expect(Tokens.RPAREN)
                    self.scan()
                    call = True
                else:
                    args = None
                    call = False
                expr = ast.FieldExpr(
                    name,
                    args,
                    self.place_from(marker)
                )
                tail.append(expr)
            elif self.tok == Tokens.LBRACK:
                call = False
                if self.scan() == Tokens.RBRACK:
                    self.error('Expected expression', marker[0], True)
                index = self.parseExpression()
                self.expect(Tokens.RBRACK)
                self.scan()
                expr = ast.IndexExpr(
                    index,
                    self.place_from(marker)
                )
                tail.append(expr)
            else:
                break
        return tail, call

    def parseArguments(self: TypeParser) -> ast.Args:
        expr_list: List[Optional[ast.Expr]] = []
        while True:
            if self.tok in init_of_expr:
                expr_list.append(self.parseExpression())
            else:
                expr_list.append(None)
            if self.tok == Tokens.COMMA:
                self.scan()
            else:
                break
        return expr_list

    def parseTernaryExpr(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        self.scan()
        self.expect(Tokens.LPAREN)
        self.scan()
        cond = self.parseExpression()
        self.expect(Tokens.COMMA)
        self.scan()
        then_part = self.parseExpression()
        self.expect(Tokens.COMMA)
        self.scan()
        else_part = self.parseExpression()
        self.expect(Tokens.RPAREN)
        tail: List[ast.TailItemExpr]
        if self.scan() == Tokens.PERIOD:
            tail, _ = self.parseTail()
        else:
            tail = []
        expr = ast.TernaryExpr(
            cond,
            then_part,
            else_part,
            tail,
            self.place_from(marker)
        )
        return expr

    def parseParenExpr(self: TypeParser) -> ast.Expr:
        marker = self.marker()
        self.scan()
        expr = self.parseExpression()
        self.expect(Tokens.RPAREN)
        self.scan()
        paren_expr = ast.ParenExpr(
            expr,
            self.place_from(marker)
        )
        return paren_expr

    def parseModDecls(self) -> List[ast.Decl]:
        decls: List[ast.Decl] = []
        while isinstance(self.tok, Directives):
            self.directive = self.tok
            self.scan()
        while True:
            if self.tok == Keywords.VAR and self.allow_var:
                decls.append(self.parseVarModListDecl())
            elif self.tok == Keywords.FUNCTION:
                self.is_func = True
                decls.append(self.ParseMethodDecl())
                self.is_func = False
                self.allow_var = False
            elif self.tok == Keywords.PROCEDURE:
                decls.append(self.ParseMethodDecl())
                self.allow_var = False
            elif self.tok == PrepInstructions.REGION:
                decls.append(self.parsePrepRegionInst())
                self.scan()
            elif self.tok == PrepInstructions.ENDREGION:
                decls.append(self.parsePrepEndRegionInst())
                self.scan()
            elif self.tok == PrepInstructions.IF:
                decls.append(self.parsePrepIfInst())
                self.scan()
            elif self.tok == PrepInstructions.ELSIF:
                decls.append(self.parsePrepElsIfInst())
                self.scan()
            elif self.tok == PrepInstructions.ELSE:
                decls.append(self.parsePrepElseInst())
                self.scan()
            elif self.tok == PrepInstructions.ENDIF:
                decls.append(self.parsePrepEndIfInst())
                self.scan()
            else:
                break
            self.directive = None
            while isinstance(self.tok, Directives):
                self.directive = self.tok
                self.scan()
        return decls

    def parseVarModListDecl(self) -> ast.VarModListDecl:
        marker = self.marker()
        self.scan()
        var_list: List[ast.VarModDecl] = []
        var_list.append(self.parseVarModDecl())
        while self.tok == Tokens.COMMA:
            self.scan()
            var_list.append(self.parseVarModDecl())
        decl = ast.VarModListDecl(
            self.directive,
            var_list,
            self.place_from(marker)
        )
        self.expect(Tokens.SEMICOLON)
        self.scan()
        while self.tok == Tokens.SEMICOLON:
            self.scan()
        return decl

    def parseVarModDecl(self) -> ast.VarModDecl:
        marker = self.marker()
        self.expect(Tokens.IDENT)
        name = self.lit
        name_lower = name.lower()
        export: bool
        if self.scan() == Keywords.EXPORT:
            export = True
            self.scan()
        else:
            export = False
        decl = ast.VarModDecl(
            name,
            self.directive,
            export,
            self.place_from(marker)
        )
        if self.vars.get(name_lower) is not None:
            self.error('Identifier already declared', marker[0], True)
        item = ast.Item(name, decl)
        self.vars[name_lower] = item
        if export:
            self.interface.append(item)
        return decl

    def parseVars(self) -> List[ast.Decl]:
        decls: List[ast.Decl] = []
        while self.tok == Keywords.VAR:
            self.scan()
            decls.append(self.parseVarLocDecl())
            while self.tok == Tokens.COMMA:
                self.scan()
                decls.append(self.parseVarLocDecl())
            self.expect(Tokens.SEMICOLON)
            self.scan()
        return decls

    def parseVarLocDecl(self) -> ast.VarLocDecl:
        marker = self.marker()
        self.expect(Tokens.IDENT)
        name = self.lit
        name_lower = name.lower()
        decl = ast.VarLocDecl(
            name,
            self.place()
        )
        if self.vars.get(name_lower) is not None:
            self.error("Identifier already declared", marker[0], True)
        self.vars[name_lower] = ast.Item(name, decl)
        self.scan()
        return decl

    def ParseMethodDecl(self) -> ast.MethodDecl:
        marker = self.marker()
        export = False
        self.scan()
        self.expect(Tokens.IDENT)
        name = self.lit
        name_lower = name.lower()
        self.scan()
        self.open_scope()
        params = self.ParseParams()
        if self.tok == Keywords.EXPORT:
            export = True
            self.scan()
        sign: Union[ast.FuncSign, ast.ProcSign]
        if self.is_func:
            sign = ast.FuncSign(
                name,
                self.directive,
                params,
                export,
                self.place_from(marker)
            )
        else:
            sign = ast.ProcSign(
                name,
                self.directive,
                params,
                export,
                self.place_from(marker)
            )
        item = self.unknown.pop(name_lower, None)
        if item is not None:
            item.Decl = sign
        else:
            item = ast.Item(name, sign)
        if self.methods.get(name_lower) is not None:
            self.error('Method already declared', marker[0], True)
        self.methods[name_lower] = item
        if export:
            self.interface.append(item)
        var_list = self.parseVars()
        body = self.parseStatements()
        if self.is_func:
            self.expect(Keywords.ENDFUNCTION)
        else:
            self.expect(Keywords.ENDPROCEDURE)
        auto: List[ast.AutoDecl] = []
        for auto_decl in self.scope.Auto:
            auto.append(auto_decl)
        self.close_scope()
        self.scan()
        decl = ast.MethodDecl(
            sign,
            var_list,
            auto,
            body,
            self.place_from(marker)
        )
        return decl

    def ParseParams(self) -> List[ast.Decl]:
        self.expect(Tokens.LPAREN)
        self.scan()
        params: List[ast.Decl] = []
        if self.tok != Tokens.RPAREN:
            params.append(self.parseParamDecl())
            while self.tok == Tokens.COMMA:
                self.scan()
                params.append(self.parseParamDecl())
        self.expect(Tokens.RPAREN)
        self.scan()
        return params

    def parseParamDecl(self) -> ast.ParamDecl:
        marker = self.marker()
        by_val = False
        if self.tok == Keywords.VAL:
            by_val = True
            self.scan()
        self.expect(Tokens.IDENT)
        name = self.lit
        name_lower = name.lower()
        decl: ast.ParamDecl
        if self.scan() == Tokens.EQL:
            self.scan()
            decl = ast.ParamDecl(
                name,
                by_val,
                self.parseUnaryExpr(),
                self.place_from(marker)
            )
        else:
            decl = ast.ParamDecl(
                name,
                by_val,
                None,
                self.place_from(marker)
            )
        if self.vars.get(name_lower):
            self.error('Identifier already declared', marker[0], True)
        self.vars[name_lower] = ast.Item(name, decl)
        return decl

    def parseStatements(self) -> List[ast.Stmt]:
        statements: List[ast.Stmt] = []
        stmt = self.parseStmt()
        if stmt is not None:
            statements.append(stmt)
        while True:
            if self.tok == Tokens.SEMICOLON:
                self.scan()
            elif not isinstance(self.tok, PrepInstructions):
                break
            stmt = self.parseStmt()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def parseStmt(self) -> Optional[ast.Stmt]:
        stmt: Optional[ast.Stmt] = None
        if self.tok == Tokens.IDENT:
            stmt = self.parseAssignOrCallStmt()
        elif self.tok == Keywords.IF:
            stmt = self.parseIfStmt()
        elif self.tok == Keywords.TRY:
            stmt = self.parseTryStmt()
        elif self.tok == Keywords.WHILE:
            stmt = self.parseWhileStmt()
        elif self.tok == Keywords.FOR:
            if self.scan() == Keywords.EACH:
                stmt = self.parseForEachStmt()
            else:
                stmt = self.parseForStmt()
        elif self.tok == Keywords.RETURN:
            stmt = self.parseReturnStmt()
        elif self.tok == Keywords.BREAK:
            stmt = self.parseBreakStmt()
        elif self.tok == Keywords.CONTINUE:
            stmt = self.parseContinueStmt()
        elif self.tok == Keywords.RAISE:
            stmt = self.parseRaiseStmt()
        elif self.tok == Keywords.EXECUTE:
            stmt = self.parseExecuteStmt()
        elif self.tok == Keywords.GOTO:
            stmt = self.parseGotoStmt()
        elif self.tok == Tokens.LABEL:
            stmt = self.parseLabelStmt()
        elif self.tok == PrepInstructions.REGION:
            stmt = self.parsePrepRegionInst()
        elif self.tok == PrepInstructions.ENDREGION:
            stmt = self.parsePrepEndRegionInst()
        elif self.tok == PrepInstructions.IF:
            stmt = self.parsePrepIfInst()
        elif self.tok == PrepInstructions.ELSIF:
            stmt = self.parsePrepElsIfInst()
        elif self.tok == PrepInstructions.ELSE:
            stmt = self.parsePrepElseInst()
        elif self.tok == PrepInstructions.ENDIF:
            stmt = self.parsePrepEndIfInst()
        elif self.tok == Tokens.SEMICOLON:
            pass
        else:
            pass
        return stmt

    def parseRaiseStmt(self) -> ast.Stmt:
        marker = self.marker()
        expr = None
        if self.scan() in init_of_expr:
            expr = self.parseExpression()
        stmt = ast.RaiseStmt(
            expr,
            self.place_from(marker)
        )
        return stmt

    def parseExecuteStmt(self) -> ast.Stmt:
        marker = self.marker()
        self.scan()
        stmt = ast.ExecuteStmt(
            self.parseExpression(),
            self.place_from(marker)
        )
        return stmt

    def parseAssignOrCallStmt(self) -> Union[ast.CallStmt, ast.AssignStmt]:
        marker = self.marker()
        left, var, call = self.parseIdentExpr(True)
        stmt: Union[ast.CallStmt, ast.AssignStmt]
        if call:
            stmt = ast.CallStmt(
                left,
                self.place_from(marker)
            )
        else:
            self.expect(Tokens.EQL)
            self.scan()
            right = self.parseExpression()
            if var is not None:
                self.vars[var.Name.lower()] = var
                assert isinstance(var.Decl, ast.AutoDecl)
                self.scope.Auto.append(var.Decl)
            stmt = ast.AssignStmt(
                left,
                right,
                self.place_from(marker)
            )
        return stmt

    def parseIfStmt(self) -> ast.IfStmt:
        marker = self.marker()
        self.scan()
        cond = self.parseExpression()
        self.expect(Keywords.THEN)
        self.scan()
        then_part = self.parseStatements()
        elsif_part: Optional[List[ast.ElsIfStmt]] = None
        else_part: Optional[ast.ElseStmt] = None
        if self.tok == Keywords.ELSIF:
            elsif_part = []
            while self.tok == Keywords.ELSIF:
                elsif_part.append(self.parseElsIfStmt())
        if self.tok == Keywords.ELSE:
            else_part = self.parseElseStmt()
        self.expect(Keywords.ENDIF)
        self.scan()
        stmt = ast.IfStmt(
            cond,
            then_part,
            elsif_part,
            else_part,
            self.place_from(marker)
        )
        return stmt

    def parseElsIfStmt(self) -> ast.ElsIfStmt:
        marker = self.marker()
        self.scan()
        cond = self.parseExpression()
        self.expect(Keywords.THEN)
        self.scan()
        then = self.parseStatements()
        stmt = ast.ElsIfStmt(
            cond,
            then,
            self.place_from(marker)
        )
        return stmt

    def parseElseStmt(self) -> ast.ElseStmt:
        marker = self.marker()
        self.scan()
        stmt = ast.ElseStmt(
            self.parseStatements(),
            self.place_from(marker)
        )
        return stmt

    def parseTryStmt(self) -> ast.TryStmt:
        marker = self.marker()
        self.scan()
        try_part = self.parseStatements()
        self.expect(Keywords.EXCEPT)
        except_part = self.parseExceptStmt()
        self.expect(Keywords.ENDTRY)
        self.scan()
        stmt = ast.TryStmt(
            try_part,
            except_part,
            self.place_from(marker)
        )
        return stmt

    def parseExceptStmt(self) -> ast.ExceptStmt:
        marker = self.marker()
        self.scan()
        stmt = ast.ExceptStmt(
            self.parseStatements(),
            self.place_from(marker)
        )
        return stmt

    def parseWhileStmt(self) -> ast.WhileStmt:
        marker = self.marker()
        self.scan()
        cond = self.parseExpression()
        self.expect(Keywords.DO)
        self.scan()
        body = self.parseStatements()
        self.expect(Keywords.ENDDO)
        self.scan()
        stmt = ast.WhileStmt(
            cond,
            body,
            self.place_from(marker)
        )
        return stmt

    def parseForStmt(self) -> ast.ForStmt:
        marker = self.marker()
        self.expect(Tokens.IDENT)
        var_pos = self.beg_pos
        ident, var, call = self.parseIdentExpr()
        if call:
            self.error('Expected variable', var_pos, True)
        self.expect(Tokens.EQL)
        self.scan()
        from_expr = self.parseExpression()
        self.expect(Keywords.TO)
        self.scan()
        until = self.parseExpression()
        if var is not None:
            self.vars[var.Name.lower()] = var
            assert isinstance(var.Decl, ast.AutoDecl)
            self.scope.Auto.append(var.Decl)
        self.expect(Keywords.DO)
        self.scan()
        body = self.parseStatements()
        self.expect(Keywords.ENDDO)
        self.scan()
        stmt = ast.ForStmt(
            ident,
            from_expr,
            until,
            body,
            self.place_from(marker)
        )
        return stmt

    def parseForEachStmt(self) -> ast.ForEachStmt:
        marker = self.marker()
        self.scan()
        self.expect(Tokens.IDENT)
        var_pos = self.beg_pos
        ident, var, call = self.parseIdentExpr(True)
        if call:
            self.error('Expected variable', var_pos, True)
        self.expect(Keywords.IN)
        self.scan()
        collection = self.parseExpression()
        if var is not None:
            self.vars[var.Name.lower()] = var
            assert isinstance(var.Decl, ast.AutoDecl)
            self.scope.Auto.append(var.Decl)
        self.expect(Keywords.DO)
        self.scan()
        body = self.parseStatements()
        self.expect(Keywords.ENDDO)
        self.scan()
        stmt = ast.ForEachStmt(
            ident,
            collection,
            body,
            self.place_from(marker)
        )
        return stmt

    def parseGotoStmt(self) -> ast.GotoStmt:
        marker = self.marker()
        self.scan()
        self.expect(Tokens.LABEL)
        label = self.lit
        self.scan()
        stmt = ast.GotoStmt(
            label,
            self.place_from(marker)
        )
        return stmt

    def parseReturnStmt(self) -> ast.ReturnStmt:
        marker = self.marker()
        self.scan()
        expr = None
        if self.is_func:
            expr = self.parseExpression()
        stmt = ast.ReturnStmt(
            expr,
            self.place_from(marker)
        )
        return stmt

    def parseBreakStmt(self) -> ast.BreakStmt:
        marker = self.marker()
        self.scan()
        stmt = ast.BreakStmt(
            self.place_from(marker)
        )
        return stmt

    def parseContinueStmt(self) -> ast.ContinueStmt:
        marker = self.marker()
        self.scan()
        stmt = ast.ContinueStmt(
            self.place_from(marker)
        )
        return stmt

    def parseLabelStmt(self) -> ast.Stmt:
        marker = self.marker()
        label = self.lit
        self.scan()
        self.expect(Tokens.COLON)
        self.tok = Tokens.SEMICOLON  # cheat code
        stmt = ast.LabelStmt(
            label,
            self.place_from(marker)
        )
        return stmt

    def parsePrepExpression(self) -> ast.PrepExpr:
        marker = self.marker()
        expr = self.parsePrepAndExpr()
        while self.tok == Keywords.OR:
            operator = self.tok
            self.scan()
            expr = ast.PrepBinaryExpr(
                expr,
                operator,
                self.parsePrepAndExpr(),
                self.place_from(marker)
            )
        return expr

    def parsePrepAndExpr(self) -> ast.PrepExpr:
        marker = self.marker()
        expr = self.parsePrepNotExpr()
        while self.tok == Keywords.AND:
            operator = self.tok
            self.scan()
            expr = ast.PrepBinaryExpr(
                expr,
                operator,
                self.parsePrepNotExpr(),
                self.place_from(marker)
            )
        return expr

    def parsePrepNotExpr(self) -> ast.PrepExpr:
        marker = self.marker()
        expr: ast.PrepExpr
        if self.tok == Keywords.NOT:
            self.scan()
            expr = ast.PrepNotExpr(
                self.parsePrepOperand(),
                self.place_from(marker)
            )
        else:
            expr = self.parsePrepOperand()
        return expr

    def parsePrepOperand(self) -> ast.PrepExpr:
        if self.tok == Tokens.IDENT:
            operand = self.parsePrepSymExpr()
        elif self.tok == Tokens.LPAREN:
            operand = self.parsePrepParenExpr()
        else:
            self.error('Expected preprocessor symbol', self.cur_pos - len(self.lit), True)
        return operand

    def parsePrepSymExpr(self) -> ast.PrepExpr:
        marker = self.marker()
        symbol_exist = (PrepSymbols.get(self.lit) is not None)
        symbol = ast.PrepSymExpr(
            self.lit,
            symbol_exist,
            self.place_from(marker)
        )
        self.scan()
        return symbol

    def parsePrepParenExpr(self) -> ast.PrepExpr:
        marker = self.marker()
        self.scan()
        expr = self.parsePrepExpression()
        self.expect(Tokens.RPAREN)
        self.scan()
        paren_expr = ast.PrepParenExpr(
            expr,
            self.place_from(marker)
        )
        return paren_expr

    def parsePrepIfInst(self) -> ast.PrepInst:
        marker = self.marker()
        self.scan()
        cond = self.parsePrepExpression()
        self.expect(Keywords.THEN)
        self.tok = Tokens.SEMICOLON  # cheat code
        inst = ast.PrepIfInst(
            cond,
            self.place_from(marker)
        )
        return inst

    def parsePrepElsIfInst(self) -> ast.PrepInst:
        marker = self.marker()
        self.scan()
        cond = self.parsePrepExpression()
        self.expect(Keywords.THEN)
        self.tok = Tokens.SEMICOLON  # cheat code
        inst = ast.PrepElsIfInst(
             cond,
             self.place_from(marker)
         )
        return inst

    def parsePrepElseInst(self) -> ast.PrepInst:
        marker = self.marker()
        self.tok = Tokens.SEMICOLON  # cheat code
        self.end_line = self.cur_line  # cheat code
        inst = ast.PrepElseInst(
            self.place_from(marker)
        )
        return inst

    def parsePrepEndIfInst(self) -> ast.PrepInst:
        marker = self.marker()
        self.tok = Tokens.SEMICOLON  # cheat code
        self.end_line = self.cur_line  # cheat code
        inst = ast.PrepEndIfInst(
            self.place_from(marker)
        )
        return inst

    def parsePrepRegionInst(self) -> ast.PrepInst:
        marker = self.marker()
        self.scan()
        self.expect(Tokens.IDENT)
        name = self.lit
        self.tok = Tokens.SEMICOLON
        inst = ast.PrepRegionInst(
            name,
            self.place_from(marker)
        )
        return inst

    def parsePrepEndRegionInst(self) -> ast.PrepInst:
        marker = self.marker()
        self.tok = Tokens.SEMICOLON  # cheat code
        self.end_line = self.cur_line  # cheat code
        inst = ast.PrepEndRegionInst(
            self.place_from(marker)
        )
        return inst