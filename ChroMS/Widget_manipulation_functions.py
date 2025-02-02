import tkinter as tk
import os
import time

from HPLC_MS_data_classes import HPLC_3D_Data, MS_Data

import Text_outputs_functions as tof
import Main_GUI_parameters as mgp

def write_output_type_n_text(outputs_dict, key, output_object):
    """Uses output dictionary whose text is inserted into Outputwidget using specific output type."""
    out_type, out_text = outputs_dict[key]
    output_object.insert_text(text = out_text, output_type = out_type)

def get_path(folder, file):
    """Returns path consisting of folder and file. folder, file - str."""
    return os.path.join(folder, file)

def create_dir_if_not_present(dir_name, parent_dir = os.getcwd()):
    """Creates a directory in specific parent_dir if the dir_name is not present there.
    dir_name, parent_dir - str."""
    if dir_name not in os.listdir(parent_dir):
        new_path = get_path(parent_dir, dir_name)
        os.mkdir(new_path)

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
                    hist_folder = "my_browsing_history", hist_file_name = "chrom", save_hist = True):
    """Updates combobox (also listbox) and saves combobox contents into history file."""
    combobox_object.get_select_option()
    if os.path.isdir(combobox_object.selected_folder):
        if save_hist:
            combobox_object.save(folder = hist_folder, name = hist_file_name)
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
    is_dir = os.path.isdir(folder)
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
    file_list = os.listdir(selected_folder)
    for file in file_list:
        condition4 = FILE_NAME_FILTER.lower() in file.lower()
        condition5 = fast_filter(symbol = "*", filter_str = FILE_NAME_FILTER.lower(),
                                 check_str = file.lower())
        
        if not FILE_EXT and any([condition4, condition5]):
            insert_to_listbox()
        else:
            is_folder = os.path.isdir(selected_folder + "\\"+ file)
            condition1 = "folder" in FILE_EXT and is_folder
            condition2 = any([ext in file for ext in FILE_EXT if (ext != "folder" and ext != "")])
            condition3 = all([("" in FILE_EXT) and (".txt" not in file) and not is_folder])
            if any([condition1, condition2, condition3]) and any([condition4, condition5]):
                insert_to_listbox()
    listbox_object.all_items = listbox_object.listbox.get(0, tk.END)


def folder_search(combobox_object, listbox_object, FILE_EXT, entry_object, output_object, hist_file_name):
    """Folder search through filedialog."""
    create_dir_if_not_present(dir_name = mgp.DATA_FOLDER_NAMES[0])
    folder = tk.filedialog.askdirectory(initialdir = mgp.DATA_FOLDER_NAMES[0])
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
    path = get_path(folder_name, file_name)
    return path, truncated_file_name

def get_nearest_wvs(possible_wavelengths, sq_differences, num = 10):
    nearest_wvs = []
    for i in range(num):
        nearest = possible_wavelengths[sq_differences == sq_differences.min()]
        
        nearest = nearest.min() if len(nearest) != 1 else nearest[0]
        
        not_nearest_poss_wvs = possible_wavelengths != nearest
        sq_differences = sq_differences[not_nearest_poss_wvs]
        possible_wavelengths = possible_wavelengths[not_nearest_poss_wvs]
        nearest_wvs.append(int(nearest))
    return sorted(nearest_wvs)

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
        nearest_values = get_nearest_wvs(possible_wavelengths, sq_differences, num = 10)
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

