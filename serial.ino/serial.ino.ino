String x;
int pushButton = 53;
int estado = 0;
int marcaEstado = 0;
void setup() {
 Serial.begin(115200);
 pinMode(pushButton, INPUT);
}
void loop() {
   
   if (digitalRead(pushButton) == HIGH){
      if (marcaEstado == 0) {
        estado == 0;
      }
      marcaEstado = 1;
      estado++;
   }
   
   if (estado >= 10 or digitalRead(pushButton) == LOW) {
      marcaEstado = 0;
   }
   
   if (marcaEstado){
      Serial.print("ocupado\n");
      delay(500);
    }else{
        Serial.print("desocupado\n");
        delay(500);
    }
}
