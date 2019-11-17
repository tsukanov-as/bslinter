# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import Union, List, Dict, Optional
from decimal import Decimal
from bsl.enums import Tokens, Keywords, Directives, PrepInstructions, PrepSymbols
from bsl.visitor import Visitor
from abc import abstractmethod
from collections import namedtuple

class Scope:

    def __init__(self, outer: Optional['Scope'] = None):
        self.Outer: Optional['Scope'] = outer
        self.Vars: Dict[str, Item] = {}
        self.Auto: List[AutoDecl] = []
        self.Methods: Dict[str, Item] = {}

class Item:
    """
    Узел хранит информацию об объекте области видимости.
    Поле Decl хранит объявление данного объекта (None = объявление не обнаружено).
    """
    def __init__(self, name, decl=None):
        self.Name: str = name
        self.Decl: Optional[Decl] = decl


class Place:

    def __init__(self, begpos, endpos, begline, endline, begcolumn, endcolumn):
        self.BegPos: int = begpos
        self.EndPos: int = endpos
        self.BegLine: int = begline
        self.EndLine: int = endline
        self.BegColumn: int = begcolumn
        self.EndColumn: int = endcolumn

class Comment:

    def __init__(self, text, pos, line, column):
        self.text = text
        self.pos = pos
        self.line = line
        self.column = column

class Node:

    @abstractmethod
    def visit(self, vesitor: Visitor):
        pass


class Module(Node):
    """
    Корень AST. Узел хранит информацию о модуле в целом.
    """
    def __init__(self, decls, auto, statements, interface, comments):
        self.Decls: List[Decl] = decls
        self.Auto: List[AutoDecl] = auto
        self.Body: List[Stmt] = statements
        self.Interface: List[Item] = interface
        self.Comments: Dict[int, Comment] = comments

    def visit(self, visitor: Visitor):
        visitor.visit_Module(self)
        for decl in self.Decls:
            decl.visit(visitor)
        for auto in self.Auto:
            auto.visit(visitor)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.leave_Module(self)

Env = namedtuple('Env', [
        'Client',
        'ExternalConnection',
        'MobileApplication',
        'MobileClient',
        'MobileServer',
        'Server',
        'ThickClient',
        'ThinClient',
        'WebClient',
        'Integration',
    ],
    defaults=(False,False,False,False,False,False,False,False,False,False)
)

#region Declarations


class Decl(Node):
    Place: Place

class GlobalObject(Decl):
    """
    Хранит информацию об объекте глобального контекста
    """
    def __init__(self, name, env, attribs=None, methods=None):
        self.Name: str = name
        self.Env: Env = env
        self.Attribs: Optional[List[str]] = attribs
        self.Methods: Optional[List[GlobalMethod]] = methods
        self.Place: Place = Place(0, 0, 0, 0, 0, 0)

    def visit(self, visitor: Visitor):
        pass # не посещается

class GlobalMethodParameter(Decl):
    """
    Хранит информацию о параметре метода глобального контекста
    """
    def __init__(self, name, required):
        self.Name: str = name
        self.Required: bool = required
        self.Place: Place = Place(0, 0, 0, 0, 0, 0)

    def visit(self, visitor: Visitor):
        pass # не посещается

class GlobalMethod(Decl):
    """
    Хранит информацию о методе глобального контекста
    """
    def __init__(self, name, retval, params, env):
        self.Name: str = name
        self.Env: Env = env
        self.Params: List[GlobalMethodParameter] = params
        self.RetVal: bool = retval
        self.Place: Place = Place(0, 0, 0, 0, 0, 0)

    def visit(self, visitor: Visitor):
        pass # не посещается

class VarModListDecl(Decl):
    """
    Хранит информацию об инструкции объявления переменных уровня модуля.
    Пример:
    <pre>
    &НаКлиенте            // поле "Directive"
    Перем П1 Экспорт, П2; // поле "List"
    </pre>
    """
    def __init__(self, directive, varlist, place):
        self.Directive: Optional[Directives] = directive
        self.List: List[VarModDecl] = varlist
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_VarModListDecl(self)
        for decl in self.List:
            decl.visit(visitor)
        visitor.leave_VarModListDecl(self)


