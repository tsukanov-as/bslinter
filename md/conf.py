# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import List, Optional
from decimal import Decimal
from enum import EnumMeta

import md.enums as enums
from md.visitor import Visitor
from md.base import XMLData, XMLFile, XMLParser, fill_types

import os.path

#region basic

Uuid = str
DataPath = str
MDObjectRef = str
MDMethodRef = str
FieldRef = str
IncludeInCommandCategoriesType = str
QName = str

class LocalStringTypeItem(XMLData):
    lang:    Optional[str]
    content: Optional[str]

    def visit(self, visitor: Visitor):
        visitor.visit_LocalStringTypeItem(self)

class LocalStringType(XMLData):
    item: List[LocalStringTypeItem]

    def visit(self, visitor: Visitor):
        visitor.visit_LocalStringType(self)
        if self.item is not None:
            for item in self.item:
                item.visit(visitor)
        visitor.leave_LocalStringType(self)

class MDListTypeItem(XMLData):
    type:  Optional[str]
    _text: Optional[str]


class MDListType(XMLData):
    Item: List[MDListTypeItem]


class FieldListItem(XMLData):
    type:  Optional[str]
    _text: Optional[str]


class FieldList(XMLData):
    Field: Optional[FieldListItem]


class ChoiceParameterLink(XMLData):
    Name:        Optional[str]
    DataPath:    Optional[str]
    ValueChange: Optional[enums.LinkedValueChangeMode]


class ChoiceParameterLinks(XMLData):
    Link: List[ChoiceParameterLink]


class TypeLink(XMLData):
    DataPath:    Optional[DataPath]
    LinkItem:    Optional[Decimal]
    ValueChange: Optional[enums.LinkedValueChangeMode]


class FillValue(XMLData):
    type:  Optional[str]
    _text: Optional[str]


#endregion basic

#region standard

class StandardAttribute(XMLData):
    name:                 Optional[str]
    Synonym:              Optional[LocalStringType]
    Comment:              Optional[str]
    ToolTip:              Optional[LocalStringType]
    QuickChoice:          Optional[enums.UseQuickChoice]
    FillChecking:         Optional[enums.FillChecking]
    FillValue:            Optional[FillValue]
    FillFromFillingValue: Optional[enums.Bool]
    ChoiceParameterLinks: Optional[ChoiceParameterLinks]
    LinkByType:           Optional[TypeLink]
    FullTextSearch:       Optional[enums.FullTextSearchUsing]
    PasswordMode:         Optional[enums.Bool]
    DataHistory:          Optional[enums.DataHistoryUse]
    Format:               Optional[LocalStringType]
    EditFormat:           Optional[LocalStringType]
    Mask:                 Optional[str]
    MultiLine:            Optional[enums.Bool]
    ExtendedEdit:         Optional[enums.Bool]
    MarkNegatives:        Optional[enums.Bool]
    ChoiceForm:           Optional[MDObjectRef]
    CreateOnInput:        Optional[enums.CreateOnInput]
    ChoiceHistoryOnInput: Optional[enums.ChoiceHistoryOnInput]
    #ChoiceParameters
    #MinValue
    #MaxValue

class StandardAttributes(XMLData):
    StandardAttribute: List[StandardAttribute]

class StandardTabularSection(XMLData):
    name:               Optional[str]
    Synonym:            Optional[LocalStringType]
    Comment:            Optional[str]
    ToolTip:            Optional[LocalStringType]
    FillChecking:       Optional[enums.FillChecking]
    StandardAttributes: Optional[StandardAttributes]

class StandardTabularSections(XMLData):
    StandardTabularSection: Optional[StandardTabularSection]

class CharacteristicTypes(XMLData):
    # from:             Optional[MDObjectRef]
    KeyField:         Optional[FieldRef]
    TypesFilterField: Optional[FieldRef]
    # TypesFilterValue

class CharacteristicValues(XMLData):
    # from:        Optional[MDObjectRef]
    ObjectField: Optional[FieldRef]
    TypeField:   Optional[FieldRef]
    # ValueField

class Characteristic(XMLData):
    CharacteristicTypes:  Optional[CharacteristicTypes]
    CharacteristicValues: Optional[CharacteristicValues]

class Characteristics(XMLData):
    Characteristic: Optional[Characteristic]

#endregion standard

#region types

class NumberQualifiers(XMLData):
    Digits:         Optional[Decimal]
    FractionDigits: Optional[Decimal]
    AllowedSign:    Optional[enums.AllowedSign]

class StringQualifiers(XMLData):
    Length:        Optional[Decimal]
    AllowedLength: Optional[enums.AllowedLength]

class DateQualifiers(XMLData):
    DateFractions: Optional[enums.DateFractions]

class BinaryDataQualifiers(XMLData):
    Length:        Optional[Decimal]
    AllowedLength: Optional[enums.AllowedLength]

class TypeDescription(XMLData):
    Type:                 Optional[QName]
    TypeSet:              Optional[QName]
    TypeId:               Optional[Uuid]
    NumberQualifiers:     Optional[NumberQualifiers]
    StringQualifiers:     Optional[StringQualifiers]
    DateQualifiers:       Optional[DateQualifiers]
    BinaryDataQualifiers: Optional[BinaryDataQualifiers]

#endregion types

#region children

class AttributeProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    Type:                  Optional[TypeDescription]
    PasswordMode:          Optional[enums.Bool]
    Format:                Optional[LocalStringType]
    EditFormat:            Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    MarkNegatives:         Optional[enums.Bool]
    Mask:                  Optional[str]
    MultiLine:             Optional[enums.Bool]
    ExtendedEdit:          Optional[enums.Bool]
    FillFromFillingValue:  Optional[enums.Bool]
    FillValue:             Optional[FillValue]
    FillChecking:          Optional[enums.FillChecking]
    ChoiceFoldersAndItems: Optional[enums.FoldersAndItemsUse]
    ChoiceParameterLinks:  Optional[ChoiceParameterLinks]
    QuickChoice:           Optional[enums.UseQuickChoice]
    CreateOnInput:         Optional[enums.CreateOnInput]
    ChoiceForm:            Optional[MDObjectRef]
    LinkByType:            Optional[TypeLink]
    ChoiceHistoryOnInput:  Optional[enums.ChoiceHistoryOnInput]
    Indexing:              Optional[enums.Indexing]
    FullTextSearch:        Optional[enums.FullTextSearchUsing]
    Use:                   Optional[enums.AttributeUse]
    ScheduleLink:          Optional[MDObjectRef]
    DataHistory:           Optional[enums.DataHistoryUse]
    #MinValue
    #MaxValue
    #ChoiceParameters

class Attribute(XMLData):
    uuid:       Optional[str]
    Properties: Optional[AttributeProperties]

class DimensionProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    Type:                  Optional[TypeDescription]
    PasswordMode:          Optional[enums.Bool]
    Format:                Optional[LocalStringType]
    EditFormat:            Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    MarkNegatives:         Optional[enums.Bool]
    Mask:                  Optional[str]
    MultiLine:             Optional[enums.Bool]
    ExtendedEdit:          Optional[enums.Bool]
    FillChecking:          Optional[enums.FillChecking]
    ChoiceFoldersAndItems: Optional[enums.FoldersAndItemsUse]
    ChoiceParameterLinks:  Optional[ChoiceParameterLinks]
    QuickChoice:           Optional[enums.UseQuickChoice]
    CreateOnInput:         Optional[enums.CreateOnInput]
    ChoiceForm:            Optional[MDObjectRef]
    LinkByType:            Optional[TypeLink]
    ChoiceHistoryOnInput:  Optional[enums.ChoiceHistoryOnInput]
    Balance:               Optional[enums.Bool]
    AccountingFlag:        Optional[MDObjectRef]
    DenyIncompleteValues:  Optional[enums.Bool]
    Indexing:              Optional[enums.Indexing]
    FullTextSearch:        Optional[enums.FullTextSearchUsing]
    UseInTotals:           Optional[enums.Bool]
    RegisterDimension:     Optional[MDObjectRef]
    LeadingRegisterData:   Optional[MDListType]
    FillFromFillingValue:  Optional[enums.Bool]
    FillValue:             Optional[FillValue]
    Master:                Optional[enums.Bool]
    MainFilter:            Optional[enums.Bool]
    BaseDimension:         Optional[enums.Bool]
    ScheduleLink:          Optional[MDObjectRef]
    DocumentMap:           Optional[MDListType]
    RegisterRecordsMap:    Optional[MDListType]
    DataHistory:           Optional[enums.DataHistoryUse]
    #MinValue
    #MaxValue
    #ChoiceParameters

class Dimension(XMLData):
    uuid:       Optional[str]
    Properties: Optional[DimensionProperties]

