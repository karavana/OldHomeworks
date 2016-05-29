function varargout = soundmixer(varargin)
% soundmixer:	Sound mixing and fx GUI.
%
% Input:   
%
% Output:  
%
% Author:   Jayson Bowen
%           SSLI
%			Dept. of Electrical Engineering
%			University of Washington, Seattle, WA
%
% Date:     09-09-2007
%
% Modification log:
%	09-10-2007, Jayson Bowen:
%       - Changed soundsc to wavplay with scale function so that the code 
%         would block.  This would allow the button to be disabled while
%         playing.
%       - Moved Noise from filter bank to Signal Options.
%       - Added Gain to filter bank.
%       - Added color on activation on various controls.
%       - Added Record and Silence buttons.
%
% GUIDE Generated comments:
% SOUNDMIXER M-file for soundmixer.fig
%      SOUNDMIXER, by itself, creates a new SOUNDMIXER or raises the existing
%      singleton*.
%
%      H = SOUNDMIXER returns the handle to a new SOUNDMIXER or the handle to
%      the existing singleton*.
%
%      SOUNDMIXER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SOUNDMIXER.M with the given input arguments.
%
%      SOUNDMIXER('Property','Value',...) creates a new SOUNDMIXER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before soundmixer_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to soundmixer_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help soundmixer

% Last Modified by GUIDE v2.5 11-Sep-2007 01:08:36

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @soundmixer_OpeningFcn, ...
                   'gui_OutputFcn',  @soundmixer_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  OPENING FUNCTION - Executes just before soundmixer is made visible.
