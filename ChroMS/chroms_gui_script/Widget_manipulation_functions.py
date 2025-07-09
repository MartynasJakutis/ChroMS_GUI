import tkinter as tk

from HPLC_MS_data_classes import HPLC_3D_Data, MS_Data
from time import (time as time_time)

import Text_outputs_functions as tof
import Main_GUI_parameters as mgp
import Path_manipulation_functions as pmf

def write_output_type_n_text(outputs_dict, key, output_object):
    """Uses output dictionary whose text is inserted into Outputwidget using specific output type."""
    out_type, out_text = outputs_dict[key]
    output_object.insert_text(text = out_text, output_type = out_type)

def fast_filter(symbol, filter_str, check_str):
    """Checks if filter_str is suitable to find check_str. Symbol is such character which indicates missing parts of the text or
    empty string. Inputs : symbol, filter_str, check_str - str. Output: has_all_fragments - bool."""
    if symbol in filter_str:
        str_list = filter_str.split(symbol)
        check_str_mod = check_str
        has_all_fragments = True
        for str_frag in str_list:
            if str_frag in check_str_mod:
                has_all_fragments = has_all_fragments and True
                check_str_trunc_methods = {True : (lambda : check_str_mod[check_str_mod.index(str_frag) : ]),
                                           False : (lambda : check_str_mod.split(str_frag, 1)[-1])}
                check_str_mod = check_str_trunc_methods[str_frag == '']()
            else:
                return False
        return has_all_fragments
    else:
        return False

def filter_file_extensions(combobox_object, listbox_object, checkbutton_obj, ext, FILE_EXT, entry_object):
    """Filters files inside listbox by file extensions and updates the combobox 
    (which updates the listbox respectively)."""
    if checkbutton_obj.var.get() == 1:
        if ext not in FILE_EXT:
            FILE_EXT.append(ext)
    else:
        if ext in FILE_EXT:
            FILE_EXT.remove(ext)
    update_combobox(combobox_object = combobox_object, listbox_object = listbox_object,
                    FILE_EXT = FILE_EXT, entry_object = entry_object, save_hist = False)
    focus_and_activate_listbox(listbox_object)

def filter_by_file_name(combobox_object, listbox_object, FILE_EXT, entry_object):
    """Filters files by file name and updates combobox (also listbox)."""
    entry_object.FILE_NAME_FILTER = entry_object.entry.get()
    update_combobox(combobox_object = combobox_object, listbox_object = listbox_object, 
                    FILE_EXT = FILE_EXT, entry_object = entry_object, save_hist = False)
    
def update_combobox(combobox_object, listbox_object, FILE_EXT, entry_object,
                    hist_file_name = "chrom", save_hist = True):
    """Updates combobox (also listbox) and saves combobox contents into history file."""
    combobox_object.get_select_option()
    if pmf.isdir(combobox_object.selected_folder):
        if save_hist:
            combobox_object.save(name = hist_file_name)
        file_search(combobox_object = combobox_object, listbox_object = listbox_object, FILE_EXT = FILE_EXT,
                    entry_object = entry_object)
    
def focus_and_activate_listbox(listbox_object):
    """Sets focus on the listbox. Also activate the first item if the listbox is 
    not empty and there is no selection."""
    current_sele = listbox_object.listbox.curselection()
    all_items = listbox_object.all_items
    if current_sele == () and all_items != ():
        listbox_object.listbox.select_set(0)
        listbox_object.listbox.activate(0)
    listbox_object.listbox.focus_force()

def mod_and_update_combobox(combobox_object, listbox_object, FILE_EXT, entry_object, folder, hist_file_name):
    """Adds value to combobox and updates combobox currently selected value."""
    combobox_object.add(folder)
    combobox_object.combobox.current(0)
    update_combobox(combobox_object = combobox_object, listbox_object = listbox_object,
                    FILE_EXT = FILE_EXT, entry_object = entry_object, hist_file_name = hist_file_name)
    
def check_dir_presence(combobox_object, listbox_object, FILE_EXT, entry_object,
                       outputs_dict, output_object, folder, hist_file_name):
    """Checks if directory is found and modifies combobox. 
    Returns is_dir - bool"""
    is_dir = pmf.isdir(folder) if folder != () else False
    if is_dir:
        mod_and_update_combobox(combobox_object, listbox_object, FILE_EXT, entry_object, folder, hist_file_name)
    else:
        listbox_object.clear()
        listbox_object.all_items = listbox_object.listbox.get(0, tk.END)
    write_output_type_n_text(outputs_dict = outputs_dict, key = is_dir, output_object = output_object)
    return is_dir

def file_search(combobox_object, listbox_object, FILE_EXT, entry_object):
    """File search by combobox item (path) and filters of file names and extensions.
    Updates listbox_object 'all_items' attribute."""
    FILE_NAME_FILTER = entry_object.FILE_NAME_FILTER
    def insert_to_listbox():
        listbox_object.listbox.insert(tk.END, "  " + file)
        
    selected_folder = combobox_object.selected_folder
    listbox_object.clear()
    file_list_unsorted = pmf.listdir(selected_folder)
    file_list = sorted(file_list_unsorted)
    for file in file_list:
        condition4 = FILE_NAME_FILTER.lower() in file.lower()
        condition5 = fast_filter(symbol = "*", filter_str = FILE_NAME_FILTER.lower(),
                                 check_str = file.lower())
        
        if not FILE_EXT and any([condition4, condition5]):
            insert_to_listbox()
        else:
            is_folder = pmf.isdir(pmf.get_path(selected_folder, file))
            condition1 = "folder" in FILE_EXT and is_folder
            condition2 = any([ext in file for ext in FILE_EXT if (ext != "folder" and ext != "")])
            condition3 = all([("" in FILE_EXT) and (".txt" not in file) and not is_folder])
            if any([condition1, condition2, condition3]) and any([condition4, condition5]):
                insert_to_listbox()
    listbox_object.all_items = listbox_object.listbox.get(0, tk.END)


def folder_search(combobox_object, listbox_object, FILE_EXT, entry_object, output_object, hist_file_name):
    """Folder search through filedialog."""
    pmf.create_dir_if_not_present(dir_name = mgp.DATA_FOLDER_NAMES[0])
    initial_search_dir = pmf.get_path(mgp.SCRIPT_PATH_FATHER, mgp.DATA_FOLDER_NAMES[0])
    folder = tk.filedialog.askdirectory(initialdir = initial_search_dir)
    outputs_dict = tof.load_folder_outputs_mod(folder)
    check_dir_presence(combobox_object = combobox_object, listbox_object = listbox_object, FILE_EXT = FILE_EXT,
                       entry_object = entry_object, outputs_dict = outputs_dict, output_object = output_object,
                       folder = folder, hist_file_name = hist_file_name)
    focus_and_activate_listbox(listbox_object)

def manual_folder_search(combobox_object, listbox_object, FILE_EXT, entry_object, output_object, hist_file_name):
    """Enables manual folder browsing by writing in combobox. 
    Not automatic, must be executed manualy by pressing button."""
    folder = combobox_object.combobox.get()
    outputs_dict = tof.load_folder_outputs(folder)
    is_dir = check_dir_presence(combobox_object = combobox_object, listbox_object = listbox_object, FILE_EXT = FILE_EXT,
                                entry_object = entry_object, outputs_dict = outputs_dict, output_object = output_object,
                                folder = folder, hist_file_name = hist_file_name)
    if is_dir:
        focus_and_activate_listbox(listbox_object)
        
def select_combobox_opt(combobox_object, listbox_object, output_object, hist_file_name, FILE_EXT, entry_object):
    """Defines events which occur by selecting combobox value from the dropdown menu."""
    combobox_object.get_select_option()
    selected_folder = combobox_object.selected_folder
    outputs_dict = tof.load_folder_outputs(selected_folder)
    is_dir = check_dir_presence(combobox_object = combobox_object, listbox_object = listbox_object, FILE_EXT = FILE_EXT,
                                entry_object = entry_object, outputs_dict = outputs_dict, output_object = output_object,
                                folder = selected_folder, hist_file_name = hist_file_name)
    file_search(combobox_object = combobox_object, listbox_object = listbox_object, FILE_EXT = FILE_EXT,
                entry_object = entry_object)
    focus_and_activate_listbox(listbox_object)

