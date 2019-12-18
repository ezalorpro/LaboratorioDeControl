# import timeit
# from rk45adaptativo import ejecutar
# from matplotlib import pyplot as plt
from numba.pycc import CC
import numpy as np

cc = CC('my_module')

# for i in range(10):
#     # ejecutar(figindex=i + 1, kp=(i+1) / 10, ki=(i+1) / 10, kd=(i+1) / 10)
#     ejecutar()

# plt.show()

# # print(timeit.timeit(ejecutar, number=30)/30)
@cc.export('dopri5', '(f8[::1,:], f8[:,::1], f8[:,::1], f8[:,::1], f8[:,::1], f8, f8)')
def dopri5(A, B, C, D, x, h, inputValue):
    k1 = h * (np.dot(A, x) + np.dot(B,inputValue))
    k2 = h * (np.dot(A, x + k1/5) + B*inputValue)
    k3 = h * (np.dot(A, x + k1*3/40 + k2*9/40) + B*inputValue)
    k4 = h * (np.dot(A, x + k1*44/45 - k2*56/15 + k3*32/9) + B*inputValue)
    k5 = h * (np.dot(A, x + k1*19372/6561 - k2*25360/2187 + k3*64448/6561 - k4*212/729) +
              B*inputValue)
    k6 = h * (np.dot(
        A, x + k1*9017/3168 - k2*355/33 + k3*46732/5247 + k4*49/176 - k5*5103/18656) +
              B*inputValue)
    k7 = h * (
        np.dot(A, x + k1*35/384 + k3*500/1113 + k4*125/192 - k5*2187/6784 + k6*11/84) +
        B*inputValue)

    y5th = np.dot(C, x) + D*inputValue
    x5th = x + (k1*35/384 + k3*500/1113 + k4*125/192 - k5*2187/6784 + k6*11/84)
    x4th = x + (k1*5179/57600 + k3*7571/16695 + k4*393/640 - k5*92097/339200 +
                k6*187/2100 + k7/40)

    return y5th, x5th, x4th

if __name__ == '__main__':
    cc.compile()