class ResourceProperties(XMLData):
    Name:                       Optional[str]
    Synonym:                    Optional[LocalStringType]
    Comment:                    Optional[str]
    Type:                       Optional[TypeDescription]
    PasswordMode:               Optional[enums.Bool]
    Format:                     Optional[LocalStringType]
    EditFormat:                 Optional[LocalStringType]
    ToolTip:                    Optional[LocalStringType]
    MarkNegatives:              Optional[enums.Bool]
    Mask:                       Optional[str]
    MultiLine:                  Optional[enums.Bool]
    ExtendedEdit:               Optional[enums.Bool]
    FillChecking:               Optional[enums.FillChecking]
    ChoiceFoldersAndItems:      Optional[enums.FoldersAndItemsUse]
    ChoiceParameterLinks:       Optional[ChoiceParameterLinks]
    QuickChoice:                Optional[enums.UseQuickChoice]
    CreateOnInput:              Optional[enums.CreateOnInput]
    ChoiceForm:                 Optional[MDObjectRef]
    LinkByType:                 Optional[TypeLink]
    ChoiceHistoryOnInput:       Optional[enums.ChoiceHistoryOnInput]
    FullTextSearch:             Optional[enums.FullTextSearchUsing]
    Balance:                    Optional[enums.Bool]
    AccountingFlag:             Optional[MDObjectRef]
    ExtDimensionAccountingFlag: Optional[MDObjectRef]
    NameInDataSource:           Optional[str]
    FillFromFillingValue:       Optional[enums.Bool]
    FillValue:                  Optional[FillValue]
    Indexing:                   Optional[enums.Indexing]
    DataHistory:                Optional[enums.DataHistoryUse]
    #MinValue
    #MaxValue
    #ChoiceParameters

class Resource(XMLData):
    uuid:       Optional[str]
    Properties: Optional[ResourceProperties]

class CommandProperties(XMLData):
    Name:                 Optional[str]
    Synonym:              Optional[LocalStringType]
    Comment:              Optional[str]
    Group:                Optional[IncludeInCommandCategoriesType]
    CommandParameterType: Optional[TypeDescription]
    ParameterUseMode:     Optional[enums.CommandParameterUseMode]
    ModifiesData:         Optional[enums.Bool]
    Representation:       Optional[enums.ButtonRepresentation]
    ToolTip:              Optional[LocalStringType]
    #Picture
    #Shortcut

class Command(XMLData):
    uuid:         Optional[str]
    Properties: Optional[CommandProperties]

class AccountingFlagProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    Type:                  Optional[TypeDescription]
    PasswordMode:          Optional[enums.Bool]
    Format:                Optional[LocalStringType]
    EditFormat:            Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    MarkNegatives:         Optional[enums.Bool]
    Mask:                  Optional[str]
    MultiLine:             Optional[enums.Bool]
    ExtendedEdit:          Optional[enums.Bool]
    FillFromFillingValue:  Optional[enums.Bool]
    FillValue:             Optional[FillValue]
    FillChecking:          Optional[enums.FillChecking]
    ChoiceFoldersAndItems: Optional[enums.FoldersAndItemsUse]
    ChoiceParameterLinks:  Optional[ChoiceParameterLinks]
    QuickChoice:           Optional[enums.UseQuickChoice]
    CreateOnInput:         Optional[enums.CreateOnInput]
    ChoiceForm:            Optional[MDObjectRef]
    LinkByType:            Optional[TypeLink]
    ChoiceHistoryOnInput:  Optional[enums.ChoiceHistoryOnInput]
    #MinValue
    #MaxValue
    #ChoiceParameters

class AccountingFlag(XMLData):
    uuid:       Optional[str]
    Properties: Optional[AccountingFlagProperties]

class ExtDimensionAccountingFlagProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    Type:                  Optional[TypeDescription]
    PasswordMode:          Optional[enums.Bool]
    Format:                Optional[LocalStringType]
    EditFormat:            Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    MarkNegatives:         Optional[enums.Bool]
    Mask:                  Optional[str]
    MultiLine:             Optional[enums.Bool]
    ExtendedEdit:          Optional[enums.Bool]
    FillFromFillingValue:  Optional[enums.Bool]
    FillValue:             Optional[FillValue]
    FillChecking:          Optional[enums.FillChecking]
    ChoiceFoldersAndItems: Optional[enums.FoldersAndItemsUse]
    ChoiceParameterLinks:  Optional[ChoiceParameterLinks]
    QuickChoice:           Optional[enums.UseQuickChoice]
    CreateOnInput:         Optional[enums.CreateOnInput]
    ChoiceForm:            Optional[MDObjectRef]
    LinkByType:            Optional[TypeLink]
    ChoiceHistoryOnInput:  Optional[enums.ChoiceHistoryOnInput]
    #MinValue
    #MaxValue
    #ChoiceParameters

class ExtDimensionAccountingFlag(XMLData):
    uuid:       Optional[str]
    Properties: Optional[ExtDimensionAccountingFlagProperties]

class ColumnProperties(XMLData):
    Name:       Optional[str]
    Synonym:    Optional[LocalStringType]
    Comment:    Optional[str]
    Indexing:   Optional[enums.Indexing]
    References: Optional[MDListType]

class Column(XMLData):
    uuid:       Optional[str]
    Properties: Optional[ColumnProperties]

class EnumValueProperties(XMLData):
    Name:    Optional[str]
    Synonym: Optional[LocalStringType]
    Comment: Optional[str]

class EnumValue(XMLData):
    uuid:       Optional[str]
    Properties: Optional[EnumValueProperties]

class FormProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    FormType:              Optional[enums.FormType]
    IncludeHelpInContents: Optional[enums.Bool]
    ExtendedPresentation:  Optional[LocalStringType]
    #UsePurposes  "FixedArray"

class Form(XMLData):
    uuid:       Optional[str]
    Properties: Optional[FormProperties]

class Template(XMLData):
    uuid:         Optional[str]
    Name:         Optional[str]
    Synonym:      Optional[LocalStringType]
    Comment:      Optional[str]
    TemplateType: Optional[enums.TemplateType]

class AddressingAttributeProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    Type:                  Optional[TypeDescription]
    PasswordMode:          Optional[enums.Bool]
    Format:                Optional[LocalStringType]
    EditFormat:            Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    MarkNegatives:         Optional[enums.Bool]
    Mask:                  Optional[str]
    MultiLine:             Optional[enums.Bool]
    ExtendedEdit:          Optional[enums.Bool]
    FillFromFillingValue:  Optional[enums.Bool]
    FillValue:             Optional[FillValue]
    FillChecking:          Optional[enums.FillChecking]
    ChoiceFoldersAndItems: Optional[enums.FoldersAndItemsUse]
    ChoiceParameterLinks:  Optional[ChoiceParameterLinks]
    QuickChoice:           Optional[enums.UseQuickChoice]
    CreateOnInput:         Optional[enums.CreateOnInput]
    ChoiceForm:            Optional[MDObjectRef]
    LinkByType:            Optional[TypeLink]
    ChoiceHistoryOnInput:  Optional[enums.ChoiceHistoryOnInput]
    Indexing:              Optional[enums.Indexing]
    AddressingDimension:   Optional[MDObjectRef]
    FullTextSearch:        Optional[enums.FullTextSearchUsing]
    #MinValue
    #MaxValue
    #ChoiceParameters

class AddressingAttribute(XMLData):
    uuid:       Optional[str]
    Properties: Optional[AddressingAttributeProperties]

class TabularSectionProperties(XMLData):
    Name:               Optional[str]
    Synonym:            Optional[LocalStringType]
    Comment:            Optional[str]
    ToolTip:            Optional[LocalStringType]
    FillChecking:       Optional[enums.FillChecking]
    StandardAttributes: Optional[StandardAttributes]
    Use:                Optional[enums.AttributeUse]

class TabularSectionChildObjects(XMLData):
    Attribute: List[Attribute]