def get_txt_file_path(combobox_object, listbox_object, purpose = "chrom"):
    """Returns .txt file path and file name without extension."""
    file_name = listbox_object.selected_file[2:]
    ms_exts = ["_ms_+.txt", "_ms_-.txt"]
    end_of_txt_file = {"chrom" : ["_chrom.txt"],
                       "ms1" : ms_exts,
                       "ms2" : ms_exts}.get(purpose)
    end_of_txt_file.append(".txt")
    truncated_file_name = file_name
    for end in end_of_txt_file:
        truncated_file_name = truncated_file_name.replace(end, "")
    folder_name = combobox_object.selected_folder
    path = pmf.get_path(folder_name, file_name)
    return path, truncated_file_name

def get_nearest_values(possible_values, sq_differences, num = 10, ret_type = int):
    nearest_values = []
    for i in range(num):
        nearest = possible_values[sq_differences == sq_differences.min()]
        
        nearest = nearest.min() if len(nearest) != 1 else nearest[0]
        
        not_nearest_poss_values = possible_values != nearest
        sq_differences = sq_differences[not_nearest_poss_values]
        possible_values = possible_values[not_nearest_poss_values]
        nearest_values.append(ret_type(nearest))
    return sorted(nearest_values)

def check_wv_presence(hplc_3d_data_object, entry_object, output_object, plot_object, purpose):
    wavelength = entry_object.entry.get()
    if wavelength != "":
        wavelength = int(wavelength)
    else:
        errorkey, wv, compared_to_wvs, wv_min, wv_max = ("Empty", None, None, 
                                                         int(hplc_3d_data_object.wavelengths.min()),
                                                         int(hplc_3d_data_object.wavelengths.max()))
        outputs_dict = tof.set_wavelength_warnings(wv, compared_to_wvs, wv_min, wv_max)
        warning_output(outputs_dict = outputs_dict, key = errorkey,
                       output_object = output_object, plot_object = plot_object, purpose = purpose)
        return False
    
    if wavelength > hplc_3d_data_object.wavelengths.max() or wavelength < hplc_3d_data_object.wavelengths.min():
        compared_to_wavelengths = {wavelength > hplc_3d_data_object.wavelengths.max() : "too high",
                                   wavelength < hplc_3d_data_object.wavelengths.min() : "too low"}
        errorkey, compared_to_wvs, result = "Outside range", compared_to_wavelengths[True], False

    elif wavelength not in hplc_3d_data_object.wavelengths:
        possible_wavelengths = hplc_3d_data_object.wavelengths.copy()
        sq_differences = (hplc_3d_data_object.wavelengths - wavelength) ** 2
        nearest_values = get_nearest_values(possible_wavelengths, sq_differences, num = 10)
        errorkey, compared_to_wvs, result = "Not found", str(nearest_values)[1:-1], False
    else:
        result = True

    if result == False:
        wv, wv_min, wv_max = (wavelength, int(hplc_3d_data_object.wavelengths.min()), 
                              int(hplc_3d_data_object.wavelengths.max()))
        outputs_dict = tof.set_wavelength_warnings(wv, compared_to_wvs, wv_min, wv_max)
        warning_output(outputs_dict = outputs_dict, key = errorkey,
                       output_object = output_object, plot_object = plot_object, purpose = purpose)
    return result

def check_inten_min_max(entry_min, entry_max, output_object, plot_object, purpose):
    not_numbers = ["-", ".", "-.", ""]
    min_intensity, max_intensity = entry_min.entry.get(), entry_max.entry.get()
    min_isnum, max_isnum = min_intensity not in not_numbers, max_intensity not in not_numbers
    recommended_min, recommended_max = 0.00000, 1.00000
    if min_isnum and max_isnum:
        return True
    elif min_isnum:
        errorkey, provided, default, recommended = ("max", max_intensity, 
                                                    mgp.DEFAULT_MAX_INTENSITY, recommended_max)
    elif max_isnum:
        errorkey, provided, default, recommended = ("min", min_intensity, 
                                                    mgp.DEFAULT_MIN_INTENSITY, recommended_min)
    else:
        errorkey, provided, default, recommended = ("both", [min_intensity, max_intensity], 
                                                    [mgp.DEFAULT_MIN_INTENSITY, mgp.DEFAULT_MAX_INTENSITY], 
                                                    [recommended_min, recommended_max])
    outputs_dict = tof.set_intensity_warnings(provided, default, recommended)
    warning_output(outputs_dict = outputs_dict, key = errorkey,
                   output_object = output_object, plot_object = plot_object, purpose = purpose)
    return False

create_list_of_clean_values = lambda data_str : [x for x in data_str.split(",") if x != ""]

def rts_for_return(rts):
    if type(rts) == list:
        rts = ",".join(rts)
    rts_mod = rts if len(rts) <= 30 else rts[ : 30] + " (first 30 symbols)"
    return rts_mod

def create_pos_pm_dev_output(pos_ind, dev_ind, rt_pos_values, rt_dev_values):
    out_list = []
    for pos_i, dev_i in zip(pos_ind, dev_ind):
        out_list.append(rt_pos_values[pos_i] + "±" + rt_dev_values[dev_i])
    out_string = f"'{rts_for_return(rts = out_list)}'"
    return out_string

def calculate_only_dot_values(data_values):
    number_of_only_dots = 0
    for data_value in data_values:
        if data_value == ".":
            number_of_only_dots += 1
    return number_of_only_dots

def check_for_not_num_rt(rt_pos_str, rt_dev_str, rt_pos_values, rt_dev_values, for_ms = False):
    result = True    
    strings, values = (rt_pos_str, rt_dev_str), (rt_pos_values, rt_dev_values)
    poss_ent_names = ["'Find m/z 1'", "'Find m/z 2'"] if for_ms else ["'Peak positions'", "'Peak deviations'"]
    ent_names = [n for n, s in zip(poss_ent_names, strings) if s != None]
    used_strs = [x for x in strings if x != None]
    used_values = [x for x in values if x != []]

    are_not_num = [x.replace(".", "").replace(",", "") == "" for x in used_strs]
    are_dot_num = [calculate_only_dot_values(data_values = x) for x in used_values]
    ret_strings = [rts_for_return(x) for x in used_strs]
    
    cond1, cond2 = any([are_not_num[0], are_dot_num[0]]), False
    if len(used_strs) > 1:
        both_not_num, both_dot_num  = all(are_not_num), all(are_dot_num)
        pos_not_and_dev_dot, dev_not_and_pos_dot = are_not_num[0] and are_dot_num[1], are_not_num[1] and are_dot_num[0]
        both_entry_prob = [both_not_num, both_dot_num, pos_not_and_dev_dot, dev_not_and_pos_dot]
        cond2 = any([are_not_num[1], are_dot_num[1]])
    else:
        both_entry_prob = [False]

    if any(both_entry_prob):
        errorkey, entry_names, entry_values, dot_num = ("both", f"{ent_names[0]} and {ent_names[1]}", 
                                                        f"'{ret_strings[0]}' and '{ret_strings[1]}'",
                                                        f"({are_dot_num[0]} and {are_dot_num[1]})")
    elif cond1:
        errorkey, entry_names, entry_values, dot_num = "one", f"{ent_names[0]}", f"'{ret_strings[0]}'", f"({are_dot_num[0]})"
    elif cond2:
        errorkey, entry_names, entry_values, dot_num = "one", f"{ent_names[1]}", f"'{ret_strings[1]}'", f"({are_dot_num[1]})"
    else:
        result, errorkey, entry_names, entry_values, dot_num = (False,) + (None,) * 4
    warning_args = {"entry_names" : entry_names,
                    "entry_values" : entry_values,
                    "dot_num" : dot_num}
    return result, errorkey, warning_args

def check_rt_lengths(rt_pos_values, rt_dev_values):
    result = True
    len_rt_pos_values, len_rt_dev_values = len(rt_pos_values), len(rt_dev_values)
    e_pos, e_dev, e_pos_l, e_dev_l = "'Peak positions'", "'Peak deviations'", len_rt_pos_values, len_rt_dev_values
    if len_rt_dev_values == 1:
        errorkey = None
    elif len_rt_dev_values != len_rt_pos_values:
        result, errorkey = False, "!="
    else:
        errorkey = None
    warning_args = {"e_pos" : e_pos,
                    "e_dev" : e_dev,
                    "e_pos_l" : e_pos_l,
                    "e_dev_l" : e_dev_l} 
    return result, errorkey, warning_args

