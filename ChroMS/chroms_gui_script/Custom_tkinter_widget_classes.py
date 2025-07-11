import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tk_st

import Path_manipulation_functions as pmf

from time import (strftime as time_strftime)

class Hauptwidget_Grid(object):
    """Parent of other tkinter custom widget classes."""
    def __init__(self, master, row, column):
        self.master = master
        self.row = row
        self.column = column

class Tab(object):
    def __init__(self, master, text, style):
        self.master = master
        self.text = text
        self.style = style
        
    def create(self):
        self.tab = ttk.Frame(master = self.master, style = self.style)
        self.master.add(self.tab, text = self.text)
        return self.tab
    
class Frame(Hauptwidget_Grid):
    def __init__(self, master, style, sticky = None, row = None, column = None):
        super().__init__(master, row, column)
        self.sticky = sticky
        self.style = style
        
    def create(self):
        self.frame = ttk.Frame(master = self.master, style = self.style)
        if self.row == None and self.column == None and self.sticky == None:
            self.frame.pack()
        else:
            self.frame.grid(row = self.row, column = self.column, sticky = self.sticky)
        return self.frame

class NotebookWithSbFrames(Hauptwidget_Grid):
    def __init__(self, master, style, sticky, row, column, padx, pady, tab_names):
        super().__init__(master, row, column)
        self.style = style
        self.sticky = sticky
        self.tab_names = tab_names
        self.tabs = {}
        self.sb_frames = {}
        self.padx = padx
        self.pady = pady

    def add_tabs(self):
        for tab_name in self.tab_names:
            self.tabs[tab_name] = Tab(master = self.notebook, text = tab_name, style = "NewCusFrame.TFrame").create()
            self.sb_frames[tab_name] = ScrollableFrame(master = self.tabs[tab_name], style = "NewCusFrame.TFrame", sticky = tk.E + tk.W,
                                                       row = 0, column = 0)
            self.sb_frames[tab_name].create()

    def create(self):
        self.notebook = ttk.Notebook(master = self.master, style = self.style)
        self.add_tabs()
        self.notebook.grid(row = self.row, column = self.column, sticky = self.sticky, padx = self.padx, pady = self.pady)

class ScrollableFrame(Hauptwidget_Grid):
    def __init__(self, master, style, sticky, row, column):
        super().__init__(master, row, column)
        self.style = style
        self.sticky = sticky

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def populate(self):
        '''Put in some fake data'''
        for row in range(100):
            tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Label(self.frame, text=t).grid(row=row, column=1)
        
    def create(self):
        self.outer_frame = ttk.Frame(master = self.master, style = self.style)
        self.canvas = tk.Canvas(master = self.outer_frame, 
                                borderwidth = 0, background = "#ffffff", width = 450, height = 220)
        self.frame = ttk.Frame(master = self.canvas)
        self.vsb = tk.Scrollbar(master = self.outer_frame, orient = "vertical",
                                command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.vsb.set)
        self.vsb.pack(side = "right", fill = "y")
        self.canvas.pack(side = "left", fill = "both", expand = True)
        self.canvas.create_window((4,4), window = self.frame, anchor = "nw",
                                  tags = "self.frame")
        self.outer_frame.pack(side="top", fill="both", expand=True)
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.populate()

class LabelFrame(Hauptwidget_Grid):
    def __init__(self, master, text, row, column, padx, pady, height, width, style, sticky = '', rowspan = 0):
        super().__init__(master, row, column)
        self.text = text
        self.padx = padx
        self.pady = pady
        self.height = height
        self.width = width
        self.style = style
        self.sticky = sticky
        self.rowspan = rowspan
        
    def create(self):
        self.labelwidget = ttk.Label(master = self.master, text = self.text, style = "Bold.TLabel")
        self.labelframe = ttk.LabelFrame(self.master, height = self.height, width = self.width,
                                         style = self.style, labelwidget = self.labelwidget)
        self.labelframe.grid(row = self.row, column = self.column,
                             padx = self.padx, pady = self.pady, sticky = self.sticky)
        return self.labelframe

class Label(Hauptwidget_Grid):
    def __init__(self, master, text, style, row, column, sticky, background, padx, pady):
        super().__init__(master, row, column)
        self.text = text
        self.style = style
        self.sticky = sticky
        self.background = background
        self.padx = padx
        self.pady = pady
        
    def create(self):
        self.label = ttk.Label(master = self.master, text = self.text, style = self.style)
        self.label.grid(row = self.row, column = self.column, sticky = self.sticky,
                        padx = self.padx, pady = self.pady)
        self.label.configure(background = self.background)
        return self.label

