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
        self.ui.diagnostics_tab.setEnabled(False)
        self.ui.acquisition_tab.setEnabled(False)
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
        self.safe_to_exit = True
        self.write_app_status('application launched', colour='blue')
        
    def closeEvent(self, event):
        if self.safe_to_exit:
            self.save_gui_values()
            event.accept()
        else:
            event.ignore()
            self.message_unsafe_exit()            
        
    def setup_dropdowns(self):
        self.ui.a_distribution_cb.addItem('Exponential')
        self.ui.a_distribution_cb.addItem('Linear')
        self.ui.a_ordering_cb.addItem('Linear')
        #self.ui.a_ordering_cb.addItem('Random')
        return
        
    def setup_gui_connections(self):
        # hardware tab
        self.ui.h_iCCD_connect_btn.clicked.connect(self.exec_h_camera_connect_btn)
        self.ui.h_iCCD_disconnect_btn.clicked.connect(self.exec_h_camera_disconnect_btn)
        self.ui.h_delaystage_connect_btn.clicked.connect(self.exec_h_delaystage_connect_btn)
        self.ui.h_delaystage_disconnect_btn.clicked.connect(self.exec_h_delaystage_disconnect_btn)
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
        self.ui.d_abort_btn.clicked.connect(self.exec_d_abort_btn)
        self.ui.d_exit_btn.clicked.connect(self.exec_exit_btn)
        # acquisition tab: launch buttons
        self.ui.a_run_btn.clicked.connect(self.exec_run_btn)
        self.ui.a_stop_btn.clicked.connect(self.exec_stop_btn)
        self.ui.a_exit_btn.clicked.connect(self.exec_exit_btn)
        # spectrograph stuff
        self.ui.d_central_wavelength_sb.valueChanged.connect(self.update_central_wavelength)
        self.ui.d_slitwidth_sb.valueChanged.connect(self.update_slit_width)
        return
    
    def initialise_gui_values(self):
        self.ui.h_iCCD_status.setText('ready to connect')
        self.ui.h_delaystage_status.setText('ready to connect')
        self.ui.h_iCCD_disconnect_btn.setEnabled(False)
        self.ui.h_delaystage_disconnect_btn.setEnabled(False)
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
            self.ui.a_end_time_sb.setValue(self.last_instance_values['tend'])
            self.ui.a_num_points_sb.setValue(self.last_instance_values['num tpoints'])
            self.ui.a_num_sweeps_sb.setValue(self.last_instance_values['num sweeps'])
            self.ui.a_ordering_cb.setCurrentIndex(self.last_instance_values['ordering'])
            self.ui.d_central_wavelength_sb.setValue(self.last_instance_values['central wavelength'])
            self.ui.d_slitwidth_sb.setValue(self.last_instance_values['slit width'])
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
        return
        
    def update_gui_values(self):
        self.update_a_exp_time()
        self.update_a_num_accum()
        self.update_a_gain()
        self.update_a_gate_delay()
        self.update_a_gate_width()
        self.update_filepath()
        #self.update_kinetics_wavelength()
        self.update_central_wavelength()
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
        self.last_instance_values.to_csv(self.last_instance_filename, sep=':', header=False)
        return
        
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
        if distribution == 'Linear':
            self.ui.a_num_points_sb.setMinimum(5)
        else:
            self.ui.a_num_points_sb.setMinimum(25)
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
        # add more fields here
        return

    def update_kinetics_wavelength(self):
        self.kinetics_wavelength = self.wavelength_marker.value()
        self.kinetics_pixel = int(self.camera.num_pixels*((self.kinetics_wavelength-self.wavelengths[0])/(self.wavelengths[-1]-self.wavelengths[0])))
        if self.final_plots:
            self.a_kinetics_plot()
        return
    
    def update_time_pixel(self):
        self.spectrum_time = self.time_marker.value()
        self.time_pixel = np.where((self.times-self.spectrum_time)**2 == min((self.times-self.spectrum_time)**2))[0][0]
        if self.final_plots:
            self.a_spectrum_plot()
        return
    
    def update_central_wavelength(self):
        self.central_wavelength = self.ui.d_central_wavelength_sb.value()
        if self.camera_connected:
            # move spectrograph
            self.wavelengths = np.linspace(505, 805, self.camera.num_pixels)
            # update plot x-axes
            self.ui.d_spectrum_graph.setXRange(self.wavelengths[0], self.wavelengths[-1], padding=0)
            self.ui.a_spectrum_graph.setXRange(self.wavelengths[0], self.wavelengths[-1], padding=0)
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
        return
    
    def exec_h_camera_connect_btn(self):
        self.ui.h_iCCD_connect_btn.setEnabled(False)
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
        self.safe_to_exit = False
        self.update_central_wavelength()
        if self.delaystage_connected:
            self.ui.acquisition_tab.setEnabled(True)
            self.ui.diagnostics_tab.setEnabled(True)
        self.ui.h_iCCD_disconnect_btn.setEnabled(True)
        self.ui.h_iCCD_status.setText('ready')
        return
        
    def exec_h_camera_disconnect_btn(self):
        self.ui.acquisition_tab.setEnabled(False)
        self.ui.diagnostics_tab.setEnabled(False)
        self.ui.h_iCCD_disconnect_btn.setEnabled(False)
        self.ui.h_iCCD_status.setText('warming up iCCD - please wait ...')
        self.camera.start_warmup()
        current_temperature = self.camera.get_temperature()
        while current_temperature < 0:
            current_temperature = 21
            self.update_iCCD_temperature_displays(current_temperature)
        self.ui.h_iCCD_status.setText('disconnecting ...')
        self.camera.ccdexit()
        self.camera_connected = False
        self.ui.h_iCCD_connect_btn.setEnabled(True)
        self.ui.h_iCCD_status.setText('ready to connect')
        if not self.delaystage_connected:
            self.safe_to_exit = True
        return
        
    def apply_acquisition_settings(self):
        self.camera.exposure_time = self.exp_time
        self.camera.gain = self.gain
        self.camera.num_accumulations = self.num_accum
        self.camera.gate_delay = self.gate_delay
        self.camera.gate_width = self.gate_width
        self.camera.apply_acquisition_settings()
        return
    
    def exec_h_delaystage_connect_btn(self):
        self.ui.h_delaystage_connect_btn.setEnabled(False)
        self.ui.h_delaystage_status.setText('establishing connection ...')
        self.delaystage = DelayStage(self.time_zero)
        self.ui.h_delaystage_status.setText('referencing - please wait ...')
        self.delaystage.initialise()
        self.ui.h_delaystage_status.setText('homing - please wait ...')
        self.delaystage.home()
        self.ui.h_delaystage_status.setText('moving to previous time zero - please wait ...')
        self.delaystage.move_to(0)
        self.delaystage_connected = True
        if self.camera_connected:
            self.ui.acquisition_tab.setEnabled(True)
            self.ui.diagnostics_tab.setEnabled(True)
        self.ui.h_delaystage_disconnect_btn.setEnabled(True)
        self.ui.h_delaystage_status.setText('ready')
        return
        
    def exec_h_delaystage_disconnect_btn(self):
        self.ui.acquisition_tab.setEnabled(False)
        self.ui.diagnostics_tab.setEnabled(False)
        self.ui.h_delaystage_disconnect_btn.setEnabled(False)
        self.ui.h_delaystage_status.setText('closing connection ...')
        self.delaystage.close()
        self.delaystage_connected = False
        self.ui.h_delaystage_connect_btn.setEnabled(True)
        self.ui.h_delaystage_status.setText('ready to connect')
        if not self.camera_connected:
            self.safe_to_exit = True
        return
      
    def create_plots(self):
        self.ui.a_spectrum_graph.plotItem.setLabels(left='PL (counts)', bottom='Wavelength (nm)')
        self.ui.a_spectrum_graph.plotItem.showAxis('top', show=True)
        self.ui.a_spectrum_graph.getAxis('top').style['showValues'] = False
        self.ui.a_spectrum_graph.plotItem.showAxis('right', show=True)
        self.ui.a_spectrum_graph.getAxis('right').style['showValues'] = False        
        
        self.ui.a_kinetics_graph.plotItem.setLabels(left='PL (counts)', bottom='Time (ps)')
        self.ui.a_kinetics_graph.plotItem.showAxis('top', show=True)
        self.ui.a_kinetics_graph.getAxis('top').style['showValues'] = False
        self.ui.a_kinetics_graph.plotItem.showAxis('right', show=True)
        self.ui.a_kinetics_graph.getAxis('right').style['showValues'] = False
        
        self.ui.d_spectrum_graph.plotItem.setLabels(left='PL (counts)', bottom='Wavelength (nm)')
        self.ui.d_spectrum_graph.plotItem.showAxis('top', show=True)
        self.ui.d_spectrum_graph.getAxis('top').style['showValues'] = False
        self.ui.d_spectrum_graph.plotItem.showAxis('right', show=True)
        self.ui.d_spectrum_graph.getAxis('right').style['showValues'] = False
        return
    
    def d_spectrum_plot(self):
        self.ui.d_spectrum_graph.plotItem.plot(self.wavelengths, self.current_spectrum, pen='b', clear=True)
        return
      
    def a_colourmap_plot(self):
        self.ui.a_colourmap_graph.setImage(self.current_sweep.avg_data, scale=(len(self.wavelengths)/len(self.times), 1))
        return
   
    def a_kinetics_plot(self):
        if self.current_sweep.sweep_index > 0 and not self.final_plots:
            self.ui.a_kinetics_graph.plotItem.plot(self.times[0:self.timestep+1], self.current_sweep.current_data[0:self.timestep+1, self.kinetics_pixel], pen='c', symbol='s', symbolPen='c', symbolBrush=None, symbolSize=4, clear=True)
            self.ui.a_kinetics_graph.plotItem.plot(self.times, self.current_sweep.avg_data[:, self.kinetics_pixel], pen='b', symbol='s', symbolPen='b', symbolBrush=None, symbolSize=4, clear=False)
        elif self.current_sweep.sweep_index == 0 and not self.final_plots:
            self.ui.a_kinetics_graph.plotItem.plot(self.times[0:self.timestep+1], self.current_sweep.current_data[0:self.timestep+1, self.kinetics_pixel], pen='c', symbol='s', symbolPen='c', symbolBrush=None, symbolSize=4, clear=True)
        else:
            for item in self.ui.a_kinetics_graph.plotItem.listDataItems():
                self.ui.a_kinetics_graph.plotItem.removeItem(item)
            self.ui.a_kinetics_graph.plotItem.plot(self.times, self.current_sweep.avg_data[:, self.kinetics_pixel], pen='b', symbol='s', symbolPen='b', symbolBrush=None, symbolSize=4)
        return
   
    def a_spectrum_plot(self):
        for item in self.ui.a_spectrum_graph.plotItem.listDataItems():
            self.ui.a_spectrum_graph.plotItem.removeItem(item)
        if self.final_plots:
            self.ui.a_spectrum_graph.plotItem.plot(self.wavelengths, self.current_sweep.avg_data[self.time_pixel, :], pen='b')
        else:
            self.ui.a_spectrum_graph.plotItem.plot(self.wavelengths, self.current_spectrum, pen='b')
        return
    
    def add_time_marker(self):
        self.time_marker = pg.InfiniteLine(self.times[int(len(self.times)/2)], movable=True, bounds=[min(self.times), max(self.times)])
        self.ui.a_kinetics_graph.addItem(self.time_marker)
        self.time_marker.sigPositionChangeFinished.connect(self.update_time_pixel)
        self.time_marker_label = pg.InfLineLabel(self.time_marker, text='{value:.2f}ps', movable=True, position=0.9)
        self.update_time_pixel()
        return
        
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
    
    def message_unsafe_exit(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText('cannot close application')
        msg.setInformativeText('stop acquisition and disconnect from hardware')
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
        self.write_app_status('running', 'green')
        self.ui.hardware_tab.setEnabled(False)
        self.ui.a_acquisition_settings_box.setEnabled(False)
        self.ui.a_time_box.setEnabled(False)
        self.ui.a_metadata_box.setEnabled(False)
        self.ui.a_file_box.setEnabled(False)
        self.ui.a_run_btn.setEnabled(False)
        self.ui.d_acquisition_settings_box.setEnabled(False)
        self.ui.d_run_btn.setEnabled(False)
        self.ui.d_spectrograph_settings_box.setEnabled(False)
        if not self.diagnostics_on:
            self.ui.d_time_box.setEnabled(False)
        return
            
    def idling(self):
        self.idle = True
        self.write_app_status('idling', 'blue')
        self.ui.hardware_tab.setEnabled(True)
        self.ui.a_acquisition_settings_box.setEnabled(True)
        self.ui.a_time_box.setEnabled(True)
        self.ui.a_metadata_box.setEnabled(True)
        self.ui.a_file_box.setEnabled(True)
        self.ui.a_run_btn.setEnabled(True)
        self.ui.d_acquisition_settings_box.setEnabled(True)
        self.ui.d_run_btn.setEnabled(True)
        self.ui.d_spectrograph_settings_box.setEnabled(True)
        self.ui.d_time_box.setEnabled(True)
        return

    def acquire(self):
        self.acquisition.start_acquire.emit()
        return
   
    def post_acquire(self, spectrum):
        self.current_spectrum = spectrum#-self.bgd
        self.current_sweep.add_current_data(self.current_spectrum, self.timestep)
        # update plots
        if self.ui.acquisition_tab.isVisible() is True:
            self.a_colourmap_plot()
            self.a_spectrum_plot()
            self.a_kinetics_plot()
        if self.ui.diagnostics_tab.isVisible() is True:
            self.d_spectrum_plot()
        # stopping
        if self.stop_request is True:
            self.finish()
        elif self.timestep == len(self.times)-1:
            self.post_sweep()
        else:
            self.timestep = self.timestep+1
            self.time = self.times[self.timestep]
            self.ui.a_current_time_lcd.display(self.time)
            self.ui.a_sweep_progressbar.setValue(self.timestep+1)
            self.ui.a_measurement_progressbar.setValue(self.current_sweep.sweep_index*len(self.times)+self.timestep+1)
            self.move(self.time)
            self.acquire()
        return

    def acquire_bgd(self):
        self.acquisition.start_acquire.emit()
        return
        
    def post_acquire_bgd(self, spectrum):
        self.bgd = spectrum
        self.message_unblock()
        self.run()          
        return

    def exec_run_btn(self):
        self.stop_request = False
        self.diagnostics_on = False
        self.final_plots = False
        self.running()
        # deal with markers
        try:
            self.ui.a_spectrum_graph.removeItem(self.wavelength_marker)
        except:
            pass
        try:
            self.ui.a_kinetics_graph.removeItem(self.time_marker)
        except:
            pass
        self.add_wavelength_marker()
        # check that delay time is on stage!
        success = self.delaystage.check_times(self.times)
        if success is False:
            self.message_time_points()
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
        self.acquisition.data_ready.connect(self.post_acquire_bgd)
        # run
        self.message_block()
        self.write_log('recording background')
        self.acquire_bgd()
        return
    
    def add_wavelength_marker(self):
        self.wavelength_marker = pg.InfiniteLine(self.central_wavelength, movable=True, bounds=[self.wavelengths[0], self.wavelengths[-1]])
        self.ui.a_spectrum_graph.addItem(self.wavelength_marker)
        self.wavelength_marker.sigPositionChangeFinished.connect(self.update_kinetics_wavelength)
        self.wavelength_marker_label = pg.InfLineLabel(self.wavelength_marker, text='{value:.2f}nm', movable=True, position=0.9)
        self.update_kinetics_wavelength()
        return

    def run(self):
        self.update_metadata()
        self.current_sweep = SweepProcessing(self.times, self.camera.num_pixels, self.filepath, self.metadata)    
        # reset signals
        self.acquisition.data_ready.disconnect(self.post_acquire_bgd)
        self.acquisition.data_ready.connect(self.post_acquire)
        
        self.write_log('starting sweep {0}'.format(self.current_sweep.sweep_index))
        self.ui.a_current_sweep_lcd.display(self.current_sweep.sweep_index+1)
        self.ui.a_sweep_progressbar.setMaximum(len(self.times))
        self.ui.a_measurement_progressbar.setMaximum(len(self.times)*self.num_sweeps)
        self.start_sweep()
        return

    def finish(self):
        self.acquire_thread.quit()
        self.final_plots = True
        self.add_time_marker()
        self.a_kinetics_plot()
        self.a_spectrum_plot()
        self.idling()
        return
    
    def start_sweep(self):
        self.timestep = 0
        self.time = self.times[self.timestep]
        self.ui.a_current_time_lcd.display(self.time)
        self.ui.a_sweep_progressbar.setValue(self.timestep+1)
        self.ui.a_measurement_progressbar.setValue(self.current_sweep.sweep_index*len(self.times)+self.timestep+1)
        self.move(self.time)
        self.acquire()
        return
        
    def post_sweep(self):
        self.write_log('saving sweep {0}'.format(self.current_sweep.sweep_index))
        self.current_sweep.save_current_data(self.wavelengths)
        self.current_sweep.save_avg_data(self.wavelengths)
        self.current_sweep.next_sweep()
        if self.current_sweep.sweep_index == self.num_sweeps:
            self.finish()
        else:
            self.write_log('starting sweep {0}'.format(self.current_sweep.sweep_index))
            self.ui.a_current_sweep_lcd.display(self.current_sweep.sweep_index+1)
            self.start_sweep()
        return
   
    def exec_stop_btn(self):
        self.stop_request=True
        return
  
    def exec_exit_btn(self):
        if self.safe_to_exit:
            self.save_gui_values()
            self.close()
        else:
            self.message_unsafe_exit() 
        return
    
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
        return
        
    def d_post_single_acquisition(self, spectrum):
        self.current_spectrum = spectrum
        self.d_spectrum_plot()
        self.d_finish()
        return
        
    def exec_d_abort_btn(self):
        return
    
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
        return
        
    def d_run(self):
        self.d_move_to_time()
        self.d_acquire()
        return
    
    def d_acquire(self):
        self.acquisition.start_acquire.emit()
        return
        
    def d_post_acquire(self, spectrum):
        self.current_spectrum = spectrum
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
       
    def exec_d_exit_btn(self):
        if self.safe_to_exit:
            self.save_gui_values()
            self.close()
        else:
            self.message_unsafe_exit() 
        return

        
def main():
    
    # create application
    QtGui.QApplication.setStyle('breeze')
    app = QtGui.QApplication(sys.argv)
    
    # load the parameter values from last time and launch GUI
    last_instance_filename = 'last_instance_values.txt'
    last_instance_values = pd.read_csv(last_instance_filename, sep=':', header=None, index_col=0, squeeze=True)
    
    ex = Application(last_instance_filename, last_instance_values=last_instance_values, preloaded=True)

    ex.show()
    ex.create_plots()
    
    # kill application
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()
