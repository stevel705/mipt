// ConsoleApplication1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>

#define MSIZE 1024
unsigned char g_Ima_A[1024][1024] = { 0 };
unsigned char g_ImaBin_A[1024][1024 / 8] = { 0 };
unsigned char g_Ima_B[1024][1024] = { 0 };
unsigned char g_ImaBin_B[1024][1024 / 8] = { 0 };
int to_binary(unsigned char *pIma, unsigned char *pImaBin)
{
	if (!pImaBin || !pIma)
		return 0;
	int i, j, k;
	unsigned char uC;
	for (i = 0; i < MSIZE; i++) {
		for (j = 0; j < MSIZE; j += 8) {
			uC = 0;
			for (k = 0; k < 8; k++) {
				uC <<= 1;
				uC |= pIma[i * MSIZE + j + k];
			}
			pImaBin[(i * MSIZE / 8) + (j / 8)] = uC;
		}
	}

	return 1;
}

int to_grey(unsigned char *pImaBin, unsigned char *pIma)
{
	if (!pImaBin || !pIma)
		return 0;
	int i, j;
	unsigned char uC;
	for (i = 0; i < MSIZE; i++) {
		for (j = 0; j < MSIZE; j += 8) {
			uC = pImaBin[(i * MSIZE / 8)  + (j / 8)];
			pIma[i * MSIZE + j + 0] = (uC & 0x80 );
			pIma[i * MSIZE + j + 1] = (uC & 0x40 );
			pIma[i * MSIZE + j + 2] = (uC & 0x20 );
			pIma[i * MSIZE + j + 3] = (uC & 0x10 );
			pIma[i * MSIZE + j + 4] = (uC & 0x08 );
			pIma[i * MSIZE + j + 5] = (uC & 0x04 );
			pIma[i * MSIZE + j + 6] = (uC & 0x02 );
			pIma[i * MSIZE + j + 7] = (uC & 0x01 );			
		}
	}

	return 1;
}

int main(int argc, char* argv[])
{	
	int nC = 0;
	int i, j, k;
	srand(0);
	
	for (j = 0; j < MSIZE; j++) {
		for (k = 0; k < MSIZE; k++) {
			g_Ima_A[j][k] = (unsigned char)(rand() > 256 * 127);
			g_Ima_B[j][k] = (unsigned char)(rand() > 256 * 127);
		}
	}

	for (i = 0; i < 256; i++) {
		to_binary(&g_Ima_A[0][0], &g_ImaBin_A[0][0]);
		to_binary(&g_Ima_B[0][0], &g_ImaBin_B[0][0]);
		for (j = 0; j < MSIZE; j++) {
			for (k = 0; k < MSIZE/8; k++) {
				printf("\r       ");
				printf("\r%d  ", nC++);
				g_ImaBin_A[j][k/8] &= g_ImaBin_B[j][k / 8];
			}
		}
		to_grey(&g_ImaBin_A[0][0], &g_Ima_A[0][0]);
	}
	return nC;
}