class TabularSection(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[TabularSectionProperties]
    ChildObjects: Optional[TabularSectionChildObjects]

#endregion children

#region meta

class AccountingRegisterProperties(XMLData):
    Name:                     Optional[str]
    Synonym:                  Optional[LocalStringType]
    Comment:                  Optional[str]
    UseStandardCommands:      Optional[enums.Bool]
    IncludeHelpInContents:    Optional[enums.Bool]
    ChartOfAccounts:          Optional[MDObjectRef]
    Correspondence:           Optional[enums.Bool]
    PeriodAdjustmentLength:   Optional[Decimal]
    DefaultListForm:          Optional[MDObjectRef]
    AuxiliaryListForm:        Optional[MDObjectRef]
    StandardAttributes:       Optional[StandardAttributes]
    DataLockControlMode:      Optional[enums.DefaultDataLockControlMode]
    EnableTotalsSplitting:    Optional[enums.Bool]
    FullTextSearch:           Optional[enums.FullTextSearchUsing]
    ListPresentation:         Optional[LocalStringType]
    ExtendedListPresentation: Optional[LocalStringType]
    Explanation:              Optional[LocalStringType]

class AccountingRegisterChildObjects(XMLData):
    Dimension: List[Dimension]
    Resource:  List[Resource]
    Attribute: List[Attribute]
    Form:      List[str]
    Template:  List[str]
    Command:   List[Command]

class AccountingRegister(XMLData):
    uuid:          Optional[str]
    Properties:    Optional[AccountingRegisterProperties]
    ChildObjects:  Optional[AccountingRegisterChildObjects]

class AccumulationRegisterProperties(XMLData):
    Name:                     Optional[str]
    Synonym:                  Optional[LocalStringType]
    Comment:                  Optional[str]
    UseStandardCommands:      Optional[enums.Bool]
    DefaultListForm:          Optional[MDObjectRef]
    AuxiliaryListForm:        Optional[MDObjectRef]
    RegisterType:             Optional[enums.AccumulationRegisterType]
    IncludeHelpInContents:    Optional[enums.Bool]
    StandardAttributes:       Optional[StandardAttributes]
    DataLockControlMode:      Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:           Optional[enums.FullTextSearchUsing]
    EnableTotalsSplitting:    Optional[enums.Bool]
    ListPresentation:         Optional[LocalStringType]
    ExtendedListPresentation: Optional[LocalStringType]
    Explanation:              Optional[LocalStringType]

class AccumulationRegisterChildObjects(XMLData):
    Resource:  List[Resource]
    Attribute: List[Attribute]
    Dimension: List[Dimension]
    Form:      List[str]
    Template:  List[str]
    Command:   List[Command]

class AccumulationRegister(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[AccumulationRegisterProperties]
    ChildObjects: Optional[AccumulationRegisterChildObjects]

class BusinessProcessProperties(XMLData):
    Name:                             Optional[str]
    Synonym:                          Optional[LocalStringType]
    Comment:                          Optional[str]
    UseStandardCommands:              Optional[enums.Bool]
    EditType:                         Optional[enums.EditType]
    InputByString:                    Optional[FieldList]
    CreateOnInput:                    Optional[enums.CreateOnInput]
    SearchStringModeOnInputByString:  Optional[enums.SearchStringModeOnInputByString]
    ChoiceDataGetModeOnInputByString: Optional[enums.ChoiceDataGetModeOnInputByString]
    FullTextSearchOnInputByString:    Optional[enums.FullTextSearchOnInputByString]
    DefaultObjectForm:                Optional[MDObjectRef]
    DefaultListForm:                  Optional[MDObjectRef]
    DefaultChoiceForm:                Optional[MDObjectRef]
    AuxiliaryObjectForm:              Optional[MDObjectRef]
    AuxiliaryListForm:                Optional[MDObjectRef]
    AuxiliaryChoiceForm:              Optional[MDObjectRef]
    ChoiceHistoryOnInput:             Optional[enums.ChoiceHistoryOnInput]
    NumberType:                       Optional[enums.BusinessProcessNumberType]
    NumberLength:                     Optional[Decimal]
    NumberAllowedLength:              Optional[enums.AllowedLength]
    CheckUnique:                      Optional[enums.Bool]
    StandardAttributes:               Optional[StandardAttributes]
    Characteristics:                  Optional[Characteristics]
    Autonumbering:                    Optional[enums.Bool]
    BasedOn:                          Optional[MDListType]
    NumberPeriodicity:                Optional[enums.BusinessProcessNumberPeriodicity]
    Task:                             Optional[MDObjectRef]
    CreateTaskInPrivilegedMode:       Optional[enums.Bool]
    DataLockFields:                   Optional[FieldList]
    DataLockControlMode:              Optional[enums.DefaultDataLockControlMode]
    IncludeHelpInContents:            Optional[enums.Bool]
    FullTextSearch:                   Optional[enums.FullTextSearchUsing]
    ObjectPresentation:               Optional[LocalStringType]
    ExtendedObjectPresentation:       Optional[LocalStringType]
    ListPresentation:                 Optional[LocalStringType]
    ExtendedListPresentation:         Optional[LocalStringType]
    Explanation:                      Optional[LocalStringType]

class BusinessProcessChildObjects(XMLData):
    Attribute:      List[Attribute]
    TabularSection: List[TabularSection]
    Form:           List[str]
    Template:       List[str]
    Command:        List[Command]

class BusinessProcess(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[BusinessProcessProperties]
    ChildObjects: Optional[BusinessProcessChildObjects]

class CalculationRegisterProperties(XMLData):
    Name:                     Optional[str]
    Synonym:                  Optional[LocalStringType]
    Comment:                  Optional[str]
    UseStandardCommands:      Optional[enums.Bool]
    DefaultListForm:          Optional[MDObjectRef]
    AuxiliaryListForm:        Optional[MDObjectRef]
    Periodicity:              Optional[enums.CalculationRegisterPeriodicity]
    ActionPeriod:             Optional[enums.Bool]
    BasePeriod:               Optional[enums.Bool]
    Schedule:                 Optional[MDObjectRef]
    ScheduleValue:            Optional[MDObjectRef]
    ScheduleDate:             Optional[MDObjectRef]
    ChartOfCalculationTypes:  Optional[MDObjectRef]
    IncludeHelpInContents:    Optional[enums.Bool]
    StandardAttributes:       Optional[StandardAttributes]
    DataLockControlMode:      Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:           Optional[enums.FullTextSearchUsing]
    ListPresentation:         Optional[LocalStringType]
    ExtendedListPresentation: Optional[LocalStringType]
    Explanation:              Optional[LocalStringType]

class CalculationRegisterChildObjects(XMLData):
    Resource:      List[Resource]
    Attribute:     List[Attribute]
    Dimension:     List[Dimension]
    Recalculation: List[str]
    Form:          List[str]
    Template:      List[str]
    Command:       List[Command]

class CalculationRegister(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[CalculationRegisterProperties]
    ChildObjects: Optional[CalculationRegisterChildObjects]

class CatalogProperties(XMLData):
    Name:                             Optional[str]
    Synonym:                          Optional[LocalStringType]
    Comment:                          Optional[str]
    Hierarchical:                     Optional[enums.Bool]
    HierarchyType:                    Optional[enums.HierarchyType]
    LimitLevelCount:                  Optional[enums.Bool]
    LevelCount:                       Optional[Decimal]
    FoldersOnTop:                     Optional[enums.Bool]
    UseStandardCommands:              Optional[enums.Bool]
    Owners:                           Optional[MDListType]
    SubordinationUse:                 Optional[enums.SubordinationUse]
    CodeLength:                       Optional[Decimal]
    DescriptionLength:                Optional[Decimal]
    CodeType:                         Optional[enums.CatalogCodeType]
    CodeAllowedLength:                Optional[enums.AllowedLength]
    CodeSeries:                       Optional[enums.CatalogCodesSeries]
    CheckUnique:                      Optional[enums.Bool]
    Autonumbering:                    Optional[enums.Bool]
    DefaultPresentation:              Optional[enums.CatalogMainPresentation]
    StandardAttributes:               Optional[StandardAttributes]
    Characteristics:                  Optional[Characteristics]
    PredefinedDataUpdate:             Optional[enums.PredefinedDataUpdate]
    EditType:                         Optional[enums.EditType]
    QuickChoice:                      Optional[enums.Bool]
    ChoiceMode:                       Optional[enums.ChoiceMode]
    InputByString:                    Optional[FieldList]
    SearchStringModeOnInputByString:  Optional[enums.SearchStringModeOnInputByString]
    FullTextSearchOnInputByString:    Optional[enums.FullTextSearchOnInputByString]
    ChoiceDataGetModeOnInputByString: Optional[enums.ChoiceDataGetModeOnInputByString]
    DefaultObjectForm:                Optional[MDObjectRef]
    DefaultFolderForm:                Optional[MDObjectRef]
    DefaultListForm:                  Optional[MDObjectRef]
    DefaultChoiceForm:                Optional[MDObjectRef]
    DefaultFolderChoiceForm:          Optional[MDObjectRef]
    AuxiliaryObjectForm:              Optional[MDObjectRef]
    AuxiliaryFolderForm:              Optional[MDObjectRef]
    AuxiliaryListForm:                Optional[MDObjectRef]
    AuxiliaryChoiceForm:              Optional[MDObjectRef]
    AuxiliaryFolderChoiceForm:        Optional[MDObjectRef]
    IncludeHelpInContents:            Optional[enums.Bool]
    BasedOn:                          Optional[MDListType]
    DataLockFields:                   Optional[FieldList]
    DataLockControlMode:              Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:                   Optional[enums.FullTextSearchUsing]
    ObjectPresentation:               Optional[LocalStringType]
    ExtendedObjectPresentation:       Optional[LocalStringType]
    ListPresentation:                 Optional[LocalStringType]
    ExtendedListPresentation:         Optional[LocalStringType]
    Explanation:                      Optional[LocalStringType]
    CreateOnInput:                    Optional[enums.CreateOnInput]
    ChoiceHistoryOnInput:             Optional[enums.ChoiceHistoryOnInput]
    DataHistory:                      Optional[enums.DataHistoryUse]

class CatalogChildObjects(XMLData):
    Attribute:      List[Attribute]
    TabularSection: List[TabularSection]
    Form:           List[str]
    Template:       List[str]
    Command:        List[Command]

class Catalog(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[CatalogProperties]
    ChildObjects: Optional[CatalogChildObjects]

class ChartOfAccountsProperties(XMLData):
    Name:                             Optional[str]
    Synonym:                          Optional[LocalStringType]
    Comment:                          Optional[str]
    UseStandardCommands:              Optional[enums.Bool]
    IncludeHelpInContents:            Optional[enums.Bool]
    BasedOn:                          Optional[MDListType]
    ExtDimensionTypes:                Optional[MDObjectRef]
    MaxExtDimensionCount:             Optional[Decimal]
    CodeMask:                         Optional[str]
    CodeLength:                       Optional[Decimal]
    DescriptionLength:                Optional[Decimal]
    CodeSeries:                       Optional[enums.CharOfAccountCodeSeries]
    CheckUnique:                      Optional[enums.Bool]
    DefaultPresentation:              Optional[enums.AccountMainPresentation]
    StandardAttributes:               Optional[StandardAttributes]
    Characteristics:                  Optional[Characteristics]
    StandardTabularSections:          Optional[StandardTabularSections]
    PredefinedDataUpdate:             Optional[enums.PredefinedDataUpdate]
    EditType:                         Optional[enums.EditType]
    QuickChoice:                      Optional[enums.Bool]
    ChoiceMode:                       Optional[enums.ChoiceMode]
    InputByString:                    Optional[FieldList]
    SearchStringModeOnInputByString:  Optional[enums.SearchStringModeOnInputByString]
    FullTextSearchOnInputByString:    Optional[enums.FullTextSearchOnInputByString]
    ChoiceDataGetModeOnInputByString: Optional[enums.ChoiceDataGetModeOnInputByString]
    CreateOnInput:                    Optional[enums.CreateOnInput]
    ChoiceHistoryOnInput:             Optional[enums.ChoiceHistoryOnInput]
    DefaultObjectForm:                Optional[MDObjectRef]
    DefaultListForm:                  Optional[MDObjectRef]
    DefaultChoiceForm:                Optional[MDObjectRef]
    AuxiliaryObjectForm:              Optional[MDObjectRef]
    AuxiliaryListForm:                Optional[MDObjectRef]
    AuxiliaryChoiceForm:              Optional[MDObjectRef]
    AutoOrderByCode:                  Optional[enums.Bool]
    OrderLength:                      Optional[Decimal]
    DataLockFields:                   Optional[FieldList]
    DataLockControlMode:              Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:                   Optional[enums.FullTextSearchUsing]
    ObjectPresentation:               Optional[LocalStringType]
    ExtendedObjectPresentation:       Optional[LocalStringType]
    ListPresentation:                 Optional[LocalStringType]
    ExtendedListPresentation:         Optional[LocalStringType]
    Explanation:                      Optional[LocalStringType]

class ChartOfAccountsChildObjects(XMLData):
    Attribute:                  List[Attribute]
    TabularSection:             List[TabularSection]
    AccountingFlag:             List[AccountingFlag]
    ExtDimensionAccountingFlag: List[ExtDimensionAccountingFlag]
    Form:                       List[str]
    Template:                   List[str]
    Command:                    List[Command]

class ChartOfAccounts(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[ChartOfAccountsProperties]
    ChildObjects: Optional[ChartOfAccountsChildObjects]

class ChartOfCalculationTypesProperties(XMLData):
    Name:                             Optional[str]
    Synonym:                          Optional[LocalStringType]
    Comment:                          Optional[str]
    UseStandardCommands:              Optional[enums.Bool]
    CodeLength:                       Optional[Decimal]
    DescriptionLength:                Optional[Decimal]
    CodeType:                         Optional[enums.ChartOfCalculationTypesCodeType]
    CodeAllowedLength:                Optional[enums.AllowedLength]
    DefaultPresentation:              Optional[enums.CalculationTypeMainPresentation]
    EditType:                         Optional[enums.EditType]
    QuickChoice:                      Optional[enums.Bool]
    ChoiceMode:                       Optional[enums.ChoiceMode]
    InputByString:                    Optional[FieldList]
    SearchStringModeOnInputByString:  Optional[enums.SearchStringModeOnInputByString]
    FullTextSearchOnInputByString:    Optional[enums.FullTextSearchOnInputByString]
    ChoiceDataGetModeOnInputByString: Optional[enums.ChoiceDataGetModeOnInputByString]
    CreateOnInput:                    Optional[enums.CreateOnInput]
    ChoiceHistoryOnInput:             Optional[enums.ChoiceHistoryOnInput]
    DefaultObjectForm:                Optional[MDObjectRef]
    DefaultListForm:                  Optional[MDObjectRef]
    DefaultChoiceForm:                Optional[MDObjectRef]
    AuxiliaryObjectForm:              Optional[MDObjectRef]
    AuxiliaryListForm:                Optional[MDObjectRef]
    AuxiliaryChoiceForm:              Optional[MDObjectRef]
    BasedOn:                          Optional[MDListType]
    DependenceOnCalculationTypes:     Optional[enums.ChartOfCalculationTypesBaseUse]
    BaseCalculationTypes:             Optional[MDListType]
    ActionPeriodUse:                  Optional[enums.Bool]
    StandardAttributes:               Optional[StandardAttributes]
    Characteristics:                  Optional[Characteristics]
    StandardTabularSections:          Optional[StandardTabularSections]
    PredefinedDataUpdate:             Optional[enums.PredefinedDataUpdate]
    IncludeHelpInContents:            Optional[enums.Bool]
    DataLockFields:                   Optional[FieldList]
    DataLockControlMode:              Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:                   Optional[enums.FullTextSearchUsing]
    ObjectPresentation:               Optional[LocalStringType]
    ExtendedObjectPresentation:       Optional[LocalStringType]
    ListPresentation:                 Optional[LocalStringType]
    ExtendedListPresentation:         Optional[LocalStringType]
    Explanation:                      Optional[LocalStringType]

class ChartOfCalculationTypesChildObjects(XMLData):
    Attribute:      List[Attribute]
    TabularSection: List[TabularSection]
    Form:           List[str]
    Template:       List[str]
    Command:        List[Command]

class ChartOfCalculationTypes(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[ChartOfCalculationTypesProperties]
    ChildObjects: Optional[ChartOfCalculationTypesChildObjects]

class ChartOfCharacteristicTypesProperties(XMLData):
    Name:                             Optional[str]
    Synonym:                          Optional[LocalStringType]
    Comment:                          Optional[str]
    UseStandardCommands:              Optional[enums.Bool]
    IncludeHelpInContents:            Optional[enums.Bool]
    CharacteristicExtValues:          Optional[MDObjectRef]
    Type:                             Optional[TypeDescription]
    Hierarchical:                     Optional[enums.Bool]
    FoldersOnTop:                     Optional[enums.Bool]
    CodeLength:                       Optional[Decimal]
    CodeAllowedLength:                Optional[enums.AllowedLength]
    DescriptionLength:                Optional[Decimal]
    CodeSeries:                       Optional[enums.CharacteristicKindCodesSeries]
    CheckUnique:                      Optional[enums.Bool]
    Autonumbering:                    Optional[enums.Bool]
    DefaultPresentation:              Optional[enums.CharacteristicTypeMainPresentation]
    StandardAttributes:               Optional[StandardAttributes]
    Characteristics:                  Optional[Characteristics]
    PredefinedDataUpdate:             Optional[enums.PredefinedDataUpdate]
    EditType:                         Optional[enums.EditType]
    QuickChoice:                      Optional[enums.Bool]
    ChoiceMode:                       Optional[enums.ChoiceMode]
    InputByString:                    Optional[FieldList]
    CreateOnInput:                    Optional[enums.CreateOnInput]
    SearchStringModeOnInputByString:  Optional[enums.SearchStringModeOnInputByString]
    ChoiceDataGetModeOnInputByString: Optional[enums.ChoiceDataGetModeOnInputByString]
    FullTextSearchOnInputByString:    Optional[enums.FullTextSearchOnInputByString]
    ChoiceHistoryOnInput:             Optional[enums.ChoiceHistoryOnInput]
    DefaultObjectForm:                Optional[MDObjectRef]
    DefaultFolderForm:                Optional[MDObjectRef]
    DefaultListForm:                  Optional[MDObjectRef]
    DefaultChoiceForm:                Optional[MDObjectRef]
    DefaultFolderChoiceForm:          Optional[MDObjectRef]
    AuxiliaryObjectForm:              Optional[MDObjectRef]
    AuxiliaryFolderForm:              Optional[MDObjectRef]
    AuxiliaryListForm:                Optional[MDObjectRef]
    AuxiliaryChoiceForm:              Optional[MDObjectRef]
    AuxiliaryFolderChoiceForm:        Optional[MDObjectRef]
    BasedOn:                          Optional[MDListType]
    DataLockFields:                   Optional[FieldList]
    DataLockControlMode:              Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:                   Optional[enums.FullTextSearchUsing]
    ObjectPresentation:               Optional[LocalStringType]
    ExtendedObjectPresentation:       Optional[LocalStringType]
    ListPresentation:                 Optional[LocalStringType]
    ExtendedListPresentation:         Optional[LocalStringType]
    Explanation:                      Optional[LocalStringType]

class ChartOfCharacteristicTypesChildObjects(XMLData):
    Attribute:      List[Attribute]
    TabularSection: List[TabularSection]
    Form:           List[str]
    Template:       List[str]
    Command:        List[Command]

class ChartOfCharacteristicTypes(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[ChartOfCharacteristicTypesProperties]
    ChildObjects: Optional[ChartOfCharacteristicTypesChildObjects]

class CommandGroupProperties(XMLData):
    Name:           Optional[str]
    Synonym:        Optional[LocalStringType]
    Comment:        Optional[str]
    Representation: Optional[enums.ButtonRepresentation]
    ToolTip:        Optional[LocalStringType]
    Category:       Optional[enums.CommandGroupCategory]
    #Picture

class CommandGroup(XMLData):
    uuid:       Optional[str]
    Properties: Optional[CommandGroupProperties]

class CommonAttributeProperties(XMLData):
    Name:                              Optional[str]
    Synonym:                           Optional[LocalStringType]
    Comment:                           Optional[str]
    Type:                              Optional[TypeDescription]
    PasswordMode:                      Optional[enums.Bool]
    Format:                            Optional[LocalStringType]
    EditFormat:                        Optional[LocalStringType]
    ToolTip:                           Optional[LocalStringType]
    MarkNegatives:                     Optional[enums.Bool]
    Mask:                              Optional[str]
    MultiLine:                         Optional[enums.Bool]
    ExtendedEdit:                      Optional[enums.Bool]
    FillFromFillingValue:              Optional[enums.Bool]
    FillValue:                         Optional[FillValue]
    FillChecking:                      Optional[enums.FillChecking]
    ChoiceFoldersAndItems:             Optional[enums.FoldersAndItemsUse]
    ChoiceParameterLinks:              Optional[ChoiceParameterLinks]
    QuickChoice:                       Optional[enums.UseQuickChoice]
    CreateOnInput:                     Optional[enums.CreateOnInput]
    ChoiceForm:                        Optional[MDObjectRef]
    LinkByType:                        Optional[TypeLink]
    ChoiceHistoryOnInput:              Optional[enums.ChoiceHistoryOnInput]
    AutoUse:                           Optional[enums.CommonAttributeAutoUse]
    DataSeparation:                    Optional[enums.CommonAttributeDataSeparation]
    SeparatedDataUse:                  Optional[enums.CommonAttributeSeparatedDataUse]
    DataSeparationValue:               Optional[MDObjectRef]
    DataSeparationUse:                 Optional[MDObjectRef]
    ConditionalSeparation:             Optional[MDObjectRef]
    UsersSeparation:                   Optional[enums.CommonAttributeUsersSeparation]
    AuthenticationSeparation:          Optional[enums.CommonAttributeAuthenticationSeparation]
    ConfigurationExtensionsSeparation: Optional[enums.CommonAttributeConfigurationExtensionsSeparation]
    Indexing:                          Optional[enums.Indexing]
    FullTextSearch:                    Optional[enums.FullTextSearchUsing]
    DataHistory:                       Optional[enums.DataHistoryUse]
    #MinValue
    #MaxValue
    #ChoiceParameters
    #Content  CommonAttributeContent

class CommonAttribute(XMLData):
    uuid:       Optional[str]
    Properties: Optional[CommonAttributeProperties]

class CommonCommandProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    Representation:        Optional[enums.ButtonRepresentation]
    ToolTip:               Optional[LocalStringType]
    IncludeHelpInContents: Optional[enums.Bool]
    CommandParameterType:  Optional[TypeDescription]
    ParameterUseMode:      Optional[enums.CommandParameterUseMode]
    ModifiesData:          Optional[enums.Bool]
    #Group  IncludeInCommandCategoriesType
    #Picture
    #Shortcut

class CommonCommand(XMLData):
    uuid:       Optional[str]
    Properties: Optional[CommonCommandProperties]

class CommonFormProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    FormType:              Optional[enums.FormType]
    IncludeHelpInContents: Optional[enums.Bool]
    UseStandardCommands:   Optional[enums.Bool]
    ExtendedPresentation:  Optional[LocalStringType]
    Explanation:           Optional[LocalStringType]
    #UsePurposes  "FixedArray"

class CommonForm(XMLData):
    uuid:       Optional[str]
    Properties: Optional[CommonFormProperties]

class CommonModuleProperties(XMLData):
    Name:                      Optional[str]
    Synonym:                   Optional[LocalStringType]
    Comment:                   Optional[str]
    Global:                    Optional[enums.Bool]
    ClientManagedApplication:  Optional[enums.Bool]
    Server:                    Optional[enums.Bool]
    ExternalConnection:        Optional[enums.Bool]
    ClientOrdinaryApplication: Optional[enums.Bool]
    Client:                    Optional[enums.Bool]
    ServerCall:                Optional[enums.Bool]
    Privileged:                Optional[enums.Bool]
    ReturnValuesReuse:         Optional[enums.ReturnValuesReuse]

    def visit(self, visitor: Visitor):
        visitor.visit_CommonModuleProperties(self)
        if self.Synonym is not None:
            self.Synonym.visit(visitor)
        visitor.leave_CommonModuleProperties(self)

class CommonModule(XMLFile):
    uuid:       Optional[str]
    Properties: Optional[CommonModuleProperties]

    def visit(self, visitor: Visitor):
        visitor.visit_CommonModule(self)
        if self.Properties is not None:
            self.Properties.visit(visitor)
        visitor.leave_CommonModule(self)

class CommonPictureProperties(XMLData):
    Name:    Optional[str]
    Synonym: Optional[LocalStringType]
    Comment: Optional[str]

class CommonPicture(XMLData):
    uuid:       Optional[str]
    Properties: Optional[CommonPictureProperties]

class CommonTemplateProperties(XMLData):
    Name:         Optional[str]
    Synonym:      Optional[LocalStringType]
    Comment:      Optional[str]
    TemplateType: Optional[enums.TemplateType]

class CommonTemplate(XMLData):
    uuid:         Optional[str]
    Properties: Optional[CommonTemplateProperties]

class ConfigurationProperties(XMLData):
    Name:                                            Optional[str]
    Synonym:                                         Optional[LocalStringType]
    Comment:                                         Optional[str]
    NamePrefix:                                      Optional[str]
    ConfigurationExtensionCompatibilityMode:         Optional[enums.CompatibilityMode]
    DefaultRunMode:                                  Optional[enums.ClientRunMode]
    ScriptVariant:                                   Optional[enums.ScriptVariant]
    DefaultRoles:                                    Optional[MDListType]
    Vendor:                                          Optional[str]
    Version:                                         Optional[str]
    UpdateCatalogAddress:                            Optional[str]
    IncludeHelpInContents:                           Optional[enums.Bool]
    UseManagedFormInOrdinaryApplication:             Optional[enums.Bool]
    UseOrdinaryFormInManagedApplication:             Optional[enums.Bool]
    AdditionalFullTextSearchDictionaries:            Optional[MDListType]
    CommonSettingsStorage:                           Optional[MDObjectRef]
    ReportsUserSettingsStorage:                      Optional[MDObjectRef]
    ReportsVariantsStorage:                          Optional[MDObjectRef]
    FormDataSettingsStorage:                         Optional[MDObjectRef]
    DynamicListsUserSettingsStorage:                 Optional[MDObjectRef]
    Content:                                         Optional[MDListType]
    DefaultReportForm:                               Optional[MDObjectRef]
    DefaultReportVariantForm:                        Optional[MDObjectRef]
    DefaultReportSettingsForm:                       Optional[MDObjectRef]
    DefaultDynamicListSettingsForm:                  Optional[MDObjectRef]
    DefaultSearchForm:                               Optional[MDObjectRef]
    MainClientApplicationWindowMode:                 Optional[enums.MainClientApplicationWindowMode]
    DefaultInterface:                                Optional[MDObjectRef]
    DefaultStyle:                                    Optional[MDObjectRef]
    DefaultLanguage:                                 Optional[MDObjectRef]
    BriefInformation:                                Optional[LocalStringType]
    DetailedInformation:                             Optional[LocalStringType]
    Copyright:                                       Optional[LocalStringType]
    VendorInformationAddress:                        Optional[LocalStringType]
    ConfigurationInformationAddress:                 Optional[LocalStringType]
    DataLockControlMode:                             Optional[enums.DefaultDataLockControlMode]
    ObjectAutonumerationMode:                        Optional[enums.ObjectAutonumerationMode]
    ModalityUseMode:                                 Optional[enums.ModalityUseMode]
    SynchronousPlatformExtensionAndAddInCallUseMode: Optional[enums.SynchronousPlatformExtensionAndAddInCallUseMode]
    InterfaceCompatibilityMode:                      Optional[enums.InterfaceCompatibilityMode]
    CompatibilityMode:                               Optional[enums.CompatibilityMode]
    DefaultConstantsForm:                            Optional[MDObjectRef]
    #UsePurposes  "FixedArray"
    #RequiredMobileApplicationPermissions  "FixedMap"

    def visit(self, visitor: Visitor):
        visitor.visit_ConfigurationProperties(self)
        if self.Synonym is not None:
            self.Synonym.visit(visitor)
        visitor.leave_ConfigurationProperties(self)

class ConfigurationChildObjects(XMLData):
    AccountingRegister:         List[str]
    AccumulationRegister:       List[str]
    BusinessProcess:            List[str]
    CalculationRegister:        List[str]
    Catalog:                    List[str]
    ChartOfAccounts:            List[str]
    ChartOfCalculationTypes:    List[str]
    ChartOfCharacteristicTypes: List[str]
    CommandGroup:               List[str]
    CommonAttribute:            List[str]
    CommonCommand:              List[str]
    CommonForm:                 List[str]
    CommonModule:               List[str]
    CommonPicture:              List[str]
    CommonTemplate:             List[str]
    Constant:                   List[str]
    DataProcessor:              List[str]
    DefinedType:                List[str]
    Document:                   List[str]
    DocumentJournal:            List[str]
    DocumentNumerator:          List[str]
    Enum:                       List[str]
    EventSubscription:          List[str]
    ExchangePlan:               List[str]
    ExternalDataSource:         List[str]
    FilterCriterion:            List[str]
    FunctionalOption:           List[str]
    FunctionalOptionsParameter: List[str]
    HTTPService:                List[str]
    InformationRegister:        List[str]
    Interface:                  List[str]
    Language:                   List[str]
    Report:                     List[str]
    Role:                       List[str]
    ScheduledJob:               List[str]
    Sequence:                   List[str]
    SessionParameter:           List[str]
    SettingsStorage:            List[str]
    Style:                      List[str]
    StyleItem:                  List[str]
    Subsystem:                  List[str]
    Task:                       List[str]
    WebService:                 List[str]
    WSReference:                List[str]
    XDTOPackage:                List[str]

class Configuration(XMLFile):
    uuid:         Optional[str]
    Properties:   Optional[ConfigurationProperties]
    ChildObjects: Optional[ConfigurationChildObjects]

    def walk(self, visitor: Visitor):

        if self.Properties is not None:
            self.Properties.visit(visitor)

        dirname = os.path.dirname(self._path)

        if self.ChildObjects is not None:

            # CommonModules

            names = self.ChildObjects.CommonModule
            if names is not None:
                subdirname = os.path.join(dirname, 'CommonModules')
                for name in names:
                    path = os.path.join(subdirname, name + '.xml')
                    node: Root = XMLParser(path, Root).parse()
                    mdo: Optional[MetaDataObject] = node.MetaDataObject
                    if mdo is not None and mdo.CommonModule is not None:
                        mdo.CommonModule.walk(visitor)


    def visit(self, visitor: Visitor):
        visitor.visit_Configuration(self)
        if self.Properties is not None:
            self.Properties.visit(visitor)
        visitor.leave_Configuration(self)

class ConstantProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    Type:                  Optional[TypeDescription]
    UseStandardCommands:   Optional[enums.Bool]
    DefaultForm:           Optional[MDObjectRef]
    ExtendedPresentation:  Optional[LocalStringType]
    Explanation:           Optional[LocalStringType]
    PasswordMode:          Optional[enums.Bool]
    Format:                Optional[LocalStringType]
    EditFormat:            Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    MarkNegatives:         Optional[enums.Bool]
    Mask:                  Optional[str]
    MultiLine:             Optional[enums.Bool]
    ExtendedEdit:          Optional[enums.Bool]
    FillChecking:          Optional[enums.FillChecking]
    ChoiceFoldersAndItems: Optional[enums.FoldersAndItemsUse]
    ChoiceParameterLinks:  Optional[ChoiceParameterLinks]
    QuickChoice:           Optional[enums.UseQuickChoice]
    ChoiceForm:            Optional[MDObjectRef]
    LinkByType:            Optional[TypeLink]
    ChoiceHistoryOnInput:  Optional[enums.ChoiceHistoryOnInput]
    DataLockControlMode:   Optional[enums.DefaultDataLockControlMode]
    #MinValue
    #MaxValue
    #ChoiceParameters

class Constant(XMLData):
    uuid:       Optional[str]
    Properties: Optional[ConstantProperties]

class DataProcessorProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    UseStandardCommands:   Optional[enums.Bool]
    DefaultForm:           Optional[MDObjectRef]
    AuxiliaryForm:         Optional[MDObjectRef]
    IncludeHelpInContents: Optional[enums.Bool]
    ExtendedPresentation:  Optional[LocalStringType]
    Explanation:           Optional[LocalStringType]

class DataProcessorChildObjects(XMLData):
    Attribute:      List[Attribute]
    TabularSection: List[TabularSection]
    Form:           List[str]
    Template:       List[str]
    Command:        List[Command]

class DataProcessor(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[DataProcessorProperties]
    ChildObjects: Optional[DataProcessorChildObjects]

class DocumentProperties(XMLData):
    Name:                             Optional[str]
    Synonym:                          Optional[LocalStringType]
    Comment:                          Optional[str]
    UseStandardCommands:              Optional[enums.Bool]
    Numerator:                        Optional[MDObjectRef]
    NumberType:                       Optional[enums.DocumentNumberType]
    NumberLength:                     Optional[Decimal]
    NumberAllowedLength:              Optional[enums.AllowedLength]
    NumberPeriodicity:                Optional[enums.DocumentNumberPeriodicity]
    CheckUnique:                      Optional[enums.Bool]
    Autonumbering:                    Optional[enums.Bool]
    StandardAttributes:               Optional[StandardAttributes]
    Characteristics:                  Optional[Characteristics]
    BasedOn:                          Optional[MDListType]
    InputByString:                    Optional[FieldList]
    CreateOnInput:                    Optional[enums.CreateOnInput]
    SearchStringModeOnInputByString:  Optional[enums.SearchStringModeOnInputByString]
    FullTextSearchOnInputByString:    Optional[enums.FullTextSearchOnInputByString]
    ChoiceDataGetModeOnInputByString: Optional[enums.ChoiceDataGetModeOnInputByString]
    DefaultObjectForm:                Optional[MDObjectRef]
    DefaultListForm:                  Optional[MDObjectRef]
    DefaultChoiceForm:                Optional[MDObjectRef]
    AuxiliaryObjectForm:              Optional[MDObjectRef]
    AuxiliaryListForm:                Optional[MDObjectRef]
    AuxiliaryChoiceForm:              Optional[MDObjectRef]
    Posting:                          Optional[enums.Posting]
    RealTimePosting:                  Optional[enums.RealTimePosting]
    RegisterRecordsDeletion:          Optional[enums.RegisterRecordsDeletion]
    RegisterRecordsWritingOnPost:     Optional[enums.RegisterRecordsWritingOnPost]
    SequenceFilling:                  Optional[enums.SequenceFilling]
    RegisterRecords:                  Optional[MDListType]
    PostInPrivilegedMode:             Optional[enums.Bool]
    UnpostInPrivilegedMode:           Optional[enums.Bool]
    IncludeHelpInContents:            Optional[enums.Bool]
    DataLockFields:                   Optional[FieldList]
    DataLockControlMode:              Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:                   Optional[enums.FullTextSearchUsing]
    ObjectPresentation:               Optional[LocalStringType]
    ExtendedObjectPresentation:       Optional[LocalStringType]
    ListPresentation:                 Optional[LocalStringType]
    ExtendedListPresentation:         Optional[LocalStringType]
    Explanation:                      Optional[LocalStringType]
    ChoiceHistoryOnInput:             Optional[enums.ChoiceHistoryOnInput]
    DataHistory:                      Optional[enums.DataHistoryUse]

class DocumentChildObjects(XMLData):
    Attribute:      List[Attribute]
    Form:           List[str]
    TabularSection: List[TabularSection]
    Template:       List[str]
    Command:        List[Command]

class Document(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[DocumentProperties]
    ChildObjects: Optional[DocumentChildObjects]

class DocumentJournalProperties(XMLData):
    Name:                     Optional[str]
    Synonym:                  Optional[LocalStringType]
    Comment:                  Optional[str]
    DefaultForm:              Optional[MDObjectRef]
    AuxiliaryForm:            Optional[MDObjectRef]
    UseStandardCommands:      Optional[enums.Bool]
    RegisteredDocuments:      Optional[MDListType]
    IncludeHelpInContents:    Optional[enums.Bool]
    StandardAttributes:       Optional[StandardAttributes]
    ListPresentation:         Optional[LocalStringType]
    ExtendedListPresentation: Optional[LocalStringType]
    Explanation:              Optional[LocalStringType]

class DocumentJournalChildObjects(XMLData):
    Column:   List[Column]
    Form:     List[str]
    Template: List[str]
    Command:  List[Command]

class DocumentJournal(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[DocumentJournalProperties]
    ChildObjects: Optional[DocumentJournalChildObjects]

class DocumentNumeratorProperties(XMLData):
    Name:                Optional[str]
    Synonym:             Optional[LocalStringType]
    Comment:             Optional[str]
    NumberType:          Optional[enums.DocumentNumberType]
    NumberLength:        Optional[Decimal]
    NumberAllowedLength: Optional[enums.AllowedLength]
    NumberPeriodicity:   Optional[enums.DocumentNumberPeriodicity]
    CheckUnique:         Optional[enums.Bool]

class DocumentNumerator(XMLData):
    uuid:       Optional[str]
    Properties: Optional[DocumentNumeratorProperties]

class EnumProperties(XMLData):
    Name:                     Optional[str]
    Synonym:                  Optional[LocalStringType]
    Comment:                  Optional[str]
    UseStandardCommands:      Optional[enums.Bool]
    StandardAttributes:       Optional[StandardAttributes]
    Characteristics:          Optional[Characteristics]
    QuickChoice:              Optional[enums.Bool]
    ChoiceMode:               Optional[enums.ChoiceMode]
    DefaultListForm:          Optional[MDObjectRef]
    DefaultChoiceForm:        Optional[MDObjectRef]
    AuxiliaryListForm:        Optional[MDObjectRef]
    AuxiliaryChoiceForm:      Optional[MDObjectRef]
    ListPresentation:         Optional[LocalStringType]
    ExtendedListPresentation: Optional[LocalStringType]
    Explanation:              Optional[LocalStringType]
    ChoiceHistoryOnInput:     Optional[enums.ChoiceHistoryOnInput]

class EnumChildObjects(XMLData):
    EnumValue: List[EnumValue]
    Form:      List[str]
    Template:  List[str]
    Command:   List[Command]

class Enum(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[EnumProperties]
    ChildObjects: Optional[EnumChildObjects]

class EventSubscriptionProperties(XMLData):
    Name:    Optional[str]
    Synonym: Optional[LocalStringType]
    Comment: Optional[str]
    Source:  Optional[TypeDescription]
    Handler: Optional[MDMethodRef]
    #Event  AliasedStringType

class EventSubscription(XMLData):
    uuid:       Optional[str]
    Properties: Optional[EventSubscriptionProperties]

class ExchangePlanProperties(XMLData):
    Name:                             Optional[str]
    Synonym:                          Optional[LocalStringType]
    Comment:                          Optional[str]
    UseStandardCommands:              Optional[enums.Bool]
    CodeLength:                       Optional[Decimal]
    CodeAllowedLength:                Optional[enums.AllowedLength]
    DescriptionLength:                Optional[Decimal]
    DefaultPresentation:              Optional[enums.DataExchangeMainPresentation]
    EditType:                         Optional[enums.EditType]
    QuickChoice:                      Optional[enums.Bool]
    ChoiceMode:                       Optional[enums.ChoiceMode]
    InputByString:                    Optional[FieldList]
    SearchStringModeOnInputByString:  Optional[enums.SearchStringModeOnInputByString]
    FullTextSearchOnInputByString:    Optional[enums.FullTextSearchOnInputByString]
    ChoiceDataGetModeOnInputByString: Optional[enums.ChoiceDataGetModeOnInputByString]
    DefaultObjectForm:                Optional[MDObjectRef]
    DefaultListForm:                  Optional[MDObjectRef]
    DefaultChoiceForm:                Optional[MDObjectRef]
    AuxiliaryObjectForm:              Optional[MDObjectRef]
    AuxiliaryListForm:                Optional[MDObjectRef]
    AuxiliaryChoiceForm:              Optional[MDObjectRef]
    StandardAttributes:               Optional[StandardAttributes]
    Characteristics:                  Optional[Characteristics]
    BasedOn:                          Optional[MDListType]
    DistributedInfoBase:              Optional[enums.Bool]
    CreateOnInput:                    Optional[enums.CreateOnInput]
    ChoiceHistoryOnInput:             Optional[enums.ChoiceHistoryOnInput]
    IncludeHelpInContents:            Optional[enums.Bool]
    DataLockFields:                   Optional[FieldList]
    DataLockControlMode:              Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:                   Optional[enums.FullTextSearchUsing]
    ObjectPresentation:               Optional[LocalStringType]
    ExtendedObjectPresentation:       Optional[LocalStringType]
    ListPresentation:                 Optional[LocalStringType]
    ExtendedListPresentation:         Optional[LocalStringType]
    Explanation:                      Optional[LocalStringType]

class ExchangePlanChildObjects(XMLData):
    Attribute:      List[Attribute]
    TabularSection: List[TabularSection]
    Form:           List[str]
    Template:       List[str]
    Command:        List[Command]

class ExchangePlan(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[ExchangePlanProperties]
    ChildObjects: Optional[ExchangePlanChildObjects]

class FilterCriterionProperties(XMLData):
    Name:                     Optional[str]
    Synonym:                  Optional[LocalStringType]
    Comment:                  Optional[str]
    Type:                     Optional[TypeDescription]
    UseStandardCommands:      Optional[enums.Bool]
    Content:                  Optional[MDListType]
    DefaultForm:              Optional[MDObjectRef]
    AuxiliaryForm:            Optional[MDObjectRef]
    ListPresentation:         Optional[LocalStringType]
    ExtendedListPresentation: Optional[LocalStringType]
    Explanation:              Optional[LocalStringType]

class FilterCriterionChildObjects(XMLData):
    Form:    List[str]
    Command: List[Command]

class FilterCriterion(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[FilterCriterionProperties]
    ChildObjects: Optional[FilterCriterionChildObjects]

class FunctionalOptionProperties(XMLData):
    Name:              Optional[str]
    Synonym:           Optional[LocalStringType]
    Comment:           Optional[str]
    Location:          Optional[MDObjectRef]
    PrivilegedGetMode: Optional[enums.Bool]
    #Content  FuncOptionContentType

class FunctionalOption(XMLData):
    uuid:       Optional[str]
    Properties: Optional[FunctionalOptionProperties]

class FunctionalOptionsParameterProperties(XMLData):
    Name:    Optional[str]
    Synonym: Optional[LocalStringType]
    Comment: Optional[str]
    Use:     Optional[MDListType]

class FunctionalOptionsParameter(XMLData):
    uuid:       Optional[str]
    Properties: Optional[FunctionalOptionsParameterProperties]

class Method(XMLData):
    Name:     Optional[str]
    Synonym:  Optional[LocalStringType]
    Comment:  Optional[str]
    HTTPMethod: Optional[enums.HTTPMethod]

class URLTemplateChildObjects(XMLData):
    Method: List[Method]

class URLTemplateProperties(XMLData):
    Name:     Optional[str]
    Synonym:  Optional[LocalStringType]
    Comment:  Optional[str]
    Template: Optional[str]

class URLTemplate(XMLData):
    Properties:   Optional[URLTemplateProperties]
    ChildObjects: Optional[URLTemplateChildObjects]

class HTTPServiceProperties(XMLData):
    Name:          Optional[str]
    Synonym:       Optional[LocalStringType]
    Comment:       Optional[str]
    RootURL:       Optional[str]
    ReuseSessions: Optional[enums.SessionReuseMode]
    SessionMaxAge: Optional[Decimal]

class HTTPServiceChildObjects(XMLData):
    URLTemplate: List[URLTemplate]

class HTTPService(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[HTTPServiceProperties]
    ChildObjects: Optional[HTTPServiceChildObjects]

class InformationRegisterProperties(XMLData):
    Name:                           Optional[str]
    Synonym:                        Optional[LocalStringType]
    Comment:                        Optional[str]
    UseStandardCommands:            Optional[enums.Bool]
    EditType:                       Optional[enums.EditType]
    DefaultRecordForm:              Optional[MDObjectRef]
    DefaultListForm:                Optional[MDObjectRef]
    AuxiliaryRecordForm:            Optional[MDObjectRef]
    AuxiliaryListForm:              Optional[MDObjectRef]
    StandardAttributes:             Optional[StandardAttributes]
    InformationRegisterPeriodicity: Optional[enums.InformationRegisterPeriodicity]
    WriteMode:                      Optional[enums.RegisterWriteMode]
    MainFilterOnPeriod:             Optional[enums.Bool]
    IncludeHelpInContents:          Optional[enums.Bool]
    DataLockControlMode:            Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:                 Optional[enums.FullTextSearchUsing]
    EnableTotalsSliceFirst:         Optional[enums.Bool]
    EnableTotalsSliceLast:          Optional[enums.Bool]
    RecordPresentation:             Optional[LocalStringType]
    ExtendedRecordPresentation:     Optional[LocalStringType]
    ListPresentation:               Optional[LocalStringType]
    ExtendedListPresentation:       Optional[LocalStringType]
    Explanation:                    Optional[LocalStringType]
    DataHistory:                    Optional[enums.DataHistoryUse]

class InformationRegisterChildObjects(XMLData):
    Resource:  List[Resource]
    Attribute: List[Attribute]
    Dimension: List[Dimension]
    Form:      List[str]
    Template:  List[str]
    Command:   List[Command]

class InformationRegister(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[InformationRegisterProperties]
    ChildObjects: Optional[InformationRegisterChildObjects]

class LanguageProperties(XMLData):
    Name:         Optional[str]
    Synonym:      Optional[LocalStringType]
    Comment:      Optional[str]
    LanguageCode: Optional[str]

class Language(XMLData):
    uuid:       Optional[str]
    Properties: Optional[LanguageProperties]

class ReportProperties(XMLData):
    Name:                      Optional[str]
    Synonym:                   Optional[LocalStringType]
    Comment:                   Optional[str]
    UseStandardCommands:       Optional[enums.Bool]
    DefaultForm:               Optional[MDObjectRef]
    AuxiliaryForm:             Optional[MDObjectRef]
    MainDataCompositionSchema: Optional[MDObjectRef]
    DefaultSettingsForm:       Optional[MDObjectRef]
    AuxiliarySettingsForm:     Optional[MDObjectRef]
    DefaultVariantForm:        Optional[MDObjectRef]
    VariantsStorage:           Optional[MDObjectRef]
    SettingsStorage:           Optional[MDObjectRef]
    IncludeHelpInContents:     Optional[enums.Bool]
    ExtendedPresentation:      Optional[LocalStringType]
    Explanation:               Optional[LocalStringType]

class ReportChildObjects(XMLData):
    Attribute:      List[Attribute]
    TabularSection: List[TabularSection]
    Form:           List[str]
    Template:       List[str]
    Command:        List[Command]

class Report(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[ReportProperties]
    ChildObjects: Optional[ReportChildObjects]

class RoleProperties(XMLData):
    Name:    Optional[str]
    Synonym: Optional[LocalStringType]
    Comment: Optional[str]

class Role(XMLData):
    uuid:       Optional[str]
    Properties: Optional[RoleProperties]

class ScheduledJobProperties(XMLData):
    Name:                     Optional[str]
    Synonym:                  Optional[LocalStringType]
    Comment:                  Optional[str]
    MethodName:               Optional[MDMethodRef]
    Description:              Optional[str]
    Key:                      Optional[str]
    Use:                      Optional[enums.Bool]
    Predefined:               Optional[enums.Bool]
    RestartCountOnFailure:    Optional[Decimal]
    RestartIntervalOnFailure: Optional[Decimal]

class ScheduledJob(XMLData):
    uuid:       Optional[str]
    Properties: Optional[ScheduledJobProperties]

class SequenceProperties(XMLData):
    Name:                  Optional[str]
    Synonym:               Optional[LocalStringType]
    Comment:               Optional[str]
    MoveBoundaryOnPosting: Optional[enums.MoveBoundaryOnPosting]
    Documents:             Optional[MDListType]
    RegisterRecords:       Optional[MDListType]
    DataLockControlMode:   Optional[enums.DefaultDataLockControlMode]

class SequenceChildObjects(XMLData):
    Dimension: List[Dimension]

class Sequence(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[SequenceProperties]
    ChildObjects: Optional[SequenceChildObjects]

class SessionParameterProperties(XMLData):
    Name:    Optional[str]
    Synonym: Optional[LocalStringType]
    Comment: Optional[str]
    Type:    Optional[TypeDescription]

class SessionParameter(XMLData):
    uuid:         Optional[str]
    Properties: Optional[SessionParameterProperties]

class SettingsStorageProperties(XMLData):
    Name:              Optional[str]
    Synonym:           Optional[LocalStringType]
    Comment:           Optional[str]
    DefaultSaveForm:   Optional[MDObjectRef]
    DefaultLoadForm:   Optional[MDObjectRef]
    AuxiliarySaveForm: Optional[MDObjectRef]
    AuxiliaryLoadForm: Optional[MDObjectRef]

class SettingsStorageChildObjects(XMLData):
    Form:     List[str]
    Template: List[str]

class SettingsStorage(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[SettingsStorageProperties]
    ChildObjects: Optional[SettingsStorageChildObjects]

class SubsystemProperties(XMLData):
    Name:                      Optional[str]
    Synonym:                   Optional[LocalStringType]
    Comment:                   Optional[str]
    IncludeHelpInContents:     Optional[enums.Bool]
    IncludeInCommandInterface: Optional[enums.Bool]
    Explanation:               Optional[LocalStringType]
    Content:                   Optional[MDListType]
    #Picture

class SubsystemChildObjects(XMLData):
    Subsystem: List[str]

class Subsystem(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[SubsystemProperties]
    ChildObjects: Optional[SubsystemChildObjects]

class TaskProperties(XMLData):
    Name:                             Optional[str]
    Synonym:                          Optional[LocalStringType]
    Comment:                          Optional[str]
    UseStandardCommands:              Optional[enums.Bool]
    NumberType:                       Optional[enums.TaskNumberType]
    NumberLength:                     Optional[Decimal]
    NumberAllowedLength:              Optional[enums.AllowedLength]
    CheckUnique:                      Optional[enums.Bool]
    Autonumbering:                    Optional[enums.Bool]
    TaskNumberAutoPrefix:             Optional[enums.TaskNumberAutoPrefix]
    DescriptionLength:                Optional[Decimal]
    Addressing:                       Optional[MDObjectRef]
    MainAddressingAttribute:          Optional[MDObjectRef]
    CurrentPerformer:                 Optional[MDObjectRef]
    BasedOn:                          Optional[MDListType]
    StandardAttributes:               Optional[StandardAttributes]
    Characteristics:                  Optional[Characteristics]
    DefaultPresentation:              Optional[enums.TaskMainPresentation]
    EditType:                         Optional[enums.EditType]
    InputByString:                    Optional[FieldList]
    SearchStringModeOnInputByString:  Optional[enums.SearchStringModeOnInputByString]
    FullTextSearchOnInputByString:    Optional[enums.FullTextSearchOnInputByString]
    ChoiceDataGetModeOnInputByString: Optional[enums.ChoiceDataGetModeOnInputByString]
    CreateOnInput:                    Optional[enums.CreateOnInput]
    DefaultObjectForm:                Optional[MDObjectRef]
    DefaultListForm:                  Optional[MDObjectRef]
    DefaultChoiceForm:                Optional[MDObjectRef]
    AuxiliaryObjectForm:              Optional[MDObjectRef]
    AuxiliaryListForm:                Optional[MDObjectRef]
    AuxiliaryChoiceForm:              Optional[MDObjectRef]
    ChoiceHistoryOnInput:             Optional[enums.ChoiceHistoryOnInput]
    IncludeHelpInContents:            Optional[enums.Bool]
    DataLockFields:                   Optional[FieldList]
    DataLockControlMode:              Optional[enums.DefaultDataLockControlMode]
    FullTextSearch:                   Optional[enums.FullTextSearchUsing]
    ObjectPresentation:               Optional[LocalStringType]
    ExtendedObjectPresentation:       Optional[LocalStringType]
    ListPresentation:                 Optional[LocalStringType]
    ExtendedListPresentation:         Optional[LocalStringType]
    Explanation:                      Optional[LocalStringType]

class TaskChildObjects(XMLData):
    Attribute:           List[Attribute]
    TabularSection:      List[TabularSection]
    Form:                List[str]
    Template:            List[str]
    AddressingAttribute: List[AddressingAttribute]
    Command:             List[Command]

class Task(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[TaskProperties]
    ChildObjects: Optional[TaskChildObjects]

class ParameterProperties(XMLData):
    Name:              Optional[str]
    Synonym:           Optional[LocalStringType]
    Comment:           Optional[str]
    XDTOValueType:     Optional[QName]
    Nillable:          Optional[enums.Bool]
    TransferDirection: Optional[enums.TransferDirection]

class Parameter(XMLData):
    uuid:       Optional[str]
    Properties: Optional[ParameterProperties]

class OperationProperties(XMLData):
    Name:                   Optional[str]
    Synonym:                Optional[LocalStringType]
    Comment:                Optional[str]
    XDTOReturningValueType: Optional[QName]
    Nillable:               Optional[enums.Bool]
    Transactioned:          Optional[enums.Bool]
    ProcedureName:          Optional[str]

class OperationChildObjects(XMLData):
    Parameter: List[Parameter]

class Operation(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[OperationProperties]
    ChildObjects: Optional[OperationChildObjects]

class WebServiceProperties(XMLData):
    Name:               Optional[str]
    Synonym:            Optional[LocalStringType]
    Comment:            Optional[str]
    Namespace:          Optional[str]
    DescriptorFileName: Optional[str]
    ReuseSessions:      Optional[enums.SessionReuseMode]
    SessionMaxAge:      Optional[Decimal]
    #XDTOPackages  ValueList

class WebServiceChildObjects(XMLData):
    Operation: List[Operation]

class WebService(XMLData):
    uuid:         Optional[str]
    Properties:   Optional[WebServiceProperties]
    ChildObjects: Optional[WebServiceChildObjects]

class WSReferenceProperties(XMLData):
    Name:        Optional[str]
    Synonym:     Optional[LocalStringType]
    Comment:     Optional[str]
    LocationURL: Optional[str]

class WSReference(XMLData):
    uuid:       Optional[str]
    Properties: Optional[WSReferenceProperties]

class XDTOPackageProperties(XMLData):
    Name:      Optional[str]
    Synonym:   Optional[LocalStringType]
    Comment:   Optional[str]
    Namespace: Optional[str]

class XDTOPackage(XMLData):
    uuid:       Optional[str]
    Properties: Optional[XDTOPackageProperties]

class MetaDataObject(XMLData):
    version:                    Optional[Decimal]
    AccountingRegister:         Optional[AccountingRegister]
    AccumulationRegister:       Optional[AccumulationRegister]
    BusinessProcess:            Optional[BusinessProcess]
    CalculationRegister:        Optional[CalculationRegister]
    Catalog:                    Optional[Catalog]
    ChartOfAccounts:            Optional[ChartOfAccounts]
    ChartOfCalculationTypes:    Optional[ChartOfCalculationTypes]
    ChartOfCharacteristicTypes: Optional[ChartOfCharacteristicTypes]
    CommandGroup:               Optional[CommandGroup]
    CommonAttribute:            Optional[CommonAttribute]
    CommonCommand:              Optional[CommonCommand]
    CommonForm:                 Optional[CommonForm]
    CommonModule:               Optional[CommonModule]
    CommonPicture:              Optional[CommonPicture]
    CommonTemplate:             Optional[CommonTemplate]
    Configuration:              Optional[Configuration]
    Constant:                   Optional[Constant]
    DataProcessor:              Optional[DataProcessor]
    Document:                   Optional[Document]
    DocumentJournal:            Optional[DocumentJournal]
    DocumentNumerator:          Optional[DocumentNumerator]
    Enum:                       Optional[Enum]
    EventSubscription:          Optional[EventSubscription]
    ExchangePlan:               Optional[ExchangePlan]
    FilterCriterion:            Optional[FilterCriterion]
    Form:                       Optional[Form]
    FunctionalOption:           Optional[FunctionalOption]
    FunctionalOptionsParameter: Optional[FunctionalOptionsParameter]
    HTTPService:                Optional[HTTPService]
    InformationRegister:        Optional[InformationRegister]
    Language:                   Optional[Language]
    Report:                     Optional[Report]
    Role:                       Optional[Role]
    ScheduledJob:               Optional[ScheduledJob]
    Sequence:                   Optional[Sequence]
    SessionParameter:           Optional[SessionParameter]
    SettingsStorage:            Optional[SettingsStorage]
    Subsystem:                  Optional[Subsystem]
    Task:                       Optional[Task]
    Template:                   Optional[Template]
    WebService:                 Optional[WebService]
    WSReference:                Optional[WSReference]
    XDTOPackage:                Optional[XDTOPackage]

class Root(XMLFile):
    MetaDataObject: Optional[MetaDataObject]

#endregion meta

fill_types(globals())
