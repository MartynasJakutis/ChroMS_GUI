import tkinter as tk
import Custom_tkinter_widget_classes as ctwc
import Widget_manipulation_functions as wmf
import Main_GUI_parameters as mgp

class SeveralRadiobuttons(object):
    def __init__(self, master, start_row, start_col, radiobtn_var, radiobtn_names, orientation = "horizontal"):
        self.master = master
        self.start_row = start_row
        self.start_col = start_col
        self.radiobtn_var = radiobtn_var
        self.radiobtn_names = radiobtn_names
        self.orientation = orientation
        self.radiobutton_pars = {}
        self.radiobuttons = {}
    def set_params(self):
        row_num, col_num = self.start_row, self.start_col
        for ind, radiobtn_name in enumerate(self.radiobtn_names):
            self.radiobutton_pars.update({radiobtn_name : {"text" : radiobtn_name, "row" : row_num, 
                                                           "column" : col_num, "onvalue" : ind}})
            if self.orientation == "horizontal":
                col_num += 1
            elif self.orientation == "vertical":
                row_num += 1
    def create(self):
        self.set_params()
        for radiobutton in self.radiobutton_pars.keys():
            self.radiobuttons[radiobutton] = ctwc.Radiobutton(master = self.master, padx = 2.5, pady = 0,
                                                              var = self.radiobtn_var, 
                                                              command = None,
                                                              **self.radiobutton_pars[radiobutton])
            self.radiobuttons[radiobutton].create()             
        
class MSRadiobuttonLabelFrame(object):
    def __init__(self, master, radiobtn_var):
        self.master = master
        self.radiobtn_var = radiobtn_var
        self.radiobuttons = {}
        self.ms_ffm_labelframe_params = {"master" : self.master,
                                         "text" : "Choose\nMS file: ",
                                         "row" : 0, "column" : 0}
        self.radiobutton_pars = {"radiobutton1" : {"text" : "MS1", "row" : 0,
                                                   "column" : 0, "onvalue" : 0},
                                 "radiobutton2" : {"text" : "MS2", "row" : 1,
                                                   "column" : 0, "onvalue" : 1}}
    def create(self):
        self.labelframe = ctwc.LabelFrame(padx = 2.5, pady = 2.5, width = 0, height = 0, 
                                          style = "Font.TLabelframe", sticky = tk.E + tk.W,
                                          **self.ms_ffm_labelframe_params).create()
        for radiobutton in self.radiobutton_pars.keys():
            self.radiobuttons[radiobutton] = ctwc.Radiobutton(master = self.labelframe, padx = 2.5, pady = 0,
                                                              var = self.radiobtn_var, 
                                                              command = None,
                                                              **self.radiobutton_pars[radiobutton])
            self.radiobuttons[radiobutton].create()