class VarModDecl(Decl):
    """
    Хранит информацию об объявлении переменной уровня модуля.
    Пример:
    Объявления переменных заключены в скобки <...>
    <pre>
    &НаКлиенте
    Перем <П1 Экспорт>, <П2>;
    </pre>
    """
    def __init__(self, name, directive, export, place):
        self.Name: str = name
        self.Directive: Optional[Directives] = directive
        self.Export: bool = export
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_VarModDecl(self)


class VarLocDecl(Decl):
    """
    Хранит информацию об объявлении локальной переменной.
    Пример:
    Объявления переменных заключены в скобки <...>
    <pre>
    Перем <П1>, <П2>;
    </pre>
    """
    def __init__(self, name, place):
        self.Name: str = name
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_VarLocDecl(self)


class AutoDecl(Decl):
    """
    Хранит информацию об объявлении авто-переменной.
    Пример:
    Объявления переменных заключены в скобки <...>
    <pre>
    <Макс> = 0;
    Для <Индекс> = 0 По Массив.ВГраница() Цикл
        <Структура> = Массив[Индекс];
        Для Каждого <Элемент> Из Структура Цикл
            Если Макс < Элемент.Значение Тогда
                Макс = Элемент.Значение;
            КонецЕсли;
        КонецЦикла;
    КонецЦикла
    """
    def __init__(self, name, place):
        self.Name: str = name
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_AutoDecl(self)


class ParamDecl(Decl):
    """
    Хранит информацию об объявлении параметра.
    Пример:
    Объявления параметров заключены в скобки <...>
    <pre>
    Процедура(<П1>, <Знач П2 = Неопределено>)
    </pre>
    """
    def __init__(self, name, byval, value, place):
        self.Name: str = name
        self.ByVal: bool = byval
        self.Value: Union[UnaryExpr, BasicLitExpr, None] = value
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_ParamDecl(self)
        if self.Value is not None:
            visitor.visit_Expr(self.Value)
            self.Value.visit(visitor)
            visitor.leave_Expr(self.Value)
        visitor.leave_ParamDecl(self)


class MethodDecl(Decl):
    """
    Хранит информацию об объявлении метода.
    Сигнатура метода хранится в поле Sign.
    Пример:
    <pre>
    &НаКлиенте
    Функция Тест() Экспорт
        Перем П1;    // поле "Vars" хранит объявления переменных.
        П1 = 2;      // операторы собираются в поле Body
        П2 = П1 + 2; // Авто-переменные (П2) собираются в поле "Auto".
    КонецФункции
    </pre>
    """
    def __init__(self, sign, decls, auto, body, place):
        self.Sign: Union[ProcSign, FuncSign] = sign
        self.Vars: List[VarLocDecl] = decls
        self.Auto: List[AutoDecl] = auto
        self.Body: List[Stmt] = body
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_MethodDecl(self)
        self.Sign.visit(visitor)
        for decl in self.Vars:
            decl.visit(visitor)
        for auto in self.Auto:
            auto.visit(visitor)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.leave_MethodDecl(self)


class ProcSign(Decl):
    """
    Хранит информацию о сигнатуре объявления процедуры.
    Пример:
    <pre>
    &НаКлиенте
    Процедура Тест(П1, П2) Экспорт
    </pre>
    """
    def __init__(self, name, directive, params, export, place):
        self.Name: str = name
        self.Directive: Directives = directive
        self.Params: List[ParamDecl] = params
        self.Export: bool = export
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_ProcSign(self)
        for decl in self.Params:
            decl.visit(visitor)
        visitor.leave_ProcSign(self)

class FuncSign(Decl):
    """
    Хранит информацию о сигнатуре объявления функции.
    Пример:
    <pre>
    &НаКлиенте
    Функция Тест(П1, П2) Экспорт
    </pre>
    """
    def __init__(self, name, directive, params, export, place):
        self.Name: str = name
        self.Directive: Directives = directive
        self.Params: List[ParamDecl] = params
        self.Export: bool = export
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_FuncSign(self)
        for decl in self.Params:
            decl.visit(visitor)
        visitor.leave_FuncSign(self)

#endregion Declarations


#region Expressions


class Expr(Node):
    Place: Place


