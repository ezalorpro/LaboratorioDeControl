import controlmdf as ctrl
from matplotlib import pyplot as plt 
import numpy as np 

A = [ [-1, -1], [1,  0] ]
B = [ [1], [0] ]
C = [ [0, 1] ]
D = [ [0] ]

kp = 0
ki = 0.16
kd = 0
pid = ctrl.tf([kd+ki+kp, (-2*kd-kp), kd],[1, -1, 0], 0.1)
pid2 = ctrl.tf([kd, kp, ki], [1,0])
print(pid)
ss = ctrl.StateSpace(A, B, C, D, delay=3)
tf = ctrl.TransferFunction([1, 2], [1, 2, 1], delay=3)
tf = ctrl.sample_system(tf, 0.1)
# delay = [0]*(int(3/0.1) + 1)
# delay[0] = 1
# tf = tf * ctrl.tf([1], delay, 0.1)

w = np.linspace(0, 100 * np.pi, 10000)
mag, phase, omega = ctrl.bode(tf, w, margins=True, Plot=False)
real, imag, freq = ctrl.nyquist_plot(tf, w)
plt.plot(real, imag)
plt.plot(real, -imag)
plt.show()
ax1 = plt.subplot(211)
ax1.semilogx(omega, 20 * np.log10(mag))
ax1.grid(True, which="both")

ax2 = plt.subplot(212)
ax2.semilogx(omega, phase * 180.0 / np.pi)
ax2.grid(True, which="both")
plt.show()

T = np.arange(0, 100, 0.1)
t, y = ctrl.step_response(ctrl.feedback(pid*tf), T)
plt.step(t, y[0])
plt.show()