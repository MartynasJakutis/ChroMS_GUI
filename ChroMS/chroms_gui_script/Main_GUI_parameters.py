from platform import (system as platform_system)
from Path_manipulation_functions import (get_absolute_script_path as pmf_get_absolute_script_path,
                                         get_path as pmf_get_path)

machine_os = platform_system()
if machine_os == "Windows":
    WINDOW_STATE = "zoomed"
    DEFAULT_LABEL_COLOR = "SystemButtonFace"
    DEFAULT_CONSOLE_SCHRIFT = "Consolas"
    DEFAULT_SCHRIFT = "TkDefaultFont"
    FONTSIZE_PRIMARY = 16
    FONTSIZE_SECONDARY = 14
    FONTSIZE_TERTIARY = 12
    FILE_SEARCH_ENTRY_WIDTH = 55
    FILE_LISTBOX_WIDTH = 70
    CONSOLE_WIDTH = 72
    FOLDER_COMBOBOX_WIDTH = 70
else:
    WINDOW_STATE = "normal"
    DEFAULT_LABEL_COLOR = "white"
    DEFAULT_CONSOLE_SCHRIFT = "fixed"
    DEFAULT_SCHRIFT = "helvetica"
    FONTSIZE_PRIMARY = 15
    FONTSIZE_SECONDARY = 13
    FONTSIZE_TERTIARY = 11
    FILE_SEARCH_ENTRY_WIDTH = 52
    FILE_LISTBOX_WIDTH = 60
    CONSOLE_WIDTH = 64
    FOLDER_COMBOBOX_WIDTH = 60

MY_BROWSING_HISTORY_DIRNAME = "my_browsing_history"
WINDOW_ICON_REL_PATH = pmf_get_path("icons", "ChroMS_icon.png")
DATA_FOLDER_NAMES = ["data"]

SCRIPT_PATH = pmf_get_absolute_script_path(output_parent_dir = False)
SCRIPT_PATH_FATHER = pmf_get_absolute_script_path()

WINDOW_ICON_PATH = pmf_get_path(SCRIPT_PATH, WINDOW_ICON_REL_PATH)

WINDOW_TITLE = "ChroMS_GUI"


TAB_1_NAME = "Blank Page"
HPLC_TAB_NAME = "HPLC"
MS_TAB_NAME = "MS"

DEFAULT_WAVELENGTH = "254"
DEFAULT_MIN_INTENSITY = "0.00000"
DEFAULT_MAX_INTENSITY = "1.00000"
DEFAULT_PEAK_POS_SEQ = ""
DEFAULT_PEAK_DEV_SEQ = "0.25"

DEFAULT_FIND_MZ1_SEQ = ""
DEFAULT_FIND_MZ2_SEQ = ""

DEFAULT_CHROM_X_MIN = ""
DEFAULT_CHROM_X_MAX = ""
DEFAULT_CHROM_Y_MIN = ""
DEFAULT_CHROM_Y_MAX = ""

DEFAULT_MS_X_MIN = ""
DEFAULT_MS_X_MAX = ""
DEFAULT_MS_Y_MIN = ""
DEFAULT_MS_Y_MAX = ""

DEFAULT_MZ_TRIM_PERC = "70"
DEFAULT_MZ_RANDNUM_PERC = "15"

LEN_4_DIGIT_INT = 4
LEN_5_DIGIT_INT = 5
LEN_5_DIGIT_FLOAT = 5

LEN_TIME_AFTER_DEC = 5
LEN_MZ_AFTER_DEC = 5

DEFAULT_MATPLOTLIB_STYLE_IDENTIFIERS = ["seaborn", "ticks"]
