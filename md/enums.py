# Copyright 2019 Tsukanov Alexander. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from enum import Enum, auto

class EnumBase(Enum):

    @classmethod
    def get(cls, key):
        # pylint: disable=no-member
        return cls._member_map_.get(key.upper())  # TODO: кидать исключение если значение не найдено

class Bool(EnumBase):
    TRUE = auto()
    FALSE = auto()

class LinkedValueChangeMode(EnumBase):
    DONTCHANGE = auto()
    CLEAR = auto()

class DefaultDataLockControlMode(EnumBase):
    MANAGED = auto()
    AUTOMATIC = auto()
    AUTOMATICANDMANAGED = auto()

class FullTextSearchUsing(EnumBase):
    USE = auto()
    DONTUSE = auto()

class UseQuickChoice(EnumBase):
    AUTO = auto()
    USE = auto()
    DONTUSE = auto()

class FillChecking(EnumBase):
    DONTCHECK = auto()
    SHOWERROR = auto()

class DataHistoryUse(EnumBase):
    USE = auto()
    DONTUSE = auto()

class CreateOnInput(EnumBase):
    USE = auto()
    AUTO = auto()
    DONTUSE = auto()

class ChoiceHistoryOnInput(EnumBase):
    AUTO = auto()
    DONTUSE = auto()

class FoldersAndItemsUse(EnumBase):
    ITEMS = auto()
    FOLDERSANDITEMS = auto()
    FOLDERS = auto()

class Indexing(EnumBase):
    DONTINDEX = auto()
    INDEX = auto()
    INDEXWITHADDITIONALORDER = auto()

class AttributeUse(EnumBase):
    FORFOLDER = auto()
    FORFOLDERANDITEM = auto()
    FORITEM = auto()

class AllowedSign(EnumBase):
    ANY = auto()
    NONNEGATIVE = auto()

class AllowedLength(EnumBase):
    VARIABLE = auto()
    FIXED = auto()

class DateFractions(EnumBase):
    DATE = auto()
    TIME = auto()
    DATETIME = auto()

class CommandParameterUseMode(EnumBase):
    SINGLE = auto()
    MULTIPLE = auto()

class ButtonRepresentation(EnumBase):
    AUTO = auto()
    PICTURE = auto()
    PICTUREANDTEXT = auto()
    TEXT = auto()

class FormType(EnumBase):
    ORDINARY = auto()
    MANAGED = auto()

class TemplateType(EnumBase):
    ACTIVEDOCUMENT = auto()
    HTMLDOCUMENT = auto()
    ADDIN = auto()
    GEOGRAPHICALSCHEMA = auto()
    GRAPHICALSCHEMA = auto()
    BINARYDATA = auto()
    DATACOMPOSITIONAPPEARANCETEMPLATE = auto()
    DATACOMPOSITIONSCHEMA = auto()
    SPREADSHEETDOCUMENT = auto()
    TEXTDOCUMENT = auto()

class AccumulationRegisterType(EnumBase):
    TURNOVERS = auto()
    BALANCE = auto()

class EditType(EnumBase):
    INDIALOG = auto()
    INLIST = auto()
    BOTHWAYS = auto()

class SearchStringModeOnInputByString(EnumBase):
    BEGIN = auto()
    ANYPART = auto()

class ChoiceDataGetModeOnInputByString(EnumBase):
    DIRECTLY = auto()
    BACKGROUND = auto()

class FullTextSearchOnInputByString(EnumBase):
    DONTUSE = auto()
    USE = auto()

class BusinessProcessNumberType(EnumBase):
    STRING = auto()
    NUMBER = auto()

class BusinessProcessNumberPeriodicity(EnumBase):
    YEAR = auto()
    DAY = auto()
    QUARTER = auto()
    MONTH = auto()
    NONPERIODICAL = auto()

class CalculationRegisterPeriodicity(EnumBase):
    YEAR = auto()
    DAY = auto()
    QUARTER = auto()
    MONTH = auto()

class HierarchyType(EnumBase):
    HIERARCHYFOLDERSANDITEMS = auto()
    HIERARCHYOFITEMS = auto()

class SubordinationUse(EnumBase):
    TOFOLDERS = auto()
    TOFOLDERSANDITEMS = auto()
    TOITEMS = auto()

class CatalogCodeType(EnumBase):
    STRING = auto()
    NUMBER = auto()

