import configparser
import os
import tools.filetool as ft
from logic.GConst import gConst

#通过item更新config文件
def updateConf(filename,updateItems):
    cf = configparser.ConfigParser()
    for key in updateItems.keys():
        cf.add_section(key)
        item = updateItems[key]
        for inerkey in item.keys():
            cf.set(key, inerkey, item[inerkey])
    with open(filename, "w+") as f:
        cf.write(f)

#通过设定值更新config文件
def updateItem(filename,section,key,value):
    cf = configparser.ConfigParser()
    cf.read(filename)
    cf.set(section, key, value)
    with open(filename, "w+") as f:
        cf.write(f)
#读取某项config
def loadOption(settingPath, section, option):
    cf = configparser.ConfigParser()
    cf.read(settingPath)
    return cf.get(section, option)


#创建配置文件
def createConfFile(filename,value):
    ft.createfile(filename,value)

#读取配置文件目录
def loadconfigPath(LocalConfigDir="config"):
    fullpath=os.path.join(os.getcwd(),LocalConfigDir)
    if  not ft.checkPathexist(fullpath):
        ft.createdir(fullpath)
    return fullpath
#读取配置文件
def loadconfigfile(LocalConfigDir="config",LocalCibfigFile="setting.ini"):
    fullname=os.path.join(loadconfigPath(LocalConfigDir),LocalCibfigFile)
    return fullname

#读取安装文件目录
def loadSetupPath():
    return os.getcwd()



# if __name__ == '__main__':
#     filename=gConst["settings"]["setfilepath"]
#     createConfFile(filename=filename)
#     items=gConst["defaultSettings"]
#     updateConf(filename=filename, updateItems=items)

if __name__ == "__main__":
    string=gConst["settings"]["defaultValue"]
    print(string)
    createConfFile(loadconfigfile(),string)
    #  print(loadSetupPath())