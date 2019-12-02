T = 1/5;
W = 15.707963267954021;

valor = evalfr(Gs,exp(j*W*T));

fase = rad2deg(angle(valor))
magnitud = mag2db(abs(valor))