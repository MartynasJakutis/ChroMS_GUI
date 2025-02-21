import tkinter as tk
import Custom_tkinter_widget_classes as ctwc
import Widget_manipulation_functions as wmf
import Main_GUI_parameters as mgp

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
                                                      "row" : 2, "column" : 1}})
        for frame in self.frame_params.keys():
            self.frames[frame] = ctwc.Frame(style = "NewCusFrame.TFrame", sticky = tk.E + tk.W, 
                                            **self.frame_params[frame]).create()
            
        self.label_params = self.label_params_func(plot_opt_lf = self.labelframes["plot_opt"])
        if self.purpose == "chrom":                                                       
            self.label_params.update({"label2" : {"master" : self.labelframes["plot_opt"], "text" : "Wavelength, nm: ", 
                                                  "row" : 1, "column" : 0, "sticky" : tk.W},
                                      "label3" : {"master" : self.labelframes["plot_opt"], "text" : "Find peaks: ", 
                                                  "row" : 2, "column" : 0, "sticky" : tk.W},
                                      "label4" : {"master" : self.labelframes["plot_opt"], "text" : "Range: ", 
                                                  "row" : 3, "column" : 0, "sticky" : tk.W},
                                      "label5" : {"master" : self.frames["wavelength"], "text" : "\tIntensity, AU: ", 
                                                  "row" : 0, "column" : 1, "sticky" : tk.W},
                                      "label6" : {"master" : self.frames["wavelength"], "text" : "min", 
                                                  "row" : 0, "column" : 2, "sticky" : tk.W},
                                      "label7" : {"master" : self.frames["wavelength"], "text" : "max", 
                                                  "row" : 0, "column" : 4, "sticky" : tk.W},
                                      "label8" : {"master" : self.frames["find_peaks"], "text" : "±", 
                                                  "row" : 0, "column" : 1, "sticky" : tk.W},
                                      "label9" : {"master" : self.frames["find_peaks"], "text" : "min.", 
                                                  "row" : 0, "column" : 3, "sticky" : tk.W}})
            
            
        for label in self.label_params.keys():
            padx = (5, 20) if label == "label9" else (5, 0)
            self.labels[label] = ctwc.Label(padx = padx, pady = 0, background = "SystemButtonFace",
                                            style = "Normal.TLabel", **self.label_params[label]).create()
        
            
    def create_advanced_widgets(self):
        """Creates widgets which are supposed to have additional functionality"""
        self.output = ctwc.Outputwidget(master = self.labelframes["output"], width = 65, height = 6.5, 
                                        font = ("DefaultTkFont", 12, "normal"), row = 0, column = 0, 
                                        padx = 2.5, pady = 0)
        widgets = [self.output]
        self.output.create()
        if self.purpose == "chrom":
            self.wv_entry = ctwc.Entry(master = self.frames["wavelength"], style = "TEntry", 
                                       font = ("TkDefaultFont", 12, "normal"), width = 5, 
                                       row = 0, column = 0, padx = 2.5, pady = (2.5, 1.25), sticky = tk.E + tk.W)
            self.inten_min_entry = ctwc.Entry(master = self.frames["wavelength"], style = "TEntry", 
                                       font = ("TkDefaultFont", 12, "normal"), width = 8, 
                                       row = 0, column = 3, padx = 2.5, pady = (2.5, 1.25), sticky = tk.E + tk.W)
            self.inten_max_entry = ctwc.Entry(master = self.frames["wavelength"], style = "TEntry", 
                                       font = ("TkDefaultFont", 12, "normal"), width = 8, 
                                       row = 0, column = 5, padx = 2.5, pady = (2.5, 1.25), sticky = tk.E + tk.W)
            self.peak_value_entry = ctwc.Entry(master = self.frames["find_peaks"], style = "TEntry", 
                                       font = ("TkDefaultFont", 12, "normal"), width = 15, 
                                       row = 0, column = 0, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
            self.peak_dev_entry = ctwc.Entry(master = self.frames["find_peaks"], style = "TEntry", 
                                       font = ("TkDefaultFont", 12, "normal"), width = 8, 
                                       row = 0, column = 2, padx = 2.5, pady = 1.25, sticky = tk.E + tk.W)
            for entry, const in zip([self.wv_entry, self.inten_min_entry, self.inten_max_entry, 
                                     self.peak_value_entry, self.peak_dev_entry],
                                    [mgp.DEFAULT_WAVELENGTH, mgp.DEFAULT_MIN_INTENSITY, mgp.DEFAULT_MAX_INTENSITY,
                                     mgp.DEFAULT_PEAK_POS_SEQ, mgp.DEFAULT_PEAK_DEV_SEQ]):
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

        else:
            pass
        self.output.create()
    def create_all_widgets(self):
        self.load_widget_params()
        self.create_simple_widgets()
        self.create_advanced_widgets()


class FileFolderManagerBackbone(OutputPlotManagerBackbone):
    """Class which contains methods for File and Folder Manager Backbone (ffm) creation.
    master - higher hierarchy widget, purpose - str which refers what kind of ffm to create."""
    def __init__(self, master, purpose):
        super().__init__(master, purpose)
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
            self.labels[label] = ctwc.Label(padx = (5, 0), pady = 0, background = "SystemButtonFace",
                                            style = "Normal.TLabel", **self.label_params[label]).create()
    def create_advanced_widgets(self):
        """Creates widgets which are supposed to have additional functionality"""
        self.combobox = ctwc.ComboBox(master = self.labelframes["file_input"],
                                      width = 70, row = 0, column = 1)
        self.listbox = ctwc.Listbox(master = self.frames["listbox"], background = 'black', foreground = 'green', width = 70, 
                                    height = 10, selectbackground = 'gray', selectforeground = 'black', row = 0, column = 0, 
                                    padx = (0, 0), pady = 0, padx_scroll = 0, pady_scroll = 0, exportselection = False)
        self.file_search_entry = ctwc.Entry(master = self.frames["file_search"], style = "TEntry", 
                                            font = ("TkDefaultFont", 12, "normal"), width = 55, 
                                            row = 0, column = 1, padx = 2.5, pady = 2.5, sticky = tk.E + tk.W)
        self.file_search_entry.create_file_name_filter()
        for widget in [self.combobox, self.listbox, self.file_search_entry]:
            widget.create()