class Entry(Hauptwidget_Grid):
    def __init__(self, master, style, font, width, row, column, padx, pady, sticky = ''):
        super().__init__(master, row, column)
        self.style = style
        self.font = font
        self.width = width
        self.padx = padx
        self.pady = pady
        self.sticky = sticky
        self.text_var = tk.StringVar()
        self.text_var.set("")
        
    def create(self):
        self.entry = ttk.Entry(master = self.master, style = self.style, font = self.font,
                               width = self.width, textvariable = self.text_var)
        self.entry.grid(row = self.row, column = self.column,
                        padx = self.padx, pady = self.pady, sticky = self.sticky)
        
    def create_file_name_filter(self):
        self.FILE_NAME_FILTER = ""

    def change_entry_text(self, change_to):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, change_to)
    
    def change_entry_text_and_icursor(self, entry_text, cursor_ind):
        self.change_entry_text(change_to = entry_text)
        self.entry.icursor(cursor_ind)

    def get_clipboard(self):
        try: 
           self.clipboard = self.entry.clipboard_get()
        except: 
           self.clipboard = ''   

    def replace_selection(self, num_type = "int"):
        entry_text = self.entry.get()
        selection = self.entry.selection_get()
        start_ind = self.entry.index("sel.first")
        end_ind = self.entry.index("sel.last")
        if num_type == "int":
            if len(self.clipboard) <= len(selection):
                entry_text = entry_text[ : start_ind] + self.clipboard + entry_text[end_ind : ]
                self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = start_ind + len(self.clipboard))
            else: 
                truncated_clipboard = self.clipboard[ : end_ind - start_ind]
                entry_text = entry_text[ : start_ind] + truncated_clipboard + entry_text[end_ind : ]
                self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = start_ind + len(truncated_clipboard))
        elif num_type == "float":
            if any([x in self.clipboard for x in [".", "-"]]):
                entry_text = self.clipboard
                self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = len(self.clipboard)) 
            else:
                entry_text = entry_text[ : start_ind] + self.clipboard + entry_text[end_ind : ]
                self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = start_ind + len(self.clipboard))
        elif num_type == "sequence":
            entry_text = entry_text[ : start_ind] + self.clipboard + entry_text[end_ind : ]
            cursor_ind = start_ind + len(self.clipboard)
            #self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = cursor_ind)
            return entry_text, cursor_ind
    
    def maintain_entry_len(self, max_len, cursor_ind, num_type = "int", string = None, total_current_len = 0):
        item = string if num_type == "sequence" else self.entry.get()
        item_len = len(item)
        cursor_diff = cursor_ind - total_current_len
        cursor_after_item = cursor_diff == item_len
        if num_type == "int":
            condition = item_len > max_len
            ind = max_len if cursor_after_item else cursor_ind
            max_ind = max_len + 1
        elif num_type == "float":
            condition = len(item.split(".")[1]) > max_len
            ind = item.find(".") + max_len + 1 if cursor_after_item else cursor_ind
            max_ind = item.find(".") + max_len + 2
        elif num_type == "sequence":
            condition = len(item.split(".")[1]) > max_len
            ind = item.find(".") + max_len + 1
            max_ind = item.find(".") + max_len + 2

        if condition:
            new_item = item[ : ind] + item[ind + 1 : max_ind]
            if num_type in ["int", "float"]:
                self.change_entry_text_and_icursor(entry_text = new_item, cursor_ind = ind)

        if num_type == "sequence":
            if condition:
                len_diff = len(item) - len(new_item)
                if cursor_ind > total_current_len + len(new_item):
                    cursor_ind -= len_diff
            else:
                new_item = item
            return new_item, cursor_ind
    
    def paste(self, max_len = 4, num_type = "int", is_startup = False, provided_clip = "", default_value = ""):

        def replace_with_cb(clipboard_string):
            self.change_entry_text_and_icursor(entry_text = clipboard_string, cursor_ind = len(clipboard_string))

        def set_entry_text_for_startup():
            if is_startup:
                self.change_entry_text(change_to = default_value)

        cursor_ind = 0 if is_startup else self.entry.index(tk.INSERT)
        entry_text = self.entry.get()
        if is_startup:
            self.clipboard = provided_clip
        else:
            self.get_clipboard()

        self.entry.clipboard_clear()
        
        len_sum = len(entry_text) + len(self.clipboard)
        if num_type == "int" and self.clipboard.isdecimal():
            if self.entry.selection_present():
                self.replace_selection(num_type = num_type)
            else:
                if len(self.clipboard) >= 3:
                    replace_with_cb(clipboard_string = self.clipboard)
                elif len_sum <= max_len:
                    entry_text = entry_text[: cursor_ind] + self.clipboard + entry_text[cursor_ind :]
                    self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = cursor_ind + len(self.clipboard))
                else:
                    replace_with_cb(clipboard_string = self.clipboard)

        elif num_type == "float" and self.clipboard.replace(".", "", 1).replace("-", "", 1).isdecimal():
            if self.entry.selection_present():
                self.replace_selection(num_type = num_type)
            else:
                if self.clipboard.find("-") == 0 and (self.clipboard.find(".") > self.clipboard.find("-")):
                    replace_with_cb(clipboard_string = self.clipboard)

                elif "-" in self.clipboard and self.clipboard.index("-") == 0:
                    replace_with_cb(clipboard_string = self.clipboard)
                else:
                    if all([x not in self.clipboard for x in [".", "-"]]):
                        entry_text = entry_text[: cursor_ind] + self.clipboard + entry_text[cursor_ind :]
                        self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = cursor_ind + len(self.clipboard))
                    elif "." in self.clipboard and (not "-" in self.clipboard):
                        condition = entry_text.find(".") <= cursor_ind and entry_text.find(".") != -1
                        cursor_ind -= 1 if condition else cursor_ind
                        entry_text = entry_text.replace(".", "")
                        entry_text = entry_text[: cursor_ind] + self.clipboard + entry_text[cursor_ind :]
                        self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = cursor_ind + len(self.clipboard))
                    else:
                        set_entry_text_for_startup()
        
        elif num_type == "sequence" and (self.clipboard.replace(".", "").replace(",", "").isdecimal()):
            are_appropriate_nums = all([x.count(".") <= 1 for x in entry_text.split(",")])
            if are_appropriate_nums:
                if self.entry.selection_present():
                    entry_text, cursor_ind = self.replace_selection(num_type = num_type)
                else:
                    entry_text = entry_text[ : cursor_ind] + self.clipboard + entry_text[cursor_ind : ]
                    cursor_ind = cursor_ind + len(self.clipboard)
                self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = cursor_ind)

                values = self.entry.get().split(",")
                
                total_current_len = 0

                for i, value in enumerate(values):
                    if "." in value:
                        value, cursor_ind = self.maintain_entry_len(max_len = max_len, cursor_ind = cursor_ind, num_type = num_type, 
                                                                    string = value, total_current_len = total_current_len)
                    values[i] = value
                    total_current_len += len(value) + 1
                entry_text = ",".join(values)
                if is_startup:
                    self.change_entry_text_and_icursor(entry_text = "", cursor_ind = 0)
                self.change_entry_text_and_icursor(entry_text = entry_text, cursor_ind = cursor_ind)
        else:
            set_entry_text_for_startup()
        if num_type == "int" or (num_type == "float" and "." in self.entry.get()):
            self.maintain_entry_len(max_len = max_len, cursor_ind = cursor_ind, num_type = num_type)

        self.entry.after(20, lambda: self.entry.clipboard_append(self.clipboard))

    def bind_key_or_event(self, key_or_event, func):
        self.entry.bind(key_or_event, func)
        
