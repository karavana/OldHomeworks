LIST    P=18F8722

#INCLUDE <p18f8722.inc>
CONFIG OSC = HSPLL, FCMEN = OFF, IESO = OFF, PWRT = OFF, BOREN = OFF, WDT = OFF, MCLRE = ON, LPT1OSC = OFF, LVP = OFF, XINST = OFF, DEBUG = OFF

 led_flag        EQU 0X20

ORG     0x00
goto    main

init
movlw h'00'
movwf TRISB
clrf LATB

movlw h'00'
movwf TRISC
clrf  LATC

movlw h'00'
movwf TRISD
clrf LATD

movlw h'00'
movwf led_flag


return


led_task
btfsc led_flag,0
goto state1
goto state0

wait_for_press:
;when button pressed, wait for release
btfss PORTA,4
goto wait_for_press
goto wait_for_release


wait_for_release:
btfsc PORTA,4
goto wait_for_release
goto exit


state0: 
movlw b'00000000'
movwf LATB
movwf LATC
movwf LATD
movlw b'00000001'
movwf LATB
movwf LATC
movwf LATD
movlw b'00000011'
movwf LATB
movwf LATC
movwf LATD
movlw b'00000111'
movwf LATB
movwf LATC
movwf LATD
movlw b'00001111'
movwf LATB
movwf LATC
movwf LATD
movlw b'00011111'
movwf LATB
movwf LATC
movwf LATD
movlw b'00111111'
movwf LATB
movwf LATC
movwf LATD
movlw b'01111111'
movwf LATB
movwf LATC
movwf LATD
movlw b'11111111'
movwf LATB
movwf LATC
movwf LATD

movlw b'01111111'
movwf LATB
movwf LATC
movwf LATD
movlw b'00111111'
movwf LATB
movwf LATC
movwf LATD
movlw b'00011111'
movwf LATB
movwf LATC
movwf LATD
movlw b'00001111'
movwf LATB
movwf LATC
movwf LATD
movlw b'00000111'
movwf LATB
movwf LATC
movwf LATD
movlw b'00000011'
movwf LATB
movwf LATC
movwf LATD
movlw b'00000001'
movwf LATB
movwf LATC
movwf LATD
movlw b'00000000'
movwf LATB
movwf LATC
movwf LATD
bsf led_flag,0
goto wait_for_press

state1:

movlw b'10000000'
movwf LATB
movwf LATC
movwf LATD
movlw b'11000000'
movwf LATB
movwf LATC
movwf LATD
movlw b'11100000'
movwf LATB
movwf LATC
movwf LATD
movlw b'11110000'
movwf LATB
movwf LATC
movwf LATD
movlw b'11111000'
movwf LATB
movwf LATC
movwf LATD
movlw b'11111100'
movwf LATB
movwf LATC
movwf LATD
movlw b'11111110'
movwf LATB
movwf LATC
movwf LATD
movlw b'11111111'
movwf LATB
movwf LATC
movwf LATD

movlw b'11111110'
movwf LATB
movwf LATC
movwf LATD
movlw b'11111100'
movwf LATB
movwf LATC
movwf LATD
movlw b'11111000'
movwf LATB
movwf LATC
movwf LATD
movlw b'11110000'
movwf LATB
movwf LATC
movwf LATD
movlw b'11100000'
movwf LATB
movwf LATC
movwf LATD
movlw b'11000000'
movwf LATB
movwf LATC
movwf LATD
movlw b'10000000'
movwf LATB
movwf LATC
movwf LATD
movlw b'00000000'
movwf LATB
movwf LATC
movwf LATD
bcf led_flag,0
goto wait_for_press


exit:
return


main:
call init
loop:
    call led_task
goto loop
end