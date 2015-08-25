from PIL import Image
import urllib2
import urllib
import httplib
from StringIO import StringIO


class ImageUtil:
    def __init__(self):
        pass
    
    def merge(self, img1, img2, r=255,g=255,b=255):
        img1 = img1.convert('RGB')
        img2 = img2.convert('RGB')
        R, G, B = img2.split()
        R = R.point(lambda i,r=r: (i == r or 0) and 255)
        G = G.point(lambda i,g=g: (i == g or 0) and 255)
        B = B.point(lambda i,b=b: (i == b or 0) and 255)
        mask = Image.composite(Image.composite(R, G, G), B, B)
        return Image.composite(img1, img2, mask)

    def mergeImageList(self,imageList):
        if not imageList:
            return None
        if len(imageList) == 1:
            return imageList[0]
        if imageList > 1:
            resImg = imageList[0]
            imageList = imageList[1:]
            for img in imageList:
                resImg = self.merge(resImg,img)
            return resImg
    
    def getPILImageFromData(self,data):    
        fo = StringIO()
        fo.write(data)
        fo.flush()    
        fo.seek(0)
        img = Image.open(fo)
        return img
        
    def getURLContent(self,url,data={}):
        """        
        """                 
        if data:
            if type(data) == unicode:                    
                data = str(urllib.unquote(data))                                
            if type(data) == str:
                #data = urllib.urlencode(data)
                f = urllib.urlopen(url,data)  
            else:
                params = urllib.urlencode(data)
                f = urllib.urlopen(url,params) 
        else:
            f = urllib.urlopen(url)        
        data = f.read()
        f.close()
        return data