import tkinter as tk

from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.pyplot import style


NONE_TUPLE = (None, None, None, None)

NavigationToolbar2.toolitems = 3 * (NONE_TUPLE,) + (('Home', 'Reset original view', 'home', 'home'),) +\
                               5 * (NONE_TUPLE,) + (('Back', 'Back to  previous view', 'back', 'back'),) +\
                               3 * (NONE_TUPLE,) + (('Forward', 'Forward to next view', 'forward', 'forward'),) +\
                               5 * (NONE_TUPLE,) +\
                               (('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),) +\
                               3 * (NONE_TUPLE,) + (('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),) +\
                               5 * (NONE_TUPLE,) + (('Save', 'Save the figure', 'filesave', 'save_figure'),) +\
                               3 * (NONE_TUPLE,)

class Diagram(object):
    """Parent class of HPLC_Diagram and MS_Diagram. Includes shared attributes and methods."""
    def __init__(self, dpi, need_title1, title1, title1_pos, title1_text_color, 
                 title1_weight, title1_fontsize, xlabel1, xlabel2, ylabel1, ylabel2,
                 xlabel1_pos, xlabel2_pos, ylabel1_pos, ylabel2_pos, 
                 xlabel1_text_color, xlabel2_text_color, ylabel1_text_color, ylabel2_text_color,
                 xlabel1_weight, xlabel2_weight, ylabel1_weight, ylabel2_weight,
                 xlabel1_fontsize, xlabel2_fontsize, ylabel1_fontsize, ylabel2_fontsize,
                 matplotlib_style1, matplotlib_style2, state, 
                 master_labelframe, add_multiplier_w, add_multiplier_h, radiobutton_var, screenheight,
                 screenwidth):
        self.dpi = dpi
        self.need_title1 = need_title1
        self.title1 = title1
        self.title1_pos = title1_pos
        self.title1_text_color = title1_text_color
        self.title1_weight = title1_weight
        self.title1_fontsize = title1_fontsize
        self.xlabel1 = xlabel1
        self.ylabel1 = ylabel1
        self.xlabel2 = xlabel2
        self.ylabel2 = ylabel2
        self.xlabel1_pos = xlabel1_pos
        self.ylabel1_pos = ylabel1_pos
        self.xlabel2_pos = xlabel2_pos
        self.ylabel2_pos = ylabel2_pos
        self.xlabel1_text_color = xlabel1_text_color
        self.xlabel2_text_color = xlabel2_text_color
        self.ylabel1_text_color = ylabel1_text_color
        self.ylabel2_text_color = ylabel2_text_color
        self.xlabel1_weight = xlabel1_weight
        self.xlabel2_weight = xlabel2_weight
        self.ylabel1_weight = ylabel1_weight
        self.ylabel2_weight = ylabel2_weight
        self.xlabel1_fontsize = xlabel1_fontsize
        self.xlabel2_fontsize = xlabel2_fontsize
        self.ylabel1_fontsize = ylabel1_fontsize
        self.ylabel2_fontsize = ylabel2_fontsize
        self.matplotlib_style1 = matplotlib_style1
        self.matplotlib_style2 = matplotlib_style2
        self.state = state
        self.master_labelframe = master_labelframe
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.add_multiplier_w = add_multiplier_w
        self.add_multiplier_h = add_multiplier_h
        self.figsize = (self.screenwidth/(1.9 * self.dpi) * self.add_multiplier_w, 
                        self.screenheight/(1.2 * self.dpi) * self.add_multiplier_h)
        self.radiobutton_var = radiobutton_var
        self.num_subp_padding_dict = {1 : 25, 2 : 15}
        
    def create_a_figure(self):
        """Creates Figure canvas containing matplotlib.Figure object with its 
        toolbar and embeds them inside the master widget"""
        self.fig = Figure(figsize = self.figsize, dpi = self.dpi)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.master_labelframe)
        toolbar = NavigationToolbar2Tk(self.canvas, self.master_labelframe)
        toolbar.update()
        toolbar.pack(fill = tk.BOTH)
        self.canvas.get_tk_widget().pack()

    def add_subplots(self, subplot_name_list, subplot_indexes_list):
        """Updates matplotlib.Figure object by inserting subplots inside."""
        self.subplots_available = {}
        for subplot_name, subplot_index in zip(subplot_name_list, subplot_indexes_list):
            if subplot_name == subplot_name_list[0]:
                self.subplots_available[subplot_name] = self.fig.add_subplot(subplot_index)
                first_subplot = self.subplots_available[subplot_name]
            else:
                self.subplots_available[subplot_name] = self.fig.add_subplot(subplot_index, sharex = first_subplot)
                
    def set_labels(self, subplot, xlabel, xlabel_text_color, xlabel_weight, xlabel_fontsize, xlabel_pos0, xlabel_pos1,
                   ylabel, ylabel_text_color, ylabel_weight, ylabel_fontsize, ylabel_pos0, ylabel_pos1):
        "Sets labels of x and y axes."
        subplot.set_xlabel(xlabel = xlabel, color = xlabel_text_color, weight = xlabel_weight, 
                           fontsize = xlabel_fontsize, x = xlabel_pos0, y = xlabel_pos1)
        subplot.set_ylabel(ylabel = ylabel, color = ylabel_text_color, weight = ylabel_weight, 
                           fontsize = ylabel_fontsize, x = ylabel_pos0, y = ylabel_pos1)

    def set_labels_1st_subplot(self, subplot):
        self.set_labels(subplot = subplot, xlabel = self.xlabel1, xlabel_text_color = self.xlabel1_text_color,
                        xlabel_weight = self.xlabel1_weight, xlabel_fontsize = self.xlabel1_fontsize,
                        xlabel_pos0 = self.xlabel1_pos[0], xlabel_pos1 = self.xlabel1_pos[1],
                        ylabel = self.ylabel1, ylabel_text_color = self.ylabel1_text_color,
                        ylabel_weight = self.ylabel1_weight, ylabel_fontsize = self.ylabel1_fontsize,
                        ylabel_pos0 = self.ylabel1_pos[0], ylabel_pos1 = self.ylabel1_pos[1])
        
    def set_labels_2nd_subplot(self, subplot):
        self.set_labels(subplot = subplot, xlabel = self.xlabel2, xlabel_text_color = self.xlabel2_text_color,
                        xlabel_weight = self.xlabel2_weight, xlabel_fontsize = self.xlabel2_fontsize,
                        xlabel_pos0 = self.xlabel2_pos[0], xlabel_pos1 = self.xlabel2_pos[1],
                        ylabel = self.ylabel2, ylabel_text_color = self.ylabel2_text_color,
                        ylabel_weight = self.ylabel2_weight, ylabel_fontsize = self.ylabel2_fontsize,
                        ylabel_pos0 = self.ylabel2_pos[0], ylabel_pos1 = self.ylabel2_pos[1])

    def set_title_1st_subplot(self, subplot):
        padding = self.num_subp_padding_dict.get(len(self.subplots_available))
        subplot.set_title(label = self.title1, color = self.title1_text_color, weight = self.title1_weight, 
                         fontsize = self.title1_fontsize, x = self.title1_pos[0], y = self.title1_pos[1], pad = padding)

    def set_titles_all(self):
        """Sets title only for the first subplot."""
        for i in self.subplots_available.keys():
            if self.need_title1 == True and i == list(self.subplots_available.keys())[0]:
                self.set_title_1st_subplot(subplot = self.subplots_available[i])
    
    def set_layout(self):
        """Sets figure layout according to the current Diagram object state."""
        layouts_dict = {"initial" : None,
                        "not_initial" : "constrained"}
        selected_layout = layouts_dict.get(self.state)
        self.fig.set_layout_engine(selected_layout)
        
    def plotting_init_state(self, subplot):
        """Plotting initial Diagram state in the subplot."""
        x_ticks = subplot.get_xticks()
        y_ticks = subplot.get_yticks()
        x_pos = x_ticks.mean()
        y_pos = y_ticks.mean()
        subplot.text(x_pos, y_pos, s = "Specimen", weight = 'bold', ha = 'center',
                     va = "center", fontsize = 77, color = "k")

    def set_term_state_plotting_funcs(self, f_subplot1, f_subplot2):
        """Specifies terminal Diagram state plotting functions/methods for different subplots"""
        self.subplots_term_state_funcs = {"subplot1" : f_subplot1,
                                          "subplot2" : f_subplot2}
                
    def draw_diagram(self):
        """Updates figure canvas."""

        subplots_dict = {0 : "both",
                         1 : "subplot1",
                         2 : "subplot2"}
        showed_subplots = subplots_dict.get(self.radiobutton_var.get())
        self.selected_subplots = showed_subplots
        style.use(self.matplotlib_style1)
        
        possible_subplots = {subplots_dict[0] : (lambda : self.add_subplots(["subplot1", "subplot2"], [211, 212])),
                             subplots_dict[1] : (lambda : self.add_subplots(["subplot1"], [111])),
                             subplots_dict[2] : (lambda : self.add_subplots(["subplot2"], [111]))}
    
        possible_subplots[showed_subplots]()

        num_of_subplots = len(self.subplots_available)
        if self.xlabel1 != None: self.original_xlabel1 = self.xlabel1 
        if num_of_subplots > 1:
            self.xlabel1 = None
        else:
            self.xlabel1 = self.original_xlabel1

        subplot_available_keys_dict = {k : [k] for k in ["subplot1", "subplot2"]}

        for i in self.subplots_available.keys():
            subplot_to_draw = self.subplots_available[i]
            if self.state == "initial":
                self.plotting_init_state(subplot = subplot_to_draw)
            else:
                self.subplots_term_state_funcs[i](subplot_to_draw)
                
        self.set_titles_all()
        self.canvas.draw()

    def redraw_diagram(self):
        self.fig.clear()
        self.set_layout()
        self.draw_diagram()
        
    def set_main_param_values(self, **kwargs):
        """Modifies attribute values if such are present."""
        for k, v in kwargs.items():
            if k in dir(self):
                setattr(self, k, v)

