from logic.GConst import gConst
from tools.strtool import contains
from xlutils.copy import copy
import os
import tools.conftool as ct
import xlrd
import tools.xlstool as xt
import tools.filetool as ft
from UI.Mydialog import MyWindow
from PyQt5.QtWidgets import QMessageBox,QProgressDialog
from tools.conftool import updateItem ,loadOption
from tools.dialogTools import showPathDialog,showFilePathDialog,showSaveFileDialog
from logic.feedback import feedback as Fb
from logic.oilstation import oilcheck as oc
import  traceback


def initTabOil(self:MyWindow):
    filepath=loadinputPath()
    self.lb_inputpath.setText(filepath)
    filepath=loadOutputPath()
    self.lb_outputpath.setText(filepath)
    filepath = loadFeedbackOutputPath()
    self.lb_fb_outputfilepath.setText(filepath)
    self.pbExport.clicked.connect(lambda: dataExport(self))
    self.pbOutputPath.clicked.connect(lambda: showSaveFileDialog(self, loadinputPath(),lambda x:saveOutputPath(self,x)))
    self.pbInputPath.clicked.connect(lambda:showPathDialog(self, loadinputPath(),lambda x:saveInputPath(self,x)))
    self.pboutput.setValue(0)
    #self.lv_feedback_path.setSelectionMode(QtGui.QAbstractItemView.SingleSelection )  #xtendedSelection 按住ctrl多选, SingleSelection 单选 MultiSelection 点击多选 ContiguousSelection 鼠标拖拉多选
    self.pb_add_teamfeedbackpath.clicked.connect(lambda :showFilePathDialog(self,loadFeedbackFilepath(self),lambda x:addFeedbackFilepath(self,x)))
    self.pb_del_fblv_select.clicked.connect(lambda :removeFeedbackSelection(self))
    self.pb_teamfeedbackexport.clicked.connect(lambda:feedbackexport(self))
    self.pb_feedbackoutputpath.clicked.connect(lambda :showSaveFileDialog(self,os.path.split(loadOption(getlocalpath(), "feedback", "outputpath"))[0],lambda x:saveFeedbackOutputpath(self,x)))
    self.pb_oil_update.clicked.connect(lambda :saveOildata2DB(self))

def showDialog(self):
    try:
        num = 1000000
        progress = QProgressDialog(self)
        progress.setWindowTitle("请稍等")
        progress.setLabelText("正在操作...")
        progress.setCancelButtonText("取消")
        progress.setMinimumDuration(5)
        progress.setRange(0, num)
        for i in range(num):
            progress.setValue(i)
            if progress.wasCanceled():
                QMessageBox.warning(self, "提示", "操作失败")
                break
        else:
            progress.setValue(num)
            QMessageBox.information(self, "提示", "操作成功")
    except:
        traceback.print_exc()

def saveOildata2DB(self:MyWindow):
    reply = QMessageBox.information(self,  # 使用infomation信息框
                                    "提示",
                                    "确定将数据导入数据库中？",
                                    QMessageBox.Yes | QMessageBox.No)
    print(reply==QMessageBox.Yes)
    try:
        if reply==QMessageBox.Yes:
            oc.save2Data(self.lb_inputpath.text())
            QMessageBox.information(self,"提示","导入完成")
    except:
        traceback.print_exc()
        #showDialog(self)
    pass #1、显示确认对话框
         #2、显示等待对话框
         #3、完成任务提示，显示结果



#获取当前路径
def getlocalpath():
    settingPath = os.path.join(ct.loadSetupPath(), gConst["settings"]["setfilepath"])
    print(settingPath)
    #如果目录不存在，是否是编码文件目录
    if not ft.checkfileexist(settingPath):
        settingPath=os.path.join((os.path.dirname(os.getcwd())),"tools\\config\\setting.ini")
    if not ft.checkfileexist(settingPath):
        settingPath=""
    print(settingPath)
    return settingPath
#读取反馈输出目录
def loadFeedbackOutputPath():
    return loadOption(getlocalpath(), "feedback", "outputpath")

#设置反馈输出目录
def saveFeedbackOutputpath(self,path):
    if path is "":
        return
    try:
        self.lb_fb_outputfilepath.setText(str(path))
        updateItem(getlocalpath(), "feedback", "outputpath", path)
    except:
        traceback.print_exc()

#导出反馈数据
def feedbackexport(self:MyWindow):
    try:
        list=[]
        for i in range( self.list_feedbackinpath.count()):
            list.append(self.list_feedbackinpath.item(i).text().replace("/","\\"))
        print(list)
        result=Fb.scanfiles_3(list)
        #ft.copyFile("G:\\pythonproject\\res\\xls\\temple.xls","G:\\油耗\\temple.xls")
        Fb.writetofile(result[0],"G:\\油耗\\temple.xls","统计表","路别")
        #Fb.writetofile(result[1],"G:\\油耗\\temple.xls","单车运行表","路别")
        #Fb.writeSumToXls(result[0], self.lb_fb_outputfilepath.text())
        #Fb.writeDetailToXls(result[1], self.lb_fb_outputfilepath.text())

    except:
        traceback.print_exc()


