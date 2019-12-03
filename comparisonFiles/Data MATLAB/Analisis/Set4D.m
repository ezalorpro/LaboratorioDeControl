
A = [[ 0.84900356 -0.5634196  -0.03730587];
 [ 0.18652935  0.94226823 -0.00383155];
 [ 0.01915773  0.19610822  0.99974142];];

%[ [-0.5, -3, -0.2], [1,  0, 0],[0,1,0] ]
%[ [1], [0],[0] ]
%[ [1, 2, 0.5] ]

B = [[0.18652935];
 [0.01915773];
 [0.00129292];];

C = [[1.  2.  0.5]];

D = [[0.]];

Gs = ss(A,B,C,D, 0.2)

[Step_y, Step_t] = step(Gs, 100);
[Impulse_y, Impulse_t] = impulse(Gs, 100);
[MagB, PhaB, FreqB] = bode(Gs);
[GM, GP, Wg, Wp] = margin(Gs);
[Re,Img,FreqN] = nyquist(Gs);
[r, k] = rlocus(Gs);
[MagN, PhaN, WN] = nichols(Gs);


GM = mag2db(GM);
Mag = mag2db(MagB);
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

set = 'S4D';
save(strcat(set,'Step'),'Step_t','Step_y')
save(strcat(set,'Imp'),'Impulse_y','Impulse_t')
save(strcat(set,'Bode'),'MagB','PhaB','FreqB')
save(strcat(set,'Margin'),'GM','GP','Wg','Wp')
save(strcat(set,'Nyquist'),'Re','Img','FreqN')
save(strcat(set,'Rlocus'),'r','k')
save(strcat(set,'Nichols'),'MagN','PhaN','WN')