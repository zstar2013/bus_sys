import xlrd
from xlutils.copy import copy

from bus_info.models import BusInfo, MonthlyFeedback,RouteMaintainCount
from tools import strtool as st
import bus_info.logic.function.createTableFile as ct
import re
import tools.filetool as ft
from xlwt import Workbook,easyxf
import traceback
import datetime

gConst = {"xls": {"sheetName": "新页面", "fileName": "G:\\油耗\\测试数据.xlsx"}}
mFilename = ["G:\\油耗\\12月\\1队\\2017年12月一车队油耗和汇总表.xls"]
mTime = "2017-012"
xOffset=3

#获取明细数据
def load_detail_data(table, item,mlist,time):

    nrows = table.nrows
    indexR = item[0]
    carNoC = item[1]
    route = getRoute(table.name)
    saveMainteData(table,route,time)
    for i in range(indexR, nrows):
        if table.cell(i, carNoC).value is "":
            continue
        if table.cell(i, carNoC).value is "0":
            continue
        if st.contain_zh(str(table.cell(i, carNoC).value)):
            continue
        try:
            car_id=getCar_id(table.cell(i, carNoC).value,table.name)
            bi = BusInfo.objects.get(car_id=car_id)
        except BusInfo.DoesNotExist:
            bi = None

        if bi is not None:
            for mf in mlist:
                if mf.carInfo==bi and mf.route==route:
                    try:
                        mf.work_days= getFloatValue(table.cell(i, carNoC + 5).value)       # 工作天数
                        mf.fix_days=getFloatValue(table.cell(i, carNoC + 2).value)         # 修理天数
                        mf.stop_days=getFloatValue(table.cell(i, carNoC + 4).value)        # 停驶天数
                        mf.shunt_mileage=getFloatValue(table.cell(i, carNoC + 10).value)   # 调车公里
                        mf.engage_mileage=getFloatValue(table.cell(i, carNoC + 8).value)   # 包车公里
                        mf.public_mileage=getFloatValue(table.cell(i, carNoC + 9).value)   # 公用公里
                        mf.fault_times=getFloatValue(table.cell(i, carNoC + 14).value)     # 故障次数
                        mf.fault_minutes=getFloatValue(table.cell(i, carNoC + 15).value)   # 故障分钟
                        mf.save()
                        mlist.remove(mf)
                    except:
                        traceback.print_exc()
                        print("--------------------------",mf.carInfo)

                    break
    #print("---------------------------------------mlist", mlist)

        # item.append(table.cell(i, carNoC + 1).value)    #营运天数
        # item.append(table.cell(i, carNoC + 2).value)    #修理天数
        # item.append(table.cell(i, carNoC + 3).value)    #完整天数
        # item.append(table.cell(i, carNoC + 4).value)  # 停驶天数
        # item.append(table.cell(i, carNoC + 5).value)  # 工作天数
        # item.append(table.cell(i, carNoC + 7).value)  # 营业公里
        # item.append(table.cell(i, carNoC + 8).value)  # 包车公里
        # item.append(table.cell(i, carNoC + 9).value)  # 公用公里
        # item.append(table.cell(i, carNoC + 10).value)  # 调车公里
        # item.append(table.cell(i, carNoC + 14).value)  # 故障次数
        # item.append(table.cell(i, carNoC + 15).value)  # 故障分钟

def getFloatValue(s):
    result=str(s).replace('/t','')
    if result =="":
        return 0.0

    else:
        return float(result)

def getIntValue(s):
    result = str(s).replace('/t', '')
    if result =="":
        return 0
    else:
        return int(result)

#保存一保二保数目
def saveMainteData(table,route,time):
    # 获取每张表格一保二保数目
    for i in range(0, table.nrows):
        for j in range(0, table.ncols):
            string = str(table.cell(i, j).value)
            if st.contains(string, "一保"):
                frist=re.findall(r"\d+\.?\d*", string)[0]
            if st.contains(string, "二保"):
                second = re.findall(r"\d+\.?\d*", string)[0]
    try:
        rmc=RouteMaintainCount.objects.get(route=route,date=datetime.datetime(2018,3,1))
        rmc.num_fir_maintain += getIntValue(frist)
        rmc.num_sec_maintain += getIntValue(second)
        rmc.save()
    except RouteMaintainCount.DoesNotExist:
        nrmc=RouteMaintainCount(route=route,date=datetime.datetime(2018,3,1),num_fir_maintain=frist,num_sec_maintain=second)
        nrmc.save()
        return


#读取统计数据文件
def load_sum_data(table, item):
    nrows = table.nrows
    list = []
    indexR = item[0]
    carNoC = item[1]
    for i in range(indexR, nrows):
        if table.cell(i, carNoC).value is "":
            continue
        if st.contains(str(table.cell(i, carNoC).value), "小计"):
            continue
        try:
            car_id=getCar_id(table.cell(i, carNoC).value,table.name)
            bi = BusInfo.objects.get(car_id=car_id)
        except BusInfo.DoesNotExist:
            bi = None
            pass
        if bi is not None:
            route = getRoute(table.name)
            mileage = getFloatValue(table.cell(i, carNoC + 1).value)  # 车公里
            team_target = getFloatValue(table.cell(i, carNoC + 3).value)  # 车队上报指标
            oilwear = getFloatValue(table.cell(i, carNoC + 4).value)  # 车辆油耗
            maintain = getFloatValue(table.cell(i, carNoC + 8).value)  # 二保
            follow = getFloatValue(table.cell(i, carNoC + 9).value)  # 跟车
            mf = MonthlyFeedback(date=datetime.datetime(2018, 3, 1), route=route, carInfo=bi, mileage=mileage,
                                 oilwear=oilwear, maintain=maintain, follow=follow,team_target=team_target)
            #mf.save()
            list.append(mf)

    return list

