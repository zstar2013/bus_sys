import pytesseract
from PIL import Image
import os
import traceback

class GetImageDate(object):
    def m(self):
        image = Image.open("G:\\b.png")
        text = pytesseract.image_to_string(image)
        return text.encode("utf-8")

    def SaveResultToDocument(self):
        text = self.m()
        f = open("G:\\Verification.txt","w")
        print(text)
        f.write(str(text).encode("utf-8"))
        f.close()

g = GetImageDate()

if __name__ == '__main__':
    os.chdir('G:\\')
    print(os.getcwd())
    try:
        gid=GetImageDate()
        print(gid.m())
    except:
        traceback.print_exc()