def txt_file_processing(combobox_object, listbox_object, plot_object, output_object, purpose, entry_object = None):
    """HPLC and MS data processing. Reads files, saves the data in data classes, draws diagrams and calculates time used to 
    complete these processes."""
    redraw_diagram_method_args = {}
    path, truncated_file_name = get_txt_file_path(combobox_object, 
                                                  listbox_object, purpose = purpose)
    data_classes = {"chrom" : {"class" : HPLC_3D_Data, "title_arg" : "title1"},
                    "ms1" : {"class" : MS_Data, "title_arg" : "title1"},
                    "ms2" : {"class" : MS_Data, "title_arg" : "title2"}}
    Data_Class = data_classes.get(purpose).get("class")
    file_title = data_classes.get(purpose).get("title_arg")
    data_class_args = {"file" : path}
    start_time_calc = time.time()
    if Data_Class == HPLC_3D_Data:
        data = Data_Class(**data_class_args)
        data.read()
        wv_exists = check_wv_presence(hplc_3d_data_object = data, entry_object = entry_object, output_object = output_object,
                                      plot_object = plot_object, purpose = purpose)
        if not wv_exists:
           return
        data.get_ab_intensity_of_wv(wave_nm = int(entry_object.entry.get()))
    elif Data_Class == MS_Data:
        data = Data_Class(**data_class_args)
        data.read()

    data_calc_text = f"""File: '{path}'\n Calc time: {time.time() - start_time_calc :.3f} s\n"""
    main_param_dict = {"state" : "not_initial"}
    if Data_Class == HPLC_3D_Data:
        dict_update = {"data_rt" : data.retention_time, "data_ab" : data.ab_intensity,
                       "data_wv_all" : data.wavelengths, "data_ab_all" : data.all_ab_intensities,
                       "data_wave_nm" : data.wave_nm, file_title : truncated_file_name}
    else:
        num = purpose[2]
        dict_update = {f"data_mz{num}" : data.mz, f"data_inten{num}" : data.absolute_intensity,
                       file_title : truncated_file_name + f"\t{data.retention_time} min.\t{data.ionization_type}"}
        redraw_diagram_method_args.update({"purpose" : purpose})

    main_param_dict.update(dict_update)
    
    start_time_draw = time.time()
    plot_object.set_main_param_values(**main_param_dict)
    plot_object.redraw_diagram(**redraw_diagram_method_args)
    data_draw_text = f"Draw time: {time.time() - start_time_draw :.3f} s"
    output_object.insert_text(text = data_calc_text + data_draw_text,
                              output_type = "success")
    listbox_object.listbox.focus_set()

def warning_output(outputs_dict, key, output_object, plot_object, purpose):
    """Outputs warning to output_object, sets plot_object state to 'initial'"""
    write_output_type_n_text(outputs_dict = outputs_dict, key = key,
                             output_object = output_object)
    if plot_object.state == "not_initial":
        if purpose == "chrom":
            set_chrom_plot_state_to_initial(plot_object)
        else:
            set_ms_plot_state_to_initial(plot_object, purpose)


def set_chrom_plot_state_to_initial(plot_object):
    """Sets chrom plot state to initials, replaces all the data with zeros and redraws the diagram."""
    plot_object.set_main_param_values(state = "initial", title1 = "", data_rt = 0, data_ab = 0, 
                                      data_wv_all = 0, data_ab_all = 0, data_wave_nm = 0)
    plot_object.redraw_diagram()

def set_ms_plot_state_to_initial(plot_object, purpose):
    """Sets ms plot state to initials, replaces all the data with zeros and redraws the diagram."""
    num = int(purpose[-1])
    title_par = f"title{num}"
    arg_dictionary = {f"data_mz{num}" : 0, f"data_inten{num}" : 0,
                      title_par : None}
    plot_object.set_main_param_values(state = "initial", **arg_dictionary)
    plot_object.redraw_diagram(purpose = purpose)

def select_file(combobox_object, listbox_object, plot_object, output_object, entry_object, purpose = "chrom"):
    """Selects file and removes 2 space symbols. Selected file is used for data processing. If thats not possible, will be
    raised exceptions and provided respective text output."""
    selected_file_dtype = {"chrom" : "HPLC 3D"}.get(purpose, "MS 2D")
    try :
        listbox_object.get_select_option()
        selected_file = listbox_object.selected_file[2:]
    except IndexError as indexerr:
        outputs_dict = tof.select_file_warnings(None, selected_file_dtype)
        warning_output(outputs_dict = outputs_dict, key = type(indexerr),
                       output_object = output_object, plot_object = plot_object, purpose = purpose)
    else:
        outputs_dict = tof.select_file_warnings(selected_file, selected_file_dtype)
        txt_f_processing_errors = list(outputs_dict.keys())
        txt_f_processing_errors.remove("OtherError")
        txt_f_processing_errors = tuple(txt_f_processing_errors)
        txt_file_processing(combobox_object = combobox_object, listbox_object = listbox_object, 
                                plot_object = plot_object, output_object = output_object, entry_object = entry_object,
                                purpose = purpose) 
        #try:
        #    txt_file_processing(combobox_object = combobox_object, listbox_object = listbox_object, 
        #                        plot_object = plot_object, output_object = output_object, entry_object = entry_object,
        #                        purpose = purpose)
        #except txt_f_processing_errors as err:
        #    warning_output(outputs_dict = outputs_dict, key = type(err),
        #                   output_object = output_object, plot_object = plot_object, purpose = purpose)
        #except:
        #    warning_output(outputs_dict = outputs_dict, key = "OtherError",
        #                   output_object = output_object, plot_object = plot_object, purpose = purpose)


def select_subplots(plot_object, listbox_object, purpose):
    """Changes number of shown subplots by redrawing diagram."""
    if purpose == "chrom":
        plot_object.redraw_diagram()
    else:
        plot_object.redraw_diagram(purpose = purpose)
    focus_and_activate_listbox(listbox_object)

