import numpy as np
import os
import h5py
import datetime as dt

class SweepProcessing:
    
    def __init__(self, times, num_pixels, filepath, metadata):
        # remove any unwanted file extension and add hdf5 extension
        self.filename = os.path.splitext(filepath)[0]
        self.hdf5_filename = self.filename+'.hdf5'
        # add indices to filename if it already exists to avoid overwriting
        i = 1
        while os.path.isfile(self.hdf5_filename) is True:
            self.hdf5_filename = self.filename+'_'+str(i)+'.hdf5'
            i += 1
        self.metadata = metadata
        self.sweep_index = 0
        self.times = np.array(times, ndmin=2)
        self.sweep_index_array = np.zeros(shape=(self.times.size, 1))
        self.pixels = np.linspace(0, num_pixels-1, num_pixels)
        self.current_data = np.zeros(shape=(self.times.size, num_pixels))
        self.avg_data = np.zeros(shape=(self.times.size, num_pixels))
        
    def add_current_data(self, spectrum, time_point):
        self.current_data[time_point, :] = spectrum
        if self.sweep_index == 0:
            self.avg_data[time_point, :] = spectrum
        else:
            self.avg_data[time_point, :] = np.array(((self.avg_data[time_point, :]*self.sweep_index_array[time_point])+spectrum)/(self.sweep_index_array[time_point]+1))
        self.sweep_index_array[time_point] = self.sweep_index_array[time_point]+1 
        return
            
    def next_sweep(self):
        self.sweep_index = self.sweep_index+1
        self.current_data = np.zeros(shape=(self.times.size, self.pixels.size))
        return
        
    def save_current_data(self, wavelengths):
        save_data = np.vstack((np.hstack((0, wavelengths)),
                               np.hstack((self.times.T, self.current_data))))
        with h5py.File(self.hdf5_filename) as hdf5_file:
            dset = hdf5_file.create_dataset('Sweeps/Sweep_'+str(self.sweep_index), data=save_data)
            dset.attrs['date'] = str(dt.datetime.now().date()).encode('ascii', 'ignore')
            dset.attrs['time'] = str(dt.datetime.now().time()).encode('ascii', 'ignore')
        return
        
    def save_avg_data(self, wavelengths):
        save_data = np.vstack((np.hstack((0, wavelengths)),
                               np.hstack((self.times.T, self.avg_data))))
        with h5py.File(self.hdf5_filename) as hdf5_file:
            try:
                dset = hdf5_file['Average']
                dset[:, :] = save_data
                dset.attrs.modify('end_date', str(dt.datetime.now().date()).encode('ascii', 'ignore'))
                dset.attrs.modify('end_time', str(dt.datetime.now().time()).encode('ascii', 'ignore'))
                dset.attrs.modify('num_sweeps', str(self.sweep_index).encode('ascii', 'ignore'))
            except:
                self.save_metadata_initial()
                dset = hdf5_file.create_dataset('Average', data=save_data)
                dset.attrs['start date'] = str(dt.datetime.now().date()).encode('ascii', 'ignore')
                dset.attrs['start time'] = str(dt.datetime.now().time()).encode('ascii', 'ignore')
                for key, item in self.metadata.items():
                    dset.attrs[key] = str(item).encode('ascii', 'ignore')
                dset.attrs['num_sweeps'] = str(self.sweep_index).encode('ascii', 'ignore')
        return
        
    def save_metadata_initial(self):
        with h5py.File(self.hdf5_filename) as hdf5_file:
            data = np.zeros((1, 1))
            dset = hdf5_file.create_dataset('Metadata', data=data)
            for key, item in self.metadata.items():
                dset.attrs[key] = str(item).encode('ascii', 'ignore')

