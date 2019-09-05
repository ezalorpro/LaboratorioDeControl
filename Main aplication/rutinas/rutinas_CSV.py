from PySide2 import QtCore, QtGui, QtWidgets
import controlmdf as ctrl
import matplotlib.ticker as mticker
import numpy as np


def procesar_csv(self, csv_data):

    for i, header in enumerate(csv_data[0]):
        if 'time' in header.lower():
            indexTime = i
        if 'vp' in header.lower():
            indexVp = i
        if 'efc' in header.lower():
            indexEFC = i

    csv_data = np.delete(csv_data, 0, 0)

    dic_data = dict()
    dic_data['time'] = np.array(csv_data[:, indexTime])
    dic_data['vp'] = np.array(list(map(float, csv_data[:, indexVp])))
    dic_data['efc'] = np.array(list(map(float, csv_data[:, indexEFC])))

    Tiempo = []

    for time_entry in dic_data['time']:
        my_time = str(time_entry)
        t1 = sum(i * j for i, j in zip(list(map(float, my_time.split(':')))[::-1], [1, 60, 3600]))
        Tiempo.append(t1)

    dic_data['time'] = np.array(Tiempo) - Tiempo[0]

    MinVP = float(self.main.EditLVP.text())
    MaxVP = float(self.main.EditUVP.text())
    MinEFC = float(self.main.EditLEFC.text())
    MaxEFC = float(self.main.EditUEFC.text())

    FactorVP = 100 / MaxVP - MinVP
    FactorEFC = 100 / MaxEFC - MinEFC

    dic_data['vp'] = (dic_data['vp']-MinVP)*FactorVP
    dic_data['efc'] = (dic_data['efc']-MinEFC)*FactorEFC

    _, indices = np.unique(dic_data['vp'], return_index=True)
    indices = np.sort(indices)

    dic_data['time'] = dic_data['time'][indices]
    dic_data['vp'] = dic_data['vp'][indices]
    dic_data['efc'] = dic_data['efc'][indices]

    return dic_data, [indexTime, indexVp, indexEFC, MinVP, MaxVP, MinEFC, MaxEFC]


def calcular_modelo(self,
                    dic_data,
                    indexTime,
                    indexVp,
                    indexEFC,
                    MinVP,
                    MaxVP,
                    MinEFC,
                    MaxEFC):

    y = dic_data['vp']
    t = dic_data['time']

    vpmin = np.min(dic_data['vp'][0])
    vpmax = np.max(dic_data['vp'][-1])
    efcmin = np.min(dic_data['efc'][0])
    efcmax = np.max(dic_data['efc'][-1])

    i_max = np.argmax(np.abs(np.gradient(y)))
    efc_max = np.argmax(np.abs(np.gradient(dic_data['efc'])))

    for index, i in enumerate(y):
        if i >= 0.63 * (vpmax-vpmin) + vpmin:
            indexv = index
            break

    Kc = (vpmax - vpmin)/(efcmax - efcmin)

    slop = (y[i_max] - y[i_max - 1]) / (t[i_max] - t[i_max - 1])
    t0 = t[efc_max]
    t1 = ((vpmin - y[i_max]) / (slop) + t[i_max])
    t2 = t[indexv]
    y1 = vpmin
    y2 = slop * (t2 - t[i_max]) + y[i_max]
    tau = t2 - t1
    anclaT = t[i_max]
    anclaY = y[i_max]

    return Kc, tau, y1, y2, t0, t1, t2, anclaT, anclaY


