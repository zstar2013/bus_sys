import tools.strtool as st
from xlwt import Workbook,easyxf
import xlrd
from xlutils.copy import copy


#创建新的xls文件
def createNewFile(filename,sheetname="sheet1"):
    w = Workbook()
    ws = w.add_sheet(sheetname)
    w.save(filename)

#检查在xls文件中是否存在sheet表
def checkSheetExist(filename,sheetname):
    data = xlrd.open_workbook(filename)
    for sheet in data.sheets():
        if sheet is not None:
            if sheet.name==sheetname:
                return True
    return False

def createSheet(filename,sheetname):
    oldWb = xlrd.open_workbook(filename, formatting_info=True)
    newWb = copy(oldWb)
    newWb.add_sheet(sheetname)
    newWb.save(filename)


def loadXmlData(table, exceptlist=[]):
    '''

    :param table:xml表
    :return:
    '''
    # 获取当前表格的行数
    nrows = table.nrows
    # 获取当前表格的列数
    ncols = table.ncols
    datalist = []
    index = getStartIndex(table)
    for i in range(index, nrows):
        item = []
        if len(exceptlist) and st.containsAnyOr(table.cell(i, 0), childstrlist=exceptlist):
            continue
        for j in (0, ncols):
            item.append(table.cell(i, j))
            datalist.append(item)
    return datalist


# 获取起始值
def getStartIndex(table, targetstr):
    rowindex = None
    nrows = table.nrows
    ncols = table.ncols
    for i in range(0, nrows):
        for j in range(0, ncols):
            if st.contains(str(table.cell(i, j).value), targetstr):
                rowindex = i + 1
                break
    return rowindex


# 获取当前文件最后一行
def getLastRowIndext(filename, sheetname):
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    return nrows



def writeTitle(filename, sheetname, titles):
    styleBoldRed = easyxf('font: color-index red, bold on')
    headerStyle = styleBoldRed
    wb = Workbook()
    ws = wb.add_sheet(sheetname)
    for i in range(0, len(titles)):
        ws.write(0, i, titles[i], headerStyle)
    wb.save(filename)

    # open existed xls file
    # newWb = xlutils.copy(filename);
    # newWb = copy(filename);


def writetofile(mlist, filename, sheetname ,prograssUpdate):
    oldWb = xlrd.open_workbook(filename, formatting_info=True)
    newWb = copy(oldWb)
    newWs = newWb.get_sheet(sheetname)
    index =getLastRowIndext(filename, sheetname)
    print("-------------------lastindex:"+str(index))
    end = len(mlist)
    print("-------------------------size:"+str(end))
    progress=0
    for i in range(0, end):
        new=int(i*100/end)
        if progress!=new:
            progress=new
            prograssUpdate(new)
        item=mlist[i]
        keys = list(item.keys())
        for j in range(0, len(keys)):
            newWs.write(i + index, j, item.get(keys[j]))
    newWb.save(filename)
    prograssUpdate(100)


if __name__ == '__main__':
    #createNewFile("G:\\油耗\\1234.xls","1")
    string="abcde"
    print(string[0:-2])
    #print(checkSheetExist(\\"G:\\油耗油料数据.xls","2017.01"))