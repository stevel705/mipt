// ConsoleApplication1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>

double *g_pMem = 0;
int     g_MemSize = 1024;
double function_mem(double fA, int nSkip) {
	g_pMem = new double [g_MemSize] ;
	int i;
	double fP = 0;
	for (i = 0; i < g_MemSize; i++) {
		g_pMem[i] = (double)i;
	}
	for (i = nSkip; i < g_MemSize; i++) {
		fP += g_pMem[i] ;
	}
	
	delete[] g_pMem;
	return fP;
}

int main(int argc, char* argv[])
{
	//getchar();	
	double dC = 0;
	int i, j, k;
	for (i = 0; i < 100; i++) {
		for (j = 0; j < 100; j++) {
			for (k = 0; k < 100; k++) {
				printf("\r       ");
				printf("\r%d %d %d ", i, j, k);				
				dC += function_mem((double)(i + i + k), i);
			}
		}
	}
	return (int)dC;
}

