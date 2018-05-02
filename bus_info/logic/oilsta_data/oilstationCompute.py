import xlrd
import os
import tools.xlstool as xt
import tools.filetool as ft
from xlutils.copy import copy
from tools.strtool import contains
def getlocation(filename,sheetname):
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    items={}
    for i in range(0,nrows):
        if table.cell(i, 1).value !="线路"and table.cell(i, 1).value !="":
            items [str((table.cell(i,1).value)).replace(".0","")]=[i,2]
    for i in range(0,nrows):
        if table.cell(i, 4).value!="线路" and table.cell(i, 4).value !="":
            items [str((table.cell(i,4).value)).replace(".0","")]=[i,5]
    items["21专线"]=items["21支"]
    items["一公司公备"]=[30,5]


    return items

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
                item = load_xml_data(table,os.path.split(filepath)[1][0:-6])
                items.append(item)
    return items
def load_xml_data(table,routename):
    # 获取当前表格的行数
    nrows = table.nrows
    # 获取当前表格的列数
    ncols = table.ncols
    item = {}
    item["route"] = routename.replace("路","")
    totalCharge=0
    index = xt.getStartIndex(table,"交易时间")
    for i in range(index, nrows):
        # carId = str(table.cell(i, 1).value)
        if table.cell(i, 0).value is "":
            continue
        if contains(table.cell(i, 0).value, "合计"):
            continue
        charge = table.cell(i, 6).value
        totalCharge+=float(charge)

    item["charge"]=totalCharge
    return item
def writeToFile(filename,sheetname,locals,datas):
    if not ft.checkfileexist(filename):
        ft.copyFile("G:\\pythonproject\\res\\xls\\temple.xls",filename)
    oldWb = xlrd.open_workbook(filename, formatting_info=True)
    newWb = copy(oldWb)
    newWs = newWb.get_sheet(sheetname)

    for data in datas:
        local=locals[data["route"]]
        newWs.write(local[0], local[1], data["charge"])
    newWb.save(filename)

def option1():
    items = getlocation("G:\\pythonproject\\res\\xls\\temple.xls", "汇总")
    items2 = searchforFile("G:\\油耗\\油料中心\\4月")
    writeToFile("G:\\油耗\\导出数据\\18年4月油耗.xls", "汇总", items, items2)


if __name__ =="__main__":
    print(os.getcwd())
    items=getlocation("G:\\pythonproject\\res\\xls\\temple.xls","汇总")
    items2 = searchforFile("G:\\油耗\\油料中心\\4月")
    writeToFile("G:\\油耗\\导出数据\\18年4月油耗2222.xls","汇总",items, items2)
