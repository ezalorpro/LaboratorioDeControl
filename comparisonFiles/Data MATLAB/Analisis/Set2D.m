numerador = [0.04433 0.04433];
denominador = [1 -0.9704];

Gs = tf(numerador, denominador, 0.3);

Gs

[S2DStep_y, S2DStep_t] = step(Gs, 80);
[S2DImpulse_y, S2DImpulse_t] = impulse(Gs, 80);

figure(1)
stairs(S2DStep_t, S2DStep_y)
grid()

figure(2)
plot(S2DImpulse_t, S2DImpulse_y)
grid()