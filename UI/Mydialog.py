from PyQt5 import QtWidgets
from UI.linkDialog import LinkDialog
from UI.tabBusInfo import TabBusInfo
from UI.tabMileage import TABMileage
from qt_ui_file.mainwindow import Ui_MainWindow
import UI.modelOil

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow, TabBusInfo, TABMileage):

    # 类初始化
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.initTabBusInfo()
        UI.modelOil.initTabOil(self)




    #显示连接配置对话框
    def show_link_dialog(self):
        ld = LinkDialog(parent=self)
        if ld.exec_():
            pass

    def close(self):
        sys.exit()



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dlg = MyWindow()
    dlg.show()

    sys.exit(app.exec_())
