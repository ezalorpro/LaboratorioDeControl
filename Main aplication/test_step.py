import controlmdf as ctrl
from matplotlib import pyplot as plt 
import numpy as np 

tf = ctrl.tf([1], [1, 1, 1])
tf = ctrl.sample_system(tf, 0.1)

delayV = [0]*(int(1/0.1) + 1)
delayV[0] = 1
fig, ax = plt.subplots()
system_delay = tf * ctrl.TransferFunction([1], delayV, 0.1)
            
ctrl.root_locus(system_delay, figure=fig, ax=ax)
plt.show()