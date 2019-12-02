numerador = [1, 2, 0.5];
denominador = [1 0.5 3, 0.2];

[A,B,C,D] = tf2ss(numerador, denominador)
Gs = ss(A,B,C,D)

% A = [[-0.5 -3.  -0.2]
%  [ 1.   0.   0. ]
%  [ 0.   1.   0. ]]
% 
% B = [[1.]
%  [0.]
%  [0.]]
% 
% C = [[1.  2.  0.5]]
% 
% D = [[0.]]


[S4Step_y, S4Step_t] = step(Gs, 100);
[S4Impulse_y, S4Impulse_t] = impulse(Gs, 100);

figure(1)
plot(S4Step_t, S4Step_y)
grid()

figure(2)
plot(S4Impulse_t, S4Impulse_y)
grid()