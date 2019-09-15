""" 
[Archivo para definir los metodos de Runge-kutta explicitos y embebidos, en todos los casos se utiliza un algoritmo para el ajuste del tamaño de paso, en el caso de los metodos explicitos se utiliza el metodo de doble paso] 
"""


import numpy as np


def norm(x):
    """
    [Funcion para calcular la norma RMS de un vector]
    
    :param x: [Vector]
    :type x: [numpyArray]
    """
    return np.linalg.norm(x) / x.size**0.5


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
            yS, xVectSn = metodo(systema, xVectB, h_ant, entrada)
            h_est = h_ant
        else:
            # Paso de tamaño regular
            yB, xVectBn = metodo(systema, xVectB, h_ant, entrada)

            # Dos pasos de tamaño medio
            yS, xVectSn = metodo(systema, xVectB, h_ant / 2, entrada)
            yS, xVectSn = metodo(systema, xVectSn, h_ant / 2, entrada)

            # Ajuste del tamaño de paso
            scale = atol + rtol * (np.abs(xVectBn) + np.abs(xVectB)) / 2
            delta1 = np.abs(xVectBn - xVectSn)
            error_norm = norm(delta1 / scale)

            if error_norm == 0:
                # Incremento maximo dado el bajo error
                h_est = h_ant * max_step_increase
            elif error_norm < 1:
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


def runge_kutta2(ss, x, h, inputValue):
    """
    [Runge-Kutta de orden 2, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))

    x = x + k2
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


def runge_kutta3(ss, x, h, inputValue):
    """
    [Runge-Kutta de orden 3, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h, (np.dot(ss.A, (x - k1 + np.dot(k2, 2))) + np.dot(ss.B, inputValue)))

    x = x + (np.dot(k1, 1 / 6) + np.dot(k2, 2 / 3) + np.dot(k3, 1 / 6))
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


def heun3(ss, x, h, inputValue):
    """
    [Runge-Kutta Heun de orden 3, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 3))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h, (np.dot(ss.A, (x + np.dot(k2, 2 / 3))) + np.dot(ss.B, inputValue)))

    x = x + (np.dot(k1, 1 / 4) + np.dot(k3, 3 / 4))
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


def ralston3(ss, x, h, inputValue):
    """
    [Runge-Kutta Ralston de orden 3, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h, (np.dot(ss.A, (x + np.dot(k2, 3 / 4))) + np.dot(ss.B, inputValue)))

    x = x + (np.dot(k1, 2 / 9) + np.dot(k2, 1 / 3) + np.dot(k3, 4 / 9))
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


def SSPRK3(ss, x, h, inputValue):
    """
    [Runge-Kutta con preservado de estabilidad fuerte de orden 3, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + k1)) + np.dot(ss.B, inputValue)))
    k3 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 1 / 4) + np.dot(k2, 1 / 4))) + np.dot(ss.B, inputValue)))

    x = x + (np.dot(k1, 1 / 6) + np.dot(k2, 1 / 6) + np.dot(k3, 2 / 3))
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


def runge_kutta4(ss, x, h, inputValue):
    """
    [Runge-Kutta de orden 4, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h, (np.dot(ss.A, (x + np.dot(k2, 1 / 2))) + np.dot(ss.B, inputValue)))
    k4 = np.dot(h, (np.dot(ss.A, (x + k3)) + np.dot(ss.B, inputValue)))

    x = x + (np.dot(k1, 1 / 6) + np.dot(k2, 1 / 3) + np.dot(k3, 1 / 3) +
             np.dot(k4, 1 / 6))
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


def tres_octavos4(ss, x, h, inputValue):
    """
    [Runge-Kutta 3/8 de orden 4, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 3))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h, (np.dot(ss.A,
                           (x + np.dot(k1, -1 / 3) + k2)) + np.dot(ss.B, inputValue)))
    k4 = np.dot(h, (np.dot(ss.A, (x + k1 - k2 + k3)) + np.dot(ss.B, inputValue)))

    x = x + (np.dot(k1, 1 / 8) + np.dot(k2, 3 / 8) + np.dot(k3, 3 / 8) +
             np.dot(k4, 1 / 8))
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


def ralston4(ss, x, h, inputValue):
    """
    [Runge-Kutta Ralston con minimo error de truncamiento de orden 4, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 0.4))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k1, 0.29697761) + np.dot(k2, 0.15875964))) +
                 np.dot(ss.B, inputValue)))
    k4 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 0.21810040) + np.dot(k2, -3.05096516) +
                         np.dot(k3, 3.83286476))) + np.dot(ss.B, inputValue)))

    x = x + (np.dot(k1, 0.17476028) + np.dot(k2, -0.55148066) + np.dot(k3, 1.20553560) +
             np.dot(k4, 0.17118478))
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


