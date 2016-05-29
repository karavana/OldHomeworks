%% Filter definition
[b,a] = butter(2,0.15)

%% My freqz calculation
N = 1024; % Number of points to evaluate at
upp = pi; % Evaluate only up to fs/2
% Create the vector of angular frequencies at one more point.
% After that remove the last element (Nyquist frequency)
w = linspace(0, pi, N+1); 
w(end) = [];
ze = exp(-1j*w); % Pre-compute exponent
H = polyval(b, ze)./polyval(a, ze); % Evaluate transfer function and take the amplitude
Ha = abs(H);
Hdb  = 20*log10(Ha/1); % Convert to dB scale
wn   = w/pi;
% Plot and set axis limits
figure
xlim = ([0 1]);
plot(wn, Hdb,'r')
hold on

[b,a] = butter(5,0.15)

%% My freqz calculation
N = 1024; % Number of points to evaluate at
upp = pi; % Evaluate only up to fs/2
% Create the vector of angular frequencies at one more point.
% After that remove the last element (Nyquist frequency)
w = linspace(0, pi, N+1); 
w(end) = [];
ze = exp(-1j*w); % Pre-compute exponent
H = polyval(b, ze)./polyval(a, ze); % Evaluate transfer function and take the amplitude
Ha = abs(H);
Hdb  = 20*log10(Ha/1); % Convert to dB scale
wn   = w/pi;
% Plot and set axis limits
xlim = ([0 1]);
plot(wn, Hdb,'b')
hold on

[b,a] = butter(20,0.15)

%% My freqz calculation
N = 1024; % Number of points to evaluate at
upp = pi; % Evaluate only up to fs/2
% Create the vector of angular frequencies at one more point.
% After that remove the last element (Nyquist frequency)
w = linspace(0, pi, N+1); 
w(end) = [];
ze = exp(-1j*w); % Pre-compute exponent
H = polyval(b, ze)./polyval(a, ze); % Evaluate transfer function and take the amplitude
Ha = abs(H);
Hdb  = 20*log10(Ha/1); % Convert to dB scale
wn   = w/pi;

xlim = ([0 1]);
plot(wn, Hdb,'g')

title('|H(e^jw)| vs. w');
xlabel('w');
ylabel('|H(e^jw)|');
