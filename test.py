
"""
Это пример отладочного скрипта для разработки диагностики исходного кода.
Запуск выполняется в один поток и анализируется один файл test.bsl - это позволяет
выполнять отладку без боли.
Если в редакторе VSC отладчик не осталанвливается на точках останова внутри плагина,
то нужно выключить настройку "python.dataScience.debugJustMyCode".
"""

import plugins.bsl.errors as errors
from bsl.parser import Parser
import bsl.visitor
import os.path
import bsl.ast as ast

class Test:

    """
    Плагин - диагностика исходного кода в простейшем виде для отладки.
    Ошибки просто выводятся в консоль.
    """

    def __init__(self, path, src):
        """
        Инициализация плагина.
        """
        self.path = path # путь к исходнику
        self.src = src   # текст исходника
        self.errors: List[str] = [] # список ошибок

    def visit_MethodDecl(self, node: ast.MethodDecl, stack, counters):
        """
        Подписка на объявление метода. Будет вызвана визитером для каждого объявления в порядке их следования.
        """
        if (type(node.Sign) == ast.FuncSign # проверяются только функции
            and (len(node.Body) == 0 or type(node.Body[-1]) != ast.ReturnStmt)):
            # если тело функции пустое или последняя инструкция не Возврат, то регистрируем ошибку:
            self.errors.append(f"Функция {node.Sign.Name} в строке {node.Place.BegLine} должна оканчиваться инструкцией Возврат")

    def close(self):
        return '\n'.join(self.errors)

def parse():
    path = 'test.bsl'
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            src = f.read()
            parser = Parser(src)
            try:
                ast = parser.parse() # разбор исходного кода с результатом в виде AST
                plugins = [
                    Test(path, src),
                    # сюда можно добавить еще плагины
                ]
                visitor = bsl.visitor.Visitor(plugins) # создание визитера с набором указанных плагинов
                ast.visit(visitor) # обход AST, в процессе которого вызываются методы плагинов.
                results = [] # список результатов работы плагинов
                for plugin in plugins:
                    results.append(plugin.close())
                return results
            except Exception as e:
                print(path)
                print(e)

results = parse()

print('\n'.join(results))

# Функция Тест1 в строке 2 должна оканчиваться инструкцией Возврат
# Функция Тест2 в строке 6 должна оканчиваться инструкцией Возврат
