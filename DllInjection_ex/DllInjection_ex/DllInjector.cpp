#include "DllInjector.h"

using namespace std;
DllInjector::DllInjector() {
	injectDllPath = L"PassFilePath.dll";

}


void DllInjector::InjectorStart() {
	this->GetOfficeProcessHandle();
}

BOOL DllInjector::InjectDll(DWORD processID) {
	WCHAR* pathConvStr = NULL;
	wchar_t programPath[_MAX_PATH];
	_bstr_t convert(injectDllPath);
	pathConvStr = convert;
	NTSTATUS status = RhInjectLibrary(
		processID,
		0,
		EASYHOOK_INJECT_DEFAULT,
		NULL,
		pathConvStr,
		NULL,
		0


	);


	GetModuleFileName(NULL, programPath, _MAX_PATH);

	// OutputDebugString(programPath);
	if (status != 0) {
		if (status == -1073741790) { // ACCESS 권한이 DENY 여서 HOOKING을 못할 경우 return, 이미 시스템에서 사용하고 있을 경우
			return FALSE;
		}


		// 다른 에러 코드 필터링
		printf("RhInjectLibaray failed with error code = %d\n", status);
		PWCHAR err = RtlGetLastErrorString();
		wcout << err << endl;

	}
	else {
		wcout << L"Libaray Injected success" << endl;

	}

	return TRUE;
}



BOOL DllInjector::SearchDll(HANDLE hProcess) {
	HMODULE hMods[1024];
	DWORD cbNeeded;
	unsigned int i;
	
	BOOL dllfindFlag = false;

	if (EnumProcessModules(hProcess, hMods, sizeof(hMods), &cbNeeded)) {
		
		for (i = 0; i < (cbNeeded / sizeof(HMODULE)); i++) {
			TCHAR szModName[MAX_PATH];
			
			if (GetModuleFileNameEx(hProcess, hMods[i], szModName, sizeof(szModName) / sizeof(TCHAR))) {

				wstring strDllPath = szModName;
				
				if (strDllPath.find(injectDllPath) != wstring::npos) { // 로드된 모듈 중에 해당 DLL 이 인식이 될 경우 
					cout << "dllFind!!";
					cout << endl;
					
					dllfindFlag = true;
					break;
				}
			}
		}
	}

	return dllfindFlag;
}



int DllInjector::GetOfficeProcessHandle() {
	HANDLE hProcess = NULL;
	BOOL dllInjectFlag = false;
	while (true) {
		PROCESSENTRY32 entry; // 프로세스 항목을 지정할 구조체
		entry.dwSize = sizeof(PROCESSENTRY32); // 구조체 사이즈 지정

		// 현 시스템의 모든 프로세스에 대한 스냅샷을 포함, NULL 일 경우 특정 프로세스가 아닌 모든 프로세스 대상으로 스냅샷 포함

		HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, NULL);

		if (Process32First(snapshot, &entry) == TRUE) {
			while (Process32Next(snapshot, &entry) == TRUE) {

				
				if (lstrcmpW(entry.szExeFile, L"WINWORD.EXE") == 0) {
					// stricmp : 대소문자 구분하지 않는 문자열 비교 수행, 0 == 일치할 경우
					std::cout << "word find!!";
					
					hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, entry.th32ProcessID);
					dllInjectFlag = SearchDll(hProcess);
					
					if (!dllInjectFlag) { // 기존에 dll 이 없을 경우에만
					
						this->InjectDll(entry.th32ProcessID);
					}
					
					
				}
				

				if (lstrcmpW(entry.szExeFile, L"POWERPNT.EXE") == 0) {
					// stricmp : 대소문자 구분하지 않는 문자열 비교 수행, 0 == 일치할 경우
					std::cout << "ppt find!!";
					
					hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, entry.th32ProcessID);
					dllInjectFlag = SearchDll(hProcess);

					if (!dllInjectFlag) { // 기존에 dll 이 없을 경우에만
						
						this->InjectDll(entry.th32ProcessID);
					}
					
				}

				if (lstrcmpW(entry.szExeFile, L"EXCEL.EXE") == 0){
					// stricmp : 대소문자 구분하지 않는 문자열 비교 수행, 0 == 일치할 경우
					std::cout << "excel find!!";
					hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, entry.th32ProcessID);
					dllInjectFlag = SearchDll(hProcess);
					if (!dllInjectFlag) { // 기존에 dll 이 없을 경우에만
						
						this->InjectDll(entry.th32ProcessID);
					}
					
				}
				
			}

		}
		Sleep(50);
		cout << "next!!!!" << endl;

	}



	
	
}

