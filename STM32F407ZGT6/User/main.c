#include "stm32f4xx.h"                  // Device header
#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "servo.h"
#include "motor.h"


int main(void)
{
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	Uart_Init(9600);
	Delay_Init(168);
	PWM_Servo_Init();
	PWM_Motor_Init();
	while(1)
	{
		Motor_Run();
		delay_ms(1000);
		/*
		Motor_Stop();
		delay_ms(1000);
		*/
		/*
		if(USART_RX_STA)
		{

			PWM_Servo_SetCompare1(1000);
			delay_ms(500);
			PWM_Servo_SetCompare1(1500);
			delay_ms(500);
			USART_RX_STA = 0;
		}
		PWM_Servo_SetCompare1(500);
		*/
	}
}
