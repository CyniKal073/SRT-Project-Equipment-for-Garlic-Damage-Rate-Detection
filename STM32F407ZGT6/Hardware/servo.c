#include "stm32f4xx.h"                  // Device header

void PWM_Servo_Init()
{
	RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM14, ENABLE);
	GPIO_PinAFConfig(GPIOA, GPIO_PinSource7, GPIO_AF_TIM14);
	
	GPIO_InitTypeDef GPIO_InitStructure = {0};   //PA1_GPIO配置
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_7;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;  //开复用推挽由片上外设控制
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;
	GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;
	GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	//TIM_InternalClockConfig(TIM2);  //以内部时钟为时基单元时钟

	
    TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStruct = {0};  //选择时基单元
    TIM_TimeBaseInitStruct.TIM_ClockDivision = TIM_CKD_DIV1;
    TIM_TimeBaseInitStruct.TIM_CounterMode = TIM_CounterMode_Up;
    TIM_TimeBaseInitStruct.TIM_Period = 20000-1;     //ARR
    TIM_TimeBaseInitStruct.TIM_Prescaler = 84-1;   //PSC
    TIM_TimeBaseInitStruct.TIM_RepetitionCounter = 0;
    TIM_TimeBaseInit(TIM14, &TIM_TimeBaseInitStruct);
	
	TIM_OCInitTypeDef TIM_OCInitStruct = {0};
    TIM_OCStructInit(&TIM_OCInitStruct);
    TIM_OCInitStruct.TIM_OCMode = TIM_OCMode_PWM1;
    TIM_OCInitStruct.TIM_OCPolarity = TIM_OCPolarity_High;
    TIM_OCInitStruct.TIM_OutputState = TIM_OutputState_Enable;
    TIM_OCInitStruct.TIM_Pulse = 0;   //CCR
    TIM_OC1Init(TIM14, &TIM_OCInitStruct);
	TIM_OC1PreloadConfig(TIM14, TIM_OCPreload_Enable);
	TIM_ARRPreloadConfig(TIM14, ENABLE);

    TIM_Cmd(TIM14, ENABLE);
}

void PWM_Servo_SetCompare1(uint16_t Compare)
{
    TIM_SetCompare1(TIM14 , Compare);

}

void Servo_SetAngle(float Angle)
{
	PWM_Servo_SetCompare1(Angle / 180 * 2000 + 500);
	
}

