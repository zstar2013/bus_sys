from PyQt5.QtWidgets import QDialog
from qt_ui_file.connseting import Ui_Dialog
from logic.PyDbHelper import PyDbHelper
import tools.retool as rt


class LinkDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.pbtestlink.clicked.connect(self.db_connect)
        self.pbsavelink.clicked.connect(self.db_save)
        self.pbcancel.clicked.connect(self.cancel)

    def cancel(self):
        self.destroy()

    def get_current_value(self):
        list = {}
        list["db_ip"] = self.ledb.text()
        list["username"] = self.leusr.text()
        list["password"] = self.lepwd.text()
        list["dbname"] = self.ledbname.text()
        return list

    def db_connect(self):
        if self.ledb.text() is "":
            self.lbstatus.setText("数据库信息未填写!!")
        elif rt.matchipv4(self.ledb.text()) is None:
            self.lbstatus.setText("数据库ip填写错误!!")
        elif self.leusr.text() is "":
            self.lbstatus.setText("用户名信息未填写!!")
        else:
            self.lbstatus.setText("开始连接数据库....")
            pyd = PyDbHelper.GetInstance()
            list = self.get_current_value()
            print(list)
            result=pyd.testConnect(host=list["db_ip"], user=list["username"], passwd=list["password"], db=list["dbname"])
            if result=="ok":
                self.lbstatus.setText("数据库连接成功！")
            else:
                self.lbstatus.setText("无法连接指定数据库！\n"+str(result))

    def db_save(self):
        list=self.get_current_value()
        pyd=PyDbHelper.GetInstance()
        pyd.set_config(host=list["db_ip"], user=list["username"], passwd=list["password"], db=list["dbname"])
        self.lbstatus.setText("数据保存成功！")
        #todo 将数据保存至本地文件