def maintain_four_digit_integer(entry_object, is_startup = False):
    string = entry_object.entry.get()
    cursor_ind = entry_object.entry.index(tk.INSERT)        
    if is_startup and not string.isdigit():
        entry_object.change_entry_text(change_to = "254")
        return

    #is_not_digit = (not string.isdigit()) and string != ""
    #starting_0 = string.startswith("0") and len(string) > 1
    #more_than_4_sym = len(string) > 4
    #while is_not_digit or starting_0 or more_than_4_sym:
    #    is_not_digit = (not string.isdigit()) and string != ""
    #    starting_0 = string.startswith("0") and len(string) > 1
    #    more_than_4_sym = len(string) > 4
    #    if is_not_digit:
    #        string = string[ : cursor_ind - 1] + string[cursor_ind : ]
    #        change_entry_text(entry_object = entry_object, change_to = string)
    #        entry_object.entry.icursor(cursor_ind - 1)
    #    elif starting_0:
    #        while string.startswith("0") and len(string) != 1:
    #            string = string.replace("0", "", 1)
    #        change_entry_text(entry_object = entry_object, change_to = string)
    #        entry_object.entry.icursor(cursor_ind - 1)
    #    elif more_than_4_sym:
    #        ind = len(string) - 1 if cursor_ind > len(string) - 1 else cursor_ind
    #        string = string[: ind] + string[ind + 1: ]
    #        change_entry_text(entry_object = entry_object, change_to = string)
    #        entry_object.entry.icursor(ind)
    #    else:
    #        string = str(int(string)) if string != "" else ""
    #        change_entry_text(entry_object = entry_object, change_to = string)
    #        entry_object.entry.icursor(cursor_ind)

    if not string.isdigit():
        string = string[ : cursor_ind - 1] + string[cursor_ind : ]
        entry_object.change_entry_text(change_to = string)
        entry_object.entry.icursor(cursor_ind - 1)
    elif string.startswith("0") and len(string) > 1:
        while string.startswith("0") and len(string) != 1:
            string = string.replace("0", "", 1)
        entry_object.change_entry_text(change_to = string)
        entry_object.entry.icursor(cursor_ind - 1)
    elif len(string) > 4:
        ind = len(string) - 1 if cursor_ind > len(string) - 1 else cursor_ind
        string = string[: ind] + string[ind + 1: ]
        entry_object.change_entry_text(change_to = string)
        entry_object.entry.icursor(ind)
    else:
        string = str(int(string))
        entry_object.change_entry_text(change_to = string)
        entry_object.entry.icursor(cursor_ind)
    

def maintain_pos_neg_float(entry_object, is_startup = False):
    string = entry_object.entry.get()
    cursor_ind = entry_object.entry.index(tk.INSERT)  
    
    no_sep_minus = string.replace(".", "").replace("-", "")
    allowed_not_digits = ["", ".", "-", "-."]
    if not no_sep_minus.isdigit() and no_sep_minus not in allowed_not_digits:
        entry_object.change_entry_text(change_to = string[: cursor_ind - 1] + string[cursor_ind : ])
        entry_object.entry.icursor(cursor_ind - 1)
    elif string.count("-") == 1:
        entry_object.change_entry_text(change_to = "-" + string.replace("-", ""))
        entry_object.entry.icursor(cursor_ind)
    elif string.count("-") > 1:
        entry_object.change_entry_text(change_to = string.replace("-", ""))
        entry_object.entry.icursor(cursor_ind - 2)
    if string.count(".") > 1:
        first_sep_ind = string.index(".")
        last_sep_ind = string.index(".", first_sep_ind + 1)
        init_cursor_ind = cursor_ind - 1
        print(f"1st :{first_sep_ind}, lst: {last_sep_ind}, cur: {init_cursor_ind}")
        if init_cursor_ind == 0 and "-" in string:
            entry_object.change_entry_text(change_to = string.replace(".", "", 1))
        elif init_cursor_ind == first_sep_ind:
            entry_object.change_entry_text(change_to = string[::-1].replace(".", "", 1)[::-1])
        else:
            entry_object.change_entry_text(change_to = string.replace(".", "", 1))        
        entry_object.entry.icursor(cursor_ind - 1)
    elif "." in string and len(string.split(".")[1]) > 5:
        ind = len(string) - 1 if cursor_ind > len(string) - 1 else cursor_ind
        entry_object.change_entry_text(change_to = string[: ind] + string[ind + 1: ])
        entry_object.entry.icursor(ind)
