#pragma once

#include <cstdio>
#include <windows.h>
#include <tchar.h>
#include <TlHelp32.h>
#include <iostream>
#include <string>
#include <Psapi.h>
#include <string>
#include "Shlwapi.h"
#include <comdef.h>
#include <easyhook.h>

class DllInjector {
	
private:
	const wchar_t* injectDllPath;
	
	int GetOfficeProcessHandle();

	BOOL SearchDll(HANDLE);
	BOOL InjectDll(DWORD);
	
	
public:
	DllInjector();
	~DllInjector();
	void InjectorStart();
	
	
};