class CatalogCodesSeries(EnumBase):
    WHOLECATALOG = auto()
    WITHINSUBORDINATION = auto()
    WITHINOWNERSUBORDINATION = auto()

class CatalogMainPresentation(EnumBase):
    ASCODE = auto()
    ASDESCRIPTION = auto()

class PredefinedDataUpdate(EnumBase):
    AUTO = auto()
    DONTAUTOUPDATE = auto()
    AUTOUPDATE = auto()

class ChoiceMode(EnumBase):
    BOTHWAYS = auto()
    FROMFORM = auto()
    QUICKCHOICE = auto()

class CharOfAccountCodeSeries(EnumBase):
    WHOLECHARTOFACCOUNTS = auto()
    WITHINSUBORDINATION = auto()

class AccountMainPresentation(EnumBase):
    ASCODE = auto()
    ASDESCRIPTION = auto()

class ChartOfCalculationTypesCodeType(EnumBase):
    STRING = auto()
    NUMBER = auto()

class CalculationTypeMainPresentation(EnumBase):
    ASCODE = auto()
    ASDESCRIPTION = auto()

class ChartOfCalculationTypesBaseUse(EnumBase):
    DONTUSE = auto()
    ONACTIONPERIOD = auto()
    ONREGISTRATIONPERIOD = auto()

class CharacteristicKindCodesSeries(EnumBase):
    WHOLECHARACTERISTICKIND = auto()
    WITHINSUBORDINATION = auto()

class CharacteristicTypeMainPresentation(EnumBase):
    ASCODE = auto()
    ASDESCRIPTION = auto()

class CommandGroupCategory(EnumBase):
    FORMCOMMANDBAR = auto()
    ACTIONSPANEL = auto()
    NAVIGATIONPANEL = auto()
    FORMNAVIGATIONPANEL = auto()

class CommonAttributeAutoUse(EnumBase):
    USE = auto()
    DONTUSE = auto()

class CommonAttributeDataSeparation(EnumBase):
    DONTUSE = auto()
    SEPARATE = auto()

class CommonAttributeSeparatedDataUse(EnumBase):
    INDEPENDENTLY = auto()
    INDEPENDENTLYANDSIMULTANEOUSLY = auto()

class CommonAttributeUsersSeparation(EnumBase):
    DONTUSE = auto()
    SEPARATE = auto()

class CommonAttributeAuthenticationSeparation(EnumBase):
    DONTUSE = auto()
    SEPARATE = auto()

class CommonAttributeConfigurationExtensionsSeparation(EnumBase):
    DONTUSE = auto()
    SEPARATE = auto()

class ReturnValuesReuse(EnumBase):
    DURINGREQUEST = auto()
    DURINGSESSION = auto()
    DONTUSE = auto()

class CompatibilityMode(EnumBase):
    VERSION8_1 = auto()
    VERSION8_2_13 = auto()
    VERSION8_2_16 = auto()
    VERSION8_3_1 = auto()
    VERSION8_3_2 = auto()
    VERSION8_3_3 = auto()
    VERSION8_3_4 = auto()
    VERSION8_3_5 = auto()
    VERSION8_3_6 = auto()
    VERSION8_3_7 = auto()
    VERSION8_3_8 = auto()
    VERSION8_3_9 = auto()
    VERSION8_3_10 = auto()
    VERSION8_3_11 = auto()
    VERSION8_3_12 = auto()
    VERSION8_3_13 = auto()
    VERSION8_3_14 = auto()
    DONTUSE = auto()

class ClientRunMode(EnumBase):
    AUTO = auto()
    ORDINARYAPPLICATION = auto()
    MANAGEDAPPLICATION = auto()

class ScriptVariant(EnumBase):
    ENGLISH = auto()
    RUSSIAN = auto()

class MainClientApplicationWindowMode(EnumBase):
    KIOSK = auto()
    NORMAL = auto()
    FULLSCREENWORKPLACE = auto()
    WORKPLACE = auto()

class ObjectAutonumerationMode(EnumBase):
    NOTAUTOFREE = auto()
    AUTOFREE = auto()

class ModalityUseMode(EnumBase):
    USE = auto()
    USEWITHWARNINGS = auto()
    DONTUSE = auto()

class SynchronousPlatformExtensionAndAddInCallUseMode(EnumBase):
    USE = auto()
    USEWITHWARNINGS = auto()
    DONTUSE = auto()