#删除反馈目录中被选中的项
def removeFeedbackSelection(self:MyWindow):
    try:
        for item in self.list_feedbackinpath.selectedItems():
            print(self.list_feedbackinpath.row(item))
            print(item.text())
            self.list_feedbackinpath.takeItem(self.list_feedbackinpath.row(item))
    except:
        traceback.print_exc()

#读取车队反馈目录,从list被选中项中获取，如果列表为空，则为为根目录
def loadFeedbackFilepath(self:MyWindow):
    try:
        if self.list_feedbackinpath.count()>0:
            return os.path.split(self.list_feedbackinpath.item(self.list_feedbackinpath.count()-1).text())[0]
        else:
            return os.path.split(loadOption(getlocalpath(), "feedback", "inputpath"))[0]
    except:
        traceback.print_exc()

#添加目录到反馈目录列表
def addFeedbackFilepath(self:MyWindow,path):
    try:
        for i in range(self.list_feedbackinpath.count()):
            if self.list_feedbackinpath.item(i).text()==path:
                return
        self.list_feedbackinpath.addItem(path)
        updateItem(getlocalpath(), "feedback", "inputpath", path)
    except:
        traceback.print_exc()

#combobox发生改变触发时间
def monthchange(self:MyWindow):
    path=os.path.split(self.lb_outputpath.text())[0]
    self.lb_outputpath.setText(path)

#获取当前导出目录
def loadOutputPath():
    return  loadOption(getlocalpath(),"oil","outputpath")

#获取当前导入目录
def loadinputPath():
    return loadOption(getlocalpath(),"oil","inputpath")

#保存当前导入目录
def saveInputPath(self,path):
    self.lb_inputpath.setText(str(path))
    updateItem(getlocalpath(), "oil", "inputpath", path)
#保存当前导出目录
def saveOutputPath(self,path):
    self.lb_outputpath.setText(str(path))
    updateItem(getlocalpath(), "oil", "outputpath", path)

def dataExport(self:MyWindow):
    exportSheet1="明细"
    exportSheet2="汇总"
    items=searchforFile(self.lb_inputpath.text())
    exportPath=self.lb_outputpath.text()
    if not ft.checkfileexist(exportPath):
        xt.createNewFile(exportPath,exportSheet1)
    if not xt.checkSheetExist(exportPath,exportSheet1):
        xt.createSheet(exportPath,exportSheet1)
    try:
        xt.writetofile(items,exportPath,exportSheet1,lambda x:self.pboutput.setValue(x))

        QMessageBox.information(self,"提示","导出成功")
        self.pboutput.setValue(0)
    except:
        traceback.print_exc()

def writehuizong(items,filename,sheetname):
    oldWb = xlrd.open_workbook(filename, formatting_info=True)
    newWb = copy(oldWb)
    newWs = newWb.get_sheet(sheetname)

def getlocation(filename,sheetname):
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    ncols=table.ncols
    datalist=[]
    for i in range(0,ncols):
        if table.cell(i, 1)!="":
            item ={table.cell(i,1).value:[i,2]}
            datalist.append(item)
    for i in range(0,ncols):
        if table.cell(i, 4)!="":
            item ={table.cell(i,4).value:[i,5]}
            datalist.append(item)
    return datalist



def load_xml_data(table,routename):
    # 获取当前表格的行数
    nrows = table.nrows
    # 获取当前表格的列数
    ncols = table.ncols
    list = []
    index = xt.getStartIndex(table,"交易时间")
    for i in range(index, nrows):
        # carId = str(table.cell(i, 1).value)
        if table.cell(i, 0).value is "":
            continue
        if contains(table.cell(i, 0).value, "合计"):
            continue
        paytime = table.cell(i, 0).value
        carNum = table.cell(i, 1).value
        printnum = table.cell(i, 2).value
        carId = "闽AY" + str(table.cell(i, 3).value)[0:4]
        oiltpye = table.cell(i, 4).value
        station = table.cell(i, 5).value
        charge = table.cell(i, 6).value
        item = {}
        item["route"]=routename
        item["paytime"] = paytime
        item["cardnum"] = carNum
        item["printnum"] = printnum
        item["carid"] = carId
        item["oiltype"] = oiltpye
        item["oilstation"] = station
        item["charge"] = charge
        list.append(item)

    return list


def searchforFile(path):
    items = []
    dirs = os.listdir(path)
    for file in dirs:
        filepath = path + "\\" + str(file)
        if os.path.isdir(filepath):
            items += searchforFile(filepath)
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1] == ".xls" and contains(filepath, "明细"):
                print(filepath)
                data = xlrd.open_workbook(filepath)
                table = data.sheet_by_name("1")
                list = load_xml_data(table,os.path.split(filepath)[1][0:-6])
                for item in list:
                    items.append(item)
    return items