def get_toolo_toohi_rts(rt_pos_values, rt_pos_values_fl, min_rts, max_rts):
    too_hi_rts, too_lo_rts = [], []
    for entvals, entvals_fl, min_rt, max_rt in zip(rt_pos_values, rt_pos_values_fl, min_rts, max_rts):
        condition = any([x == None for x in (entvals, entvals_fl, min_rt, max_rt)])
        if condition:
            too_hi_rts.append([])
            too_lo_rts.append([])
            continue
        too_hi_rts.append([entval for entval, entval_fl in zip(entvals, entvals_fl) if entval_fl > max_rt])
        too_lo_rts.append([entval for entval, entval_fl in zip(entvals, entvals_fl) if entval_fl < min_rt])
    return too_hi_rts, too_lo_rts

def compare_mz_positions(mz_pos_values1, mz_pos_values_fl1, mz_pos_values2, mz_pos_values_fl2, ms_data_object, ms_diag_object, purpose):
    result = False
    other_mz_name_dict = {"ms1" : "mz2",
                          "ms2" : "mz1"}
    entry_names_init = ["'Find m/z 1'", "'Find m/z 2'"]
    poss_purposes = list(other_mz_name_dict.keys())
    mz_pos_values, mz_pos_values_fl = (mz_pos_values1, mz_pos_values2), (mz_pos_values_fl1, mz_pos_values_fl2) 
    
    curr_mz = ms_data_object.mz
    if type(curr_mz) != int:
        min_mz_curr, max_mz_curr = curr_mz.min(), curr_mz.max()
    else:
        min_mz_curr, max_mz_curr = (None,) * 2

    other_mz_name = other_mz_name_dict.get(purpose)
    other_mz = ms_diag_object.get_data_mz(mz = other_mz_name)

    if type(other_mz) != int:
        min_mz_othr, max_mz_othr = other_mz.min(), other_mz.max()
    else:
        min_mz_othr, max_mz_othr = (None,) * 2

    min_mzs = [min_mz_curr, min_mz_othr] if purpose == poss_purposes[0] else [min_mz_othr, min_mz_curr]
    max_mzs = [max_mz_curr, max_mz_othr] if purpose == poss_purposes[0] else [max_mz_othr, max_mz_curr]
    
    ret_ranges_dict = {k : f"{v1} – {v2}" for k, v1, v2 in zip(entry_names_init, min_mzs, max_mzs)}

    too_hi_mzs, too_lo_mzs = get_toolo_toohi_rts(rt_pos_values = mz_pos_values, rt_pos_values_fl = mz_pos_values_fl,
                                                 min_rts = min_mzs, max_rts = max_mzs)
    entry_names = [n for n, th, tl in zip(entry_names_init, too_hi_mzs, too_lo_mzs) if th != [] or tl != []]

    #normal_mzs = [n for n, th, tl in zip(entry_names_init, too_hi_mzs, too_lo_mzs) if th == [] and tl == []]
    
    mz_ranges_ret = [ret_ranges_dict.get(entry_name) for entry_name in entry_names]
 
    too_hi_mzs_ret = [f"'{rts_for_return(rts = x)}'" for x in too_hi_mzs]
    too_lo_mzs_ret = [f"'{rts_for_return(rts = x)}'" for x in too_lo_mzs]
    
    if len(entry_names) == 0:    
        result, errorkey = True, None
    elif len(entry_names) == 2:
        errorkey = "both"
    else:
        errorkey = entry_names[0]
    warning_args = {"entry_names" : entry_names_init,
                    "entry_names_term" : entry_names,
                    "too_hi" : too_hi_mzs_ret,
                    "too_lo" : too_lo_mzs_ret,
                    "mz_ranges" : mz_ranges_ret}    
    

    return result, errorkey, warning_args    

def compare_rt_positions(rt_pos_values, rt_pos_values_fl, hplc_3d_data_object):
    result = False
    entry_names = "'Peak positions'"
    
    min_rt, max_rt = hplc_3d_data_object.retention_time.min(), hplc_3d_data_object.retention_time.max()
    too_hi_rts, too_lo_rts = get_toolo_toohi_rts(rt_pos_values = [rt_pos_values], rt_pos_values_fl = [rt_pos_values_fl],
                                                 min_rts = [min_rt], max_rts = [max_rt])
    too_hi_rts, too_lo_rts = too_hi_rts[0], too_lo_rts[0]
    too_hi_rts_ret, too_lo_rts_ret = [f"'{rts_for_return(rts = x)}'" for x in [too_hi_rts, too_lo_rts]]
    

    if len(too_hi_rts) and len(too_lo_rts):
        errorkey = "both"
    elif len(too_hi_rts):
        errorkey = "too_hi"
    elif len(too_lo_rts):
        errorkey = "too_lo"
    else:
        result, errorkey = True, None
    warning_args = {"entry_names" : entry_names,
                    "too_hi" : too_hi_rts_ret,
                    "too_lo" : too_lo_rts_ret,
                    "lo" : min_rt,
                    "hi" : max_rt}    

    return result, errorkey, warning_args

def get_nearest_rt_values(bad_item_ind, rt_pos_values, rt_pos_values_fl, possible_rt_pos_values, num):
    output_str = ""
    for ind in bad_item_ind:
        sq_differences = (possible_rt_pos_values - rt_pos_values_fl[ind]) ** 2
        nearest_rts = get_nearest_values(possible_rt_pos_values, sq_differences, num = num, ret_type = float)
        output_str += rt_pos_values[ind] + " : " + str(list(nearest_rts))[1 : -1]
        output_str = output_str + "\n" if ind != bad_item_ind[-1] else output_str
    return output_str

def check_for_found_rt(rt_pos_values, rt_dev_values, rt_pos_values_fl, rt_dev_values_fl, hplc_3d_data_object):
    hplc_3d_data_object.get_max_ab_intensities_by_rts(rt_pos = rt_pos_values_fl, rt_dev = rt_dev_values_fl)
    attr_list = [hplc_3d_data_object.rt_pos_prob_ind, hplc_3d_data_object.rt_dev_prob_ind]
    entry_names = "'Peak positions'"
    if all([len(x) == 0 for x in attr_list]):
        result, errorkey, rt_values_out, nearest_rts = True, None, None, None
    else:
        result = False
        rt_values_out = create_pos_pm_dev_output(pos_ind = attr_list[0], dev_ind = attr_list[1],
                                                 rt_pos_values = rt_pos_values, rt_dev_values = rt_dev_values)

        errorkey = "=1" if all([len(x) == 1 for x in attr_list]) else ">1"
        num = 5 if all([len(x) == 1 for x in attr_list]) else 5
        nearest_rts = get_nearest_rt_values(bad_item_ind = attr_list[0], rt_pos_values = rt_pos_values,
                                            rt_pos_values_fl = rt_pos_values_fl,
                                            possible_rt_pos_values = hplc_3d_data_object.retention_time, num = num)
    warning_args = {"entry_names" : entry_names,
                    "rt_values_out" : rt_values_out,
                    "nearest_rts" : nearest_rts}

    return result, errorkey, warning_args

def find_and_set_ms_subplot_errors(errorkey, err_entry_names, plot_object):
    err_dict = {"'Find m/z 1'" : "subplot1",
                "'Find m/z 2'" : "subplot2"}
    if type(err_entry_names) == str:
        split_char = " and " if errorkey == "both" else "\t"
        err_entry_names = err_entry_names.split(split_char)
    #print(err_entry_names,errorkey)
    ms_subplot_errors = [err_dict.get(i) for i in err_entry_names]
    plot_object.subplot_errors = ms_subplot_errors
    #print(plot_object.subplot_errors)

