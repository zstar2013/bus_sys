from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QColorDialog, QPushButton, QGridLayout, QFrame,QGraphicsScene,QGraphicsPixmapItem
from PyQt5.QtGui import QPalette,QPixmap
from qt_ui_file.ImageDialog import Ui_Dialog
from logic.GConst import gConst
from tools.filetool import searchForFile
import sys
import os


class ImageDialog(QDialog, Ui_Dialog):
    scene=None
    item=None
    currentIndex=0
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.pbPrepage.clicked.connect(self.pageUp)
        self.pbNextpage.clicked.connect(self.pageDown)
        self.pbClose.clicked.connect(self.close)

    def setFilePath(self,filepath):
        self.item = searchForFile(filepath, ".jpg")
        self.loadfiles(self.item[self.currentIndex])

    def pageUp(self):
        if self.currentIndex>0:
            self.currentIndex-=1
            self.loadfiles(self.item[self.currentIndex])

    def pageDown(self):
        if self.currentIndex<len(self.item)-1:
            self.currentIndex+=1
            self.loadfiles(self.item[self.currentIndex])


    def loadfiles(self, filePath):
        if os.path.exists(filePath):
            pixmap =QPixmap()
            pixmap.load(filePath)
            oldHeight=pixmap.height()
            oldWidth=pixmap.width()
            self.scene = QGraphicsScene(self)
            height = int(gConst["imagedialog"]["defaultHeight"])
            width = int(gConst["imagedialog"]["defaultWidth"])
            dh = height/oldHeight
            dw = width /oldWidth
            item = QGraphicsPixmapItem(pixmap)
            if dh>dw:
                item.setScale(dw)
            else:
                item.setScale(dh)
            self.scene.addItem(item)
            self.graphicsView.setScene(self.scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageDialog()
    ex.show()
    sys.exit(app.exec_())