#ifndef _COMMON_H
#define COMMON_H

/**********************************************************************
 * ----------------------- GLOBAL DEFINITIONS -------------------------
 **********************************************************************/

#define X 		1		// the position of Set Value, x, in the receive array
#define Y		3		// the position of Offset Value, y, in the receive array

/* System States */
#define _WAITING	0		// waiting state
#define _OPERATING	1		// operating state

/* Temperature Status */
#define NORMAL		0		// temperature status is NORMAL
#define LOW		1		// temperature status is LOW
#define HIGH		2		// temperature status is HIGH
#define CRITICAL	3		// temperature status is CRITICAL
#define SENSOR		4		// temperature status is SENSOR


/**********************************************************************
 * ----------------------- FUNCTION PROTOTYPES ------------------------
 **********************************************************************/
 /* transmits data using serial communication */
void transmitData();
/* Invoked when receive interrupt occurs; meaning that data is received */
void dataReceived();




#endif

/* End of File : common.h */