def check_mz_presence(ms_data_object, entry_mz1, entry_mz2, output_object, plot_object, purpose):
    plot_object.subplot_errors = []
    result, outputs_dict, mz1_values, mz2_values, mz1_values_fl, mz2_values_fl = (False,) + (None,) * 5
    are_no_num_found, is_pos_str_not_empty, are_values_in_range, are_all_values_found = (True,) + (False,) * 3
    mz1_str, mz2_str = [x.entry.get() for x in [entry_mz1, entry_mz2]]
    disabled_entries = [str(x.entry.cget("state")) == str(tk.DISABLED) for x in [entry_mz1, entry_mz2]]
    strings = [s if not d else "" for s, d in zip([mz1_str, mz2_str], disabled_entries)]
    empty_entries = strings == ["", ""]
    if empty_entries or all(disabled_entries):
        is_pos_str_not_empty = False
    else:
        is_pos_str_not_empty = True
        mz1_str, mz2_str = [x if x != "" else None for x in strings]
        #mz1_str, mz1_values = [x if x not in ["", []] else None for x in [mz1_str, mz1_values]]
        #mz2_str, mz2_values = [x if x not in ["", []] else None for x in [mz2_str, mz2_values]]

    if is_pos_str_not_empty:
        mz1_values, mz2_values = [create_list_of_clean_values(data_str = x) for x in strings]
        are_no_num_found, errorkey, warning_args = check_for_not_num_rt(rt_pos_str = mz1_str, rt_dev_str = mz2_str,
                                                                        rt_pos_values = mz1_values, rt_dev_values = mz2_values,
                                                                        for_ms = True)
        err_entry_names = warning_args.get("entry_names")
    else:
        return None, mz1_values_fl, mz2_values_fl, None, None
    
    if not are_no_num_found:
        mz1_values_fl, mz2_values_fl = [list(map(float, x)) if x != None else None for x in [mz1_values, mz2_values]]
        are_values_in_range, errorkey, warning_args = compare_mz_positions(mz1_values, mz1_values_fl, mz2_values, 
                                                                           mz2_values_fl, ms_data_object, plot_object, 
                                                                           purpose)
        err_entry_names = warning_args.pop("entry_names_term")
    else:
        find_and_set_ms_subplot_errors(errorkey, err_entry_names, plot_object)
        outputs_dict = tof.set_peaks_warnings_not_num(**warning_args) if not outputs_dict else outputs_dict

    if are_values_in_range:
        result, errorkey, warning_args = True, None, None
    else:
        find_and_set_ms_subplot_errors(errorkey, err_entry_names, plot_object)
        outputs_dict = tof.set_peaks_warnings_val_mz(errorkey, **warning_args) if not outputs_dict else outputs_dict

    #if result == False:
    #    warning_output(outputs_dict = outputs_dict, key = errorkey,
    #                   output_object = output_object, plot_object = plot_object, purpose = purpose, retain_data = True)
    for subplot in plot_object.subplot_errors:
        if subplot == "subplot1":
            mz1_values_fl = []
        elif subplot == "subplot2":
            mz2_values_fl = []
    return result, mz1_values_fl, mz2_values_fl, outputs_dict, errorkey

def check_rt_presence(hplc_3d_data_object, entry_pos, entry_dev, output_object, plot_object, purpose):
    result, outputs_dict, rt_pos_values, rt_dev_values = False, None, None, None
    are_no_num_found, is_pos_str_not_empty, are_compatible_len, are_values_in_range, are_all_values_found = (True,) + (False,) * 4
    rt_pos_str, rt_dev_str = [x.entry.get() for x in [entry_pos, entry_dev]]
    disabled_entries = [str(x.entry.cget("state")) == str(tk.DISABLED) for x in [entry_pos, entry_dev]]
    strings = [s for s, d in zip([rt_pos_str, rt_dev_str], disabled_entries) if not d]
    empty_entries = rt_pos_str == ""
    if empty_entries or all(disabled_entries):
        is_pos_str_not_empty = False
    else:
        is_pos_str_not_empty = True

    if is_pos_str_not_empty:
        rt_pos_values, rt_dev_values = [create_list_of_clean_values(data_str = x) for x in strings]
        are_no_num_found, errorkey, warning_args = check_for_not_num_rt(rt_pos_str = rt_pos_str, rt_dev_str = rt_dev_str,
                                                                        rt_pos_values = rt_pos_values, rt_dev_values = rt_dev_values,
                                                                        for_ms = False)
    else:
        return None, rt_pos_values, rt_dev_values
    
    if not are_no_num_found:
        are_compatible_len, errorkey, warning_args = check_rt_lengths(rt_pos_values = rt_pos_values,
                                                                      rt_dev_values = rt_dev_values)
    else:
        outputs_dict = tof.set_peaks_warnings_not_num(**warning_args) if not outputs_dict else outputs_dict

    if are_compatible_len:
        rt_pos_values_fl, rt_dev_values_fl = [list(map(float, x)) if x != None else None for x in [rt_pos_values, rt_dev_values]]
        are_values_in_range, errorkey, warning_args = compare_rt_positions(rt_pos_values, rt_pos_values_fl, hplc_3d_data_object)

    else:
        outputs_dict = tof.set_peaks_warnings_len(**warning_args) if not outputs_dict else outputs_dict

    if are_values_in_range:
        are_all_values_found, errorkey, warning_args = check_for_found_rt(rt_pos_values = rt_pos_values, rt_dev_values = rt_dev_values,
                                                                          rt_pos_values_fl = rt_pos_values_fl, 
                                                                          rt_dev_values_fl = rt_dev_values_fl,
                                                                          hplc_3d_data_object = hplc_3d_data_object)
    else:
        outputs_dict = tof.set_peaks_warnings_val(**warning_args) if not outputs_dict else outputs_dict

    if are_all_values_found:
        result = True
    else:
        outputs_dict = tof.set_peaks_warnings_notf(**warning_args) if not outputs_dict else outputs_dict

    if result == False:
        warning_output(outputs_dict = outputs_dict, key = errorkey,
                       output_object = output_object, plot_object = plot_object, purpose = purpose, retain_data = False)
    return result, rt_pos_values, rt_dev_values

def limit_processing(limits):
    new_limits = [float(limit) if limit != "" else None for limit in limits]
    if new_limits[0] == new_limits[1] and new_limits != [None, None]:
        if new_limits[0] == 0:
            new_limits[0], new_limits[1] = new_limits[0] - 1, new_limits[1] + 1
        elif new_limits[0] > 0:
            new_limits[0], new_limits[1] = new_limits[0] * 0.95, new_limits[1] * 1.05
        else:
            new_limits[0], new_limits[1] = new_limits[0] * 1.05, new_limits[1] * 0.95
    return new_limits
        
def x_y_limit_processing(x_min, x_max, y_min, y_max):
    x_limits = limit_processing(limits = [x_min, x_max])
    y_limits = limit_processing(limits = [y_min, y_max])
    return x_limits, y_limits

def check_axis_limits(x_min, x_max, y_min, y_max, output_object, plot_object, purpose):
    not_numbers = ["-", ".", "-."]
    lim_not_num = lambda x : x in not_numbers
    entry_names = {"'X min'" : x_min, "'X max'" : x_max,
                   "'Y min'" : y_min, "'Y max'" : y_max}
    problem_vals = {k : f"'{v}'" for k, v in entry_names.items() if lim_not_num(v)}
    if not len(problem_vals):
        result, errorkey = True, None
    else:
        result = False
        errorkey = "one" if len(problem_vals) == 1 else "more"
    
    if result == False:
        outputs_dict = tof.set_limits_prohibited_vals(errorkey = errorkey, problem_vals = problem_vals)
        warning_output(outputs_dict = outputs_dict, key = errorkey,
                       output_object = output_object, plot_object = plot_object, purpose = purpose)
    
    return result

def hplc_3d_data_checking(data, entry_objects, output_object, plot_object, purpose):
    wv_exists = check_wv_presence(hplc_3d_data_object = data, entry_object = entry_objects["wv"], 
                                      output_object = output_object,
                                      plot_object = plot_object, purpose = purpose)
    if not wv_exists:
        return False
        
    data.get_ab_intensity_of_wv(wave_nm = int(entry_objects["wv"].entry.get()))
    inten_min_max_are_num = check_inten_min_max(entry_min = entry_objects["inten_min"], entry_max = entry_objects["inten_max"],
                                                    output_object = output_object, plot_object = plot_object, purpose = purpose)
    if not inten_min_max_are_num:
        return False
    intensity_min = float(entry_objects["inten_min"].entry.get())
    intensity_max = float(entry_objects["inten_max"].entry.get())
    intensities = [intensity_min, intensity_max]

    rt_exists, rt_pos_values, rt_dev_values = check_rt_presence(hplc_3d_data_object = data, entry_pos = entry_objects["peak_pos"],
                                                                entry_dev = entry_objects["peak_dev"], output_object = output_object,
                                                                plot_object = plot_object, purpose = purpose)
    if rt_exists == None:
        data.get_max_ab_intensities_by_rts(rt_pos = rt_pos_values, rt_dev = rt_dev_values)
        return True, intensities
    elif not rt_exists:
        return False
    return True, intensities


