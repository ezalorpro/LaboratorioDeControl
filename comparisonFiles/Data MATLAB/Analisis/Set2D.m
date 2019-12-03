
A = [[ 0.85150898 -0.55915571 -0.03703018];
 [ 0.1851509   0.94408443 -0.00370302];
 [ 0.01851509  0.19440844  0.9996297 ];];

%[ [-0.5, -3, -0.2], [1,  0, 0],[0,1,0] ]
%[ [1], [0],[0] ]
%[ [1, 2, 0.5] ]

B = [[0.1851509 ];
 [0.01851509];
 [0.00185151];];

C =  [[1.11553416 1.71310868 0.47768932]];

D = [[0.11155342]];

Gs = ss(A,B,C,D, 0.2)

[Step_y, Step_t] = step(Gs, 100);
[Impulse_y, Impulse_t] = impulse(Gs, 100);
[MagB, PhaB, FreqB] = bode(Gs);
[GM, GP, Wg, Wp] = margin(Gs);
[Re,Img,FreqN] = nyquist(Gs);
[r, k] = rlocus(Gs);
[MagN, PhaN, WN] = nichols(Gs);


GM = mag2db(GM);
MagB = mag2db(MagB);
MagN = mag2db(MagN);

figure(1)
stairs(Step_t, Step_y)
grid()

figure(2)
stairs(Impulse_t, Impulse_y)
grid()

figure(3)
semilogx(FreqB, squeeze(MagB))
grid()

figure(4)
semilogx(FreqB, squeeze(PhaB))
grid()

figure(5)
plot(squeeze(Re), squeeze(Img),squeeze(Re), squeeze(-Img))
grid()

figure(6)
index = size(r);
for i=1:index(1)
    plot(real(r(i,:)), imag(r(i,:)))
    hold on
end
grid()
hold off

figure(7)
plot(squeeze(PhaN), squeeze(MagN))
grid()

set = 'S2D';
save(strcat(set,'Step'),'Step_t','Step_y')
save(strcat(set,'Imp'),'Impulse_y','Impulse_t')
save(strcat(set,'Bode'),'MagB','PhaB','FreqB')
save(strcat(set,'Margin'),'GM','GP','Wg','Wp')
save(strcat(set,'Nyquist'),'Re','Img','FreqN')
save(strcat(set,'Rlocus'),'r','k')
save(strcat(set,'Nichols'),'MagN','PhaN','WN')