class Button(Hauptwidget_Grid):
    def __init__(self, master, text, command, row, column, padx, pady):
        super().__init__(master, row, column)
        self.text = text
        self.command = command
        self.padx = padx
        self.pady = pady
        
    def create(self):
        self.tk_styles = ttk.Style()
        tk_style_theme = self.tk_styles.theme_use()
        if tk_style_theme == "classic":
            self.button = ttk.Button(master = self.master, text = self.text, command = self.command,
                                     width = 9, padding = (0,0))
        else:
            self.button = ttk.Button(master = self.master, text = self.text, command = self.command)
        self.button.grid(row = self.row, column = self.column, padx = self.padx, pady = self.pady)
        return self.button
    
class ComboBox(Hauptwidget_Grid):
    def __init__(self, master, width, row, column):
        super().__init__(master, row, column)
        self.width =  width
        
    def create(self):
        self.textvar = tk.StringVar()
        self.combobox = ttk.Combobox(master = self.master, width = self.width, 
                                     textvariable = self.textvar)
        self.combobox.grid(row = self.row, column = self.column)
        return self.combobox

    def set_history_folder(self, folder):
        folder_obj = pmf.MyDir(dir_name = folder)
        folder_obj.create()
        self.hist_folder_name = folder
        self.hist_folder_path = folder_obj.path

        
    def add(self, value):
        """Adds new value into combobox. The maximum size of combobox - 10 items. Every item appears once per item list.
        The last used item inserted at the top of the item list. value - str."""
        def rm_and_ins_into_list(modlist, pop_index, ins_value):
                modlist.pop(pop_index)
                modlist.insert(0, ins_value)
        list_of_tuple = list(self.combobox["values"])
        if value in list_of_tuple:
            rm_and_ins_into_list(modlist = list_of_tuple, pop_index = list_of_tuple.index(value),
                                 ins_value = value)
        else:
            if len(self.combobox["values"]) < 10:
                list_of_tuple.insert(0, value)
            else:
                rm_and_ins_into_list(modlist = list_of_tuple, pop_index = -1,
                                     ins_value = value)
        self.combobox["values"] = tuple(list_of_tuple)
        
    def save(self, name):
        """Saves contents of combobox to the 'name'(str) + '_history.txt' file which will be located in the folder.
        folder, name - str."""
        self.set_history_folder(folder = self.hist_folder_name)
        file = open(pmf.get_path(self.hist_folder_path, name + "_history.txt"), "w", encoding = "utf-8")
        for i in self.combobox["values"]:
            file.write(i + "\n")
        file.close()
        
    def load(self, name):
        """Loads contents of history file located in specified folder in to combobox. folder, name - str."""
        self.set_history_folder(folder = self.hist_folder_name)
        if name + "_history.txt" in pmf.listdir(self.hist_folder_path):
            file = open(pmf.get_path(self.hist_folder_path, name + "_history.txt"), "r", encoding = "utf-8")
            list_of_file = file.readlines()
            file.close()
            for i in list_of_file[::-1]:
                i_without_endl = i[:-1]
                if pmf.isdir(i_without_endl):
                    self.add(value = i_without_endl)
            if len(self.combobox["values"]) != 0:
                self.combobox.current(0)
                
    def get_select_option(self):
        """Provides selected combobox item and rearranges the order of combobox items"""
        self.selected_folder = self.combobox.get()
        list_of_tuple = list(self.combobox["values"])
        if list_of_tuple == []:
            pass
        else:
            ind = list_of_tuple.index(self.selected_folder)
            removed_folder = list_of_tuple.pop(ind)
            list_of_tuple.insert(0, removed_folder)
            self.combobox["values"] = tuple(list_of_tuple)
            
    def bind_key_or_event(self, key_or_event, func):
        self.combobox.bind(key_or_event, func)