# Общий тип для аргументов.
# Элементы списка опциональные,
# т.к. аргумент может быть не указан.
Args = List[Optional[Expr]]


class BasicLitExpr(Expr):
    """
    Хранит информацию о литерале примитивного типа.
    """
    def __init__(self, kind, value, place):
        self.Kind: Tokens = kind
        self.Value: Union[str, bool, Decimal, None] = value  # TODO: date, null
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_BasicLitExpr(self)


class TailItemExpr(Expr):
    """
    Базовый класс для элементов хвоста.
    Подклассы: FieldExpr и IndexExpr
    """


class FieldExpr(TailItemExpr):
    """
    Хранит информацию об обращении к полю объекта через точку.
    В поле Name содержится имя поля.
    В поле Args содержатся аргументы вызова (если это вызов).
    Пример:
    <pre>
    // обращения через точку заключены в скобки <...>
    Значение = Объект<.Поле>
    Значение = Объект<.Добавить(П1, П2)>
    </pre>
    """
    def __init__(self, name, args, place):
        self.Name: str = name
        self.Args: Optional[Args] = args
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_FieldExpr(self)
        if self.Args is not None:
            for expr in self.Args:
                if expr is not None:
                    expr.visit(visitor)
        visitor.leave_FieldExpr(self)

class IndexExpr(TailItemExpr):
    """
    Хранит информацию об обращении к элементу объекта по индексу.
    Пример:
    <pre>
    // обращение по индексу заключено в скобки <...>
    Значение = Объект<[Ключ]>
    </pre>
    """
    def __init__(self, expr, place):
        self.Expr: Expr = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_IndexExpr(self)
        self.Expr.visit(visitor)
        visitor.leave_IndexExpr(self)

class IdentExpr(Expr):
    """
    Хранит информацию об обращении к идентификатору.
    В поле Head содержится объект области видимости соответствующий идентификатору.
    В поле Tail содержится последовательность обращений через точку и по индексу.
    В поле Args содержатся аргументы вызова (если это вызов).
    Пример:
    <pre>
    // идентификатор заключен в скобки <...>
    // поле "Head" будет содержать объект переменной "Запрос";
    // поле "Tail" будет содержать три обращения;
    // поле "Args" будет равно Неопределено, т.к. обращение к "Запрос" не является вызовом.
    Возврат <Запрос.Выполнить().Выгрузить()[0]>;
    </pre>
    """
    def __init__(self, item, tail, args, place):
        self.Head: Item = item
        self.Args: Optional[Args] = args
        self.Tail: List[Union[FieldExpr, IndexExpr]] = tail
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_IdentExpr(self)
        if self.Args is not None:
            for expr in self.Args:
                if expr is not None:
                    expr.visit(visitor)
        for item in self.Tail:
            item.visit(visitor)
        visitor.leave_IdentExpr(self)


class UnaryExpr(Expr):
    """
    Хранит унарное выражение.
    Пример:
    <pre>
    // унарные выражения заключены в скобки <...>
    // поле "Operator" равно либо Tokens.Add, либо Tokens.Sub
    // поле "Operand" хранит операнд-выражение
    Значение = <-Сумма> * 2;
    Значение = <+Сумма>;
    Значение = <-(Сумма1 + Сумма2)> / 2;
    </pre>
    """
    def __init__(self, operator, operand, place):
        self.Operator: Tokens = operator
        self.Operand: Expr = operand
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_UnaryExpr(self)
        self.Operand.visit(visitor)
        visitor.leave_UnaryExpr(self)

class BinaryExpr(Expr):
    """
    Хранит бинарное выражение.
    Пример:
    <pre>
    // бинарные выражения заключены в скобки <...>
    // поле "Operator" равно одному из допустимых операторов:
    // - логических (кроме "Не")
    // - реляционных
    // - арифметических
    // поля "Left" и "Right" содержат операнды-выражения
    Если <Не Отмена И Продолжить> Тогда
        Значение = <Сумма1 + <Сумма2 * Коэффициент>>;
    КонецЕсли;
    </pre>
    """
    def __init__(self, left, operator, right, place):
        self.Left: Expr = left
        self.Operator: Tokens = operator
        self.Right: Expr = right
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_BinaryExpr(self)
        self.Left.visit(visitor)
        self.Right.visit(visitor)
        visitor.leave_BinaryExpr(self)

