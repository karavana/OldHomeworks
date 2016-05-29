/**********************************************************************/
/*                                                                    */
/* File name: common.c                                                */
/*                                                                    */
/* Purpose:   Holds all the global variables and functions required   */
/*            by the tasks                                            */
/*                                                                    */
/**********************************************************************/

#include "define.h"
#include "common.h"

/**********************************************************************
 * ----------------------- GLOBAL VARIABLES ---------------------------
 **********************************************************************/
char systemState = _OPERATING;		// current state of the system; _WAITING or _OPERATING
unsigned int temperature = 5;		
char transmitBuffer[5];			// holds the bytes to be transmitted/displayed. format: XXYYY
char transmitCount;			// index to the transmitBuffer array; the current byte to be transmitted
char receiveBuffer[5];			// holds the received bytes


/**********************************************************************
 * ----------------------- GLOBAL FUNCTIONS ---------------------------
 **********************************************************************/
/* transmits data using serial communication */
void transmitData()
{
	if (transmitCount < 5) {
		TXREG1 = transmitBuffer[transmitCount];
		transmitCount++;
	}
	else {  // all the bytes have been sent
		TXSTA1bits.TXEN = 0;  // disable transmitter, will be enabled again in 250 msecs
	}
}

/* Invoked when receive interrupt occurs; meaning that data is received */
void dataReceived()
{
	unsigned char receivedChar = RCREG1;
	
	if (receivedChar == '$') {  // stop character
		systemState = _WAITING;  // go back to waiting state/mode
	}
}


/* End of File : common.c */