class OutputPlotManagerBackbone(object):
    """Class which contains methods for Outputwidget and Plot Manager Backbone (opm) creation.
    master - master widget, purpose - str which refers what kind of opm to create."""
    def __init__(self, master, purpose):
        self.master = master
        self.purpose = purpose
        self.frames = {}
        self.labelframes = {}
        self.labels = {}
    def load_widget_params(self):
        purpose_dict = {"chrom" : "HPLC 3D heatmap and/or chromatogram: ",
                        "ms" : "Mass spectrum/spectra: "}
        ms_chrom_lf_text = purpose_dict.get(self.purpose)
        self.main_frame_params_func = lambda master : {"main" : {"master" : master, "row" : 0, "column" : 0,
                                                                 "style" : "NewCusFrame.TFrame", 
                                                                 "sticky" : tk.E + tk.W}}
        self.labelframe_params_func = lambda main_f, plot_f : {"plot_opt" : {"master" : main_f, "text" : "Plot options: ",
                                                                             "row" : 2, "column" : 0},
                                                               "output" : {"master" : main_f, "text" : "Text output: ",
                                                                           "row" : 3, "column" : 0},
                                                               "chrom/ms" : {"master" : plot_f,
                                                                             "text" : ms_chrom_lf_text,
                                                                             "row" : 0, "column" : 1}}
        self.frame_params_func = lambda plot_opt_lf : {"radiobutton" : {"master" : plot_opt_lf, 
                                                                        "row" : 0, "column" : 1}}
        self.label_params_func = lambda plot_opt_lf : {"label1" : {"master" : plot_opt_lf, "text" : "Select subplots: ", 
                                                                   "row" : 0, "column" : 0, "sticky" : tk.W}}
                                                               
    def create_simple_widgets(self):
        """Creates widgets which has no additional functionality"""
        self.main_frame_params = self.main_frame_params_func(self.master)
        mframe = list(self.main_frame_params.keys())[0]
        self.frames[mframe] = ctwc.Frame(**self.main_frame_params[mframe]).create()
        
        self.labelframe_params = self.labelframe_params_func(main_f = self.frames[mframe],
                                                             plot_f = self.master)
        for lframe in self.labelframe_params.keys():
            self.labelframes[lframe] = ctwc.LabelFrame(padx = 2.5, pady = 2.5, width = 400, height = 0, 
                                                       style = "Font.TLabelframe", sticky = tk.E + tk.W,
                                                       **self.labelframe_params[lframe]).create()

        self.frame_params = self.frame_params_func(plot_opt_lf = self.labelframes["plot_opt"])

        if self.purpose == "chrom":
            self.frame_params.update({"wavelength" : {"master" : self.labelframes["plot_opt"], 
                                                      "row" : 1, "column" : 1},
                                      "find_peaks" : {"master" : self.labelframes["plot_opt"], 
                                                      "row" : 2, "column" : 1},
                                      "set_ranges" : {"master" : self.labelframes["plot_opt"], 
                                                      "row" : 3, "column" : 1}})
        elif self.purpose == "ms":
            self.frame_params.update({"find_mz1" : {"master" : self.labelframes["plot_opt"], 
                                                      "row" : 1, "column" : 1},
                                      "find_mz2" : {"master" : self.labelframes["plot_opt"], 
                                                      "row" : 2, "column" : 1},
                                      "set_ranges" : {"master" : self.labelframes["plot_opt"], 
                                                      "row" : 3, "column" : 1}})
        for frame in self.frame_params.keys():
            self.frames[frame] = ctwc.Frame(style = "NewCusFrame.TFrame", sticky = tk.E + tk.W,
                                            **self.frame_params[frame]).create()
            
        self.label_params = self.label_params_func(plot_opt_lf = self.labelframes["plot_opt"])

        if self.purpose == "chrom":                                                       
            self.label_params.update({"label2" : {"master" : self.labelframes["plot_opt"], "text" : "Wavelength, nm: ", 
                                                  "row" : 1, "column" : 0, "sticky" : tk.W},
                                      "label3" : {"master" : self.labelframes["plot_opt"], "text" : "Find peaks: ", 
                                                  "row" : 2, "column" : 0, "sticky" : tk.W},
                                      "label4" : {"master" : self.labelframes["plot_opt"], "text" : "Set ranges: ", 
                                                  "row" : 3, "column" : 0, "sticky" : tk.W},
                                      "label5" : {"master" : self.frames["wavelength"], "text" : "Intensity, AU: ", 
                                                  "row" : 0, "column" : 1, "sticky" : tk.W},
                                      "label6" : {"master" : self.frames["wavelength"], "text" : "min", 
                                                  "row" : 0, "column" : 2, "sticky" : tk.W},
                                      "label7" : {"master" : self.frames["wavelength"], "text" : "max", 
                                                  "row" : 0, "column" : 4, "sticky" : tk.W},
                                      "label8" : {"master" : self.frames["find_peaks"], "text" : "±", 
                                                  "row" : 0, "column" : 1, "sticky" : tk.E + tk.W},
                                      "label9" : {"master" : self.frames["find_peaks"], "text" : "min.", 
                                                  "row" : 0, "column" : 3, "sticky" : tk.W}})
        elif self.purpose == "ms":                                                       
            self.label_params.update({"label2" : {"master" : self.labelframes["plot_opt"], "text" : "Find m/z 1: ", 
                                                  "row" : 1, "column" : 0, "sticky" : tk.W},
                                      "label3" : {"master" : self.labelframes["plot_opt"], "text" : "Find m/z 2: ", 
                                                  "row" : 2, "column" : 0, "sticky" : tk.W},
                                      "label4" : {"master" : self.labelframes["plot_opt"], "text" : "Set ranges: ", 
                                                  "row" : 3, "column" : 0, "sticky" : tk.W}})        
            
        for label in self.label_params.keys():
            padx = (5, 20) if label == "label9" else (5, 0)
            self.labels[label] = ctwc.Label(padx = padx, pady = 0, background = mgp.DEFAULT_LABEL_COLOR,
                                            style = "Normal.TLabel", **self.label_params[label]).create()
        
            
    def create_advanced_widgets(self):
        """Creates widgets which are supposed to have additional functionality"""
        self.output = ctwc.Outputwidget(master = self.labelframes["output"], width = mgp.CONSOLE_WIDTH, height = 6.5, 
                                        font = (mgp.DEFAULT_CONSOLE_SCHRIFT, 11, "normal"), row = 0, column = 0, 
                                        padx = 2.5, pady = 0)
        self.fill_set_ranges_frame(master = self.frames["set_ranges"])
        widgets = [self.output]
        self.output.create()
        self.create_entries_for_peak_search()
        if self.purpose == "chrom":
            self.wv_entry = ctwc.Entry(master = self.frames["wavelength"], style = "TEntry", 
                                       font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 5, 
                                       row = 0, column = 0, padx = 2.5, pady = (2.5, 1.25), sticky = tk.E + tk.W)
            self.inten_min_entry = ctwc.Entry(master = self.frames["wavelength"], style = "TEntry", 
                                       font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 8, 
                                       row = 0, column = 3, padx = 2.5, pady = (2.5, 1.25), sticky = tk.E + tk.W)
            self.inten_max_entry = ctwc.Entry(master = self.frames["wavelength"], style = "TEntry", 
                                       font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 8, 
                                       row = 0, column = 5, padx = 2.5, pady = (2.5, 1.25), sticky = tk.E + tk.W)
            
            entries_list = [self.wv_entry, self.inten_min_entry, self.inten_max_entry, 
                            self.peak_value_entry, self.peak_dev_entry, self.x_min_entry,
                            self.x_max_entry, self.y_min_entry, self.y_max_entry]

            const_list = [mgp.DEFAULT_WAVELENGTH, mgp.DEFAULT_MIN_INTENSITY, mgp.DEFAULT_MAX_INTENSITY,
                          mgp.DEFAULT_PEAK_POS_SEQ, mgp.DEFAULT_PEAK_DEV_SEQ, mgp.DEFAULT_CHROM_X_MIN,
                          mgp.DEFAULT_CHROM_X_MAX, mgp.DEFAULT_CHROM_Y_MIN, mgp.DEFAULT_CHROM_Y_MAX]
            
            for entry, const in zip(entries_list, const_list):
                entry.create()
                entry.entry.insert(index = 0, string = const)

            self.wv_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_four_digit_integer(entry_object = self.wv_entry,
                                                                                            max_len = mgp.LEN_4_DIGIT_INT))
            self.inten_max_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_neg_float(entry_object = self.inten_max_entry,
                                                                                              max_len = mgp.LEN_5_DIGIT_FLOAT))
            self.inten_min_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_neg_float(entry_object = self.inten_min_entry,
                                                                                              max_len = mgp.LEN_5_DIGIT_FLOAT))
            self.peak_value_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_float_seq(entry_object = self.peak_value_entry,
                                                                                              max_len = mgp.LEN_TIME_AFTER_DEC))
            self.peak_dev_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_float_seq(entry_object = self.peak_dev_entry,
                                                                                             max_len = mgp.LEN_TIME_AFTER_DEC))

            wmf.maintain_four_digit_integer(entry_object = self.wv_entry, is_startup = True, 
                                            max_len = mgp.LEN_4_DIGIT_INT, default_value = "254")
            wmf.maintain_pos_neg_float(entry_object = self.inten_min_entry, is_startup = True,
                                       max_len = mgp.LEN_5_DIGIT_FLOAT, default_value = "0.00000")
            wmf.maintain_pos_neg_float(entry_object = self.inten_max_entry, is_startup = True,
                                       max_len = mgp.LEN_5_DIGIT_FLOAT, default_value = "1.00000")
            wmf.maintain_pos_float_seq(entry_object = self.peak_value_entry, is_startup = True,
                                       max_len = mgp.LEN_TIME_AFTER_DEC, default_value = "")
            wmf.maintain_pos_float_seq(entry_object = self.peak_dev_entry, is_startup = True,
                                       max_len = mgp.LEN_TIME_AFTER_DEC, default_value = "0.25")

        elif self.purpose == "ms":
            entries_list = [self.find_mz1_entry, self.find_mz2_entry, self.x_min_entry,
                            self.x_max_entry, self.y_min_entry, self.y_max_entry]
            const_list = [mgp.DEFAULT_FIND_MZ1_SEQ, mgp.DEFAULT_FIND_MZ2_SEQ, mgp.DEFAULT_MS_X_MIN,
                          mgp.DEFAULT_MS_X_MAX, mgp.DEFAULT_MS_Y_MIN, mgp.DEFAULT_MS_Y_MAX]
            for entry, const in zip(entries_list, const_list):
                entry.create()
                entry.entry.insert(index = 0, string = const)

            self.find_mz1_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_float_seq(entry_object = self.find_mz1_entry,
                                                                                               max_len = mgp.LEN_MZ_AFTER_DEC))
            self.find_mz2_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_float_seq(entry_object = self.find_mz2_entry,
                                                                                               max_len = mgp.LEN_MZ_AFTER_DEC))
            wmf.maintain_pos_float_seq(entry_object = self.find_mz1_entry, is_startup = True,
                                       max_len = mgp.LEN_MZ_AFTER_DEC, default_value = "")
            wmf.maintain_pos_float_seq(entry_object = self.find_mz2_entry, is_startup = True,
                                       max_len = mgp.LEN_MZ_AFTER_DEC, default_value = "")

        self.x_min_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_neg_float(entry_object = self.x_min_entry,
                                                                                      max_len = mgp.LEN_5_DIGIT_FLOAT))
        self.x_max_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_neg_float(entry_object = self.x_max_entry,
                                                                                      max_len = mgp.LEN_5_DIGIT_FLOAT))
        self.y_min_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_neg_float(entry_object = self.y_min_entry,
                                                                                      max_len = mgp.LEN_5_DIGIT_FLOAT))
        self.y_max_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_pos_neg_float(entry_object = self.y_max_entry,
                                                                                      max_len = mgp.LEN_5_DIGIT_FLOAT))
        wmf.maintain_pos_neg_float(entry_object = self.x_min_entry, is_startup = True,
                                   max_len = mgp.LEN_5_DIGIT_FLOAT, default_value = "")
        wmf.maintain_pos_neg_float(entry_object = self.x_max_entry, is_startup = True,
                                   max_len = mgp.LEN_5_DIGIT_FLOAT, default_value = "")
        wmf.maintain_pos_neg_float(entry_object = self.y_min_entry, is_startup = True,
                                   max_len = mgp.LEN_5_DIGIT_FLOAT, default_value = "")
        wmf.maintain_pos_neg_float(entry_object = self.y_max_entry, is_startup = True,
                                   max_len = mgp.LEN_5_DIGIT_FLOAT, default_value = "")

    def create_all_widgets(self):
        self.load_widget_params()
        self.create_simple_widgets()
        self.create_advanced_widgets()

    def fill_set_ranges_frame(self, master):
        self.set_ranges_labels = {}
        x_units, y_units = ("min.", "AU") if self.purpose == "chrom" else ("m/z", "I")
        self.set_ranges_label_params = {"label1" : {"master" : master, "text" : "X [", 
                                                    "row" : 0, "column" : 0, "sticky" : tk.E},
                                        "label2" : {"master" : master, "text" : "-", 
                                                    "row" : 0, "column" : 2, "sticky" : tk.E + tk.W},
                                        "label3" : {"master" : master, "text" : f"] {x_units}", 
                                                     "row" : 0, "column" : 4, "sticky" : tk.W},
                                        "label4" : {"master" : master, "text" : "Y [", 
                                                     "row" : 0, "column" : 5, "sticky" : tk.E},
                                        "label5" : {"master" : master, "text" : "-", 
                                                     "row" : 0, "column" : 7, "sticky" : tk.E + tk.W},
                                        "label6" : {"master" : master, "text" : f"] {y_units}", 
                                                     "row" : 0, "column" : 9, "sticky" : tk.W}}
        for label in self.set_ranges_label_params.keys():
            padx = (5, 0)
            self.set_ranges_labels[label] = ctwc.Label(padx = padx, pady = 0, background = mgp.DEFAULT_LABEL_COLOR,
                                                       style = "Normal.TLabel", **self.set_ranges_label_params[label]).create()
        
        self.x_min_entry = ctwc.Entry(master = master, style = "TEntry", 
                                      font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 7, 
                                      row = 0, column = 1, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
        self.x_max_entry = ctwc.Entry(master = master, style = "TEntry", 
                                      font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 7, 
                                      row = 0, column = 3, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
        self.y_min_entry = ctwc.Entry(master = master, style = "TEntry", 
                                      font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 7, 
                                      row = 0, column = 6, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
        self.y_max_entry = ctwc.Entry(master = master, style = "TEntry", 
                                      font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 7, 
                                      row = 0, column = 8, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)

    def create_entries_for_peak_search(self):
        if self.purpose == "chrom":
            self.peak_value_entry = ctwc.Entry(master = self.frames["find_peaks"], style = "TEntry", 
                                               font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 15, 
                                               row = 0, column = 0, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
            self.peak_dev_entry = ctwc.Entry(master = self.frames["find_peaks"], style = "TEntry", 
                                             font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 8, 
                                             row = 0, column = 2, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
        elif self.purpose == "ms":
            self.find_mz1_entry = ctwc.Entry(master = self.frames["find_mz1"], style = "TEntry", 
                                               font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 15, 
                                               row = 0, column = 0, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
            self.find_mz2_entry = ctwc.Entry(master = self.frames["find_mz2"], style = "TEntry", 
                                               font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 15, 
                                               row = 0, column = 0, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
        self.ctrl_entries = self.return_controlled_entries()
    def return_controlled_entries(self):
        if self.purpose == "ms":
            return {"find_mz1" : self.find_mz1_entry,
                    "find_mz2" : self.find_mz2_entry}
        else:
            return {"peak_pos" : self.peak_value_entry,
                    "peak_dev" : self.peak_dev_entry}
class FileFolderManagerBackbone(OutputPlotManagerBackbone):
    """Class which contains methods for File and Folder Manager Backbone (ffm) creation.
    master - higher hierarchy widget, purpose - str which refers what kind of ffm to create."""
    def __init__(self, master, purpose, ms_radiobutton_var = None):
        super().__init__(master, purpose)
        self.ms_radiobutton_var = ms_radiobutton_var
        self.FILE_EXT = []
    def load_widget_params(self):
        purpose_dict = {"chrom" : "HPLC 3D",
                        "ms1" : "MS (File 1)",
                        "ms2" : "MS (File 2)"}
        input_lf_t = purpose_dict.get(self.purpose)
        self.labelframe_params_func = lambda main_frame : {"file_input" : {"master" : main_frame, 
                                                                           "text" : f"Upload your {input_lf_t} data files from here: ",
                                                                           "row" : 0, "column" : 0},
                                                           "file_filter" : {"master" : main_frame,
                                                                            "text" : "File filters: ",
                                                                            "row" : 1, "column" : 0}}
        self.frame_params_func = lambda input_lf, filter_lf : {"listbox" : {"master" : input_lf, 
                                                                            "row" : 1, "column" : 1},
                                                               "for_options" : {"master" : input_lf, 
                                                                            "row" : 1, "column" : 2},
                                                               "checkbutton" : {"master" : filter_lf, 
                                                                                "row" : 0, "column" : 1},
                                                               "file_search" : {"master" : filter_lf, 
                                                                                "row" : 1, "column" : 1}}
        self.label_params_func = lambda input_lf, filter_lf : {"label1" : {"master" : input_lf, "text" : "Folder: ",
                                                                           "row" : 0, "column" : 0, "sticky" : tk.W},
                                                               "label2" : {"master" : input_lf, "text" : "Files: ", 
                                                                           "row" : 1, "column" : 0, "sticky" : tk.N + tk.W},
                                                               "label3" : {"master" : filter_lf, "text" : "Show ONLY: ", 
                                                                           "row" : 0, "column" : 0, "sticky" : tk.W},
                                                               "label4" : {"master" : filter_lf, "text" : "Find files: ", 
                                                                           "row" : 1, "column" : 0, "sticky" : tk.W}}
    def create_simple_widgets(self):
        self.labelframe_params = self.labelframe_params_func(self.master)
        for lframe in self.labelframe_params.keys():
            self.labelframes[lframe] = ctwc.LabelFrame(padx = 2.5, pady = 2.5, width = 400, height = 400, 
                                                       style = "Font.TLabelframe", sticky = tk.E + tk.W,
                                                       **self.labelframe_params[lframe]).create()

        self.frame_params = self.frame_params_func(input_lf = self.labelframes["file_input"],
                                                   filter_lf = self.labelframes["file_filter"])
        for frame in self.frame_params.keys():
            self.frames[frame] = ctwc.Frame(style = "NewCusFrame.TFrame", sticky = tk.E + tk.W, 
                                            **self.frame_params[frame]).create()
            
        self.label_params = self.label_params_func(input_lf = self.labelframes["file_input"],
                                                   filter_lf = self.labelframes["file_filter"])
        for label in self.label_params.keys():
            self.labels[label] = ctwc.Label(padx = (5, 0), pady = 0, background = mgp.DEFAULT_LABEL_COLOR,
                                            style = "Normal.TLabel", **self.label_params[label]).create()
    def create_advanced_widgets(self):
        """Creates widgets which are supposed to have additional functionality"""
        self.combobox = ctwc.ComboBox(master = self.labelframes["file_input"],
                                      width = mgp.FOLDER_COMBOBOX_WIDTH, row = 0, column = 1)
        self.listbox = ctwc.Listbox(master = self.frames["listbox"], background = 'black', foreground = 'green',
                                    width = mgp.FILE_LISTBOX_WIDTH, 
                                    height = 10, selectbackground = 'gray', selectforeground = 'black', row = 0, column = 0, 
                                    padx = (0, 0), pady = 0, padx_scroll = 0, pady_scroll = 0, exportselection = False)
        self.file_search_entry = ctwc.Entry(master = self.frames["file_search"], style = "TEntry", 
                                            font = (mgp.DEFAULT_SCHRIFT, 12, "normal"),
                                            width = mgp.FILE_SEARCH_ENTRY_WIDTH, 
                                            row = 0, column = 1, padx = 2.5, pady = 2.5, sticky = tk.E + tk.W)
        self.to_options_btn = ctwc.Button(master = self.frames["for_options"], text = "To options", 
                                          command = lambda : None,
                                          row = 1, column = 0, padx = 2.5, pady = 0).create()
        self.file_search_entry.create_file_name_filter()
        widgets = [self.combobox, self.listbox, self.file_search_entry]
        if self.purpose in ["ms1", "ms2"] and self.ms_radiobutton_var:
            self.ms_radiobutton_lf = MSRadiobuttonLabelFrame(master = self.frames["for_options"],
                                                             radiobtn_var = self.ms_radiobutton_var)
            widgets.append(self.ms_radiobutton_lf)
        for widget in widgets:
            widget.create()

##############################################################################################
class OptionManagerBackbone(OutputPlotManagerBackbone):
    def __init__(self, master, purpose, ms_radiobutton_var = None):
        super().__init__(master, purpose)
        self.ms_radiobutton_var = ms_radiobutton_var
    def load_widget_params(self):
        purpose_dict = {"chrom" : "HPLC 3D",
                        "ms1" : "MS (File 1)",
                        "ms2" : "MS (File 2)"}
        input_lf_t = purpose_dict.get(self.purpose)
        self.labelframe_params_func = lambda main_frame : {"design_options" : {"master" : main_frame, 
                                                                               "text" : f"More options for {input_lf_t} visualization: ",
                                                                               "row" : 0, "column" : 0, "rowspan" : 2},
                                                           "algorithms" : {"master" : main_frame,
                                                                           "text" : "Algorithms: ",
                                                                           "row" : 2, "column" : 0}}
        self.frame_params_func = lambda des_lf, alg_lf : {"opt_notebook" : {"master" : des_lf, 
                                                                            "row" : 1, "column" : 1, "sticky" : tk.W},
                                                          "for_options" : {"master" : des_lf, 
                                                                           "row" : 1, "column" : 2, "sticky" : tk.W}}

    def create_simple_widgets(self):
        self.labelframe_params = self.labelframe_params_func(main_frame = self.master)

        for lframe in self.labelframe_params.keys():
            self.labelframes[lframe] = ctwc.LabelFrame(padx = 2.5, pady = 2.5, width = 400, height = 400, 
                                                       style = "Font.TLabelframe", sticky = tk.E + tk.W,
                                                       **self.labelframe_params[lframe]).create()
        self.frame_params = self.frame_params_func(des_lf = self.labelframes["design_options"],
                                                   alg_lf = self.labelframes["algorithms"])
        if self.purpose == "chrom":
            self.frame_params.update({})
        else:
           self.frame_params.update({"inten_radiobtn" : {"master" : self.labelframes["algorithms"], 
                                                         "row" : 0, "column" : 1, "sticky" : tk.E + tk.W},
                                     "trim_radiobtn" : {"master" : self.labelframes["algorithms"], 
                                                        "row" : 1, "column" : 1, "sticky" : tk.E + tk.W},
                                     "trim_perc": {"master" : self.labelframes["algorithms"], 
                                                   "row" : 2, "column" : 1, "sticky" : tk.E + tk.W},
                                     "gen_randnum_perc": {"master" : self.labelframes["algorithms"], 
                                                          "row" : 3, "column" : 1, "sticky" : tk.E + tk.W}})

        for frame in self.frame_params.keys():
            self.frames[frame] = ctwc.Frame(style = "NewCusFrame.TFrame", 
                                            **self.frame_params[frame]).create()
        if self.purpose == "chrom":
            self.label_params = {"label1" : {"master" : self.labelframes["algorithms"], "text" : "Intensity: ", 
                                         "row" : 0, "column" : 0, "sticky" : tk.W}}
        else:
            self.label_params = {"label1" : {"master" : self.labelframes["algorithms"], "text" : "Intensity: ", 
                                             "row" : 0, "column" : 0, "sticky" : tk.W},
                                 "label2" : {"master" : self.labelframes["algorithms"], "text" : "Trim m/zs: ", 
                                             "row" : 1, "column" : 0, "sticky" : tk.W},
                                 "label3" : {"master" : self.labelframes["algorithms"], "text" : "Trim pars: ", 
                                             "row" : 2, "column" : 0, "sticky" : tk.W},
                                 "label4" : {"master" : self.frames["trim_perc"], "text" : "Trim values >=", 
                                             "row" : 0, "column" : 0, "sticky" : tk.W},
                                 "label5" : {"master" : self.frames["trim_perc"], "text" : "% of min m/z", 
                                             "row" : 0, "column" : 2, "sticky" : tk.W},
                                 "label6" : {"master" : self.frames["gen_randnum_perc"], "text" : "Generate random numbers <=", 
                                             "row" : 0, "column" : 0, "sticky" : tk.W},
                                 "label7" : {"master" : self.frames["gen_randnum_perc"], "text" : "% of min m/z", 
                                             "row" : 0, "column" : 2, "sticky" : tk.W}}

        for label in self.label_params.keys():
            self.labels[label] = ctwc.Label(padx = (5, 0), pady = 0, background = mgp.DEFAULT_LABEL_COLOR,
                                            style = "Normal.TLabel", **self.label_params[label]).create()
    def create_advanced_widgets(self):
        """Creates widgets which are supposed to have additional functionality"""
        self.notebook_w_sb = ctwc.NotebookWithSbFrames(master = self.frames["opt_notebook"], 
                                                       style = "Opt.TNotebook", sticky = tk.W,
                                                       row = 0, column = 0,
                                                       padx = (10, 0), pady = (5, 10),
                                                       tab_names = [f"{i}" for i in range(5)])
                
        self.to_ffm_btn = ctwc.Button(master = self.frames["for_options"], text = "Go back", 
                                          command = lambda : None,
                                          row = 1, column = 0, padx = 2.5, pady = 0).create()
        widgets = [self.notebook_w_sb]
        if self.purpose in ["ms1", "ms2"] and self.ms_radiobutton_var:
            pur_num = self.purpose[-1]
            self.inten_radiobtn_variable = tk.IntVar(master = self.labelframes["algorithms"], value = 0)
            self.trim_radiobtn_variable = tk.IntVar(master = self.labelframes["algorithms"], value = 0)
            inten_radiobtn_names = ["Absolute", "Absolute (SciNot)","Relative (%)", "Relative (fraction)"]
            trim_radiobtn_names = ["Disabled", "Enabled"]
            self.ms_radiobutton_lf = MSRadiobuttonLabelFrame(master = self.frames["for_options"],
                                                             radiobtn_var = self.ms_radiobutton_var)
            self.inten_radiobuttons = SeveralRadiobuttons(master = self.frames["inten_radiobtn"], start_row = 0, 
                                                          start_col = 0, radiobtn_var = self.inten_radiobtn_variable, 
                                                          radiobtn_names = inten_radiobtn_names,
                                                          orientation = "horizontal")
            self.trim_radiobuttons = SeveralRadiobuttons(master = self.frames["trim_radiobtn"], start_row = 0, 
                                                         start_col = 0, radiobtn_var = self.trim_radiobtn_variable, 
                                                         radiobtn_names = trim_radiobtn_names,
                                                         orientation = "horizontal")

            self.trim_perc_entry = ctwc.Entry(master = self.frames["trim_perc"], style = "TEntry", 
                                            font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 5, 
                                            row = 0, column = 1, padx = 2.5, pady = 2.5, sticky = tk.E + tk.W)

            self.gen_randnum_perc_entry = ctwc.Entry(master = self.frames["gen_randnum_perc"], style = "TEntry", 
                                            font = (mgp.DEFAULT_SCHRIFT, 12, "normal"), width = 5, 
                                            row = 0, column = 1, padx = 2.5, pady = 2.5, sticky = tk.E + tk.W)

            entries_list = [self.trim_perc_entry, self.gen_randnum_perc_entry]
            const_list = [mgp.DEFAULT_MZ_TRIM_PERC, mgp.DEFAULT_MZ_RANDNUM_PERC]
            widgets.extend([self.ms_radiobutton_lf, self.inten_radiobuttons,
                            self.trim_radiobuttons])

            for entry, const in zip(entries_list, const_list):
                entry.create()
                entry.entry.insert(index = 0, string = const)
                entry.entry.config(state = tk.DISABLED)

            self.trim_perc_entry.text_var.trace("w", lambda a,b,c: wmf.maintain_four_digit_integer(entry_object = self.trim_perc_entry,
                                                                                                   max_len = mgp.LEN_5_DIGIT_INT))
            self.gen_randnum_perc_entry.text_var.trace("w",
                                                       lambda a,b,c: wmf.maintain_four_digit_integer(entry_object = self.gen_randnum_perc_entry,
                                                                                                     max_len = mgp.LEN_5_DIGIT_INT))

            wmf.maintain_four_digit_integer(entry_object = self.trim_perc_entry, is_startup = True, 
                                            max_len = mgp.LEN_5_DIGIT_INT, default_value = "70")
            wmf.maintain_four_digit_integer(entry_object = self.gen_randnum_perc_entry, is_startup = True, 
                                            max_len = mgp.LEN_5_DIGIT_INT, default_value = "15")
        for widget in widgets:
            widget.create()
       


             
########################################################################
