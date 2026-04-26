#ifndef __servo_H
#define __servo_H
#include "stm32f4xx.h"

void PWM_Servo_Init(void);
void PWM_Servo_SetCompare1(uint16_t Compare);
void Servo_SetAngle(float Angle);

#endif /* __servo_H */
