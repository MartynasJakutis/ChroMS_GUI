load_folder_outputs = lambda folder : {True : ("success", 
                                       f"""The folder\n"{folder}"\nwas loaded successfully."""),
                                       False : ("warning",
                                       f"""The folder\n"{folder}"\nwas not found.""")}
load_folder_outputs_mod = lambda folder : {True : ("success", 
                                           f"""The folder\n"{folder}"\nwas loaded successfully."""),
                                           False : ("warning",
                                           f"""Closing filedialog is not an option to select the folder.\nNice try.""")}

select_file_warnings = lambda file, file_type : {IndexError : ("warning", f"Choosing a blank space and expecting that a file " +\
                                                   f"was selected is not the best idea.\nNice try."),
                                                 PermissionError : ("warning", f"Chosen object\n'{file}'\nis not a proper file, " +\
                                                        f"most probably it is a folder."),
                                                 UnicodeDecodeError : ("warning", f"Chosen object\n'{file}'\nis not a proper file, " +\
                                                           f"because it cannot be decoded."),
                                                 UnboundLocalError : ("warning", f"Chosen object\n'{file}'\nis not a proper file, " +\
                                                           f"because it does not contain '{file_type}' data."),
                                                 AttributeError : ("warning", f"Chosen object\n'{file}'\nis not a proper file, " +\
                                                           f"because it contains '{file_type}' data which is corrupted."),
                                                 "OtherError" : ("warning", f"An unexpected error occured while opening object\n" +\
                                                     f"'{file}'.\nContact martynasjk@gmail.com to inform about this error.")}

set_wavelength_warnings = lambda wv, compared_to_wvs, wv_min, wv_max : {"Outside range" : ("warning", "The selected wavelength:\n" +\
                                                                                           f"{wv} nm is {compared_to_wvs}.\n" +\
                                                                                           f"Wavelength range {wv_min}–{wv_max} nm."),
                                                                        "Not found" : ("warning", "The selected wavelength:\n" +\
                                                                        f"{wv} nm is not found in the range {wv_min}–{wv_max} nm. " +\
                                                                        f"Did You mean one of these values:\n{compared_to_wvs}?"),
                                                                        "Empty" : ("warning", "There is no provided wavelength.\n" +\
                                                                        f"Use the provided wavelength range: {wv_min}–{wv_max} nm.")}

set_intensity_warnings = lambda provided, default, recommended : {"min" : ("warning", "The selected min intensity value is not valid:\n" +\
                                                                                      f"Used value: '{provided}' Use appropriate min intensity value:\n" +\
                                                                                      f"Default: '{default}' (Recommended: '{recommended}')"),
                                                                  "max" : ("warning", "The selected max intensity value is not valid:\n" +\
                                                                                      f"Used value: '{provided}' Use appropriate max intensity value:\n" +\
                                                                                      f"Default: '{default}' (Recommended: '{recommended}')"),
                                                                  "both" : ("warning", "The selected min and max intensity values are not valid:\n" +\
                                                                                       f"Used values: '{provided}' Use appropriate min and max intensity values:\n" +\
                                                                                       f"Default: '{default}' (Recommended: '{recommended}')")}

set_peaks_warnings_not_num = lambda entry_names, entry_values, dot_num : {"both" : ("warning", f"The provided values in {entry_names} entries are not valid:\n" +\
                                                                                      f"Used values: {entry_values}\n" +\
                                                                                      f"Use only integers and/or floating point numbers,\nremove separate '.' values {dot_num} " +\
                                                                                      f"and unnecessary ',' symbols."),
                                                                          "one" : ("warning", f"The provided values in {entry_names} entry are not valid:\n" +\
                                                                                      f"Used values: {entry_values}\n" +\
                                                                                      f"Use only integers and/or floating point numbers,\nremove separate '.' values {dot_num} " +\
                                                                                      f"and unnecessary ',' symbols.")}

set_peaks_warnings_len = lambda e_pos, e_dev, e_pos_l, e_dev_l : {"!=" : ("warning", f"The provided sequence length in {e_dev} entry is incorrect.\n" +\
                                                                  f"Length of {e_dev} sequence: {e_dev_l}\n" +\
                                                                  f"Length of {e_pos}   sequence: {e_pos_l}\n" +\
                                                                  f"Length of {e_dev} sequence must be 1 or equal to length of {e_pos} sequence.")}

set_peaks_warnings_val = lambda entry_names, too_hi, too_lo, lo, hi : {"both" : ("warning", f"The provided sequences in {entry_names} entry\n" +\
                                                                       f"include values outside the retention time range ({lo} - {hi} min).\n" +\
                                                                       f"Too high values:  {too_hi}\n" +\
                                                                       f"Too low  values:  {too_lo}."),
                                                                       "too_hi" : ("warning", f"The provided sequences in {entry_names} entry\n" +\
                                                                       f"include values outside the retention time range ({lo} - {hi} min).\n" +\
                                                                       f"Too high values:  {too_hi}."),
                                                                       "too_lo" : ("warning", f"The provided sequences in {entry_names} entry\n" +\
                                                                       f"include values outside the retention time range ({lo} - {hi} min).\n" +\
                                                                       f"Too low  values:  {too_lo}.")}

set_peaks_warnings_notf = lambda entry_names, rt_values_out, nearest_rts : {"=1" : ("warning", f"No data found for {entry_names} entry value and its deviation.\n" +\
                                                                            f"Problematic value : '{rt_values_out}'.\n" +\
                                                                            f"Try to change either deviation or the position value (as provided below):\n" +\
                                                                            f"{nearest_rts}."),
                                                                            ">1" : ("warning", f"No data found for {entry_names} entry values and their deviations.\n" +\
                                                                            f"Problematic values : '{rt_values_out}'.\n" +\
                                                                            f"Try to change either deviations or the position values (as provided below):\n" +\
                                                                            f"{nearest_rts}.")}

def set_limits_prohibited_vals(errorkey, problem_vals):
    msg_type = "warning"
    if errorkey == "one":
        first_line = f"The following entry includes a prohibited value."
    elif errorkey == "more":
        first_line = f"The following entries includes prohibited values."
    other_text = ""
    for i, (k, v) in enumerate(problem_vals.items()):
        additional_text = "\n" if i % 2 == 0 else ""
        appended_text = additional_text + k + " : " + v + " " * 10
        other_text += appended_text
    end_line = "\nUse only integers and/or floating point numbers."
    
    return {errorkey : (msg_type, first_line + other_text + end_line)}