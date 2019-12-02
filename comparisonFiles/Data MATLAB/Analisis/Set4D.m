
A = [[ 0.84900356 -0.5634196  -0.03730587];
 [ 0.18652935  0.94226823 -0.00383155];
 [ 0.01915773  0.19610822  0.99974142];];

B = [[0.18652935];
 [0.01915773];
 [0.00129292];];

C = [[1.  2.  0.5]];

D = [[0.]];

Gs = ss(A,B,C,D, 0.2)

[S4DStep_y, S4DStep_t] = step(Gs, 100);
[S4DImpulse_y, S4DImpulse_t] = impulse(Gs, 100);

figure(1)
stairs(S4DStep_t, S4DStep_y)
grid()

figure(2)
plot(S4DImpulse_t, S4DImpulse_y)
grid()