def runge_kutta5(ss, x, h, inputValue):
    """
    [Runge-Kutta de orden 5, metodo asignado por defecto, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 4))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 1 / 8) + np.dot(k2, 1 / 8))) + np.dot(ss.B, inputValue)))
    k4 = np.dot(h, (np.dot(ss.A,
                           (x + np.dot(k2, -1 / 2) + k3)) + np.dot(ss.B, inputValue)))
    k5 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k1, -3 / 16) + np.dot(k4, 9 / 16))) +
                 np.dot(ss.B, inputValue)))
    k6 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, -3 / 7) + np.dot(k2, 2 / 7) + np.dot(k3, 12 / 7) +
                 np.dot(k4, -12 / 7) + np.dot(k5, 8 / 7))) + np.dot(ss.B, inputValue)))

    x = x + (np.dot(k1, 7 / 90) + np.dot(k3, 32 / 90) + np.dot(k4, 12 / 90) +
             np.dot(k5, 32 / 90) + np.dot(k6, 7 / 90))
    y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
    return y.item(), x


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
            yr, ytemp, xr, xtemp = metodo(systema, xVectr, h_ant, entrada)
            h_est = h_ant
        else:
            # Metodo embebido, la integracion se continua con yr y xr
            yr, ytemp, xr, xtemp = metodo(systema, xVectr, h_ant, entrada)

            # Ajuste del tamaño de paso
            scale = atol + np.maximum(np.abs(xVectr), np.abs(xr)) * rtol
            delta1 = np.abs(xr - xtemp)
            error_norm = norm(delta1 / scale)

            if error_norm == 0:
                # Incremento maximo dado el bajo error
                h_est = h_ant * max_step_increase
            elif error_norm < 1:
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


def bogacki_shampine23(ss, x, h, inputValue):
    """
    [Runge-Kutta embebido de Bogacki-Shampine 2(3), la integracion se continua con la salida de orden 2, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h, (np.dot(ss.A, (x + np.dot(k2, 3 / 4))) + np.dot(ss.B, inputValue)))
    k4 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 2 / 9) + np.dot(k2, 1 / 3) + np.dot(k3, 4 / 9))) +
                 np.dot(ss.B, inputValue)))

    x3th = x + (np.dot(k1, 2 / 9) + np.dot(k2, 1 / 3) + np.dot(k3, 4 / 9))

    x2th = x + (np.dot(k1, 7 / 24) + np.dot(k2, 1 / 4) + np.dot(k3, 1 / 3) +
                np.dot(k4, 1 / 8))

    y3th = ss.C * x3th + ss.D * inputValue
    y2th = ss.C * x2th + ss.D * inputValue
    return y2th.item(), y3th.item(), x2th, x3th