class InterfaceCompatibilityMode(EnumBase):
    VERSION8_2 = auto()
    VERSION8_2ENABLETAXI = auto()
    TAXI = auto()
    TAXIENABLEVERSION8_2 = auto()

class DocumentNumberType(EnumBase):
    STRING = auto()
    NUMBER = auto()

class DocumentNumberPeriodicity(EnumBase):
    YEAR = auto()
    DAY = auto()
    QUARTER = auto()
    MONTH = auto()
    NONPERIODICAL = auto()

class Posting(EnumBase):
    ALLOW = auto()
    DENY = auto()

class RealTimePosting(EnumBase):
    DENY = auto()
    ALLOW = auto()

class RegisterRecordsDeletion(EnumBase):
    AUTODELETEOFF = auto()
    AUTODELETE = auto()
    AUTODELETEONUNPOST = auto()

class RegisterRecordsWritingOnPost(EnumBase):
    WRITESELECTED = auto()
    WRITEMODIFIED = auto()

class SequenceFilling(EnumBase):
    AUTOFILL = auto()
    AUTOFILLOFF = auto()

class DataExchangeMainPresentation(EnumBase):
    ASCODE = auto()
    ASDESCRIPTION = auto()

class SessionReuseMode(EnumBase):
    AUTOUSE = auto()
    DONTUSE = auto()
    USE = auto()

class InformationRegisterPeriodicity(EnumBase):
    YEAR = auto()
    DAY = auto()
    QUARTER = auto()
    MONTH = auto()
    NONPERIODICAL = auto()
    RECORDERPOSITION = auto()
    SECOND = auto()

class RegisterWriteMode(EnumBase):
    INDEPENDENT = auto()
    RECORDERSUBORDINATE = auto()

class MoveBoundaryOnPosting(EnumBase):
    DONTMOVE = auto()
    MOVE = auto()

class TaskNumberType(EnumBase):
    STRING = auto()
    NUMBER = auto()

class TaskNumberAutoPrefix(EnumBase):
    BUSINESSPROCESSNUMBER = auto()
    DONTUSE = auto()

class TaskMainPresentation(EnumBase):
    ASCODE = auto()
    ASDESCRIPTION = auto()

class TransferDirection(EnumBase):
    IN = auto()
    INOUT = auto()
    OUT = auto()


class Rights(EnumBase): # TODO: ?
    ACTIVEUSERS = auto()
    ADMINISTRATION = auto()
    ALLFUNCTIONSMODE = auto()
    AUTOMATION = auto()
    COLLABORATIONSYSTEMINFOBASEREGISTRATION = auto()
    CONFIGURATIONEXTENSIONSADMINISTRATION = auto()
    DATAADMINISTRATION = auto()
    DELETE = auto()
    EDIT = auto()
    EVENTLOG = auto()
    EXCLUSIVEMODE = auto()
    EXECUTE = auto()
    EXTERNALCONNECTION = auto()
    GET = auto()
    INPUTBYSTRING = auto()
    INSERT = auto()
    INTERACTIVEACTIVATE = auto()
    INTERACTIVECHANGEOFPOSTED = auto()
    INTERACTIVECLEARDELETIONMARK = auto()
    INTERACTIVECLEARDELETIONMARKPREDEFINEDDATA = auto()
    INTERACTIVEDELETE = auto()
    INTERACTIVEDELETEMARKED = auto()
    INTERACTIVEDELETEMARKEDPREDEFINEDDATA = auto()
    INTERACTIVEDELETEPREDEFINEDDATA = auto()
    INTERACTIVEEXECUTE = auto()
    INTERACTIVEINSERT = auto()
    INTERACTIVEOPENEXTDATAPROCESSORS = auto()
    INTERACTIVEOPENEXTREPORTS = auto()
    INTERACTIVEPOSTING = auto()
    INTERACTIVEPOSTINGREGULAR = auto()
    INTERACTIVESETDELETIONMARK = auto()
    INTERACTIVESETDELETIONMARKPREDEFINEDDATA = auto()
    INTERACTIVESTART = auto()
    INTERACTIVEUNDOPOSTING = auto()
    OUTPUT = auto()
    POSTING = auto()
    READ = auto()
    SAVEUSERDATA = auto()
    SESSIONOSAUTHENTICATIONCHANGE = auto()
    SESSIONSTANDARDAUTHENTICATIONCHANGE = auto()
    SET = auto()
    STANDARDAUTHENTICATIONCHANGE = auto()
    START = auto()
    THICKCLIENT = auto()
    THINCLIENT = auto()
    TOTALSCONTROL = auto()
    UNDOPOSTING = auto()
    UPDATE = auto()
    UPDATEDATABASECONFIGURATION = auto()
    USE = auto()
    VIEW = auto()
    WEBCLIENT = auto()
    READDATAHISTORY = auto()
    READDATAHISTORYOFMISSINGDATA = auto()
    UPDATEDATAHISTORY = auto()
    UPDATEDATAHISTORYOFMISSINGDATA = auto()
    UPDATEDATAHISTORYSETTINGS = auto()
    UPDATEDATAHISTORYVERSIONCOMMENT = auto()
    VIEWDATAHISTORY = auto()
    EDITDATAHISTORYVERSIONCOMMENT = auto()
    SWITCHTODATAHISTORYVERSION = auto()

