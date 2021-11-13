// ConsoleApplication1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <cmath>  

double function(double fA) {
	double fP = pow(fA, 3.000001);
	return fP;
}

int main(int argc, char* argv[])
{
	//getchar();
	double dB = 0;
	double dC = 0;
	int i, j, k;
	for (i = 0; i < 100; i++) {
		for (j = 0; j < 100; j++) {
			for (k = 0; k < 100; k++) {
				printf("\r       ");
				printf("\r%d %d %d ", i, j, k);
				dB += function((double)(i));
				dC += function((double)(i + i + k));
			}
		}
	}
	return (int)dC;
}

