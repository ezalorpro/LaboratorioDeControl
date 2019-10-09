import cProfile
from fuzzRuleProfile import ejecutar

Controlador, error, derror = ejecutar()

cProfile.runctx(
    '''for valores in zip(error, derror):
        Controlador.calcular_valor(valores)''',
    globals(),
    locals(),
    'myProfilingFile.pstats')