class NewExpr(Expr):
    """
    Хранит выражение "Новый".
    Пример:
    <pre>
    // выражения "Новый" заключены в скобки <...>
    // в этом варианте поле "Name" хранит имя типа "Массив",
    // а поле "Args" хранит массив из одного выражения
    Параметры = <Новый Массив(1)>;
    Параметры[0] = 10;
    // в этом варианте поле "Name" равно Неопределено,
    // а поле "Args" хранит массив из двух выражений
    Массив = <Новый (Тип("Массив"), Параметры)>;
    </pre>
    """
    def __init__(self, name, args, place):
        self.Name: Optional[str] = name
        self.Args: Args = args
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_NewExpr(self)
        for expr in self.Args:
            if expr is not None:
                expr.visit(visitor)
        visitor.leave_NewExpr(self)

class TernaryExpr(Expr):
    """
    Хранит тернарное выражение "?(,,)".
    Пример:
    <pre>
    Значение = ?(Ложь,   // поле "Cond"
        Неопределено,    // поле "Then"
        Новый Массив     // поле "Else"
    ).Количество();      // поле "Tail"
    </pre>
    """
    def __init__(self, cond, thenpart, elsepart, tail, place):
        self.Cond: Expr = cond
        self.Then: Expr = thenpart
        self.Else: Expr = elsepart
        self.Tail: List[FieldExpr, IndexExpr] = tail
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_TernaryExpr(self)
        self.Cond.visit(visitor)
        self.Then.visit(visitor)
        self.Else.visit(visitor)
        for item in self.Tail:
            item.visit(visitor)
        visitor.leave_TernaryExpr(self)

class ParenExpr(Expr):
    """
    Хранит скобочное выражение.
    Пример:
    <pre>
    // скобочное выражение заключено в скобки <...>
    Сумма = <(Сумма1 + Сумма2)> * Количество;
    </pre>
    """
    def __init__(self, expr, place):
        self.Expr: Expr = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_ParenExpr(self)
        self.Expr.visit(visitor)
        visitor.leave_ParenExpr(self)


class NotExpr(Expr):
    """
    Хранит выражение, к которому применено логическое отрицание "Не".
    Пример:
    <pre>
    // выражение-отрицание заключено в скобки <...>
    НеРавны = <Не Сумма1 = Сумма2>;
    </pre>
    """
    def __init__(self, expr, place):
        self.Expr: Expr = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_NotExpr(self)
        self.Expr.visit(visitor)
        visitor.leave_NotExpr(self)


class StringExpr(Expr):
    """
    Хранит строковое выражение.
    Поле "List" хранит упорядоченный список частей строки.
    Пример:
    <pre>
    Строка1 = "Часть1" "Часть2"; // эта строка состоит из двух частей типа Nodes.String
    Строка2 =                    // эта строка состоит из пяти частей типа:
    "Начало строки               // Nodes.StringBeg
    | продолжение строки         // Nodes.StringMid
    | еще продолжение строки     // Nodes.StringMid
    | окончание строки"          // Nodes.StringEnd
    "еще часть";                 // Nodes.String
    </pre>
    """
    def __init__(self, exprlist, place):
        self.List: List[BasicLitExpr] = exprlist
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_StringExpr(self)
        for expr in self.List:
            expr.visit(visitor)
        visitor.leave_StringExpr(self)


#endregion Expressions


#region Statements


class Stmt(Node):
    Place: Place


class AssignStmt(Stmt):
    """
    Хранит оператор присваивания.
    """
    def __init__(self, left, right, place):
        self.Left: IdentExpr = left
        self.Right: Expr = right
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_AssignStmt(self)

        visitor.visit_Expr(self.Left)
        self.Left.visit(visitor)
        visitor.leave_Expr(self.Left)

        visitor.visit_Expr(self.Right)
        self.Right.visit(visitor)
        visitor.leave_Expr(self.Right)

        visitor.leave_AssignStmt(self)


