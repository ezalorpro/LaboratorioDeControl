numerador = [3];
denominador = [10 1];

Gs = tf(numerador, denominador);

Gs

[S2Step_y, S2Step_t] = step(Gs, 80);
[S2Impulse_y, S2Impulse_t] = impulse(Gs, 80);

figure(1)
plot(S2Step_t, S2Step_y)
grid()

figure(2)
plot(S2Impulse_t, S2Impulse_y)
grid()