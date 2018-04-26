
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QMessageBox,QAbstractItemView,QPushButton
from PyQt5.QtCore import Qt
from UI.BusInfoDialog import BusInfoDialog
from dao.businfoDAO import BusinfoDAO
from logic.GConst import gConst


class TabBusInfo(object):
    # 记录当前查询数据索引
    indexcount = 0
    # 页面大小
    pagesize = 15
    # 属性数
    columnsize = 9
    # 结果数
    resultcount = 0
    # 信息处理业务类
    biDao = None
    #获得点击index
    lastIndex = -1

    def initTabBusInfo(self):
        self.btn_tbnext.clicked.connect(self.btnnext)
        self.btn_tbpre.clicked.connect(self.btnpre)
        self.biDao = BusinfoDAO()
        # 直接登录数据库
        item_list = self.biDao.defaultQuery()
        self.settableitem(item_list)
        self.result_count = self.biDao.defaultresultcount()
        print(self.result_count)
        # todo 是否将result_count 移到dao
        for i in range(1, int((self.result_count + self.pagesize - 1) / self.pagesize) + 1):
            self.comboBox.insertItem(i, str(i))
        self.comboBox.currentIndexChanged.connect(self.comboxchange)
        self.btn_query.clicked.connect(self.btnQuery)
        self.tableWidget.setHorizontalHeaderLabels(self.biDao.getHeader())
        self.actionlink.triggered.connect(self.show_link_dialog)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.itemClicked.connect(self.addInFoButton)
        for i in range(0, len(gConst["businfo"]["powertpye"])):
            self.cbPowertype.insertItem(i, gConst["businfo"]["powertpye"][i])
        for i in range(0, len(gConst["businfo"]["teams"])):
            self.cb_team.insertItem(i, gConst["businfo"]["teams"][i])

    # 获取查询字段字典
    def getdict(self):
        textRoute = self.edit_route.text()
        textTeam = self.cb_team.currentText()
        textcarid = self.edit_carid.text()
        textpt=self.cbPowertype.currentText()
        print(textpt)
        dict = {}
        if textRoute != "":
            dict['route'] = textRoute
        if textTeam != "":
            dict['team'] = textTeam[0:1]
        if textcarid != "":
            dict['car_id'] = textcarid
        if textpt!="":
            dict['powertype']=textpt
        return dict

    # 获取模糊字段字典
    def getlikedict(self):
        # todo
        like = {'car_id': '1'}
        return like

    # 相应点击上一页按钮的事件
    def btnpre(self):
        if self.comboBox.currentIndex() > 0:
            self.comboBox.setCurrentIndex(self.comboBox.currentIndex() - 1)
        else:
            QMessageBox.information(self, "提示", "已到最前")

    # 响应点下一页按钮的事件
    def btnnext(self):
        print(self.comboBox.count())
        if self.comboBox.currentIndex() < self.comboBox.count() - 1:
            self.comboBox.setCurrentIndex(self.comboBox.currentIndex() + 1)
        else:
            QMessageBox.information(self, "提示", "已到最后")

    def settableitem(self, items):
        for i in range(0, self.pagesize):
            row_1 = items[i] if i < len(items) else None
            for j in range(0, self.columnsize):
                item = QTableWidgetItem()
                if row_1 is None:
                    item.setText("")
                elif str(row_1.get(self.biDao.keymap[j])) == "None":
                    item.setText("")
                else:
                    item.setText(str(row_1.get(self.biDao.keymap[j])))
                # 设置居中
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
        self.setTableNo()

    def setTableNo(self):
        no = []
        currentpage = self.comboBox.currentIndex()
        if currentpage < 0:
            currentpage = 0
        for i in range(1, self.pagesize + 1):
            no.append(str(currentpage * self.pagesize + i))
        self.tableWidget.setVerticalHeaderLabels(no)

    # 点击查询按钮事件
    def btnQuery(self):
        list = self.biDao.query(self.getdict(), self.getlikedict())
        self.settableitem(list)
        self.resetComboBox()
        self.clearInfoButton()

    # 重置Combox数据
    def resetComboBox(self):
        self.comboBox.setCurrentIndex(0)
        self.resultcount = self.biDao.getresultconut(self.getlikedict())
        print("-------------" + str(self.resultcount))
        count = self.comboBox.count()
        size = int((self.resultcount + self.pagesize - 1) / self.pagesize)
        if size == 0:
            size = 1
            QMessageBox.information(self, "提示", "未查询到记录")
        if count < size:
            for i in range(count + 1, size + 1):
                self.comboBox.insertItem(i, str(i))
        if count > size:
            for i in range(size, count):
                self.comboBox.removeItem(size)

    def comboxchange(self):
        print("combox change!!!!!")
        list = self.biDao.turntopage(self.comboBox.currentIndex())
        self.settableitem(list)
        self.clearInfoButton()

    # 显示车辆详细对话框
    def addInFoButton(self):
        self.clearInfoButton()
        selectindex = self.tableWidget.currentRow()
        item = self.tableWidget.item(selectindex, 0)
        if item is not None and item.text() != "":
            self.lastIndex = selectindex
            combox = QPushButton("详细")
            combox.clicked.connect(self.showBusInfoDialog)
            self.tableWidget.setCellWidget(self.lastIndex, 9, combox)

    def clearInfoButton(self):
        if self.lastIndex != -1:
            self.tableWidget.cellWidget(self.lastIndex, 9).clicked.disconnect(self.showBusInfoDialog)
            self.tableWidget.removeCellWidget(self.lastIndex, 9)
            self.lastIndex = -1

    def showBusInfoDialog(self):
        bid = BusInfoDialog(parent=self)
        car_id = self.tableWidget.item(self.lastIndex, 0).text()
        list = bid.loaddata(car_id)
        if bid.exec_():
            pass
