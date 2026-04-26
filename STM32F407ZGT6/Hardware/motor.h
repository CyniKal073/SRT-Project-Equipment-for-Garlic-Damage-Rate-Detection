#ifndef __motor_H
#define __motor_H 			   	  
#include "stm32f4xx.h"

void PWM_Motor_Init(void);
void Motor_Run(void);
void Motor_Stop(void);

#endif