%%
function soundmixer_OpeningFcn(hObject, eventdata, handles, varargin)
    % This function has no output args, see OutputFcn.
    % hObject    handle to figure
    % eventdata  reserved - to be defined in a future version of MATLAB
    % handles    structure with handles and user data (see GUIDATA)
    % varargin   command line arguments to soundmixer (see VARARGIN)

    % Choose default command line output for soundmixer
    handles.output = hObject;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%  GLOBALS - handles.g
    handles.g.FS                 = 22050;        % global sampling frequency

    handles.g.FILT_CLIP_MAX      = 90;           % Max percentage clip
    handles.g.FILT_CLIP_VAL      = 50;           % Default clipping value
    handles.g.FILT_COSMOD_LIM    = [0.01 10];    % [min max] cos freq. for modulation
    handles.g.FILT_COSMOD_VAL    = 2;            % Default cosine modulation frequency in Hz
    handles.g.FILT_HP_FREQ_LIM   = [50 handles.g.FS/3]; % [min max] HP cutoff freq.
    handles.g.FILT_LP_FREQ_LIM   = [50 handles.g.FS/3]; % [min max] LP cutoff freq.
    handles.g.FILT_HP_FREQ_VAL   = 2000;         % Default HP cutoff freq.
    handles.g.FILT_LP_FREQ_VAL   = 500;          % Default LP cutoff freq.
    handles.g.FILT_NOISE_LIM     = [1 100];      % [min max] percentage of noise
    handles.g.FILT_NOISE_VAL     = 50;           % Default percentage of noise
    handles.g.FILT_TIMESCALE_LIM = [0.01 15];    % [min max] timescale factor
    handles.g.FILT_TIMESCALE_VAL = 5;            % Default timescale factor, x times faster
    handles.g.FILT_ECHO_LIM      = [0.01 10];    % [min max] echo delay in seconds
    handles.g.FILT_ECHO_VAL      = 0.15;         % Default echo delay in seconds
    handles.g.FILT_GAIN_LIM      = [0.01 10];    % [min max] gain factor
    handles.g.FILT_GAIN_VAL      = 0.5;          % Default gain factor

    handles.g.COS_FREQ_LIM       = [50 2000];    % [min max] Hz
    handles.g.COS_FREQ_VAL       = 440;          % Hz
    handles.g.COS_AMP_LIM        = [0.01 10];    % [min max] gain factor
    handles.g.COS_AMP_VAL        = 1;            % [min max] gain factor
    handles.g.COS_DUR_LIM        = [0.5 10];     % [min max] length sec
    handles.g.COS_DUR_VAL        = 1;            % sec
    handles.g.REC_DUR_LIM        = [0.5 10];     % [min max] length sec
    handles.g.REC_DUR_VAL        = 2;            % sec

    handles.g.SYS_BUTTON_BG      = get(handles.togSignal, 'BackgroundColor');
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%  Main Mix Data - handles.mix
    handles.mix.wavdata = [];
    handles.mix.Fs      = handles.g.FS;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%  Signal Data - handles.sig
    handles.sig.wavdata = [];
    handles.sig.Fs      = handles.g.FS;
    
    handles.filt.selected = get(handles.rbClip,'Tag');

    % Update handles structure
    guidata(hObject, handles);

    % Init Axes
    set(handles.axMainmix, 'XTick', [], 'YTick', []);
    set(handles.axSignal, 'XTick', [], 'YTick', []);
    set(handles.uipSignal, 'BorderType', 'line', 'BorderWidth', 1, 'HighlightColor', [0 0 0]);
    set(handles.uipMainmix, 'BorderType', 'line', 'BorderWidth', 1, 'HighlightColor', [0 0 0]);

    % Init toggle buttons
    set(handles.togMainmix,'Value', get(handles.togMainmix,'Min'));
    set(handles.togSignal,'Value', get(handles.togSignal,'Max'));
    % Start with signal selected
    set(handles.uipSignal, 'BorderType', 'line', 'BorderWidth', 5, 'HighlightColor', [1 0 0]);
    set(handles.togSignal, 'BackgroundColor', [1 0 0]);

    % Init Filter Selection
    set(handles.rbClip,'Value', get(handles.rbClip,'Max'));
    set(handles.txtFilter, 'String', 'Percentage of signal to clip.');
    set(handles.tbFilter, 'String', num2str(handles.g.FILT_CLIP_VAL));
    set(handles.slFilter, 'Min', 0, 'Max', handles.g.FILT_CLIP_MAX, 'Value', handles.g.FILT_CLIP_VAL);
    
    % UIWAIT makes soundmixer wait for user response (see UIRESUME)
    % uiwait(handles.figure1);

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  OUTPUT FUNCTION - Outputs from this function are returned to the 
%%                    command line.
%%
function varargout = soundmixer_OutputFcn(hObject, eventdata, handles) 
    % varargout  cell array for returning output args (see VARARGOUT);
    % hObject    handle to figure
    % eventdata  reserved - to be defined in a future version of MATLAB
    % handles    structure with handles and user data (see GUIDATA)

    % Get default command line output from handles structure
    varargout{1} = handles.output;



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TOGGLE BUTTON CALLBACK - Filter Signal Toggle
%%
function togSignal_Callback(hObject, eventdata, handles)
    % Hint: get(hObject,'Value') returns toggle state of togSignal
    button_state = get(hObject,'Value');
    if button_state == get(hObject,'Max')
        % toggle button is pressed
        set(handles.togMainmix,'Value', get(handles.togMainmix,'Min'));        
        set(handles.uipMainmix, 'BorderType', 'line', 'BorderWidth', 1, 'HighlightColor', [0 0 0]);
        set(handles.togMainmix, 'Enable', 'on', 'BackgroundColor', handles.g.SYS_BUTTON_BG);

        set(handles.uipSignal, 'BorderType', 'line', 'BorderWidth', 5, 'HighlightColor', [1 0 0]);
        set(handles.togSignal, 'Enable', 'off', 'BackgroundColor', [1 0 0]);

    elseif button_state == get(hObject,'Min')
        % toggle button is not pressed
        set(handles.togMainmix,'Value', get(handles.togMainmix,'Max'));
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TOGGLE BUTTON CALLBACK - Filter Main Mix Toggle
%%
function togMainmix_Callback(hObject, eventdata, handles)
    % Hint: get(hObject,'Value') returns toggle state of togMainmix    
    button_state = get(hObject,'Value');
    if button_state == get(hObject,'Max')
        % toggle button is pressed
        set(handles.togSignal,'Value', get(handles.togSignal,'Min'));
        set(handles.uipSignal, 'BorderType', 'line', 'BorderWidth', 1, 'HighlightColor', [0 0 0]);
        set(handles.togSignal, 'Enable', 'on', 'BackgroundColor', handles.g.SYS_BUTTON_BG);

        set(handles.uipMainmix, 'BorderType', 'line', 'BorderWidth', 5, 'HighlightColor', [1 0 0]);
        set(handles.togMainmix, 'Enable', 'off', 'BackgroundColor', [1 0 0]);
    elseif button_state == get(hObject,'Min')
        % toggle button is not pressed
        set(handles.togSignal,'Value', get(handles.togSignal,'Max'));
    end

    
    
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON GROUP SELECTION CHANGE FUNCTION - Filter Button Group
%%
function uipFilters_SelectionChangeFcn(hObject, eventdata, handles)
    % hObject    handle to button handel
    filtSel = get(hObject, 'Tag');   % Get Tag of selected object
    handles.filt.selected = filtSel;
    guidata(hObject, handles);  % Update handles structure
    set(handles.tbFilter, 'Enable', 'on');
    set(handles.slFilter, 'Enable', 'on');     
    switch filtSel
        case 'rbClip'
            set(handles.txtFilter, 'String', 'Percentage of signal to clip.');
            set(handles.tbFilter, 'String', num2str(handles.g.FILT_CLIP_VAL));
            set(handles.slFilter, 'Min', 0, 'Max', handles.g.FILT_CLIP_MAX, 'Value', handles.g.FILT_CLIP_VAL);                        
        case 'rbCosmodulate'
            set(handles.txtFilter, 'String', 'Frequency in Hz of Cosine modulation');
            set(handles.tbFilter, 'String', num2str(handles.g.FILT_COSMOD_VAL));
            set(handles.slFilter, 'Min', handles.g.FILT_COSMOD_LIM(1), 'Max', handles.g.FILT_COSMOD_LIM(2), 'Value', handles.g.FILT_COSMOD_VAL);
        case 'rbHighpass'
            set(handles.txtFilter, 'String', 'Cutoff Frequency in Hz.');
            set(handles.tbFilter, 'String', num2str(handles.g.FILT_HP_FREQ_VAL));
            set(handles.slFilter, 'Min', handles.g.FILT_HP_FREQ_LIM(1), 'Max', handles.g.FILT_HP_FREQ_LIM(2), 'Value', handles.g.FILT_HP_FREQ_VAL);
        case 'rbLowpass'
            set(handles.txtFilter, 'String', 'Cutoff Frequency in Hz.');
            set(handles.tbFilter, 'String', num2str(handles.g.FILT_LP_FREQ_VAL));
            set(handles.slFilter, 'Min', handles.g.FILT_LP_FREQ_LIM(1), 'Max', handles.g.FILT_LP_FREQ_LIM(2), 'Value', handles.g.FILT_LP_FREQ_VAL);
        case 'rbGain'
            set(handles.txtFilter, 'String', 'Gain factor.');
            set(handles.tbFilter, 'String', num2str(handles.g.FILT_GAIN_VAL));
            set(handles.slFilter, 'Min', handles.g.FILT_GAIN_LIM(1), 'Max', handles.g.FILT_GAIN_LIM(2), 'Value', handles.g.FILT_GAIN_VAL);