class HTTPMethod(EnumBase):
    GET = auto()
    PUT = auto()
    POST = auto()
    DELETE = auto()
    PATCH = auto()
    MERGE = auto()
    OPTIONS = auto()
    TRACE = auto()
    CONNECT = auto()
    PROPFIND = auto()
    PROPPATCH = auto()
    MOVE = auto()
    COPY = auto()
    LOCK = auto()
    UNLOCK = auto()
    MKCOL = auto()
    ANY = auto()

#region forms

class AutoCapitalizationOnTextInput(EnumBase):
    AUTO = auto()
    NONE = auto()
    WORDS = auto()
    SENTENCES = auto()
    ALLCHARACTERS = auto()

class AutoCorrectionOnTextInput(EnumBase):
    AUTO = auto()
    USE = auto()
    DONTUSE = auto()

class AutoSaveFormDataInSettings(EnumBase):
    DONTUSE = auto()
    USE = auto()

class AutoShowClearButtonMode(EnumBase):
    AUTO = auto()
    ALWAYS = auto()
    FILLEDONLY = auto()

class AutoShowOpenButtonMode(EnumBase):
    AUTO = auto()
    ALWAYS = auto()
    FILLEDONLY = auto()

class BWAValue(EnumBase):
    TRUE = auto()
    FALSE = auto()
    AUTO = auto()

class ButtonGroupRepresentation(EnumBase):
    AUTO = auto()
    USUAL = auto()
    COMPACT = auto()

class ButtonShape(EnumBase):
    AUTO = auto()
    USUAL = auto()
    OVAL = auto()

class ButtonShapeRepresentation(EnumBase):
    AUTO = auto()
    ALWAYS = auto()
    WHENACTIVE = auto()
    NONE = auto()

class CheckBoxType(EnumBase):
    AUTO = auto()
    CHECKBOX = auto()
    TUMBLER = auto()

class ChoiceButtonRepresentation(EnumBase):
    AUTO = auto()
    SHOWINDROPLIST = auto()
    SHOWINDROPLISTANDININPUTFIELD = auto()
    SHOWININPUTFIELD = auto()

class CollapseFormItemsByImportance(EnumBase):
    AUTO = auto()
    USE = auto()
    DONTUSE = auto()

class ColumnsGroup(EnumBase):
    HORIZONTAL = auto()
    VERTICAL = auto()
    INCELL = auto()

class CurrentRowUse(EnumBase):
    USE = auto()
    DONTUSE = auto()
    AUTO = auto()

class DisplayImportance(EnumBase):
    AUTO = auto()
    VERYHIGH = auto()
    HIGH = auto()
    USUAL = auto()
    LOW = auto()
    VERYLOW = auto()

class EditTextUpdate(EnumBase):
    AUTO = auto()
    DONTUSE = auto()
    ONVALUECHANGE = auto()
    ALWAYS = auto()

class EventHandlerCallType(EnumBase):
    BEFORE = auto()
    AFTER = auto()
    OVERRIDE = auto()

class FileDragMode(EnumBase):
    ASFILE = auto()
    ASFILEREF = auto()

class FoldersAndItems(EnumBase):
    ITEMS = auto()
    FOLDERS = auto()
    FOLDERSANDITEMS = auto()
    AUTO = auto()

