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
		if (status == -1073741790) { // ACCESS ������ DENY ���� HOOKING�� ���� ��� return, �̹� �ý��ۿ��� ����ϰ� ���� ���
			return FALSE;
		}


		// �ٸ� ���� �ڵ� ���͸�
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
				
				if (strDllPath.find(injectDllPath) != wstring::npos) { // �ε�� ��� �߿� �ش� DLL �� �ν��� �� ��� 
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
		PROCESSENTRY32 entry; // ���μ��� �׸��� ������ ����ü
		entry.dwSize = sizeof(PROCESSENTRY32); // ����ü ������ ����

		// �� �ý����� ��� ���μ����� ���� �������� ����, NULL �� ��� Ư�� ���μ����� �ƴ� ��� ���μ��� ������� ������ ����

		HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, NULL);

		if (Process32First(snapshot, &entry) == TRUE) {
			while (Process32Next(snapshot, &entry) == TRUE) {

				
				if (lstrcmpW(entry.szExeFile, L"WINWORD.EXE") == 0) {
					// stricmp : ��ҹ��� �������� �ʴ� ���ڿ� �� ����, 0 == ��ġ�� ���
					std::cout << "word find!!";
					
					hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, entry.th32ProcessID);
					dllInjectFlag = SearchDll(hProcess);
					
					if (!dllInjectFlag) { // ������ dll �� ���� ��쿡��
					
						this->InjectDll(entry.th32ProcessID);
					}
					
					
				}
				

				if (lstrcmpW(entry.szExeFile, L"POWERPNT.EXE") == 0) {
					// stricmp : ��ҹ��� �������� �ʴ� ���ڿ� �� ����, 0 == ��ġ�� ���
					std::cout << "ppt find!!";
					
					hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, entry.th32ProcessID);
					dllInjectFlag = SearchDll(hProcess);

					if (!dllInjectFlag) { // ������ dll �� ���� ��쿡��
						
						this->InjectDll(entry.th32ProcessID);
					}
					
				}

				if (lstrcmpW(entry.szExeFile, L"EXCEL.EXE") == 0){
					// stricmp : ��ҹ��� �������� �ʴ� ���ڿ� �� ����, 0 == ��ġ�� ���
					std::cout << "excel find!!";
					hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, entry.th32ProcessID);
					dllInjectFlag = SearchDll(hProcess);
					if (!dllInjectFlag) { // ������ dll �� ���� ��쿡��
						
						this->InjectDll(entry.th32ProcessID);
					}
					
				}
				
			}

		}
		Sleep(50);
		cout << "next!!!!" << endl;

	}



	
	
}