%        case 'rbNoise'
%            set(handles.txtFilter, 'String', 'Percentage of Noise.');
%            set(handles.tbFilter, 'String', num2str(handles.g.FILT_NOISE_VAL));
%            set(handles.slFilter, 'Min', handles.g.FILT_NOISE_LIM(1), 'Max', handles.g.FILT_NOISE_LIM(2), 'Value', handles.g.FILT_NOISE_VAL);
        case 'rbReverse'            
            set(handles.txtFilter, 'String', 'No options.');
            set(handles.tbFilter, 'Enable', 'off');
            set(handles.slFilter, 'Enable', 'off');     
        case 'rbTimescale'
            set(handles.txtFilter, 'String', 'Factor to timescale the signal. (5 = five times faster)');
            set(handles.tbFilter, 'String', num2str(handles.g.FILT_TIMESCALE_VAL));
            set(handles.slFilter, 'Min', handles.g.FILT_TIMESCALE_LIM(1), 'Max', handles.g.FILT_TIMESCALE_LIM(2), 'Value', handles.g.FILT_TIMESCALE_VAL);
        case 'rbEcho'
            set(handles.txtFilter, 'String', 'Delay of Echo in seconds.');
            set(handles.tbFilter, 'String', num2str(handles.g.FILT_ECHO_VAL));
            set(handles.slFilter, 'Min', handles.g.FILT_ECHO_LIM(1), 'Max', handles.g.FILT_ECHO_LIM(2), 'Value', handles.g.FILT_ECHO_VAL);
    end

    
    

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Filter Preview
%%
function pbFiltpreview_Callback(hObject, eventdata, handles)
    set(hObject, 'Enable', 'off', 'BackgroundColor', [0 1 0]); pause(0.001);
    if (get(handles.togSignal,'Value') == get(handles.togSignal,'Max'))
        % Filter Signal
        if (~isempty(handles.sig.wavdata))
            y = filterSig(handles.sig.wavdata, handles.g.FS, handles.filt.selected, str2num(get(handles.tbFilter, 'String')));
            if (~isempty(y))
                wavplay(scaleSnd(y), handles.g.FS);
            end
        end        
    elseif (get(handles.togMainmix,'Value') == get(handles.togMainmix,'Max'))
        % Filter Main Mix
        if (~isempty(handles.mix.wavdata))
            y = filterSig(handles.mix.wavdata, handles.g.FS, handles.filt.selected, str2num(get(handles.tbFilter, 'String')));
            if (~isempty(y))
                wavplay(scaleSnd(y), handles.g.FS);
            end
        end        
    end
    set(hObject, 'Enable', 'on', 'BackgroundColor', handles.g.SYS_BUTTON_BG);
    

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Filter Apply
%%
function pbFiltapply_Callback(hObject, eventdata, handles)
    set(hObject, 'Enable', 'off'); pause(0.001);
    if (get(handles.togSignal,'Value') == get(handles.togSignal,'Max'))
        % Filter Signal
        if (~isempty(handles.sig.wavdata))
            y = filterSig(handles.sig.wavdata, handles.g.FS, handles.filt.selected, str2num(get(handles.tbFilter, 'String')));
            if (~isempty(y))
                handles.sig.wavdata = y;
                guidata(hObject, handles);  % Update handles structure
                wavPlot(handles.axSignal, handles.sig.wavdata, handles.g.FS);  % plot waveform
            end
        end        
    elseif (get(handles.togMainmix,'Value') == get(handles.togMainmix,'Max'))
        % Filter Main Mix
        if (~isempty(handles.mix.wavdata))
            y = filterSig(handles.mix.wavdata, handles.g.FS, handles.filt.selected, str2num(get(handles.tbFilter, 'String')));
            if (~isempty(y))
                handles.mix.wavdata = y;
                guidata(hObject, handles);  % Update handles structure
                wavPlot(handles.axMainmix, handles.mix.wavdata, handles.g.FS);  % plot waveform
            end
        end        
    end
    set(hObject, 'Enable', 'on');




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Copy Signal to Main Mix
%%
function pbCopytomix_Callback(hObject, eventdata, handles)
    if (~isempty(handles.sig.wavdata))
        mixlen = length(handles.mix.wavdata);
        siglen = length(handles.sig.wavdata);
        y = zeros(max([mixlen siglen]), 1);
        y(1:mixlen) = handles.mix.wavdata;
        y(1:siglen) = y(1:siglen) + handles.sig.wavdata;
        handles.mix.wavdata = y;
        guidata(hObject, handles);  % Update handles structure
        wavPlot(handles.axMainmix, handles.mix.wavdata, handles.g.FS);  % plot waveform
    end    
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Append Signal to Main Mix
%%
function pbAppendtomix_Callback(hObject, eventdata, handles)
    if (~isempty(handles.sig.wavdata))
        handles.mix.wavdata = [handles.mix.wavdata; handles.sig.wavdata];
        guidata(hObject, handles);  % Update handles structure
        wavPlot(handles.axMainmix, handles.mix.wavdata, handles.g.FS);  % plot waveform
    end    





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Signal Play
%%
function pbSigplay_Callback(hObject, eventdata, handles)
    set(hObject, 'Enable', 'off', 'BackgroundColor', [0 1 0]); pause(0.001);
    if (~isempty(handles.sig.wavdata))
        wavplay(scaleSnd(handles.sig.wavdata), handles.sig.Fs);
    end
    set(hObject, 'Enable', 'on', 'BackgroundColor', handles.g.SYS_BUTTON_BG);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Signal Load WAV File
