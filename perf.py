# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
Замер производительности анализа файлов *.bsl.
"""

from bsl.parser import Parser
from bsl.visitor import Visitor

import time
import pathlib
import concurrent.futures

def parse(path):
    with open(str(path), 'r', encoding='utf-8-sig') as f:
        s = f.read()
        p = Parser(s)
        try:
            AST = p.parse()
            visitor = Visitor([])
            AST.visit(visitor) # обход AST в холостую без плагинов
        except Exception as e:
            print(f"Не удалось разобрать модуль: {path}")
        return p.cur_line

def main():

    mypath = "C:/temp/RUERP24" # путь к выгрузке конфигурации
    print(f"Выполняется анализ файлов *.bsl в папке {mypath}...")
    print("Пожалуйста, дождитесь окончания (это не долго)")

    strt = time.perf_counter()

    result = list(pathlib.Path(mypath).rglob("*.[bB][sS][lL]"))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.map(parse, result)

    print('Время анализа (сек.):', time.perf_counter() - strt)

    print('Строк исходного кода проанализировано:', sum(result))

if __name__ == "__main__":
    main()
