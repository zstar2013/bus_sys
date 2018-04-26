# -*- coding:utf8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
import traceback

#QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))


class PixItem(QGraphicsItem):
    def __init__(self, QPixmap):
        super(PixItem, self).__init__()
        self.pix = QPixmap

    def boundingRect(self):
        return QRectF(-2 - self.pix.width() / 2, -2 - self.pix.height() / 2, self.pix.width() + 4,
                      self.pix.height() + 4)

    def paint(self, painter, option, widget):
        painter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.angle = 0
        self.scale = 5
        self.shear = 5
        self.translate = 50

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-200, -200, 400, 400)
        self.pixmap = QPixmap("F:\\媒体材料\\行驶证\\6577\\6577-x.jpg")
        self.item = PixItem(self.pixmap)

        self.scene.addItem(self.item)
        self.item.setPos(0, 0)

        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.setMinimumSize(400, 400)

        self.ctrlFrame = QFrame()
        self.createControllFrame()

        self.rightlayout = QVBoxLayout()
        self.rightlayout.addWidget(self.rotateGroup)
        self.rightlayout.addWidget(self.scaleGroup)
        self.rightlayout.addWidget(self.shearGroup)
        self.rightlayout.addWidget(self.translateGroup)

        self.leftlayout = QHBoxLayout()
        self.leftlayout.addWidget(self.view)
        self.leftlayout.addWidget(self.ctrlFrame)

        self.mainlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.leftlayout)
        self.mainlayout.addLayout(self.rightlayout)
        self.setLayout(self.mainlayout)

        self.setWindowTitle(self.tr("Graphics Item 的各种变形"))

    def createControllFrame(self):
        self.rotateGroup = QGroupBox(self.tr("旋转"))
        rotateSlider = QSlider()
        rotateSlider.setOrientation(Qt.Horizontal)
        rotateSlider.setRange(0, 360)
        rotateSlider.valueChanged.connect(lambda:self.slotRotate(rotateSlider.value()))
        #self.connect(rotateSlider, SIGNAL("valueChanged(int)"), self.slotRotate)
        rotateLayout = QHBoxLayout()
        rotateLayout.addWidget(rotateSlider)
        self.rotateGroup.setLayout(rotateLayout)

        self.scaleGroup = QGroupBox(self.tr("缩放"))
        scaleSlider = QSlider()
        scaleSlider.setOrientation(Qt.Horizontal)
        #self.connect(scaleSlider, SIGNAL("valueChanged(int)"), self.slotScale)
        scaleSlider.valueChanged.connect(lambda :self.soltScale(scaleSlider.value()))
        scaleLayout = QHBoxLayout()
        scaleLayout.addWidget(scaleSlider)
        self.scaleGroup.setLayout(scaleLayout)

        self.shearGroup = QGroupBox(self.tr("切变"))
        shearSlider = QSlider()
        shearSlider.setOrientation(Qt.Horizontal)
        shearSlider.valueChanged.connect(lambda :self.slotShear(shearSlider.value()))
        #self.connect(shearSlider, SIGNAL("valueChanged(int)"), self.slotShear)
        shearLayout = QHBoxLayout()
        shearLayout.addWidget(shearSlider)
        self.shearGroup.setLayout(shearLayout)

        self.translateGroup = QGroupBox(self.tr("位移"))
        translateSlider = QSlider()
        translateSlider.setOrientation(Qt.Horizontal)
        translateSlider.valueChanged.connect(lambda :self.slotTranslate(translateSlider.value()))
        #self.connect(translateSlider, SIGNAL("valueChanged(int)"), self.slotTranslate)
        translateLayout = QHBoxLayout()
        translateLayout.addWidget(translateSlider)
        self.translateGroup.setLayout(translateLayout)

    def slotRotate(self, value):

        try:
            print(value)
            self.item.rotate(value - self.angle)
            self.angle = value
        except:
            print(traceback.print_exc())

    def slotScale(self, value):
        if value > self.scale:
            s = math.pow(1.1, (value - self.scale))
        else:
            s = math.pow(1 / 1.1, (self.scale - value))
        self.item.scale(s, s)
        self.scale = value

    def slotShear(self, value):
        self.item.shear((value - self.shear) / 10.0, 0)
        self.shear = value

    def slotTranslate(self, value):
        self.item.translate(value - self.translate, value - self.translate)
        self.translate = value


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainwindow = MainWidget()
    mainwindow.show()
    sys.exit(app.exec_())