def txt_file_processing(combobox_object, listbox_object, plot_object, output_object, purpose, entry_objects,
                        ms_inten_radiobtn_val, mz_trim_radiobtn_val):
    """HPLC and MS data processing. Reads files, saves the data in data classes, draws diagrams and calculates time used to 
    complete these processes."""
    start_time_calc = time_time()
    err_text = ""
    mzs_text_str = ""
    main_param_dict = {}
    if purpose == "chrom":
        redraw_diagram_method_args, read_meth_args = {}, {}
    else:
        intensity_type_dict = {0 : "absolute",
                               1 : "absolute_scinot",
                               2 : "relative_perc",
                               3 : "relative_frac"}
        inten_type_num, is_trimming_on = ms_inten_radiobtn_val.get(), mz_trim_radiobtn_val.get()
        intensity_type = intensity_type_dict.get(inten_type_num)
        use_scinot = True if intensity_type == "absolute_scinot" else False
        redraw_diagram_method_args, read_meth_args = {"purpose" : purpose}, {"intensity_type" : intensity_type}

    path, truncated_file_name = get_txt_file_path(combobox_object, 
                                                  listbox_object, purpose = purpose)

    data_classes = {"chrom" : {"class" : HPLC_3D_Data, "title_arg" : "title1"},
                    "ms1" : {"class" : MS_Data, "title_arg" : "title1"},
                    "ms2" : {"class" : MS_Data, "title_arg" : "title2"}}
    Data_Class = data_classes.get(purpose).get("class")
    file_title = data_classes.get(purpose).get("title_arg")
    data_class_args = {"file" : path}

    data = Data_Class(**data_class_args)
    data.read(**read_meth_args)

    if Data_Class == HPLC_3D_Data:
        check_result = hplc_3d_data_checking(data, entry_objects, output_object, plot_object, purpose)
        if not check_result:
            return
        else:
            intensity_min, intensity_max = check_result[1]
        
    elif Data_Class == MS_Data:
        num = purpose[-1]
        rem_perc1, rem_perc2, ran_perc1, ran_perc2 = [int(entry_objects[i].entry.get()) if len(entry_objects[i].entry.get()) != 0 else None for i in 
                                                      ["trim_perc1", "trim_perc2", "gen_randnum_perc1", "gen_randnum_perc2"]]
        space_3, space_4 = " " * 3, " " * 4
        dict_update = {f"data_mz{num}" : data.mz, f"data_inten{num}" : data.intensity,
                       file_title : space_3 + truncated_file_name + f"{space_4}{data.retention_time} min.{space_4}{data.ionization_type}",
                       f"trimming_on{num}" : is_trimming_on, "rem_perc1" : rem_perc1, "rem_perc2" : rem_perc2,
                       "ran_perc1" : ran_perc1, "ran_perc2" : ran_perc2, f"use_scinot{num}" : use_scinot}
        redraw_diagram_method_args.update({"purpose" : purpose, "ms_error" : True})
        #print(rem_perc1, rem_perc2, ran_perc1, ran_perc2)
        main_param_dict.update(dict_update)
        plot_object.set_main_param_values(**main_param_dict)
        check_mz_presence_results = check_mz_presence(ms_data_object = data, entry_mz1 = entry_objects["find_mz1"],
                                                      entry_mz2 = entry_objects["find_mz2"], output_object = output_object,
                                                      plot_object = plot_object, purpose = purpose)
        mz_exists, mz_pos_values1, mz_pos_values2, outputs_dict, errorkey = check_mz_presence_results
        if mz_exists == None:
            plot_object.get_nearest_mz_values(mzs1 = mz_pos_values1, mzs2 = mz_pos_values2)
            #data.get_max_ab_intensities_by_rts(rt_pos = rt_pos_values, rt_dev = rt_dev_values)
        elif not mz_exists:
            plot_object.get_nearest_mz_values(mzs1 = mz_pos_values1, mzs2 = mz_pos_values2)
            mzs_prov, mzs_calc = plot_object.get_nearest_mz_values(mzs1 = mz_pos_values1, mzs2 = mz_pos_values2)
            #print(mzs_prov, mzs_calc)
            mzs_text_str = get_text_mzs_prov_calc(mzs_prov, mzs_calc)
            out_type, out_text = outputs_dict[errorkey]
            err_text = out_text
        else:
            mzs_prov, mzs_calc = plot_object.get_nearest_mz_values(mzs1 = mz_pos_values1, mzs2 = mz_pos_values2)
            mzs_text_str = get_text_mzs_prov_calc(mzs_prov, mzs_calc)
            #print(mzs_prov, mzs_calc)

        
    if purpose != "chrom" and mz_exists == False:
        provided_xlim, provided_ylim = (None, None), (None, None)
    else:
        x_min, x_max, y_min, y_max = [entry_objects[x].entry.get() for x in ["x_min", "x_max", "y_min", "y_max"]]
        are_limits_correct = check_axis_limits(x_min = x_min, x_max = x_max, y_min = y_min, y_max = y_max, 
                                           output_object = output_object, plot_object = plot_object, purpose = purpose)
        if are_limits_correct:
            provided_xlim, provided_ylim = x_y_limit_processing(x_min, x_max, y_min, y_max)
        else:
            return

    if Data_Class == HPLC_3D_Data:
        dict_update = {"data_rt" : data.retention_time, "data_ab" : data.ab_intensity,
                       "data_wv_all" : data.wavelengths, "data_ab_all" : data.all_ab_intensities,
                       "data_wave_nm" : data.wave_nm,
                       "intensity_min" : intensity_min, "intensity_max" : intensity_max,
                       "peak_intensity" : data.max_ab_intensities, "peak_time" : data.rts_of_max_intensity,
                       "show_peak_text" : True, "show_peaks" : True, "peak_dec_num" : 3,
                       "provided_xlim" : provided_xlim, "provided_ylim" : provided_ylim,
                       file_title : truncated_file_name}
        main_param_dict.update(dict_update)
        plot_object.set_main_param_values(**main_param_dict)

    

    
    plot_object.set_main_param_values(**{"state" : "not_initial", "provided_xlim" : provided_xlim,
                                         "provided_ylim" : provided_ylim})
    calc_time = time_time() - start_time_calc    
    start_time_draw = time_time()
    plot_object.redraw_diagram(**redraw_diagram_method_args)
    draw_time = time_time() - start_time_draw

    return path, calc_time, draw_time, err_text, mzs_text_str

def get_spacing_correction_for_values(mzs):
    mzs_strs = [str(i) for i in mzs]
    nums_aft_dec = [len(i[i.index(".") + 1 : ]) for i in mzs_strs]
    max_nums_aft_dec = max(nums_aft_dec)
    spacing_corr = [max_nums_aft_dec - i for i in nums_aft_dec]
    return spacing_corr

def get_text_mzs_prov_calc(mzs_prov, mzs_calc):
    mzs_text_list = []
    mz_labels = [f"m/z {i}" for i in range(1,3)]
    for mz_label, mzs_p, mzs_c in zip(mz_labels, mzs_prov, mzs_calc):
        if any([x == [] for x in (mzs_p, mzs_c)]):
            continue
        mz_prov_lab, mz_calc_lab = [mz_label + " " + i for i in ("provided", "calculated")]
        mz_prov_l_spacing, mz_calc_l_spacing = len(mz_prov_lab) + 3, len(mz_calc_lab) + 5
        title = f"{mz_prov_lab:>{mz_prov_l_spacing}}{mz_calc_lab:>{mz_calc_l_spacing}}"
        mzs_text_list.append(title)
        
        mzs_p_corr = get_spacing_correction_for_values(mzs = mzs_p)
        mzs_c_corr = get_spacing_correction_for_values(mzs = mzs_c)
        
        for mz_p, mz_c, mz_p_corr, mz_c_corr in zip(mzs_p, mzs_c, mzs_p_corr, mzs_c_corr):
            mz_prov_v_spacing = mz_prov_l_spacing - mz_p_corr
            mz_calc_v_spacing = mz_calc_l_spacing - mz_c_corr + mz_p_corr
            mz_values = f"{mz_p:>{mz_prov_v_spacing}}{mz_c:>{mz_calc_v_spacing}}"
            mzs_text_list.append(mz_values)
        mzs_text_list.append("")
    mzs_text_str = "\n".join(mzs_text_list)
    return mzs_text_str

