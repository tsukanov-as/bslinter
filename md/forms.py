# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import List, Optional
from decimal import Decimal
from enum import EnumMeta

from md.common import LocalStringType, LocalStringTypeItem, MDObjectRef, TypeDescription, ChoiceParameterLinks
from md.base import XMLData, XMLFile, OrderedXMLData, fill_types
import md.enums as enums
from md.visitor import Visitor, ModuleFile, ModuleKinds
import md.context as context

from bsl.ast import Item, GlobalObject, Env

import os.path

DateTime = str
FormItemRef = str
LFEDataPath  = str
base64Binary = str
Color = str
CommandSourceName = str

#region Other

class Font(XMLData):
    ref:       Optional[str] # StyleRef
    faceName:  Optional[str]
    height:    Optional[Decimal]
    bold:      Optional[enums.Bool]
    italic:    Optional[enums.Bool]
    underline: Optional[enums.Bool]
    strikeout: Optional[enums.Bool]
    kind:      Optional[enums.FontType]
    scale:     Optional[Decimal]


class Border(XMLData):
    ref:   Optional[str]  #StyleRef
    style: Optional[str]  #BorderType
    width: Optional[Decimal] #unsignedInt


class StandardPeriod(XMLData):
    variant:   Optional[enums.StandardPeriodVariant]
    startDate: Optional[DateTime]
    endDate:   Optional[DateTime]

class ValueListItem(XMLData):
    Presentation: Optional[str]
    CheckState:   Optional[Decimal]
    #Value ValueListItem

class ValueList(XMLData):
    Item: List[ValueListItem]


class FormattedStringType(XMLData):
    item:      List[LocalStringTypeItem]
    formatted: Optional[enums.Bool]


class Picture(XMLData):
    url: Optional[str]
    ref: Optional[str] #PictureRef
    t:   Optional[enums.Bool]
    tx:  Optional[Decimal]
    ty:  Optional[Decimal]
    gx:  Optional[Decimal]
    gy:  Optional[Decimal]
    gw:  Optional[Decimal]
    gh:  Optional[Decimal]
    _text:   Optional[base64Binary]


class ChoiceParameter(XMLData):  # TODO: сделать
    choiceParameter: Optional[str]
    #value ""; # ChoiceParameter()

class ChoiceParameters(XMLData):
    item: List[ChoiceParameter]


class ItemTypeLink(XMLData):
    DataPath: Optional[str]
    LinkItem: Optional[Decimal]

class AdjustableBooleanItemType(XMLData):
    name: Optional[MDObjectRef]
    _text:    Optional[enums.Bool]

class AdjustableBoolean(XMLData):
    Common: List[bool]
    Value:  List[AdjustableBooleanItemType]

class CommandsContent(XMLData):
    ExcludedCommand: List[str]

#endregion Other

#region Form