%%
function pbSigloadwav_Callback(hObject, eventdata, handles)
    y = loadWavFile(handles.g.FS);
    if (~isempty(y))
        handles.sig.wavdata = y;        
        guidata(hObject, handles);  % Update handles structure
        wavPlot(handles.axSignal, handles.sig.wavdata, handles.g.FS);  % plot waveform
    end
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Signal Clear
%%
function pbSigclear_Callback(hObject, eventdata, handles)
    handles.sig.wavdata = [];
    guidata(hObject, handles); % Update handles structure
    axes(handles.axSignal);    
    plot(0);
    set(handles.axSignal, 'XTick', [], 'YTick', []);
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Signal Add Cosine Wave
%%
function pbSigaddcosine_Callback(hObject, eventdata, handles)
    len = str2num(get(handles.tbCosdur, 'String'));
    freq = str2num(get(handles.tbCosfreq, 'String'));
    amp = str2num(get(handles.tbCosamp, 'String'));
    
    t = 0:1/handles.g.FS:len;
    y = cos(2*pi*freq*t)' * amp;
        
    if (isempty(handles.sig.wavdata))
        handles.sig.wavdata = y(:);
    else        
        yy = zeros(1,max([length(handles.sig.wavdata) length(y)]));
        yy(1:length(y)) = y;
        oldsound = yy(1:length(handles.sig.wavdata));
        yy(1:length(handles.sig.wavdata)) = oldsound(:) + handles.sig.wavdata;
        handles.sig.wavdata = yy(:);
    end    
    guidata(hObject, handles);  % Update handles structure
    wavPlot(handles.axSignal, handles.sig.wavdata, handles.g.FS);  % plot waveform

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Signal Record
%%
function pbSigrecord_Callback(hObject, eventdata, handles)
    len = str2num(get(handles.tbSigreclen, 'String'));
    set(hObject, 'Enable', 'off', 'BackgroundColor', [1 0 0]); pause(0.001);
    handles.sig.wavdata = wavrecord(len*handles.g.FS, handles.g.FS);
    set(hObject, 'Enable', 'on', 'BackgroundColor', handles.g.SYS_BUTTON_BG);
    guidata(hObject, handles);  % Update handles structure
    wavPlot(handles.axSignal, handles.sig.wavdata, handles.g.FS);  % plot waveform


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Signal Insert Noise
%%
function pbSignoise_Callback(hObject, eventdata, handles)
    len = str2num(get(handles.tbSigreclen, 'String'));
    handles.sig.wavdata = (rand(len*handles.g.FS, 1)*2)-1; % random from -1 to 1
    guidata(hObject, handles);  % Update handles structure
    wavPlot(handles.axSignal, handles.sig.wavdata, handles.g.FS);  % plot waveform


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Signal Insert Silence
%%
function pbSigsilence_Callback(hObject, eventdata, handles)
    len = str2num(get(handles.tbSigreclen, 'String'));
    handles.sig.wavdata = zeros(len*handles.g.FS, 1);
    guidata(hObject, handles);  % Update handles structure
    wavPlot(handles.axSignal, handles.sig.wavdata, handles.g.FS);  % plot waveform


    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Main Mix Play