class FormBaseFontVariant(EnumBase):
    AUTO = auto()
    NORMAL = auto()
    COMPACT = auto()

class FormButtonPictureLocation(EnumBase):
    AUTO = auto()
    LEFT = auto()
    RIGHT = auto()

class FormChildrenAlign(EnumBase):
    AUTO = auto()
    NONE = auto()
    ITEMSLEFTTITLESLEFT = auto()
    ITEMSRIGHTTITLESLEFT = auto()
    ITEMSLEFTTITLESRIGHT = auto()
    ITEMSRIGHTTITLESRIGHT = auto()
    TITLESLEFTDATALEFT = auto()
    TITLESLEFTDATARIGHT = auto()
    TITLESRIGHTDATALEFT = auto()
    TITLESRIGHTDATARIGHT = auto()
    TITLESLEFTDATAAUTO = auto()

class FormChildrenGroup(EnumBase):
    HORIZONTAL = auto()
    VERTICAL = auto()
    HORIZONTALIFPOSSIBLE = auto()
    ALWAYSHORIZONTAL = auto()

class FormChildrenWidth(EnumBase):
    AUTO = auto()
    EQUAL = auto()
    LEFTWIDE = auto()
    LEFTWIDEST = auto()
    LEFTNARROW = auto()
    LEFTNARROWEST = auto()

class FormDateSelectionMode(EnumBase):
    SINGLE = auto()
    MULTIPLE = auto()
    INTERVAL = auto()

class FormElementCommandBarLocation(EnumBase):
    NONE = auto()
    AUTO = auto()
    TOP = auto()
    BOTTOM = auto()

class FormElementOrientation(EnumBase):
    HORIZONTAL = auto()
    VERTICAL = auto()

class FormElementOrigin(EnumBase):
    SOURCE = auto()
    AUTOGENERATED = auto()
    ADDEDFROMCONTEXT = auto()
    ADDEDFROMMAINCONF = auto()

class FormElementTitleLocation(EnumBase):
    NONE = auto()
    AUTO = auto()
    LEFT = auto()
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()

class FormEnterKeyBehavior(EnumBase):
    CONTROLNAVIGATION = auto()
    DEFAULTBUTTON = auto()

class FormFixedInTable(EnumBase):
    NONE = auto()
    LEFT = auto()
    RIGHT = auto()

class FormItemSpacing(EnumBase):
    AUTO = auto()
    NONE = auto()
    HALF = auto()
    SINGLE = auto()
    ONEANDHALF = auto()
    DOUBLE = auto()

class FormPagesRepresentation(EnumBase):
    NONE = auto()
    TABSONTOP = auto()
    TABSONBOTTOM = auto()
    TABSONLEFTHORIZONTAL = auto()
    TABSONRIGHTHORIZONTAL = auto()
    SWIPE = auto()

class FormPagesState(EnumBase):
    AUTO = auto()
    TITLESANDCURRENTPAGE = auto()
    TITLES = auto()
    CURRENTPAGE = auto()

class FormProgressBarRepresentation(EnumBase):
    SMOOTH = auto()
    BROKEN = auto()
    BROKENTILT = auto()

class FormWindowOpeningMode(EnumBase):
    INDEPENDENT = auto()
    LOCKOWNERWINDOW = auto()
    LOCKWHOLEINTERFACE = auto()

class HeightControlVariant(EnumBase):
    AUTO = auto()
    USEHEIGHTINFORMROWS = auto()
    USECONTENTHEIGHT = auto()

class IncompleteItemChoiceMode(EnumBase):
    ONENTERPRESSED = auto()
    ONACTIVATE = auto()

class ItemHorizontalAlignment(EnumBase):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()
    AUTO = auto()

class ItemVerticalAlignment(EnumBase):
    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()
    AUTO = auto()

class LFTableListEditingMode(EnumBase):
    NONE = auto()
    MULTIPLESELECTION = auto()
    LINESREARRANGEMENT = auto()

class LogFormElementAdditionKind(EnumBase):
    SEARCHSTRINGREPRESENTATION = auto()
    VIEWSTATUSREPRESENTATION = auto()
    SEARCHCONTROL = auto()

class LogFormScrollMode(EnumBase):
    AUTO = auto()
    USE = auto()
    USEIFNECESSARY = auto()
    USEWITHOUTSTRETCH = auto()

class LogFormShowConversations(EnumBase):
    AUTO = auto()
    SHOW = auto()
    DONTSHOW = auto()