class ReturnStmt(Stmt):
    """
    Хранит оператор "Возврат".
    Поле "Expr" равно Неопределено если это возврат из процедуры.
    """
    def __init__(self, expr, place):
        self.Expr: Optional[Expr] = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_ReturnStmt(self)

        if self.Expr is not None:
            visitor.visit_Expr(self.Expr)
            self.Expr.visit(visitor)
            visitor.leave_Expr(self.Expr)

        visitor.leave_ReturnStmt(self)


class BreakStmt(Stmt):
    """
    Хранит оператор "Прервать".
    """
    def __init__(self, place):
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_BreakStmt(self)


class ContinueStmt(Stmt):
    """
    Хранит оператор "Продолжить".
    """
    def __init__(self, place):
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_ContinueStmt(self)


class RaiseStmt(Stmt):
    """
    Хранит оператор "ВызватьИсключение".
    Поле "Expr" равно Неопределено если это вариант оператора без выражения.
    """
    def __init__(self, expr, place):
        self.Expr: Optional[Expr] = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_RaiseStmt(self)

        if self.Expr is not None:
            visitor.visit_Expr(self.Expr)
            self.Expr.visit(visitor)
            visitor.leave_Expr(self.Expr)

        visitor.leave_RaiseStmt(self)


class ExecuteStmt(Stmt):
    """
    Хранит оператор "Выполнить".
    """
    def __init__(self, expr, place):
        self.Expr: Expr = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_ExecuteStmt(self)

        visitor.visit_Expr(self.Expr)
        self.Expr.visit(visitor)
        visitor.leave_Expr(self.Expr)

        visitor.leave_ExecuteStmt(self)


class CallStmt(Stmt):
    """
    Хранит вызов процедуры или функции как процедуры.
    """
    def __init__(self, identexpr, place):
        self.Ident: IdentExpr = identexpr
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_CallStmt(self)

        visitor.visit_Expr(self.Ident)
        self.Ident.visit(visitor)
        visitor.leave_Expr(self.Ident)

        visitor.leave_CallStmt(self)


class IfStmt(Stmt):
    """
    Хранит оператор "Если".
    Пример:
    <pre>
    Если Сумма > 0 Тогда // поле "Cond" хранит условие (выражение)
        // поле "Then" хранит операторы в этом блоке
    ИначеЕсли Сумма = 0 Тогда
        // поле-массив "ElsIf" хранит последовательность блоков ИначеЕсли
    Иначе
        // поле "Else" хранит операторы в этом блоке
    КонецЕсли
    </pre>
    Поля "ElsIf" и "Else" равны Неопределено если
    соответствующие блоки отсутствуют в исходном коде.
    """
    def __init__(self, cond, thenpart, elsifpart, elsepart, place):
        self.Cond: Expr = cond
        self.Then: List[Stmt] = thenpart
        self.ElsIf: Optional[List[ElsIfStmt]] = elsifpart
        self.Else: Optional[ElseStmt] = elsepart
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_IfStmt(self)

        visitor.visit_Expr(self.Cond)
        self.Cond.visit(visitor)
        visitor.leave_Expr(self.Cond)

        for stmt in self.Then:
            stmt.visit(visitor)

        if self.ElsIf is not None:
            for stmt in self.ElsIf:
                stmt.visit(visitor)

        if self.Else is not None:
            self.Else.visit(visitor)

        visitor.leave_IfStmt(self)


class ElseStmt(Stmt):
    """
    Хранит блок "Иначе"
    """
    def __init__(self, body, place):
        self.Body: List[Stmt] = body
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_ElseStmt(self)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.leave_ElseStmt(self)


class ElsIfStmt(Stmt):
    """
    Хранит блок "ИначеЕсли" оператора "Если".
    Пример:
    <pre>
    ...
    ИначеЕсли Сумма < 0 Тогда // поле "Cond" хранит условие (выражение)
        // поле "Then" хранит операторы в этом блоке
    ...
    </pre>
    """
    def __init__(self, cond, then, place):
        self.Cond: Expr = cond
        self.Then: List[Stmt] = then
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_ElsIfStmt(self)

        visitor.visit_Expr(self.Cond)
        self.Cond.visit(visitor)
        visitor.leave_Expr(self.Cond)

        for stmt in self.Then:
            stmt.visit(visitor)

        visitor.leave_ElsIfStmt(self)


