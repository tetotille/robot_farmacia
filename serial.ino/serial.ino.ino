String x;
int pushButton = 2;
int estado = 0;
void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
 pinMode(pushButton, INPUT);
}
void loop() {
   while (!Serial.available());

   if (digitalRead(pushButton) == HIGH){
      estado++;
      delay(500);
   }
   if (estado > 1){
      estado = 0;
   }

   if (estado == 0){
      Serial.print("desocupado\n");
      delay(500);
    }else if(estado == 1){
        Serial.print("ocupado\n");
        delay(500);
    }
}
