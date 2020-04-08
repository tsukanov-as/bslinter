
from typing import List, Optional
from decimal import Decimal
from enum import EnumMeta

from md.base import XMLData, fill_types #, XMLFile, OrderedXMLData
import md.enums as enums

Field = str
ParameterType = str

class TypedValue(XMLData):
    type: Optional[str]
    _text: Optional[str]

class ParameterValue(XMLData):
    use: Optional[enums.Bool]
    parameter: Optional[ParameterType]
    value: Optional[TypedValue] #???
    # item: List['ParameterValue']

class Appearance(XMLData):
    item: List[ParameterValue]


class AppearanceField(XMLData):
    iID: Optional[Decimal]
    use: Optional[enums.Bool]
    field: Optional[Field]

class AppearanceFields(XMLData):
    item: List[AppearanceField]

class FilterItem(XMLData):
    type: Optional[str] # FilterItemComparison, FilterItemGroup
    iID: Optional[Decimal]
    use: Optional[enums.Bool]

    left: Optional[TypedValue] #???
    comparisonType: Optional[enums.DataCompositionComparisonType]
    right: Optional[TypedValue] #???

    groupType: Optional[enums.DataCompositionFilterItemsGroupType]
    item: Optional['FilterItem']

    presentation: Optional[str] #???
    application: Optional[enums.DataCompositionFilterApplicationType]
    viewMode: Optional[enums.DataCompositionSettingsItemViewMode]
    userSettingID: Optional[str]
    userSettingPresentation: Optional[str] #???

class Filter(XMLData):
    item: List[FilterItem]
    viewMode: Optional[enums.DataCompositionSettingsItemViewMode]
    userSettingID: Optional[str]
    userSettingPresentation: Optional[str] #???

class ConditionalAppearanceItem(XMLData):
    iID: Optional[Decimal]
    use: Optional[enums.Bool]
    selection: Optional[AppearanceFields]
    filter: Optional[Filter]
    appearance: Optional[Appearance]
    presentation: Optional[str] #???
    viewMode: Optional[enums.DataCompositionSettingsItemViewMode]
    userSettingID: Optional[str]
    userSettingPresentation: Optional[str] #???
    useInGroup: Optional[enums.DataCompositionConditionalAppearanceUse]
    useInHierarchicalGroup: Optional[enums.DataCompositionConditionalAppearanceUse]
    useInOverall: Optional[enums.DataCompositionConditionalAppearanceUse]
    useInFieldsHeader: Optional[enums.DataCompositionConditionalAppearanceUse]
    useInHeader: Optional[enums.DataCompositionConditionalAppearanceUse]
    useInParameters: Optional[enums.DataCompositionConditionalAppearanceUse]
    useInFilter: Optional[enums.DataCompositionConditionalAppearanceUse]

class ConditionalAppearance(XMLData):
    item: Optional[ConditionalAppearanceItem]
    viewMode: Optional[enums.DataCompositionSettingsItemViewMode]
    userSettingID: Optional[str]
    userSettingPresentation: Optional[str] #???

fill_types(globals())