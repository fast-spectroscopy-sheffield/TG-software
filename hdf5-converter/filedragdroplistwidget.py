from PyQt5 import QtWidgets, QtGui

           
class FileDragDropListWidget(QtWidgets.QListWidget):    
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

    def mimeTypes(self):
        mimetypes = super().mimeTypes()
        mimetypes.append('text/uri-list')
        return mimetypes

    def dropMimeData(self, index, data, action):
        if data.hasUrls():
            for url in data.urls():
                item = QtWidgets.QListWidgetItem(str(url.toLocalFile()))
                self.addItem(item)
                self.setCurrentItem(item)
            return True
        else:
            return False