def get_message_about_run_pars(running_from_entry, purpose, entry_objects):
    def add_entry_msg_line(msg_dict, entry_name, var_type, ending, fixed_len = False):
        if fixed_len:
            entry_text = rts_for_return(entry_objects[entry_name].entry.get())
        else:
            entry_text = entry_objects[entry_name].entry.get()
        msg_dict[entry_name] = f"{var_type} was set to {entry_text} {ending}.\n"
    msg_dict = {}
    if purpose == "chrom":
        x_axis_dim, y_axis_dim = "min", "AU"
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "wv", var_type = "Wavelength", ending = "nm")
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "inten_min", var_type = "Minimum intensity", ending = "AU")
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "inten_max", var_type = "Maximum intensity", ending = "AU")
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "peak_pos", 
                           var_type = "Peak positions sequence", ending = "min", fixed_len = True)
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "peak_dev", 
                           var_type = "Peak deviations sequence", ending = "min", fixed_len = True)
        #msg_dict = {"wv_entry" : f"Wavelength was set to {}"}
    elif purpose in ["ms1", "ms2"]:
        x_axis_dim, y_axis_dim = "m/z", "units"
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "find_mz1",
                           var_type = "m/z 1 peak sequence", ending = x_axis_dim, fixed_len = True)
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "find_mz2", 
                           var_type = "m/z 2 peak sequence", ending = x_axis_dim, fixed_len = True)
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "trim_perc1", var_type = "Trim percentage 1", ending = "% of min m/z")
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "trim_perc2", var_type = "Trim percentage 2", ending = "% of min m/z")
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "gen_randnum_perc1", 
                           var_type = "Random number percentage 1", ending = "% of min m/z")
        add_entry_msg_line(msg_dict = msg_dict, entry_name = "gen_randnum_perc2",
                           var_type = "Random number percentage 2", ending = "% of min m/z")
    add_entry_msg_line(msg_dict = msg_dict, entry_name = "x_min", var_type = "X axis minimum", ending = x_axis_dim)
    add_entry_msg_line(msg_dict = msg_dict, entry_name = "x_max", var_type = "X axis maximum", ending = x_axis_dim)
    add_entry_msg_line(msg_dict = msg_dict, entry_name = "y_min", var_type = "Y axis minimum", ending = y_axis_dim)
    add_entry_msg_line(msg_dict = msg_dict, entry_name = "y_max", var_type = "Y axis maximum", ending = y_axis_dim)
    msg = msg_dict.get(running_from_entry, "")
    return msg
#rts_for_return(rts)

def make_file_processing_text_output(path, calc_time, draw_time, mod_text, err_text, output_object, plot_object, listbox_object, purpose):
    data_path_text = f"File: '{path}'\n"
    calc_draw_time = create_data_calc_draw_text(calc_time, draw_time)
    if mod_text:
        output_text = data_path_text + "\n" + mod_text + "\n" + calc_draw_time
    else:
        output_text = data_path_text + "\n" + calc_draw_time
    if not err_text:
        output_object.insert_text(text = output_text, output_type = "success")
    else:
        output_object.insert_text(text = output_text, output_type = "warning")
        set_ms_plot_state_to_initial(plot_object, purpose, retain_data = True)
    listbox_object.listbox.focus_set()

def append_to_output_text(mod_text, mzs_text_str, err_text):
    if mzs_text_str:
        mod_text += mzs_text_str        
    if err_text:
        mod_text += err_text + "\n"
    return mod_text

def select_file_by_click(combobox_object, listbox_object, plot_object, output_object, purpose, entry_objects = None, 
                         ms_inten_radiobtn_val = None, mz_trim_radiobtn_val = None, running_from_entry = None):
    process_results = txt_file_processing(combobox_object, listbox_object, plot_object, output_object, 
                                          purpose, entry_objects, ms_inten_radiobtn_val, mz_trim_radiobtn_val)
    if process_results == None:
        return
    else:
        path, calc_time, draw_time, err_text, mzs_text_str = process_results
        mod_text = get_message_about_run_pars(running_from_entry = running_from_entry, purpose = purpose, entry_objects = entry_objects)
        mod_text = append_to_output_text(mod_text, mzs_text_str, err_text)
    make_file_processing_text_output(path = path, calc_time = calc_time, draw_time = draw_time, mod_text = mod_text,
                                     err_text = err_text, output_object = output_object, plot_object = plot_object, 
                                     listbox_object = listbox_object, purpose = purpose)

def select_file_by_ms_inten_radiobtn(combobox_object, listbox_object, plot_object, output_object, purpose, entry_objects = None, 
                                     ms_inten_radiobtn_val = None, mz_trim_radiobtn_val = None):
    intensity_modes = {0 : {"text" : "ABSOLUTE (DEFAULT)", "EN" : "Absolute intensity", "LT" : "Absoliutus intensyvumas"},
                       1 : {"text" : "ABSOLUTE (SCINOT)", "EN" : "Absolute intensity", "LT" : "Absoliutus intensyvumas"},
                       2 : {"text" : "RELATIVE (%)", "EN" : "Relative intensity, %", "LT" : "Santykinis intensyvumas, %"},
                       3 : {"text" : "RELATIVE (FRACTION)", "EN" : "Relative intensity", "LT" : "Santykinis intensyvumas"}}
    pur_num = purpose[-1]
    intensity_mode_dict = intensity_modes.get(ms_inten_radiobtn_val.get())
    intensity_mode = intensity_mode_dict.get("text")
    ylabel_text = intensity_mode_dict.get("EN")
    mod_text = f"MS{pur_num} intensity was set to {intensity_mode}\n" 
    output_text = mod_text

    plot_object.set_main_param_values(**{f"ylabel{pur_num}" : ylabel_text})
    data_mz = plot_object.get_main_param_values(f"data_mz{pur_num}")[0]
    if type(data_mz) == int or plot_object.state == "initial":
        output_object.insert_text(text = output_text, output_type = "success")
        return
    
    process_results = txt_file_processing(combobox_object, listbox_object, plot_object, output_object, 
                                          purpose, entry_objects, ms_inten_radiobtn_val, mz_trim_radiobtn_val)
    
    if process_results == None:
        return
    else:
        path, calc_time, draw_time, err_text, mzs_text_str = process_results
        mod_text = append_to_output_text(mod_text, mzs_text_str, err_text)
    make_file_processing_text_output(path = path, calc_time = calc_time, draw_time = draw_time, mod_text = mod_text,
                                     err_text = err_text, output_object = output_object, plot_object = plot_object, 
                                     listbox_object = listbox_object, purpose = purpose)
    
def select_file_by_mz_trim_radiobtn(combobox_object, listbox_object, plot_object, output_object, purpose, entry_objects = None, 
                                    mz_trim_radiobtn_val = None, ms_inten_radiobtn_val = None):
    trimming_modes = {0 : "DISABLED",
                      1 : "ENABLED"}
    pur_num = purpose[-1]
    mod_text = f"Trimming of mzs{pur_num} values was set to {trimming_modes.get(mz_trim_radiobtn_val.get())}\n" 
    output_text = mod_text
    data_mz = plot_object.get_main_param_values(f"data_mz{pur_num}")[0]
    if type(data_mz) == int or plot_object.state == "initial":
        output_object.insert_text(text = output_text, output_type = "success")
        return
    process_results = txt_file_processing(combobox_object, listbox_object, plot_object, output_object, 
                                          purpose, entry_objects, ms_inten_radiobtn_val, mz_trim_radiobtn_val)
    if process_results == None:
        return
    else:
        path, calc_time, draw_time, err_text, mzs_text_str = process_results
        mod_text = append_to_output_text(mod_text, mzs_text_str, err_text)
    make_file_processing_text_output(path = path, calc_time = calc_time, draw_time = draw_time, mod_text = mod_text,
                                     err_text = err_text, output_object = output_object, plot_object = plot_object, 
                                     listbox_object = listbox_object, purpose = purpose)



def create_data_calc_draw_text(calc_time, draw_time):
    data_calc_text = f"""{"Calc time"}: {calc_time :>9.3f} s\n"""
    data_draw_text = f"""{"Draw time"}: {draw_time :>9.3f} s"""
    return data_calc_text + data_draw_text

