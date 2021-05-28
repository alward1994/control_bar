// аналог пины
#define POT A4
#define RELAY 7
unsigned long tmr=0;
float p;
float d;
float pav;
int t;

#include "EncButton.h"
#include "Parser.h"
#include "AsyncStream.h"  // асинхронное чтение сериал
AsyncStream<50> serial(&Serial, ';');   // указываем обработчик и стоп символ




void setup() {
  Serial.begin(115200);
  pinMode(13, 1);
  pinMode(RELAY, 1);
  
}


void loop() {
  parsing();
  tmr++;
  t=tmr/100;
  d=analogRead(POT);
  pav=(d-78)/5.4;
  p=(p*9/10)+pav/10;
  delay(10);
  static uint32_t tm=0;
  if (millis() - tm > 1000) {
    tm = millis();
    Serial.print(0);
    Serial.print(',');
    Serial.print(t);
    Serial.print(',');
    Serial.println(p);
  }
}

// функция парсинга, опрашивать в лупе
void parsing() {
  if (serial.available()) {
    Parser data(serial.buf, ',');  // отдаём парсеру
    int ints[10];           // массив для численных данных
    data.parseInts(ints);   // парсим в него

    switch (ints[0]) {
      case 0: digitalWrite(13, ints[1]);
        break;
      case 1:
        digitalWrite(RELAY, ints[1]);
        break; 

      } 
    }
  }

//  void my_fun(int t1,int t2,float pp){  
//  if(t >= t1 && t < t2 ){
//    digitalWrite(RELAY,0);
//    if(p <= pp){
//           digitalWrite(RELAY,1);}
//       else{ digitalWrite(RELAY,0);}
//  }   
// }
