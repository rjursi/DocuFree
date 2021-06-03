#include <tchar.h>
#include <easyhook.h>
#include <Windows.h>
#include <processenv.h>
#include <iostream>
#include <fstream>
#include <string>
#include <locale>
#include <stdio.h>
#include <sqlite3.h>
#include <openssl/md5.h>
#include <iomanip>
#include <sstream>



BOOL FindInWhiteList(LPCWSTR lpFileName) {
	
	
	HMODULE hm = NULL;
	wchar_t dllPath[_MAX_PATH];
	wchar_t dir[_MAX_PATH];
	wchar_t drive[_MAX_PATH];

	// 초기 dll의 경로르 가져옴
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, L"CreateFileFunctionHook", &hm);
	GetModuleFileName(hm, dllPath, sizeof(dllPath));

	_wsplitpath_s(dllPath, drive, _MAX_PATH, dir, _MAX_PATH, NULL, NULL, NULL, NULL);
	// dir : PassFilePath.dll 파일 디렉토리 위치
	

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



BOOL UnblockDocuFile(LPCWSTR lpFileName) {
	
	
	std::wstring str_identFile = std::wstring(lpFileName) + L":Zone.Identifier";
	OutputDebugString(str_identFile.c_str());
	
	DeleteFileW(str_identFile.c_str());
	
	
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
	std::wstring str_lpFileName = L"";


	BOOL whiteListFlag = FALSE;

	wchar_t chDocPath[200];
	int nFind = 0;

	wchar_t dllPath[_MAX_PATH];
	wchar_t drive[_MAX_PATH];

	HMODULE hm = NULL;

	str_lpFileName = lpFileName;

	fullPathStr = lpFileName;

	ext = fullPathStr.substr(fullPathStr.find_last_of(L".") + 1);

	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT, L"CreateFileFunctionHook", &hm);
	GetModuleFileName(hm, dllPath, sizeof(dllPath));


	_wsplitpath_s(dllPath, drive, _MAX_PATH, chDocPath, _MAX_PATH, NULL, NULL, NULL, NULL);

	if (str_lpFileName.find(L"docufree") == std::wstring::npos) {
		if (str_lpFileName.find(L"Content.MSO") == std::wstring::npos) {


			if (ext.find(L"doc") != std::wstring::npos) { // 워드 파일일 경우

				OutputDebugString(L"doc!");
				OutputDebugString(lpFileName);

				whiteListFlag = FindInWhiteList(lpFileName);


				if (!whiteListFlag) {
					OutputDebugString(L"Not Found In WhiteLIst!!");

				
					if (str_lpFileName.find(L"~$") == std::wstring::npos) {
						SendFilePath(lpFileName);
						UnblockDocuFile(lpFileName);
						return CreateFileW(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
					}

					/*
					wcscat_s(drive, chDocPath);

					if (ext.compare(L"doc") == 0) {

						if (str_lpFileName.find(L"~$") == std::wstring::npos) {
							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
							return CreateFileW(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
						}
					}

					if (ext.compare(L"docm") == 0) {
						OutputDebugString(L"Real Docm!");
						if (str_lpFileName.find(L"~$") != std::wstring::npos) { // 임시 파일이면
							wcscat_s(drive, L"freeDocuments\\~$docufree.docm");
							
						}
						else {

							wcscat_s(drive, L"freeDocuments\\docufree.docm");
							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
						}
					}
					else if(ext.compare(L"docx") == 0){

						if (str_lpFileName.find(L"~$") != std::wstring::npos) { // 임시 파일이면
							wcscat_s(drive, L"freeDocuments\\~$docufree.docx");
							
						}
						else {

							wcscat_s(drive, L"freeDocuments\\docufree.docx");
							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
						}
					}
					
			
					return CreateFileW(drive, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);


					*/
				}


			}
			else if (ext.find(L"xls") != std::wstring::npos) { // 엑셀 파일일 경우


				OutputDebugString(L"xls");
				OutputDebugString(lpFileName);


				whiteListFlag = FindInWhiteList(lpFileName);

				if (!whiteListFlag) {
					OutputDebugString(L"Not Found In WhiteLIst!!");

					if (str_lpFileName.find(L"~$") == std::wstring::npos) {
						SendFilePath(lpFileName);
						UnblockDocuFile(lpFileName);
						return CreateFileW(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
					}

					/*
					wcscat_s(drive, chDocPath);

					if (ext.compare(L"xls") == 0) {

						if (str_lpFileName.find(L"~$") == std::wstring::npos) {
							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
							return CreateFileW(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
						}
					}


					if (ext.compare(L"xlsm") == 0) {
						if (str_lpFileName.find(L"~$") != std::wstring::npos) {
							wcscat_s(drive, L"freeDocuments\\~$docufree.xlsm");

						}
						else {

							wcscat_s(drive, L"freeDocuments\\docufree.xlsm");
							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
						}
					}
					else if (ext.compare(L"xlsx") == 0) {
						if (str_lpFileName.find(L"~$") != std::wstring::npos) {
							wcscat_s(drive, L"freeDocuments\\~$docufree.xlsx");

						}
						else {

							wcscat_s(drive, L"freeDocuments\\docufree.xlsx");
							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
						}
					}

					
					
					return CreateFileW(drive, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
					*/


				}

			}
			else if (ext.find(L"ppt") != std::wstring::npos) { // 파워포인트 파일일 경우
				OutputDebugString(L"ppt");
				OutputDebugString(lpFileName);

				whiteListFlag = FindInWhiteList(lpFileName);


				if (!whiteListFlag) {
					OutputDebugString(L"Not Found In WhiteLIst!!");

					if (str_lpFileName.find(L"~$") == std::wstring::npos) {
						SendFilePath(lpFileName);
						UnblockDocuFile(lpFileName);
						return CreateFileW(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
					}

					/*
					wcscat_s(drive, chDocPath);



					if (ext.compare(L"ppt") == 0) {
						if (str_lpFileName.find(L"~$") == std::wstring::npos) {

							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
							return CreateFileW(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
						}
						
					}
					if (ext.compare(L"pptm") == 0) {
						if (str_lpFileName.find(L"~$") != std::wstring::npos) {
							wcscat_s(drive, L"freeDocuments\\~$docufree.pptm");

						}
						else {

							wcscat_s(drive, L"freeDocuments\\docufree.pptm");
							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
						}

					}
					else if(ext.compare(L"pptx") == 0){


						if (str_lpFileName.find(L"~$") != std::wstring::npos) {
							wcscat_s(drive, L"freeDocuments\\~$docufree.pptx");

						}
						else {

							wcscat_s(drive, L"freeDocuments\\docufree.pptx");
							SendFilePath(lpFileName);
							UnblockDocuFile(lpFileName);
						}

					}

					

					return CreateFileW(drive, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
					*/
				}

			}
		}
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