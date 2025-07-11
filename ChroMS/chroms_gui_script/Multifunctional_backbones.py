﻿import tkinter as tk
from matplotlib import style as stl

from Object_manager_backbones import OutputPlotManagerBackbone, FileFolderManagerBackbone, OptionManagerBackbone
from HPLC_MS_diagram_classes import HPLC_Diagram, MS_Diagram
import Custom_tkinter_widget_classes as ctwc

import Widget_manipulation_functions as wmf

import Main_GUI_parameters as mgp

identifiers = mgp.DEFAULT_MATPLOTLIB_STYLE_IDENTIFIERS
check_for_identifiers = lambda name, ids : all([i in name for i in ids]) 

default_matplotlib_styles = [s for s in stl.available if check_for_identifiers(name = s, ids = identifiers)]
default_matplotlib_style = default_matplotlib_styles[0]

class MultifunctionalBackbone(object):
    """Class which has methods to create Output and Plot, File and Folder managers (opm, ffm), concatenate 
    them and provide additional functionality for them"""
    def __init__(self, window, screenheight, screenwidth, opm_master, purpose):
        self.window = window
        self.screenheight = screenheight
        self.screenwidth = screenwidth
        self.opm_master = opm_master
        self.purpose = purpose
        self.ffm_ms_radiobutton_variable = tk.IntVar(master = self.window, value = 0)
        self.curr_in_opt = False

    def create_output_plot_man(self):
        outpltman = OutputPlotManagerBackbone(master = self.opm_master, purpose = self.purpose)
        outpltman.create_all_widgets()
        return outpltman
        
    def create_file_folder_man(self, outpltman, purpose):
        """creates ffm of specific purpose and places it in the opm main frame."""
        master = outpltman.frames["main"]
        fifoman = FileFolderManagerBackbone(master = master, purpose = purpose, 
                                            ms_radiobutton_var = self.ffm_ms_radiobutton_variable)
        fifoman.create_all_widgets()
        fifoman.purpose = purpose
        return fifoman
    
    def create_option_man(self, outpltman, purpose):
        """creates om of specific purpose and places it in the opm main frame."""
        master = outpltman.frames["main"]
        oman = OptionManagerBackbone(master = master, purpose = purpose, 
                                     ms_radiobutton_var = self.ffm_ms_radiobutton_variable)
        oman.create_all_widgets()
        oman.purpose = purpose
        return oman

    def set_ms_radiobtn_frames_funcs(self):
        """Creates radiobuttons to select type of MS File"""
        if self.purpose == "ms":
            for ffm in self.ffms + self.oms:
                for i in ffm.ms_radiobutton_lf.radiobuttons.keys():
                    ffm.ms_radiobutton_lf.radiobuttons[i].radiobutton.config(command = self.change_ms_ffm_labelframe)

    def hide_obj_man_labelframes(self, to_hide):
        """Hides specified MS ffm labelframe"""
        for lf in to_hide.labelframes.keys():
            to_hide.labelframes[lf].grid_remove()
        
    def show_obj_man_labelframes(self, to_show):
        """Shows specified MS ffm labelframe"""
        for lf in to_show.labelframes.keys():
            to_show.labelframes[lf].grid()

    def config_subplots_radiobuttons(self, ffm_to_show):
        """Configures command of radiobuttons for subplot selection and changes listbox_object 
        parameter to listbox object present in ffm_to_show ffm."""
        for radiobutton in self.opm.radiobuttons.keys():
            self.opm.radiobuttons[radiobutton].radiobutton.config(command = lambda : self.change_subplots(select_file_args_dict = ffm_to_show.select_file_args_dict))

    def change_listbox_focus(self, ffm_to_show):
        """Sets focus on listbox widget."""
        listbox_object = ffm_to_show.listbox
        wmf.focus_and_activate_listbox(listbox_object)
    
    def change_obj_man_labelframes(self, to_hide, to_show):
        self.hide_obj_man_labelframes(to_hide)
        self.show_obj_man_labelframes(to_show)

    def go_ffm_to_options(self, ffm, om):
        self.curr_in_opt = True
        self.opm.labelframes["plot_opt"].grid_remove()
        self.change_obj_man_labelframes(to_hide = ffm, to_show = om)

    def go_options_to_ffm(self, om, ffm):
        self.curr_in_opt = False
        self.opm.labelframes["plot_opt"].grid()
        self.change_obj_man_labelframes(to_hide = om, to_show = ffm)
        self.change_listbox_focus(ffm_to_show = ffm)
        
    def set_ffm_to_options_btn_funcs(self):
        if self.purpose == "chrom":
            self.ffm1.to_options_btn.config(command = lambda : self.go_ffm_to_options(ffm = self.ffm1, om = self.om1))
        elif self.purpose == "ms":
            self.ffm1.to_options_btn.config(command = lambda : self.go_ffm_to_options(ffm = self.ffm1, om = self.om1))
            self.ffm2.to_options_btn.config(command = lambda : self.go_ffm_to_options(ffm = self.ffm2, om = self.om2))

    def set_options_to_ffm_btn_funcs(self):
        if self.purpose == "chrom":
            self.om1.to_ffm_btn.config(command = lambda : self.go_options_to_ffm(om = self.om1, ffm = self.ffm1))
        elif self.purpose == "ms":
            self.om1.to_ffm_btn.config(command = lambda : self.go_options_to_ffm(om = self.om1, ffm = self.ffm1))
            self.om2.to_ffm_btn.config(command = lambda : self.go_options_to_ffm(om = self.om2, ffm = self.ffm2))

    def change_ms_ffm_labelframe(self):
        """Replaces one MS ffm to another and deactivates radiobutton of 
        selecting subplots which corresponds to hidden ppm"""
        ffm_radiobtn_val = self.ffm_ms_radiobutton_variable.get()
        radiobtn_vals_and_labels = {0: {"om_to_hide" : self.om2, "om_to_show" : self.om1,
                                        "ffm_to_hide" : self.ffm2, "ffm_to_show" : self.ffm1,
                                        "activated_rb" : "radiobutton2", "deactivated_rb" : "radiobutton3",
                                        "subplot_to_draw" : "subplot1"},
                                    1: {"om_to_hide" : self.om1, "om_to_show" : self.om2,
                                        "ffm_to_hide" : self.ffm1, "ffm_to_show" : self.ffm2,
                                        "activated_rb" : "radiobutton3", "deactivated_rb" : "radiobutton2",
                                        "subplot_to_draw" : "subplot2"}}

        radiobtn_val_labels = radiobtn_vals_and_labels.get(ffm_radiobtn_val)
        om_to_hide, om_to_show = [radiobtn_val_labels.get(i) for i in ("om_to_hide", "om_to_show")]
        ffm_to_hide, ffm_to_show = [radiobtn_val_labels.get(i) for i in ("ffm_to_hide", "ffm_to_show")]
        rbtn_to_activate, rbtn_to_deactivate = [radiobtn_val_labels.get(i) for i in ("activated_rb", "deactivated_rb")]
        subplot_to_draw = radiobtn_val_labels.get("subplot_to_draw")
        self.config_subplots_radiobuttons(ffm_to_show = ffm_to_show)
        
        self.active_ffm = ffm_to_show
        if self.curr_in_opt:
            to_hide, to_show = om_to_hide, om_to_show
        else:
            to_hide, to_show = ffm_to_hide, ffm_to_show
            self.change_listbox_focus(ffm_to_show = ffm_to_show)
        self.change_obj_man_labelframes(to_hide = to_hide, to_show = to_show)
        self.change_active_subplot_radiobutton(rbtn_to_deactivate, rbtn_to_activate, ffm_to_show)
        self.change_entry_funcs(ffm_to_show = ffm_to_show)
    
    def change_active_subplot_radiobutton(self, rbtn_to_deactivate, rbtn_to_activate, ffm_to_show):
        opm_deact_radiobtn_val = self.opm.radiobutton_variable.get()
        current_radiobtn_val = self.opm.radiobuttons[rbtn_to_deactivate].onvalue
        self.opm.radiobuttons[rbtn_to_deactivate].disable()
        self.opm.radiobuttons[rbtn_to_activate].enable()
        if opm_deact_radiobtn_val == current_radiobtn_val:
            self.opm.radiobutton_variable.set(self.opm.radiobuttons[rbtn_to_activate].onvalue)
            self.change_subplots(select_file_args_dict = ffm_to_show.select_file_args_dict)
            #wmf.select_subplots(plot_object = self.opm.graph, output_object = self.opm.output,
            #                    listbox_object = ffm_to_show.listbox, entry_objects = self.opm.ctrl_entries,
            #                    purpose = ffm_to_show.purpose)
        

    def change_find_mz_entry_and_radiobtn_states(self):
        def get_entry_state(on_off_var, init_state):
            if on_off_var.get() and init_state == tk.NORMAL:
                return tk.NORMAL
            else:
                return tk.DISABLED

        find_mz_entries = [self.opm.find_mz1_entry, self.opm.find_mz2_entry]
        on_off_rbtn_vars = [self.opm.radiobutton_variable_on_off_mz1, self.opm.radiobutton_variable_on_off_mz2]
        radiobtns1 = ["radiobutton_on_mz1", "radiobutton_off_mz1"]
        radiobtns2 = ["radiobutton_on_mz2", "radiobutton_off_mz2"]
        entry_states0 = [get_entry_state(i,j) for i,j in zip(on_off_rbtn_vars, [tk.NORMAL, tk.NORMAL])]
        entry_states1 = [get_entry_state(i,j) for i,j in zip(on_off_rbtn_vars, [tk.NORMAL, tk.DISABLED])]
        entry_states2 = [get_entry_state(i,j) for i,j in zip(on_off_rbtn_vars, [tk.DISABLED, tk.NORMAL])]         

        subplot_states_dict = {0 : {"entries" : {k : v for k, v in zip(find_mz_entries, entry_states0)},
                                    "radiobtns" : {"enable" : radiobtns1 + radiobtns2, "disable" : []}},
                               1 : {"entries" : {k : v for k, v in zip(find_mz_entries, entry_states1)},
                                    "radiobtns" : {"enable" : radiobtns1, "disable" : radiobtns2}},
                               2 : {"entries" : {k : v for k, v in zip(find_mz_entries, entry_states2)},
                                    "radiobtns" : {"enable" : radiobtns2, "disable" : radiobtns1}}}

        subplot_radiobtn_value = self.opm.radiobutton_variable.get()
        entry_radiobtn_states_dict = subplot_states_dict.get(subplot_radiobtn_value)
        entry_state_dict = entry_radiobtn_states_dict.get("entries")
        radiobtns_state_dict = entry_radiobtn_states_dict.get("radiobtns")

        for entry in entry_state_dict:
            entry.entry.config(state = entry_state_dict[entry])

        for key in radiobtns_state_dict:
            for radiobtn in radiobtns_state_dict[key]:
                if key == "enable":
                    self.opm.radiobuttons_for_fe[radiobtn].enable()
                else:
                    self.opm.radiobuttons_for_fe[radiobtn].disable()

    def create_checkbuttons(self, ffm, hist_file_name):
        """Creates checkbuttons for file filtering by their extensions."""
        ext_name_dict = {"chrom" : "_chrom.txt",
                         "ms1" : "_ms_+.txt",
                         "ms2" : "_ms_-.txt"}
        texts_exts_func = lambda ext : {"text" : [f"{ext} files", ".txt files", "not .txt files", "folders"],
                                        "ext" : [f"{ext}", ".txt", "", "folder"]}
        default_ext = ext_name_dict.get(hist_file_name)
        texts_exts = texts_exts_func(default_ext)
        ffm.FILE_EXT.append(default_ext)
        texts = texts_exts.get("text")
        exts = texts_exts.get("ext")
        ffm.checkbuttons = {}
        ffm.checkbuttons[0] = ctwc.Checkbutton(master = ffm.frames["checkbutton"], text = texts[0],
                                               row = 0, column = 1, padx = 2.5, pady = 0, is_selected = True,
                                               command = lambda : wmf.filter_file_extensions(combobox_object = ffm.combobox,
                                                                                             listbox_object = ffm.listbox,
                                                                                             checkbutton_obj = ffm.checkbuttons[0],
                                                                                             ext = exts[0],
                                                                                             FILE_EXT = ffm.FILE_EXT,
                                                                                             entry_object = ffm.file_search_entry))
        ffm.checkbuttons[1] = ctwc.Checkbutton(master = ffm.frames["checkbutton"], text = texts[1],
                                               row = 0, column = 2, padx = 2.5, pady = 0, is_selected = False,
                                               command = lambda : wmf.filter_file_extensions(combobox_object = ffm.combobox,
                                                                                             listbox_object = ffm.listbox,
                                                                                             checkbutton_obj = ffm.checkbuttons[1], 
                                                                                             ext = exts[1],
                                                                                             FILE_EXT = ffm.FILE_EXT,
                                                                                             entry_object = ffm.file_search_entry))
        ffm.checkbuttons[2] = ctwc.Checkbutton(master = ffm.frames["checkbutton"], text = texts[2],
                                               row = 0, column = 3, padx = 2.5, pady = 0, is_selected = False, 
                                               command = lambda : wmf.filter_file_extensions(combobox_object = ffm.combobox,
                                                                                             listbox_object = ffm.listbox,
                                                                                             checkbutton_obj = ffm.checkbuttons[2], 
                                                                                             ext = exts[2],
                                                                                             FILE_EXT = ffm.FILE_EXT,
                                                                                             entry_object = ffm.file_search_entry))
        ffm.checkbuttons[3] = ctwc.Checkbutton(master = ffm.frames["checkbutton"], text = texts[3],
                                               row = 0, column = 4, padx = 2.5, pady = 0, is_selected = False,
                                               command = lambda : wmf.filter_file_extensions(combobox_object = ffm.combobox,
                                                                                             listbox_object = ffm.listbox,
                                                                                             checkbutton_obj = ffm.checkbuttons[3], 
                                                                                             ext = exts[3],
                                                                                             FILE_EXT = ffm.FILE_EXT,
                                                                                             entry_object = ffm.file_search_entry))
        for checkbutton in ffm.checkbuttons.values():
            checkbutton.create()
            
    def create_subplot_radiobuttons(self):
        """Creates radiobuttons for subplot selection"""
        self.opm.radiobuttons = {}
        self.opm.radiobutton_variable = tk.IntVar(master = self.window, value = 0)
        if self.purpose == "chrom":
            subplot1, subplot2 = "Heatmap", "Chromatogram"
        elif self.purpose == "ms":
            subplot1, subplot2 = "MS1", "MS2" 
        self.opm.radiobutton_pars_func = lambda subp1, subp2: {"radiobutton1" : {"text" : "Both subplots", "row" : 0,
                                                                                 "column" : 0, "onvalue" : 0},
                                                               "radiobutton2" : {"text" : f"Subplot1 ({subp1})", "row" : 0,
                                                                                 "column" : 1, "onvalue" : 1},
                                                               "radiobutton3" : {"text" : f"Subplot2 ({subp2})", "row" : 0,
                                                                                 "column" : 2, "onvalue" : 2}}
        self.opm.radiobutton_pars = self.opm.radiobutton_pars_func(subplot1, subplot2)
        for radiobutton in self.opm.radiobutton_pars.keys():
            self.opm.radiobuttons[radiobutton] = ctwc.Radiobutton(master = self.opm.frames["radiobutton"], padx = 2.5, pady = 0,
                                                             var = self.opm.radiobutton_variable, 
                                                             command = None,
                                                             **self.opm.radiobutton_pars[radiobutton])
            self.opm.radiobuttons[radiobutton].create()
    
    def create_radiobuttons_on_off_entry(self):
        """Creates radiobuttons for turning on or off the entry"""
        self.opm.radiobuttons_for_fe = {}
        if self.purpose == "chrom":
            master_frame = self.opm.frames["find_peaks"]
            self.opm.radiobutton_variable_on_off = tk.IntVar(master = self.window, value = 1)
            self.opm.radiobutton_on_off_pars = {"radiobutton_on" : {"master" : master_frame, "text" : "On", "row" : 0,
                                                               "column" : 4, "onvalue" : 1,
                                                               "var" : self.opm.radiobutton_variable_on_off,
                                           "command" : None},
                                           "radiobutton_off" : {"master" : master_frame, "text" : "Off", "row" : 0,
                                                                "column" : 5, "onvalue" : 0,
                                                                "var" : self.opm.radiobutton_variable_on_off,
                                           "command" : None}}

        elif self.purpose == "ms":
            master_frame1, master_frame2 = [self.opm.frames[x] for x in ("find_mz1", "find_mz2")]
            self.opm.radiobutton_variable_on_off_mz1 = tk.IntVar(master = self.window, value = 1)
            self.opm.radiobutton_variable_on_off_mz2 = tk.IntVar(master = self.window, value = 1)
            self.opm.radiobutton_on_off_pars = {"radiobutton_on_mz1" : {"master" : master_frame1, "text" : "On", "row" : 0,
                                                                   "column" : 1, "onvalue" : 1,
                                                                   "var" : self.opm.radiobutton_variable_on_off_mz1,
                                           "command" : None},
                                           "radiobutton_off_mz1" : {"master" : master_frame1, "text" : "Off", "row" : 0,
                                                                    "column" : 2, "onvalue" : 0,
                                                                    "var" : self.opm.radiobutton_variable_on_off_mz1,
                                           "command" : None},
                                           "radiobutton_on_mz2" : {"master" : master_frame2, "text" : "On", "row" : 0,
                                                                   "column" : 1, "onvalue" : 1,
                                                                   "var" : self.opm.radiobutton_variable_on_off_mz2,
                                           "command" : None},
                                           "radiobutton_off_mz2" : {"master" : master_frame2, "text" : "Off", "row" : 0,
                                                                    "column" : 2, "onvalue" : 0,
                                                                    "var" : self.opm.radiobutton_variable_on_off_mz2,
                                           "command" : None}}

        for radiobutton in self.opm.radiobutton_on_off_pars.keys():
            self.opm.radiobuttons_for_fe[radiobutton] = ctwc.Radiobutton(padx = 2.5, pady = 0, 
                                                             **self.opm.radiobutton_on_off_pars[radiobutton])
            self.opm.radiobuttons_for_fe[radiobutton].create()

    def enable_disable_mzs_trimming_entry(self, var, select_file_args_dict):
        trim_vars_n_entries = {self.om1.trim_radiobtn_variable == var : {"entries" : [self.om1.trim_perc_entry, self.om1.gen_randnum_perc_entry],
                                                                  "purpose" : "ms1"},
                               self.om2.trim_radiobtn_variable == var: {"entries" : [self.om2.trim_perc_entry, self.om2.gen_randnum_perc_entry],
                                                                  "purpose" : "ms2"}}
        entries, purpose = [trim_vars_n_entries.get(True).get(x) for x in ("entries", "purpose")]
        if var.get():
            state = tk.NORMAL
        else:
            state = tk.DISABLED
        for entry in entries:
            entry.entry.config(state = state)
        wmf.select_file(**select_file_args_dict, event_type = "mz_trim_radiobtn")
        self.change_listbox_focus(ffm_to_show = self.active_ffm)   

    def enable_disable_entry(self, var, select_file_args_dict, for_turning_on_off_entry = True):
        show_peaks_str = "show_peaks"        
        if self.purpose == "chrom":
            entries = [self.opm.peak_value_entry, self.opm.peak_dev_entry]
            purpose = self.purpose
        elif self.purpose == "ms":
            mz_variables = [self.opm.radiobutton_variable_on_off_mz1, self.opm.radiobutton_variable_on_off_mz2]
            mz_entries = [self.opm.find_mz1_entry, self.opm.find_mz2_entry]
            entry_dict = {var == var_mz : [ent] for var_mz, ent in zip(mz_variables, mz_entries)}
            purpose_dict = {var == var_mz : pur for var_mz, pur in zip(mz_variables, ["ms1", "ms2"])}
            entries = entry_dict.get(True)
            purpose = purpose_dict.get(True)
            show_peaks_str += purpose[-1]
        if var.get():
            state, str_state, show_peaks = tk.NORMAL, "ENABLED", True
        else:
            state, str_state, show_peaks = tk.DISABLED, "DISABLED", False
        self.opm.graph.set_main_param_values(**{show_peaks_str : show_peaks})
        
        for entry in entries:
            entry.entry.config(state = state)

        if for_turning_on_off_entry:
            wmf.select_file(**select_file_args_dict, event_type = "find_entry_radiobtn")
            self.change_listbox_focus(ffm_to_show = self.active_ffm)

    def change_subplots(self, select_file_args_dict):
        if select_file_args_dict["purpose"] in ["ms1", "ms2"]:
            self.change_find_mz_entry_and_radiobtn_states()
        wmf.select_file(**select_file_args_dict, event_type = "change_subplots_radiobtn")
        self.change_listbox_focus(ffm_to_show = self.active_ffm)

    def create_graph(self):
        self.opm.graph_params = {"dpi" : 100, "need_title1" : True, "title1" : "", "title1_pos" : (0.5, 0.95),
                            "title1_text_color" : "k", "title1_weight" : "bold", "title1_fontsize" : 13,
                            "xlabel1_pos" : (0.5, 0.05), "xlabel2_pos" : (0.5, 0.05),
                            "ylabel1_pos" : (0.02, 0.5), "ylabel2_pos" : (0.02, 0.5), 
                            "xlabel1_text_color" : "k", "xlabel2_text_color" : "k",
                            "ylabel1_text_color" : "k", "ylabel2_text_color" : "k",
                            "xlabel1_weight" : "bold", "xlabel2_weight" : "bold",
                            "ylabel1_weight" : "bold", "ylabel2_weight" : "bold",
                            "xlabel1_fontsize" : 14, "xlabel2_fontsize" : 14,
                            "ylabel1_fontsize" : 14, "ylabel2_fontsize" : 14,
                            "matplotlib_style1" : default_matplotlib_style, 
                            "matplotlib_style2" : default_matplotlib_style,
                            "master_labelframe" : self.opm.labelframes["chrom/ms"], 
                            "add_multiplier_w" : 0.98, "add_multiplier_h" : 0.90,
                            "radiobutton_var" : self.opm.radiobutton_variable, "state" : "initial", 
                            "screenheight" : self.screenheight, "screenwidth" : self.screenwidth,
                            "provided_xlim" : (None, None), "provided_ylim" : (None, None)}
        
        if self.purpose == "chrom":
            dict_update = {"xlabel1" : "Time, min", "xlabel2" : "Time, min",
                           "ylabel1" : "Wavelength\nλ, nm", "ylabel2" : "Absorption intensity, AU",
                           "colorbar_label" : "Intensity, AU", "colorbar_text_color" : "k",
                           "colorbar_weight" : "bold", "colorbar_fontsize" : 14,
                           "data_wave_nm" : 0, "data_rt" : 0, "data_ab" : 0, "data_ab_all" : 0, "data_wv_all" : 0,
                           "intensity_min" : 0, "intensity_max" : 1, "peak_intensity" : 0, "peak_time" : 0,
                           "peak_dec_num" : 3, "show_peak_text" : True, "show_peaks" : True}
            Used_Diagram = HPLC_Diagram
            
        elif self.purpose == "ms":
            dict_update = {"need_title2" : True, "title2" : "", "title2_pos" : (0.5, 0.95),
                           "title2_text_color" : "k", "title2_weight" : "bold", "title2_fontsize" : 13,
                           "xlabel1" : "m/z", "xlabel2" : "m/z",
                           "ylabel1" : "Absolute intensity", "ylabel2" : "Absolute intensity",
                           "data_mz1" : 0, "data_mz2" : 0, "data_inten1" : 0, "data_inten2" : 0,
                           "peak_dec_num" : 0, "show_peak_text1" : True, "show_peaks1" : True,
                           "show_peak_text2" : True, "show_peaks2" : True, "rem_perc1" : None, "rem_perc2" : None,
                           "ran_perc1" : None, "ran_perc2" : None, "trimming_on1" : False, "trimming_on2" : False,
                           "use_scinot1" : False, "use_scinot2" : False}
            Used_Diagram = MS_Diagram
            
        self.opm.graph_params.update(dict_update)
        self.opm.graph = Used_Diagram(**self.opm.graph_params)
        
        if Used_Diagram == HPLC_Diagram:
            plotting_funcs_dict = {"f_subplot1" : self.opm.graph.plotting_term_state_heat,
                                   "f_subplot2" : self.opm.graph.plotting_term_state_chrom}
        elif Used_Diagram == MS_Diagram:
            plotting_funcs_dict = {"f_subplot1" : self.opm.graph.plotting_term_state_ms1,
                                   "f_subplot2" : self.opm.graph.plotting_term_state_ms2}
        self.opm.graph.create_a_figure()
        self.opm.graph.set_term_state_plotting_funcs(**plotting_funcs_dict)
        self.opm.graph.draw_diagram()
        
    def update_backbone(self):
        """Updates ffm: loads browsing history to combobox and updates listbox."""
        for ffm, hist_file_name in zip(self.ffms, self.hist_file_names):
            ffm.combobox.set_history_folder(folder = mgp.MY_BROWSING_HISTORY_DIRNAME)
            ffm.combobox.load(name = hist_file_name)
            wmf.update_combobox(combobox_object = ffm.combobox, listbox_object = ffm.listbox,
                            FILE_EXT = ffm.FILE_EXT, entry_object = ffm.file_search_entry,
                            save_hist = False)

    def create_opm_with_widgets(self):
        self.opm = self.create_output_plot_man()
        self.create_subplot_radiobuttons()
        self.create_radiobuttons_on_off_entry()
        if self.purpose == "chrom":
            self.opm.wv_entry.bind_key_or_event(key_or_event = "<Control-v>", func = lambda event : ctwc.Entry.paste(self.opm.wv_entry,
                                                                                                                     max_len = mgp.LEN_4_DIGIT_INT, 
                                                                                                                     num_type = "int"))
            self.opm.inten_max_entry.bind_key_or_event(key_or_event = "<Control-v>", func = lambda event : ctwc.Entry.paste(self.opm.inten_max_entry, 
                                                                                                                     max_len = mgp.LEN_5_DIGIT_FLOAT, 
                                                                                                                     num_type = "float"))
            self.opm.inten_min_entry.bind_key_or_event(key_or_event = "<Control-v>", func = lambda event : ctwc.Entry.paste(self.opm.inten_min_entry,
                                                                                                                     max_len = mgp.LEN_5_DIGIT_FLOAT, 
                                                                                                                     num_type = "float"))
            self.opm.peak_value_entry.bind_key_or_event(key_or_event = "<Control-v>", func = lambda event : ctwc.Entry.paste(self.opm.peak_value_entry,
                                                                                                                     max_len = mgp.LEN_TIME_AFTER_DEC, 
                                                                                                                     num_type = "sequence"))
            self.opm.peak_dev_entry.bind_key_or_event(key_or_event = "<Control-v>", func = lambda event : ctwc.Entry.paste(self.opm.peak_dev_entry,
                                                                                                                     max_len = mgp.LEN_TIME_AFTER_DEC, 
                                                                                                                     num_type = "sequence"))
        self.create_graph()
    
    def concatenate_backbones(self):
        """Concatenates ffm/ffms and opm together."""
        self.create_opm_with_widgets()
        self.create_opm_entry_object_dict()
        if self.purpose == "chrom":
            self.ffm1 = self.create_file_folder_man(outpltman = self.opm, purpose = self.purpose)
            self.om1 = self.create_option_man(outpltman = self.opm, purpose = self.purpose)
            self.ffms, self.oms = [self.ffm1], [self.om1]
            self.hist_file_names = [self.purpose]
            self.hide_obj_man_labelframes(to_hide = self.om1)
        elif self.purpose == "ms":
            self.opm.radiobuttons["radiobutton3"].disable()
            self.ffm1 = self.create_file_folder_man(outpltman = self.opm, purpose = "ms1")
            self.ffm2 = self.create_file_folder_man(outpltman = self.opm, purpose = "ms2")
            #wmf.focus_and_activate_listbox(self.ffm2.listbox)
            self.om1 = self.create_option_man(outpltman = self.opm, purpose = "ms1")
            self.om2 = self.create_option_man(outpltman = self.opm, purpose = "ms2")
            self.ffms, self.oms = [self.ffm1, self.ffm2], [self.om1, self.om2]
            self.update_opm_entry_object_dict()
            self.hist_file_names = [self.purpose + str(i) for i in range(1,3)]
            #self.set_ms_radiobtn_frames_funcs()
            for i in [self.ffm2, self.om1, self.om2]:
                self.hide_obj_man_labelframes(to_hide = i)
        for ffm, om, hf_name in zip(self.ffms, self.oms, self.hist_file_names):
            self.create_ffm_multifunc_widgets(ffm = ffm, om = om, hist_file_name = hf_name)
        self.set_find_entry_radiobtn_funcs()
        self.set_subplot_radiobtn_funcs()
        self.set_ms_radiobtn_frames_funcs()
        self.set_ffm_to_options_btn_funcs()
        self.set_options_to_ffm_btn_funcs()
        self.set_entry_funcs()
        self.update_backbone()
        self.active_ffm = self.ffm1
        
    def create_opm_entry_object_dict(self):
        self.entry_objects = {"x_min" : self.opm.x_min_entry,
                              "x_max" : self.opm.x_max_entry,
                              "y_min" : self.opm.y_min_entry,
                              "y_max" : self.opm.y_max_entry}
        if self.purpose == "chrom":
            self.entry_objects.update({"wv" : self.opm.wv_entry,
                                       "inten_min" : self.opm.inten_min_entry,
                                       "inten_max" : self.opm.inten_max_entry,
                                       "peak_pos" : self.opm.peak_value_entry,
                                       "peak_dev" : self.opm.peak_dev_entry})
        else:
            self.entry_objects.update({"find_mz1" : self.opm.find_mz1_entry,
                                       "find_mz2" : self.opm.find_mz2_entry})
    
    def update_opm_entry_object_dict(self):
        if self.purpose == "chrom":
            pass
        else:
            self.entry_objects.update({"trim_perc1" : self.om1.trim_perc_entry,
                                       "trim_perc2" : self.om2.trim_perc_entry,
                                       "gen_randnum_perc1" : self.om1.gen_randnum_perc_entry,
                                       "gen_randnum_perc2" : self.om2.gen_randnum_perc_entry})

    def set_ms_inten_radiobtn_funcs(self, om, select_file_args_dict):
        for i in om.inten_radiobuttons.radiobuttons:
            om.inten_radiobuttons.radiobuttons[i].radiobutton.config(command = lambda : wmf.select_file(**select_file_args_dict, 
                                                                                                        event_type = "ms_inten_radiobtn"))
        for i in om.trim_radiobuttons.radiobuttons:
            om.trim_radiobuttons.radiobuttons[i].radiobutton.config(command = lambda : self.enable_disable_mzs_trimming_entry(var = om.trim_radiobtn_variable,
                                                                    select_file_args_dict = select_file_args_dict))

    def set_find_entry_radiobtn_funcs(self):
        if self.purpose == "chrom":
            self.opm.radiobuttons_for_fe["radiobutton_on"].radiobutton.config(command = lambda: self.enable_disable_entry(var = self.opm.radiobutton_variable_on_off,
                                                                                 select_file_args_dict = self.ffm1.select_file_args_dict))
            self.opm.radiobuttons_for_fe["radiobutton_off"].radiobutton.config(command = lambda: self.enable_disable_entry(var = self.opm.radiobutton_variable_on_off,
                                                                                 select_file_args_dict = self.ffm1.select_file_args_dict))

        elif self.purpose == "ms":

            self.opm.radiobuttons_for_fe["radiobutton_on_mz1"].radiobutton.config(command = lambda: self.enable_disable_entry(var = self.opm.radiobutton_variable_on_off_mz1,
                                                                                 select_file_args_dict = self.ffm1.select_file_args_dict))
            self.opm.radiobuttons_for_fe["radiobutton_off_mz1"].radiobutton.config(command = lambda: self.enable_disable_entry(var = self.opm.radiobutton_variable_on_off_mz1,
                                                                                 select_file_args_dict = self.ffm1.select_file_args_dict))

            self.opm.radiobuttons_for_fe["radiobutton_on_mz2"].radiobutton.config(command = lambda: self.enable_disable_entry(var = self.opm.radiobutton_variable_on_off_mz2,
                                                                                 select_file_args_dict = self.ffm2.select_file_args_dict))
            self.opm.radiobuttons_for_fe["radiobutton_off_mz2"].radiobutton.config(command = lambda: self.enable_disable_entry(var = self.opm.radiobutton_variable_on_off_mz2,
                                                                                 select_file_args_dict = self.ffm2.select_file_args_dict))

    def set_subplot_radiobtn_funcs(self):
        for radiobutton in self.opm.radiobuttons:
            self.opm.radiobuttons[radiobutton].radiobutton.config(command = lambda : self.change_subplots(select_file_args_dict = self.ffm1.select_file_args_dict))

    def create_select_file_args_dict(self, ffm, om):
        select_file_args_dict = {"combobox_object" : ffm.combobox, "listbox_object" : ffm.listbox,
                                 "plot_object" : self.opm.graph, "output_object" : self.opm.output,
                                 "entry_objects" : self.entry_objects, "purpose" : ffm.purpose}
        if self.purpose == "ms":
            select_file_args_dict.update({"ms_inten_radiobtn_val" : om.inten_radiobtn_variable,
                                          "mz_trim_radiobtn_val" : om.trim_radiobtn_variable})

        if ffm == self.ffm1 and om == self.om1:
            self.ffm1.select_file_args_dict = select_file_args_dict
        elif ffm == self.ffm2 and om == self.om2:
            self.ffm2.select_file_args_dict = select_file_args_dict


    def change_entry_funcs(self, ffm_to_show):
        widget_bindings = {self.opm.x_min_entry : {"<Return>" : lambda event : wmf.select_file(**ffm_to_show.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "x_min")},
                           self.opm.x_max_entry : {"<Return>" : lambda event : wmf.select_file(**ffm_to_show.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "x_max")},
                           self.opm.y_min_entry : {"<Return>" : lambda event : wmf.select_file(**ffm_to_show.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "y_min")},
                           self.opm.y_max_entry : {"<Return>" : lambda event : wmf.select_file(**ffm_to_show.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "y_max")},}

        for entry in widget_bindings.keys():
            key_or_event = list(widget_bindings[entry].keys())[0]
            func = list(widget_bindings[entry].values())[0]
            entry.bind_key_or_event(key_or_event = key_or_event, func = func)



    def set_entry_funcs(self):
        widget_bindings = {self.opm.x_min_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "x_min")},
                           self.opm.x_max_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "x_max")},
                           self.opm.y_min_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "y_min")},
                           self.opm.y_max_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "y_max")},}
        if self.purpose == "chrom":
            widget_bindings.update({self.opm.wv_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "wv")},
                               self.opm.inten_min_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "inten_min")},
                               self.opm.inten_max_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "inten_max")},
                               self.opm.peak_value_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "peak_pos")},
                               self.opm.peak_dev_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "peak_dev")},})
        elif self.purpose == "ms":
            widget_bindings.update({self.opm.find_mz1_entry : {"<Return>" : lambda event : wmf.select_file_depending_on_ffm(ffm_radiobtn_var = self.ffm_ms_radiobutton_variable,
                                                                                                                            ffm = self.ffm1, active_ffm = self.active_ffm,
                                                                                                                            running_from_entry = "find_mz1")},
                                    self.opm.find_mz2_entry : {"<Return>" : lambda event : wmf.select_file_depending_on_ffm(ffm_radiobtn_var = self.ffm_ms_radiobutton_variable,
                                                                                                                            ffm = self.ffm1, active_ffm = self.active_ffm,
                                                                                                                            running_from_entry = "find_mz1")},
                                    self.om1.trim_perc_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "trim_perc1")},
                                    self.om2.trim_perc_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm2.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "trim_perc2")},
                                    self.om1.gen_randnum_perc_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm1.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "gen_randnum_perc1")},
                                    self.om2.gen_randnum_perc_entry : {"<Return>" : lambda event : wmf.select_file(**self.ffm2.select_file_args_dict, 
                                                                                                event_type = "click",
                                                                                                running_from_entry = "gen_randnum_perc2")},})
        for entry in widget_bindings.keys():
            key_or_event = list(widget_bindings[entry].keys())[0]
            func = list(widget_bindings[entry].values())[0]
            entry.bind_key_or_event(key_or_event = key_or_event, func = func)
