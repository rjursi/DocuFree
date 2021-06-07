#include <Windows.h>

#include <cstdio>
#include "DllInjector.h"


int _tmain(int argc, TCHAR* argv[]) {
	DllInjector *dlIInjector = new DllInjector();
	/*
	HWND hConsole = GetConsoleWindow();
	
	ShowWindow(hConsole, SW_HIDE);
	*/
	dlIInjector->InjectorStart();


}