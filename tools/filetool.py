
import os
import shutil

def createFileIfnotExist(filename):
    if not checkfileexist(filename):
        createfile(filename)

#创建新文件
def createfile(filename,value=""):
    if checkfileexist(filename):
        print("文件已经存在！！！！")
        return
    print("文件不存在！！！！")
    dirpath = os.path.split(filename)[0]
    print("dirpath:"+dirpath)
    if not checkPathexist(dirpath):
        print("目录不存在")
        os.mkdir(dirpath)
    fp=open(filename, "w+")
    fp.write(value)
    fp.close()
#创建新目录
def createdir(dirname):
    if checkPathexist(dirname):
        print("目录已经存在！！！！")
    print("目录不存在！！！！")
    os.mkdir(dirname)

# 扫描文件,并将路径+文件名以列表形式返回
def searchForFile(path,splix):
    items=[]
    dirs = os.listdir(path)
    for file in dirs:
        filepath = path + "\\" + str(file)
        if os.path.isdir(filepath):
            items+=searchForFile(filepath,splix)
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1]== splix:
                print(filepath)
                items.append(filepath)
    return items

#复制文件到新的地址
def copyFile(oldfile,newfile):
    #如果旧文件不存在
    if not checkfileexist(oldfile):
        print("target file didn't exist!")
        return
    #如果新文件目录不存在
    newfiledir=os.path.split(newfile)[0]
    if not os.path.isdir(newfiledir):
        #创建新目录
        os.makedirs(newfiledir)
    shutil.copy(oldfile,newfile)
def copyFiles(sourceDir,  targetDir):
    if sourceDir.find(".svn") > 0:
        return
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,  file)
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            First_Directory = False
            copyFiles(sourceFile, targetFile)

#判断是否是文件
def checkfileexist(filename):
    return os.path.isfile(filename)

#判断路径是否存在
def checkPathexist(dirpath):
    return os.path.isdir(dirpath)
# 读取文件内容并打印
def readFile(filename):
    fopen = open(filename, 'r')  # r 代表read
    for eachLine in fopen:
        print
        "读取到得内容如下：", eachLine
    fopen.close()

