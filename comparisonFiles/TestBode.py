import control as ctrl
from scipy import io
from matplotlib import pyplot as plt
from scipy.signal import correlate
from scipy.stats import energy_distance
from scipy.integrate import cumtrapz
import numpy as np


def margenes_ganancias(system, mag, phase, omega):
    """
    [Funcion para obtener el margen de ganancia y el margen de fase]
    
    :param system: [Representación del sistema]
    :type system: [LTI]
    :param mag: [Magnitud de la respuesta en frecuencia]
    :type mag: [numpyArray]
    :param phase: [Fase de la respuesta en frecuencia]
    :type phase: [numpyArray]
    :param omega: [Frecuencias utilizadas para la respuesta en frecuencia]
    :type omega: [numpyArray]
    """

    gainDb = 20 * np.log10(mag)
    degPhase = phase * 180.0 / np.pi

    # Transformado la fase a : -360 < phase < 360, para +/- 360  phase -> 0
    comp_phase = np.copy(degPhase)
    degPhase = degPhase - (degPhase / 360).astype(int) * 360

    # Para evitar la deteccion de cruces al llevar las fases al rango -360 < phase < 360
    crossHack1 = np.diff(1 * (degPhase > -183) != 0)
    crossHack2 = np.diff(1 * (degPhase > -177) != 0)
    crossHack = ~crossHack1 * ~crossHack2

    # Deteccion de cruce
    indPhase = np.diff(1 * (gainDb > 0) != 0)
    indGain = np.diff(1 * (degPhase > -180) != 0)
    indGain = indGain * crossHack

    # Calculo de la respuesta en frecuencia para omega = 0 rad/s y pi en caso de ser discreto
    if ctrl.isdtime(system, strict=True):
        zero_freq_response = ctrl.evalfr(system, 1)

        nyquist_freq_response = ctrl.evalfr(system, np.exp(np.pi * 1j))
        nyquistMag = np.abs(nyquist_freq_response)
        nyquistPhase = np.angle(nyquist_freq_response)

        if nyquistPhase * 180.0 / np.pi >= 180:
            nyquistPhase = nyquistPhase - 2 * np.pi

        omega = np.insert(omega, len(omega), np.pi / self.dt)
        gainDb = np.insert(gainDb, len(gainDb), 20 * np.log10(nyquistMag))
        degPhase = np.insert(degPhase, len(degPhase), nyquistPhase * 180.0 / np.pi)

        # Verificando "cruce" por -180 grados para la frecuencia de Nyquist
        if np.isclose(nyquistPhase * 180.0 / np.pi, -180):
            indGain = np.insert(indGain, len(indGain), True)
        else:
            indGain = np.insert(indGain, len(indGain), False)

        # Verificando "cruce" por 0 dB para la frecuencia de Nyquist
        if np.isclose(20 * np.log10(nyquistMag), 0):
            indPhase = np.insert(indPhase, len(indPhase), True)
        else:
            indPhase = np.insert(indPhase, len(indPhase), False)
    else:
        zero_freq_response = ctrl.evalfr(system, 0j)

    omega = np.insert(omega, 0, 0)
    zeroPhase = np.angle(zero_freq_response)
    zeroMag = np.abs(zero_freq_response)
    if zeroPhase * 180.0 / np.pi >= 180:
        zeroPhase = zeroPhase - 2 * np.pi
    gainDb = np.insert(gainDb, 0, 20 * np.log10(zeroMag))
    degPhase = np.insert(degPhase, 0, zeroPhase * 180.0 / np.pi)

    # Verificando "cruce" por -180 grados para omega = 0 rad/s
    if np.isclose(zeroPhase * 180.0 / np.pi, -180):
        indGain = np.insert(indGain, 0, True)
    else:
        indGain = np.insert(indGain, 0, False)

    # Verificando "cruce" por 0 dB para omega = 0 rad/s
    if np.isclose(20 * np.log10(zeroMag), 0):
        indPhase = np.insert(indPhase, 0, True)
    else:
        indPhase = np.insert(indPhase, 0, False)

    # Margen de ganancia
    if len(omega[:-1][indGain]) > 0:
        newGainIndex = np.argmin(np.abs(gainDb[:-1][indGain]))
        omegaGain = omega[:-1][indGain][newGainIndex]
        GainMargin = -gainDb[:-1][indGain][newGainIndex]
    else:
        omegaGain = np.nan
        GainMargin = np.infty

    # Margen de Fase
    if len(omega[:-1][indPhase]) > 0:
        newPhaIndex = min(range(len(degPhase[:-1][indPhase])),
                          key=lambda i: abs(np.abs(degPhase[:-1][indPhase][i]) - 180))
        omegaPhase = omega[:-1][indPhase][newPhaIndex]
        PhaseMargin = 180 + degPhase[:-1][indPhase][newPhaIndex]
    else:
        omegaPhase = np.nan
        PhaseMargin = np.infty

    return GainMargin, PhaseMargin, omegaGain, omegaPhase


