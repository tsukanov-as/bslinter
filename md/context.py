# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from bsl.ast import Item, GlobalObject, GlobalMethod, GlobalMethodParameter as P, Env
from collections import namedtuple
from typing import List

Prop = namedtuple('Prop', 'names item')

def attrib(name, runame, context):
    decl = GlobalObject(name, context)
    return Prop([name, runame] , Item(name, decl))

def method(name, runame, retval, params, context):
    decl = GlobalMethod(name, retval, params, context)
    return Prop([name, runame] , Item(name, decl))

class Context():

    standard: List[Prop] = []
    attribs: List[Prop] = []
    methods: List[Prop] = []

    @classmethod
    def fill(cls, scope):

        for prop in cls.standard:
            for name in prop.names:
                if not scope.Vars.get(name):
                    scope.Vars[name.lower()] = prop.item

        for prop in cls.attribs:
            for name in prop.names:
                scope.Vars[name.lower()] = prop.item

        for prop in cls.methods:
            for name in prop.names:
                scope.Methods[name.lower()] = prop.item

class ClientApplicationForm(Context):
    # TODO: выделить в отдельный класс расширения формы для документов, справочников и т.д.
    attribs = [
        attrib('UUID', 'УникальныйИдентификатор', Env()),
        attrib('ThisObject', 'ЭтотОбъект', Env()),
        attrib('ThisForm', 'ЭтаФорма', Env()),
        attrib('Items', 'Элементы', Env()),
        attrib('Parameters', 'Параметры', Env()),
        attrib('ReadOnly', 'ТолькоПросмотр', Env()),
        attrib('ConditionalAppearance', 'УсловноеОформление', Env()),
        attrib('Modified', 'Модифицированность', Env()),
        attrib('Window', 'Окно', Env()),
        attrib('Commands', 'Команды', Env()),
        attrib('FormOwner', 'ВладелецФормы', Env()),
        attrib('CurrentItem', 'ТекущийЭлемент', Env()),
        attrib('CommandBar', 'КоманднаяПанель', Env()),
        attrib('Title', 'Заголовок', Env()),
    ]
    methods = [
        method('FormAttributeToValue', 'РеквизитФормыВЗначение', True, [P('AttributeName', True), P('Type', False)], Env()),
        method('ValueToFormAttribute', 'ЗначениеВРеквизитФормы', True, [P('Value', True), P('AttributeName', True)], Env()),
        method('Write', 'записать', True, [P('WriteParameters', False)], Env()),
        method('LockFormDataForEdit', 'ЗаблокироватьДанныеФормыДляРедактирования', False, [], Env()),
        method('IsInputAvailable', 'ВводДоступен', True, [], Env()),
        method('Close', 'Закрыть', True, [P('CloseParameter', False)], Env()),
        method('Read', 'Прочитать', False, [], Env()),
        method('GetFormFunctionalOption', 'ПолучитьФункциональнуюОпциюФормы', False, [P('Name', True)], Env()),
        method('RefreshDataRepresentation', 'ОбновитьОтображениеДанных', False, [P('UpdateItems', False)], Env()),
        method('GetAttributes', 'ПолучитьРеквизиты', True, [P('Path', False)], Env()),
        method('ChangeAttributes', 'ИзменитьРеквизиты', False, [P('AttributesToBeAdded', False), P('AttributesToBeDeleted', False)], Env()),
        method('NotifyChoice', 'ОповеститьОВыборе', False, [P('SelectionValue', True)], Env()),
        method('ShowChooseFromList', 'ПоказатьВыборИзСписка', False, [P('NotifyOnCloseDescription', True), P('ValueList', True), P('FormItem', False), P('InitialValue', False)], Env()),
        method('CheckFilling', 'ПроверитьЗаполнение', True, [], Env()),
        method('ClearMarkIncomplete', 'ОтключитьОтметкуНезаполненного', False, [], Env()),
        method('IsOpen', 'Открыта', True, [], Env()),
        method('Activate', 'Активизировать', False, [], Env()),
        method('SetFormFunctionalOptionParameters', 'УстановитьПараметрыФункциональныхОпцийФормы', False, [P('ParametersToBeSpecified', True), P('ParametersToBeReset', False)], Env()),
        method('ShowChooseFromMenu', 'ПоказатьВыборИзМеню', False, [P('NotifyDescriptionOnCompletion', True), P('ListOfValues', True), P('FormItem', False)], Env()),
    ]

class CommonModule(Context):
    attribs = [
        attrib('ThisObject', 'ЭтотОбъект', Env()),
    ]

class DocumentObject(Context):
    standard = [
        attrib('Ref', 'Ссылка', Env()),
        attrib('Number', 'Номер', Env()),
        attrib('Date', 'Дата', Env()),
    ]
    attribs = [
        attrib('AdditionalProperties', 'ДополнительныеСвойства', Env()),
        attrib('RegisterRecords', 'Движения', Env()),
        attrib('DataExchange', 'ОбменДанными', Env()),
        attrib('DeletionMark', 'ПометкаУдаления', Env()),
    ]
    methods = [
        method('PointInTime', 'МоментВремени', True, [], Env()),
        method('Metadata', 'Метаданные', True, [], Env()),
        method('IsNew', 'ЭтоНовый', True, [], Env()),
        method('CheckFilling', 'ПроверитьЗаполнение', True, [], Env()),
        method('Fill', 'Заполнить', False, [P('FillingData', True)], Env()),
        method('SetNewNumber', 'УстановитьНовыйНомер', False, [P('NumberPrefix', False)], Env()),
        method('SetNewObjectRef', 'УстановитьСсылкуНового', False, [P('Reference', True)], Env()),
    ]

class DocumentManager(Context):

    methods = [
        method('GetTemplate', 'ПолучитьМакет', True, [P('Template', True)], Env()),
        method('EmptyRef', 'ПустаяСсылка', True, [], Env()),
    ]

class DocumentStandardAttributes(Context):
    pass