#define F_CPU   16000000UL
#define BAUD    9600
#define MYUBRR  (F_CPU/16/BAUD-1)
#define FLAG_T2         TIFR2 & (1 << TOV2)
#define BUTTON          (PINB & 0b00001111)

#include <avr/io.h>
#include <stdio.h>
#include <stdlib.h>
#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <util/delay.h>
/* FreeRTOS kernel includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

#include <stdio.h>
#include "myprintf.h"

#include "lcdpcf8574.h"

#include <IRremote.h>
const int RECV_PIN = 38;
IRrecv irrecv(RECV_PIN);
decode_results results;
unsigned long key_value=0;

QueueHandle_t Queue_Handle_Button =0;
QueueHandle_t Queue_Handle_ACK =0;
QueueHandle_t Queue_Handle_Rasp =0;
QueueHandle_t Queue_Handle_LCD =0;
QueueHandle_t Queue_Handle_Teclado=0;
QueueHandle_t Queue_Handle_Control=0;

void delay_20ms( void );
void portsInit( void );
void debounce( void );
void USART_Init( void);
unsigned char USART_Receive( void );
void USART_Transmit( unsigned char data );
unsigned char checkI(void);
unsigned char check_Remo(void);
void printInfo(unsigned char can);

enum timer2     { initCount_20ms = 178};

/*
void sender_task(void *p)
{
    int but=0;
    int ack=1;
    while (1) {
        while(ack==0){
            xQueueReceive(Queue_Handle_ACK, &ack, 1000);
        }
        ack=0;
        while ((PINB & 0b00001111)==0b00000000);
        delay_20ms();
        if ((BUTTON)!=0b00000000){
            if ((BUTTON)==0b00000001){
                but=1;
            }
            else if ((BUTTON)==0b00000010){
                but=2;
            }
            else if ((BUTTON)==0b00000100){
                but=3;
            }
            else if ((BUTTON)==0b00001000){
                but=4;
            }
            xQueueSend(Queue_Handle_Button, &but, 1000);
            //vTaskDelay(100);
        }
        //vTaskDelay(1100);
        //vTaskDelay(1100);
  }

}*/

void idle_task(void *p)
{
    int but=0;
    int tecCtl=0;
    int ack=3;
    while (1) {
      
        while(ack==0){
            xQueueReceive(Queue_Handle_ACK, &ack, 1000);
        }
        ack=0;
        unsigned char tecla='f';
        if (but==0){
          /*if (tecCtl==0){
            irrecv.resume();
          }*/
          while (tecla=='f'){
            tecla=checkI();
            if (tecla=='f'){
              tecla=check_Remo();
              if (tecla!='f'){
                tecCtl=1;
              }
            }else{
              tecCtl=0;
            }
            
          }
          xQueueSend(Queue_Handle_Button, &tecla, 1000);
            but=1;
            tecla='f' ;
        }else{
          xQueueSend(Queue_Handle_Button, &tecla, 1000);
          but=0;
          //vTaskDelay(100);
        }
        //vTaskDelay(1100);
        //vTaskDelay(1100);
  }

}
/*
void sender_task(void *p)
{
    int but=0;
    int ack=3;
    while (1) {
      
        while(ack==0){
            xQueueReceive(Queue_Handle_ACK, &ack, 1000);
        }
        ack=0;
        unsigned char tecla='f';
        if (but==0){
            unsigned char tecla=checkI();
            xQueueSend(Queue_Handle_Button, &tecla, 1000);
            but=1;
        }else{
          xQueueSend(Queue_Handle_Button, &tecla, 1000);
          but=0;
          //vTaskDelay(100);
        }
        //vTaskDelay(1100);
        //vTaskDelay(1100);
  }

}*/

void receiver_task(void *p)
{
    int rx_int = 0;
    unsigned char rx_char;
    while (1) {
        while (!xQueueReceive(Queue_Handle_Button, &rx_char, 1000));
        //{
        /*
            if (rx_int==1){
                myprintf("Up\n");
            }
            else if (rx_int==2){
                myprintf("Down\n");
            }
            else if (rx_int==3){
                myprintf("Left\n");
            }
            else if (rx_int==4){
                myprintf("Right\n");
            }else{
                myprintf(" ");
            }*/
         USART_Transmit(rx_char);
         xQueueSend(Queue_Handle_Rasp, &rx_char, 1000);
            //vTaskDelay(1000);
        /*}
        else{
            myprintf("Failed to receive data from queue\n");
        }*/
  }

}