%%
function pbMainmixplay_Callback(hObject, eventdata, handles)
    set(hObject, 'Enable', 'off', 'BackgroundColor', [0 1 0]); pause(0.001);
    if (~isempty(handles.mix.wavdata))
        wavplay(scaleSnd(handles.mix.wavdata), handles.mix.Fs);
    end
    set(hObject, 'Enable', 'on', 'BackgroundColor', handles.g.SYS_BUTTON_BG);
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Main Mix Load WAV file
%%
function pbMainmixload_Callback(hObject, eventdata, handles)
    y = loadWavFile(handles.g.FS);
    if (~isempty(y))
        handles.mix.wavdata = y;        
        guidata(hObject, handles);  % Update handles structure
        wavPlot(handles.axMainmix, handles.mix.wavdata, handles.g.FS);  % plot waveform
    end
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Main Mix Clear
%%
function pbMainmixclear_Callback(hObject, eventdata, handles)
    handles.mix.wavdata = [];
    guidata(hObject, handles); % Update handles structure
    axes(handles.axMainmix);    
    plot(0);
    set(handles.axMainmix, 'XTick', [], 'YTick', []);
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  BUTTON CALLBACK - Main Mix Save to File
%%
function pbMainmixsave_Callback(hObject, eventdata, handles)
    if (~isempty(handles.mix.wavdata))
        [filename,pathname] = uiputfile('*.wav', 'Save the sound file');
        if (isequal(filename,0) | isequal(pathname,0))    
        else
            y = handles.mix.wavdata;
            
            % Normalize between -1 and 1, TODO: better normalize function            
            %y = (y / max([abs(min(y)) max(y)]))*0.98; 
            y = scaleSnd(y)*.99; % scale by .99 to prevent clipping warning
            
            wavwrite(y, handles.g.FS, fullfile(pathname,filename));
        end
    end




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  SLIDER CALLBACK - Filter Options Slider
%%
function slFilter_Callback(hObject, eventdata, handles)
    % Hints: get(hObject,'Value') returns position of slider
    %        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    set(handles.tbFilter, 'String', num2str(get(hObject,'Value')));


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  SLIDER CREATE FUNCTION - Filter Options Slider
%%
function slFilter_CreateFcn(hObject, eventdata, handles)
    % Hint: slider controls usually have a light gray background.
    if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor',[.9 .9 .9]);
    end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CALLBACK - Filter Options Textbox