class HPLC_Diagram(Diagram):
    def __init__(self, dpi, need_title1, title1, title1_pos, title1_text_color, 
                 title1_weight, title1_fontsize, xlabel1, xlabel2, ylabel1, ylabel2,
                 xlabel1_pos, xlabel2_pos, ylabel1_pos, ylabel2_pos, 
                 xlabel1_text_color, xlabel2_text_color, ylabel1_text_color, ylabel2_text_color,
                 xlabel1_weight, xlabel2_weight, ylabel1_weight, ylabel2_weight,
                 xlabel1_fontsize, xlabel2_fontsize, ylabel1_fontsize, ylabel2_fontsize,
                 matplotlib_style1, matplotlib_style2, state, 
                 master_labelframe, add_multiplier_w, add_multiplier_h, data_rt, data_ab, data_wv_all, data_ab_all,
                 data_wave_nm, intensity_min, intensity_max, peak_intensity, peak_time, show_peak_text, show_peaks, peak_dec_num,
                 provided_xlim, provided_ylim,
                 colorbar_label, colorbar_text_color, colorbar_weight, colorbar_fontsize,
                 radiobutton_var, screenheight, screenwidth):
        super().__init__(dpi, need_title1, title1, title1_pos, title1_text_color, 
                         title1_weight, title1_fontsize, xlabel1, xlabel2, ylabel1, ylabel2,
                         xlabel1_pos, xlabel2_pos, ylabel1_pos, ylabel2_pos, 
                         xlabel1_text_color, xlabel2_text_color, ylabel1_text_color, ylabel2_text_color,
                         xlabel1_weight, xlabel2_weight, ylabel1_weight, ylabel2_weight,
                         xlabel1_fontsize, xlabel2_fontsize, ylabel1_fontsize, ylabel2_fontsize,
                         matplotlib_style1, matplotlib_style2, state, 
                         master_labelframe, add_multiplier_w, add_multiplier_h, radiobutton_var, screenheight,
                         screenwidth)
        self.data_rt = data_rt
        self.data_ab = data_ab
        self.data_ab_all = data_ab_all
        self.data_wv_all = data_wv_all
        self.data_wave_nm = data_wave_nm
        self.intensity_min = intensity_min
        self.intensity_max = intensity_max

        self.peak_intensity = peak_intensity
        self.peak_time = peak_time
        self.show_peak_text = show_peak_text
        self.show_peaks = show_peaks
        self.peak_dec_num = peak_dec_num
        self.provided_xlim = provided_xlim
        self.provided_ylim = provided_ylim

        self.colorbar_label = colorbar_label
        self.colorbar_text_color = colorbar_text_color
        self.colorbar_weight = colorbar_weight
        self.colorbar_fontsize = colorbar_fontsize
        
    def plotting_term_state_heat(self, subplot):
        """Method for HPLC 3D heatmap drawing when Diagram has 'not_initial' state."""    
        heatmap = subplot.pcolormesh(self.data_rt, self.data_wv_all, self.data_ab_all, cmap = 'hot', 
                                     vmin = self.intensity_min, vmax = self.intensity_max)
        self.set_labels_1st_subplot(subplot = subplot)
        subplot.set_ylim(max(self.data_wv_all), min(self.data_wv_all))
        cbar = self.fig.colorbar(heatmap)
        cbar.set_label(label = self.colorbar_label, weight = self.colorbar_weight,
                       fontsize = self.colorbar_fontsize, color = self.colorbar_text_color,
                       rotation = 90, loc = "center")
    
    def plotting_term_state_chrom(self, subplot):
        """Method for chromatogram drawing when Diagram has 'not_initial' state."""
        init_ylabel2 = self.ylabel2
        self.ylabel2 = self.ylabel2 + "\nλ = {0} nm".format(self.data_wave_nm)
        self.set_labels_2nd_subplot(subplot = subplot)
        self.ylabel2 = init_ylabel2
        subplot.plot(self.data_rt, self.data_ab)
        self.set_xlim_ylim_chrom(subplot = subplot)
        self.mark_max_ab_intensities(subplot = subplot)

    def set_xlim_ylim_chrom(self, subplot):
        x_min = min(self.data_rt) if self.provided_xlim[0] == None else self.provided_xlim[0]
        x_max = max(self.data_rt) if self.provided_xlim[1] == None else self.provided_xlim[1]

        y_min = self.data_ab.min() - self.data_ab.max() * 0.1 if self.provided_ylim[0] == None else self.provided_ylim[0]
        y_max = self.data_ab.max() * 1.2 if self.provided_ylim[0] == None else self.provided_ylim[1]
       
        subplot.set_xlim(x_min, x_max)
        subplot.set_ylim(y_min, y_max)

    def redraw_diagram(self):
        """Sets Diagram state according to condition if all attributes are integers and redraws the diagram."""
        are_main_par_ints = [type(x) == int for x in [self.data_wave_nm, self.data_rt, 
                                                      self.data_ab, self.data_ab_all, 
                                                      self.data_wv_all]]        
        self.state = "initial" if all(are_main_par_ints) else "not_initial"
        super().redraw_diagram()
        
    def mark_max_ab_intensities(self, subplot):
        if any([x == 0 for x in [self.peak_time, self.peak_intensity, int(self.show_peaks)]]):
            return
        else:
            subplot.scatter(self.peak_time, self.peak_intensity, color = "k")
            self.write_peak_text(subplot = subplot)

    def write_peak_text(self, subplot):
        if self.show_peak_text:
            for ptime, inten in zip(self.peak_time, self.peak_intensity):
                str_time  = "{0:.{1}f} min".format(ptime, self.peak_dec_num)
                y_text = inten + self.data_ab.max() * 0.1 if inten >= 0 else inten - self.data_ab.max() * 0.1
                subplot.text(ptime, y_text, s = str_time, weight = 'bold', ha = 'center',
                             va = "center", fontsize = 12, color = "k")

