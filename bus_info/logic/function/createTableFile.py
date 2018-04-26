from xlwt import Workbook,easyxf
from UI.style import xlsStyle

#生成单车燃料消耗统计表
def write(ws):
    styleTitle = easyxf(xlsStyle.styles["table"]["table_title"])
    ws.write_merge(0,0,0,12,u'车公里单车燃料消耗统计表',styleTitle)
    styleSubTitle=easyxf(xlsStyle.styles["table"]["table_subtitle"])
    ws.write_merge(1,1,0,12,u'2018年2月 (1--28日）        第1页',styleSubTitle)
    stylenormal = easyxf(xlsStyle.styles["table"]["table_normal"])
    ws.write_merge(2,4,0,0,u'单位',stylenormal)
    ws.write_merge(2,4,1,1,u'序号',stylenormal)
    ws.write_merge(2,4,2,2,u'车号',stylenormal)
    ws.write_merge(2,4,3,3,u'车公里',stylenormal)
    ws.write_merge(2,2,4,7,u'柴油消耗(升)',stylenormal)
    ws.write_merge(3,3,4,5,u'指标',stylenormal)
    ws.write_merge(3,3,6,7,u'实绩',stylenormal)
    ws.write(4,4,u'总量',stylenormal)
    ws.write(4,5,u'百公里',stylenormal)
    ws.write(4,6,u'总量',stylenormal)
    ws.write(4,7,u'百公里',stylenormal)
    ws.write_merge(3, 4, 8, 8, u'节约', stylenormal)
    ws.write_merge(3, 4, 9, 9, u'超耗', stylenormal)
    ws.write_merge(2, 3, 10, 12, u'备注', stylenormal)
    ws.write(4, 10, u'二保', stylenormal)
    ws.write(4, 11, u'跟车', stylenormal)
    ws.write(4, 12, u'年审', stylenormal)

#生成单车运行情况汇总表
def write2(ws,route):
    styleTitle = easyxf(xlsStyle.styles["table"]["table_title"])
    ws.write_merge(0, 0, 0, 18, u'单车运行情况汇总表', styleTitle)
    styleSubTitle = easyxf(xlsStyle.styles["table"]["table_subtitle_left"])
    string="福州市公交第一公司一车队"+route+"路"
    ws.write_merge(1, 1, 0, 5,string, styleSubTitle)
    styleSubTitle = easyxf(xlsStyle.styles["table"]["table_subtitle"])
    ws.write_merge(1, 1, 6, 18, u'2018年2月   第1页', styleSubTitle)
    stylenormal = easyxf(xlsStyle.styles["table"]["table_normal"])
    ws.write_merge(2, 4, 0, 0, u'车号', stylenormal)
    ws.write_merge(2, 2, 1, 5, u'车日运用', stylenormal)
    ws.write_merge(3, 4, 1, 1, u'营运\n车日', stylenormal)
    ws.write_merge(3, 4, 2, 2, u'修理\n车日', stylenormal)
    ws.write_merge(3, 4, 3, 3, u'完好\n车日', stylenormal)
    ws.write_merge(3, 3, 4, 5, u'其中', stylenormal)
    ws.write(4, 4, u'停驶车日', stylenormal)
    ws.write(4, 5, u'工作车日', stylenormal)

    ws.write_merge(2, 2, 6, 10, u'车公里', stylenormal)
    ws.write_merge(3, 4, 6, 6, u'合计', stylenormal)
    ws.write_merge(3, 3, 7, 10, u'其中', stylenormal)
    ws.write(4, 7, u'营业', stylenormal)
    ws.write(4, 8, u'包车', stylenormal)
    ws.write(4, 9, u'公用', stylenormal)
    ws.write(4, 10, u'调车', stylenormal)

    ws.write_merge(2, 2, 11, 15, u'营运效率', stylenormal)
    ws.write_merge(3, 4, 11, 11, u'完好车率', stylenormal)
    ws.write_merge(3, 4, 12, 12, u'工作车率', stylenormal)
    ws.write_merge(3, 4, 13, 13, u'故障率', stylenormal)
    ws.write_merge(3, 3, 14, 15, u'故障', stylenormal)
    ws.write(4, 14, u'次', stylenormal)
    ws.write(4, 15, u'分', stylenormal)

    ws.write_merge(2, 3, 16, 17, u'柴油消耗(升)', stylenormal)
    ws.write(4, 16, u'指标', stylenormal)
    ws.write(4, 17, u'实际', stylenormal)

    ws.write_merge(2, 4, 18, 18, u'备注', stylenormal)
