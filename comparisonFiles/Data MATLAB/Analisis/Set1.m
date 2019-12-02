numerador = [1];
denominador = [1 1 1];

Gs = tf(numerador, denominador);

[S1Step_y, S1Step_t] = step(Gs, 20);
[S1Impulse_y, S1Impulse_t] = impulse(Gs, 20);

figure(1)
plot(S1Step_t, S1Step_y)
grid()

figure(2)
plot(S1Impulse_t, S1Impulse_y)
grid()