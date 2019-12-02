numerador = [0.02561 0.003084 -0.02375];
denominador = [1 -1.968 0.9753];

Gs = tf(numerador, denominador, 0.05, 'InputDelay', 1.5/0.05);

Gs

[S3DStep_y, S3DStep_t] = step(Gs, 35);
[S3DImpulse_y, S3DImpulse_t] = impulse(Gs, 35);

figure(1)
stairs(S3DStep_t, S3DStep_y)
grid()

figure(2)
plot(S3DImpulse_t, S3DImpulse_y)
grid()