#self.ffm_ms_radiobutton_variable.get()
#self.active_ffm
#"find_mz2"

    def create_ffm_multifunc_widgets(self, ffm, om, hist_file_name):
        """Creates ffm multifunctional widgets and binds events/keys to them"""
        
        self.create_select_file_args_dict(ffm = ffm, om = om)
        if self.purpose == "ms":
            self.set_ms_inten_radiobtn_funcs(om = om, select_file_args_dict = ffm.select_file_args_dict)
        ffm.browse_btn = ctwc.Button(master = ffm.labelframes["file_input"], text = "Browse", 
                                     command = lambda : wmf.folder_search(combobox_object = ffm.combobox,
                                                                          listbox_object = ffm.listbox,
                                                                          FILE_EXT = ffm.FILE_EXT,
                                                                          entry_object = ffm.file_search_entry,
                                                                          output_object = self.opm.output,
                                                                          hist_file_name = hist_file_name),
                                     row = 0, column = 2, padx = 2.5, pady = 0).create()


        ffm.file_search_entry.text_var.trace("w", lambda a,b,c: wmf.filter_by_file_name(combobox_object = ffm.combobox,
                                                                                        listbox_object = ffm.listbox,
                                                                                        FILE_EXT = ffm.FILE_EXT,
                                                                                        entry_object = ffm.file_search_entry))
        
        ffm.combobox_binds = {"<<ComboboxSelected>>" : lambda event : wmf.select_combobox_opt(combobox_object = ffm.combobox, 
                                                                                              listbox_object = ffm.listbox, 
                                                                                              output_object = self.opm.output, 
                                                                                              hist_file_name = hist_file_name,
                                                                                              FILE_EXT = ffm.FILE_EXT,
                                                                                              entry_object = ffm.file_search_entry), 
                              "<Return>" : lambda event : wmf.manual_folder_search(combobox_object = ffm.combobox,
                                                                                   listbox_object = ffm.listbox,
                                                                                   FILE_EXT = ffm.FILE_EXT,
                                                                                   entry_object = ffm.file_search_entry,
                                                                                   output_object = self.opm.output,
                                                                                   hist_file_name = hist_file_name)}

        ffm.listbox_binds = {"<Right>" : lambda event : ffm.listbox.going_up_down(direction = "down"),
                             "<Left>"  : lambda event : ffm.listbox.going_up_down(direction = "up"),
                             "<<ListboxSelect>>" : lambda event : wmf.select_file(**ffm.select_file_args_dict, event_type = "click"),
                             "<Return>" : lambda event : wmf.select_file(**ffm.select_file_args_dict, event_type = "click")}
        ffm.file_search_entry_binds = {"<Return>" : lambda event : wmf.focus_and_activate_listbox(listbox_object = ffm.listbox)}
        
        widgets = [ffm.combobox, ffm.listbox, ffm.file_search_entry]
        event_func_pairs = [ffm.combobox_binds.items(), ffm.listbox_binds.items(), 
                            ffm.file_search_entry_binds.items()]
        for widget, event_funcs in zip(widgets, event_func_pairs):
            for event_func in event_funcs:
                widget.bind_key_or_event(key_or_event = event_func[0], func = event_func[1])
        self.create_checkbuttons(ffm = ffm, hist_file_name = hist_file_name)
