import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import correlate
from scipy.stats import energy_distance
from scipy.integrate import cumtrapz
from scipy import io
from matplotlib import pyplot as plt
import pickle

MatFileMATLAB = io.loadmat('comparisonFiles/Data MATLAB/Simulacion/PIDdmasf9', squeeze_me=True)
MatFileSciLab = io.loadmat('comparisonFiles/Data SciLab/Simulacion/PIDmasfd9', squeeze_me=True)

with open('comparisonFiles/Data LVSCCD/Simulacion/ControladorD9.pkl', 'rb') as f:
    t_lv, yout_lv, yc_lv, set_point, _ = pickle.load(f)

t_lv = np.asarray(t_lv)
yout_lv = np.asarray(yout_lv)
yc_lv = np.asarray(yc_lv)
set_point = np.asarray(set_point)

t_mat = MatFileMATLAB['t']
yout_mat = MatFileMATLAB['yout']
yc_mat = MatFileMATLAB['yc']

t_sci = MatFileSciLab['t']
yout_sci = MatFileSciLab['yout']
yc_sci = MatFileSciLab['yc']

mask1 = t_lv <= max(t_mat)
mask2 = t_lv[mask1] <= max(t_sci)

t_lv = t_lv[mask1][mask2]
yout_lv = yout_lv[mask1][mask2]

funcion1 = interp1d(t_mat, yout_mat)
yout_mat = funcion1(t_lv)

funcion2 = interp1d(t_sci, yout_sci)
yout_sci = funcion2(t_lv)

t_comun = t_lv

index_m = np.argmax([abs(yout_lv - yout_mat), abs(yout_lv - yout_sci)], axis=1)
index_temp = np.argmax([
    abs(yout_lv[index_m[0]] - yout_mat[index_m[0]]),
    abs(yout_lv[index_m[1]] - yout_sci[index_m[1]])
])

index_temp2 = np.argmax([
    yout_lv[index_m[index_temp]],
    yout_mat[index_m[index_temp]],
    yout_sci[index_m[index_temp]]
])

index_temp3 = np.argmin([
    yout_lv[index_m[index_temp]],
    yout_mat[index_m[index_temp]],
    yout_sci[index_m[index_temp]]
])

index_max = index_m[index_temp]
index_min = index_m[index_temp]

if index_temp2 == 0:
    YMAX = yout_lv
elif index_temp2 == 1:
    YMAX = yout_mat
else:
    YMAX = yout_sci

if index_temp3 == 0:
    YMIN = yout_lv
elif index_temp3 == 1:
    YMIN = yout_mat
else:
    YMIN = yout_sci


fig, ax = plt.subplots(figsize=(5.1, 4.2))
ax.plot(t_comun, yout_mat, color="#001C7F", label='MATLAB', linewidth=2)
ax.plot(t_comun, yout_lv, 'r', dashes=[1, 2], label='Laboratorio Virtual', linewidth=3)
ax.plot(t_comun, yout_sci, color="#12711C", dashes=[2, 2], label='SciLab', linewidth=2)
ax.set_title('Controlador PID mas controlador difuso simple', fontsize=11)
ax.legend(loc=7)
ax.grid()

fig.tight_layout()
plt.show()