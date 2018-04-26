import hashlib
import os
import time




def get_md5_01(file_path="G:\myfile\GitHubDesktopSetup.exe"):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5






def get_md5_02(file_path="G:\myfile\GitHubDesktopSetup.exe"):
    f = open(file_path, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    return md5

if __name__ == "__main__":
    start=time.clock()
    file_path = r'G:\myfile\jdk-8u144-windows-x64.exe'
    md5_01 = get_md5_01(file_path)
    print(md5_01)
    end=time.clock()
    print((end-start)/10000)

    start=time.clock()
    file_path = r'G:\myfile\jdk-8u144-windows-x64.exe'
    md5_02 = get_md5_02(file_path)
    print(md5_02)
    end=time.clock()
    print((end-start)/10000)
# if __name__ == "__main__":
#     file_path = r'D:\test\test.jar'
#     md5_02 = get_md5_02(file_path)
#     print(md5_02)