%%
function tbFilter_Callback(hObject, eventdata, handles)
    % Hints: get(hObject,'String') returns contents of tbFilter as text
    %        str2double(get(hObject,'String')) returns contents of tbFilter as a double
    v = str2num(get(hObject, 'String'));
    if (isnumeric(v) && ~isempty(v))
        if (v > get(handles.slFilter, 'Max'))
            v = get(handles.slFilter, 'Max');            
        elseif (v < get(handles.slFilter, 'min'))
            v = get(handles.slFilter, 'Min');
        end        
        set(handles.slFilter, 'Value', v);
        set(hObject, 'String', num2str(v));
    end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CREATE FUNCTION - Filter Options Textbox
%%
function tbFilter_CreateFcn(hObject, eventdata, handles)
    % Hint: edit controls usually have a white background on Windows.
    %       See ISPC and COMPUTER.
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CALLBACK - Signal Add Cosine Frequency
%%
function tbCosfreq_Callback(hObject, eventdata, handles)
    % Hints: get(hObject,'String') returns contents of tbCosfreq as text
    %        str2double(get(hObject,'String')) returns contents of tbCosfreq as a double
    r = handles.g.COS_FREQ_LIM;    
    v = str2num(get(hObject, 'String'));
    if (isnumeric(v) && ~isempty(v))
        if (v > r(2))
            v = r(2);            
        elseif (v < r(1))
            v = r(1);
        end        
        set(hObject, 'String', num2str(v));
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CREATE FUNCTION - Signal Add Cosine Frequency
%%
function tbCosfreq_CreateFcn(hObject, eventdata, handles)
    % Hint: edit controls usually have a white background on Windows.
    %       See ISPC and COMPUTER.
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CALLBACK - Signal Add Cosine Amplitude
%%
function tbCosamp_Callback(hObject, eventdata, handles)
    % Hints: get(hObject,'String') returns contents of tbCosamp as text
    %        str2double(get(hObject,'String')) returns contents of tbCosamp as a double
    r = handles.g.COS_AMP_LIM;    
    v = str2num(get(hObject, 'String'));
    if (isnumeric(v) && ~isempty(v))
        if (v > r(2))
            v = r(2);            
        elseif (v < r(1))
            v = r(1);
        end        
        set(hObject, 'String', num2str(v));
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CREATE FUNCTION - Signal Add Cosine Amplitude
%%
function tbCosamp_CreateFcn(hObject, eventdata, handles)
    % Hint: edit controls usually have a white background on Windows.
    %       See ISPC and COMPUTER.
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CALLBACK - Signal Add Cosine Duration
%%
function tbCosdur_Callback(hObject, eventdata, handles)
    % Hints: get(hObject,'String') returns contents of tbCosdur as text
    %        str2double(get(hObject,'String')) returns contents of tbCosdur as a double
    r = handles.g.COS_DUR_LIM;    
    v = str2num(get(hObject, 'String'));
    if (isnumeric(v) && ~isempty(v))
        if (v > r(2))
            v = r(2);            
        elseif (v < r(1))
            v = r(1);
        end        
        set(hObject, 'String', num2str(v));
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CREATE FUNCTION - Signal Add Cosine Duration
%%
function tbCosdur_CreateFcn(hObject, eventdata, handles)
    % Hint: edit controls usually have a white background on Windows.
    %       See ISPC and COMPUTER.
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CALLBACK - Signal Record Length
%%
function tbSigreclen_Callback(hObject, eventdata, handles)
% Hints: get(hObject,'String') returns contents of tbSigreclen as text
%        str2double(get(hObject,'String')) returns contents of tbSigreclen as a double
    r = handles.g.REC_DUR_LIM;    
    v = str2num(get(hObject, 'String'));
    if (isnumeric(v) && ~isempty(v))
        if (v > r(2))
            v = r(2);            
        elseif (v < r(1))
            v = r(1);
        end        
        set(hObject, 'String', num2str(v));
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  TEXTBOX CREATE FUNCTION - Signal Record Length
%%
function tbSigreclen_CreateFcn(hObject, eventdata, handles)
    % Hint: edit controls usually have a white background on Windows.
    %       See ISPC and COMPUTER.
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  loadWavFile: Load Wave File
%%      Loads a user selected wave file.  Converts stereo to mono and to 
%%      the current global sample rate.
%%
%%  newFs: Sample rate to convert to
%%
function [ y ] = loadWavFile(newFs)
    [filename,pathname] = uigetfile('*.wav', 'Select the sound file');
    if (isequal(filename, 0))
       y = []; %disp('User selected Cancel')
    else        
        [y Fs] = wavread(fullfile(pathname, filename));
        
        % if the sound is stereo, make it mono
        if (size(y,2) > 1)
            y = sum(y,2)/size(y,2);
        end
        
        if (Fs ~= newFs)
            y = convertsamplerate(y, Fs, newFs);
        end        
    end                

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  wavPlot: Plot Waveform
%%
%%  ax: Axes to plot to
%%   y: Wave data
%%  Fs: Sample rate
%%    
function wavPlot(ax, y, Fs)
    t = (0:length(y)-1) / Fs;
    % plot the waveform
    axes(ax);        
    plot(t, y);        
    %ylim([-1 1]);       % set ylim
    xlim(t([1 end]));   % set xlim to the first and last value of t
    set(ax, 'YTick', []);
    xlabel('Time (sec)');       


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  filterSig: Filter Signal
%%
%%        x: Signal to filter
%%  filtSel: Selected Filter (radio button tag name)
%%        
function [ y ] = filterSig(x, Fs, filtSel, filtPar)
    len = length(x);
    if (isnumeric(filtPar))
        switch filtSel
            case 'rbClip'
                m = max([abs(min(x)) abs(max(x))]) * (filtPar/100);
                y = x;
                y(abs(y)>m) = m;                
            case 'rbCosmodulate'
                t = 0:1/Fs:(len-1)/Fs;
                y = x .* cos(2*pi*filtPar*t)';
            case 'rbHighpass'
                [b,a] = butter(3, filtPar/(Fs/2), 'high');
                y = filter(b, a, x);
            case 'rbLowpass'
                [b,a] = butter(3, filtPar/(Fs/2), 'low');
                y = filter(b, a, x);