def warning_output(outputs_dict, key, output_object, plot_object, purpose, retain_data = False):
    """Outputs warning to output_object, sets plot_object state to 'initial'"""
    write_output_type_n_text(outputs_dict = outputs_dict, key = key,
                             output_object = output_object)
    if plot_object.state == "not_initial":
        if purpose == "chrom":
            set_chrom_plot_state_to_initial(plot_object)
        else:
            set_ms_plot_state_to_initial(plot_object, purpose, retain_data = retain_data)


def set_chrom_plot_state_to_initial(plot_object):
    """Sets chrom plot state to initials, replaces all the data with zeros and redraws the diagram."""
    plot_object.set_main_param_values(state = "initial", title1 = "", data_rt = 0, data_ab = 0, 
                                      data_wv_all = 0, data_ab_all = 0, data_wave_nm = 0)
    plot_object.redraw_diagram()

def set_ms_plot_state_to_initial(plot_object, purpose, retain_data = False):
    """Sets ms plot state to initials, replaces all the data with zeros and redraws the diagram."""
    num = int(purpose[-1])
    if retain_data:
        plot_object.redraw_diagram(purpose = purpose, ms_error = True)
    else:
        arg_dictionary = {f"data_mz{num}" : 0, f"data_inten{num}" : 0,
                      f"title{num}" : None}
        plot_object.set_main_param_values(state = "initial", **arg_dictionary)
        plot_object.redraw_diagram(purpose = purpose)

def select_file(combobox_object, listbox_object, plot_object, output_object, entry_objects, purpose = "chrom", ms_inten_radiobtn_val = None,
                event_type = "click", mz_trim_radiobtn_val = None, running_from_entry = None):
    """Selects file and removes 2 space symbols. Selected file is used for data processing. If thats not possible, will be
    raised exceptions and provided respective text output."""
    select_file_func_args = {"combobox_object" : combobox_object, "listbox_object" : listbox_object, "plot_object" : plot_object,
                             "output_object" : output_object, "entry_objects" : entry_objects, "purpose" : purpose,
                             "ms_inten_radiobtn_val" : ms_inten_radiobtn_val, "mz_trim_radiobtn_val" : mz_trim_radiobtn_val}
    select_file_funcs = {"click" : lambda : select_file_by_click(**select_file_func_args, running_from_entry = running_from_entry),
                         "ms_inten_radiobtn" : lambda : select_file_by_ms_inten_radiobtn(**select_file_func_args),
                         "mz_trim_radiobtn" : lambda : select_file_by_mz_trim_radiobtn(**select_file_func_args),
                         "find_entry_radiobtn" : lambda : select_file_by_find_entry_radiobtn(**select_file_func_args),
                         "change_subplots_radiobtn": lambda : select_file_by_subplots_radiobtn(**select_file_func_args)}
    select_file_func = select_file_funcs.get(event_type)
    selected_file_dtype = {"chrom" : "HPLC 3D"}.get(purpose, "MS 2D")
    try:
        listbox_object.get_select_option()
        selected_file = listbox_object.selected_file[2:]
    except IndexError as indexerr:
        if select_file_func in [select_file_funcs.get(i) for i in ("ms_inten_radiobtn",
                                                                   "mz_trim_radiobtn")]:
          select_file_func()
          return
        else:
          outputs_dict = tof.select_file_warnings(None, selected_file_dtype)
          warning_output(outputs_dict = outputs_dict, key = type(indexerr),
                       output_object = output_object, plot_object = plot_object, purpose = purpose)
    else:
        outputs_dict = tof.select_file_warnings(selected_file, selected_file_dtype)
        txt_f_processing_errors = list(outputs_dict.keys())
        txt_f_processing_errors.remove("OtherError")
        txt_f_processing_errors = tuple(txt_f_processing_errors)
        #select_file_func()
        #try:
        #    select_file_func()
        #except txt_f_processing_errors as err:
        #    warning_output(outputs_dict = outputs_dict, key = type(err),
        #                   output_object = output_object, plot_object = plot_object, purpose = purpose)
        #except:
        #    warning_output(outputs_dict = outputs_dict, key = "OtherError",
        #                   output_object = output_object, plot_object = plot_object, purpose = purpose)


        try:
            select_file_func()
        except txt_f_processing_errors as err:
            warning_output(outputs_dict = outputs_dict, key = type(err),
                           output_object = output_object, plot_object = plot_object, purpose = purpose)
        except:
            #import traceback
            #traceback.print_exc()
            warning_output(outputs_dict = outputs_dict, key = "OtherError",
                           output_object = output_object, plot_object = plot_object, purpose = purpose)

        #try:
        #    select_file_func()
        #except Exception as e:
        #    import traceback
        #    traceback.print_exc()

def select_file_by_subplots_radiobtn(combobox_object, listbox_object, plot_object, output_object, purpose, entry_objects = None, 
                                    mz_trim_radiobtn_val = None, ms_inten_radiobtn_val = None):
    pur_num = purpose[-1]
    subplots_options = {0 : "BOTH",
                        1 : "SUBPLOT1",
                        2 : "SUBPLOT2"}
    data_dict = {"chrom" : {"data_name" : "data_rt", "redraw_method" : lambda x : x.redraw_diagram()},
                 "ms1" : {"data_name" : f"data_mz{pur_num}", "redraw_method" : lambda x : x.redraw_diagram(purpose = purpose, ms_error = True)},
                 "ms2" : {"data_name" : f"data_mz{pur_num}", "redraw_method" : lambda x : x.redraw_diagram(purpose = purpose, ms_error = True)}}
    selected_subplots = subplots_options.get(plot_object.radiobutton_var.get())

    mod_text = f"""Selection of subplots was changed to {selected_subplots}\n"""
    output_text = mod_text
    data_objects = data_dict.get(purpose)
    data_name = data_objects.get("data_name")
    redraw_diag = data_objects.get("redraw_method")
    #data = plot_object.get_main_param_values(data_name)[0]

    process_results = txt_file_processing(combobox_object, listbox_object, plot_object, output_object, 
                                          purpose, entry_objects, ms_inten_radiobtn_val, mz_trim_radiobtn_val)
    if process_results == None:
        redraw_diag(plot_object)
        return
    else:
        path, calc_time, draw_time, err_text, mzs_text_str = process_results
        mod_text = append_to_output_text(mod_text, mzs_text_str, err_text)
    make_file_processing_text_output(path = path, calc_time = calc_time, draw_time = draw_time, mod_text = mod_text,
                                     err_text = err_text, output_object = output_object, plot_object = plot_object, 
                                     listbox_object = listbox_object, purpose = purpose)

def select_subplots(plot_object, listbox_object, output_object, entry_objects, purpose):
    """Changes number of shown subplots by redrawing diagram."""
    only_drawing_and_time_output(plot_object, output_object, purpose)
    change_active_entries_and_radiobuttons(plot_object, entry_objects, purpose)
    focus_and_activate_listbox(listbox_object)

def change_active_entries_and_radiobuttons(plot_object, entry_objects, purpose):
    subplot_var_val = plot_object.get_main_param_values("radiobutton_var")[0].get()
    if subplot_var_val:
        pass
        #print(subplot_var_val)
        #print(entry_objects)

def select_file_by_find_entry_radiobtn(combobox_object, listbox_object, plot_object, output_object, purpose, entry_objects = None, 
                                       mz_trim_radiobtn_val = None, ms_inten_radiobtn_val = None):
    activity_modes = {str(tk.DISABLED) : "DISABLED",
                      str(tk.NORMAL) : "ENABLED"}
    pur_num = purpose[-1]

    if purpose == "chrom":
        kind_of_entry = "chromatogram peaks"
        entry_object = entry_objects["peak_pos"]
    else:
        kind_of_entry = f"m/z {pur_num} peaks"
        entry_object = entry_objects[f"find_mz{pur_num}"]

    entry_activity_mode = str(entry_object.entry.cget("state")) 
    activity_mode = activity_modes.get(entry_activity_mode)
    
    mod_text = f"Feature of showing {kind_of_entry} was set to {activity_mode}\n" 
    output_text = mod_text
    data_mz = plot_object.get_main_param_values(f"data_mz{pur_num}")[0]
    #if type(data_mz) == int or plot_object.state == "initial":
    #    output_object.insert_text(text = output_text, output_type = "success")
    #    return
    process_results = txt_file_processing(combobox_object, listbox_object, plot_object, output_object, 
                                          purpose, entry_objects, ms_inten_radiobtn_val, mz_trim_radiobtn_val)
    if process_results == None:
        return
    else:
        path, calc_time, draw_time, err_text, mzs_text_str = process_results
        mod_text = append_to_output_text(mod_text, mzs_text_str, err_text)
    make_file_processing_text_output(path = path, calc_time = calc_time, draw_time = draw_time, mod_text = mod_text,
                                     err_text = err_text, output_object = output_object, plot_object = plot_object, 
                                     listbox_object = listbox_object, purpose = purpose)

