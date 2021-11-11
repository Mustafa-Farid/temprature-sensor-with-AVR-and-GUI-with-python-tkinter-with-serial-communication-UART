/*
 * PWM.c
 *
 *  Created on: Nov 9, 2021
 *      Author: Mustafa farid
 */

#include <avr/io.h>
#include <util/delay.h>
#include "common_macros.h"
void PWM_init_timer1_oc1a(){
	DDRD|=(1<<5);
	TCCR1A |= ((1<<WGM11)|(1<<WGM10)|(1<<COM1A1)); // Fast PWM PWM at OC1A
	TCCR1B = 1<<WGM12 | 1<<CS10;
}
void PWM_stop_timer1_oc1a(){
	CLEAR_BIT(TCCR1A,COM1A1);
	CLEAR_BIT(TCCR1A,COM1A0);
}
void PWM_stop_timer1_oc1b(){
	CLEAR_BIT(TCCR1A,COM1B0);
	CLEAR_BIT(TCCR1A,COM1B1);
}

/*
duty = (ocr1a / 1023) * 100
OCR1A = duty* 10.23;
*/


void set_duty_oc1a(unsigned char duty){
	OCR1A = duty* 10.23;
}



void PWM_init_timer1_oc1b(){
	DDRD|=(1<<4);
	TCCR1A |= 1<<COM1B1 | 1<<WGM10 | 1<<WGM11;
	TCCR1B = 1<<WGM12 | 1<<CS10;
}

void set_duty_oc1b(unsigned char duty){
	OCR1B = duty* 10.23;
}