%            case 'rbNoise'
%                m = max([abs(min(x)) abs(max(x))]) * (filtPar/100);
%                y = x + rand(len,1) * m;
            case 'rbGain'
                y = x * filtPar;
            case 'rbReverse'
                y = flipud(x);
            case 'rbTimescale'
                y = timescale(x, filtPar);
            case 'rbEcho'
                % check to see if we need to zero pad
                if (floor(filtPar*Fs) > len)
                    x = [x; zeros(floor(filtPar*Fs) - len, 1)];
                    len = length(x); % update the length
                end                
                h = [1; zeros(len-1, 1)];
                h(floor(filtPar*Fs)) = .8;  % TODO: change hard coded gain to param
                X = fft(x);
                H = fft(h);
                y = ifft(X.*H);
        end
    else
        y = [];
    end
    
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  convertsamplerate: Converts from one sample rate to another
%%      This function changes the sample rate of the sound x from the old 
%%      samplerate of oldFs to a new sample rate of newFs. 
%%
%%      Example:  
%%      This will change the sampling rate of mySound from 8192 to 44100.
%%      y = changesamplerate(mySound, 8192, 44100)
%%
%%      x: Signal
%%  oldFs: Sample rate of signal
%%  newFs: New sample rate
%%
function [ y ] = convertsamplerate(x, oldFs, newFs)
    [P, Q] = rat(newFs/oldFs);
    y = resample(x, P, Q);
   
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  timescale: Time Scales a signal
%%      This function time-scales the vector x at N times the original 
%%      speed.
%%
%%      Example:  
%%      This will slow the signal x down by a factor of 2/3.
%%      y = timescale(x, 2/3)
%%
%%  x: Signal
%%  N: Scale factor
%%
function [ y ] = timescale(x, N)
    [P, Q] = rat(N);
    %y = resample(x, P, Q);  % this should work??? but it's backwords
    y = resample(x, Q, P);  % need to do this because... explain 

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  scaleSnd: Scale Sound from -1 to 1.  Code from MATLAB soundsc.m.
%%
%%        x: Signal to scale
%%        
function [ y ] = scaleSnd(x)
    % Determine scaling vector, SLIM:
    xmin = min(x(:));
    xmax = max(x(:));
    slim = [xmin xmax];

    % Scale the data so that the limits in
    % SLIM are scaled to the range [-1 +1]
    %
    dx = diff(slim);
    if (dx == 0)
        % Protect against divide-by-zero errors:
        y = zeros(size(x));
    else
        y = (x-slim(1))/dx*2-1;
    end


%% EOF
