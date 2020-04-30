# bslinter

Используется:
* python 3.8
* VSC
* vscode-python
* vscode-python-test-adapter
* mypy
* pytest

## Полезные настройки VSC
* "python.linting.mypyEnabled" - включить, т.к. mypy контролирует типы лучше чем pylint.
* "python.linting.pylintEnabled" - выключить если pylint раздражает ложными срабатываниями.
* "python.dataScience.debugJustMyCode" - выключить если отладчик не останавливается в плагине.
* "files.trimTrailingWhitespace" - включить, чтобы мусор не попадал в репозиторий.
* "debug.internalConsoleOptions" - переключить на "openOnSessionStart", чтобы при запуске отладки открывалась отладочная консоль.
* "editor.multiCursorModifier" - переключить на "ctrlCmd" если раздражают ссылки при нажатии ctrl.
* "python.autoComplete.addBrackets" - включить если нужно чтобы скобки автоматически добавлялись для функций при наборе кода.
