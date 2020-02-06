"""
write some stuff here about versions, contacts etc and code layout
"""

# general
import sys
import os
from PyQt5 import QtGui, QtCore

# gui object
from gui import Ui_pyTGgui as pyTGgui

# graphics
import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# data manipulation
import numpy as np
import pandas as pd

# hardware
from camera import Camera, Acquisition
from delay import DelayStage

# sweep processing
from sweeps import SweepProcessing

# hack to get the app to display an icon (Windows OS only?)
#import ctypes
#ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('pyTG')


class Application(QtGui.QMainWindow):
    
    def __init__(self, last_instance_filename, last_instance_values=None, preloaded=False):     
        super(Application, self).__init__()
        self.ui=pyTGgui()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.ui.tabs.setCurrentIndex(0)
        self.show()
        self.last_instance_filename = last_instance_filename
        self.last_instance_values = last_instance_values
        self.preloaded = preloaded
        self.camera_connected = False
        self.delaystage_connected = False
        self.metadata = {}
        self.datafolder = os.path.join(os.path.expanduser('~'), 'Documents', 'data')
        self.setup_dropdowns()
        self.setup_gui_connections()
        self.initialise_gui_values()
        self.update_gui_values()
        self.idle = True
        self.write_app_status('application launched', colour='blue')
        
    def setup_dropdowns(self):
        self.ui.a_distribution_cb.addItem('Exponential')
        self.ui.a_distribution_cb.addItem('Linear')
        self.ui.a_ordering_cb.addItem('Linear')
        self.ui.a_ordering_cb.addItem('Random')
        
    def setup_gui_connections(self):
        # hardware tab: iCCD
        self.ui.h_iCCD_connect_btn.clicked.connect(self.exec_h_camera_connect_btn)
        self.ui.h_delaystage_connect_btn.clicked.connect(self.exec_h_delaystage_connect_btn)
        # acquisition tab: acquisition settings
        self.ui.a_exp_time_sb.valueChanged.connect(self.update_a_exp_time)
        self.ui.a_num_accum_sb.valueChanged.connect(self.update_a_num_accum)
        self.ui.a_gain_sb.valueChanged.connect(self.update_a_gain)
        self.ui.a_gate_delay_sb.valueChanged.connect(self.update_a_gate_delay)
        self.ui.a_gate_width_sb.valueChanged.connect(self.update_a_gate_width)
        # diagnostics tab: acquisition settings
        self.ui.d_exp_time_sb.valueChanged.connect(self.update_d_exp_time)
        self.ui.d_num_accum_sb.valueChanged.connect(self.update_d_num_accum)
        self.ui.d_gain_sb.valueChanged.connect(self.update_d_gain)
        self.ui.d_gate_delay_sb.valueChanged.connect(self.update_d_gate_delay)
        self.ui.d_gate_width_sb.valueChanged.connect(self.update_d_gate_width)
        # acquisition tab: time points setup
        self.ui.a_distribution_cb.currentIndexChanged.connect(self.update_times)
        self.ui.a_start_time_sb.valueChanged.connect(self.update_times)
        self.ui.a_end_time_sb.valueChanged.connect(self.update_times)
        self.ui.a_num_points_sb.valueChanged.connect(self.update_times)
        self.ui.a_ordering_cb.currentIndexChanged.connect(self.update_times)
        self.ui.a_num_sweeps_sb.valueChanged.connect(self.update_num_sweeps)
        # acquisition tab: metadata
        self.ui.a_pump_wl_le.textChanged.connect(self.update_metadata)
        self.ui.a_pump_power_le.textChanged.connect(self.update_metadata)
        self.ui.a_spot_size_le.textChanged.connect(self.update_metadata)
        # acquisition tab: file stuff
        self.ui.a_folder_browse_btn.clicked.connect(self.exec_folder_browse_btn)
        self.ui.a_filename_le.textChanged.connect(self.update_filepath)
        # diagnostics tab: time stuff
        self.ui.d_current_time_sb.valueChanged.connect(self.update_d_current_time)
        self.ui.d_move_to_time_btn.clicked.connect(self.d_move_to_time)
        self.ui.d_time_zero_sb.valueChanged.connect(self.update_time_zero)
        self.ui.d_time_step_sb.valueChanged.connect(self.update_d_time_step)
        self.ui.d_time_forward_btn.clicked.connect(self.d_jog_later)
        self.ui.d_time_back_btn.clicked.connect(self.d_jog_earlier)
        self.ui.d_set_current_time_btn.clicked.connect(self.exec_d_set_current_as_time_zero_btn)
        # diagnostics tab: launch buttons
        self.ui.d_run_btn.clicked.connect(self.exec_d_run_btn)
        self.ui.d_stop_btn.clicked.connect(self.exec_d_stop_btn)
        self.ui.d_acquire_btn.clicked.connect(self.exec_d_single_acquisition_btn)
        return
    
    def initialise_gui_values(self):
        self.ui.h_iCCD_status.setText('no connection')
        self.ui.h_delaystage_status.setText('no connection')
        self.ui.d_autoscale_checkbox.setChecked(True)
        self.ui.d_current_time_sb.setValue(0)
        self.ui.a_sweep_progressbar.setValue(0)
        self.ui.a_measurement_progressbar.setValue(0)
        self.ui.a_filename_le.setText('newfile')
        if self.preloaded:
            self.ui.a_exp_time_sb.setValue(self.last_instance_values['exposure time'])
            self.ui.a_num_accum_sb.setValue(self.last_instance_values['accumulations'])
            self.ui.a_gain_sb.setValue(self.last_instance_values['gain'])
            self.ui.a_gate_width_sb.setValue(self.last_instance_values['gate width'])
            self.ui.a_gate_delay_sb.setValue(self.last_instance_values['gate delay'])
            self.ui.d_time_zero_sb.setValue(self.last_instance_values['time zero'])
            self.ui.a_distribution_cb.setCurrentIndex(self.last_instance_values['distribution'])
            self.ui.a_start_time_sb.setValue(self.last_instance_values['tstart'])
            self.ui.a_end_time_sb.setValue(self.last_instance['tend'])
            self.ui.a_num_points_sb.setValue(self.last_instance_values['num tpoints'])
            self.ui.a_num_sweeps_sb.setValue(self.last_instance_values['num sweeps'])
            self.ui.a_ordering_cb.setCurrentIndex(self.last_instance_values['ordering'])
            self.ui.d_central_wavelength_sb.setValue(self.last_instance_values['central wavelength'])
            self.ui.d_slitwidth_sb.setValue(self.last_instance_values['slit width'])
            self.ui.a_kinetic_wavelength_sb.setValue(self.last_instance_values['wavelength monitored'])
        else:
            self.ui.a_exp_time_sb.setValue(0.05)
            self.ui.a_num_accum_sb.setValue(1)
            self.ui.a_gain_sb.setValue(0)
            self.ui.a_gate_width_sb.setValue(2)
            self.ui.a_gate_delay_sb.setValue(2840)
            self.ui.d_time_zero_sb.setValue(10)
            self.ui.a_distribution_cb.setCurrentIndex(0)
            self.ui.a_start_time_sb.setValue(-5)
            self.ui.a_end_time_sb.setValue(1000)
            self.ui.a_num_points_sb.setValue(100)
            self.ui.a_num_sweeps_sb.setValue(3)
            self.ui.a_ordering_cb.setCurrentIndex(0)
            self.ui.d_central_wavelength_sb.setValue(600)
            self.ui.d_slitwidth_sb.setValue(200)
            self.ui.a_kinetic_wavelength_sb.setValue(600)
        return
        
    def update_gui_values(self):
        self.update_a_exp_time()
        self.update_a_num_accum()
        self.update_a_gain()
        self.update_a_gate_delay()
        self.update_a_gate_width()
        self.update_central_wavelength()
        self.update_filepath()
        self.update_kinetics_wavelength()
        self.update_metadata()
        self.update_time_zero()
        self.update_times()
        self.update_slit_width()
        self.update_num_sweeps()
        self.update_d_current_time()
        self.update_d_time_step()
        return
        
    def save_gui_values(self):
        self.last_instance_values['exposure time'] = self.ui.a_exp_time_sb.value()
        self.last_instance_values['accumulations'] = self.ui.a_num_accum_sb.value()
        self.last_instance_values['gain'] = self.ui.a_gain_sb.value()
        self.last_instance_values['gate delay'] = self.ui.a_gate_delay_sb.value()
        self.last_instance_values['gate width'] = self.ui.a_gate_width_sb.value()
        self.last_instance_values['time zero'] = self.ui.d_time_zero_sb.value()
        self.last_instance_values['distribution'] = self.ui.a_distribution_cb.currentIndex()
        self.last_instance_values['tstart'] = self.ui.a_start_time_sb.value()
        self.last_instance_values['tend'] = self.ui.a_end_time_sb.value()
        self.last_instance_values['num tpoints'] = self.ui.a_num_points_sb.value()
        self.last_instance_values['num sweeps'] = self.ui.a_num_sweeps_sb.value()
        self.last_instance_values['ordering'] = self.ui.a_ordering_cb.currentIndex()
        self.last_instance_values['central wavelength'] = self.ui.d_central_wavelength_sb.value()
        self.last_instance_values['slit width'] = self.ui.d_slitwidth_sb.value()
        self.last_instance_values['wavelength monitored'] = self.ui.a_kinetic_wavelength_sb.value()
        self.pl.to_csv(self.last_instance_filename, sep=':', header=False)
        
    def update_a_exp_time(self):
        self.exp_time = self.ui.a_exp_time_sb.value()
        self.ui.d_exp_time_sb.setValue(self.exp_time)
        return
    
    def update_d_exp_time(self):
        self.exp_time = self.ui.d_exp_time_sb.value()
        self.ui.a_exp_time_sb.setValue(self.exp_time)
        return
    
    def update_a_num_accum(self):
        self.num_accum = self.ui.a_num_accum_sb.value()
        self.ui.d_num_accum_sb.setValue(self.num_accum)
        return
    
    def update_d_num_accum(self):
        self.num_accum = self.ui.d_num_accum_sb.value()
        self.ui.a_num_accum_sb.setValue(self.num_accum)
        return
    
    def update_a_gain(self):
        self.gain = self.ui.a_gain_sb.value()
        self.ui.d_gain_sb.setValue(self.gain)
        return
    
    def update_d_gain(self):
        self.gain = self.ui.d_gain_sb.value()
        self.ui.a_gain_sb.setValue(self.gain)
        return
    
    def update_a_gate_delay(self):
        self.gate_delay = self.ui.a_gate_delay_sb.value()
        self.ui.d_gate_delay_sb.setValue(self.gate_delay)
        return
    
    def update_d_gate_delay(self):
        self.gate_delay = self.ui.d_gate_delay_sb.value()
        self.ui.a_gate_delay_sb.setValue(self.gate_delay)
        return
    
    def update_a_gate_width(self):
        self.gate_width = self.ui.a_gate_width_sb.value()
        self.ui.d_gate_width_sb.setValue(self.gate_width)
        return
    
    def update_d_gate_width(self):
        self.gate_width = self.ui.d_gate_width_sb.value()
        self.ui.a_gate_width_sb.setValue(self.gate_width)
        return
    
    def update_times(self):
        distribution = self.ui.a_distribution_cb.currentText()
        start_time = self.ui.a_start_time_sb.value()
        end_time = self.ui.a_end_time_sb.value()
        num_points = self.ui.a_num_points_sb.value()
        ordering = self.ui.a_ordering_cb.currentText()
        times = np.linspace(start_time, end_time, num_points)
        if distribution == 'Exponential':
            times = self.calculate_times_exponential(start_time, end_time, num_points)
        if ordering == 'Random':
            np.random.shuffle(times)
        self.times = times
        return
    
    @staticmethod
    def calculate_times_exponential(start_time, end_time, num_points):
        num_before_zero = 20
        step = 0.1
        before_zero = np.linspace(start_time, 0, num_before_zero, endpoint=False)
        zero_onwards = np.geomspace(step, end_time+step, num_points-num_before_zero)-step
        times = np.concatenate((before_zero, zero_onwards))
        return times
    
    def update_num_sweeps(self):
        self.num_sweeps = self.ui.a_num_sweeps_sb.value()
        return
    
    def update_metadata(self):
        self.metadata['pump wavelength'] = self.ui.a_pump_wl_le.text()
        self.metadata['pump power'] = self.ui.a_pump_power_le.text()
        self.metadata['pump spot size'] = self.ui.a_spot_size_le.text()
        
    def update_kinetics_wavelength(self):
        self.kinetics_wavelength = self.ui.a_kinetic_wavelength_sb.value()
        return
    
    def update_central_wavelength(self):
        self.central_wavelength = self.ui.d_central_wavelength_sb.value()
        # move spectrograph
        return
    
    def update_slit_width(self):
        self.slit_width = self.ui.d_slitwidth_sb.value()
        # move slit
        return
    
    def update_time_zero(self):
        self.time_zero = self.ui.d_time_zero_sb.value()
        if self.delaystage_connected:
            self.delaystage.t0 = self.time_zero
        return
    
    def update_d_time_step(self):
        self.d_time_step = self.ui.d_time_step_sb.value()
        return
    
    def update_filepath(self):
        self.filename = self.ui.a_filename_le.text()
        self.filepath = os.path.join(self.datafolder, self.filename)
        self.ui.a_filepath_le.setText(self.filepath)
        return
   
    def exec_folder_browse_btn(self):
        self.datafolder = QtGui.QFileDialog.getExistingDirectory(None, 'Select Folder', self.datafolder)
        self.datafolder = os.path.normpath(self.datafolder)
        self.update_filepath()
        return
        
    def write_log(self, message):
        self.ui.log_window.appendPlainText(message)
        return
    
    def write_app_status(self, message, colour, timeout=0):
        self.ui.statusBar.clearMessage()
        self.ui.statusBar.setStyleSheet('QStatusBar{color:'+colour+';}')
        self.ui.statusBar.showMessage(message, msecs=timeout)
        return
        
    def update_sweep_progress_bar(self, i):
        self.ui.a_sweep_progressbar.setValue(i)
        return
    
    def update_measurement_progress_bar(self, i):
        self.ui.a_measurement_progressbar.setValue(i)
        return
    
    def update_d_current_time(self):
        self.d_current_time = self.ui.d_current_time_sb.value()
        return
    
    def update_iCCD_temperature_displays(self, current_temperature):
        lcd_colour = '(255, 0, 0)' if current_temperature > -30.0 else '(0, 0, 255)'
        self.ui.h_temperature_lcd.setStyleSheet('QLCDNumber{background-color: rgb'+lcd_colour+';}')
        self.ui.h_temperature_lcd.display(current_temperature)
        self.ui.d_temperature_lcd.setStyleSheet('QLCDNumber{background-color: rgb'+lcd_colour+';}')
        self.ui.d_temperature_lcd.display(current_temperature)
        self.ui.a_temperature_lcd.setStyleSheet('QLCDNumber{background-color: rgb'+lcd_colour+';}')
        self.ui.a_temperature_lcd.display(current_temperature)
    
    def exec_h_camera_connect_btn(self):
        self.ui.h_iCCD_status.setText('establishing connection ...')
        self.camera = Camera()
        self.ui.h_iCCD_status.setText('cooling down iCCD - please wait ...')
        self.camera.initialise()
        current_temperature = self.camera.get_temperature()
        self.update_iCCD_temperature_displays(current_temperature)
        while current_temperature > -30.0:
            current_temperature = self.camera.get_temperature()
            self.update_iCCD_temperature_displays(current_temperature)
        self.ui.h_iCCD_status.setText('applying acquisition settings ...')
        self.apply_acquisition_settings()
        self.camera_connected = True
        self.ui.h_iCCD_status.setText('ready')
        
    def apply_acquisition_settings(self):
        self.camera.exposure_time = self.exp_time
        self.camera.gain = self.gain
        self.camera.num_accumulations = self.num_accum
        self.camera.gate_delay = self.gate_delay
        self.camera.gate_width = self.gate_width
        self.camera.apply_acquisition_settings()
        return
    
    def update_h_stage_position(self, current_position):
        self.ui.h_delaystage_position_lcd.display(current_position)
        return
    
    def exec_h_delaystage_connect_btn(self):
        self.ui.h_delaystage_status.setText('establishing connection ...')
        self.delaystage = DelayStage(self.time_zero)
        self.ui.h_delaystage_status.setText('referencing - please wait ...')
        self.delaystage.initialise()
        self.ui.h_delaystage_status.setText('homing - please wait ...')
        self.delaystage.home()
        self.ui.h_delaystage_status.setText('moving to previous time zero - please wait ...')
        self.delaystage.move_to(0)
        self.delaystage_connected = True
        self.ui.h_delaystage_status.setText('ready')
      
    def create_plots(self):
        self.ui.a_spectrum_graph.plotItem.setLabels(left='PL (counts)', bottom='Wavelength (nm)')
        self.ui.a_spectrum_graph.plotItem.showAxis('top', show=True)
        self.ui.a_spectrum_graph.plotItem.showAxis('right', show=True)
        
        self.ui.a_kinetics_graph.plotItem.setLabels(left='PL (counts)', bottom='Time (ps)')
        self.ui.a_kinetics_graph.plotItem.showAxis('top', show=True)
        self.ui.a_kinetics_graph.plotItem.showAxis('right', show=True)
        
        self.ui.d_spectrum_graph.plotItem.setLabels(left='PL (counts)', bottom='Wavelength (nm)')
        self.ui.d_spectrum_graph.plotItem.showAxis('top', show=True)
        self.ui.d_spectrum_graph.plotItem.showAxis('right', show=True)
        return
    
    def d_spectrum_plot(self):
        self.ui.d_spectrum_graph.plotItem.plot(self.current_data[:, 0], self.current_data[:, 1], pen='r', clear=True)
        return
    
    """    
    def region_updated(self,regionItem):
        px1,px2 = regionItem.getRegion()
        self.ui.d_vline1.display(px1)
        self.ui.d_vline2.display(px2)
        return
        
    def create_plot_waves_and_times(self):
        '''updates all plots within the gui. Note that it will only plot the ones
           that are displayed. When an acquisition is running, it is possible to
           switch between the acquire and diagnostics tab and the plots will update
           accordingly'''
        self.waves = self.pixels_to_waves()
        if self.use_calib is True:
            self.plot_waves = self.pixels_to_waves()
        else:
            self.plot_waves = np.linspace(0,self.num_pixels-1,self.num_pixels)
        
        if self.use_actual_times is True:
            self.plot_times = self.times
        else:
            self.plot_times = np.linspace(0,self.times.size-1,self.times.size)
        
        if self.use_logscale is True:
            self.plot_times = np.log10(self.plot_times)
            
        self.ui.kinetic_wave.display(self.plot_waves[self.kinetic_pixel])
        self.ui.spectra_time.display(self.plot_times[self.spectra_timestep])
        
        if self.diagnostics_on is False:
            self.plot_dtt = self.current_sweep.avg_data[:]
        self.plot_ls = self.current_data.dtt[:]
        self.plot_probe_shot_error = self.current_data.probe_shot_error[:]
        if self.ui.d_use_reference.isChecked() is True:
            self.plot_ref_shot_error = self.current_data.ref_shot_error[:]
            self.plot_dtt_error = self.current_data.dtt_error[:]
        self.plot_probe_on = self.current_data.probe_on[:]
        self.plot_reference_on = self.current_data.reference_on[:]
        self.plot_probe_on_array = self.current_data.probe_on_array[:]
        self.plot_reference_on_array = self.current_data.reference_on_array[:]
        if self.use_cutoff is True:
            self.plot_waves = self.plot_waves[self.cutoff[0]:self.cutoff[1]]
            if self.diagnostics_on is False:
                self.plot_dtt = self.plot_dtt[:,self.cutoff[0]:self.cutoff[1]]
            self.plot_ls = self.plot_ls[self.cutoff[0]:self.cutoff[1]]
            self.plot_probe_shot_error = self.plot_probe_shot_error[self.cutoff[0]:self.cutoff[1]]
            if self.ui.d_use_reference.isChecked() is True:
                self.plot_ref_shot_error = self.plot_ref_shot_error[self.cutoff[0]:self.cutoff[1]]
                self.plot_dtt_error = self.plot_dtt_error[self.cutoff[0]:self.cutoff[1]]
            self.plot_probe_on = self.plot_probe_on[self.cutoff[0]:self.cutoff[1]]
            self.plot_reference_on = self.plot_reference_on[self.cutoff[0]:self.cutoff[1]]
            self.plot_probe_on_array = self.plot_probe_on_array[:,self.cutoff[0]:self.cutoff[1]]
            self.plot_reference_on_array = self.plot_reference_on_array[:,self.cutoff[0]:self.cutoff[1]]        
        return
        
    def pixels_to_waves(self):
        '''uses calibration values to transform pixels to wavelength values'''
        slope = (self.calib[3]-self.calib[2])/(self.calib[1]-self.calib[0])
        y_int = self.calib[2]-slope*self.calib[0]
        return np.linspace(0,self.num_pixels-1,self.num_pixels)*slope+y_int
                
    def ls_plot(self):
        '''last shot plot on acquire tab'''
        try:
            self.ui.last_shot_graph.plotItem.plot(self.plot_waves,self.plot_ls,clear=True,pen='b')
        except:
            self.append_history('Error Plotting Last Shot')
        return
        
    def top_plot(self):
        '''top plot on acquire tab'''
        try:
            self.ui.top_graph.setImage(self.plot_dtt,scale=(len(self.plot_waves)/len(self.plot_times),1))
        except:
            self.append_history('Error Plotting Top Plot')
        return
        
    def kin_plot(self):
        '''kinetic plot on acquire tab'''
        self.update_kinetic_pixel()
        if self.use_logscale is True:
            plot_times = self.plot_times[np.isfinite(self.plot_times)]
        else:
            plot_times = self.plot_times
        try:
            kinetic_pixel_index = self.kinetic_pixel if not self.use_cutoff else self.kinetic_pixel-self.cutoff[0]
            self.ui.kinetic_graph.plotItem.plot(plot_times, self.plot_dtt[np.isfinite(self.plot_times), kinetic_pixel_index], pen='r', clear=True)
        except:
            self.append_history('Error Plotting Kinetic Plot')
        return
        
    def spec_plot(self):
        '''spectra plot on acquire tab'''
        self.update_spectra_timestep()
        try:
            self.ui.spectra_graph.plotItem.plot(self.plot_waves,self.plot_dtt[self.spectra_timestep,:],pen='g',clear=True)
        except:
            self.append_history('Error Plotting Spectra Plot')
        return
        
    def d_error_plot(self):
        '''error plot on diagnostics tab'''
        try:
            self.ui.d_error_graph.plotItem.plot(self.plot_waves,np.log10(self.plot_probe_shot_error),pen='r',clear=True,fillBrush='r')
            if self.ui.d_use_reference.isChecked() is True:         
                self.ui.d_error_graph.plotItem.plot(self.plot_waves,np.log10(self.plot_ref_shot_error),pen='g',clear=False,fillBrush='g')    
                self.ui.d_error_graph.plotItem.plot(self.plot_waves,np.log10(self.plot_dtt_error),pen='b',clear=False,fillBrush='b')
        except:
            self.append_history('Error plotting error!')
        self.ui.d_error_graph.plotItem.setYRange(-4,1,padding=0)
        return
        
    def d_trigger_plot(self):
        '''trigger plot on diagnostics tab'''
        try:
            self.ui.d_trigger_graph.plotItem.plot(np.arange(self.num_shots),self.current_data.trigger,pen=None,symbol='o',clear=True)
        except:
            self.append_history('Error Plotting Trigger')
        return
        
    def d_probe_ref_plot(self):
        '''probe and reference spectra plot on diagnostics tab'''
        for item in self.ui.d_probe_ref_graph.plotItem.listDataItems():
            self.ui.d_probe_ref_graph.plotItem.removeItem(item)
        try:
            if self.ui.d_display_mode.currentIndex() == 0:
                self.ui.d_probe_ref_graph.plotItem.plot(self.plot_waves,self.plot_probe_on,pen='r')
                if self.ui.d_use_reference.isChecked() is True:
                    self.ui.d_probe_ref_graph.plotItem.plot(self.plot_waves,self.plot_reference_on,pen='b')
            if self.ui.d_display_mode.currentIndex() == 1:
                if self.ui.d_display_mode_spectra.currentIndex() == 0:
                    for spec in self.plot_probe_on_array:
                        self.ui.d_probe_ref_graph.plotItem.plot(self.plot_waves,spec,pen='r')
                if self.ui.d_display_mode_spectra.currentIndex() == 1:
                    for spec in self.plot_reference_on_array:
                        self.ui.d_probe_ref_graph.plotItem.plot(self.plot_waves,spec,pen='b')
        except:
            self.append_history('Error Plotting Probe and/or Reference Spectra')
        return
        
    def d_ls_plot(self):
        '''last shot plot on diagnostics tab'''
        try:
            self.ui.d_last_shot_graph.plotItem.plot(self.plot_waves,self.plot_ls,pen='b',clear=True)
        except:
            self.append_history('Error Plotting Last Shot')
        return
        

    """
        
    def message_block(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText('block pump beam')
        msg.setInformativeText('press once and wait for background acquisition')
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        retval = msg.exec_()
        return retval
        
    def message_unblock(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("unblock pump beam")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        retval = msg.exec_()
        return retval
        
    def message_time_points(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText('one or more time points exceed delay stage limits')
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        retval = msg.exec_()
        return retval
        
    def message_error_saving(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("error saving file")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        retval = msg.exec_()
        return retval
    
    def running(self):
        self.idle = False
        # enable / disable stuff
        return
            
    def idling(self):
        self.idle = True
        # enable / disable stuff
        return
    
    """    
    def acquire(self):
        '''acquire data from camera'''
        self.append_history('Acquiring '+str(self.num_shots)+' shots')
        self.camera.start_acquire.emit()  # connects to the Acquire signal in the camera class, which results in a signal data_ready being emitted containing the data from probe and reference. This signal connects to post_acquire method, which loops back to acquire
        return
        
    def post_acquire(self,probe,reference,first_pixel,num_pixels):
        '''process ta data according to functions found in ta_data_processing.py'''
        try:
            self.current_data.update(probe,
                                     reference,
                                     first_pixel,
                                     num_pixels)
        except:
             self.current_data = taDataProcessing(probe,
                                                  reference,
                                                  first_pixel,
                                                  num_pixels)
        if self.ui.d_use_linear_corr.isChecked():
            try:
                self.current_data.linear_pixel_correlation(self.linear_corr)
            except:
                self.append_history('Error using linear pixel correction')
        self.high_trig_std = self.current_data.separate_on_off(self.threshold,self.tau_flip_request)
        if self.ui.test_run_btn.isChecked() is False:
            self.current_data.sub_bgd(self.bgd)
        if self.ui.d_use_ref_manip.isChecked() is True:
            self.current_data.manipulate_reference(self.refman)
        self.current_data.average_shots()
        if self.ui.d_use_reference.isChecked() is True:
            self.current_data.correct_probe_with_reference()
            self.current_data.average_refd_shots()
            self.high_dtt = self.current_data.calcuate_dtt(use_reference=True,cutoff=self.cutoff,use_avg_off_shots=self.ui.d_use_avg_off_shots.isChecked(),max_dtt=np.abs(self.ui.d_max_dtt.value()))
            self.current_data.calculate_dtt_error(use_reference=True,use_avg_off_shots=self.ui.d_use_avg_off_shots.isChecked())
        else:
            self.high_dtt = self.current_data.calcuate_dtt(use_reference=False,cutoff=self.cutoff,use_avg_off_shots=self.ui.d_use_avg_off_shots.isChecked(),max_dtt=np.abs(self.ui.d_max_dtt.value()))
            self.current_data.calculate_dtt_error(use_reference=False,use_avg_off_shots=self.ui.d_use_avg_off_shots.isChecked())
        if (self.high_trig_std is False) and (self.high_dtt is False):
            self.current_sweep.add_current_data(self.current_data.dtt,time_point=self.timestep)
        else:
            self.append_history('Did not add last point')
        self.create_plot_waves_and_times()
        if self.ui.acquire_tab.isVisible() is True:
            self.ls_plot()
            self.top_plot()
            self.kin_plot()
            self.spec_plot()
        if self.ui.diagnos_tab.isVisible() is True:
            self.d_ls_plot()
            self.d_error_plot()
            self.d_trigger_plot()
            self.d_probe_ref_plot()
        
        if self.stop_request is True:
            self.finish()
        elif self.timestep == len(self.times)-1:
            self.post_sweep()
        else:
            self.timestep = self.timestep+1
            self.time = self.times[self.timestep]
            self.ui.time_display.display(self.time)
            self.ui.progressBar.setValue(self.timestep+1)
            self.move(self.time)
            self.acquire()
        return
   
    def acquire_bgd(self):
        '''acquire data from camera for background - increases shots by 10x'''
        self.append_history('Acquiring '+str(self.num_shots*10)+' shots')
        self.camera.start_acquire.emit()
        return
        
    def post_acquire_bgd(self,probe,reference,first_pixel,num_pixels):      
        '''process background data'''
        self.message_unblock()
        self.bgd = taDataProcessing(probe,
                                    reference,
                                    first_pixel,
                                    num_pixels)
        if self.ui.d_use_linear_corr.isChecked():
            try:
                self.bgd_data.linear_pixel_correlation(self.linear_corr)
            except:
                self.append_history('Error using linear pixel correction')
        self.bgd.separate_on_off(self.threshold)
        self.bgd.average_shots() 
        self.camera.Exit()
        self.run()          
        return    
    
    def exec_run_btn(self):
        '''executes when run on aquire tab is pressed, if test mode is selected
           data will not be saved. This function loops over the number of sweeps'''
        if self.ui.test_run_btn.isChecked() is True:
            self.append_history('Launching Test Run!')
        else:
            self.append_history('Launching Run!')
        
        self.stop_request = False
        self.diagnostics_on = False
        self.running()
        self.update_num_shots()
        
        if self.delay_type == 0:
            self.append_history('Connecting to short delay stage')
            self.delay = PIShortStageDelay(self.shortstage_t0)
        if self.delay_type == 1:
            self.append_history('Connecting to long delay stage')
            self.delay = PILongStageDelay(self.longstage_t0)
        if self.delay_type == 2:
            self.append_history('Connecting to delay generator')
            self.delay = InnolasPinkLaserDelay(self.pinklaser_t0)
            
        if self.delay.initialized is False:
            self.append_history('Stage Not Initialized Correctly')
            self.idling()
            return
        
        success = self.delay.check_times(self.times)
        if success is False:
            self.message_time_points()
            self.idling()
            return
        
        self.append_history('Initializing Camera')
        self.acquire_thread = QtCore.QThread()
        self.acquire_thread.start()
        
        self.camera = StresingCameraVIS()
        self.num_pixels = self.camera.num_pixels
        self.camera.moveToThread(self.acquire_thread)
        self.camera.start_acquire.connect(self.camera.Acquire)
        self.camera.data_ready.connect(self.post_acquire_bgd)
        
        if self.ui.test_run_btn.isChecked() is False:
            self.camera.Initialize(number_of_scans=self.num_shots*10,exposure_time_us=self.exp_time_us)##,use_ir_gain=self.ui.d_use_ir_gain.isChecked())
            self.message_block()
            self.append_history('Taking Background')
            self.acquire_bgd()
        else:
            self.run()
        return
            
    def run(self):
        self.update_metadata()
        self.current_sweep = SweepProcessing(self.times,self.num_pixels,self.filename,self.metadata)    
        
        self.camera.data_ready.disconnect(self.post_acquire_bgd)
        self.camera.data_ready.connect(self.post_acquire)
        self.camera.Initialize(number_of_scans=self.num_shots,exposure_time_us=self.exp_time_us)##,use_ir_gain=self.ui.d_use_ir_gain.isChecked())
        
        self.append_history('Starting Sweep '+str(self.current_sweep.sweep_index))
        self.ui.sweep_display.display(self.current_sweep.sweep_index+1)
        self.ui.progressBar.setMaximum(len(self.times))
        self.start_sweep()
        
    def finish(self):
        self.camera.Exit()
        self.acquire_thread.quit()
        self.idling()
        try:
            self.delay.close()
        except:
            pass
        return
        
    def start_sweep(self):
        '''loop over number of timesteps in timefile and plots after acquisition'''
        self.timestep = 0
        self.time = self.times[self.timestep]
        self.ui.time_display.display(self.time)
        self.ui.progressBar.setValue(self.timestep+1)
        self.move(self.time)
        self.acquire()
        return
        
    def post_sweep(self):
        if self.ui.test_run_btn.isChecked() is False:
            self.append_history('Saving Sweep '+str(self.current_sweep.sweep_index))
            try:
                self.current_sweep.save_current_data(self.waves)
                self.current_sweep.save_avg_data(self.waves)
                self.current_sweep.save_metadata_each_sweep(self.current_data.probe_on,
                                                            self.current_data.reference_on,
                                                            self.current_data.probe_shot_error)
            except:
                self.message_error_saving()
        
        self.current_sweep.next_sweep()
        
        if self.current_sweep.sweep_index == self.num_sweeps:
            self.finish()
        else:
            self.append_history('Starting Sweep '+str(self.current_sweep.sweep_index))
            self.ui.sweep_display.display(self.current_sweep.sweep_index+1)
            self.start_sweep()
        return
        
    def exec_stop_btn(self):
        '''stops acquisition from running'''
        self.append_history('Stopped')
        self.stop_request=True
        return
        
    def exec_exit_btn(self):
        '''will exit from gui. some safeguarding in case exit is called before stop'''
        self.append_history('Stopped')
        if self.idle is False:
            self.finish()
        self.save_gui_data()
        self.close()
        return
    """
    
    def move(self, new_time): 
        self.delaystage.move_to(new_time)
        return
    
    def d_move_to_time(self):
        self.move(self.d_current_time)
        return
    
    def d_jog_earlier(self):
        new_time = self.d_current_time-self.d_time_step
        self.move(new_time)
        self.ui.d_current_time_sb.setValue(new_time)
        return
    
    def d_jog_later(self):
        new_time = self.d_current_time+self.d_time_step
        self.move(new_time)
        self.ui.d_current_time_sb.setValue(new_time)
        return
        
    def exec_d_set_current_as_time_zero_btn(self):
        self.ui.d_time_zero_sb.setValue(self.d_current_time)
        return
    
    def exec_d_single_acquisition_btn(self):
        self.diagnostics_on = True
        self.running()
        # check that delay time is on stage!
        success = self.delaystage.check_time(self.d_current_time)
        if success is False:
            self.write_log('time point not on stage')
            self.idling()
            return
        # apply current acquisition settings
        self.apply_acquisition_settings()
        # move acquisiton to separate thread
        self.acquisition = Acquisition(self.camera)
        self.acquire_thread = QtCore.QThread()
        self.acquire_thread.start()
        self.acquisition.moveToThread(self.acquire_thread)
        # set up acquire signals
        self.acquisition.start_acquire.connect(self.acquisition.acquire)
        self.acquisition.data_ready.connect(self.d_post_single_acquisition)
        # run
        self.d_run()
        
    def d_post_single_acquisition(self, spectrum):
        self.current_data = spectrum
        self.d_spectrum_plot()
        self.d_finish()
    
    def exec_d_run_btn(self):
        self.stop_request = False
        self.diagnostics_on = True
        self.running()
        # check that delay time is on stage!
        success = self.delaystage.check_time(self.d_current_time)
        if success is False:
            self.write_log('time point not on stage')
            self.idling()
            return
        # apply current acquisition settings
        self.apply_acquisition_settings()
        # move acquisiton to separate thread
        self.acquisition = Acquisition(self.camera)
        self.acquire_thread = QtCore.QThread()
        self.acquire_thread.start()
        self.acquisition.moveToThread(self.acquire_thread)
        # set up acquire signals
        self.acquisition.start_acquire.connect(self.acquisition.acquire)
        self.acquisition.data_ready.connect(self.d_post_acquire)
        # run
        self.d_run()
        
    def d_run(self):
        self.d_move_to_time()
        self.d_acquire()
    
    def d_acquire(self):
        self.acquisition.start_acquire.emit()
        
    def d_post_acquire(self, spectrum):
        self.current_data = spectrum
        self.d_spectrum_plot()
        if self.stop_request is True:
            self.d_finish()
        else:
            self.d_acquire()
        return
    
    def d_finish(self):  
        self.acquire_thread.quit()
        self.idling()
        return
        
    def exec_d_stop_btn(self):
        self.stop_request = True
        return
    
    """    
    def exec_d_exit_btn(self):
        '''will exit from gui - some safeguarding in case exit is called before stop'''
        if self.idle is False:
            self.d_finish()        
        self.save_gui_data()
        self.close()
        return
        

    """

        
def main():
    
    # create application
    QtGui.QApplication.setStyle('breeze')
    app = QtGui.QApplication(sys.argv)
    
    # load the parameter values from last time and launch GUI
    last_instance_filename = 'last_instance_values.txt'
    try:
        last_instance_values = pd.read_csv(last_instance_filename, sep=':', header=None, index_col=0, squeeze=True)
        ex = Application(last_instance_filename, last_instance_values=last_instance_values, preloaded=True)
    except:
        ex = Application(last_instance_filename)

    ex.show()
    ex.create_plots()
    
    # kill application
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