void receiveRasp_task(void *p)
{
    
    unsigned char set='n';
    while (1) {
        while (!xQueueReceive(Queue_Handle_Rasp, &set, 1000));
        /*{
         */set=USART_Receive();
            /*if (set=='1'){
                bor=1;
            }
            else if (set=='2'){
                bor=2;
            }
            else if (set=='3'){
                bor=3;
            }
            else if (set=='4'){
                bor=4;
            }else{
                bor=8;
            }*/
//            set=USART_Receive();
            xQueueSend(Queue_Handle_LCD, &set, 1000);
            //vTaskDelay(1000);
        /*}
        else{
            myprintf("Failed to receive data from queue\n");
        }*/
  }

}

void LCD_task(void *p)
{
    unsigned char tecla2;
    int dir = 0;
    int one=1;
    while (1) {
        while (!xQueueReceive(Queue_Handle_LCD, &tecla2, 1000));
        //{
        uint8_t col = 0;
        uint8_t row = 0;
        uint8_t led = 0;
        lcd_gotoxy(col, row);
        /*
            if (dir==1){
                lcd_puts("Up\n");
            }
            else if (dir==2){
                lcd_puts("Down\n");
            }
            else if (dir==3){
                lcd_puts("Left\n");
            }
            else if (dir==4){
                lcd_puts("Right\n");
            }else{
                lcd_puts(" ");
            }*/
            if (tecla2!='f'){
                /*lcd_putc(tecla2);
                vTaskDelay(1000);*/
                printInfo(tecla2);
            }
            //irrecv.resume();
            xQueueSend(Queue_Handle_ACK, &one, 1000);
            //vTaskDelay(1000);
        /*}
        else{
            myprintf("Failed to receive data from queue\n");
        }*/
  }

}


int main(void) {
     /* Replace with your application code */

lcd_init(LCD_DISP_ON_BLINK);
USART_Init( ); /* initialize serial communication */
portsInit();
irrecv.enableIRIn();

Queue_Handle_ACK = xQueueCreate(1, sizeof(int));
Queue_Handle_Button = xQueueCreate(1, sizeof(int));
Queue_Handle_Teclado = xQueueCreate(1, sizeof(int));
Queue_Handle_LCD = xQueueCreate(1, sizeof(int));
Queue_Handle_Rasp = xQueueCreate(1, sizeof(int));
Queue_Handle_Control = xQueueCreate(1, sizeof(int));

lcd_home();
lcd_led(0); //set led
  xTaskCreate( idle_task, /* The function that implements the task. */
          (char*) "id",/* The text name assigned to the task. */
          1024,     /* The size of the stack for the task. */
          NULL,   /* The parameter passed to the task  */
          1,            /* The priority assigned to the task. */
        NULL );  
    /*
  xTaskCreate( sender_task, // The function that implements the task. 
          (char*) "tx",// The text name assigned to the task. 
          1024,     // The size of the stack for the task. 
          NULL,   // The parameter passed to the task  
          2,            // The priority assigned to the task. 
        NULL );       // The task handle is not required. 
    
    xTaskCreate( remote_task, // The function that implements the task. 
          (char*) "ir",// The text name assigned to the task. 
          1024,     // The size of the stack for the task. 
          NULL,   // The parameter passed to the task  
          2,            // The priority assigned to the task. 
        NULL );  
    */
    xTaskCreate( receiver_task, /* The function that implements the task. */
          (char*) "rx",/* The text name assigned to the task. */
          1024,     /* The size of the stack for the task. */
          NULL,   /* The parameter passed to the task  */
          3,            /* The priority assigned to the task. */
        NULL );       /* The task handle is not required. */

    xTaskCreate( receiveRasp_task, /* The function that implements the task. */
          (char*) "ra",/* The text name assigned to the task. */
          1024,     /* The size of the stack for the task. */
          NULL,   /* The parameter passed to the task  */
          4,            /* The priority assigned to the task. */
        NULL );       /* The task handle is not required. */


    xTaskCreate( LCD_task, /* The function that implements the task. */
          (char*) "lc",/* The text name assigned to the task. */
          1024,     /* The size of the stack for the task. */
          NULL,   /* The parameter passed to the task  */
          5,            /* The priority assigned to the task. */
        NULL );  
        
  /* Start the tasks and timer running. */
  vTaskStartScheduler();

  return 0;
}