class ManagedFormButtonType(EnumBase):
    COMMANDBARBUTTON = auto()
    USUALBUTTON = auto()
    HYPERLINK = auto()
    COMMANDBARHYPERLINK = auto()

class ManagedFormDecorationType(EnumBase):
    LABEL = auto()
    PICTURE = auto()

class ManagedFormFieldType(EnumBase):
    DEFAULT = auto()
    LABELFIELD = auto()
    INPUTFIELD = auto()
    CHECKBOXFIELD = auto()
    PICTUREFIELD = auto()
    RADIOBUTTONFIELD = auto()
    SPREADSHEETDOCUMENTFIELD = auto()
    TEXTDOCUMENTFIELD = auto()
    FORMATTEDDOCUMENTFIELD = auto()
    PLANNERFIELD = auto()
    CALENDARFIELD = auto()
    PERIODFIELD = auto()
    PROGRESSBARFIELD = auto()
    TRACKBARFIELD = auto()
    CHARTFIELD = auto()
    GANTTCHARTFIELD = auto()
    DENDROGRAMFIELD = auto()
    GRAPHICALSCHEMAFIELD = auto()
    HTMLDOCUMENTFIELD = auto()
    GEOGRAPHICALSCHEMAFIELD = auto()

class ManagedFormGroupType(EnumBase):
    COMMANDBAR = auto()
    POPUP = auto()
    COLUMNGROUP = auto()
    PAGES = auto()
    PAGE = auto()
    USUALGROUP = auto()
    BUTTONGROUP = auto()
    CONTEXTMENU = auto()
    AUTOCOMMANDBAR = auto()
    NAVIGATOR = auto()

class MarkingStyle(EnumBase):
    DONTSHOW = auto()
    TOPLEFT = auto()
    BOTTOMRIGHT = auto()
    BOTHSIDES = auto()

class MenuElementPlacementArea(EnumBase):
    MAINCMDSLEFT = auto()
    AUTOCMDS = auto()
    USERCMDS = auto()
    MAINCMDSRIGHT = auto()

class OnScreenKeyboardReturnKeyText(EnumBase):
    AUTO = auto()
    RETURN = auto()
    GO = auto()
    JOIN = auto()
    NEXT = auto()
    SEARCH = auto()
    SEND = auto()
    DONE = auto()
    CONTINUE = auto()

class PictureSize(EnumBase):
    REALSIZE = auto()
    STRETCH = auto()
    PROPORTIONALLY = auto()
    TILE = auto()
    AUTOSIZE = auto()
    REALSIZEIGNORESCALE = auto()
    AUTOSIZEIGNORESCALE = auto()

class RadioButtonType(EnumBase):
    AUTO = auto()
    RADIOBUTTONS = auto()
    TUMBLER = auto()

class RefreshRequestMethod(EnumBase):
    NONE = auto()
    PULLFROMTOP = auto()
    PULLFROMBOTTOM = auto()
    PULLFROMTOPORBOTTOM = auto()

class ReportFormType(EnumBase):
    MAIN = auto()
    SETTINGS = auto()
    VARIANT = auto()

class RepresentationInContextMenu(EnumBase):
    NONE = auto()
    ADDITIONALINCONTEXTMENU = auto()
    ONLYINCONTEXTMENU = auto()
    AUTO = auto()

class SaveFormDataInSettings(EnumBase):
    DONTUSE = auto()
    USELIST = auto()

class SearchControlLocation(EnumBase):
    AUTO = auto()
    NONE = auto()
    COMMANDBAR = auto()

class SearchOnInput(EnumBase):
    USE = auto()
    DONTUSE = auto()
    AUTO = auto()

class SearchStringLocation(EnumBase):
    AUTO = auto()
    NONE = auto()
    COMMANDBAR = auto()
    TOP = auto()
    BOTTOM = auto()
    FORMCAPTION = auto()
    PULLFROMTOP = auto()

class SelectionShowMode(EnumBase):
    WHENACTIVE = auto()
    ALWAYS = auto()
    DONTSHOW = auto()
    WHENMULTIPLECELLSSELECTED = auto()
    WHENMULTIPLECELLSSELECTEDWHENACTIVE = auto()

