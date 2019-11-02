
import pytest
from bsl.parser import Parser, Error
from bsl.parser import UnexpectedSyntax, UnexpectedChar, UnexpectedToken, UnknownToken
from bsl.parser import AlreadyDeclared

def error(src, err):
    p = Parser(src)
    p.parse()
    assert len(p.errors) == 1
    assert p.errors[0] == err

def parse(src):
    Parser(src).parse()

class TestParser:

    def test_pass(self):

        parse("var x; x = x + 1")
        parse("var x; x = +x + -1")
        parse("var x; y = ?(x, 1, 2).y(1)")
        parse("var x; y = x[0]")
        parse("var x; y = x[0].z()")
        parse("var x; y = x[0].z[1].q.q()")
        parse("var x; x.y = x")

    def test_ast(self):

        m = Parser("var x; x = x + 1").parse()
        assert len(m.Auto) == 0
        assert len(m.Decls) == 1
        assert len(m.Body) == 1
        stmt = m.Body[0]
        assert stmt.Place.BegPos == 7 and stmt.Place.EndPos == 16

    def test_exception(self):

        with pytest.raises(UnexpectedToken):
            parse("x = / + 1")

        with pytest.raises(UnexpectedToken):
            parse("x = + + 1")

        with pytest.raises(UnexpectedToken):
            parse("x = * 1")

        with pytest.raises(UnexpectedToken):
            parse("x = = 1")

        with pytest.raises(UnexpectedToken):
            parse(" = 1")

    def test_error(self):

        error("x = x + 1", Error('Undeclared identifier "x"', 4, 1))