void USART_Init(void){
  //(Pag. 206 datasheet)
    UBRR0H = (unsigned char)(MYUBRR>>8);
    UBRR0L = (unsigned char)MYUBRR;
    /* Enable receiver and transmitter */
    UCSR0B = (1<<RXEN0)|(1<<TXEN0);
    /* Set frame format: 8 bit-data, 1stop bit */
    UCSR0C |=  (3<<UCSZ00);

    //Free-Style
    UCSR0A= UCSR0A | (1 << UDRE0); //Indica que USART está listo para recibir

}

void portsInit( void ){ 
    PORTB = 0b11111111; // pull-up conectado para todos los PORTB pins
    DDRB = 0B11110000; //  0 input 1 output
    MCUCR = MCUCR & 0b11101111; // pull-up habilitado para todos los PORTBs
}

void debounce( void ){
    while( BUTTON );//              wait until BUTTON is pressed (0)
    delay_20ms( );//                delay of 20 ms
    if( BUTTON ) return;//          ask again, if (1) then is not really pressed
    PORTB = PORTB & ~(1 << PB1);//  clean signal (0)
    while( !BUTTON );//             wait until BUTTON is released (1)
    delay_20ms( );    
    PORTB = PORTB | (1 << PB1);//    clean signal (1)
}
void delay_20ms( void ){
    for( unsigned char i = 0; i < (20/8); i++ ) {
  TCNT2 = initCount_20ms;//       load initial count  
    TIFR2 = TIFR2 | (1  << TOV2);// clear the Timer2 ovf flag, look for TIFR2 register
    TCCR2A = TCCR2A & ~(1 << WGM21) & ~(1 << WGM20);//    waveform generation mode 0:
    TCCR2B = TCCR2B & ~(1 << WGM22) & ~(1 << CS22) & ~(1 << CS21) & ~(1 << CS20) ;//    normal operation 
    TCCR2B = TCCR2B  | (1 << CS22) | (1 << CS21) | (1 << CS20);//    Timer 2 enabled with 1024 prescaler
    while( !FLAG_T2 );//            wait for Timer 2 overflow
    TCCR2B = TCCR2B & ~(1 << WGM22) & ~(1 << CS22) & ~(1 << CS21) & ~(1 << CS20) ;//      stop Timer 2
    }
}

unsigned char USART_Receive( void ){
/* Wait for data to be received */
while ( !(UCSR0A & (1<<RXC0)) );
/* Get and return received data from buffer */
return UDR0;
}

void USART_Transmit( unsigned char data ){
/* Wait for empty transmit buffer */
while ( !( UCSR0A & (1<<UDRE0)) );
/* Put data into buffer, sends the data */
UDR0 = data;
}

unsigned char checkI(void){
    unsigned char tecla='f';
    int ret=0;
    //while(ret==0){
        PORTB = 0b11101111;
        if ((PINB & 0b00000001)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
                tecla='3';
                ret=1;
            return tecla; 
        }
        if ((PINB & 0b00000010)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='o';//'D';
            ret=1;
            //irrecv.resume();
            return tecla;
        }
        if ((PINB & 0b00000100)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='0';
            ret=1;
            return tecla;
        }
        if ((PINB & 0b00001000)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='u';//'*';
            ret=1;
            return tecla;
        }
        PORTB = 0b11011111;
        if ((PINB & 0b00000001)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='E';//'#';
            ret=1;
            return tecla; 
        }
        if ((PINB & 0b00000010)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='s';//'C';
            ret=1;
            //irrecv.resume();
            return tecla;
        }
        if ((PINB & 0b00000100)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='8';
            ret=1;
            return tecla;
        }
        if ((PINB & 0b00001000)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='7';
            ret=1;
            return tecla;
        }
        PORTB = 0b10111111;
        if ((PINB & 0b00000001)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='9';
            ret=1;
            return tecla; 
        }
        if ((PINB & 0b00000010)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='b';//'B';
            ret=1;
            //irrecv.resume();
            return tecla;
        }
        if ((PINB & 0b00000100)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='5';
            ret=1;
            return tecla;
        }
        if ((PINB & 0b00001000)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='4';
            ret=1;
            return tecla;
        }
        PORTB = 0b01111111;
        if ((PINB & 0b00000001)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='6';
            ret=1;
            return tecla; 
        }
        if ((PINB & 0b00000010)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='p';//'A';
            ret=1;
            //irrecv.resume();
            return tecla;
        }
        if ((PINB & 0b00000100)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='2';
            ret=1;
            return tecla;
        }
        if ((PINB & 0b00001000)==0){
            for (unsigned char i = 0; i < 40; i++){
                delay_20ms();
            }
            tecla='1';
            ret=1;
            return tecla;
        }
    return tecla;
    ret=1;
    //}
    //return 'e';
}

