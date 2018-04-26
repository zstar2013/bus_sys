from PyQt5.QtWidgets import QDialog,QMessageBox,QFileDialog
from PyQt5.QtCore import QLocale
from qt_ui_file.FormDialog import Ui_Dialog
from dao.businfoDAO import BusinfoDAO
from UI.imageDialog import ImageDialog
import os
import traceback


class BusInfoDialog(QDialog, Ui_Dialog):
    #o为详情模式，1为编辑模式
    currrntMode=1
    mDAO=None

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.mDAO=BusinfoDAO()
        self.setupUi(self)
        self.retranslateUi(self)
        self.pbClose.clicked.connect(self.close)
        self.pbEdit.clicked.connect(self.editButtonClick)


    def loaddata(self,car_id):
        item=self.mDAO.queryByCarId(car_id=car_id)[0]
        self.lineEdit_car_id.setText(str(item["car_id"]))
        self.lineEdit_route.setText(str(item["route"]))
        self.lineEdit_carlength.setText(str(item["length"]))
        self.lineEdit_busload.setText(str(item["busload"]))
        self.lineEdit_updatetime.setText(str(item["uptime"]))
        self.lineEdit_cartype.setText(str(item["cartype"]))
        self.lineEdit_team.setText(str(item["team"]))
        self.textEdit_des.setText(str(item["descript"]))
        self.le_scrap.setText(str(item["scrap"]))
        self.pbshowImage.clicked.connect(lambda: self.openFile(self.lineEdit_car_id.text()))
        self.setItemUneditable()

    def openFile(self,filePath):
        try:

            filePath="F:\\媒体材料\\行驶证\\"+filePath[3:7]
            if os.path.exists(filePath):
                Id = ImageDialog(parent=self)
                Id.setFilePath(filePath)
                if Id.exec_():
                    pass
            else:
                QMessageBox.information(self,"提示","路径错误！")
        except:
            print(traceback.print_exc())

    def editButtonClick(self):
        #如果当前处于可编辑状态
        if self.currrntMode==1:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "提示",
                                            "是否保存？",
                                            QMessageBox.Yes | QMessageBox.No)
            if reply==QMessageBox.Yes:
                try:
                    self.saveBudInfo()
                    self.setItemUneditable()
                except:
                    print(traceback.print_exc())

        else:
            self.setItemEditable()



    #保存数据
    def saveBudInfo(self):
        item={}
        item["car_id"]=self.lineEdit_car_id.text()
        item["route"]=self.lineEdit_route.text()
        item["length"]=self.lineEdit_carlength.text()
        item["busload"]=self.lineEdit_busload.text()
        item["uptime"]=self.lineEdit_updatetime.text()
        item["cartype"]=self.lineEdit_cartype.text()
        item["team"]=self.lineEdit_team.text()
        item["descript"]=self.textEdit_des.toPlainText()
        item["scrap"]=self.le_scrap.text()
        print(str(self.mDAO.update(item)))
        self.parent().btnQuery()

    def setItemUneditable(self):
        if self.currrntMode==1:
            self.currrntMode=0
            self.lineEdit_car_id.setEnabled(False)
            self.lineEdit_route.setEnabled(False)
            self.lineEdit_carlength.setEnabled(False)
            self.lineEdit_busload.setEnabled(False)
            self.lineEdit_updatetime.setEnabled(False)
            self.lineEdit_cartype.setEnabled(False)
            self.lineEdit_team.setEnabled(False)
            self.textEdit_des.setEnabled(False)
            self.le_scrap.setEnabled(False)
        self.pbEdit.setText("编辑")

    def setItemEditable(self):
        if self.currrntMode==0:
            self.currrntMode=1
            self.lineEdit_car_id.setEnabled(True)
            self.lineEdit_route.setEnabled(True)
            self.lineEdit_carlength.setEnabled(True)
            self.lineEdit_busload.setEnabled(True)
            self.lineEdit_updatetime.setEnabled(True)
            self.lineEdit_cartype.setEnabled(True)
            self.lineEdit_team.setEnabled(True)
            self.textEdit_des.setEnabled(True)
            self.le_scrap.setEnabled(True)
        self.pbEdit.setText("保存")