def fehlberg45(ss, x, h, inputValue):
    """
    [Runge-Kutta embebido de Fehlberg 4(5), la integracion se continua con la salida de orden 4, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 4))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k1, 3 / 32) + np.dot(k2, 9 / 32))) +
                 np.dot(ss.B, inputValue)))
    k4 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 1932 / 2197) + np.dot(k2, -7200 / 2197) +
                         np.dot(k3, 7296 / 2197))) + np.dot(ss.B, inputValue)))
    k5 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 439 / 216) + np.dot(k2, -8) + np.dot(k3, 3680 / 513) +
                 np.dot(k4, -845 / 4104))) + np.dot(ss.B, inputValue)))
    k6 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, -8 / 27) + np.dot(k2, 2) + np.dot(k3, -3544 / 2565) +
                 np.dot(k4, 1859 / 4104) + np.dot(k5, -11 / 40))) +
         np.dot(ss.B, inputValue)))

    x5th = x + (np.dot(k1, 16 / 135) + np.dot(k3, 6656 / 12825) +
                np.dot(k4, 28561 / 56430) + np.dot(k5, -9 / 50) + np.dot(k6, 2 / 55))

    x4th = x + (np.dot(k1, 25 / 216) + np.dot(k3, 1408 / 2565) + np.dot(k4, 2197 / 4104) +
                np.dot(k5, -1 / 5))

    y5th = ss.C * x5th + ss.D * inputValue
    y4th = ss.C * x4th + ss.D * inputValue
    return y4th.item(), y5th.item(), x4th, x5th


def cash_karp45(ss, x, h, inputValue):
    """
    [Runge-Kutta embebido de Cash-Karp 4(5), la integracion se continua con la salida de orden 4, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 5))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k1, 3 / 40) + np.dot(k2, 9 / 40))) +
                 np.dot(ss.B, inputValue)))
    k4 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 3 / 10) + np.dot(k2, -9 / 10) + np.dot(k3, 6 / 5))) +
         np.dot(ss.B, inputValue)))
    k5 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, -11 / 54) + np.dot(k2, 5 / 2) + np.dot(k3, -70 / 27) +
                 np.dot(k4, 35 / 27))) + np.dot(ss.B, inputValue)))
    k6 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 1631 / 55296) + np.dot(k2, 175 / 512) +
                         np.dot(k3, 575 / 13824) + np.dot(k4, 44275 / 110592) +
                         np.dot(k5, 253 / 4096))) + np.dot(ss.B, inputValue)))

    x5th = x + (np.dot(k1, 37 / 378) + np.dot(k3, 250 / 621) + np.dot(k4, 125 / 594) +
                np.dot(k6, 512 / 1771))

    x4th = x + (np.dot(k1, 2825 / 27648) + np.dot(k3, 18575 / 48384) +
                np.dot(k4, 13525 / 55296) + np.dot(k5, 277 / 14336) + np.dot(k6, 1 / 4))

    y5th = ss.C * x5th + ss.D * inputValue
    y4th = ss.C * x4th + ss.D * inputValue
    return y4th.item(), y5th.item(), x4th, x5th


def dopri54(ss, x, h, inputValue):
    """
    [Runge-Kutta embebido de Dormand-Prince 5(4), la integracion se continua con la salida de orden 5, en el metodo se asumio entrada constante, por lo que se descarta t + h*ai]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param h: [Tamaño de paso]
    :type h: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """

    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 5))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k1, 3 / 40) + np.dot(k2, 9 / 40))) +
                 np.dot(ss.B, inputValue)))
    k4 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 44 / 45) + np.dot(k2, -56 / 15) + np.dot(k3, 32 / 9))) +
         np.dot(ss.B, inputValue)))
    k5 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 19372 / 6561) + np.dot(k2, -25360 / 2187) +
                         np.dot(k3, 64448 / 6561) + np.dot(k4, -212 / 729))) +
                 np.dot(ss.B, inputValue)))
    k6 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 9017 / 3168) + np.dot(k2, -355 / 33) +
                         np.dot(k3, 46732 / 5247) + np.dot(k4, 49 / 176) +
                         np.dot(k5, -5103 / 18656))) + np.dot(ss.B, inputValue)))
    k7 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 35 / 384) + np.dot(k3, 500 / 1113) + np.dot(
                    k4, 125 / 192) + np.dot(k5, -2187 / 6784) + np.dot(k6, 11 / 84))) +
         np.dot(ss.B, inputValue)))

    x5th = x + (np.dot(k1, 35 / 384) + np.dot(k3, 500 / 1113) + np.dot(k4, 125 / 192) +
                np.dot(k5, -2187 / 6784) + np.dot(k6, 11 / 84))

    x4th = x + (np.dot(k1, 5179 / 57600) + np.dot(k3, 7571 / 16695) +
                np.dot(k4, 393 / 640) + np.dot(k5, -92097 / 339200) +
                np.dot(k6, 187 / 2100) + np.dot(k7, 1 / 40))

    y5th = ss.C * x5th + ss.D * inputValue
    y4th = ss.C * x4th + ss.D * inputValue
    return y5th.item(), y4th.item(), x5th, x4th