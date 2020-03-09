import numpy as np

# Valores para procesos en tiempo continuo
abs_dif = [9.271E-06, 2.159E-05, 6.380E-03, 3.030E-12, 4.457E-09, 1.117E-05, 4.449E-05, 4.489E-05, 4.473E-12, 1.129E-10, 3.072E-05, 7.125E-04, 4.807E-04, 3.072E-05, 7.125E-04, 2.525E-04, 9.020E-03, 3.272E-03, 2.525E-04, 9.020E-03, 1.625E-02, 1.760E-01, 5.918E-02, 2.926E-01, 1.760E-01, 5.793E-02, 2.283E-03, 1.466E-02, 6.922E-02, 2.283E-03, 1.466E-02, 1.037E+00, 8.484E-02, 7.789E-02, 1.037E+00, 8.484E-02]

perc_dif = [5.865E-02, 1.620E-03, 1.738E+00, 2.877E-10, 1.867E-07, 6.702E-03, 3.385E-03, 3.514E-03, 8.514E-07, 1.717E-05, 7.032E-03, 5.047E-03, 2.062E-04, 1.161E-02, 1.287E-03, 2.062E-04, 1.161E-02, 1.689E-01, 1.955E-01, 8.494E-02, 2.577E-01, 1.955E-01, 8.315E-02, 1.662E+00, 2.053E+00, 1.662E+00, 2.053E+00, 1.414E+00, 1.023E+00, 1.068E+00, 1.414E+00, 1.023E+00]


recm = [1.409E-06, 2.052E-06, 1.278E-03, 1.142E-12, 1.364E-09, 2.026E-06, 4.125E-06, 7.657E-06, 1.557E-12, 5.246E-11, 1.204E-05, 1.339E-04, 1.072E-04, 1.204E-05, 1.339E-04, 6.375E-05, 1.276E-03, 7.010E-04, 6.375E-05, 1.276E-03, 4.593E-04, 2.131E-03, 1.333E-02, 4.593E-04, 2.131E-03, 2.092E-01, 1.641E-02, 1.846E-02, 2.092E-01, 1.641E-02]

# Diferencia absoluta promedio:
cpromedio_abs = sum(abs_dif)/len(abs_dif)

# Diferencia porcentual promedio:
cpromedio_perc = sum(perc_dif)/len(perc_dif)

# Diferencia absoluta promedio:
cpromedio_recm = sum(recm)/len(recm)


# Valores para procesos en tiempo discreto
abs_dif = [8.438E-15, 6.457E-13, 5.895E-14, 1.021E-14, 1.832E-15, 3.916E-14, 3.331E-14, 1.832E-15, 3.893E-03, 3.378E-01, 2.067E-02, 3.893E-03, 4.406E-01, 9.114E-03, 5.692E-01, 4.406E-01, 6.090E-02, 1.624E-02, 5.524E-02, 1.231E-01, 1.454E-01, 4.178E-03, 1.314E-01, 2.284E-03, 1.493E-02, 5.538E-02, 2.284E-03, 9.413E-02, 5.167E-01, 1.346E-01, 9.413E-02]

perc_dif = [8.437E-13, 2.592E-11, 6.456E-12, 1.008E-12, 5.258E-13, 2.352E-11, 2.784E-12, 5.258E-13, 5.135E-03, 5.775E-01, 3.383E-02, 5.135E-03, 1.958E-01, 1.164E-02, 1.039E-02, 1.958E-01, 2.326E-01, 1.688E-01, 2.110E-01, 1.411E-01, 2.087E-01, 3.680E-03, 1.508E-01, 2.026E+00, 2.128E+00, 2.026E+00, 1.302E-01, 1.147E+00, 2.610E-01, 1.302E-01]


recm = [3.472E-15, 4.229E-13, 2.053E-14, 4.687E-15, 5.464E-16, 8.837E-15, 9.464E-15, 5.485E-16, 6.899E-04, 3.636E-02, 3.492E-03, 6.899E-04, 5.350E-02, 1.775E-03, 7.215E-02, 5.350E-02, 4.328E-04, 2.066E-03, 1.184E-02, 4.328E-04, 1.643E-02, 2.490E-02, 1.891E-02, 1.643E-02]

# Diferencia absoluta promedio:
dpromedio_abs = sum(abs_dif)/len(abs_dif)

# Diferencia porcentual promedio:
dpromedio_perc = sum(perc_dif)/len(perc_dif)

# Diferencia absoluta promedio:
dpromedio_recm = sum(recm)/len(recm)

# Salidas
print(f'\nDiferencia absoluta promedio - continuo: {cpromedio_abs:.3E}')
print(f'Diferencia porcentual promedio - continuo: {cpromedio_perc:.3E}')
print(f'RECM promedio - continuo: {cpromedio_recm:.3E}')

print(f'\nDiferencia absoluta promedio - discreto: {dpromedio_abs:.3E}')
print(f'Diferencia porcentual promedio - discreto: {dpromedio_perc:.3E}')
print(f'RECM promedio - discreto: {dpromedio_recm:.3E}')