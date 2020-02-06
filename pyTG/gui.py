# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pyTGgui(object):
    def setupUi(self, pyTGgui):
        pyTGgui.setObjectName("pyTGgui")
        pyTGgui.resize(1139, 712)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pyTGgui.sizePolicy().hasHeightForWidth())
        pyTGgui.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(pyTGgui)
        self.centralWidget.setObjectName("centralWidget")
        self.tabs = QtWidgets.QTabWidget(self.centralWidget)
        self.tabs.setGeometry(QtCore.QRect(10, 10, 1121, 671))
        self.tabs.setObjectName("tabs")
        self.hardware_tab = QtWidgets.QWidget()
        self.hardware_tab.setObjectName("hardware_tab")
        self.h_iCCD_box = QtWidgets.QGroupBox(self.hardware_tab)
        self.h_iCCD_box.setGeometry(QtCore.QRect(10, 10, 411, 91))
        self.h_iCCD_box.setObjectName("h_iCCD_box")
        self.h_iCCD_connect_btn = QtWidgets.QPushButton(self.h_iCCD_box)
        self.h_iCCD_connect_btn.setGeometry(QtCore.QRect(10, 30, 91, 23))
        self.h_iCCD_connect_btn.setObjectName("h_iCCD_connect_btn")
        self.h_iCCD_disconnect_btn = QtWidgets.QPushButton(self.h_iCCD_box)
        self.h_iCCD_disconnect_btn.setGeometry(QtCore.QRect(110, 30, 91, 23))
        self.h_iCCD_disconnect_btn.setObjectName("h_iCCD_disconnect_btn")
        self.h_temperature_lcd = QtWidgets.QLCDNumber(self.h_iCCD_box)
        self.h_temperature_lcd.setGeometry(QtCore.QRect(330, 30, 71, 23))
        self.h_temperature_lcd.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.h_temperature_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.h_temperature_lcd.setObjectName("h_temperature_lcd")
        self.label_7 = QtWidgets.QLabel(self.h_iCCD_box)
        self.label_7.setGeometry(QtCore.QRect(210, 30, 111, 21))
        self.label_7.setObjectName("label_7")
        self.h_iCCD_status = QtWidgets.QLabel(self.h_iCCD_box)
        self.h_iCCD_status.setGeometry(QtCore.QRect(10, 60, 391, 21))
        self.h_iCCD_status.setFrameShape(QtWidgets.QFrame.Panel)
        self.h_iCCD_status.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.h_iCCD_status.setObjectName("h_iCCD_status")
        self.h_delaystage_box = QtWidgets.QGroupBox(self.hardware_tab)
        self.h_delaystage_box.setGeometry(QtCore.QRect(10, 110, 411, 91))
        self.h_delaystage_box.setObjectName("h_delaystage_box")
        self.h_delaystage_connect_btn = QtWidgets.QPushButton(self.h_delaystage_box)
        self.h_delaystage_connect_btn.setGeometry(QtCore.QRect(10, 30, 91, 23))
        self.h_delaystage_connect_btn.setObjectName("h_delaystage_connect_btn")
        self.h_delaystage_disconnect_btn = QtWidgets.QPushButton(self.h_delaystage_box)
        self.h_delaystage_disconnect_btn.setGeometry(QtCore.QRect(110, 30, 91, 23))
        self.h_delaystage_disconnect_btn.setObjectName("h_delaystage_disconnect_btn")
        self.h_delaystage_status = QtWidgets.QLabel(self.h_delaystage_box)
        self.h_delaystage_status.setGeometry(QtCore.QRect(10, 60, 391, 21))
        self.h_delaystage_status.setFrameShape(QtWidgets.QFrame.Panel)
        self.h_delaystage_status.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.h_delaystage_status.setObjectName("h_delaystage_status")
        self.tabs.addTab(self.hardware_tab, "")
        self.acquisition_tab = QtWidgets.QWidget()
        self.acquisition_tab.setObjectName("acquisition_tab")
        self.a_colourmap_graph = ImageView(self.acquisition_tab)
        self.a_colourmap_graph.setGeometry(QtCore.QRect(210, 10, 461, 351))
        self.a_colourmap_graph.setObjectName("a_colourmap_graph")
        self.a_spectrum_graph = PlotWidget(self.acquisition_tab)
        self.a_spectrum_graph.setGeometry(QtCore.QRect(210, 360, 461, 271))
        self.a_spectrum_graph.setObjectName("a_spectrum_graph")
        self.a_kinetics_graph = PlotWidget(self.acquisition_tab)
        self.a_kinetics_graph.setGeometry(QtCore.QRect(670, 10, 441, 351))
        self.a_kinetics_graph.setObjectName("a_kinetics_graph")
        self.a_acquisition_settings_box = QtWidgets.QGroupBox(self.acquisition_tab)
        self.a_acquisition_settings_box.setGeometry(QtCore.QRect(10, 10, 191, 141))
        self.a_acquisition_settings_box.setObjectName("a_acquisition_settings_box")
        self.a_exp_time_sb = QtWidgets.QDoubleSpinBox(self.a_acquisition_settings_box)
        self.a_exp_time_sb.setGeometry(QtCore.QRect(110, 30, 71, 22))
        self.a_exp_time_sb.setDecimals(4)
        self.a_exp_time_sb.setMinimum(0.05)
        self.a_exp_time_sb.setMaximum(10.0)
        self.a_exp_time_sb.setSingleStep(0.1)
        self.a_exp_time_sb.setObjectName("a_exp_time_sb")
        self.label_30 = QtWidgets.QLabel(self.a_acquisition_settings_box)
        self.label_30.setGeometry(QtCore.QRect(10, 30, 91, 21))
        self.label_30.setObjectName("label_30")
        self.label_47 = QtWidgets.QLabel(self.a_acquisition_settings_box)
        self.label_47.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.label_47.setObjectName("label_47")
        self.label_65 = QtWidgets.QLabel(self.a_acquisition_settings_box)
        self.label_65.setGeometry(QtCore.QRect(10, 70, 91, 21))
        self.label_65.setObjectName("label_65")
        self.a_gain_sb = QtWidgets.QSpinBox(self.a_acquisition_settings_box)
        self.a_gain_sb.setGeometry(QtCore.QRect(110, 70, 71, 22))
        self.a_gain_sb.setMaximum(4095)
        self.a_gain_sb.setSingleStep(100)
        self.a_gain_sb.setObjectName("a_gain_sb")
        self.a_num_accum_sb = QtWidgets.QSpinBox(self.a_acquisition_settings_box)
        self.a_num_accum_sb.setGeometry(QtCore.QRect(110, 50, 71, 22))
        self.a_num_accum_sb.setMinimum(1)
        self.a_num_accum_sb.setMaximum(100)
        self.a_num_accum_sb.setObjectName("a_num_accum_sb")
        self.a_gate_delay_sb = QtWidgets.QSpinBox(self.a_acquisition_settings_box)
        self.a_gate_delay_sb.setGeometry(QtCore.QRect(110, 90, 71, 22))
        self.a_gate_delay_sb.setMaximum(100000)
        self.a_gate_delay_sb.setProperty("value", 2840)
        self.a_gate_delay_sb.setObjectName("a_gate_delay_sb")
        self.label_66 = QtWidgets.QLabel(self.a_acquisition_settings_box)
        self.label_66.setGeometry(QtCore.QRect(10, 90, 91, 21))
        self.label_66.setObjectName("label_66")
        self.a_gate_width_sb = QtWidgets.QSpinBox(self.a_acquisition_settings_box)
        self.a_gate_width_sb.setGeometry(QtCore.QRect(110, 110, 71, 22))
        self.a_gate_width_sb.setMinimum(2)
        self.a_gate_width_sb.setMaximum(100000)
        self.a_gate_width_sb.setObjectName("a_gate_width_sb")
        self.label_67 = QtWidgets.QLabel(self.a_acquisition_settings_box)
        self.label_67.setGeometry(QtCore.QRect(10, 110, 91, 21))
        self.label_67.setObjectName("label_67")
        self.a_launch_box = QtWidgets.QGroupBox(self.acquisition_tab)
        self.a_launch_box.setGeometry(QtCore.QRect(10, 560, 191, 71))
        self.a_launch_box.setObjectName("a_launch_box")
        self.a_run_btn = QtWidgets.QPushButton(self.a_launch_box)
        self.a_run_btn.setGeometry(QtCore.QRect(10, 30, 51, 31))
        self.a_run_btn.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.a_run_btn.setObjectName("a_run_btn")
        self.a_exit_btn = QtWidgets.QPushButton(self.a_launch_box)
        self.a_exit_btn.setGeometry(QtCore.QRect(130, 30, 51, 31))
        self.a_exit_btn.setStyleSheet("")
        self.a_exit_btn.setObjectName("a_exit_btn")
        self.a_stop_btn = QtWidgets.QPushButton(self.a_launch_box)
        self.a_stop_btn.setGeometry(QtCore.QRect(70, 30, 51, 31))
        self.a_stop_btn.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.a_stop_btn.setObjectName("a_stop_btn")
        self.a_time_box = QtWidgets.QGroupBox(self.acquisition_tab)
        self.a_time_box.setGeometry(QtCore.QRect(10, 160, 191, 181))
        self.a_time_box.setObjectName("a_time_box")
        self.a_start_time_sb = QtWidgets.QDoubleSpinBox(self.a_time_box)
        self.a_start_time_sb.setGeometry(QtCore.QRect(110, 60, 71, 22))
        self.a_start_time_sb.setMinimum(-1000.0)
        self.a_start_time_sb.setMaximum(10000.0)
        self.a_start_time_sb.setSingleStep(0.1)
        self.a_start_time_sb.setProperty("value", -5.0)
        self.a_start_time_sb.setObjectName("a_start_time_sb")
        self.a_end_time_sb = QtWidgets.QDoubleSpinBox(self.a_time_box)
        self.a_end_time_sb.setGeometry(QtCore.QRect(110, 80, 71, 22))
        self.a_end_time_sb.setMinimum(0.0)
        self.a_end_time_sb.setMaximum(5000.0)
        self.a_end_time_sb.setSingleStep(10.0)
        self.a_end_time_sb.setProperty("value", 500.0)
        self.a_end_time_sb.setObjectName("a_end_time_sb")
        self.label_68 = QtWidgets.QLabel(self.a_time_box)
        self.label_68.setGeometry(QtCore.QRect(10, 30, 91, 21))
        self.label_68.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_68.setObjectName("label_68")
        self.a_distribution_cb = QtWidgets.QComboBox(self.a_time_box)
        self.a_distribution_cb.setGeometry(QtCore.QRect(110, 30, 71, 23))
        self.a_distribution_cb.setObjectName("a_distribution_cb")
        self.label_69 = QtWidgets.QLabel(self.a_time_box)
        self.label_69.setGeometry(QtCore.QRect(10, 60, 91, 21))
        self.label_69.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_69.setObjectName("label_69")
        self.label_70 = QtWidgets.QLabel(self.a_time_box)
        self.label_70.setGeometry(QtCore.QRect(10, 80, 91, 21))
        self.label_70.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_70.setObjectName("label_70")
        self.label_79 = QtWidgets.QLabel(self.a_time_box)
        self.label_79.setGeometry(QtCore.QRect(10, 100, 101, 21))
        self.label_79.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_79.setObjectName("label_79")
        self.label_80 = QtWidgets.QLabel(self.a_time_box)
        self.label_80.setGeometry(QtCore.QRect(10, 120, 101, 21))
        self.label_80.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_80.setObjectName("label_80")
        self.a_num_points_sb = QtWidgets.QSpinBox(self.a_time_box)
        self.a_num_points_sb.setGeometry(QtCore.QRect(110, 100, 71, 24))
        self.a_num_points_sb.setMinimum(2)
        self.a_num_points_sb.setMaximum(1000)
        self.a_num_points_sb.setSingleStep(10)
        self.a_num_points_sb.setProperty("value", 100)
        self.a_num_points_sb.setObjectName("a_num_points_sb")
        self.a_num_sweeps_sb = QtWidgets.QSpinBox(self.a_time_box)
        self.a_num_sweeps_sb.setGeometry(QtCore.QRect(110, 120, 71, 24))
        self.a_num_sweeps_sb.setMinimum(1)
        self.a_num_sweeps_sb.setMaximum(1000)
        self.a_num_sweeps_sb.setProperty("value", 3)
        self.a_num_sweeps_sb.setObjectName("a_num_sweeps_sb")
        self.a_ordering_cb = QtWidgets.QComboBox(self.a_time_box)
        self.a_ordering_cb.setGeometry(QtCore.QRect(110, 150, 71, 23))
        self.a_ordering_cb.setObjectName("a_ordering_cb")
        self.label_86 = QtWidgets.QLabel(self.a_time_box)
        self.label_86.setGeometry(QtCore.QRect(10, 150, 91, 21))
        self.label_86.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_86.setObjectName("label_86")
        self.a_metadata_box = QtWidgets.QGroupBox(self.acquisition_tab)
        self.a_metadata_box.setGeometry(QtCore.QRect(10, 350, 191, 101))
        self.a_metadata_box.setObjectName("a_metadata_box")
        self.label_87 = QtWidgets.QLabel(self.a_metadata_box)
        self.label_87.setGeometry(QtCore.QRect(10, 30, 111, 21))
        self.label_87.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_87.setObjectName("label_87")
        self.label_88 = QtWidgets.QLabel(self.a_metadata_box)
        self.label_88.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.label_88.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_88.setObjectName("label_88")
        self.label_89 = QtWidgets.QLabel(self.a_metadata_box)
        self.label_89.setGeometry(QtCore.QRect(10, 70, 91, 21))
        self.label_89.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_89.setObjectName("label_89")
        self.a_pump_wl_le = QtWidgets.QLineEdit(self.a_metadata_box)
        self.a_pump_wl_le.setGeometry(QtCore.QRect(110, 30, 71, 21))
        self.a_pump_wl_le.setObjectName("a_pump_wl_le")
        self.a_pump_power_le = QtWidgets.QLineEdit(self.a_metadata_box)
        self.a_pump_power_le.setGeometry(QtCore.QRect(110, 50, 71, 21))
        self.a_pump_power_le.setObjectName("a_pump_power_le")
        self.a_spot_size_le = QtWidgets.QLineEdit(self.a_metadata_box)
        self.a_spot_size_le.setGeometry(QtCore.QRect(110, 70, 71, 21))
        self.a_spot_size_le.setObjectName("a_spot_size_le")
        self.a_file_box = QtWidgets.QGroupBox(self.acquisition_tab)
        self.a_file_box.setGeometry(QtCore.QRect(10, 460, 191, 91))
        self.a_file_box.setObjectName("a_file_box")
        self.a_folder_browse_btn = QtWidgets.QPushButton(self.a_file_box)
        self.a_folder_browse_btn.setGeometry(QtCore.QRect(10, 30, 51, 23))
        self.a_folder_browse_btn.setObjectName("a_folder_browse_btn")
        self.a_filename_le = QtWidgets.QLineEdit(self.a_file_box)
        self.a_filename_le.setGeometry(QtCore.QRect(70, 30, 111, 23))
        self.a_filename_le.setObjectName("a_filename_le")
        self.a_filepath_le = QtWidgets.QLineEdit(self.a_file_box)
        self.a_filepath_le.setGeometry(QtCore.QRect(12, 60, 171, 23))
        self.a_filepath_le.setObjectName("a_filepath_le")
        self.a_measurement_box = QtWidgets.QGroupBox(self.acquisition_tab)
        self.a_measurement_box.setGeometry(QtCore.QRect(710, 390, 371, 211))
        self.a_measurement_box.setObjectName("a_measurement_box")
        self.label_6 = QtWidgets.QLabel(self.a_measurement_box)
        self.label_6.setGeometry(QtCore.QRect(10, 180, 151, 21))
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.a_measurement_box)
        self.label_5.setGeometry(QtCore.QRect(10, 150, 151, 21))
        self.label_5.setObjectName("label_5")
        self.a_measurement_progressbar = QtWidgets.QProgressBar(self.a_measurement_box)
        self.a_measurement_progressbar.setGeometry(QtCore.QRect(170, 180, 191, 23))
        self.a_measurement_progressbar.setProperty("value", 0)
        self.a_measurement_progressbar.setObjectName("a_measurement_progressbar")
        self.a_sweep_progressbar = QtWidgets.QProgressBar(self.a_measurement_box)
        self.a_sweep_progressbar.setGeometry(QtCore.QRect(170, 150, 191, 23))
        self.a_sweep_progressbar.setProperty("value", 0)
        self.a_sweep_progressbar.setObjectName("a_sweep_progressbar")
        self.label_4 = QtWidgets.QLabel(self.a_measurement_box)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 141, 21))
        self.label_4.setObjectName("label_4")
        self.a_current_sweep_lcd = QtWidgets.QLCDNumber(self.a_measurement_box)
        self.a_current_sweep_lcd.setGeometry(QtCore.QRect(170, 120, 71, 23))
        self.a_current_sweep_lcd.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.a_current_sweep_lcd.setObjectName("a_current_sweep_lcd")
        self.label_3 = QtWidgets.QLabel(self.a_measurement_box)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 141, 21))
        self.label_3.setObjectName("label_3")
        self.a_current_time_lcd = QtWidgets.QLCDNumber(self.a_measurement_box)
        self.a_current_time_lcd.setGeometry(QtCore.QRect(170, 90, 71, 23))
        self.a_current_time_lcd.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.a_current_time_lcd.setObjectName("a_current_time_lcd")
        self.label = QtWidgets.QLabel(self.a_measurement_box)
        self.label.setGeometry(QtCore.QRect(10, 30, 141, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.a_measurement_box)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 141, 21))
        self.label_2.setObjectName("label_2")
        self.a_temperature_lcd = QtWidgets.QLCDNumber(self.a_measurement_box)
        self.a_temperature_lcd.setGeometry(QtCore.QRect(170, 60, 71, 23))
        self.a_temperature_lcd.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.a_temperature_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.a_temperature_lcd.setObjectName("a_temperature_lcd")
        self.a_kinetic_wavelength_sb = QtWidgets.QDoubleSpinBox(self.a_measurement_box)
        self.a_kinetic_wavelength_sb.setGeometry(QtCore.QRect(170, 30, 71, 24))
        self.a_kinetic_wavelength_sb.setMaximum(1200.0)
        self.a_kinetic_wavelength_sb.setProperty("value", 600.0)
        self.a_kinetic_wavelength_sb.setObjectName("a_kinetic_wavelength_sb")
        self.tabs.addTab(self.acquisition_tab, "")
        self.diagnostics_tab = QtWidgets.QWidget()
        self.diagnostics_tab.setObjectName("diagnostics_tab")
        self.d_acquisition_settings_box = QtWidgets.QGroupBox(self.diagnostics_tab)
        self.d_acquisition_settings_box.setGeometry(QtCore.QRect(10, 10, 191, 181))
        self.d_acquisition_settings_box.setObjectName("d_acquisition_settings_box")
        self.d_exp_time_sb = QtWidgets.QDoubleSpinBox(self.d_acquisition_settings_box)
        self.d_exp_time_sb.setGeometry(QtCore.QRect(111, 30, 71, 22))
        self.d_exp_time_sb.setDecimals(4)
        self.d_exp_time_sb.setMinimum(0.05)
        self.d_exp_time_sb.setMaximum(10.0)
        self.d_exp_time_sb.setSingleStep(0.1)
        self.d_exp_time_sb.setObjectName("d_exp_time_sb")
        self.label_24 = QtWidgets.QLabel(self.d_acquisition_settings_box)
        self.label_24.setGeometry(QtCore.QRect(10, 30, 91, 21))
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.d_acquisition_settings_box)
        self.label_25.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.d_acquisition_settings_box)
        self.label_26.setGeometry(QtCore.QRect(10, 70, 91, 21))
        self.label_26.setObjectName("label_26")
        self.d_gain_sb = QtWidgets.QSpinBox(self.d_acquisition_settings_box)
        self.d_gain_sb.setGeometry(QtCore.QRect(110, 70, 71, 22))
        self.d_gain_sb.setMaximum(4095)
        self.d_gain_sb.setSingleStep(100)
        self.d_gain_sb.setObjectName("d_gain_sb")
        self.d_num_accum_sb = QtWidgets.QSpinBox(self.d_acquisition_settings_box)
        self.d_num_accum_sb.setGeometry(QtCore.QRect(110, 50, 71, 22))
        self.d_num_accum_sb.setMinimum(1)
        self.d_num_accum_sb.setMaximum(100)
        self.d_num_accum_sb.setObjectName("d_num_accum_sb")
        self.d_gate_delay_sb = QtWidgets.QSpinBox(self.d_acquisition_settings_box)
        self.d_gate_delay_sb.setGeometry(QtCore.QRect(110, 90, 71, 22))
        self.d_gate_delay_sb.setMaximum(100000)
        self.d_gate_delay_sb.setProperty("value", 2840)
        self.d_gate_delay_sb.setObjectName("d_gate_delay_sb")
        self.label_27 = QtWidgets.QLabel(self.d_acquisition_settings_box)
        self.label_27.setGeometry(QtCore.QRect(10, 90, 91, 21))
        self.label_27.setObjectName("label_27")
        self.d_gate_width_sb = QtWidgets.QSpinBox(self.d_acquisition_settings_box)
        self.d_gate_width_sb.setGeometry(QtCore.QRect(110, 110, 71, 22))
        self.d_gate_width_sb.setMinimum(2)
        self.d_gate_width_sb.setMaximum(100000)
        self.d_gate_width_sb.setObjectName("d_gate_width_sb")
        self.label_28 = QtWidgets.QLabel(self.d_acquisition_settings_box)
        self.label_28.setGeometry(QtCore.QRect(10, 110, 91, 21))
        self.label_28.setObjectName("label_28")
        self.d_acquire_btn = QtWidgets.QPushButton(self.d_acquisition_settings_box)
        self.d_acquire_btn.setGeometry(QtCore.QRect(10, 140, 171, 31))
        self.d_acquire_btn.setStyleSheet("")
        self.d_acquire_btn.setObjectName("d_acquire_btn")
        self.d_launch_box = QtWidgets.QGroupBox(self.diagnostics_tab)
        self.d_launch_box.setGeometry(QtCore.QRect(10, 560, 191, 71))
        self.d_launch_box.setObjectName("d_launch_box")
        self.d_run_btn = QtWidgets.QPushButton(self.d_launch_box)
        self.d_run_btn.setGeometry(QtCore.QRect(10, 30, 51, 31))
        self.d_run_btn.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.d_run_btn.setObjectName("d_run_btn")
        self.d_exit_btn = QtWidgets.QPushButton(self.d_launch_box)
        self.d_exit_btn.setGeometry(QtCore.QRect(130, 30, 51, 31))
        self.d_exit_btn.setStyleSheet("")
        self.d_exit_btn.setObjectName("d_exit_btn")
        self.d_stop_btn = QtWidgets.QPushButton(self.d_launch_box)
        self.d_stop_btn.setGeometry(QtCore.QRect(70, 30, 51, 31))
        self.d_stop_btn.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.d_stop_btn.setObjectName("d_stop_btn")
        self.d_spectrum_graph = PlotWidget(self.diagnostics_tab)
        self.d_spectrum_graph.setGeometry(QtCore.QRect(210, 80, 901, 471))
        self.d_spectrum_graph.setObjectName("d_spectrum_graph")
        self.d_time_box = QtWidgets.QGroupBox(self.diagnostics_tab)
        self.d_time_box.setGeometry(QtCore.QRect(10, 200, 191, 151))
        self.d_time_box.setObjectName("d_time_box")
        self.d_time_back_btn = QtWidgets.QPushButton(self.d_time_box)
        self.d_time_back_btn.setGeometry(QtCore.QRect(10, 60, 41, 23))
        self.d_time_back_btn.setObjectName("d_time_back_btn")
        self.d_time_forward_btn = QtWidgets.QPushButton(self.d_time_box)
        self.d_time_forward_btn.setGeometry(QtCore.QRect(60, 60, 41, 23))
        self.d_time_forward_btn.setObjectName("d_time_forward_btn")
        self.d_time_step_sb = QtWidgets.QDoubleSpinBox(self.d_time_box)
        self.d_time_step_sb.setGeometry(QtCore.QRect(110, 60, 71, 22))
        self.d_time_step_sb.setMaximum(10.0)
        self.d_time_step_sb.setSingleStep(0.1)
        self.d_time_step_sb.setObjectName("d_time_step_sb")
        self.d_current_time_sb = QtWidgets.QDoubleSpinBox(self.d_time_box)
        self.d_current_time_sb.setGeometry(QtCore.QRect(110, 90, 71, 22))
        self.d_current_time_sb.setMinimum(-500.0)
        self.d_current_time_sb.setMaximum(500.0)
        self.d_current_time_sb.setSingleStep(0.1)
        self.d_current_time_sb.setObjectName("d_current_time_sb")
        self.d_move_to_time_btn = QtWidgets.QPushButton(self.d_time_box)
        self.d_move_to_time_btn.setGeometry(QtCore.QRect(10, 90, 91, 23))
        self.d_move_to_time_btn.setObjectName("d_move_to_time_btn")
        self.d_set_current_time_btn = QtWidgets.QPushButton(self.d_time_box)
        self.d_set_current_time_btn.setGeometry(QtCore.QRect(10, 120, 171, 23))
        self.d_set_current_time_btn.setObjectName("d_set_current_time_btn")
        self.d_time_zero_sb = QtWidgets.QDoubleSpinBox(self.d_time_box)
        self.d_time_zero_sb.setGeometry(QtCore.QRect(110, 30, 71, 22))
        self.d_time_zero_sb.setMinimum(-500.0)
        self.d_time_zero_sb.setMaximum(500.0)
        self.d_time_zero_sb.setSingleStep(0.1)
        self.d_time_zero_sb.setObjectName("d_time_zero_sb")
        self.label_23 = QtWidgets.QLabel(self.d_time_box)
        self.label_23.setGeometry(QtCore.QRect(10, 30, 91, 21))
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.d_display_settings_box = QtWidgets.QGroupBox(self.diagnostics_tab)
        self.d_display_settings_box.setGeometry(QtCore.QRect(210, 10, 901, 61))
        self.d_display_settings_box.setObjectName("d_display_settings_box")
        self.d_autoscale_checkbox = QtWidgets.QCheckBox(self.d_display_settings_box)
        self.d_autoscale_checkbox.setGeometry(QtCore.QRect(10, 30, 85, 21))
        self.d_autoscale_checkbox.setObjectName("d_autoscale_checkbox")
        self.d_rescale_button = QtWidgets.QPushButton(self.d_display_settings_box)
        self.d_rescale_button.setGeometry(QtCore.QRect(100, 30, 80, 23))
        self.d_rescale_button.setObjectName("d_rescale_button")
        self.d_spectrograph_settings_box = QtWidgets.QGroupBox(self.diagnostics_tab)
        self.d_spectrograph_settings_box.setGeometry(QtCore.QRect(210, 560, 901, 71))
        self.d_spectrograph_settings_box.setStyleSheet("")
        self.d_spectrograph_settings_box.setObjectName("d_spectrograph_settings_box")
        self.d_central_wavelength_sb = QtWidgets.QDoubleSpinBox(self.d_spectrograph_settings_box)
        self.d_central_wavelength_sb.setGeometry(QtCore.QRect(140, 30, 71, 24))
        self.d_central_wavelength_sb.setMaximum(1000.0)
        self.d_central_wavelength_sb.setProperty("value", 600.0)
        self.d_central_wavelength_sb.setObjectName("d_central_wavelength_sb")
        self.label_29 = QtWidgets.QLabel(self.d_spectrograph_settings_box)
        self.label_29.setGeometry(QtCore.QRect(10, 30, 121, 21))
        self.label_29.setObjectName("label_29")
        self.d_slitwidth_sb = QtWidgets.QSpinBox(self.d_spectrograph_settings_box)
        self.d_slitwidth_sb.setGeometry(QtCore.QRect(320, 30, 71, 24))
        self.d_slitwidth_sb.setMinimum(50)
        self.d_slitwidth_sb.setMaximum(2500)
        self.d_slitwidth_sb.setSingleStep(10)
        self.d_slitwidth_sb.setObjectName("d_slitwidth_sb")
        self.label_31 = QtWidgets.QLabel(self.d_spectrograph_settings_box)
        self.label_31.setGeometry(QtCore.QRect(250, 30, 61, 21))
        self.label_31.setObjectName("label_31")
        self.d_temperature_lcd = QtWidgets.QLCDNumber(self.d_spectrograph_settings_box)
        self.d_temperature_lcd.setGeometry(QtCore.QRect(820, 30, 71, 23))
        self.d_temperature_lcd.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.d_temperature_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.d_temperature_lcd.setObjectName("d_temperature_lcd")
        self.label_32 = QtWidgets.QLabel(self.d_spectrograph_settings_box)
        self.label_32.setGeometry(QtCore.QRect(690, 30, 121, 20))
        self.label_32.setObjectName("label_32")
        self.tabs.addTab(self.diagnostics_tab, "")
        self.log_tab = QtWidgets.QWidget()
        self.log_tab.setObjectName("log_tab")
        self.log_window = QtWidgets.QPlainTextEdit(self.log_tab)
        self.log_window.setGeometry(QtCore.QRect(10, 10, 1101, 621))
        self.log_window.setObjectName("log_window")
        self.tabs.addTab(self.log_tab, "")
        pyTGgui.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(pyTGgui)
        self.statusBar.setObjectName("statusBar")
        pyTGgui.setStatusBar(self.statusBar)

        self.retranslateUi(pyTGgui)
        self.tabs.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(pyTGgui)

    def retranslateUi(self, pyTGgui):
        _translate = QtCore.QCoreApplication.translate
        pyTGgui.setWindowTitle(_translate("pyTGgui", "pyTG"))
        self.h_iCCD_box.setTitle(_translate("pyTGgui", "iCCD and Spectrograph"))
        self.h_iCCD_connect_btn.setText(_translate("pyTGgui", "Connect"))
        self.h_iCCD_disconnect_btn.setText(_translate("pyTGgui", "Disconnect"))
        self.label_7.setText(_translate("pyTGgui", "iCCD Temperature"))
        self.h_iCCD_status.setText(_translate("pyTGgui", "status"))
        self.h_delaystage_box.setTitle(_translate("pyTGgui", "Delay Stage"))
        self.h_delaystage_connect_btn.setText(_translate("pyTGgui", "Connect"))
        self.h_delaystage_disconnect_btn.setText(_translate("pyTGgui", "Disconnect"))
        self.h_delaystage_status.setText(_translate("pyTGgui", "status"))
        self.tabs.setTabText(self.tabs.indexOf(self.hardware_tab), _translate("pyTGgui", "Hardware"))
        self.a_acquisition_settings_box.setTitle(_translate("pyTGgui", "Acquisition Settings"))
        self.label_30.setText(_translate("pyTGgui", "Exposure Time"))
        self.label_47.setText(_translate("pyTGgui", "Accumulations"))
        self.label_65.setText(_translate("pyTGgui", "Gain"))
        self.label_66.setText(_translate("pyTGgui", "Gate Delay"))
        self.label_67.setText(_translate("pyTGgui", "Gate Width"))
        self.a_launch_box.setTitle(_translate("pyTGgui", "Launch"))
        self.a_run_btn.setText(_translate("pyTGgui", "Run"))
        self.a_exit_btn.setText(_translate("pyTGgui", "Exit"))
        self.a_stop_btn.setText(_translate("pyTGgui", "Stop"))
        self.a_time_box.setTitle(_translate("pyTGgui", "Time"))
        self.label_68.setText(_translate("pyTGgui", "Distribution"))
        self.label_69.setText(_translate("pyTGgui", "Start Time"))
        self.label_70.setText(_translate("pyTGgui", "End Time"))
        self.label_79.setText(_translate("pyTGgui", "Num. Points"))
        self.label_80.setText(_translate("pyTGgui", "Num. Sweeps"))
        self.label_86.setText(_translate("pyTGgui", "Ordering"))
        self.a_metadata_box.setTitle(_translate("pyTGgui", "Metadata"))
        self.label_87.setText(_translate("pyTGgui", "Pump WL"))
        self.label_88.setText(_translate("pyTGgui", "Power Power"))
        self.label_89.setText(_translate("pyTGgui", "Spot Size"))
        self.a_file_box.setTitle(_translate("pyTGgui", "File"))
        self.a_folder_browse_btn.setText(_translate("pyTGgui", "Folder"))
        self.a_filename_le.setText(_translate("pyTGgui", "filename"))
        self.a_measurement_box.setTitle(_translate("pyTGgui", "Measurement"))
        self.label_6.setText(_translate("pyTGgui", "Measurement Progress"))
        self.label_5.setText(_translate("pyTGgui", "Current Sweep Progress"))
        self.label_4.setText(_translate("pyTGgui", "Current Sweep"))
        self.label_3.setText(_translate("pyTGgui", "Current Time"))
        self.label.setText(_translate("pyTGgui", "Wavelength Monitored"))
        self.label_2.setText(_translate("pyTGgui", "iCCD Temperature"))
        self.tabs.setTabText(self.tabs.indexOf(self.acquisition_tab), _translate("pyTGgui", "Acquisition"))
        self.d_acquisition_settings_box.setTitle(_translate("pyTGgui", "Acquisition Settings"))
        self.label_24.setText(_translate("pyTGgui", "Exposure Time"))
        self.label_25.setText(_translate("pyTGgui", "Accumulations"))
        self.label_26.setText(_translate("pyTGgui", "Gain"))
        self.label_27.setText(_translate("pyTGgui", "Gate Delay"))
        self.label_28.setText(_translate("pyTGgui", "Gate Width"))
        self.d_acquire_btn.setText(_translate("pyTGgui", "Single Acquisition"))
        self.d_launch_box.setTitle(_translate("pyTGgui", "Launch"))
        self.d_run_btn.setText(_translate("pyTGgui", "Run"))
        self.d_exit_btn.setText(_translate("pyTGgui", "Exit"))
        self.d_stop_btn.setText(_translate("pyTGgui", "Stop"))
        self.d_time_box.setTitle(_translate("pyTGgui", "Time"))
        self.d_time_back_btn.setText(_translate("pyTGgui", "<"))
        self.d_time_forward_btn.setText(_translate("pyTGgui", ">"))
        self.d_move_to_time_btn.setText(_translate("pyTGgui", "Move to Time"))
        self.d_set_current_time_btn.setText(_translate("pyTGgui", "Set Current as Time Zero"))
        self.label_23.setText(_translate("pyTGgui", "Time Zero"))
        self.d_display_settings_box.setTitle(_translate("pyTGgui", "Display Settings"))
        self.d_autoscale_checkbox.setText(_translate("pyTGgui", "Autoscale"))
        self.d_rescale_button.setText(_translate("pyTGgui", "Rescale"))
        self.d_spectrograph_settings_box.setTitle(_translate("pyTGgui", "Spectrograph Settings"))
        self.label_29.setText(_translate("pyTGgui", "Central Wavelength"))
        self.label_31.setText(_translate("pyTGgui", "Slit Width"))
        self.label_32.setText(_translate("pyTGgui", "iCCD Temperature"))
        self.tabs.setTabText(self.tabs.indexOf(self.diagnostics_tab), _translate("pyTGgui", "Diagnostics"))
        self.tabs.setTabText(self.tabs.indexOf(self.log_tab), _translate("pyTGgui", "Log"))

from pyqtgraph import ImageView, PlotWidget
