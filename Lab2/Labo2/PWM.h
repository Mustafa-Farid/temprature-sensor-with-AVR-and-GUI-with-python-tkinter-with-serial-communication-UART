/*
 * PWM.h
 *
 *  Created on: Nov 9, 2021
 *      Author: 20109
 */

#ifndef PWM_H_
#define PWM_H_

void PWM_init_timer1_oc1a();
void set_duty_oc1a(unsigned char duty);

void PWM_init_timer1_oc1b();
void set_duty_oc1b(unsigned char duty);

void PWM_stop_timer1_oc1b();
void PWM_stop_timer1_oc1a();

#endif /* PWM_H_ */
