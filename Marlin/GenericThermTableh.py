#!/usr/bin/python3

import numpy as np
import math as m
import sys


tbls=[601,602]  # Generates thermistortable_xxx.h

rRef=1e5  # Nominal NTC resistance at T0-25C
rPullup=4700 # Nominal pull up
tZero=273.15 # Constant C->K converson
adcFS=1023 # Full scale at the ADC representing Tthermistor=infinity

# Two constants used to fake data so that reasonable data points can be selected.
TXBETA=3500 # Arbitrary constant used to space out points kept in the table
temperatureStepSize=4 # Arbitrary spacing between temperature points given B=TXBETA


# Functions:
def v2r(vr): # In adc Units to res
    vrs=vr/adcFS
    return ((vrs*rPullup)/(1-vrs))

def r2v(r): # Res to adc units
    return adcFS*r/(r+rPullup)

# Strings:


# Header file documetation
string1=r'''// Generic NTC table {tbl:3d}
// Implements the Steinhart-Hart Equation with
//  Beta defined at compile time
// 1/T=1/T0+1/BETA*ln(R/R0)
// The voltage divider at the ADC input with the thermistor
// and the ln(R/R0) function is taken into account
// in the table that is generated.  The compiler does the math
// to generate the temperatures at selected points.


#ifndef BETA{tbl:3d}
#error Pease define BETA{tbl:3d}  in configuration.h according to thermistor specs.
#endif // BETA{tbl:3d}

#define TZero{tbl:3d} (273.15)

#define TEMPERATURE{tbl:3d}(rval) (short)(1.0/(1.0/(25.0+TZero{tbl:3d})+rval/BETA{tbl:3d})-TZero{tbl:3d}+0.5)

const short temptable_{tbl:3d}[][2] PROGMEM = '''

# format string for one record in the table
stringInstance='   OV({adc:4.0f}),   TEMPERATURE{tbl:3d}({rlvals:4.6f})'

# The range of ADC values to consider:
adcStart=20
adcStop=1020
numResult=adcStop-adcStart+1

adc=np.linspace(adcStart,adcStop,numResult)

rlvals=np.empty(numResult)

for i in range(0,numResult):
    rlvals[i]=np.log(v2r(adc[i])/rRef)
    
#fout=sys.stdout

for tbl in tbls:
    fout=open('thermistortable_{tbl:3d}.h'.format(tbl=tbl),'w')
    print(string1.format(tbl=tbl),'{',file=fout)

    oldTx=340 # Bigger temperature values than this are not useful
    lines=0

    for i in range(0,numResult):
        tx=1.0/(1.0/(25.0+tZero)+rlvals[i]/TXBETA)-tZero+0.5 # Steinhart-Hart
        if tx<oldTx: # Try to space out the temperatures so the bisect routine doesnt get a /0
            oldTx=tx-temperatureStepSize # Chosen by trial and error to yield <100 values
            print('{',stringInstance.format(adc=adc[i],rlvals=rlvals[i],tbl=tbl),'},',file=fout)
            lines+=1
            
    print('};',file=fout)
    print("Liines output=",lines)
fout.close()


testThermistorTable='''
//C program to test generated tables

#include <stdio.h>
#define PROGMEM
#define OV(x) x


#define BETA601 3950
#define BETA602 4100

#include "thermistortable_601.h"
#include "thermistortable_602.h"

int main(int argc, char ** argv)
{
	int i;
	for (i=0;i<sizeof(temptable_601)/sizeof(temptable_601[0]);i++)
		printf("%d %d %d\n",i,temptable_601[i][0],
			temptable_601[i][1]);

	printf("\n\n\n");

	for (i=0;i<sizeof(temptable_602)/sizeof(temptable_602[0]);i++)
		printf("%d %d %d\n",i,temptable_602[i][0],
			temptable_602[i][1]);
	return 0;
}

'''
