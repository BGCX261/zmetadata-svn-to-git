import time
import traceback
import sys
from zipfile import ZipFile
from StringIO import StringIO

class ZipUtil:
    def __init__(self, zipFile, mode="r"):
        """
        @param zipFile: a zip file path or a file like object
        """     
        self.mode = mode
        self.zipFile = zipFile
        self.zip = ZipFile(self.zipFile, self.mode)
        self.res = []
    
    def getFileContentWithExtension(self,ext):
        """
        @param ext: the file extensions to look for
        @return: a list of file content data
        """       
        retList = []
        for info in self.zip.infolist():
            name = info.filename
            index = name.rfind(".")
            if index != -1:
                if name[len(name)-len(ext):len(name)].lower() == ext:                    
                    data = self.zip.read(name)
                    tmp = [name, data]
                    retList.append(tmp)        
        return retList
    
    def getAllFileContents(self):
        """
        @summary:
        @return:
        """
        retList = []
        for info in self.zip.infolist():
            name = info.filename                
            data = self.zip.read(name)
            tmp = [name, data]
            retList.append(tmp)        
        return retList
    
    def writeData(self, data):
        """
        @param data: is a dict {'fileName': 'string file data'} of file name and data
        """
        if not data.keys():
            return
        
        if type(self.zipFile) == str:
            return
        
        for key in data.keys():
            self.zip.writestr(key, data[key])
        self.zip.close()
        
    def getZipFileData(self):
        """
        @summary: get the content of the written zip file as a string
        """
        data = ""
        if type(self.zipFile) == str:
            f = open(self.zipFile)
            data = f.read();
            f.close()
        if type(self.zipFile) != str:
            self.zipFile.seek(0)    
            data = self.zipFile.read()
        return data
    
if __name__ == "__main__":
    sIO = StringIO("")
    z = ZipUtil(sIO, mode="w")
    
    files = ["c:/temp/httpTest.py", "c:/temp/shpIndex.bat" ]    
    f = open(files[0], "r")
    data1 = f.read();
    f.close()
    f = open(files[1], "r")
    data2 = f.read();
    f.close()
    data = {"httpTest.py":data1, "shpIndex.bat":data2}
    z.writeData(data)
        
    

    
        
        