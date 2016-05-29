% Fourier transformation of the series x[n]=cos((2pi/5)*n)
% n is from 0 to 99

clc;
clear all;
close all;

n = 0:99;   % n is 0, 1, 2, ..., 99
x = cos(2 * pi / 10 * n);   % Here we form the series. 
figure;
plot(n, x); % We just plot x[n] vs. n
title('x[n] vs. n Graph');
xlabel('n');
ylabel('x[n]');

% Here we compute DFT of x[n]. Please note the we find X[k]
X = fft(x);
k = 0:length(X) - 1; % k is 0, 1, 2, ..., length(X)
figure;
% Below we plot |X[k]|
% In MATLAB 2013a, we have to call fftshift() after finding magnitude of
% X[k]. In the plotting, notice the impulses. They are at k=40 and k=60. 
% k=40 corresponds to -pi/5 and k=60 corresponds to pi/5.
plot(k, fftshift(abs(X)));
title('|X[k]| vs. k Graph');
xlabel('k');
ylabel('X[k]');

% Here we plot magnitude of DTFT of x[n], namely |X(e^jw)|. 
% Below, we form the w axis.
% k=0 corresponds to -pi, k=99 corresponds to pi-2pi/length(k).
w = -pi:2 * pi / length(k):pi - 2 * pi / length(k);
figure;
% Below, we plot |X(e^jw)| vs w as in the case for |X[k]|. 
plot(w, fftshift(abs(X)));
title('|X(e^jw)| vs. w Graph');
xlabel('w');
ylabel('|X(e^jw)|');

% In the figure, notice that impulses are at -pi/5 (approx. -0.628) and
% pi/5 (approx. 0.628). 