class WhileStmt(Stmt):
    """
    Хранит оператор цикла "Пока".
    Пример:
    <pre>
    Пока Индекс > 0 Цикл // поле "Cond" хранит условие (выражение)
        // поле "Body" хранит операторы в этом блоке
    КонецЦикла
    </pre>
    """
    def __init__(self, cond, body, place):
        self.Cond: Expr = cond
        self.Body: List[Stmt] = body
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_WhileStmt(self)

        visitor.visit_Expr(self.Cond)
        self.Cond.visit(visitor)
        visitor.leave_Expr(self.Cond)

        for stmt in self.Body:
            stmt.visit(visitor)

        visitor.leave_WhileStmt(self)


class ForStmt(Stmt):
    """
    Хранит оператор цикла "Для".
    Пример:
    <pre>
    Для Индекс = 0    // поля "Ident" и "From" хранят переменную и выражение инициализации.
    По Длина - 1 Цикл // поле "To" хранит выражение границы
        // поле "Body" хранит операторы в этом блоке
    КонецЦикла
    </pre>
    """
    def __init__(self, ident, fromexpr, toexpr, body, place):
        self.Ident: IdentExpr = ident
        self.From: Expr = fromexpr
        self.To: Expr = toexpr
        self.Body: List[Stmt] = body
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_ForStmt(self)

        visitor.visit_Expr(self.Ident)
        self.Ident.visit(visitor)
        visitor.leave_Expr(self.Ident)

        visitor.visit_Expr(self.From)
        self.From.visit(visitor)
        visitor.leave_Expr(self.From)

        visitor.visit_Expr(self.To)
        self.To.visit(visitor)
        visitor.leave_Expr(self.To)

        for stmt in self.Body:
            stmt.visit(visitor)

        visitor.leave_ForStmt(self)


class ForEachStmt(Stmt):
    """
    Хранит оператор цикла "Для Каждого".
    Пример:
    <pre>
    Для Каждого Элемент // поле "Ident" хранит переменную.
    Из Список Цикл    // поле "In" хранит выражение коллекции.
        // поле "Body" хранит операторы в этом блоке
    КонецЦикла
    </pre>
    """
    def __init__(self, identexpr, collection, body, place):
        self.Ident: IdentExpr = identexpr
        self.In: Expr = collection
        self.Body: List[Stmt] = body
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_ForEachStmt(self)

        visitor.visit_Expr(self.Ident)
        self.Ident.visit(visitor)
        visitor.leave_Expr(self.Ident)

        visitor.visit_Expr(self.In)
        self.In.visit(visitor)
        visitor.leave_Expr(self.In)

        for stmt in self.Body:
            stmt.visit(visitor)

        visitor.leave_ForEachStmt(self)


class TryStmt(Stmt):
    """
    Хранит оператор "Попытка"
    Пример:
    <pre>
    Попытка
        // поле "Try" хранит операторы в этом блоке.
    Исключение
        // поле "Except" хранит операторы в этом блоке
    КонецПопытки
    </pre>
    """
    def __init__(self, trypart, exceptpart, place):
        self.Try: List[Stmt] = trypart
        self.Except: ExceptStmt = exceptpart
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_TryStmt(self)
        for stmt in self.Try:
            stmt.visit(visitor)
        self.Except.visit(visitor)
        visitor.leave_TryStmt(self)


class ExceptStmt(Stmt):
    """
    Хранит блок "Исключение".
    """
    def __init__(self, body, place):
        self.Body: List[Stmt] = body
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_ExceptStmt(self)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.leave_ExceptStmt(self)


class GotoStmt(Stmt):
    """
    Хранит оператор "Перейти".
    """
    def __init__(self, label, place):
        self.Label: str = label
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_GotoStmt(self)


class LabelStmt(Stmt):
    """
    Хранит оператор метки.
    """
    def __init__(self, label, place):
        self.Label: str = label
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_LabelStmt(self)


#endregion Statements


#region PrepInst


class PrepInst(Decl, Stmt):
    Place: Place


class PrepIfInst(PrepInst):
    """
    Хранит информацию об инструкции препроцессора #Если,
    Пример:
    <pre>
    ...
    #Если Сервер Тогда // поле "Cond" хранит условие (выражение)
    ...
    </pre>
    """
    def __init__(self, cond, place):
        self.Cond: PrepExpr = cond
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_PrepIfInst(self)

        visitor.visit_PrepExpr(self.Cond)
        self.Cond.visit(visitor)
        visitor.leave_PrepExpr(self.Cond)

        visitor.leave_PrepIfInst(self)