unsigned char check_Remo(void){
  unsigned char tecla3='f';
  if (irrecv.decode(&results)){
    //Serial.println(results.value, HEX);
    
    //if (results.value == 0XFFFFFFFF)
          //results.value = key_value;

    switch(results.value){
      case 0xFFA25D:
      //irrecv.resume();
      tecla3 = 'o'; //Power
      break;
      case 0xFF629D:
      //irrecv.resume();
      tecla3 = 'r'; //Mode
      break;
      case 0xFFE21D:
      //irrecv.resume();
      tecla3 = 'm'; //("Mute");
      break;
      case 0xFF22DD:
      //irrecv.resume();
      tecla3 = 'p'; //("Play/Pause");
      break;
      case 0xFF02FD:
      //irrecv.resume();
      tecla3 = 'b'; //("|<<");
      break ;  
      case 0xFFC23D:
      //irrecv.resume();
      tecla3 = 's'; //(">>|");
      break ;               
      case 0xFFE01F:
      //irrecv.resume();
      tecla3 = 'E'; //("EQ");
      break ;  
      case 0xFFA857:
      //irrecv.resume();
      tecla3 = '-'; //("-");
      break ;  
      case 0xFF906F:
      //irrecv.resume();
      tecla3 = '+'; //("+");
      break ;  
      case 0xFF6897:
      //irrecv.resume();
      tecla3 = '0'; //("0");
      break ;  
      case 0xFF9867:
      //irrecv.resume();
      tecla3 = 'u'; //("Skip 5s");
      break ;
      case 0xFFB04F:
      //irrecv.resume();
      tecla3 = 'm'; //("Go back 5s");
      break ;
      case 0xFF30CF:
      //irrecv.resume();
      tecla3 = '1'; //("1");
      break ;
      case 0xFF18E7:
      //irrecv.resume();
      tecla3 = '2'; //("2");
      break ;
      case 0xFF7A85:
      //irrecv.resume();
      tecla3 = '3'; //("3");
      break ;
      case 0xFF10EF:
      //irrecv.resume();
      tecla3 = '4'; //("4");
      break ;
      case 0xFF38C7:
      //irrecv.resume();
      tecla3 = '5'; //("5");
      break ;
      case 0xFF5AA5:
      //irrecv.resume();
      tecla3 = '6'; //("6");
      break ;
      case 0xFF42BD:
      //irrecv.resume();
      tecla3 = '7'; //("7");
      break ;
      case 0xFF4AB5:
      //irrecv.resume();
      tecla3 = '8'; //("8");
      break ;
      case 0xFF52AD:
      //irrecv.resume();
      tecla3 = '9'; //("9");
      break ;      
    }
    //key_value = results.value;
    //irrecv.resume();
  }else{
    tecla3 = 'f';
  }
  irrecv.resume();
  return tecla3;
}

void printInfo(unsigned char can){
 /* FILE *fp;
  char str[1000];
  char* filename="canciones.txt";

  fp = fopen(filename, "r");
  while(fgets(str,1000,fp)!=NULL);
  */
  lcd_clrscr();
  unsigned char prin='a';
  while (prin!='!'){
    prin=USART_Receive();
    if (prin!='!' && prin!=','){
      lcd_putc(prin);
    }
    if (prin==','){
      lcd_gotoxy(0, 1);
    }
  }
}
