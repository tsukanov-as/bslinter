# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from enum import Enum, auto

class EnumBase(Enum):

    @classmethod
    def get(cls, key):
        # pylint: disable=no-member
        return cls._member_map_.get(key.upper())

class Keywords(EnumBase):

    IF = ЕСЛИ = auto()
    THEN = ТОГДА = auto()
    ELSIF = ИНАЧЕЕСЛИ = auto()
    ELSE = ИНАЧЕ = auto()
    ENDIF = КОНЕЦЕСЛИ = auto()
    FOR = ДЛЯ = auto()
    EACH = КАЖДОГО = auto()
    IN = ИЗ = auto()
    TO = ПО = auto()
    WHILE = ПОКА = auto()
    DO = ЦИКЛ = auto()
    ENDDO = КОНЕЦЦИКЛА = auto()
    PROCEDURE = ПРОЦЕДУРА = auto()
    ENDPROCEDURE = КОНЕЦПРОЦЕДУРЫ = auto()
    FUNCTION = ФУНКЦИЯ = auto()
    ENDFUNCTION = КОНЕЦФУНКЦИИ = auto()
    VAR = ПЕРЕМ = auto()
    VAL = ЗНАЧ = auto()
    RETURN = ВОЗВРАТ = auto()
    CONTINUE = ПРОДОЛЖИТЬ = auto()
    BREAK = ПРЕРВАТЬ = auto()
    AND = И = auto()
    OR = ИЛИ = auto()
    NOT = НЕ = auto()
    TRY = ПОПЫТКА = auto()
    EXCEPT = ИСКЛЮЧЕНИЕ = auto()
    RAISE = ВЫЗВАТЬИСКЛЮЧЕНИЕ = auto()
    ENDTRY = КОНЕЦПОПЫТКИ = auto()
    NEW = НОВЫЙ = auto()
    EXECUTE = ВЫПОЛНИТЬ = auto()
    EXPORT = ЭКСПОРТ = auto()
    GOTO = ПЕРЕЙТИ = auto()
    TRUE = ИСТИНА = auto()
    FALSE = ЛОЖЬ = auto()
    UNDEFINED = НЕОПРЕДЕЛЕНО = auto()
    NULL = auto()

class Tokens(EnumBase):

    IDENT = auto()
    NUMBER = auto()
    STRING = auto()
    DATETIME = auto()

    STRINGBEG = auto()
    STRINGMID = auto()
    STRINGEND = auto()

    EQL = auto()  # =
    NEQ = auto()  # <>
    LSS = auto()  # <
    GTR = auto()  # >
    LEQ = auto()  # <=
    GEQ = auto()  # >=
    ADD = auto()  # +
    SUB = auto()  # -
    MUL = auto()  # *
    DIV = auto()  # /
    MOD = auto()  # %

    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACK = auto()  # [
    RBRACK = auto()  # ]

    TERNARY = auto()    # ?
    COMMA = auto()      # ,
    PERIOD = auto()     # .
    COLON = auto()      # :
    SEMICOLON = auto()  # ;

    EOF = auto()
    COMMENT = auto()    # //
    LABEL = auto()      # ~
    DIRECTIVE = auto()  # &

class Directives(EnumBase):

    ATCLIENT = НАКЛИЕНТЕ = auto()
    ATSERVER = НАСЕРВЕРЕ = auto()
    ATSERVERNOCONTEXT = НАСЕРВЕРЕБЕЗКОНТЕКСТА = auto()
    ATCLIENTATSERVERNOCONTEXT = НАКЛИЕНТЕНАСЕРВЕРЕБЕЗКОНТЕКСТА = auto()
    ATCLIENTATSERVER = НАКЛИЕНТЕНАСЕРВЕРЕ = auto()

class PrepInstructions(EnumBase):

    IF = ЕСЛИ = auto()
    ELSIF = ИНАЧЕЕСЛИ = auto()
    ELSE = ИНАЧЕ = auto()
    ENDIF = КОНЕЦЕСЛИ = auto()
    REGION = ОБЛАСТЬ = auto()
    ENDREGION = КОНЕЦОБЛАСТИ = auto()

class PrepSymbols(EnumBase):

    CLIENT = КЛИЕНТ = auto()
    ATCLIENT = НАКЛИЕНТЕ = auto()
    ATSERVER = НАСЕРВЕРЕ = auto()
    MOBILEAPPCLIENT = МОБИЛЬНОЕПРИЛОЖЕНИЕКЛИЕНТ = auto()
    MOBILEAPPSERVER = МОБИЛЬНОЕПРИЛОЖЕНИЕСЕРВЕР = auto()
    THICKCLIENTORDINARYAPPLICATION = ТОЛСТЫЙКЛИЕНТОБЫЧНОЕПРИЛОЖЕНИЕ = auto()
    THICKCLIENTMANAGEDAPPLICATION = ТОЛСТЫЙКЛИЕНТУПРАВЛЯЕМОЕПРИЛОЖЕНИЕ = auto()
    SERVER = СЕРВЕР = auto()
    EXTERNALCONNECTION = ВНЕШНЕЕСОЕДИНЕНИЕ = auto()
    THINCLIENT = ТОНКИЙКЛИЕНТ = auto()
    WEBCLIENT = ВЕБКЛИЕНТ = auto()