class MS_Diagram(Diagram):
    def __init__(self, dpi, need_title1, title1, title1_pos, title1_text_color, 
                 title1_weight, title1_fontsize, need_title2, title2, title2_pos, title2_text_color, 
                 title2_weight, title2_fontsize, xlabel1, xlabel2, ylabel1, ylabel2,
                 xlabel1_pos, xlabel2_pos, ylabel1_pos, ylabel2_pos, 
                 xlabel1_text_color, xlabel2_text_color, ylabel1_text_color, ylabel2_text_color,
                 xlabel1_weight, xlabel2_weight, ylabel1_weight, ylabel2_weight,
                 xlabel1_fontsize, xlabel2_fontsize, ylabel1_fontsize, ylabel2_fontsize,
                 matplotlib_style1, matplotlib_style2, state, 
                 master_labelframe, add_multiplier_w, add_multiplier_h, data_mz1, data_mz2, data_inten1,
                 data_inten2, radiobutton_var, screenheight, screenwidth):
        super().__init__(dpi, need_title1, title1, title1_pos, title1_text_color, 
                         title1_weight, title1_fontsize, xlabel1, xlabel2, ylabel1, ylabel2,
                         xlabel1_pos, xlabel2_pos, ylabel1_pos, ylabel2_pos, 
                         xlabel1_text_color, xlabel2_text_color, ylabel1_text_color, ylabel2_text_color,
                         xlabel1_weight, xlabel2_weight, ylabel1_weight, ylabel2_weight,
                         xlabel1_fontsize, xlabel2_fontsize, ylabel1_fontsize, ylabel2_fontsize,
                         matplotlib_style1, matplotlib_style2, state, 
                         master_labelframe, add_multiplier_w, add_multiplier_h, radiobutton_var,
                         screenheight, screenwidth)
        self.need_title2 = need_title2
        self.title2 = title2
        self.title2_pos = title2_pos
        self.title2_text_color = title2_text_color
        self.title2_weight = title2_weight
        self.title2_fontsize = title2_fontsize
        self.data_mz1 = data_mz1
        self.data_mz2 = data_mz2
        self.data_inten1 = data_inten1
        self.data_inten2 = data_inten2

    def set_title_2nd_subplot(self, subplot):
        padding = self.num_subp_padding_dict.get(len(self.subplots_available))
        subplot.set_title(label = self.title2, color = self.title2_text_color, weight = self.title2_weight, 
                         fontsize = self.title2_fontsize, x = self.title2_pos[0], y = self.title2_pos[1], pad = padding)

    def set_titles_all(self):
        """Sets titles for all subplots."""
        for subplot, need_title, set_title_func in zip(["subplot1", "subplot2"],
                                                       [self.need_title1, self.need_title2],
                                                       [self.set_title_1st_subplot, self.set_title_2nd_subplot]):
            if subplot in self.subplots_available.keys() and need_title:
                set_title_func(subplot = self.subplots_available[subplot])

    def plotting_init_state(self, subplot):
        """Plotting initial Diagram state in the subplot."""
        if self.radiobutton_var.get() > 0:
            super().plotting_init_state(subplot = subplot)
        else:
            for data_mz in [self.data_mz1, self.data_mz2]:
                if type(data_mz) != int:
                    x_pos = data_mz.max()/2 * 1.05
                    y_pos = subplot.get_yticks().mean()
                    subplot.text(x_pos, y_pos, s = "Specimen", weight = 'bold', ha = 'center',
                                 va = "center", fontsize = 77, color = "k")
                    return
            super().plotting_init_state(subplot = subplot)
    
    def plotting_term_state_ms(self, subplot, data_mz, data_inten):
        """Shared plotting algorithm for both subplots."""
        
        if type(data_mz) != int:
            subplot.plot(data_mz, data_inten)
            subplot.set_xlim(min(data_mz), max(data_mz))
        else:
            self.plotting_init_state(subplot = subplot)
    
    def plotting_term_state_ms1(self, subplot):
        """Function of mass spectrum drawing for the upper subplot."""
        self.set_labels_1st_subplot(subplot = subplot)
        self.plotting_term_state_ms(subplot = subplot, 
                                    data_mz = self.data_mz1, data_inten = self.data_inten1)
        
    def plotting_term_state_ms2(self, subplot):
        """Function of mass spectrum drawing for the lower subplot"""
        self.set_labels_2nd_subplot(subplot = subplot)
        self.plotting_term_state_ms(subplot = subplot, 
                                    data_mz = self.data_mz2, data_inten = self.data_inten2)

            
    def redraw_diagram(self, purpose):
        """Redraws the diagram. Figure layout is set in such manner that if there is a subplot without sufficient data,
        it will be set to None. Otherwise the 'constrained' layout is used."""
        attribute_dict = {"ms1" : [self.data_mz1, self.data_inten1],
                          "ms2" : [self.data_mz2, self.data_inten2]}
        are_main_par_ints = all([all([type(x) != int for x in attribute_dict[y]]) for y in attribute_dict])
        not_both_subplots = self.radiobutton_var.get() > 0
        if are_main_par_ints:
            super().redraw_diagram()
        else:
            attributes = attribute_dict.get(purpose)
            if all([type(x) != int for x in attributes]) and not_both_subplots:
                super().redraw_diagram()
            else:
                self.fig.clear()
                self.state = "initial"
                self.set_layout()
                self.state = "not_initial"
                self.draw_diagram()