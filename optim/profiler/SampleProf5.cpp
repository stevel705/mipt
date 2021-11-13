// ConsoleApplication5.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
// strace -c ./a.out 
// sudo perf stat ./a.out

#include <iostream>
#include <cstring>// Добавил либу для strlen

void function_copy(char *pInp, char *pOut) {
	for (int i = 0; i < strlen(pInp); i++) {
		pOut[i] = pInp[i];
	}
	// pOut[i] = 0l // закомментировал

	return;
}

int main(int argc, char* argv[])
{
	//getchar();	
	// Убрал * у szStringOut
	char szStringOut[256], *szString[]={ 
	"string1",
	"string2",
	"string3",
	// ...
	""}; // Поставил ;
	
	int i, j, k;
	for (int i = 0; szString[i][0]; i++) {
		function_copy(szString[i], szStringOut);
	}
	return (int)szStringOut[0];
}