def select_file_depending_on_ffm(ffm_radiobtn_var, ffm, active_ffm, running_from_entry):
    ffm_radiobtn_val = ffm_radiobtn_var.get()
    select_file_args_dict = ffm.select_file_args_dict
    if running_from_entry == "find_mz1":
        is_current_ffm = ffm_radiobtn_val == 0
    elif running_from_entry == "find_mz2":
        is_current_ffm = ffm_radiobtn_val == 1
    select_file(**select_file_args_dict, event_type = "click",
                running_from_entry = running_from_entry)
    if not is_current_ffm:
        listbox_object = active_ffm.listbox
        focus_and_activate_listbox(listbox_object)

def only_drawing_and_time_output(plot_object, output_object, purpose, changing_entry_state = {}):
    start_time_calc = time_time()
    data_calc_text = f"""\n Calc time: {time_time() - start_time_calc :.3f} s\n"""
    start_time_draw = time_time()
    if purpose == "chrom":
        plot_object.redraw_diagram()
        kind_of_entry = "chromatogram peaks"
    else:
        kind_of_entry = f"m/z {purpose[-1]} peaks"
        plot_object.redraw_diagram(purpose = purpose, ms_error = True)
    data_draw_text = f"Draw time: {time_time() - start_time_draw :.3f} s"
    if changing_entry_state:
        first_line = f"""Feature of showing {kind_of_entry} is {changing_entry_state[True]}:"""
    else:
        first_line = f"""Selection of subplots was changed to "{plot_object.selected_subplots}":"""
    output_object.insert_text(text = first_line + data_calc_text + data_draw_text,
                              output_type = "success")

def eliminate_first_zeros(string, cursor_ind):
    is_normal_zero_float = string.startswith("0.") or string.startswith("-0.")
    if is_normal_zero_float:
        pass
    elif "." in string:
        temp_string = string[1 : ] if "-" in string else string
        cursor_ind = 1 if ("-" in string and cursor_ind - 1 == 0) else cursor_ind - 1
        while temp_string.startswith("0") and temp_string.find(".") != 1:
            temp_string = temp_string.replace("0", "", 1)
            string = "-" + temp_string if "-" in string else temp_string
    else: 
        temp_string = string[1 : ] if "-" in string else string
        while temp_string.startswith("0") and len(temp_string) != 1:
            temp_string = temp_string.replace("0", "", 1)
            string = "-" + temp_string if "-" in string else temp_string
        cursor_ind = 1 if "-" in string else cursor_ind - 1
    return string, cursor_ind    

def set_startup_num_value(entry_object, max_len, num_type, current_text, provided_clip, default_value):
    entry_object.change_entry_text_and_icursor(entry_text = "", cursor_ind = 0)
    if current_text != "":
        entry_object.paste(max_len = max_len, num_type = num_type, is_startup = True,
                           provided_clip = provided_clip, default_value = default_value)

def maintain_four_digit_integer(entry_object, is_startup = False, max_len = 4, default_value = "254"):    
    string = entry_object.entry.get()
    cursor_ind = entry_object.entry.index(tk.INSERT)        
    if is_startup:
        set_startup_num_value(entry_object = entry_object, max_len = max_len, num_type = "int",
                              current_text = string, provided_clip = string, default_value = default_value)
        return

    if not string.isdecimal():
        string = string[ : cursor_ind - 1] + string[cursor_ind : ]
        cursor_ind = cursor_ind - 1
    elif string.startswith("0") and len(string) > 1:
        string, cursor_ind = eliminate_first_zeros(string = string, cursor_ind = cursor_ind)
    elif len(string) > max_len:
        entry_object.maintain_entry_len(max_len = max_len, cursor_ind = cursor_ind, num_type = "int")
        string = entry_object.entry.get()
    else:
        string = str(int(string))
    entry_object.change_entry_text_and_icursor(entry_text = string, cursor_ind = cursor_ind)

def maintain_pos_neg_float(entry_object, is_startup = False, max_len = 5, default_value = "1.00000"):
    string = entry_object.entry.get()
    cursor_ind = entry_object.entry.index(tk.INSERT)  
    if is_startup:
        set_startup_num_value(entry_object = entry_object, max_len = max_len, num_type = "float",
                              current_text = string, provided_clip = string, default_value = default_value)
        return

    no_sep_minus = string.replace(".", "").replace("-", "")
    allowed_not_digits = ["", ".", "-", "-."]
    if not no_sep_minus.isdecimal() and no_sep_minus not in allowed_not_digits:
        string = string[: cursor_ind - 1] + string[cursor_ind : ]
        cursor_ind = cursor_ind - 1
    elif string.count("-") == 1:
        string = "-" + string.replace("-", "")
        cursor_ind = cursor_ind
    elif string.count("-") > 1:
        string = string.replace("-", "")
        cursor_ind = cursor_ind - 2
    if string.count(".") > 1:
        first_sep_ind = string.index(".")
        last_sep_ind = string.index(".", first_sep_ind + 1)
        init_cursor_ind = cursor_ind - 1
        if init_cursor_ind == 0 and "-" in string:
            string = string.replace(".", "", 1)
        elif init_cursor_ind == first_sep_ind:
            string = string[::-1].replace(".", "", 1)[::-1]
        else:
            string = string.replace(".", "", 1)
        
        if len(string.split(".")[1]) > max_len:
            string = string.split(".")[0] + "." + string.split(".")[1][ : max_len]
        cursor_ind = cursor_ind - 1
    elif "." in string and len(string.split(".")[1]) > max_len:
        entry_object.maintain_entry_len(max_len = max_len, cursor_ind = cursor_ind, num_type = "float")
        string = entry_object.entry.get()

    if (string.startswith("0") or string.startswith("-0")) and len(string.split(".")[0]) > 1:
        string, cursor_ind = eliminate_first_zeros(string = string, cursor_ind = cursor_ind)
    entry_object.change_entry_text_and_icursor(entry_text = string, cursor_ind = cursor_ind)

def maintain_pos_float_seq(entry_object, is_startup = False, max_len = 5, default_value = ""):
    string = entry_object.entry.get()
    cursor_ind = entry_object.entry.index(tk.INSERT)
    if is_startup:
        set_startup_num_value(entry_object = entry_object, max_len = max_len, num_type = "sequence",
                              current_text = string, provided_clip = string, default_value = default_value)
        return

    only_dec_point_or_comma = string.replace(",", "").replace(".", "") == ""
    if not string.replace(",", "").replace(".", "").isdecimal() and not only_dec_point_or_comma:
        string = string[: cursor_ind - 1] + string[cursor_ind : ]
        entry_object.change_entry_text_and_icursor(entry_text = string, cursor_ind = cursor_ind - 1)
    else:
        values = string.split(",")
        total_current_len = 0
        for i, value in enumerate(values):
            if value.count(".") > 1:
                first_sep_ind = value.index(".")
                last_sep_ind = value.index(".", first_sep_ind + 1)
                init_cursor_ind = cursor_ind - 1
                if init_cursor_ind - total_current_len == first_sep_ind:
                    value = value[::-1].replace(".", "", 1)[::-1]
                else:
                    value = value.replace(".", "", 1)
                cursor_ind -= 1
                if len(value.split(".")[1]) > max_len:
                    value = value.split(".")[0] + "." + value.split(".")[1][ : max_len]
            elif "." in value:
                if len(value.split(".")[1]) > max_len:
                    ind_aft_last = value.find(".") + max_len + 1
                    ind = ind_aft_last if cursor_ind - total_current_len == len(value) else cursor_ind - total_current_len
                    value = value[: ind] + value[ind + 1: ]
                    cursor_ind = ind + total_current_len                    
            if value.startswith("0") and len(value.split(".")[0]) > 1:
                value, cursor_ind = eliminate_first_zeros(string = value, cursor_ind = cursor_ind)
            values[i] = value
            total_current_len += len(value) + 1
            string = ",".join(values)
            entry_object.change_entry_text_and_icursor(entry_text = string, cursor_ind = cursor_ind)
