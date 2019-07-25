import controlmdf as ctrl
from matplotlib import pyplot as plt 
import numpy as np 

tf = ctrl.tf([1], [1, 1, 1])
tf = ctrl.sample_system(tf, 0.1)
w = np.linspace(0, 4 * np.pi/0.1, 5000)
mag, phase, omega = ctrl.bode(tf,w, dB=True, margins=True)
plt.show()

gainDb = 20 * np.log10(mag)
degPhase = phase * 180.0 / np.pi
    
indGain = np.where(gainDb <= 0)
indPhase = np.where(degPhase <= -180)
print(gainDb[indGain[0][1]])
print(degPhase[indPhase[0][0]])