class PrepElsIfInst(PrepInst):
    """
    Хранит информацию об инструкции препроцессора #ИначеЕсли
    Пример:
    <pre>
    ...
    #ИначеЕсли Клиент Тогда // поле "Cond" хранит условие (выражение)
    ...
    </pre>
    """
    def __init__(self, cond, place):
        self.Cond: PrepExpr = cond
        self.Place: Place = place

    def visit(self, visitor: Visitor):

        visitor.visit_PrepElsIfInst(self)

        visitor.visit_PrepExpr(self.Cond)
        self.Cond.visit(visitor)
        visitor.leave_PrepExpr(self.Cond)

        visitor.leave_PrepElsIfInst(self)


class PrepElseInst(PrepInst):
    """
    Хранит информацию об инструкции препроцессора #Иначе
    """
    def __init__(self, place):
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_PrepElseInst(self)


class PrepEndIfInst(PrepInst):
    """
    Хранит информацию об инструкции препроцессора #КонецЕсли
    """
    def __init__(self, place):
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_PrepEndIfInst(self)


class PrepRegionInst(PrepInst):
    """
    Хранит информацию об инструкции препроцессора #Обрасть,
    Пример:
    <pre>
    ...
    #Область Интерфейс   // поле "Name" хранит имя области
    ...
    </pre>
    """
    def __init__(self, name, place):
        self.Name: str = name
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_PrepRegionInst(self)


class PrepEndRegionInst(PrepInst):
    """
    Хранит информацию об инструкции препроцессора #КонецОбласти,
    Пример:
    <pre>
    ...
    #КонецОбласти
    ...
    </pre>
    """
    def __init__(self, place):
        self.Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_PrepEndRegionInst(self)

#endregion PrepInst


#region PrepExpr


class PrepExpr(Node):
    Place: Place


class PrepBinaryExpr(PrepExpr):
    """
    Хранит бинарное выражение препроцессора.
    Пример:
    <pre>
    // бинарные выражения заключены в скобки <...>
    // поле "Operator" равно либо Tokens.Or либо Tokens.And:
    // поля "Left" и "Right" содержат операнды-выражения препроцессора
    #Если <Сервер Или ВнешнееСоединение> Тогда
    ...
    </pre>
    """
    def __init__(self, left, operator, right, place):
        self.Left: PrepExpr = left
        self.Operator: Tokens = operator
        self.Right: PrepExpr = right
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_PrepBinaryExpr(self)
        self.Left.visit(visitor)
        self.Right.visit(visitor)
        visitor.leave_PrepBinaryExpr(self)


class PrepNotExpr(PrepExpr):
    """
    Хранит выражение препроцессора, к которому применено логическое отрицание "Не".
    Пример:
    <pre>
    // выражение-отрицание заключено в скобки <...>
    #Если <Не ВебКлиент> Тогда
    ...
    </pre>
    """
    def __init__(self, expr, place):
        self.Expr: PrepExpr = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_PrepNotExpr(self)
        self.Expr.visit(visitor)
        visitor.leave_PrepNotExpr(self)


class PrepSymExpr(PrepExpr):
    """
    Узел хранит информацию о символе препроцессора.
    Поле Exist = True если такой символ существует.
    Пример:
    <pre>
    // символ заключен в скобки <...>
    #Если <Сервер> Тогда
    </pre>
    """
    def __init__(self, symbol, exist, place):
        self.Symbol: str = symbol
        self.Exist: bool = exist
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_PrepSymExpr(self)


class PrepParenExpr(PrepExpr):
    """
    Хранит скобочное выражение препроцессора.
    Пример:
    <pre>
    // скобочное выражение заключено в скобки <...>
    #Если <(Сервер Или ВнешнееСоединение)> Тогда
    </pre>
    """
    def __init__(self, expr, place):
        self.Expr: PrepExpr = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.visit_PrepParenExpr(self)
        self.Expr.visit(visitor)
        visitor.leave_PrepParenExpr(self)


#endregion PrepExpr