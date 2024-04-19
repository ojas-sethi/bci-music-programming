import numpy as np
import pandas as pd
import sys
import json
import time
from telnetlib import Telnet


# Initializing the arrays required to store the data.
attention_values = np.array([])
meditation_values = np.array([])
delta_values = np.array([])
theta_values = np.array([])
lowAlpha_values = np.array([])
highAlpha_values = np.array([])
lowBeta_values = np.array([])
highBeta_values = np.array([])
lowGamma_values = np.array([])
highGamma_values = np.array([])
blinkStrength_values = np.array([])
time_array = np.array([])




start=time.perf_counter()

i=0
tn=Telnet('localhost',13854)
tn.write('{"enableRawOutput": false, "format": "Json"}'.encode('utf-8'))
while True:
	line= tn.read_until(b'\r')
	print(line)
	time.sleep(1)



