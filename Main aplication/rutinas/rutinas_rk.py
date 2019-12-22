""" 
[Archivo para definir los metodos de Runge-kutta explicitos y embebidos, en todos los casos se utiliza un algoritmo para el ajuste del tamaño de paso, en el caso de los metodos explicitos se utiliza el metodo de doble paso] 
"""


import numpy as np
from rutinas.metodos_RK import norm


def rk_doble_paso_adaptativo(systema,
                             h_ant,
                             tiempo,
                             tbound,
                             xVectB,
                             entrada,
                             metodo,
                             ordenq,
                             rtol,
                             atol,
                             max_step_increase,
                             min_step_decrease,
                             safety_factor):
    """
    [Funcion para definir y manejar el ajuste del tamaño de paso por el metodo de doble paso para Runge-kutta's explicitos, la funcion esta realizada de forma especifica para trabajar con sistemas de control representados con ecuaciones de espacio de estados]
    
    :param systema: [Representacion del sistema de control]
    :type systema: [LTI]
    :param h_ant: [Tamaño de paso actual]
    :type h_ant: [float]
    :param tiempo: [Tiempo actual]
    :type tiempo: [float]
    :param tbound: [Tiempo maximo de simulacion]
    :type tbound: [float]
    :param xVectB: [Vector de estado]
    :type xVectB: [numpyArray]
    :param entrada: [Valor de entrada al sistema]
    :type entrada: [float]
    :param metodo: [Runge-Kutta a utilizar: RK2, Rk3, etc.]
    :type metodo: [function]
    :param ordenq: [Orden del metodo]
    :type ordenq: [int]
    :param rtol: [Tolerancia relativa]
    :type rtol: [float]
    :param atol: [Tolerancia absoluta]
    :type atol: [float]
    :param max_step_increase: [Maximo incremento del tamaño de paso]
    :type max_step_increase: [float]
    :param min_step_decrease: [Minimo decremento del tamaño de paso]
    :type min_step_decrease: [float]
    :param safety_factor: [Factor de seguridad]
    :type safety_factor: [float]
    """

    while True:
        # Para asegurar el tiempo maximo
        if tiempo + h_ant >= tbound:
            h_ant = tbound - tiempo
            yS, xVectSn = metodo(*systema, xVectB, h_ant, entrada)
            h_est = h_ant
        else:
            # Paso de tamaño regular
            yB, xVectBn = metodo(*systema, xVectB, h_ant, entrada)

            # Dos pasos de tamaño medio
            yS, xVectSn = metodo(*systema, xVectB, h_ant / 2, entrada)
            yS, xVectSn = metodo(*systema, xVectSn, h_ant / 2, entrada)

            # Ajuste del tamaño de paso
            scale = atol + rtol * (np.abs(xVectBn) + np.abs(xVectSn)) / 2
            delta1 = np.abs(xVectBn - xVectSn)
            error_norm = norm(delta1 / scale)

            if error_norm == 0:
                # Incremento maximo dado el bajo error
                h_est = h_ant * max_step_increase
            elif error_norm <= 1:
                # Incremento normal
                h_est = h_ant * min(max_step_increase,
                                    max(1, safety_factor * error_norm**(-1 / (ordenq+1))))
            else:
                # Decremento normal y se vuelve a calcular la salida
                h_ant = h_ant * min(
                    1,
                    max(min_step_decrease, safety_factor * error_norm**(-1 / (ordenq+1))))
                continue
        break
    return h_ant, h_est, yS, xVectSn


def rk_embebido_adaptativo(systema,
                           h_ant,
                           tiempo,
                           tbound,
                           xVectr,
                           entrada,
                           metodo,
                           ordenq,
                           rtol,
                           atol,
                           max_step_increase,
                           min_step_decrease,
                           safety_factor):
    """
    [Funcion para definir y manejar el ajuste del tamaño de paso para Runge-kutta's embebidos, la funcion esta realizada de forma especifica para trabajar con sistemas de control representados con ecuaciones de espacio de estados]
    
    :param systema: [Representacion del sistema de control]
    :type systema: [LTI]
    :param h_ant: [Tamaño de paso actual]
    :type h_ant: [float]
    :param tiempo: [Tiempo actual]
    :type tiempo: [float]
    :param tbound: [Tiempo maximo de simulacion]
    :type tbound: [float]
    :param xVectB: [Vector de estado]
    :type xVectB: [numpyArray]
    :param entrada: [Valor de entrada al sistema]
    :type entrada: [float]
    :param metodo: [Runge-Kutta a utilizar: DOPRI54, RKF45, etc.]
    :type metodo: [function]
    :param ordenq: [Valor del metodo de menor orden]
    :type ordenq: [int]
    :param rtol: [Tolerancia relativa]
    :type rtol: [float]
    :param atol: [Tolerancia absoluta]
    :type atol: [float]
    :param max_step_increase: [Maximo incremento del tamaño de paso]
    :type max_step_increase: [float]
    :param min_step_decrease: [Minimo decremento del tamaño de paso]
    :type min_step_decrease: [float]
    :param safety_factor: [Factor de seguridad]
    :type safety_factor: [float]
    """

    while True:
        # Para asegurar el tiempo maximo
        if tiempo + h_ant >= tbound:
            h_ant = tbound - tiempo
            yr, xr, xtemp = metodo(*systema, xVectr, h_ant, entrada)
            h_est = h_ant
        else:
            # Metodo embebido, la integracion se continua con yr y xr
            yr, xr, xtemp = metodo(*systema, xVectr, h_ant, entrada)

            # Ajuste del tamaño de paso
            scale = atol + np.maximum(np.abs(xVectr), np.abs(xr)) * rtol
            delta1 = np.abs(xr - xtemp)
            error_norm = norm(delta1 / scale)

            if error_norm == 0:
                # Incremento maximo dado el bajo error
                h_est = h_ant * max_step_increase
            elif error_norm <= 1:
                # Incremento normal
                h_est = h_ant * min(max_step_increase,
                                    max(1, safety_factor * error_norm**(-1 / (ordenq+1))))
            else:
                # Decremento normal y se vuelve a calcular la salida
                h_ant = h_ant * min(
                    1,
                    max(min_step_decrease, safety_factor * error_norm**(-1 / (ordenq+1))))
                continue
        break
    return h_ant, h_est, yr, xr