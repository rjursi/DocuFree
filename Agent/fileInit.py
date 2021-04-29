import os
import time
import ctypes

from subprocess import Popen, PIPE
from win32 import win32pipe, win32file
from win32api import OutputDebugString


freeDocDir = ".\\freeDocuments\\"
txt_WhiteListPath = ".\\whiteList.txt"
txt_WhiteList = None

'''
def MakeFreeDoc():
    docxFilePath = ".\\freeDocuments\\docufree.docx"
    excelFilePath = ".\\freeDocuments\\docufree.xlsx"
    pptFilePath = ".\\freeDocuments\\docufree.pptx"

    docxInst = docx.Document()
    docxInst.save(docxFilePath)
    
    xlsxInst = openpyxl.Workbook()
    xlsxInst.save(excelFilePath)
    
    pptxInst = pptx.Presentation()
    pptxInst.save(pptFilePath)
    

def Init_makeFileDir():
    # 안전한 DocuFree 문서 파일이 담기는 폴더 생성
    # 문서 WhiteList 텍스트 파일 생성
    
    
    if not os.path.exists(freeDocDir):
        # 폴더 존재 유무 확인
        os.makedirs(freeDocDir)
        MakeFreeDoc()
    


    if not os.path.exists(txt_WhiteListPath):
        # whiteList 텍스트 파일 존재 여부 확인
        txt_WhiteList = open(txt_WhiteListPath,'w')
        txt_WhiteList.close()
        txt_WhiteList = None
''' 

def AddFileInfo(filePath):
   
    findFlag = False

    if not os.path.exists(txt_WhiteListPath):
        # whiteList 텍스트 파일 존재 여부 확인
        txt_WhiteList = open(txt_WhiteListPath,'w')
    else:
        txt_WhiteList = open(txt_WhiteListPath,'a')
    
    lines = txt_WhiteList.readlines();
    
    for line in lines:
        if filePath in line:
            findFlag = True
            break

    if(!findFlag):
        txt_WhiteList.write("{0}\n".format(filePath))
    
    txt_WhiteList.close()
    txt_WhiteList = None
    
    
def RunPollingProc():
    
   
    pollingProc = Popen(".\\DllInjector.exe", shell = False)

    pipename = "\\\\.\\pipe\\docufree"
    
    
    # 자식 프로세스 (DllInjector) 와 파일명을 추려내기 위한 Pipe 생성
    pipe = win32pipe.CreateNamedPipe(
        pipename,
        win32pipe.PIPE_ACCESS_INBOUND,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1,
        65536, 65536,
        20000,
        None
    )

    while True:
        OutputDebugString("start pipe server...")
        win32pipe.ConnectNamedPipe(pipe, );

        OutputDebugString("client Connected")

        result, data = win32file.ReadFile(pipe, 64*1024)
        win32pipe.DisconnectNamedPipe(pipe)
        OutputDebugString("file readed!!")
        print(data)
        print(data.decode('utf-16'))
        
        AddFileInfo(data.decode('utf-16'))
    
    win32file.CloseHandle(pipe)
   
        
if __name__ == "__main__":
    # Init_makeFileDir()
    RunPollingProc()

