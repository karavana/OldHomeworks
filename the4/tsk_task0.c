#include "define.h"
#include "LCD.h"

/**********************************************************************
 * Definition dedicated to the local functions.
 **********************************************************************/
#define ALARM_TSK0      0

/**********************************************************************
 * ------------------------------ TASK0 -------------------------------
 *
 * First task of the tutorial.
 *
 **********************************************************************/
TASK(TASK0)
{
  // Wait for the end of the LCD init sequence
  SetRelAlarm(ALARM_TSK0, 1, 350);

  while(1)
  {
      WaitEvent(ALARM_EVENT);
      ClearEvent(ALARM_EVENT);

      ClearLCDScreen();

      LcdPrintString(" XXXXXXXXXXXXXX ", 0, 0);
      LcdPrintString("XXXXXXXXXXXXXXXX", 0, 1);
  }

  //TerminateTask();
}
