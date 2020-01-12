import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import correlate
from scipy.stats import energy_distance
from scipy.integrate import cumtrapz
from scipy import io
from matplotlib import pyplot as plt
import pickle

MatFile = io.loadmat('comparisonFiles/Data SciLab/Analisis/S2Nyquist', squeeze_me=True)

with open('comparisonFiles/Data LVSCCD/Analisis/Set2Nyquist.pkl', 'rb') as f:
    real1, imag1, WN1 = pickle.load(f)

real2, imag2, WN2 = MatFile['Re'], MatFile['Img'], MatFile['FreqN']

mask = WN1 >= min(WN2)
WN1 = WN1[mask]
real1 = real1[mask]
imag1 = imag1[mask]

funcion1 = interp1d(WN2, real2)
real2 = funcion1(WN1)

funcion2 = interp1d(WN2, imag2)
imag2 = funcion2(WN1)

indice = np.argmax(np.abs(imag2 - imag1))
print(f'{"Frecuencia diferencia maxima: ":<38}{WN1[indice]:.4f}')

fig, ax = plt.subplots(figsize=(5.1, 4.2))
ax.plot(real1, imag2, color="#12711C", label='SciLab', linewidth=2)
ax.plot(real1, -imag2, color="#12711C", linewidth=2)
ax.plot([real1[indice]]*2, [imag1[indice], imag2[indice]], color='k', linewidth=3, label='Diferencia maxima')
ax.plot(real1, imag1, 'r', dashes=[1, 2], label='Laboratorio Virtual', linewidth=3)
ax.plot(real1, -imag1, 'r', dashes=[1, 2], linewidth=3)
ax.fill_between(real1, imag1, imag2, alpha=0.4, color="#12711C", label='Area de diferencia')
ax.set_title('Diagrama de Nyquist para el Sistema 2')
ax.legend(loc=7, bbox_to_anchor=(0.67, 0.79), prop={'size': 8})
ax.grid()

axins = ax.inset_axes([0.34, 0.14, 0.3, 0.18])
axins.plot(real1, imag2, color="#12711C", label='SciLab', linewidth=2)
axins.plot(real1, -imag2, color="#12711C", linewidth=2)
axins.plot([real1[indice]]*2, [imag1[indice], imag2[indice]], color='k', linewidth=3, label='Diferencia maxima')
axins.plot(real1, imag1, 'r', dashes=[1, 2], label='Laboratorio Virtual', linewidth=3)
axins.plot(real1, -imag1, 'r', dashes=[1, 2], linewidth=3)
axins.fill_between(real1, imag1, imag2, alpha=0.4, color="#12711C", label='Area de diferencia')
axins.xaxis.set_major_locator(plt.MaxNLocator(2))
# axins.yaxis.major.formatter.set_powerlimits((0, 0))

x1, x2 = real1[indice] - np.abs(imag1[indice] - imag2[indice]), real1[indice] + np.abs(imag1[indice] - imag2[indice])

if imag2[indice] >= imag1[indice]:
    y1, y2 = imag1[indice] - np.abs(imag1[indice] - imag2[indice]), imag2[indice] + np.abs(imag1[indice] - imag2[indice])
else:
    y1, y2 = imag2[indice] - np.abs(imag1[indice] - imag2[indice]), imag1[indice] + np.abs(imag1[indice] - imag2[indice])

axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
ax.indicate_inset_zoom(axins)
axins.grid()

fig.tight_layout()
plt.savefig('comparisonFiles/plots/Analisis/SciLab/ScSet2Nyquist.png', dpi=200)
plt.show()

print(f'{"Error absoluto: ":<38}{np.abs(imag2[indice]-imag1[indice]):.3E}')
print(f'{"Error porcentual maximo: ":<38}{np.abs(np.abs(imag2[indice]-imag1[indice])*100/imag2[indice]):.3E} %')
print(f'{"Distancia de energia: ":<38}{energy_distance(imag1, imag2):.3E}')
print(f'{"Diferencia de areas: ":<38}{np.abs(cumtrapz(imag1, real1)[-1] - cumtrapz(imag2, real1)[-1]):.3E}')
print(f'{"Raiz del Error cuadratico medio: ":<38}{np.sqrt((np.subtract(imag1, imag2)**2).mean()):.3E}')
print(f'{"Distancia euclidiana: ":<38}{np.linalg.norm(imag1-imag2):.3E}')