class SpecialTextInputMode(EnumBase):
    AUTO = auto()
    NONE = auto()
    DIGITSANDPUNCTUATION = auto()
    URL = auto()
    EMAIL = auto()
    PHONENUMBER = auto()
    DIGITS = auto()

class SpellCheckingOnTextInput(EnumBase):
    AUTO = auto()
    USE = auto()
    DONTUSE = auto()

class TableBehaviorOnHorizontalCompression(EnumBase):
    AUTO = auto()
    HIDEITEMSBYIMPORTANCE = auto()
    MOVEITEMSBYIMPORTANCE = auto()

class TableCurrentRowUse(EnumBase):
    AUTO = auto()
    CHOICE = auto()
    SELECTIONPRESENTATION = auto()
    SELECTIONPRESENTATIONANDCHOICE = auto()

class TableFieldEditMode(EnumBase):
    DIRECTLY = auto()
    ENTER = auto()
    ENTERONINPUT = auto()

class TableHeightControlVariant(EnumBase):
    AUTO = auto()
    USEHEIGHTINFORMROWS = auto()
    USEHEIGHTINTABLEROWS = auto()
    USECONTENTHEIGHT = auto()

class TableInitialListView(EnumBase):
    BEGINNING = auto()
    END = auto()
    AUTO = auto()

class TableInitialTreeView(EnumBase):
    NOEXPAND = auto()
    EXPANDTOPLEVEL = auto()
    EXPANDALLLEVELS = auto()

class TableRepresentation(EnumBase):
    LIST = auto()
    HIERARCHICALLIST = auto()
    TREE = auto()

class TableRowInputMode(EnumBase):
    ENDOFLIST = auto()
    ENDOFWINDOW = auto()
    AFTERCURRENTROW = auto()
    BEFORECURRENTROW = auto()

class TableRowSelectionMode(EnumBase):
    CELL = auto()
    ROW = auto()

class TableScrollBarUse(EnumBase):
    DONTUSE = auto()
    USEALWAYS = auto()
    AUTOUSE = auto()

class TableSelectionMode(EnumBase):
    SINGLEROW = auto()
    MULTIROW = auto()

class TooltipRepresentation(EnumBase):
    AUTO = auto()
    NONE = auto()
    BALLOON = auto()
    BUTTON = auto()
    SHOWAUTO = auto()
    SHOWTOP = auto()
    SHOWLEFT = auto()
    SHOWBOTTOM = auto()
    SHOWRIGHT = auto()

class UsualGroupBehavior(EnumBase):
    USUAL = auto()
    COLLAPSIBLE = auto()
    POPUP = auto()

class UsualGroupControlRepresentation(EnumBase):
    TITLEHYPERLINK = auto()
    PICTURE = auto()

class UsualGroupRepresentation(EnumBase):
    NONE = auto()
    STRONGSEPARATION = auto()
    WEAKSEPARATION = auto()
    NORMALSEPARATION = auto()
    GROUPBOX = auto()
    LINE = auto()
    MARGIN = auto()

class UsualGroupThroughAlign(EnumBase):
    USE = auto()
    DONTUSE = auto()
    AUTO = auto()

class VerticalAlign(EnumBase):
    TOP = auto()
    BOTTOM = auto()
    CENTER = auto()

class ViewScalingMode(EnumBase):
    AUTO = auto()
    NORMAL = auto()
    LARGE = auto()

class ViewStatusLocation(EnumBase):
    AUTO = auto()
    NONE = auto()
    TOP = auto()
    BOTTOM = auto()

class WarningOnEditRepresentation(EnumBase):
    SHOW = auto()
    DONTSHOW = auto()
    AUTO = auto()

class DataCompositionSettingsViewMode(EnumBase):
    ALL = auto()
    QUICKACCESS = auto()

class UseOutput(EnumBase):
    AUTO = auto()
    ENABLE = auto()
    DISABLE = auto()

class FontType(EnumBase):
    ABSOLUTE = auto()
    WINDOWSFONT = auto()
    STYLEITEM = auto()
    AUTOFONT = auto()