def entonar_y_graficar(self, csv_data, Kc, tau, y1, y2, t0, t1, t2):
    kp, ki, kd = auto_tuning_method_csv(self, Kc, tau, t1-t0, self.main.csvMetodo.currentText())

    self.main.csvGraphicsView.canvas.axes1.clear()
    self.main.csvGraphicsView.canvas.axes1.plot(csv_data['time'], csv_data['efc'])

    t0_efc = self.main.csvGraphicsView.canvas.axes1.axvline(x=t0,
                                                   color='k',
                                                   linestyle=':',
                                                   zorder=-20)
    t1_efc = self.main.csvGraphicsView.canvas.axes1.axvline(x=t1,
                                                   color='k',
                                                   linestyle=':',
                                                   zorder=-20)
    t2_efc = self.main.csvGraphicsView.canvas.axes1.axvline(x=t2,
                                                   color='k',
                                                   linestyle=':',
                                                   zorder=-20)

    self.main.csvGraphicsView.canvas.axes1.grid(True, which="both", color="lightgray")
    self.main.csvGraphicsView.canvas.axes1.set_title("EFC")
    self.main.csvGraphicsView.canvas.axes1.yaxis.set_major_formatter(
        mticker.FormatStrFormatter("%.1f %%")
    )

    self.main.csvGraphicsView.canvas.axes2.clear()
    self.main.csvGraphicsView.canvas.axes2.plot(csv_data['time'], csv_data['vp'])

    recta, = self.main.csvGraphicsView.canvas.axes2.plot([t1, t2], [y1, y2])

    t0_vp = self.main.csvGraphicsView.canvas.axes2.axvline(x=t0,
                                                   color='k',
                                                   linestyle=':',
                                                   zorder=-20)
    t1_vp = self.main.csvGraphicsView.canvas.axes2.axvline(x=t1,
                                                   color='k',
                                                   linestyle=':',
                                                   zorder=-20)
    t2_vp = self.main.csvGraphicsView.canvas.axes2.axvline(x=t2,
                                                   color='k',
                                                   linestyle=':',
                                                   zorder=-20)

    self.main.csvGraphicsView.canvas.axes2.grid(True, which="both", color="lightgray")
    self.main.csvGraphicsView.canvas.axes2.set_title("Vp")
    self.main.csvGraphicsView.canvas.axes2.yaxis.set_major_formatter(
        mticker.FormatStrFormatter("%.1f %%")
    )
    self.main.csvGraphicsView.canvas.axes2.set_xlabel("tiempo")

    self.main.csvGraphicsView.canvas.draw()
    self.main.csvGraphicsView.toolbar.update()

    actualizar_Datos(self, Kc, t0, t1, t2, kp, ki, kd)
    self.main.pidTiempoSlider.blockSignals(True)
    self.main.pidTiempoSlider.setValue(np.round(1000*(t1-t0)/(t2-t0), 3))
    self.main.pidTiempoLabelValue.setText(str(np.round(t1, 3)))
    self.main.pidTiempoSlider.blockSignals(False)


    return [t0_efc, t1_efc, t2_efc, recta, t0_vp, t1_vp, t2_vp], [Kc, t0, t1, t2, y2, y1]


def calculos_manual(self, GraphObjets, Kc, t0, t1, t2, slop, y1):
    kp, ki, kd = auto_tuning_method_csv(self, Kc, t2-t1, t1-t0, self.main.csvMetodo.currentText())

    GraphObjets[1].set_data(t1, [0, 1])
    GraphObjets[5].set_data(t1, [0, 1])
    new_y2 = slop * (t2 - t1) + y1
    GraphObjets[3].set_data([t1, t2], [y1, new_y2])
    self.main.csvGraphicsView.canvas.draw()
    actualizar_Datos(self, Kc, t0, t1, t2, kp, ki, kd)


def actualizar_Datos(self, Kc, t0, t1, t2, kp, ki, kd):
    Datos = "Modelo:\n"
    Datos += str(ctrl.TransferFunction([Kc], [t2-t1, 1])) + "\n"
    Datos += f"Delay: {t1-t0:.3f}\n"
    Datos += "----------------------------------------------\n"
    Datos += f"Kp: {kp:.4f}\n"
    Datos += f"Ki: {ki:.4f}\n"
    Datos += f"Kd: {kd:.4f}\n"
    self.main.csvdatosTextEdit2.setPlainText(Datos)
    self.main.pidLabelController.setText(
        f" Kc = {Kc:.3f} -- Tau = {t2-t1:.3f} -- Alpha = {t1-t0:.3f}")


def auto_tuning_method_csv(self, k_proceso, tau, alpha, metodo):

    if alpha <= 0.05:
        print('Alfa es demasiado pequeño')
        raise TypeError('Alfa es demasiado pequeño')

    if 'ZN' in metodo:
        if 'P--' in metodo:
            kp = (1/k_proceso) * (tau/alpha)
            ti = np.infty
            td = 0

        if 'PI-' in metodo:
            kp = (0.9/k_proceso) * (tau/alpha)
            ti = alpha * 3.33
            td = 0

        if 'PID' in metodo:
            kp = (1.2/k_proceso) * (tau/alpha)
            ti = alpha * 2
            td = alpha * 0.5

        kp = kp
        ki = kp / ti
        kd = kp * td

    if 'CC' in metodo:
        if 'P--' in metodo:
            kp = (1/k_proceso) * (tau/alpha) * (1 + (1/3) * (alpha/tau))
            ti = np.infty
            td = 0

        if 'PI-' in metodo:
            kp = (1/k_proceso) * (tau/alpha) * (0.9 + (1/12) * (alpha/tau))
            ti = alpha * ((30 + 3 * (alpha/tau)) / (9 + 20 * (alpha/tau)))
            td = 0

        if 'PD-' in metodo:
            kp = ((1/k_proceso) * (tau/alpha) * ((5/4) + (1/6) * (alpha/tau)))
            ti = np.infty
            td = alpha * ((6 - 2 * (alpha/tau)) / (22 + 3 * (alpha/tau)))


        if 'PID' in metodo:
            kp = ((1/k_proceso) * (tau/alpha) * ((4/3) + (1/4) * (alpha/tau)))
            ti = alpha * ((32 + 6 * (alpha/tau)) / (13 + 8 * (alpha/tau)))
            td = alpha * (4 / (11 + 2 * (alpha/tau)))

        kp = kp / 2
        ki = kp / ti
        kd = kp * td

    return kp, ki, kd