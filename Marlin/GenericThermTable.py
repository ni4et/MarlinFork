#!/usr/bin/python3
import csv
import numpy as np
import math as m
import matplotlib.pyplot as plt
import os
import re

fileSearchPath=(".","data","C:\Work\FLSUN-Marlin\MarlinFork\Marlin")

numResult=50

tis=[]
rls=[]

rRef=1e5
rPullup=4700
tZero=273.15
dacFS=1023
B=3950

def v2r(vr): # In dac Units to res
    vrs=vr/dacFS
    return ((vrs*rPullup)/(1-vrs))

def r2v(r): # Res to dac units
    return dacFS*r/(r+rPullup)


dac=np.linspace(1.0,1021.0,100)

n=dac.size

rlvals=np.empty(n)
t3950=np.empty(n)
t4500=np.empty(n)

for i in range(0,n):
    rlvals[i]=np.log(v2r(dac[i])/rRef)
    t3950[i]=1/(1/(25+tZero)+rlvals[i]/B)-tZero
    t4500[i]=1/(1/(25+tZero)+rlvals[i]/4500)-tZero


    
plt.plot(dac,t3950,'r',label="B3950")
plt.plot(dac,t4500,'g',label="B4500")
plt.grid(True)
plt.legend()
plt.show()


                
    

    
