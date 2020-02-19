"""
write some stuff here about versions, contacts etc and code layout
"""

# general
import sys
import os
from PyQt5 import QtGui, QtWidgets

# gui object
from gui import Ui_hdf5gui as hdf5gui

# data manipulation
import numpy as np
import h5py

# hack to get the app to display an icon (Windows OS only?)
#import ctypes
#ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('hdf5App')
      
 
class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = hdf5gui()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.show()
        self.files_dict = {}
        self.set_gui_connections()
        self.ui.convert_button.setEnabled(False)
    
    def set_gui_connections(self):
        self.ui.file_up.clicked.connect(self.move_file_up)
        self.ui.file_down.clicked.connect(self.move_file_down)
        self.ui.delete_button.clicked.connect(self.delete_file)
        self.ui.load_button.clicked.connect(self.load_data)
        self.ui.folder_browser.clicked.connect(self.get_save_folder)
        self.ui.convert_button.clicked.connect(self.convert)
       
    def display_status(self, message, colour, msecs=0):
        self.ui.status_bar.clearMessage()
        self.ui.status_bar.setStyleSheet('QStatusBar{color:'+colour+';}')
        self.ui.status_bar.showMessage(message, msecs=msecs)
        
    def write_console(self, message):
        self.ui.console.appendPlainText(message)
    
    def load_data(self):
        ok = True
        for index in range(self.ui.file_list.count()):
            filepath = self.ui.file_list.item(index).text()
            try:
                f = h5py.File(filepath, 'r')
                self.files_dict[filepath] = f
                self.write_console('loaded file <{0}>'.format(os.path.basename(os.path.normpath(filepath))))
            except(Exception):
                self.display_status('unable to read file {0}'.format(filepath), 'red')
                ok = False
        if ok:
            self.display_status('succesfully read all files', 'green', msecs=5000)
            
    def check_files(self):
        pass
    
    def get_save_folder(self):
        fpath = os.path.dirname(os.path.normpath(list(self.files_dict.keys())[0]))
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose folder to save data', os.path.dirname(fpath))
        self.directory = os.path.normpath(directory)
        self.ui.save_folder.setText(directory)
        self.ui.convert_button.setEnabled(True)
            
    def delete_file(self):
        row = self.ui.file_list.currentRow()
        item = self.ui.file_list.takeItem(row)
        try:
            filepath = item.text()
            del self.files_dict[filepath]
        except KeyError:
            pass
        del(item)
        
    def move_file_up(self):
        currentRow = self.ui.file_list.currentRow()
        currentItem = self.ui.file_list.takeItem(currentRow)
        self.ui.file_list.insertItem(currentRow - 1, currentItem)
        self.ui.file_list.setCurrentItem(currentItem)
    
    def move_file_down(self):
        currentRow = self.ui.file_list.currentRow()
        currentItem = self.ui.file_list.takeItem(currentRow)
        self.ui.file_list.insertItem(currentRow + 1, currentItem)
        self.ui.file_list.setCurrentItem(currentItem)
        
    def convert(self):
        for key in self.files_dict.keys():
            self.convert_hdf5_file(key)
        self.display_status('finished converting', 'green')
        
    def mkdir(self, rootfolder, folder):
        directory = os.path.join(rootfolder, folder)
        if not os.path.isdir(directory):
            self.write_console('creating directory {0}'.format(directory))
            os.mkdir(directory)
        return directory
    
    @staticmethod
    def get_sweep(string):
        s = string.split('_')
        sweep = '{0}_{1}'.format(s[0], s[1])
        name = '{0}_{1}.csv'.format(s[2], s[3])
        return sweep, name
        
    def convert_hdf5_file(self, key):
        fname = str(os.path.basename(os.path.normpath(key)))
        self.write_console('starting file <{0}>'.format(fname))
        filebasename = fname[0:-5]
        savedir = self.mkdir(self.directory, filebasename)
        f = self.files_dict[key]
        # save average data
        if self.ui.average_check.isChecked():
            array = np.array(f['Average']).T
            fpath = os.path.join(savedir, 'averaged_trpl.csv')
            self.write_console('saving averaged data to {0}'.format(str(fpath)))
            np.savetxt(fpath, array, delimiter=',')
            fpath = os.path.join(savedir, 'datetimeinfo.txt')
            g = f.get('Average')
            with open(fpath, 'w') as fmd:
                fmd.write('start: '+str(g.attrs['start date'], 'utf-8')+' '+str(g.attrs['start time'], 'utf-8')+'\n')
                fmd.write('end: '+str(g.attrs['end_date'], 'utf-8')+' '+str(g.attrs['end_time'], 'utf-8')+'\n')
        # save metadata
        if self.ui.metadata_check.isChecked():
            array = np.array(f['Metadata'])  # might want the transpose ???
            g = f.get('Metadata')
            fpath = os.path.join(savedir, 'metadata.txt')
            with open(fpath, 'w') as fmd:
                for key in g.attrs:
                    fmd.write(str(key)+': '+str(g.attrs[key], 'utf-8')+'\n')  
            self.write_console('saving metadata to {0}'.format(str(fpath)))
        # save each sweep
        if self.ui.sweeps_check.isChecked():
            newsavedir = self.mkdir(savedir, 'sweeps')
            group = f['Sweeps']
            for sweep in group.keys():
                folder = self.mkdir(newsavedir, sweep)
                array = np.array(group[sweep]).T
                fpath = os.path.join(folder, 'trpl.csv')
                self.write_console('saving sweep data to {0}'.format(fpath))
                np.savetxt(fpath, array, delimiter=',')
                fpath = os.path.join(folder, 'datetimeinfo.txt')
                attr = group.get(sweep)
                with open(fpath, 'w') as fmd:
                    fmd.write(str(attr.attrs['date'], 'utf-8')+' '+str(attr.attrs['time'], 'utf-8')+'\n')
        f.close()
        self.write_console('finished file <{0}>'.format(fname))
        
        
        
        
 
if __name__ == "__main__":
    
    # create application
    QtWidgets.QApplication.setStyle('breeze')
    app = QtWidgets.QApplication(sys.argv)
    
    ex = Application()
    ex.show()
    
    sys.exit(app.exec_())
