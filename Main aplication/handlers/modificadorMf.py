""" 90 condiciones if para transformar funciones de membresia a otras formas aproximadas """


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
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = (a+b) / 2
            sigma1 = (abs(c) + abs(a)) / 16
            mean2 = (b+c) / 2
            sigma2 = (abs(c) + abs(a)) / 16
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = (a+b) / 2
            nb = (b+c) / 2
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = b
            nc = 10 / (abs(c) + abs(a))
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = (a+b) / 2
            nc1 = 20 / (abs(c) + abs(a))
            nb2 = (b+c) / 2
            nc2 = -20 / (abs(c) + abs(a))
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

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

        if new_mf == 'trimf':
            na, nc = a, d
            nb = (c+b) / 2
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na, nb, nc, nd = a, b, c, d
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = (c+b) / 2
            sigma = (abs(d) + abs(a)) / 8
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = b
            sigma1 = (abs(d) + abs(a)) / 16
            mean2 = c
            sigma2 = (abs(d) + abs(a)) / 16
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = b
            nb = c
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = (b+c) / 2
            nc = 10 / (abs(d) + abs(a))
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = b
            nc1 = 20 / (abs(d) + abs(a))
            nb2 = c
            nc2 = -20 / (abs(d) + abs(a))
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na, nd = a, d
            nb = b
            nc = c
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = abs(d) - abs(a)
            nb = 1 / (a - (b+c) / 2)
            nc = (b+c) / 2
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'

    if old_mf == 'gaussmf':
        a, b = definicion

        if new_mf == 'trimf':
            na = a - b*4
            nc = a + b*4
            nb = a
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na = a - b*4
            nb = a - b*2
            nc = a + b*2
            nd = a + b*4
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = a
            sigma = b
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = a - b*2
            sigma1 = b / 2
            mean2 = a + b*2
            sigma2 = b / 2
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = a - b*2
            nb = a + b*2
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = a
            nc = 10 / (abs(a + b*4) + abs(a - b*4))
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = a - b*2
            nc1 = 20 / (abs(a + b*4) + abs(a - b*4))
            nb2 = a + b*2
            nc2 = -20 / (abs(a + b*4) + abs(a - b*4))
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na = a - b*4
            nb = a - b*2
            nc = a + b*2
            nd = a + b*4
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = abs(a + b*4) - abs(a - b*4)
            nb = 1 / (a - b*4 - a)
            nc = a
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'

    if old_mf == 'gauss2mf':
        a, b, c, d = definicion

        if new_mf == 'trimf':
            na = a - b*4
            nc = c + d*4
            nb = (a+c) / 2
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na = a - b*4
            nb = a
            nc = c
            nd = c + d*4
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = (a+c) / 2
            sigma = b * 2
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = a
            sigma1 = b
            mean2 = c
            sigma2 = d
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = a
            nb = c
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = (a+c) / 2
            nc = 10 / (abs(c + d*4) + abs(a - b*4))
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = a
            nc1 = 20 / (abs(c + d*4) + abs(a - b*4))
            nb2 = c
            nc2 = -20 / (abs(c + d*4) + abs(a - b*4))
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na = a - b*4
            nb = a
            nc = c
            nd = c + d*4
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = abs(c + d*4) - abs(a - b*4)
            nb = 1 / (a - b*4 - (a+c) / 2)
            nc = a
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'

    if old_mf == 'smf' or old_mf == 'zmf':
        a, c = definicion

        if new_mf == 'trimf':
            na = a - (abs(a) + abs(c)) / 4
            nc = c + (abs(a) + abs(c)) / 4
            nb = (a+c) / 2
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na = a - (abs(a) + abs(c)) / 4
            nb = a
            nc = c
            nd = c + (abs(a) + abs(c)) / 4
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = (a+c) / 2
            sigma = abs(c - (a+c) / 2) / 2
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = a
            sigma1 = abs(c - (a+c) / 2) / 4
            mean2 = c
            sigma2 = abs(c - (a+c) / 2) / 4
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = a
            nb = c
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = (a+c) / 2
            nc = 10 / (abs(c - (abs(a) + abs(c)) / 4) + abs(a - (abs(a) + abs(c)) / 4))
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = a
            nc1 = 20 / (abs(c - (abs(a) + abs(c)) / 4) + abs(a - (abs(a) + abs(c)) / 4))
            nb2 = c
            nc2 = -20 / (abs(c - (abs(a) + abs(c)) / 4) + abs(a - (abs(a) + abs(c)) / 4))
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na = a - (abs(a) + abs(c)) / 4
            nb = a
            nc = c
            nd = c + (abs(a) + abs(c)) / 4
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = abs(c - (abs(a) + abs(c)) / 4) - abs(a - (abs(a) + abs(c)) / 4)
            nb = 1 / (a - (abs(a) + abs(c)) / 4 - (a+c) / 2)
            nc = a
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'

    if old_mf == 'sigmf':
        b, c = definicion

        if new_mf == 'trimf':
            na = b - abs(c) * 5
            nb = b
            nc = b + abs(c) * 5
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na = b - abs(c) * 5
            nb = b - abs(c) * 2.5
            nc = b + abs(c) * 2.5
            nd = b + abs(c) * 5
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = b
            sigma = (abs(b - abs(c) * 5) + abs(b + abs(c) * 5)) / 8
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = (b - abs(c) * 5 + b) / 2
            sigma1 = (abs(b + abs(c) * 5) + abs(b - abs(c) * 5)) / 16
            mean2 = (b + b + abs(c) * 5) / 2
            sigma2 = (abs(b + abs(c) * 5) + abs(b - abs(c) * 5)) / 16
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = (b - abs(c) * 5 + b) / 2
            nb = (b + b + abs(c) * 5) / 2
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = b
            nc = c
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = (b - abs(c) * 5 + b) / 2
            nc1 = 20 / (abs(b + abs(c) * 5) + abs(b - abs(c) * 5))
            nb2 = (b + b + abs(c) * 5) / 2
            nc2 = -20 / (abs(b + abs(c) * 5) + abs(b - abs(c) * 5))
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na, nd = b - abs(c) * 5, b + abs(c) * 5
            nb = (b - abs(c) * 5 + b) / 2
            nc = (b + b + abs(c) * 5) / 2
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = abs(b + abs(c) * 5) - abs(b - abs(c) * 5)
            nb = 1 / (b - abs(c) * 5 - b)
            nc = b
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'

    if old_mf == 'psigmf':
        a, b, c, d = definicion

        if new_mf == 'trimf':
            na = a - b*1.25
            nb = (a+c) / 2
            nc = c - d*1.25
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na, nd = a - b*1.25, c - d*1.25
            nb = a
            nc = c
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = (a+c) / 2
            sigma = (abs(c - d*1.25) + abs(a - b*1.25)) / 8
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = a
            sigma1 = (abs(c - d*1.25) + abs(a - b*1.25)) / 16
            mean2 = c
            sigma2 = (abs(c - d*1.25) + abs(a - b*1.25)) / 16
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = a
            nb = c
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = (a+c) / 2
            nc = 10 / (abs(c - d*1.25) + abs(a - b*1.25))
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = a
            nc1 = b
            nb2 = c
            nc2 = d
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na, nd = a - b*1.25, c - d*1.25
            nb = a
            nc = c
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = abs(c - d*1.25) - abs(a - b*1.25)
            nb = 1 / (a - b*1.25 - (a+c) / 2)
            nc = (a+c) / 2
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'

    if old_mf == 'pimf':
        a, b, c, d = definicion

        if new_mf == 'trimf':
            na, nc = a, d
            nb = (c+b) / 2
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na, nb, nc, nd = a, b, c, d
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = (c+b) / 2
            sigma = (abs(d) + abs(a)) / 8
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = b
            sigma1 = (abs(d) + abs(a)) / 16
            mean2 = c
            sigma2 = (abs(d) + abs(a)) / 16
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = b
            nb = c
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = (b+c) / 2
            nc = 10 / (abs(d) + abs(a))
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = b
            nc1 = 20 / (abs(d) + abs(a))
            nb2 = c
            nc2 = -20 / (abs(d) + abs(a))
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na, nd = a, d
            nb = b
            nc = c
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = abs(d) - abs(a)
            nb = 1 / (a - (b+c) / 2)
            nc = (b+c) / 2
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'

    if old_mf == 'gbellmf':
        a, b, c = definicion

        if new_mf == 'trimf':
            na = c - abs(a / c)
            nb = c
            nc = c + abs(a / c)
            return [na, nb, nc], '[a, b, c] con: a <= b <= c'

        if new_mf == 'trapmf':
            na, nd = c - abs(a / c), c + abs(a / c)
            nb = (c - abs(a / c) + c) / 2
            nc = (c + c + abs(a / c)) / 2
            return [na, nb, nc, nd], '[a, b, c, d] con: a <= b <= c <= d'

        if new_mf == 'gaussmf':
            mean = c
            sigma = (abs(c + abs(a / c)) + abs(c - abs(a / c))) / 8
            return [mean, sigma], '[media, sigma]'

        if new_mf == 'gauss2mf':
            mean1 = (c - abs(a / c) + c) / 2
            sigma1 = (abs(c + abs(a / c)) + abs(c - abs(a / c))) / 16
            mean2 = (c + c + abs(a / c)) / 2
            sigma2 = (abs(c + abs(a / c)) + abs(c - abs(a / c))) / 16
            return [mean1, sigma1, mean2, sigma2], '[media1, sigma1, media2, sigma2] con: media1 <= media2'

        if new_mf == 'smf' or new_mf == 'zmf':
            na = (c - abs(a / c) + c) / 2
            nb = (c + c + abs(a / c)) / 2
            return [na, nb], '[a, b] siendo a el inicio del cambio \ny b el final del cambio'

        if new_mf == 'sigmf':
            nb = c
            nc = 10 / (abs(c + abs(a / c)) + abs(c - abs(a / c)))
            return [nb, nc], '[a, b] con:\n a como el centro del sigmoide\n b el ancho del sigmoide, puede ser negativo'

        if new_mf == 'psigmf':
            nb1 = (c - abs(a / c) * 2.5 + c) / 2
            nc1 = 20 / (abs(c + abs(a / c)) + abs(c - abs(a / c)))
            nb2 = (c + c + abs(a / c) * 2.5) / 2
            nc2 = -20 / (abs(c + abs(a / c)) + abs(c - abs(a / c)))
            return [nb1, nc1, nb2, nc2], '[a1, b1, a2, b2] con:\n a1, a2 como los centros de los sigmoides\n b1, b2 los anchos de los sigmoides, pueden ser negativos'

        if new_mf == 'pimf':
            na, nd = c - abs(a / c), c + abs(a / c)
            nb = (c - abs(a / c) + c) / 2
            nc = (c + c + abs(a / c)) / 2
            return [na, nb, nc, nd], '[a, b, c, d] con:\na inicio de la subida y b su final por el lado izquierdo \nc inicio de la bajada y d su final por el lado derecho'

        if new_mf == 'gbellmf':
            na = a
            nb = b
            nc = c
            return [na, nb, nc], '[a, b, c] con:\na como el ancho de la camapana\nb pendiente de la campana, puede ser negativa\nc centro de la camapana'