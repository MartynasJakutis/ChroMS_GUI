import tkinter as tk

from Object_manager_backbones import OutputPlotManagerBackbone, FileFolderManagerBackbone
from HPLC_MS_diagram_classes import HPLC_Diagram, MS_Diagram
import Custom_tkinter_widget_classes as ctwc

import Widget_manipulation_functions as wmf

import Main_GUI_parameters as mgp

class MultifunctionalBackbone(object):
    """Class which has methods to create Output and Plot, File and Folder managers (opm, ffm), concatenate 
    them and provide additional functionality for them"""
    def __init__(self, window, screenheight, screenwidth, opm_master, purpose):
        self.window = window
        self.screenheight = screenheight
        self.screenwidth = screenwidth
        self.opm_master = opm_master
        self.purpose = purpose
        
    def create_output_plot_man(self):
        outpltman = OutputPlotManagerBackbone(master = self.opm_master, purpose = self.purpose)
        outpltman.create_all_widgets()
        return outpltman
        
    def create_file_folder_man(self, outpltman, purpose):
        """creates ffm of specific purpose and places it in the opm main frame."""
        master = outpltman.frames["main"]
        fifoman = FileFolderManagerBackbone(master = master, purpose = purpose)
        fifoman.create_all_widgets()
        fifoman.purpose = purpose
        return fifoman
                        
    def create_ms_radiobtn_frame(self):
        """Creates radiobuttons to select type of MS File"""
        self.ffm1.radiobutton_variable = tk.IntVar(master = self.window, value = 0)
        for ffm in self.ffms:
            ffm.radiobuttons = {}
            ffm.ms_ffm_labelframe_params = {"master" : ffm.labelframes["file_input"],
                                            "text" : "Choose\nMS file: ",
                                            "row" : 1, "column" : 2}
            ms_radiobtn_lf = list(ffm.ms_ffm_labelframe_params.keys())[0]
            ffm.choose_ms_ffm_labelframe = ctwc.LabelFrame(padx = 2.5, pady = 2.5, width = 0, height = 0, 
                                                           style = "Font.TLabelframe", sticky = tk.E + tk.W,
                                                           **ffm.ms_ffm_labelframe_params).create()
            ffm.radiobutton_pars = {"radiobutton1" : {"text" : "MS1", "row" : 0,
                                                      "column" : 0, "onvalue" : 0},
                                    "radiobutton2" : {"text" : "MS2", "row" : 1,
                                                      "column" : 0, "onvalue" : 1}}
            for radiobutton in ffm.radiobutton_pars.keys():
                ffm.radiobuttons[radiobutton] = ctwc.Radiobutton(master = ffm.choose_ms_ffm_labelframe, padx = 2.5, pady = 0,
                                                                 var = self.ffm1.radiobutton_variable, 
                                                                 command = lambda : self.change_ms_ffm_labelframe(),
                                                                 **ffm.radiobutton_pars[radiobutton])
                ffm.radiobuttons[radiobutton].create()
            
    def hide_ms_ffm_labelframe(self, ffm_to_hide):
        """Hides specified MS ffm labelframe"""
        for lf in ffm_to_hide.labelframes.keys():
            ffm_to_hide.labelframes[lf].grid_remove()
        
    def show_ms_ffm_labelframe(self, ffm_to_show):
        """Shows specified MS ffm labelframe"""
        for lf in ffm_to_show.labelframes.keys():
            ffm_to_show.labelframes[lf].grid()
    def config_subplots_radiobuttons(self, ffm_to_show):
        """Configures command of radiobuttons for subplot selection and changes listbox_object 
        parameter to listbox object present in ffm_to_show ffm."""
        opm = self.opm
        for radiobutton in opm.radiobuttons.keys():
            opm.radiobuttons[radiobutton].radiobutton.config(command = lambda : wmf.select_subplots(plot_object = opm.graph,
                                                                                                    listbox_object = ffm_to_show.listbox,
                                                                                                    output_object = opm.output,
                                                                                                    purpose = ffm_to_show.purpose))
    def change_listbox_focus(self, ffm_to_show):
        """Sets focus on listbox widget."""
        listbox_object = ffm_to_show.listbox
        wmf.focus_and_activate_listbox(listbox_object)

    def change_ms_ffm_labelframe(self):
        """Replaces one MS ffm to another and deactivates radiobutton of 
        selecting subplots which corresponds to hidden ppm"""
        ffm_radiobtn_val = self.ffm1.radiobutton_variable.get()
        radiobtn_vals_and_labels = {0: {"ffm_to_hide" : self.ffm2, "ffm_to_show" : self.ffm1, "activated_rb" : "radiobutton2",
                                        "deactivated_rb" : "radiobutton3", "subplot_to_draw" : "subplot1"},
                                    1: {"ffm_to_hide" : self.ffm1, "ffm_to_show" : self.ffm2,  "activated_rb" : "radiobutton3",
                                        "deactivated_rb" : "radiobutton2", "subplot_to_draw" : "subplot2"}}
        radiobtn_val_labels = radiobtn_vals_and_labels.get(ffm_radiobtn_val)
        ffm_to_hide = radiobtn_val_labels.get("ffm_to_hide")
        ffm_to_show = radiobtn_val_labels.get("ffm_to_show")
        rbtn_to_activate = radiobtn_val_labels.get("activated_rb")
        rbtn_to_deactivate = radiobtn_val_labels.get("deactivated_rb")
        subplot_to_draw = radiobtn_val_labels.get("subplot_to_draw")
        self.hide_ms_ffm_labelframe(ffm_to_hide = ffm_to_hide)
        self.show_ms_ffm_labelframe(ffm_to_show = ffm_to_show)
        self.config_subplots_radiobuttons(ffm_to_show = ffm_to_show)
        self.change_listbox_focus(ffm_to_show = ffm_to_show)

        opm_deact_radiobtn_val = self.opm.radiobutton_variable.get()
        current_radiobtn_val = self.opm.radiobuttons[rbtn_to_deactivate].onvalue
        self.opm.radiobuttons[rbtn_to_deactivate].disable()
        self.opm.radiobuttons[rbtn_to_activate].enable()
        if opm_deact_radiobtn_val == current_radiobtn_val:
            self.opm.radiobutton_variable.set(self.opm.radiobuttons[rbtn_to_activate].onvalue)
            wmf.select_subplots(plot_object = self.opm.graph, output_object = self.opm.output,
                                listbox_object = ffm_to_show.listbox, purpose = ffm_to_show.purpose)
        
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
            
    def create_radiobuttons(self):
        """Creates radiobuttons for subplot selection"""
        opm = self.opm
        opm.radiobuttons = {}
        opm.radiobutton_variable = tk.IntVar(master = self.window, value = 0)
        if self.purpose == "chrom":
            subplot1, subplot2 = "Heatmap", "Chromatogram"
        elif self.purpose == "ms":
            subplot1, subplot2 = "MS1", "MS2" 
        opm.radiobutton_pars_func = lambda subp1, subp2: {"radiobutton1" : {"text" : "Both subplots", "row" : 0,
                                                                            "column" : 0, "onvalue" : 0},
                                                          "radiobutton2" : {"text" : f"Subplot1 ({subp1})", "row" : 0,
                                                                            "column" : 1, "onvalue" : 1},
                                                          "radiobutton3" : {"text" : f"Subplot2 ({subp2})", "row" : 0,
                                                                            "column" : 2, "onvalue" : 2}}
        opm.radiobutton_pars = self.opm.radiobutton_pars_func(subplot1, subplot2)
        for radiobutton in self.opm.radiobutton_pars.keys():
            opm.radiobuttons[radiobutton] = ctwc.Radiobutton(master = opm.frames["radiobutton"], padx = 2.5, pady = 0,
                                                             var = opm.radiobutton_variable, 
                                                             command = lambda : wmf.select_subplots(plot_object = opm.graph, 
                                                                                           listbox_object = self.ffm1.listbox,
                                                                                           output_object = self.opm.output,
                                                                                           purpose = self.ffm1.purpose),
                                                             **opm.radiobutton_pars[radiobutton])
            opm.radiobuttons[radiobutton].create()
    
    def create_graph(self):
        opm = self.opm
        opm.graph_params = {"dpi" : 100, "need_title1" : True, "title1" : "", "title1_pos" : (0.5, 0.95),
                            "title1_text_color" : "k", "title1_weight" : "bold", "title1_fontsize" : 13,
                            "xlabel1_pos" : (0.5, 0.05), "xlabel2_pos" : (0.5, 0.05),
                            "ylabel1_pos" : (0.02, 0.5), "ylabel2_pos" : (0.02, 0.5), 
                            "xlabel1_text_color" : "k", "xlabel2_text_color" : "k",
                            "ylabel1_text_color" : "k", "ylabel2_text_color" : "k",
                            "xlabel1_weight" : "bold", "xlabel2_weight" : "bold",
                            "ylabel1_weight" : "bold", "ylabel2_weight" : "bold",
                            "xlabel1_fontsize" : 14, "xlabel2_fontsize" : 14,
                            "ylabel1_fontsize" : 14, "ylabel2_fontsize" : 14,
                            "matplotlib_style1" : "seaborn-v0_8-ticks", "matplotlib_style2" : "seaborn-v0_8-ticks",
                            "master_labelframe" : opm.labelframes["chrom/ms"], 
                            "add_multiplier_w" : 0.98, "add_multiplier_h" : 0.90,
                            "radiobutton_var" : opm.radiobutton_variable, "state" : "initial", 
                            "screenheight" : self.screenheight, "screenwidth" : self.screenwidth}
        
        if self.purpose == "chrom":
            dict_update = {"xlabel1" : "Išėjimo laikas, min", "xlabel2" : "Išėjimo laikas, min",
                           "ylabel1" : "EMS bangos ilgis\nλ, nm", "ylabel2" : "Sugerties intensyvumas, AU",
                           "colorbar_label" : "Intensyvumas, AU", "colorbar_text_color" : "k",
                           "colorbar_weight" : "bold", "colorbar_fontsize" : 14,
                           "data_wave_nm" : 0, "data_rt" : 0, "data_ab" : 0, "data_ab_all" : 0, "data_wv_all" : 0,
                           "intensity_min" : 0, "intensity_max" : 1}
            Used_Diagram = HPLC_Diagram
            
        elif self.purpose == "ms":
            dict_update = {"need_title2" : True, "title2" : "", "title2_pos" : (0.5, 0.95),
                           "title2_text_color" : "k", "title2_weight" : "bold", "title2_fontsize" : 13,
                           "xlabel1" : "m/z", "xlabel2" : "m/z",
                           "ylabel1" : "Absoliutus intensyvumas", "ylabel2" : "Absoliutus intensyvumas",
                           "data_mz1" : 0, "data_mz2" : 0, "data_inten1" : 0, "data_inten2" : 0}
            Used_Diagram = MS_Diagram
            
        opm.graph_params.update(dict_update)
        opm.graph = Used_Diagram(**opm.graph_params)
        
        if Used_Diagram == HPLC_Diagram:
            plotting_funcs_dict = {"f_subplot1" : opm.graph.plotting_term_state_heat,
                                   "f_subplot2" : opm.graph.plotting_term_state_chrom}
        elif Used_Diagram == MS_Diagram:
            plotting_funcs_dict = {"f_subplot1" : opm.graph.plotting_term_state_ms1,
                                   "f_subplot2" : opm.graph.plotting_term_state_ms2}
        opm.graph.create_a_figure()
        opm.graph.set_term_state_plotting_funcs(**plotting_funcs_dict)
        opm.graph.draw_diagram()
        
    def update_backbone(self):
        """Updates ffm: loads browsing history to combobox and updates listbox."""
        for ffm, hist_file_name in zip(self.ffms, self.hist_file_names):
            ffm.combobox.load(folder = "my_browsing_history", name = hist_file_name)
            wmf.update_combobox(combobox_object = ffm.combobox, listbox_object = ffm.listbox,
                            FILE_EXT = ffm.FILE_EXT, entry_object = ffm.file_search_entry,
                            save_hist = False)

    def create_opm_with_widgets(self):
        self.opm = self.create_output_plot_man()
        self.create_radiobuttons()
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
        self.create_graph()
    
    def concatenate_backbones(self):
        """Concatenates ffm/ffms and opm together."""
        self.create_opm_with_widgets()    
        if self.purpose == "chrom":
            self.ffm1 = self.create_file_folder_man(outpltman = self.opm, purpose = self.purpose)
            self.ffms = [self.ffm1]
            self.hist_file_names = [self.purpose]
        elif self.purpose == "ms":
            self.opm.radiobuttons["radiobutton3"].disable()
            self.ffm1 = self.create_file_folder_man(outpltman = self.opm, purpose = "ms1")
            self.ffm2 = self.create_file_folder_man(outpltman = self.opm, purpose = "ms2")
            self.ffms = [self.ffm1, self.ffm2]
            self.hist_file_names = [self.purpose + str(i) for i in range(1,3)]
            self.create_ms_radiobtn_frame()
            self.hide_ms_ffm_labelframe(ffm_to_hide = self.ffm2)
        for ffm, hf_name in zip(self.ffms, self.hist_file_names):
            self.create_ffm_multifunc_widgets(ffm = ffm, hist_file_name = hf_name)
        self.update_backbone()

    def create_ffm_multifunc_widgets(self, ffm, hist_file_name):
        """Creates ffm multifunctional widgets and binds events/keys to them"""
        if self.purpose == "chrom":
            entry_objects = {"wv" : self.opm.wv_entry,
                             "inten_min" : self.opm.inten_min_entry,
                             "inten_max" : self.opm.inten_max_entry}
        else:
            entry_objects = None
        select_file_args_dict = {"combobox_object" : ffm.combobox, "listbox_object" : ffm.listbox,
                                 "plot_object" : self.opm.graph, "output_object" : self.opm.output,
                                 "entry_objects" : entry_objects, "purpose" : ffm.purpose}

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
                             "<<ListboxSelect>>" : lambda event : wmf.select_file(**select_file_args_dict),
                             "<Return>" : lambda event : wmf.select_file(**select_file_args_dict)}
        ffm.file_search_entry_binds = {"<Return>" : lambda event : wmf.focus_and_activate_listbox(listbox_object = ffm.listbox)}
        
        widgets = [ffm.combobox, ffm.listbox, ffm.file_search_entry]
        event_func_pairs = [ffm.combobox_binds.items(), ffm.listbox_binds.items(), 
                            ffm.file_search_entry_binds.items()]
        for widget, event_funcs in zip(widgets, event_func_pairs):
            for event_func in event_funcs:
                widget.bind_key_or_event(key_or_event = event_func[0], func = event_func[1])
        self.create_checkbuttons(ffm = ffm, hist_file_name = hist_file_name)