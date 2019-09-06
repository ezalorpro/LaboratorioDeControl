""" 22 condiciones if para transformar funciones de membresia a otras formas aproximadas """
def update_definicionmf(self, old_mf, definicion, new_mf):
    if old_mf == 'trimf':
        a, b, c = definicion

        if new_mf == 'trimf':
            na, nb, nc = a, b, c
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na, nd = a, c
            nb = (a+b) / 2
            nc = (b+c) / 2
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = b
            sigma = (abs(c) + abs(a)) / 8
            return [sigma, mean], '[sigma, media]'

        if new_mf == 'gauss2mf':
            mean1 = (a+b) / 2
            sigma1 = (abs(c) + abs(a)) / 16
            mean2 = (b+c) / 2
            sigma2 = (abs(c) + abs(a)) / 16
            return [sigma1, mean1, sigma2, mean2], '[sigma1, media1, sigma2, media2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = (a+b) / 2
            nb = (b+c) / 2
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = b
            nc = 10 / (abs(c) + abs(a))
            return [nc, nb], '[a, b] con:\n a como el ancho del sigmoide, puede ser negativo\n b el centro del sigmoide'

        if new_mf == 'dsigmf':
            nb1 = (a+b) / 2
            nc1 = 20 / (abs(c) + abs(a))
            nb2 = (b+c) / 2
            nc2 = -20 / (abs(c) + abs(a))
            return [nc1, nb1, nc2, nb2], '[a1, b1, a2, b2] con:\n b1, b2 como los centros de los sigmoides\n a1, a2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'psigmf':
            nb1 = (a+b) / 2
            nc1 = 20 / (abs(c) + abs(a))
            nb2 = (b+c) / 2
            nc2 = -20 / (abs(c) + abs(a))
            return [nc1, nb1, nc2, nb2], '[a1, b1, a2, b2] con:\n b1, b2 como los centros de los sigmoides\n a1, a2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na, nd = a, c
            nb = (a+b) / 2
            nc = (b+c) / 2
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = abs(c) - abs(a)
            nb = 1 / (a-b)
            nc = b
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'

    if old_mf == 'trapmf':
        a, b, c, d = definicion
        na, nc = a, d
        nb = (c+b) / 2
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'

    if old_mf == 'gaussmf':
        b, a = definicion
        na = a - b*4
        nc = a + b*4
        nb = a
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'

    if old_mf == 'gauss2mf':
        b, a, d, c = definicion
        na = a - b*4
        nc = c + d*4
        nb = (a+c) / 2
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'

    if old_mf == 'smf' or old_mf == 'zmf':
        a, c = definicion
        na = a - (abs(a) + abs(c)) / 4
        nc = c + (abs(a) + abs(c)) / 4
        nb = (a+c) / 2
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'

    if old_mf == 'sigmf':
        c, b = definicion
        na = b - abs(c) * 5
        nb = b
        nc = b + abs(c) * 5
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'

    if old_mf == 'dsigmf':
        b, a, d, c = definicion
        na = a - b*1.25
        nb = (a+c) / 2
        nc = c - d*1.25
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'
    
    if old_mf == 'psigmf':
        b, a, d, c = definicion
        na = a - b*1.25
        nb = (a+c) / 2
        nc = c - d*1.25
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'

    if old_mf == 'pimf':
        a, b, c, d = definicion
        na, nc = a, d
        nb = (c+b) / 2
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'

    if old_mf == 'gbellmf':
        a, b, c = definicion
        na = c - abs(a / c)
        nb = c
        nc = c + abs(a / c)
        return [na, nb, nc], '[a, b, c] con: a <= b <= c'
