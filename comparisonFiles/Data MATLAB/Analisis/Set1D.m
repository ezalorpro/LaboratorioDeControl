numerador = [0.004833 0.004675];
denominador = [1 -1.895 0.9048];

Gs = tf(numerador, denominador, 0.1);

Gs

[S1DStep_y, S1DStep_t] = step(Gs, 25);
[S1DImpulse_y, S1DImpulse_t] = impulse(Gs, 25);

figure(1)
stairs(S1DStep_t, S1DStep_y)
grid()

figure(2)
plot(S1DImpulse_t, S1DImpulse_y)
grid()