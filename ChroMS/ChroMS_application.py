import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

import Custom_tkinter_widget_classes as ctwc
from Multifunctional_backbones import MultifunctionalBackbone
import Widget_manipulation_functions as wmf

import Main_GUI_parameters as mgp

import random

class ChroMS_Application(object):
    """The main class of ChroMS application connecting other functions/classes.
    Creates the main window with all the features. Folder name list - a list containing 
    folder names which will be created in working directory"""
    def __init__(self, folder_name_list, window_state, window_title):
        self.folder_name_list = folder_name_list
        self.window_state = window_state
        self.window_title = window_title
        self.tabs = {}
        self.lvl1_frames = {}
        self.tab_configs = {"tab1" : {"text" : mgp.TAB_1_NAME, "style" : "NewTabFrame.TFrame"},
                            "tab2" : {"text" : mgp.HPLC_TAB_NAME, "style" : "NewTabFrame.TFrame"},
                            "tab3" : {"text" : mgp.MS_TAB_NAME, "style" : "NewTabFrame.TFrame"}}

    def create_folders(self):
        for folder in self.folder_name_list:
            wmf.create_dir_if_not_present(dir_name = folder)

    def set_window_params(self):
        self.screenwidth = self.window.winfo_screenwidth()
        self.screenheight = self.window.winfo_screenheight()
        self.window.state(self.window_state)
        self.window.title(self.window_title)
        self.window.geometry(f"{self.screenwidth}x{self.screenheight}")
        
    def define_and_set_styles(self):
        """Sets random tab background color and random tkinter theme."""
        self.tk_styles = ttk.Style()
        
        tab_bg_colors = ["gray" + str(i) for i in range(1, 100)]
        style_themes = self.tk_styles.theme_names()
        
        self.tab_bg_color = tab_bg_colors[random.randint(0, len(tab_bg_colors) - 1)]
        self.theme = style_themes[random.randint(0, len(style_themes) - 1)]

        self.tk_styles.theme_use(self.theme)

        self.widget_styles = {"NewNotebook.TNotebook" : {"background" : self.tab_bg_color, "foreground" : "green"},
                              "Main.TNotebook.Tab" : {"background" : "green", "foreground" : "black", 
                                                 "font" : ("URW Gothic L", 16, "bold"), "padding" : [0, 0], "width" : 10,
                                                 "anchor" : "center"},
                              "Opt.TNotebook.Tab" : {"background" : "green", "foreground" : "black", 
                                                    "font" : ("URW Gothic L", 14, "normal"), "padding" : [0, 0], "width" : 5,
                                                    "anchor" : "center"},
                              "NewTabFrame.TFrame" : {"background" : self.tab_bg_color, "padding" : [0, 0]},
                              "NewCusFrame.TFrame" : {"background" : "SystemButtonFace", "padding" : [0, 0]},
                              "TLabelframe" : {"foreground" : "black", "background" : "SystemButtonFace",
                                               "font": ("TkDefaultFont", 16, "normal")},
                              "Font.TLabelframe" : {"foreground" : "black", "background" : "SystemButtonFace",
                                                    "font" : ("TkDefaultFont", 16, "normal"), 
                                                    "relief" : "solid"},
                              "Bold.TLabel" : {"background" : "SystemButtonFace",
                                               "font" : ("TkDefaultFont", 16, "bold")},
                              "Normal.TLabel" : {"background" : "SystemButtonFace", 
                                                 "font" : ("TkDefaultFont", 12, "normal")},
                              "NegMessage.TLabel" : {"background" : "SystemButtonFace", 
                                                     "font" : ("TkDefaultFont", 12, "underline"),
                                                     "foreground" : "red"}, 
                              "PosMessage.TLabel" : {"background" : "SystemButtonFace", 
                                                     "font" : ("TkDefaultFont", 12, "underline"),
                                                     "foreground" : "green"},
                              "TEntry" : {"font": ("TkDefaultFont", 16, "bold")},
                              #"NoSelect.TEntry" : {"font": ("TkDefaultFont", 16, "bold")},
                              "TButton" : {"background" : "green", 
                                           "font" : ("TkDefaultFont", 12, "normal")},
                              "TCheckbutton" : {"background" : "SystemButtonFace"},
                              "TRadiobutton" : {"background" : "SystemButtonFace"}
                            }
        #self.widget_dynamic_styles = {"NoSelect.TEntry" : {"selectbackground" : [("focus", "white"), ("!focus", "white")],
        #                                                   "selectforeground" : [("focus", "black"), ("!focus", "black")],
        #                                                   "selectborderwidth" : [("focus", 0), ("!focus", 0)]}}

        for style in self.widget_styles.keys():
            self.tk_styles.configure(style = style, **self.widget_styles[style])
        #for dynamic_style in self.widget_dynamic_styles.keys():
        #    self.tk_styles.map(style = dynamic_style, ** self.widget_dynamic_styles[dynamic_style])
        
    def create_notebook(self):
        self.notebook = ttk.Notebook(master = self.window, style = "Main.TNotebook")
        for tab in self.tab_configs.keys():
            self.tabs[tab] = ctwc.Tab(master = self.notebook, **self.tab_configs[tab]).create()
        self.notebook.pack(expand = True, fill = 'both')

        self.lvl1_frame_configs = {f"{tab}_frame" : {"master" : self.tabs[tab]} for tab in self.tab_configs}
        for frame in self.lvl1_frame_configs.keys():
            self.lvl1_frames[frame] = ctwc.Frame(style = "NewTabFrame.TFrame", **self.lvl1_frame_configs[frame]).create()
            
    def create_ms_and_chrom_tabs(self):
        self.chrom_tab = MultifunctionalBackbone(window = self.window, screenheight = self.screenheight, 
                                                 screenwidth = self.screenwidth,
                                                 opm_master = self.lvl1_frames["tab2_frame"], purpose = "chrom")
        self.chrom_tab.concatenate_backbones()
        self.ms_tab = MultifunctionalBackbone(window = self.window, screenheight = self.screenheight, 
                                              screenwidth = self.screenwidth, opm_master = self.lvl1_frames["tab3_frame"],
                                              purpose = "ms")
        self.ms_tab.concatenate_backbones()


    def tab_selected(self, event):
        """Adjusts widget focus during tab selection. The focus will be set on listbox widget of the selected tab."""
        tabtext_tab_dict = {mgp.HPLC_TAB_NAME : self.chrom_tab,
                            mgp.MS_TAB_NAME : self.ms_tab}
        notebook = event.widget
        tab_id = notebook.select()
        tab_text = notebook.tab(tab_id, 'text')
        selected_tab = tabtext_tab_dict.get(tab_text, None)
        if selected_tab == None:
            return
        elif selected_tab == self.ms_tab and selected_tab.ffm_ms_radiobutton_variable.get():
            selected_tab_listbox = selected_tab.ffm2.listbox
        else:
            if selected_tab == self.ms_tab:
                wmf.focus_and_activate_listbox(listbox_object = selected_tab.ffm2.listbox)
            selected_tab_listbox = selected_tab.ffm1.listbox
        wmf.focus_and_activate_listbox(listbox_object = selected_tab_listbox)
        
    def close_window(self):
        if tkinter.messagebox.askokcancel("Quit", "Are you sure about that?"):
            self.window.destroy()
        
    def create_application_body(self):
        """Initializes main application window, customizes it according to predefined parameters, inserts notebook with
        mass spectrometry and hplc tabs for data analysis. Additionally, binding functions to specific events."""
        self.window = tk.Tk()
        
        self.set_window_params()
        self.define_and_set_styles()
        self.create_notebook()
        self.create_ms_and_chrom_tabs()
        
        self.notebook.bind("<<NotebookTabChanged>>", lambda event : self.tab_selected(event))
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window.mainloop()

if __name__ == "__main__":
    app = ChroMS_Application(folder_name_list = mgp.DATA_FOLDER_NAMES,
                             window_state = mgp.WINDOW_STATE, window_title = mgp.WINDOW_TITLE)
    app.create_folders()
    app.create_application_body()