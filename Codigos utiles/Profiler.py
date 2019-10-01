import cProfile
from rk4adaptativo import ejecutar

cProfile.runctx('''ejecutar()''', globals(), locals(), 'myProfilingFile.pstats')
