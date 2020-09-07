# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 22:08:43 2020

@author: luise
"""

from datetime import datetime, date, time, timedelta
import numpy as np

fecha1 = datetime(2019,2,21)
fechat= fecha1+timedelta(hours=4)

noise = np.random.randint(100, size=(8761))
acumulador=0
for i in range (0, 8761):
    if(noise[i]==44):
        acumulador=acumulador+1
print(acumulador)