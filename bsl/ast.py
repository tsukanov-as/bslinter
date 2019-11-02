# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import Union, List, Dict, Optional
from decimal import Decimal
from bsl.enums import Tokens, Keywords, Directives, PrepInstructions, PrepSymbols
from bsl.visitor import Visitor, Plugin
from abc import abstractmethod

class Scope:

    def __init__(self, outer: Optional['Scope'] = None):
        self.Outer: Optional['Scope'] = outer
        self.Items: Dict[str, Item] = {}
        self.Auto: List[AutoDecl] = []


class Item:
    """
    Узел хранит информацию об объекте области видимости.
    Поле Decl хранит объявление данного объекта (None = объявление не обнаружено).
    """
    def __init__(self, name, decl=None):
        self.Name: str = name
        self.Decl: Optional[Decl] = decl


class Place:

    def __init__(self, begpos, endpos, begline, endline):
        self.BegPos: int = begpos
        self.EndPos: int = endpos
        self.BegLine: int = begline
        self.EndLine: int = endline


class Node:

    Place: Place

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
        self.Comments: Dict[int, str] = comments

    def visit(self, visitor: Visitor):
        visitor.beforeVisitModule(self)
        for decl in self.Decls:
            decl.visit(visitor)
        for auto in self.Auto:
            auto.visit(visitor)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.afterVisitModule(self)


#region Declarations


class Decl(Node):
    pass


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
        visitor.beforeVisitVarModListDecl(self)
        for decl in self.List:
            decl.visit(visitor)
        visitor.afterVisitVarModListDecl(self)


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
        visitor.beforeVisitVarModDecl(self)
        # visitor.afterVisitVarModDecl(self)


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
        visitor.beforeVisitVarLocDecl(self)
        # visitor.afterVisitVarLocDecl(self)


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
        visitor.beforeVisitAutoDecl(self)
        # visitor.afterVisitAutoDecl(self)


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
        visitor.beforeVisitParamDecl(self)
        if self.Value is not None:
            self.Value.visit(visitor)
        visitor.afterVisitParamDecl(self)


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
        visitor.beforeVisitMethodDecl(self)
        self.Sign.visit(visitor)
        for decl in self.Vars:
            decl.visit(visitor)
        for auto in self.Auto:
            auto.visit(visitor)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.afterVisitMethodDecl(self)


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
        visitor.beforeVisitProcSign(self)
        for decl in self.Params:
            decl.visit(visitor)
        visitor.afterVisitProcSign(self)

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
        visitor.beforeVisitFuncSign(self)
        for decl in self.Params:
            decl.visit(visitor)
        visitor.afterVisitFuncSign(self)

#endregion Declarations


#region Expressions


class Expr(Node):
    pass


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
        visitor.beforeVisitBasicLitExpr(self)
        # visitor.afterVisitBasicLitExpr(self)


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
        visitor.beforeVisitFieldExpr(self)
        if self.Args is not None:
            for expr in self.Args:
                if expr is not None:
                    expr.visit(visitor)
        visitor.afterVisitFieldExpr(self)

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
        visitor.beforeVisitIndexExpr(self)
        self.Expr.visit(visitor)
        visitor.afterVisitIndexExpr(self)

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
        visitor.beforeVisitIdentExpr(self)
        if self.Args is not None:
            for expr in self.Args:
                if expr is not None:
                    expr.visit(visitor)
        for item in self.Tail:
            item.visit(visitor)
        visitor.afterVisitIdentExpr(self)


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
        visitor.beforeVisitUnaryExpr(self)
        self.Operand.visit(visitor)
        visitor.afterVisitUnaryExpr(self)

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
        visitor.beforeVisitBinaryExpr(self)
        self.Left.visit(visitor)
        self.Right.visit(visitor)
        visitor.afterVisitBinaryExpr(self)

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
        visitor.beforeVisitNewExpr(self)
        for expr in self.Args:
            if expr is not None:
                expr.visit(visitor)
        visitor.afterVisitNewExpr(self)

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
        visitor.beforeVisitTernaryExpr(self)
        self.Cond.visit(visitor)
        self.Then.visit(visitor)
        self.Else.visit(visitor)
        for item in self.Tail:
            item.visit(visitor)
        visitor.afterVisitTernaryExpr(self)

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
        visitor.beforeVisitParenExpr(self)
        self.Expr.visit(visitor)
        visitor.afterVisitParenExpr(self)


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
        visitor.beforeVisitNotExpr(self)
        self.Expr.visit(visitor)
        visitor.afterVisitNotExpr(self)


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
        visitor.beforeVisitStringExpr(self)
        for expr in self.List:
            expr.visit(visitor)
        visitor.afterVisitStringExpr(self)


#endregion Expressions


#region Statements


class Stmt(Node):
    pass


class AssignStmt(Stmt):
    """
    Хранит оператор присваивания.
    """
    def __init__(self, left, right, place):
        self.Left: IdentExpr = left
        self.Right: Expr = right
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitAssignStmt(self)
        self.Left.visit(visitor)
        self.Right.visit(visitor)
        visitor.afterVisitAssignStmt(self)


class ReturnStmt(Stmt):
    """
    Хранит оператор "Возврат".
    Поле "Expr" равно Неопределено если это возврат из процедуры.
    """
    def __init__(self, expr, place):
        self.Expr: Optional[Expr] = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitReturnStmt(self)
        if self.Expr is not None:
            self.Expr.visit(visitor)
        visitor.afterVisitReturnStmt(self)


