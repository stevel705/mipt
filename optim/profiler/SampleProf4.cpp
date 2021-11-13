// ConsoleApplication1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>

typedef struct {
	int nKey;
	char szStr[MSIZE];
} TSTRUCT;
#define MCOUNT 1024
int  swap_TSTRUCT(TSTRUCT* pA, TSTRUCT* pB) {
	if (!pA || !pB)
		return 0;
	TSTRUCT nT = *pA;
	*pA = *pB;
	*pB = nT;

	return 1;
}
int main(int argc, char* argv[])
{
	int nC = 0;
	int i, j, k;
	TSTRUCT *pStructs = new TSTRUCT [MCOUNT];
	srand(0);

	for (i = 0; i < MCOUNT; i++) {
		pStructs[i].nKey = rand();
	}	

	int  nTransposal = 0;
	TSTRUCT * p1, *p2;
	do {
		for (nTransposal = k = 0; k < MCOUNT - 1; k++) {
			p1 = &pStructs[k];
			p2 = &pStructs[k + 1];
			if (p1->nKey > p2->nKey) {
				swap_TSTRUCT(&pStructs[k], &pStructs[k + 1]);
				printf("\r%d %d  ", k, k+1);
				nTransposal++;
			}
		}
		printf("\rnTransposal= %d  \n", nTransposal);
	} while (nTransposal);
		
	return nC;
}