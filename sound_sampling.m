%sampling/aliasing demo using MATLAB's builting sounds

Fs=8192;
Ts=1/Fs;
tvec=[0:Fs*1.5]*Ts;
tone=cos(tvec*2*pi*3000);
sound(tone,Fs)
pause;
sound(tone(1:2:end), Fs/2) %downsampled by a factor of 2
pause;
sound(tone(1:3:end), Fs/3), %downsampled by a factor of 3
pause;
load laughter %also try: handel, chirp, laughter, etc
sound(y,Fs) %original rate (8192Hz)
pause;
sound(y(1:2:end), Fs/2) %downsampled by a factor of 2
pause;
sound(y(1:3:end), Fs/3), %downsampled by a factor of 3


