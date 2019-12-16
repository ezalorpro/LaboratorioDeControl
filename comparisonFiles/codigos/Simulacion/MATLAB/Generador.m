t = salida.Time;
yout = salida.Data;
yc = controlador.Data;

save('Pc1', 't', 'yout', 'yc')

subplot(2,1,1)
plot(t,yout)

subplot(2,1,2)
plot(t, yc)