class BreakStmt(Stmt):
    """
    Хранит оператор "Прервать".
    """
    def __init__(self, place):
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitBreakStmt(self)
        # visitor.afterVisitBreakStmt(self)


class ContinueStmt(Stmt):
    """
    Хранит оператор "Продолжить".
    """
    def __init__(self, place):
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitContinueStmt(self)
        # visitor.afterVisitContinueStmt(self)


class RaiseStmt(Stmt):
    """
    Хранит оператор "ВызватьИсключение".
    Поле "Expr" равно Неопределено если это вариант оператора без выражения.
    """
    def __init__(self, expr, place):
        self.Expr: Optional[Expr] = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitRaiseStmt(self)
        if self.Expr is not None:
            self.Expr.visit(visitor)
        visitor.afterVisitRaiseStmt(self)


class ExecuteStmt(Stmt):
    """
    Хранит оператор "Выполнить".
    """
    def __init__(self, expr, place):
        self.Expr: Expr = expr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitExecuteStmt(self)
        self.Expr.visit(visitor)
        visitor.afterVisitExecuteStmt(self)


class CallStmt(Stmt):
    """
    Хранит вызов процедуры или функции как процедуры.
    """
    def __init__(self, identexpr, place):
        self.Ident: IdentExpr = identexpr
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitCallStmt(self)
        self.Ident.visit(visitor)
        visitor.afterVisitCallStmt(self)


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
        visitor.beforeVisitIfStmt(self)
        self.Cond.visit(visitor)
        for stmt in self.Then:
            stmt.visit(visitor)
        if self.ElsIf is not None:
            for stmt in self.ElsIf:
                stmt.visit(visitor)
        if self.Else is not None:
            self.Else.visit(visitor)
        visitor.afterVisitIfStmt(self)


class ElseStmt(Stmt):
    """
    Хранит блок "Иначе"
    """
    def __init__(self, body, place):
        self.Body: List[Stmt] = body
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitElseStmt(self)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.afterVisitElseStmt(self)


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
        visitor.beforeVisitElsIfStmt(self)
        self.Cond.visit(visitor)
        for stmt in self.Then:
            stmt.visit(visitor)
        visitor.afterVisitElsIfStmt(self)


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
        visitor.beforeVisitWhileStmt(self)
        self.Cond.visit(visitor)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.afterVisitWhileStmt(self)


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
        visitor.beforeVisitForStmt(self)
        self.Ident.visit(visitor)
        self.From.visit(visitor)
        self.To.visit(visitor)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.afterVisitForStmt(self)


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
        visitor.beforeVisitForEachStmt(self)
        self.Ident.visit(visitor)
        self.In.visit(visitor)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.afterVisitForEachStmt(self)


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
        visitor.beforeVisitTryStmt(self)
        for stmt in self.Try:
            stmt.visit(visitor)
        self.Except.visit(visitor)
        visitor.afterVisitTryStmt(self)


class ExceptStmt(Stmt):
    """
    Хранит блок "Исключение".
    """
    def __init__(self, body, place):
        self.Body: List[Stmt] = body
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitExceptStmt(self)
        for stmt in self.Body:
            stmt.visit(visitor)
        visitor.afterVisitExceptStmt(self)


class GotoStmt(Stmt):
    """
    Хранит оператор "Перейти".
    """
    def __init__(self, label, place):
        self.Label: str = label
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitGotoStmt(self)
        # visitor.afterVisitGotoStmt(self)


class LabelStmt(Stmt):
    """
    Хранит оператор метки.
    """
    def __init__(self, label, place):
        self.Label: str = label
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitLabelStmt(self)
        # visitor.afterVisitLabelStmt(self)


#endregion Statements


#region PrepInst


class PrepInst(Decl, Stmt):
    pass


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
        visitor.beforeVisitPrepIfInst(self)
        self.Cond.visit(visitor)
        visitor.afterVisitPrepIfInst(self)


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
        visitor.beforeVisitPrepElsIfInst(self)
        self.Cond.visit(visitor)
        visitor.afterVisitPrepElsIfInst(self)


class PrepElseInst(PrepInst):
    """
    Хранит информацию об инструкции препроцессора #Иначе
    """
    def __init__(self, place):
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitPrepElseInst(self)
        # visitor.afterVisitPrepElseInst(self)


class PrepEndIfInst(PrepInst):
    """
    Хранит информацию об инструкции препроцессора #КонецЕсли
    """
    def __init__(self, place):
        self.Place: Place = place

    def visit(self, visitor: Visitor):
        visitor.beforeVisitPrepEndIfInst(self)
        # visitor.afterVisitPrepEndIfInst(self)


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
        visitor.beforeVisitPrepRegionInst(self)
        # visitor.afterVisitPrepRegionInst(self)


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
        visitor.beforeVisitPrepEndRegionInst(self)
        # visitor.afterVisitPrepEndRegionInst(self)

#endregion PrepInst


#region PrepExpr


class PrepExpr(Node):
    pass


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
        visitor.beforeVisitPrepBinaryExpr(self)
        self.Left.visit(visitor)
        self.Right.visit(visitor)
        visitor.afterVisitPrepBinaryExpr(self)


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
        visitor.beforeVisitPrepNotExpr(self)
        self.Expr.visit(visitor)
        visitor.afterVisitPrepNotExpr(self)


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
        visitor.beforeVisitPrepSymExpr(self)
        # visitor.afterVisitPrepSymExpr(self)


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
        visitor.beforeVisitPrepParenExpr(self)
        self.Expr.visit(visitor)
        visitor.afterVisitPrepParenExpr(self)


#endregion PrepExpr