MatFile = io.loadmat('comparisonFiles/Data SciLab/Analisis/S1Bode', squeeze_me=True)
Mag2, Pha2, Freq2 = MatFile['MagB'], MatFile['PhaB'], MatFile['FreqB']

MatFile2 = io.loadmat('comparisonFiles/Data SciLab/Analisis/S1Margin', squeeze_me=True)
GM2, GP2, WM2, WP2 = MatFile2['GM'], MatFile2['GP'], MatFile2['Wg'], MatFile2['Wp']

Gs = ctrl.tf([1], [1, 1, 1])
Mag1, Pha1, Freq1 = ctrl.bode(Gs)

if np.any((Pha1 * 180.0 / np.pi) >= 180):
    Pha1 = Pha1 - 2*np.pi

GM1, GP1, WM1, WP1 =  margenes_ganancias(Gs, Mag1, Pha1, Freq1)

Mag1 = 20*np.log10(Mag1)
Pha1 = Pha1 * 180.0 / np.pi

indiceMag = np.argmax(np.abs(Mag2 - Mag1))
indicePha = np.argmax(np.abs(Pha2 - Pha1))
print(f'{"Frecuencia de diferencia maxima Magnitud: ":<38}{Freq2[indiceMag]:.4f}')
print(f'{"Frecuencia de diferencia maxima Phase: ":<38}{Freq2[indicePha]:.4f}\n')



print('Magnitud')
print(f'{"Error absoluto bode: ":<38}{np.abs(Mag2[indiceMag]-Mag1[indiceMag]):.3E}')
# print(f'{"Error porcentual maximo: ":<38}{np.abs(Mag2[indiceMag]-Mag1[indiceMag])*100/Mag2[indiceMag]:.3E} %')
print(f'{"Distancia de energia: ":<38}{energy_distance(Mag1, Mag2):.3E}')
print(f'{"Diferencia de areas: ":<38}{np.abs(cumtrapz(Mag1, Freq2)[-1] - cumtrapz(Mag2, Freq2)[-1]):.3E}')
print(f'{"Raiz del Error cuadratico medio: ":<38}{np.sqrt((np.subtract(Mag1, Mag2)**2).mean()):.3E}')
print(f'{"Distancia euclidiana: ":<38}{np.linalg.norm(Mag1-Mag2):.3E}')
print(f'{"Error absoluto GM: ":<38}{np.abs(GM2-GM1):.3E}')
print(f'{"Error absoluto frecuencia GM: ":<38}{np.abs(WM2-WM1):.3E}\n')

print('Fase')
print(f'{"Error absoluto bode: ":<38}{np.abs(Pha2[indicePha]-Pha1[indicePha]):.3E}')
# print(f'{"Error porcentual maximo: ":<38}{np.abs(Pha2[indicePha]-Pha1[indicePha])*100/Pha2[indicePha]:.3E} %')
print(f'{"Distancia de energia: ":<38}{energy_distance(Pha1, Pha2):.3E}')
print(f'{"Diferencia de areas: ":<38}{np.abs(cumtrapz(Pha1, Freq2)[-1] - cumtrapz(Pha2, Freq2)[-1]):.3E}')
print(f'{"Raiz del Error cuadratico medio: ":<38}{np.sqrt((np.subtract(Pha1, Pha2)**2).mean()):.3E}')
print(f'{"Distancia euclidiana: ":<38}{np.linalg.norm(Pha1-Pha2):.3E}')
print(f'{"Error absoluto margen PM: ":<38}{np.abs(GP2-GP1):.3E}')
print(f'{"Error absoluto frecuencia PM: ":<38}{np.abs(WP2-WP1):.3E}')