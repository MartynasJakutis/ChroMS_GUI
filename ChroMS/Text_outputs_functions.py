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
                                                                        f"Did You mean one of these values:\n{compared_to_wvs[1:-1]}?")}