class AutoCommandBar(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    HorizontalAlign: Optional[enums.ItemHorizontalAlignment]
    Autofill:        Optional[enums.Bool]

class ContextMenu(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Autofill: Optional[enums.Bool]

class ManagedForm(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # this
    Title:                       Optional[LocalStringType]
    Width:                       Optional[Decimal]
    Height:                      Optional[Decimal]
    WindowOpeningMode:           Optional[enums.FormWindowOpeningMode]
    EnterKeyBehavior:            Optional[enums.FormEnterKeyBehavior]
    AutoSaveDataInSettings:      Optional[enums.AutoSaveFormDataInSettings]
    SaveDataInSettings:          Optional[enums.SaveFormDataInSettings]
    SettingsStorage:             Optional[MDObjectRef]
    AutoTitle:                   Optional[enums.Bool]
    AutoURL:                     Optional[enums.Bool]
    Group:                       Optional[enums.FormChildrenGroup]
    ChildrenAlign:               Optional[enums.FormChildrenAlign]
    HorizontalSpacing:           Optional[enums.FormItemSpacing]
    VerticalSpacing:             Optional[enums.FormItemSpacing]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    ChildItemsWidth:             Optional[enums.FormChildrenWidth]
    AutoFillCheck:               Optional[enums.Bool]
    Customizable:                Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    CommandBarLocation:          Optional[enums.FormElementCommandBarLocation]
    VerticalScroll:              Optional[enums.LogFormScrollMode]
    ScalingMode:                 Optional[enums.FormBaseFontVariant]
    Scale:                       Optional[Decimal]
    ConversationsRepresentation: Optional[enums.LogFormShowConversations]
    CommandSet:                  Optional[CommandsContent]
    ShowTitle:                   Optional[enums.Bool]
    ShowCloseButton:             Optional[enums.Bool]
    UseForFoldersAndItems:       Optional[enums.FoldersAndItemsUse]
    GroupList:                   Optional[FormItemRef]
    AutoTime:                    Optional[enums.AutoTimeMode]
    UsePostingMode:              Optional[enums.PostingModeUse]
    RepostOnWrite:               Optional[enums.Bool]
    ReportResult:                Optional[LFEDataPath]
    DetailsData:                 Optional[LFEDataPath]
    ReportFormType:              Optional[enums.ReportFormType]
    VariantAppearance:           Optional[LFEDataPath]
    AutoShowState:               Optional[enums.AutoShowStateMode]
    CustomSettingsFolder:        Optional[FormItemRef]
    Attributes:                  Optional['FormAttributes']
    Commands:                    Optional['FormCommands']
    Parameters:                  Optional['FormParameters']
    CommandInterface:            Optional['FormCommandInterface']
    #BaseForm Form

    _subnodes = [
        'Title',
        # ...
        'Attributes'
    ]

    def visit(self, visitor: Visitor):

        scope = visitor.open_scope()

        visitor.visit_ManagedForm(self)
        for name in self._subnodes:
            if node := getattr(self, name):
                node.visit(visitor)
        visitor.leave_ManagedForm(self)

        visitor.close_scope()

        module_dir = os.path.join(self._path.rsplit('.')[0]) # TODO: заменить на корректный код
        visitor.modules.append(
            ModuleFile(
                ModuleKinds.ManagedFormModule,
                os.path.join(module_dir, 'Module.bsl'),
                scope
            )
        )

#region Events

class FormItemEvent(XMLData):
    name:     Optional[str]
    callType: Optional[enums.HandlerCallType]
    _text:    Optional[str]

class FormItemEvents(XMLData):
    Event: List[FormItemEvent]

#endregion Events

#region Attributes

#region Columns

class FunctionalOptions(XMLData):
    Item: List[MDObjectRef]

class FormAttributeColumn(XMLData):
    name:              Optional[str]
    id:                Optional[Decimal]
    Title:             Optional[LocalStringType]
    View:              Optional[AdjustableBoolean]
    Edit:              Optional[AdjustableBoolean]
    FillCheck:         Optional[enums.FillChecking]
    FunctionalOptions: Optional[FunctionalOptions]

class FormAttributeAdditionalColumns(XMLData):
    table:  List[LFEDataPath]
    Column: List[FormAttributeColumn]

class FormAttributeColumns(XMLData):
    Column:            List[FormAttributeColumn]
    AdditionalColumns: List[FormAttributeAdditionalColumns]

#endregion Columns

class ContentType(XMLData):
    Field: List[LFEDataPath]

class FormAttribute(XMLData):
    name:              Optional[str]
    id:                Optional[Decimal]
    Type:              Optional[TypeDescription]
    Title:             Optional[LocalStringType]
    View:              Optional[AdjustableBoolean]
    Edit:              Optional[AdjustableBoolean]
    MainAttribute:     Optional[enums.Bool]
    SavedData:         Optional[enums.Bool]
    FillCheck:         Optional[enums.FillChecking]
    UseAlways:         Optional[ContentType]
    Save:              Optional[ContentType]
    FunctionalOptions: Optional[FunctionalOptions]
    Columns:           Optional[FormAttributeColumns]
    #Settings ""; # FormAttribute()

    _subnodes = [
        'Title',
    ]

    def visit(self, visitor: Visitor):

        if self.name:
            attribute = GlobalObject( # TODO: attribs?, methods?
                self.name,
                Env()
            )
            item = Item(self.name, attribute)
            visitor.scope.Vars[self.name.lower()] = item

        visitor.visit_FormAttribute(self)
        for name in self._subnodes:
            if node := getattr(self, name):
                node.visit(visitor)
        visitor.leave_FormAttribute(self)

class FormAttributes(XMLData):
    Attribute: List[FormAttribute]
    # Items["ConditionalAppearance"] = "ConditionalAppearance";

    def visit(self, visitor: Visitor):

        context.ClientApplicationForm.fill(visitor.scope)

        visitor.visit_FormAttributes(self)
        if self.Attribute:
            for node in self.Attribute:
                node.visit(visitor)
        visitor.leave_FormAttributes(self)

#endregion Attributes

#region Commands

class FormCommandAction(XMLData):
    callType: Optional[enums.HandlerCallType]
    _text:    Optional[str]

class FormCommand(XMLData):
    name:                     Optional[str]
    id:                       Optional[Decimal]
    Title:                    Optional[LocalStringType]
    ToolTip:                  Optional[LocalStringType]
    Use:                      Optional[AdjustableBoolean]
    Shortcut:                 Optional[str]
    Picture:                  Optional[Picture]
    Action:                   Optional[FormCommandAction]
    FunctionalOptions:        Optional[FunctionalOptions]
    Representation:           Optional[enums.DefaultRepresentation]
    ModifiesSavedData:        Optional[enums.Bool]
    CurrentRowUse:            Optional[enums.CurrentRowUse]
    AssociatedTableElementId: Optional[str] #Optional[Decimal]

class FormCommands(XMLData):
    Command: List[FormCommand]

#endregion Commands

#region CommandInterface

class FormCommandInterfaceItem(XMLData):
    Command:        Optional[str]
    Type:           Optional[enums.CommandKind]
    Attribute:      Optional[LFEDataPath]
    CommandGroup:   Optional[str]
    Index:          Optional[Decimal]
    DefaultVisible: Optional[enums.Bool]
    Visible:        Optional[AdjustableBoolean]

class FormCommandInterfaceItems(XMLData):
    Item: List[FormCommandInterfaceItem]

class FormCommandInterface(XMLData):
    NavigationPanel: Optional[FormCommandInterfaceItems]
    CommandBar:      Optional[FormCommandInterfaceItems]

#endregion CommandInterface

#region Parameters

class FormParameter(XMLData):
    name:         Optional[str]
    Type:         Optional[TypeDescription]
    KeyParameter: Optional[enums.Bool]

class FormParameters(XMLData):
    Parameter: List[FormParameter]

#endregion Parameters

#region Addition

class AdditionSource(XMLData):
    Item: Optional[str]
    Type: Optional[enums.LogFormElementAdditionKind]

class SearchControlAddition(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Addition
    Source:                Optional[AdditionSource]
    AdditionSource:        Optional[AdditionSource]
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    PlacementArea:         Optional[enums.MenuElementPlacementArea]
    Title:                 Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    HorizontalStretch: Optional[enums.BWAValue]
    BackColor:         Optional[Color]
    TextColor:         Optional[Color]
    BorderColor:       Optional[Color]
    Font:              Optional[Font]


class SearchStringAddition(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Addition
    Source:                Optional[AdditionSource]
    AdditionSource:        Optional[AdditionSource]
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    PlacementArea:         Optional[enums.MenuElementPlacementArea]
    Title:                 Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    HorizontalStretch: Optional[enums.BWAValue]
    BackColor:         Optional[Color]
    TextColor:         Optional[Color]
    BorderColor:       Optional[Color]
    Font:              Optional[Font]

class ViewStatusAddition(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Addition
    Source:                Optional[AdditionSource]
    AdditionSource:        Optional[AdditionSource]
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    PlacementArea:         Optional[enums.MenuElementPlacementArea]
    Title:                 Optional[LocalStringType]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Width:              Optional[Decimal]
    AutoMaxWidth:       Optional[enums.Bool]
    MaxWidth:           Optional[Decimal]
    MinWidth:           Optional[Decimal]
    HorizontalStretch:  Optional[enums.BWAValue]
    HorizontalLocation: Optional[enums.ItemHorizontalAlignment]
    BackColor:          Optional[Color]
    ButtonColor:        Optional[Color]
    TextColor:          Optional[Color]
    TitleTextColor:     Optional[Color]
    BorderColor:        Optional[Color]
    TitleFont:          Optional[Font]
    Font:               Optional[Font]
    Border:             Optional[Border]

#endregion Addition

#region ChildItems

class ChildItems(OrderedXMLData):
    """
    Экземпляры этого класса являются списками элементов.
    """
    AutoCommandBar:           Optional['AutoCommandBar']
    Button:                   Optional['Button']
    ButtonGroup:              Optional['ButtonGroup']
    CalendarField:            Optional['CalendarField']
    ChartField:               Optional['ChartField']
    CheckBoxField:            Optional['CheckBoxField']
    ColumnGroup:              Optional['ColumnGroup']
    CommandBar:               Optional['CommandBar']
    ContextMenu:              Optional['ContextMenu']
    DendrogramField:          Optional['DendrogramField']
    FormattedDocumentField:   Optional['FormattedDocumentField']
    GanttChartField:          Optional['GanttChartField']
    GeographicalSchemaField:  Optional['GeographicalSchemaField']
    GraphicalSchemaField:     Optional['GraphicalSchemaField']
    HTMLDocumentField:        Optional['HTMLDocumentField']
    InputField:               Optional['InputField']
    LabelDecoration:          Optional['LabelDecoration']
    LabelField:               Optional['LabelField']
    Page:                     Optional['Page']
    Pages:                    Optional['Pages']
    PeriodField:              Optional['PeriodField']
    PictureDecoration:        Optional['PictureDecoration']
    PictureField:             Optional['PictureField']
    PlannerField:             Optional['PlannerField']
    Popup:                    Optional['Popup']
    ProgressBarField:         Optional['ProgressBarField']
    RadioButtonField:         Optional['RadioButtonField']
    SearchControlAddition:    Optional['SearchControlAddition']
    SearchStringAddition:     Optional['SearchStringAddition']
    SpreadSheetDocumentField: Optional['SpreadSheetDocumentField']
    Table:                    Optional['Table']
    TextDocumentField:        Optional['TextDocumentField']
    TrackBarField:            Optional['TrackBarField']
    UsualGroup:               Optional['UsualGroup']
    ViewStatusAddition:       Optional['ViewStatusAddition']

class Button(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # this
    Type:                        Optional[enums.ManagedFormButtonType]
    DataPath:                    Optional[LFEDataPath]
    CommandName:                 Optional[str]
    UserVisible:                 Optional[AdjustableBoolean]
    Representation:              Optional[enums.ButtonRepresentation]
    DefaultButton:               Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Enabled:                     Optional[enums.Bool]
    DefaultItem:                 Optional[enums.Bool]
    OnlyInAllActions:            Optional[enums.BWAValue]
    Width:                       Optional[Decimal]
    AutoMaxWidth:                Optional[enums.Bool]
    MaxWidth:                    Optional[Decimal]
    MinWidth:                    Optional[Decimal]
    Height:                      Optional[Decimal]
    AutoMaxHeight:               Optional[enums.Bool]
    MaxHeight:                   Optional[Decimal]
    HorizontalStretch:           Optional[enums.Bool]
    VerticalStretch:             Optional[enums.Bool]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    PlacementArea:               Optional[enums.MenuElementPlacementArea]
    Check:                       Optional[enums.Bool]
    TextColor:                   Optional[Color]
    BackColor:                   Optional[Color]
    BorderColor:                 Optional[Color]
    Font:                        Optional[Font]
    Shortcut:                    Optional[str]
    Picture:                     Optional[Picture]
    Title:                       Optional[LocalStringType]
    TitleHeight:                 Optional[Decimal]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    RepresentationInContextMenu: Optional[enums.RepresentationInContextMenu]
    Shape:                       Optional[enums.ButtonShape]
    ShapeRepresentation:         Optional[enums.ButtonShapeRepresentation]
    PictureLocation:             Optional[enums.FormButtonPictureLocation]
    #Parameter: bool


class ButtonGroup(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    CommandSource:  Optional[CommandSourceName]
    PlacementArea:  Optional[enums.MenuElementPlacementArea]
    Representation: Optional[enums.ButtonGroupRepresentation]

class CalendarField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:                       Optional[Decimal]
    AutoMaxWidth:                Optional[enums.Bool]
    MaxWidth:                    Optional[Decimal]
    MinWidth:                    Optional[Decimal]
    Height:                      Optional[Decimal]
    AutoMaxHeight:               Optional[enums.Bool]
    MaxHeight:                   Optional[Decimal]
    HorizontalStretch:           Optional[enums.Bool]
    VerticalStretch:             Optional[enums.Bool]
    SelectionMode:               Optional[enums.FormDateSelectionMode]
    ShowCurrentDate:             Optional[enums.Bool]
    CalendarNavigation:          Optional[enums.Bool]
    BeginOfRepresentationPeriod: Optional[DateTime]
    EndOfRepresentationPeriod:   Optional[DateTime]
    EnableStartDrag:             Optional[enums.Bool]
    EnableDrag:                  Optional[enums.Bool]
    Font:                        Optional[Font]
    BorderColor:                 Optional[Color]
    Border:                      Optional[Border]
    ShowMonthsPanel:             Optional[enums.Bool]
    WidthInMonths:               Optional[Decimal]
    HeightInMonths:              Optional[Decimal]


class ChartField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]


class CheckBoxField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    CheckBoxType:    Optional[enums.CheckBoxType]
    ThreeState:      Optional[enums.Bool]
    BorderColor:     Optional[Color]
    BackColor:       Optional[Color]
    TextColor:       Optional[Color]
    Font:            Optional[Font]
    EditFormat:      Optional[LocalStringType]
    ItemTitleHeight: Optional[Decimal]
    ItemWidth:       Optional[Decimal]
    ItemHeight:      Optional[Decimal]
    EqualItemsWidth: Optional[enums.BWAValue]


class ColumnGroup(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Group:                 Optional[enums.ColumnsGroup]
    ShowTitle:             Optional[enums.Bool]
    TitleBackColor:        Optional[Color]
    ShowInHeader:          Optional[enums.Bool]
    HeaderDataPath:        Optional[LFEDataPath]
    HeaderHorizontalAlign: Optional[enums.ItemHorizontalAlignment]
    HeaderFormat:          Optional[LocalStringType]
    HeaderPicture:         Optional[Picture]
    FixingInTable:         Optional[enums.FormFixedInTable]


class CommandBar(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    HorizontalLocation: Optional[enums.ItemHorizontalAlignment]
    CommandSource:      Optional[CommandSourceName]

class DendrogramField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]


class FormattedDocumentField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    Output:            Optional[enums.UseOutput]
    TextColor:         Optional[Color]
    BackColor:         Optional[Color]
    BorderColor:       Optional[Color]
    Font:              Optional[Font]


class GanttChartField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]


class GeographicalSchemaField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    Output:            Optional[enums.UseOutput]
    BorderColor:       Optional[Color]


class GraphicalSchemaField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    Output:            Optional[enums.UseOutput]
    Edit:              Optional[enums.Bool]
    BorderColor:       Optional[Color]


class HTMLDocumentField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    Output:            Optional[enums.UseOutput]
    BorderColor:       Optional[Color]


class InputField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:                         Optional[Decimal]
    AutoMaxWidth:                  Optional[enums.Bool]
    MaxWidth:                      Optional[Decimal]
    MinWidth:                      Optional[Decimal]
    Height:                        Optional[Decimal]
    AutoMaxHeight:                 Optional[enums.Bool]
    MaxHeight:                     Optional[Decimal]
    HorizontalStretch:             Optional[enums.BWAValue]
    VerticalStretch:               Optional[enums.BWAValue]
    Wrap:                          Optional[enums.Bool]
    PasswordMode:                  Optional[enums.BWAValue]
    MultiLine:                     Optional[enums.BWAValue]
    ExtendedEdit:                  Optional[enums.BWAValue]
    MarkNegatives:                 Optional[enums.BWAValue]
    DropListButton:                Optional[enums.BWAValue]
    ChoiceButton:                  Optional[enums.BWAValue]
    ChoiceButtonRepresentation:    Optional[enums.ChoiceButtonRepresentation]
    ChoiceButtonPicture:           Optional[Picture]
    ClearButton:                   Optional[enums.BWAValue]
    SpinButton:                    Optional[enums.BWAValue]
    OpenButton:                    Optional[enums.BWAValue]
    CreateButton:                  Optional[enums.BWAValue]
    Mask:                          Optional[str]
    AutoChoiceIncomplete:          Optional[enums.BWAValue]
    QuickChoice:                   Optional[enums.BWAValue]
    ChoiceFoldersAndItems:         Optional[enums.FoldersAndItems]
    Format:                        Optional[LocalStringType]
    EditFormat:                    Optional[LocalStringType]
    AutoMarkIncomplete:            Optional[enums.BWAValue]
    ChooseType:                    Optional[enums.Bool]
    IncompleteChoiceMode:          Optional[enums.IncompleteItemChoiceMode]
    TypeDomainEnabled:             Optional[enums.Bool]
    TextEdit:                      Optional[enums.Bool]
    EditTextUpdate:                Optional[enums.EditTextUpdate]
    ChoiceParameterLinks:          Optional[ChoiceParameterLinks]
    ChoiceParameters:              Optional[ChoiceParameters]
    AvailableTypes:                Optional[TypeDescription]
    ListChoiceMode:                Optional[enums.Bool]
    ChoiceList:                    Optional[ValueList]
    ChoiceListButton:              Optional[enums.BWAValue]
    ChoiceListHeight:              Optional[Decimal]
    DropListWidth:                 Optional[Decimal]
    TextColor:                     Optional[Color]
    BackColor:                     Optional[Color]
    BorderColor:                   Optional[Color]
    Font:                          Optional[Font]
    TypeLink:                      Optional[ItemTypeLink]
    HeightControlVariant:          Optional[enums.HeightControlVariant]
    AutoShowClearButtonMode:       Optional[enums.AutoShowClearButtonMode]
    AutoShowOpenButtonMode:        Optional[enums.AutoShowOpenButtonMode]
    AutoCorrectionOnTextInput:     Optional[enums.AutoCorrectionOnTextInput]
    SpellCheckingOnTextInput:      Optional[enums.SpellCheckingOnTextInput]
    AutoCapitalizationOnTextInput: Optional[enums.AutoCapitalizationOnTextInput]
    SpecialTextInputMode:          Optional[enums.SpecialTextInputMode]
    OnScreenKeyboardReturnKeyText: Optional[enums.OnScreenKeyboardReturnKeyText]
    InputHint:                     Optional[LocalStringType]
    ChoiceHistoryOnInput:          Optional[enums.ChoiceHistoryOnInput]
    #MinValue MDObjectRef
    #MaxValue MDObjectRef


class LabelDecoration(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Decoration
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    Width:                 Optional[Decimal]
    AutoMaxWidth:          Optional[enums.Bool]
    MaxWidth:              Optional[Decimal]
    MinWidth:              Optional[Decimal]
    Height:                Optional[Decimal]
    AutoMaxHeight:         Optional[enums.Bool]
    MaxHeight:             Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    SkipOnInput:           Optional[enums.BWAValue]
    TextColor:             Optional[Color]
    Font:                  Optional[Font]
    Shortcut:              Optional[str]
    Title:                 Optional[FormattedStringType]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Hyperlink:       Optional[enums.Bool]
    HorizontalAlign: Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:   Optional[enums.ItemVerticalAlignment]
    TitleHeight:     Optional[Decimal]
    BackColor:       Optional[Color]
    BorderColor:     Optional[Color]
    Border:          Optional[Border]


class LabelField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.BWAValue]
    VerticalStretch:   Optional[enums.BWAValue]
    MarkNegatives:     Optional[enums.BWAValue]
    Format:            Optional[LocalStringType]
    Hiperlink:         Optional[enums.Bool]
    PasswordMode:      Optional[enums.BWAValue]
    Border:            Optional[Border]
    BorderColor:       Optional[Color]
    TextColor:         Optional[Color]
    BackColor:         Optional[Color]
    Font:              Optional[Font]


class Page(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Picture:           Optional[Picture]
    Group:             Optional[enums.FormChildrenGroup]
    ChildrenAlign:     Optional[enums.FormChildrenAlign]
    HorizontalSpacing: Optional[enums.FormItemSpacing]
    VerticalSpacing:   Optional[enums.FormItemSpacing]
    HorizontalAlign:   Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:     Optional[enums.ItemVerticalAlignment]
    ChildItemsWidth:   Optional[enums.FormChildrenWidth]
    Format:            Optional[LocalStringType]
    ShowTitle:         Optional[enums.Bool]
    TitleDataPath:     Optional[LFEDataPath]
    BackColor:         Optional[Color]
    ScrollOnCompress:  Optional[enums.Bool]


class Pages(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    PagesRepresentation: Optional[enums.FormPagesRepresentation]


class PeriodField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    Font:              Optional[Font]
    BorderColor:       Optional[Color]
    Border:            Optional[Border]


class PictureDecoration(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Decoration
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    Width:                 Optional[Decimal]
    AutoMaxWidth:          Optional[enums.Bool]
    MaxWidth:              Optional[Decimal]
    MinWidth:              Optional[Decimal]
    Height:                Optional[Decimal]
    AutoMaxHeight:         Optional[enums.Bool]
    MaxHeight:             Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    SkipOnInput:           Optional[enums.BWAValue]
    TextColor:             Optional[Color]
    Font:                  Optional[Font]
    Shortcut:              Optional[str]
    Title:                 Optional[FormattedStringType]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Picture:                Optional[Picture]
    PictureSize:            Optional[enums.PictureSize]
    Hyperlink:              Optional[enums.Bool]
    Zoomable:               Optional[enums.Bool]
    NonselectedPictureText: Optional[LocalStringType]
    EnableStartDrag:        Optional[enums.Bool]
    EnableDrag:             Optional[enums.Bool]
    Border:                 Optional[Border]
    BorderColor:            Optional[Color]


class PictureField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:                  Optional[Decimal]
    AutoMaxWidth:           Optional[enums.Bool]
    MaxWidth:               Optional[Decimal]
    MinWidth:               Optional[Decimal]
    Height:                 Optional[Decimal]
    AutoMaxHeight:          Optional[enums.Bool]
    MaxHeight:              Optional[Decimal]
    HorizontalStretch:      Optional[enums.Bool]
    VerticalStretch:        Optional[enums.Bool]
    PictureSize:            Optional[enums.PictureSize]
    Zoomable:               Optional[enums.Bool]
    Hyperlink:              Optional[enums.Bool]
    NonselectedPictureText: Optional[LocalStringType]
    EnableStartDrag:        Optional[enums.Bool]
    EnableDrag:             Optional[enums.Bool]
    ValuesPicture:          Optional[Picture]
    TextColor:              Optional[Color]
    Border:                 Optional[Border]
    BorderColor:            Optional[Color]
    Font:                   Optional[Font]


class PlannerField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    EnableStartDrag:   Optional[enums.Bool]
    EnableDrag:        Optional[enums.Bool]


class Popup(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Picture:             Optional[Picture]
    CommandSource:       Optional[CommandSourceName]
    Representation:      Optional[enums.ButtonRepresentation]
    PlacementArea:       Optional[enums.MenuElementPlacementArea]
    Shape:               Optional[enums.ButtonShape]
    ShapeRepresentation: Optional[enums.ButtonShapeRepresentation]
    BackColor:           Optional[Color]
    BorderColor:         Optional[Color]


class ProgressBarField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    MinValue:          Optional[Decimal]
    MaxValue:          Optional[Decimal]
    Orientation:       Optional[enums.FormElementOrientation]
    Representation:    Optional[enums.FormProgressBarRepresentation]
    ShowPercent:       Optional[enums.Bool]
    BorderColor:       Optional[Color]


class RadioButtonField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    RadioButtonType:   Optional[enums.RadioButtonType]
    ItemWidth:         Optional[Decimal]
    ItemHeight:        Optional[Decimal]
    ItemTitleHeight:   Optional[Decimal]
    ColumnsCount:      Optional[Decimal]
    EqualColumnsWidth: Optional[enums.BWAValue]
    ChoiceList:        Optional[ValueList]
    Font:              Optional[Font]
    TextColor:         Optional[Color]
    BackColor:         Optional[Color]
    BorderColor:       Optional[Color]

class SpreadSheetDocumentField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:                 Optional[Decimal]
    AutoMaxWidth:          Optional[enums.Bool]
    MaxWidth:              Optional[Decimal]
    MinWidth:              Optional[Decimal]
    Height:                Optional[Decimal]
    AutoMaxHeight:         Optional[enums.Bool]
    MaxHeight:             Optional[Decimal]
    HorizontalStretch:     Optional[enums.Bool]
    VerticalStretch:       Optional[enums.Bool]
    ShowGrid:              Optional[enums.Bool]
    ShowHeaders:           Optional[enums.Bool]
    VerticalScrollBar:     Optional[str] #SpreadSheetDocumentScrollBarUse
    HorizontalScrollBar:   Optional[str] #SpreadSheetDocumentScrollBarUse
    BlackAndWhiteView:     Optional[enums.Bool]
    Protection:            Optional[enums.Bool]
    SelectionShowMode:     Optional[enums.SelectionShowMode]
    Output:                Optional[enums.UseOutput]
    Edit:                  Optional[enums.Bool]
    ShowGroups:            Optional[enums.Bool]
    EnableStartDrag:       Optional[enums.Bool]
    EnableDrag:            Optional[enums.Bool]
    BorderColor:           Optional[Color]
    ViewScalingMode:       Optional[enums.ViewScalingMode]
    ShowCellNames:         Optional[enums.Bool]
    ShowRowAndColumnNames: Optional[enums.Bool]
    PointerType:           Optional[enums.SpreadsheetDocumentPointerType]


class Table(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # this
    Representation:                          Optional[enums.TableRepresentation]
    Visible:                                 Optional[enums.Bool]
    UserVisible:                             Optional[AdjustableBoolean]
    CommandBarLocation:                      Optional[enums.FormElementCommandBarLocation]
    Autofill:                                Optional[enums.Bool]
    Enabled:                                 Optional[enums.Bool]
    ReadOnly:                                Optional[enums.Bool]
    SkipOnInput:                             Optional[enums.BWAValue]
    DefaultItem:                             Optional[enums.Bool]
    ChangeRowSet:                            Optional[enums.Bool]
    ChangeRowOrder:                          Optional[enums.Bool]
    Width:                                   Optional[Decimal]
    AutoMaxWidth:                            Optional[enums.Bool]
    MaxWidth:                                Optional[Decimal]
    MinWidth:                                Optional[Decimal]
    Height:                                  Optional[Decimal]
    AutoMaxHeight:                           Optional[enums.Bool]
    MaxHeight:                               Optional[Decimal]
    HeightInTableRows:                       Optional[Decimal]
    HeightControlVariant:                    Optional[enums.TableHeightControlVariant]
    AutoMaxRowsCount:                        Optional[enums.Bool]
    MaxRowsCount:                            Optional[Decimal]
    ChoiceMode:                              Optional[enums.Bool]
    MultipleChoice:                          Optional[enums.Bool]
    RowInputMode:                            Optional[enums.TableRowInputMode]
    SelectionMode:                           Optional[enums.TableSelectionMode]
    RowSelectionMode:                        Optional[enums.TableRowSelectionMode]
    Header:                                  Optional[enums.Bool]
    HeaderHeight:                            Optional[Decimal]
    Footer:                                  Optional[enums.Bool]
    FooterHeight:                            Optional[Decimal]
    HorizontalScrollBar:                     Optional[enums.TableScrollBarUse]
    VerticalScrollBar:                       Optional[enums.TableScrollBarUse]
    HorizontalLines:                         Optional[enums.Bool]
    VerticalLines:                           Optional[enums.Bool]
    FixedLeft:                               Optional[Decimal]
    FixedRight:                              Optional[Decimal]
    UseAlternationRowColor:                  Optional[enums.Bool]
    AutoInsertNewRow:                        Optional[enums.Bool]
    AutoAddIncomplete:                       Optional[enums.BWAValue]
    AutoMarkIncomplete:                      Optional[enums.BWAValue]
    SearchOnInput:                           Optional[enums.SearchOnInput]
    InitialListView:                         Optional[enums.TableInitialListView]
    InitialTreeView:                         Optional[enums.TableInitialTreeView]
    Output:                                  Optional[enums.UseOutput]
    HorizontalStretch:                       Optional[enums.Bool]
    VerticalStretch:                         Optional[enums.Bool]
    EnableStartDrag:                         Optional[enums.Bool]
    EnableDrag:                              Optional[enums.Bool]
    DataPath:                                Optional[LFEDataPath]
    RowPictureDataPath:                      Optional[LFEDataPath]
    RowsPicture:                             Optional[Picture]
    TextColor:                               Optional[Color]
    BackColor:                               Optional[Color]
    BorderColor:                             Optional[Color]
    TitleFont:                               Optional[Font]
    Font:                                    Optional[Font]
    Title:                                   Optional[LocalStringType]
    TitleHeight:                             Optional[Decimal]
    TitleTextColor:                          Optional[Color]
    TitleLocation:                           Optional[enums.FormElementTitleLocation]
    Shortcut:                                Optional[str]
    CommandSet:                              Optional[CommandsContent]
    ToolTip:                                 Optional[LocalStringType]
    ToolTipRepresentation:                   Optional[enums.TooltipRepresentation]
    SearchStringLocation:                    Optional[enums.SearchStringLocation]
    ViewStatusLocation:                      Optional[enums.ViewStatusLocation]
    SearchControlLocation:                   Optional[enums.SearchControlLocation]
    GroupHorizontalAlign:                    Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:                      Optional[enums.ItemVerticalAlignment]
    RefreshRequest:                          Optional[enums.RefreshRequestMethod]
    ViewMode:                                Optional[enums.DataCompositionSettingsViewMode]
    SettingsNamedItemDetailedRepresentation: Optional[enums.Bool]
    AutoRefresh:                             Optional[enums.Bool]
    AutoRefreshPeriod:                       Optional[Decimal]
    Period:                                  Optional[StandardPeriod]
    ChoiceFoldersAndItems:                   Optional[enums.FoldersAndItemsUse]
    RestoreCurrentRow:                       Optional[enums.Bool]
    AllowRootChoice:                         Optional[enums.Bool]
    UserSettingsGroup:                       Optional[str]
    #TopLevelParent bool
    #RowFilter enums.UpdateOnDataChange


class TextDocumentField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    Output:            Optional[enums.UseOutput]
    TextColor:         Optional[Color]
    BackColor:         Optional[Color]
    BorderColor:       Optional[Color]
    Font:              Optional[Font]


class TrackBarField(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # Field
    DataPath:                    Optional[LFEDataPath]
    Visible:                     Optional[enums.Bool]
    UserVisible:                 Optional[AdjustableBoolean]
    DefaultItem:                 Optional[enums.Bool]
    Enabled:                     Optional[enums.Bool]
    ReadOnly:                    Optional[enums.Bool]
    SkipOnInput:                 Optional[enums.BWAValue]
    Title:                       Optional[LocalStringType]
    TitleTextColor:              Optional[Color]
    TitleBackColor:              Optional[Color]
    TitleFont:                   Optional[Font]
    TitleLocation:               Optional[enums.FormElementTitleLocation]
    TitleHeight:                 Optional[Decimal]
    ToolTip:                     Optional[LocalStringType]
    ToolTipRepresentation:       Optional[enums.TooltipRepresentation]
    WarningOnEditRepresentation: Optional[enums.WarningOnEditRepresentation]
    WarningOnEdit:               Optional[LocalStringType]
    Shortcut:                    Optional[str]
    CommandSet:                  Optional[CommandsContent]
    HorizontalAlign:             Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:               Optional[enums.ItemVerticalAlignment]
    GroupHorizontalAlign:        Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:          Optional[enums.ItemVerticalAlignment]
    EditMode:                    Optional[enums.TableFieldEditMode]
    FixingInTable:               Optional[enums.FormFixedInTable]
    CellHyperlink:               Optional[enums.Bool]
    AutoCellHeight:              Optional[enums.Bool]
    ShowInHeader:                Optional[enums.Bool]
    HeaderPicture:               Optional[Picture]
    HeaderHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]
    ShowInFooter:                Optional[enums.Bool]
    FooterDataPath:              Optional[LFEDataPath]
    FooterText:                  Optional[LocalStringType]
    FooterTextColor:             Optional[Color]
    FooterBackColor:             Optional[Color]
    FooterFont:                  Optional[Font]
    FooterPicture:               Optional[Picture]
    FooterHorizontalAlign:       Optional[enums.ItemHorizontalAlignment]

    # this
    Width:             Optional[Decimal]
    AutoMaxWidth:      Optional[enums.Bool]
    MaxWidth:          Optional[Decimal]
    MinWidth:          Optional[Decimal]
    Height:            Optional[Decimal]
    AutoMaxHeight:     Optional[enums.Bool]
    MaxHeight:         Optional[Decimal]
    HorizontalStretch: Optional[enums.Bool]
    VerticalStretch:   Optional[enums.Bool]
    MinValue:          Optional[Decimal]
    MaxValue:          Optional[Decimal]
    Step:              Optional[Decimal]
    LargeStep:         Optional[Decimal]
    MarkingStep:       Optional[Decimal]
    Orientation:       Optional[enums.FormElementOrientation]
    MarkingAppearance: Optional[enums.MarkingStyle]
    BorderColor:       Optional[Color]


class UsualGroup(XMLData):

    # FormVisualEntity
    ContextMenu:           Optional['ContextMenu']
    AutoCommandBar:        Optional['AutoCommandBar']
    ExtendedTooltip:       Optional['LabelDecoration']
    SearchStringAddition:  Optional['SearchStringAddition']
    ViewStatusAddition:    Optional['ViewStatusAddition']
    SearchControlAddition: Optional['SearchControlAddition']
    Events:                Optional['FormItemEvents']
    ChildItems:            Optional['ChildItems']

    # FormItemBase
    id:   Optional[Decimal]
    name: Optional[str]

    # GroupBase
    Visible:               Optional[enums.Bool]
    UserVisible:           Optional[AdjustableBoolean]
    Enabled:               Optional[enums.Bool]
    ReadOnly:              Optional[enums.Bool]
    EnableContentChange:   Optional[enums.Bool]
    Title:                 Optional[LocalStringType]
    TitleTextColor:        Optional[Color]
    TitleFont:             Optional[Font]
    ToolTip:               Optional[LocalStringType]
    ToolTipRepresentation: Optional[enums.TooltipRepresentation]
    Shortcut:              Optional[str]
    Width:                 Optional[Decimal]
    Height:                Optional[Decimal]
    HorizontalStretch:     Optional[enums.BWAValue]
    VerticalStretch:       Optional[enums.BWAValue]
    GroupHorizontalAlign:  Optional[enums.ItemHorizontalAlignment]
    GroupVerticalAlign:    Optional[enums.ItemVerticalAlignment]

    # this
    Group:                        Optional[enums.FormChildrenGroup]
    ChildrenAlign:                Optional[enums.FormChildrenAlign]
    HorizontalSpacing:            Optional[enums.FormItemSpacing]
    VerticalSpacing:              Optional[enums.FormItemSpacing]
    HorizontalAlign:              Optional[enums.ItemHorizontalAlignment]
    VerticalAlign:                Optional[enums.ItemVerticalAlignment]
    Behavior:                     Optional[enums.UsualGroupBehavior]
    CollapsedRepresentationTitle: Optional[LocalStringType]
    Collapsed:                    Optional[enums.Bool]
    ControlRepresentation:        Optional[enums.UsualGroupControlRepresentation]
    Representation:               Optional[enums.UsualGroupControlRepresentation]
    ShowLeftMargin:               Optional[enums.Bool]
    United:                       Optional[enums.Bool]
    ChildItemsWidth:              Optional[enums.FormChildrenWidth]
    Format:                       Optional[LocalStringType]
    ShowTitle:                    Optional[enums.Bool]
    TitleDataPath:                Optional[LFEDataPath]
    BackColor:                    Optional[Color]
    ThroughAlign:                 Optional[enums.UsualGroupThroughAlign]

#endregion ChildItems

class Root(XMLFile):
    Form: Optional[ManagedForm]

#endregion Form

fill_types(globals())
