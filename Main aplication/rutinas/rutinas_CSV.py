from PySide2 import QtCore, QtGui, QtWidgets
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

    Time = csv_data[:, indexTime]
    VP = csv_data[:, indexVp]
    EFC = csv_data[:, indexEFC]

    dic_data = dict()
    dic_data['time'] = np.array(Time)
    dic_data['vp'] = np.array(list(map(float, VP)))
    dic_data['efc'] = np.array(list(map(float, EFC)))

    Tiempo = []

    for time_entry in dic_data['time']:
        my_time = str(time_entry)
        t1 = sum(i * j for i, j in zip(list(map(float, my_time.split(':')))[::-1], [1, 60, 3600]))
        Tiempo.append(t1)

    Tiempo = np.array(Tiempo)
    Ts = Tiempo - Tiempo[0]

    dic_data['time'] = Ts
    
    MinVP = float(self.main.EditLVP.text())
    MaxVP = float(self.main.EditUVP.text())
    MinEFC = float(self.main.EditLEFC.text())
    MaxEFC = float(self.main.EditUEFC.text())
    
    FactorVP = 100 / MaxVP - MinVP
    FactorEFC = 100 / MaxEFC - MinEFC

    dic_data['vp'] = (dic_data['vp']-MinVP)*FactorVP
    dic_data['efc'] = (dic_data['efc']-MinEFC)*FactorEFC
 
    print(dic_data)
 
    return dic_data