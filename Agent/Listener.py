import os
import sys
import time
from subprocess import Popen, PIPE
import subprocess
from win32 import win32pipe, win32file
from win32api import OutputDebugString
from PyQt5.QtCore import *
from PyQt5 import QtCore


from DocuListener.CommApiServer import DocuInfoComm
from DocuListener.DocuFilter import docufree
import CheckLogUpdater



class DocuListener(QThread):
    
    # 팝업창을 main 윈도우에서 띄울수 있도록 하는 이벤트 핸들러
    threadEvent = QtCore.pyqtSignal(str)
    remove_files = []
    def __init__(self):
        super().__init__()
        self.isRun = False
        


        self.txt_WhiteListPath = "whiteList.txt"
        self.txt_WhiteList = None
        self.cmd_closeTemp = "CloseTempDocu.exe"
        self.mainPath = os.path.dirname(sys.executable)

    def ExitMessageToNamedPipe(self):
        pipename = "\\\\.\\pipe\\docufree"
        pipe_handle = win32file.CreateFile(pipename, win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)


        err, bytes_written = win32file.WriteFile(pipe_handle, bytes("exit", 'utf-16'))
        
        win32file.CloseHandle(pipe_handle)

    def run(self):
        
        
        OutputDebugString("Create Or Check DB Exists...")
        
        pollingProc = Popen(".\\DllInjector.exe", shell = False)

        # pollingProc = Popen(dllInjectorPath, shell = False)
        
        pipename = "\\\\.\\pipe\\docufree"
        filename = None
        
        # 자식 프로세스 (DllInjector) 와 파일명을 추려내기 위한 Pipe 생성
        self.pipe = win32pipe.CreateNamedPipe(
            pipename,
            win32pipe.PIPE_ACCESS_INBOUND,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1,
            65536, 65536,
            20000,
            None
        )

        while self.isRun:
            
            OutputDebugString("start pipe server...")
            win32pipe.ConnectNamedPipe(self.pipe, );

            OutputDebugString("client Connected")

            result, data = win32file.ReadFile(self.pipe, 64*1024)

            win32pipe.DisconnectNamedPipe(self.pipe)
            OutputDebugString("file readed!!")
            print(data)
            print(data.decode('utf-16'))
            filename = data.decode('utf-16');
            print(filename)


            if filename not in "exit":

                filename = repr("\"" + filename + "\"")
            
                filename = filename.replace("\\x00","")
                subprocess.run([self.cmd_closeTemp, filename]) # 열렸던 파일 닫히도록

                # ApiServer Check
                searchResult = DocuInfoComm.SetSearchFile(filename)
                
                print(searchResult)
                
                # API Server 를 통해서 검색 결과가 없을 경우에만
                if not searchResult:
                    
                    input_args = []
                    formatChanged_filename = self.ChangePathFormat(filename)
                    input_args.append(formatChanged_filename)
                    docufree_result = docufree.main(input_args)
                
                    if docufree_result[formatChanged_filename].exit_code == 20: # 의심스로운 키워드로 검출이 될 경우
                        
                        # 알림창을 띄우라는 신호를 보냄
                    
                        insert_result = DocuInfoComm.add(filename)
                        if insert_result: 
                            self.threadEvent.emit(self.ChangePathFormat_whiteList(filename))
                            os.remove(self.ChangePathFormat(filename))
                        else:
                            print("Info Insert Error!!")
                    else:
                        
                        self.AddFileInfo(self.ChangePathFormat_whiteList(filename)) # 나중에 다시 검사하지 않도록 whitelist 추가
                        os.startfile(self.ChangePathFormat(filename))
                
                    CheckLogUpdater.InsertLog(self.ChangePathFormat(filename), docufree_result[formatChanged_filename].name)


                # 서버 데이터베이스 단에서 확인이 이루어지는 경우
                else:
                    self.threadEvent.emit(self.ChangePathFormat(filename))
                    os.remove(self.ChangePathFormat(filename))


               
            

        win32file.CloseHandle(self.pipe)
        pollingProc.terminate()
    

    def ChangePathFormat_whiteList(self, filepath):
        new_pathFormat = filepath.replace("\\\\","\\").replace("//","/").replace("\'","").replace("\"","")
        
        return new_pathFormat


    def ChangePathFormat(self, filepath):
        
        new_pathFormat = filepath.replace("\\","/").replace("//","/").replace("\'","").replace("\"","")
        
        return new_pathFormat

    def AddFileInfo(self, filePath):
    
        findFlag = False
        
        
        if not os.path.exists(self.txt_WhiteListPath):
            # whiteList 텍스트 파일 존재 여부 확인
            self.txt_WhiteList = open(self.txt_WhiteListPath,'r+')
        else:
            self.txt_WhiteList = open(self.txt_WhiteListPath,'a+')
        
        lines = self.txt_WhiteList.readlines();
        
        for line in lines:
            if filePath in line:
                findFlag = True
                break

        if not findFlag:
            self.txt_WhiteList.write("{0}\n".format(filePath))
        
        self.txt_WhiteList.close()
        self.txt_WhiteList = None
        
