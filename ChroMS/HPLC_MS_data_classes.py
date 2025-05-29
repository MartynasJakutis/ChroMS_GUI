from numpy import (
	array as np_array, 
	transpose as np_transpose, 
	where as np_where, 
	float64 as np_float64)

class HPLC_MS_Data(object):
    """A parent class of HPLC_3D_Data and MS_Data"""
    def __init__(self, file):
        self.file = file
        
    def make_row_numeric(self, row_list):
        """Checks if all items in provided row are convertible to floats, converts them and returns as list.
        Otherwise, default row_list is returned"""
        try:
            return list(map(float, row_list)) #[float(member) for member in row_list]
        except:
            return row_list
            
    def make_data_list(self):
        """Creates and returns data_list containing all data rows. The data is taken from .txt file."""
        data_file = open(self.file, "r")
        data_list = [self.make_row_numeric(row.split()) for row in data_file if row != "\n"]
        data_file.close()
        return data_list
        
    def get_front_index(self, referenz, data_list):
        """Returns front_ind which indicates position of reference value in the .txt file"""
        if referenz in data_list:
            front_ind = data_list.index(referenz)
        return front_ind
        
class HPLC_3D_Data(HPLC_MS_Data):
    """Used to precess HPLC 3D data and store relevant information about the sample.
    wave_nm - tailored wavelenght (int), used to create chromatogram (nm)."""
    def __init__(self, file):
        super().__init__(file)
    def read(self):
        """Creates attributes which represent injection volume, all wavelenghts (nm), retention time (min), 
        all absorption intensities (AU) and absorption intensity at provided wavelenght (AU)."""
        self.injection_vol = "Unknown"
        front_ref_line = ['[PDA', '3D]']
        
        data_list = self.make_data_list()
        
        for row in data_list:
            if "Injection" and "Volume" in row:
                self.injection_vol = row[2]
                break
                
        front_ind = self.get_front_index(front_ref_line, data_list)
            
        data_list = data_list[front_ind + 9 :]
        
        self.wavelengths = (np_array(data_list[0]) // 100)
        
        self.data_array = np_array(data_list[1:])
        if self.data_array.dtype == np_float64:
            self.retention_time = self.data_array[:, 0]
            self.all_ab_intensities = self.data_array[:, 1:] / 1000
            
    def get_ab_intensity_of_wv(self, wave_nm):
        self.wave_nm = wave_nm
        if self.data_array.dtype == np_float64:
            wv_index = (np_where(self.wavelengths == self.wave_nm)[0])[0]
            self.ab_intensity = self.all_ab_intensities[:, wv_index]
            self.all_ab_intensities = np_transpose(self.all_ab_intensities)

    def get_max_ab_intensities_by_rts(self, rt_pos, rt_dev):
        self.rt_pos_prob_ind, self.rt_dev_prob_ind = [], []
        not_none = all([x != None for x in [rt_pos, rt_dev]])
        if not_none:
            len_rt_pos, self.len_rt_dev_init = len(rt_pos), len(rt_dev)
            if len_rt_pos != self.len_rt_dev_init:
                rt_dev = rt_dev * len_rt_pos 

            conditions_inten = [(self.retention_time >= pos - dev) & (self.retention_time <= pos + dev) for pos, dev in zip(rt_pos, rt_dev)]
            self.max_ab_intensities = [self.ab_intensity[c].max() if c.sum() != 0 else None for c in conditions_inten]

            if any([x == None for x in self.max_ab_intensities]):
                self.get_problematic_rt_pos_and_rt_dev_ind()
                self.rts_of_max_intensity = 0
                return

            self.max_ab_indices = [self.ab_intensity[c].argmax() for c in conditions_inten]
            self.rts_of_max_intensity = [self.retention_time[c][ind] for c, ind in zip(conditions_inten, self.max_ab_indices)]
        else:
            self.max_ab_intensities = 0
            self.rts_of_max_intensity = 0

    def get_problematic_rt_pos_and_rt_dev_ind(self):
        for i, max_ab_inten in enumerate(self.max_ab_intensities):
            if max_ab_inten == None:
                self.rt_pos_prob_ind.append(i)
                added_ind_rt_dev = 0 if self.len_rt_dev_init == 1 else i
                self.rt_dev_prob_ind.append(added_ind_rt_dev)
    

class MS_Data(HPLC_MS_Data):
    """For MS 2D data processing (time vs intensity). retention_time, ionization_type - str."""
    def __init__(self, file):
        super().__init__(file)
        self.retention_time = "Unknown"
        self.ionization_type = "Unknown"
        
    def read(self, intensity_type):
        """modifies retention_time and ionization_type and creates attributes of mass and charge ratio (m/z), absolute intensity,
        relative_intensity"""
        ms_event_dict = {1 : r'$\mathtt{[M + H^{+}]^{+}}$',
                         2 : r'$\mathtt{[M - H^{+}]^{-}}$'}
        front_ref_line = ['m/z', 'Absolute', 'Intensity', 'Relative', 'Intensity']
        
        data_list = self.make_data_list()

        for row in data_list:
            if "Raw" and "Spectrum" in row:
                self.retention_time = row[2].split(",")[0][1:-1]
                break

        front_ind = self.get_front_index(front_ref_line, data_list)
        
        for row in data_list[::-1]:
            if row == ['Event', '1'] or ['Event', '2']:
                self.ionization_type = ms_event_dict[int(row[1])]
                back_ind = data_list.index(row)
                break
                
        data_list = data_list[front_ind + 1 : back_ind]
        
        self.data_array = np_array(data_list)
        if self.data_array.dtype == np_float64:
            get_inten_meth_dict = {"absolute" : lambda : self.get_absolute_intensity(),
                                   "relative_perc" : lambda : self.get_relative_intensity_perc(),
                                   "relative_frac" : lambda : self.get_relative_intensity_frac()}
            self.mz = self.data_array[:, 0]
            get_inten_meth_dict.get(intensity_type)()
            #self.absolute_intensity = self.data_array[:, 1]
            
    def get_absolute_intensity(self):
        self.intensity = self.data_array[:, 1]
    def get_relative_intensity_perc(self):
        self.intensity = self.data_array[:, 2]
    def get_relative_intensity_frac(self):
        self.get_relative_intensity_perc()
        self.intensity = self.intensity / 100
