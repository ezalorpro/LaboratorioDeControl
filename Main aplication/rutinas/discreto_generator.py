from numba.pycc import CC
import numpy as np


cc = CC('discreto_sim')


@cc.export('ss_discreta', '(f8[::1,:], f8[:,::1], f8[:,::1], f8[:,::1], f8[:,::1], f8, f8)')
def ss_discreta(A, B, C, D, x, _, inputValue):
    """
    [Funcion para calcular la respuesta del sistema por medio de la representacion discreta de las ecuaciones de espacio de estados]
    
    :param ss: [Representacion del sistema]
    :type ss: [LTI]
    :param x: [Vector de estado]
    :type x: [numpyArray]
    :param _: [No importa]
    :type _: [float]
    :param inputValue: [Valor de entrada al sistema]
    :type inputValue: [float]
    """
    y = np.dot(C, x) + D*inputValue
    x = np.dot(A, x) + B*inputValue
    
    return y, x


if __name__ == '__main__':
    cc.compile()