
# ---------------- import --------------------------------------------

import re
from oletools import olevba

# 자동 실행 매크로
re_autoexec = re.compile(r'(?i)\b(?:Auto(?:Exec|_?Open|_?Close|Exit|New)' +
                         r'|Document(?:_?Open|_Close|_?BeforeClose|Change|_New)' +
                         r'|NewDocument|Workbook(?:_Open|_Activate|_Close|_BeforeClose)' +
                         r'|\w+_(?:Painted|Painting|GotFocus|LostFocus|MouseHover' +
                         r'|Layout|Click|Change|Resize|BeforeNavigate2|BeforeScriptExecute' +
                         r'|DocumentComplete|DownloadBegin|DownloadComplete|FileDownload' +
                         r'|NavigateComplete2|NavigateError|ProgressChange|PropertyChange' +
                         r'|SetSecureLockIcon|StatusTextChange|TitleChange|MouseMove' +
                         r'|MouseEnter|MouseLeave|OnConnecting))|Auto_Ope\b')

RE_OPEN_WRITE = r'(?:\bOpen\b[^\n]+\b(?:Write|Append|Binary|Output|Random)\b)'


# 쓰기 키워드
re_write = re.compile(r'(?i)\b(?:FileCopy|CopyFile|Kill|CreateTextFile|'
    + r'VirtualAlloc|RtlMoveMemory|URLDownloadToFileA?|AltStartupPath|WriteProcessMemory|'
    + r'ADODB\.Stream|WriteText|SaveToFile|SaveAs|SaveAsRTF|FileSaveAs|MkDir|RmDir|SaveSetting|SetAttr)\b|' + RE_OPEN_WRITE)

RE_DECLARE_LIB = r'(?:\bDeclare\b[^\n]+\bLib\b)'


# 실행 매크로
re_execute = re.compile(r'(?i)\b(?:Shell|CreateObject|GetObject|SendKeys|RUN|CALL|'
    + r'MacScript|FollowHyperlink|CreateThread|ShellExecuteA?|ExecuteExcel4Macro|EXEC|REGISTER|SetTimer)\b|' + RE_DECLARE_LIB)


# --- CLASSES ---------------------------------------------------------------


# 결과값 클래스 생성


class Result_NoMacro(object):
    exit_code = 0
    color = 'green'
    name = '매크로 없음'

class Result_NotMSOffice(object):
    exit_code = 1
    color = 'green'
    name = '매크로 없음'

class Result_MacroOK(object):
    exit_code = 2
    color = 'cyan'
    name = '정상 매크로'

class Result_Error(object):
    exit_code = 10
    color = 'yellow'
    name = '에러'

class Result_Suspicious(object):
    exit_code = 20
    color = 'red'
    name = '의심스러움'

class MacroDocuFree(object):
    """
    VBA 매크로 코드를 탐지하기 위한 클래스
    """

    def __init__(self, vba_code):
        """
        DocuFree 초기화
        :파라미터 값으로 vba_code를 받습니다.
        """

        self.vba_code = olevba.vba_collapse_long_lines(vba_code)
        self.autoexec = False
        self.write = False
        self.execute = False
        self.flags = ''
        self.suspicious = False
        self.autoexec_match = None
        self.write_match = None
        self.execute_match = None
        self.matches = []
    
    def scan(self):
        """
        매크로 VBA 코드를 탐지하기 위한 함수
        :return None
        """

        mode = re_autoexec.search(self.vba_code)
        if mode is not None:
            self.autoexec = True
            self.autoexec_match = mode.group()
            self.matches.append(mode.group())

        mode = re_write.search(self.vba_code) 
        if mode is not None:
            self.write = True
            self.write_match = mode.group()
            self.matches.append(mode.group())

        mode = re_execute.search(self.vba_code)
        if mode is not None:
            self.execute = True
            self.execute_match = mode.group()
            self.matches.append(mode.group())

        if self.autoexec and (self.execute or self.write):
            self.suspicious = True

def ChangePathFormat(filepath):
    
    
    filepath = filepath.replace("\\\\","\\").replace("\'","").replace("\"","")
    
    return filepath

# --- MAIN ---------------------------------------------------


def main(args):


    """
    메인
    """

    # 로그 설정, 기본값은 경고
   
    options = {'recursive': None, 'zip_password': None, 'zip_fname': '*', 'loglevel': 'warning', 'show_matches': None}
    result_dics = {}
    exitcode = -1
    
    # args = 리스트 형식으로 받음

    for filename in args:
        # 위 코드에 따라서 data, container 는 None 이 될 수도 있음 (단일 파일일 경우)
        try:
            vba_parser = olevba.VBA_Parser(filename=filename, data=None, container=None)
            

        except Exception as e:

            result = Result_Error
        

            continue

        if vba_parser.detect_vba_macros():
            vba_code_all_modules = ''
            try:
                vba_code_all_modules = vba_parser.get_vba_code_all_modules()

            except Exception as e:

                result = Result_Error

                continue
        
            docufree = MacroDocuFree(vba_code_all_modules)
            docufree.scan()


            result = Result_Suspicious if docufree.suspicious else Result_MacroOK

        else:

            result = Result_NoMacro
        

        if result.exit_code > exitcode:
            result_dics[filename] = result

        vba_parser.close()


    return result_dics




