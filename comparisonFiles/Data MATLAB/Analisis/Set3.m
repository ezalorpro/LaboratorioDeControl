numerador = [1, 2];
denominador = [1 0.5 3];

Gs = tf(numerador, denominador, 'InputDelay', 1.5);

Gs

[S3Step_y, S3Step_t] = step(Gs, 35);
[S3Impulse_y, S3Impulse_t] = impulse(Gs, 35);

figure(1)
plot(S3Step_t, S3Step_y)
grid()

figure(2)
plot(S3Impulse_t, S3Impulse_y)
grid()