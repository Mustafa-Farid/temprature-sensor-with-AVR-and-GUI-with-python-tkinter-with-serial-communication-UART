

#include "uart.h"
#include "adc.h"
#include "lcd.h"
#include "PWM.h"
#include <avr/interrupt.h>
volatile uint8 state = 'f';

ISR(USART_RXC_vect)
{
	state=UDR;
	if(state=='o')
	{
		SET_BIT(PORTD,7);
	}
	else if(state=='f')
	{
		CLEAR_BIT(PORTD,7);
	}
}

int main(void)
{
		uint32 temp;
		uint8 buffer[32];
		float speed = 0.0;
		CLEAR_BIT(DDRB,0);
		CLEAR_BIT(DDRB,1);
		SET_BIT(DDRB,6);
		SET_BIT(DDRB,7);
		SET_BIT(PORTB,7);
		CLEAR_BIT(PORTB,6);
		//uint8 led = USART_SEND_OFF;
		LCD_init(); /* initialize LCD driver */
		ADC_init(); /* initialize ADC driver */
		UART_init();
		PWM_init_timer1_oc1a();
		sei();
		LCD_clearScreen(); /* clear LCD at the beginning */



	    while(1)
	    {



	    		if(state=='o')
	    		{
	    			SET_BIT(PORTD,7);
	    			LCD_goToRowColumn(0,0); /* display the number every time at this position */
	    			temp = ADC_readChannel(2); /* read channel two where the temp sensor is connect */
	    			temp = (temp*150*5)/(1023*1.5); /* calculate the temp from the ADC value*/
	    			speed = (temp*.6);
	    			set_duty_oc1a((uint8)speed);
	    			LCD_displayString("Temp = ");
	    			LCD_goToRowColumn(0,10);
	    			LCD_intgerToString(temp); /* display the temp on LCD screen */
	    			/* display character 'C' on the screen "Temp =   C" */
	    			LCD_displayCharacter('C');
	    			ultoa(temp,buffer,10);		// change temp to string
	    			UART_sendString(buffer);	// send it by uart
	    			_delay_ms(10);
	    			if(PINB & (1<<0))
	    			{
	    				//UART_sendByte(UART_SEND_CHAR);
	    				UART_sendByte('A');
	    				_delay_ms(200);

	    			}
	    			if(PINB & (1<<1))
	    			{
	    				//UART_sendByte(UART_SEND_CHAR);
	    				UART_sendByte('Z');
	    				_delay_ms(200);
	    			}
	    		}
	    		else if(state=='f')
	    		{
	    			CLEAR_BIT(PORTD,7);
	    			set_duty_oc1a(0);
	    			LCD_clearScreen();
	    		}





	    }
}
