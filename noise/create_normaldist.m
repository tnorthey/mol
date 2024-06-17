
pkg load statistics
A=load('noise.dat');
B=A(1:81);
[xx, nn] = hist(B,10);
H10=[nn', xx'];
save('h10.dat','H10','-ascii')