class Listbox(Hauptwidget_Grid):
    def __init__(self, master, background, foreground, width, height, selectbackground, selectforeground,
                 row, column, padx, pady, padx_scroll, pady_scroll, exportselection):
        super().__init__(master, row, column)
        self.background = background
        self.foreground = foreground
        self.width = width
        self.height = height
        self.selectbackground = selectbackground
        self.selectforeground = selectforeground
        self.padx = padx
        self.pady = pady
        self.padx_scroll = padx_scroll
        self.pady_scroll = pady_scroll
        self.exportselection = exportselection
        
    def create(self):
        self.listbox = tk.Listbox(master = self.master, background = self.background, 
                                  foreground = self.foreground, width = self.width, 
                                  height = self.height, selectbackground = self.selectbackground, 
                                  selectforeground = self.selectforeground,
                                  exportselection = self.exportselection)
        self.listbox.grid(row = self.row, column = self.column, padx = self.padx, pady = self.pady)
        self.scrollbary = tk.Scrollbar(master = self.master, orient = "vertical")
        self.scrollbarx = tk.Scrollbar(master = self.master, orient = "horizontal")
        self.scrollbarx.grid(row = self.row + 1, column = self.column, padx = self.padx_scroll, pady = self.pady_scroll,
                             sticky = tk.E + tk.W)
        self.scrollbary.grid(row = self.row, column = self.column + 1, padx = self.padx_scroll, pady = self.pady_scroll,
                             sticky = tk.N + tk.S)

        self.listbox.config(xscrollcommand = self.scrollbarx.set, yscrollcommand = self.scrollbary.set)
        self.scrollbary.config(command = self.listbox.yview)
        self.scrollbarx.config(command = self.listbox.xview)
        self.all_items = self.listbox.get(0, tk.END)
        
    def get_select_option(self):
        """Provides currently selected value in the listbox."""
        current_selection = self.listbox.curselection()[0]
        self.selected_file = self.listbox.get(current_selection)
        
    def clear(self):
        self.listbox.delete(0, tk.END)
        
    def going_up_down(self, direction):
        """Enables scrolling through listbox items in cyclic manner."""
        def set_and_activate(new_active_item_index):
            self.listbox.activate(new_active_item_index)
            self.listbox.select_set(new_active_item_index)
        active_item = self.listbox.get(tk.ACTIVE)
        active_item_index = self.all_items.index(active_item)
        self.listbox.select_clear(tk.ACTIVE)
        if direction == "down":
            if active_item == self.listbox.get(tk.END):
                set_and_activate(0)
            else:
                set_and_activate(active_item_index + 1)
        elif direction == "up":
            if active_item == self.listbox.get(0):
                set_and_activate(tk.END)
            else:
                set_and_activate(active_item_index -1)
                
    def bind_key_or_event(self, key_or_event, func):
        self.listbox.bind(key_or_event, func)
        
