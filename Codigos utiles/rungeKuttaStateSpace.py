from matplotlib import pyplot as plt
import control as ctrl
import numpy as np 
import sympy

tf = ctrl.tf([1],[1, 1])
t, y = ctrl.step_response(tf)
plt.plot(t, y)

print(tf)

ss = ctrl.tf2ss(tf)
print(ss)

x = np.zeros_like(ss.B)
h = 0.01
total_t = 10
t = np.linspace(0, total_t, int(total_t/h))
u = np.ones_like(t)
result = []
for i, _ in enumerate(t):
    k1 = h * (ss.A * x + ss.B * 1)
    k2 = h * (ss.A * (x+k1/2) + ss.B * 1)
    k3 = h * (ss.A * (x+k2/2) + ss.B * 1)
    k4 = h * (ss.A * (x+k3) + ss.B * 1)
    
    x = x + (1/6)*(k1 + 2*k2 + 2*k3 + k4)
    y = ss.C * x
    result.append(y[0])

plt.plot(t, np.reshape(result, [len(t)]))
plt.show()

