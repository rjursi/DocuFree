#include <tchar.h>
#include <easyhook.h>
#include <Windows.h>
#include <processenv.h>
#include <iostream>
#include <fstream>
#include <string>
#include <locale>
#include <stdio.h>




BOOL FindInWhiteList(LPCWSTR lpFileName) {
	
	
	HMODULE hm = NULL;
	wchar_t dllPath[_MAX_PATH];
	wchar_t dir[_MAX_PATH];
	wchar_t drive[_MAX_PATH];

	// 초기 dll의 경로르 가져옴
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, L"CreateFileFunctionHook", &hm);
	GetModuleFileName(hm, dllPath, sizeof(dllPath));

	_wsplitpath_s(dllPath, drive, _MAX_PATH, dir, _MAX_PATH, NULL, NULL, NULL, NULL);
	
	wcscat_s(drive, dir);
	wcscat_s(drive, L"whiteList.txt");
	

	OutputDebugString(drive);


	std::wifstream file(drive);
	file.imbue(std::locale("Korean"));

	std::wstring line;
	
	
	BOOL findFlag = FALSE;
	size_t pos;

	
	
	
	while (std::getline(file, line)) {
		
		OutputDebugString(line.c_str());
		OutputDebugString(lpFileName);
		pos = line.find(lpFileName);
		
		if (pos != std::string::npos) {
			OutputDebugString(L"found in text!!");
			findFlag = TRUE;
			break;
		}
		else {
			OutputDebugString(L"not found!");
		}
	}

	file.close();
	return findFlag;

}


BOOL SendFilePath(LPCWSTR lpFileName) {


	HANDLE hPipe;
	DWORD cbToWrite, cbWritten;
	BOOL sendSuccess;
	LPCWSTR pipename = TEXT("\\\\.\\pipe\\docufree");
	
	
	hPipe = CreateFile(
		pipename,
		GENERIC_WRITE,
		0,
		NULL,
		OPEN_EXISTING,
		0,
		NULL
	);

	if (hPipe == INVALID_HANDLE_VALUE) {
		

		OutputDebugString(L"Invalid_HANDLE_VALUE");
		
		
	}
	else {
		cbToWrite = (lstrlen(lpFileName) + 1) * sizeof(WCHAR);

		sendSuccess = WriteFile(
			hPipe,
			lpFileName,
			cbToWrite,
			&cbWritten,
			NULL
		);


		if (!sendSuccess) {
			OutputDebugString(L"failed to send filepath");
			return FALSE;
		}
		OutputDebugString(L"send Success");
		CloseHandle(hPipe);
		return TRUE;
	}

	if (GetLastError() == ERROR_PIPE_BUSY) {
		OutputDebugString(L"Could not open pipe.");
		return FALSE;
	}

	if (!WaitNamedPipe(pipename, 20000)) {
		OutputDebugString(L"timed out");
		return FALSE;
	}	
}



HANDLE CreateFileFunctionsHook(
	LPCWSTR               lpFileName,
	DWORD                 dwDesiredAccess,
	DWORD                 dwShareMode,
	LPSECURITY_ATTRIBUTES lpSecurityAttributes,
	DWORD                 dwCreationDisposition,
	DWORD                 dwFlagsAndAttributes,
	HANDLE                hTemplateFile
) {

	std::wstring fullPathStr = L"";
	std::wstring ext = L"";
	std::wstring chDocFileName = L"";
	BOOL whiteListFlag = FALSE;

	wchar_t chDocPath[200];
	int nFind = 0;

	wchar_t dllPath[_MAX_PATH];
	wchar_t drive[_MAX_PATH];

	HMODULE hm = NULL;


	fullPathStr = lpFileName;

	dwShareMode = FILE_SHARE_READ | FILE_SHARE_WRITE;
	ext = fullPathStr.substr(fullPathStr.find_last_of(L".") + 1);

	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, L"CreateFileFunctionHook", &hm);
	GetModuleFileName(hm, dllPath, sizeof(dllPath));
	

	_wsplitpath_s(dllPath, drive, _MAX_PATH, chDocPath, _MAX_PATH, NULL, NULL, NULL, NULL);
	

	if (ext.find(L"doc") != std::wstring::npos) { // 워드 파일일 경우
		
		OutputDebugString(L"doc!");
		whiteListFlag = FindInWhiteList(lpFileName);

		// if (!whiteListFlag) {
			OutputDebugString(L"Not Found In WhiteLIst!!");
			SendFilePath(lpFileName);
			wcscat_s(drive, chDocPath);
			wcscat_s(drive, L"freeDocuments\\docufree.docx");
			OutputDebugString(drive);
			
			return CreateFileW(drive, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
			
		// }
		

	}else if(ext.find(L"xls") != std::wstring::npos){ // 엑셀 파일일 경우
		OutputDebugString(L"xls");
		whiteListFlag = FindInWhiteList(lpFileName);

		// if (!whiteListFlag) {
			OutputDebugString(L"Not Found In WhiteLIst!!");
			SendFilePath(lpFileName);
			wcscat_s(drive, chDocPath);
			wcscat_s(drive, L"freeDocuments\\docufree.xlsx");
			return CreateFileW(drive, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
			
		// }
		

	}else if (ext.find(L"ppt") != std::wstring::npos) { // 파워포인트 파일일 경우
		OutputDebugString(L"ppt");
		whiteListFlag = FindInWhiteList(lpFileName);
		
		// if (!whiteListFlag) {
			OutputDebugString(L"Not Found In WhiteLIst!!");
			SendFilePath(lpFileName);
			wcscat_s(drive, chDocPath);
			wcscat_s(drive, L"freeDocuments\\docufree.pptx");
			return CreateFileW(drive, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
			
		// }
		
	}
	
	return CreateFileW(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
	
		
	
	
}

extern "C" void __declspec(dllexport)  NativeInjectionEntryPoint(REMOTE_ENTRY_INFO * inRemoteInfo);



void NativeInjectionEntryPoint(REMOTE_ENTRY_INFO* inRemoteInfo) {
	
	
	HOOK_TRACE_INFO hHook = { NULL };

	// 후킹 Install
	
	NTSTATUS result = LhInstallHook(
		GetProcAddress(GetModuleHandle(TEXT("kernel32.dll")), "CreateFileW"),
		CreateFileFunctionsHook,
		NULL,
		&hHook);
	
		
	if (FAILED(result)) {
		
		OutputDebugString(L"Failed to install hook");
	}

	ULONG ACLEntries[1] = { 0 };
	
	LhSetExclusiveACL(ACLEntries, 1, &hHook);
	
	return;
}


BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
		
	HANDLE hThread = NULL;
	
	switch (fdwReason) {

		
		case DLL_PROCESS_ATTACH:
			// 프로세스에 바로 Attach 되었을때
			OutputDebugString(L"Attached!!!");
			break;

		case DLL_PROCESS_DETACH:
			OutputDebugString(L"Detached!!");
			
			break;
	}

	return TRUE;
}