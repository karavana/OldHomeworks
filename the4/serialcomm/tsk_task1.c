/**********************************************************************/
/*                                                                    */
/* File name: tsk_task1.c                                             */
/*                                                                    */
/**********************************************************************/

#include "define.h"
#include "common.h"

/**********************************************************************
 * Definition dedicated to the local functions.
 **********************************************************************/
#define ALARM_TSK1      1

/**********************************************************************
 * ----------------------- GLOBAL VARIABLES ---------------------------
 **********************************************************************/
extern char systemState;			// current state of the system; _WAITING or _OPERATING
extern char transmitBuffer[5];			// holds the bytes to be transmitted/displayed. format: XXYYY
extern char transmitCount;			// index to the transmitBuffer array; the current byte to be transmitted
extern char receiveBuffer[5];			// holds the received bytes: format <x:y>
extern unsigned int temperature;		// the current temperature in 16-bit precision [0-65535]
/**********************************************************************
 * ----------------------- FUNCTION PROTOTYPES ------------------------
 **********************************************************************/
/* Converts an unsigned integer to ASCCI string format */
void convertTempToString();


/**********************************************************************
 * ----------------------- LOCAL FUNCTIONS ----------------------------
 **********************************************************************/
/* Converts an unsigned number, n, to ASCCI string format */
void convertTempToString()
{
	unsigned int n = temperature;
	char i;
	for (i = 1; i >= 0; i--) {
		// transmit buffer is used to hold the resulting string
		// because this value will be transmitted to the PC
		transmitBuffer[i] = (n % 10) + '0';
		n /= 10;
	}
}

/**********************************************************************
 * ------------------------------ TASK1 -------------------------------
 *
 * Prepares the data to be transmitted
 *
 **********************************************************************/
TASK(TASK1) 
{
	float floatTemp;
	char count = 0;
	
	SetRelAlarm(ALARM_TSK1, 600, 50);
	while(1) {

		while (systemState == _WAITING) {
			;
		}
		
		
		WaitEvent(ALARM_EVENT);
		ClearEvent(ALARM_EVENT);
		
		temperature = (unsigned int)60;
		convertTempToString();	// fill the transmitBuffer array
		
		count++;
		if (count == 5) {	// 5 means 250 ms time interval
			count = 0;
			transmitCount = 0;
			TXSTA1bits.TXEN = 1;	// 250 ms passed, enable transmitter
		}
		
	}
	TerminateTask();
}

/* End of File : tsk_task1.c */