class StandardPeriodVariant(EnumBase):
    CUSTOM = auto()
    TODAY = auto()
    THISWEEK = auto()
    THISTENDAYS = auto()
    THISMONTH = auto()
    THISQUARTER = auto()
    THISHALFYEAR = auto()
    THISYEAR = auto()
    FROMBEGINNINGOFTHISWEEK = auto()
    FROMBEGINNINGOFTHISTENDAYS = auto()
    FROMBEGINNINGOFTHISMONTH = auto()
    FROMBEGINNINGOFTHISQUARTER = auto()
    FROMBEGINNINGOFTHISHALFYEAR = auto()
    FROMBEGINNINGOFTHISYEAR = auto()
    YESTERDAY = auto()
    LASTWEEK = auto()
    LASTTENDAYS = auto()
    LASTMONTH = auto()
    LASTQUARTER = auto()
    LASTHALFYEAR = auto()
    LASTYEAR = auto()
    LASTWEEKTILLSAMEWEEKDAY = auto()
    LASTTENDAYSTILLSAMEDAYNUMBER = auto()
    LASTMONTHTILLSAMEDATE = auto()
    LASTQUARTERTILLSAMEDATE = auto()
    LASTHALFYEARTILLSAMEDATE = auto()
    LASTYEARTILLSAMEDATE = auto()
    TOMORROW = auto()
    NEXTWEEK = auto()
    NEXTTENDAYS = auto()
    NEXTMONTH = auto()
    NEXTQUARTER = auto()
    NEXTHALFYEAR = auto()
    NEXTYEAR = auto()
    NEXTWEEKTILLSAMEWEEKDAY = auto()
    NEXTTENDAYSTILLSAMEDAYNUMBER = auto()
    NEXTMONTHTILLSAMEDATE = auto()
    NEXTQUARTERTILLSAMEDATE = auto()
    NEXTHALFYEARTILLSAMEDATE = auto()
    NEXTYEARTILLSAMEDATE = auto()
    TILLENDOFTHISWEEK = auto()
    TILLENDOFTHISTENDAYS = auto()
    TILLENDOFTHISMONTH = auto()
    TILLENDOFTHISQUARTER = auto()
    TILLENDOFTHISHALFYEAR = auto()
    TILLENDOFTHISYEAR = auto()
    LAST7DAYS = auto()
    NEXT7DAYS = auto()
    MONTH = auto()

class HandlerCallType(EnumBase):
    BEFORE = auto()
    AFTER = auto()
    OVERRIDE = auto()

class DefaultRepresentation(EnumBase):
    TEXT = auto()
    PICTURE = auto()
    TEXTPICTURE = auto()
    AUTO = auto()

class CommandKind(EnumBase):
    AUTO = auto()
    ADDED = auto()

class SpreadsheetDocumentPointerType(EnumBase):
    SPECIAL = auto()
    REGULAR = auto()

class AutoTimeMode(EnumBase):
    DONTUSE = auto()
    LAST = auto()
    FIRST = auto()
    CURRENTORLAST = auto()
    CURRENTORFIRST = auto()

class PostingModeUse(EnumBase):
    REGULAR = auto()
    REALTIME = auto()
    ASK = auto()
    AUTO = auto()

class AutoShowStateMode(EnumBase):
    AUTO = auto()
    DONTSHOW = auto()
    SHOW = auto()
    SHOWONCOMPOSITION = auto()

####

class DataCompositionConditionalAppearanceUse(EnumBase):
    USE = auto()
    DONTUSE = auto()

class DataCompositionSettingsItemViewMode(EnumBase):
    NORMAL = auto()
    QUICKACCESS = auto()
    INACCESSIBLE = auto()
    AUTO = auto()

class DataCompositionComparisonType(EnumBase):
    EQUAL = auto()
    NOTEQUAL = auto()
    LESS = auto()
    LESSOREQUAL = auto()
    GREATER = auto()
    GREATEROREQUAL = auto()
    CONTAINS = auto()
    INLIST = auto()
    INLISTBYHIERARCHY = auto()
    INHIERARCHY = auto()
    NOTCONTAINS = auto()
    NOTINLIST = auto()
    NOTINLISTBYHIERARCHY = auto()
    NOTINHIERARCHY = auto()
    FILLED = auto()
    NOTFILLED = auto()
    BEGINSWITH = auto()
    NOTBEGINSWITH = auto()
    LIKE = auto()
    NOTLIKE = auto()

class DataCompositionFilterApplicationType(EnumBase):
    ITEMS = auto()
    HIERARCHY = auto()
    HIERARCHYONLY = auto()

class DataCompositionFilterItemsGroupType(EnumBase):
    ANDGROUP = auto()
    ORGROUP = auto()
    NOTGROUP = auto()

#endregion forms