#对车牌号进行判断，如果不符合标准则标记为暂定无效数据
def check_ID_validty(id):
    s = str(id)
    #若车牌号小于4位，则判定为失效
    if len(s) < 4:
        return False
    return True

#获取扫描起始位置
def getStartIndex(table,target="车号"):
    rowindex = None
    colindex = None
    nrows = table.nrows
    ncols = table.ncols
    for i in range(0, nrows):
        for j in range(0, ncols):
            if table.cell(i, j).value ==target:
                rowindex = i
                colindex = j
                break
    if rowindex is None:
        return None
    item = [rowindex + xOffset, colindex]
    return item

def writetofile(list,filename=gConst['xls']['fileName'],sheetname=gConst['xls']['sheetName'],target="路别"):

    oldWb = xlrd.open_workbook(filename, formatting_info=True)
    newWb = copy(oldWb);
    newWs = newWb.get_sheet(sheetname)
    table=xlrd.open_workbook(filename).sheet_by_name(sheetname)
    index=6
    index = getStartIndex(table, target)
    end=len(list)
    for i in range(0,end):
        jend=len(list[i])
        for j in range(0,jend):
            if list[i][j] is None:
                newWs.write(i+index[0], index[1]+j, "")
                continue
            else:
                newWs.write(i+index[0], index[1]+j, list[i][j])

    newWb.save(filename)

#写入到汇总表中
def writeDetailToXls(list, filename=gConst['xls']['fileName']):
    try:
        if ft.checkfileexist(filename):
            oldWb = xlrd.open_workbook(filename, formatting_info=True)
            newWb = copy(oldWb)
        else :
            newWb = Workbook()
        index=[5,-1]
        currentroute=""
        end=len(list)
        for i in range(0,end):
            jend=len(list[i])
            for j in range(0,jend):
                if index[1]+j<0:
                    if str(list[i][j])!=currentroute:
                        currentroute=str(list[i][j])
                        ws = newWb.add_sheet(str(list[i][j])+"路汇总表")
                        ct.write2(ws,str(list[i][j]))
                        index[0]=5-i
                    continue
                if list[i][j] is None:
                    ws.write(i+index[0], index[1]+j, "")
                    continue
                else:
                    ws.write(i+index[0], index[1]+j, list[i][j])
        newWb.save(filename)
    except:
        traceback.print_exc()

def writeSumToXls(list,filename=gConst['xls']['fileName']):
    try:
        if ft.checkfileexist(filename):
            oldWb = xlrd.open_workbook(filename, formatting_info=True)
            newWb = copy(oldWb)
        else:
            newWb = Workbook()
            print(list)
        for route_list in list:
            route=str(route_list[0])
            ws = newWb.add_sheet(route + "路统计表")
            ct.write(ws)
            end = len(route_list[1])
            index = [5, 1]
            for i in range(0,end):
                print(i)
                jend = len(route_list[1][i])
                for j in range(0, jend):
                    if route_list[1][i][j][0] is None:
                        continue
                    else:
                        ws.write(i + index[0], index[1] + int(route_list[1][i][j][1]), str(route_list[1][i][j][0]))
        newWb.save(filename)
    except:
        traceback.print_exc()



#获取对应的路线名称
def getRoute(tablename):
    if st.contains(tablename, "专线"):
        return "海峡专线"
    if st.contains(tablename, "夜班"):
        return "夜班一号线"
    if st.contains(tablename.lower(), "k2"):
        return "k2"
    if st.contains(tablename.lower(), "21支"):
        return "142"
    if st.contains(tablename.lower(), "30支"):
        return "149"
    route = re.findall(r"\d+\.?\d*", tablename)
    return route[0]


# 对车辆id进行处理
def getCar_id(id, tablename):
    s = str(id)
    if (st.contains(str(id), "路")):
        s = str(id).split("路")[1].strip()
    if (st.contains(str(id), "线")):
        s = str(id).split("线")[1].strip()
    if st.contains(s, ".") or len(s) == 3:
        s = s.split(".")[0]
        if len(s)==4:
            return s
        route = getRoute(tablename)
        if route == "1" or route == "17" or route == "28" or route == "161":
            s = "A" + s
        elif route == "501"or route=="200":
            s = "B" + s
    return s


# 获取当前文件最后一行
def getlastrowindex():
    data = xlrd.open_workbook(gConst['xls']['fileName'])
    table = data.sheet_by_name(gConst['xls']['sheetName'])
    nrows = table.nrows
    return nrows

# 扫描文件
def scanfiles(filelist=mFilename, time="18年3月"):
    result=([],[])

    #依次查询文件列表
    for i in range(0, len(filelist)):
        mlist = []
        #打开文件
        data = xlrd.open_workbook(filelist[i])
        #遍历sheet
        for sheet in data.sheets():
             if st.contains(sheet.name,"统计"):
                table = data.sheet_by_name(sheet.name)
                loacl_of_startItem=getStartIndex(table)
                if loacl_of_startItem is None:
                    continue
                else:
                    mlist.extend(load_sum_data(table, loacl_of_startItem))

        #print("----------------------------------mlist", mlist)
        #再次遍历sheet
        for sheet in data.sheets():
             if st.contains(sheet.name, "汇总"):
                table = data.sheet_by_name(sheet.name)
                loacl_of_startItem = getStartIndex(table)
                if loacl_of_startItem is None:
                    continue
                else:
                    print("----------------------------------",loacl_of_startItem)
                    load_detail_data(table, loacl_of_startItem,mlist,time)
        mlist=None
    return result

def checkRouteExist(result,name):
    for i in range(0,len(result)):
        if result[i][0]==name:
            return i

    return 0