class Checkbutton(Hauptwidget_Grid):
    def __init__(self, master, text, command, row, column, is_selected, padx, pady):
        super().__init__(master, row, column)
        self.text = text
        self.var = tk.IntVar()
        self.onvalue = 1
        self.offvalue = 0
        self.command = command
        self.is_selected = is_selected
        self.padx = padx
        self.pady = pady
        
    def create(self):
        self.checkbutton = ttk.Checkbutton(master =  self.master, text = self.text, 
                                           var = self.var, onvalue = self.onvalue, 
                                           offvalue = self.offvalue, command = self.command)
        if self.is_selected:
            self.checkbutton.state(["selected"])
            pass
        else:
            self.checkbutton.state(["!selected"])
            pass
        self.checkbutton.grid(row = self.row, column = self.column, padx = self.padx, pady = self.pady)

class Radiobutton(Hauptwidget_Grid):
    def __init__(self, master, text, command, row, column, var, onvalue, padx, pady):
        super().__init__(master, row, column)
        self.text = text
        self.var = var
        self.onvalue = onvalue
        self.command = command
        self.padx = padx
        self.pady = pady
        
    def create(self):
        self.radiobutton = ttk.Radiobutton(master = self.master,
                                           text = self.text, variable = self.var, 
                                           value = self.onvalue, command = self.command)
        self.radiobutton.grid(row = self.row, column = self.column, padx = self.padx, pady = self.pady)
        
    def disable(self):
        """Disable the possibility to select the radiobutton."""
        self.radiobutton.config(state = tk.DISABLED)
        
    def enable(self):
        """Enable selection of the radiobutton."""
        self.radiobutton.config(state = tk.ACTIVE)
        
class Outputwidget(Hauptwidget_Grid):
    """Custom scrollable text widget."""
    def __init__(self, master, width, height, font, row, column, padx, pady):
        super().__init__(master, row, column)
        self.width = width
        self.height = height
        self.font = font
        self.padx = padx
        self.pady = pady
        
    def create(self):
        
        self.text_out = tk_st.ScrolledText(master = self.master, width = self.width, 
                                           height = self.height, font = self.font)
        self.text_out.grid(row = self.row, column = self.column,
                           padx = self.padx, pady = self.pady)
        greet_text = ("Welcome to ChroMS GUI (2024) for HPLC-MS result analysis and visualization.\n" + 
                      "Have a good time using that, MATE.")
        self.insert_text(text = greet_text, output_type = "greeting")

    def insert_text(self, text, output_type):
        """Inserts text to the widget according to tailored message type and scrolls the widget contents all the way.
        text, output_type - str."""
        self.enable_modifications(value = True)
        output_types = {"greeting" : "#",
                        "success" : "+",
                        "warning" : "?"}
        symbol = output_types.get(output_type)
        symbol_line = symbol * self.width
        current_time = time_strftime("%Y/%m/%d   %H:%M:%S")
        time_str = "{0:{1}<{2}}\n".format(current_time, symbol, self.width)
        term_text = symbol_line + "\n" + current_time + "\n" + text + "\n" + symbol_line
        self.text_out.insert(tk.END, term_text)
        self.enable_modifications(value = False)
        self.text_out.yview_moveto(fraction = 1)
        
    def enable_modifications(self, value):
        """Enables or disables modifications of the text. value - bool"""
        states = {True : "normal", False : "disabled"}
        state = states.get(value)
        self.text_out.configure(state = state)
