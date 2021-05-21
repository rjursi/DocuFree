__version__ = '0.0.1'

#----------------------------------------------------------------------
'''
TODO
1. file merge 
'''



# ---------------- import --------------------------------------------


import sys, logging, optparse, re, os


_thismodule_dir = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
_parent_dir = os.path.normpath(os.path.join(_thismodule_dir, '..'))

# 시스템 환경변수 설정
if not _parent_dir in sys.path:
    sys.path.insert(0, _parent_dir)


from oletools.thirdparty.xglob import xglob
from oletools.thirdparty.tablestream import tablestream

from oletools import olevba
from oletools.olevba import TYPE2TAG



# ---------------- logging --------------------------------------------


# 디버깅을 위한 전역 로그 객체 생성
log = olevba.get_logger('docufree')


#--- CONSTANTS ----------------------------------------------------------------


URL_ISSUES = 'https://github.com/rjursi/DocuFree'
MSG_ISSUES = 'Report this issue on %s' % URL_ISSUES


# 문자열 매칭을 위한 컴파일

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


# 쓰기 매크로
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
    name = 'No Macro'

class Result_NotMSOffice(object):
    exit_code = 1
    color = 'green'
    name = 'No Macro'

class Result_MacroOK(object):
    exit_code = 2
    color = 'cyan'
    name = 'Macro OK'

class Result_Error(object):
    exit_code = 10
    color = 'yellow'
    name = 'ERROR'

class Result_Suspicious(object):
    exit_code = 20
    color = 'red'
    name = 'SUSPICIOS'

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

        


    def get_flags(self):
        flags = ''
        flags += 'A' if self.autoexec else '-'
        flags += 'W' if self.write else '-'
        flags += 'X' if self.execute else '-'
        return flags

# --- MAIN ---------------------------------------------------

if __name__ == '__main__':
    """
    메인
    """

    # 로그 설정, 기본값은 경고
    DEFAULT_LOG_LEVEL = 'warning'
    LOG_LEVELS = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
            }

    """
    parser 라이브러리 사용
    


    """
    usage = 'usage: docufree [options] <filename> [filename2 ...]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-r", action="store_true", dest="recursive",
            help="find files recursively in subdirectories.")
    parser.add_option("-z", "--zip", dest='zip_password', type='str', default=None, help='if the file is a zip archive, open all files from it, using the provided password (requires Python 2.6+)')
    parser.add_option("-f", "--zipfname", dest="zip_fname", type="str", default="*",
            help="if the file is a zip archives, file(s) to be opened within the zip. Wildcards * and ? are supported. (default:*)")
    parser.add_option('-l', '--loglevel', dest="loglevel", action="store", default=DEFAULT_LOG_LEVEL)
    
    parser.add_option('-m', '--matches', action="store_true", dest="show_matches",
            help="show matches strings.")


    # 대개 변수 받아오기
    (options, args) = parser.parse_args()

    if len(args) == 0:
        print(' DocuFree %s - https://github.com/rjursi/DocuFree' % __version__)
        print('This is work in progress, please report issues at %s' % URL_ISSUES)
        print(__doc__)

        parser.print_help()

        print('\n결과 값에 기반한 exit code: ')

        for result in (Result_NoMacro, Result_NotMSOffice, Result_MacroOK, Result_Error, Result_Suspicious):
            print(' - %d: %s' % (result.exit_code, result.name))
        sys.exit()

    print('DocuFree %s - https://github.com/rjursi/DocuFre' % __version__)
    print('과정 중에 일어난, 이슈는 %s에 남겨주세요' % URL_ISSUES)

    # 로깅 래밸 설정
    logging.basicConfig(level=LOG_LEVELS[options.loglevel], format="%(levelname)-8s %(messages)s")
    
    log.setLevel(logging.NOTSET)

    
    table = tablestream.TableStream(style=tablestream.TableStyleSlim,
            header_row=['Result', 'Flags', 'Type', 'File'],
            column_width=[10, 5, 4, 56])

    exitcode = -1
    global_result = None

    for container, filename, data in xglob.iter_files(args, recursive=options.recursive, zip_password=options.zip_password, zip_fname=options.zip_fname):

        if container and filename.endswith('/'):
            continue
        
        full_name = "%s in %s" % (filename, container) if container else filename

        if isinstance(data, Exception):
            result = Result_Error
            table.write_row([result.name, '', '', full_name],
                    colors=[result.color, None, None, None])
            table.write_row(['', '', '', str(data)],
                    colors=[None, None, None, result.color])
        else:
            filetype = "???"

            try:
                vba_parser = olevba.VBA_Parser(filename=filename, data=data, container=container)
                filetype = TYPE2TAG[vba_parser.type]

            except Exception as e:

                result = Result_Error
                table.write_row([result.name, '', filetype, full_name],
                        colors=[None, None, None, result.color])

                table.write_row(['', '', '', str(e)],
                        colors=[None, None, None, result.color])
                continue

            if vba_parser.detect_vba_macros():
                vba_code_all_modules = ''
                try:
                    vba_code_all_modules = vba_parser.get_vba_code_all_modules()

                except Exception as e:

                    result = Result_Error
                    table.write_row([result.name, '', TYPE2TAG[vba_parser.type], full_name],
                            colors=[result.color, None, None, None])
                    table.write_row(['', '', '', str(e)],
                            colors=[None, None, None, result.color])
                    continue
            
                docufree = MacroDocuFree(vba_code_all_modules)
                docufree.scan()


                result = Result_Suspicious if docufree.suspicious else Result_MacroOK

                table.write_row([result.name, docufree.get_flags(), filetype, full_name],
                        colors=[result.color, None, None, None])

                if docufree.matches and options.show_matches:
                    table.write_row(['', '', '', 'Matches: %r' % docufree.matches])

            else:

                result = Result_NoMacro
                table.write_row([result.name, '', filetype, full_name],
                        colors=[result.color, None, None, None])

            if result.exit_code > exitcode:
                global_result = result
                exitcode = result.exit_code

        print('')
        print('Flags: A=AutoExec, W=Write, X=Execute')
        print('Exit code: %d - %s' % (exitcode, global_result.name))
        sys.exit(exitcode)


if __name__ == '__main__':
    main()





