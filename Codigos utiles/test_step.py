import control as ctrl
from matplotlib import pyplot as plt 
import numpy as np 

A = [ [-1, -1], [1,  0] ]
B = [ [1], [0] ]
C = [ [0, 1] ]
D = [ [0] ]

ss = ctrl.ss(A, B, C, D)
tf = ctrl.tf([1], [1, 1, 1])
pid = ctrl.tf([1, 2, 3],[1, 0])

print(ctrl.tf2ss(ctrl.feedback(pid*tf)))
print(ctrl.tf2ss(ctrl.feedback(pid*ss)))

# A = [[-1. -1. -0.]
#  [ 1.  0.  0.]
#  [ 0.  1.  0.]]

# B = [[1.]
#  [0.]
#  [0.]]

# C = [[2. 4. 3.]]

# D = [[1.]]