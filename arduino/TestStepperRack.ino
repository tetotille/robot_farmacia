#include <AccelStepper.h>
#include <SoftwareSerial.h>

#define X_STEP_PIN         54
#define X_DIR_PIN          55
#define X_ENABLE_PIN       38
#define X_MIN_PIN           3
#define X_MAX_PIN           2

#define Y_STEP_PIN         60
#define Y_DIR_PIN          61
#define Y_ENABLE_PIN       56
#define Y_MIN_PIN          14
#define Y_MAX_PIN          15

#define Z_STEP_PIN         46
#define Z_DIR_PIN          48
#define Z_ENABLE_PIN       62
#define Z_MIN_PIN          18
#define Z_MAX_PIN          19

int motor1pin1 = 5;
int motor1pin2 = 6;
int ENA = 4;

boolean x_done, y_done, z_done, done;

AccelStepper stepperX = AccelStepper(1, X_STEP_PIN, X_DIR_PIN);
AccelStepper stepperY = AccelStepper(1, Y_STEP_PIN, Y_DIR_PIN);
AccelStepper stepperZ = AccelStepper(1, Z_STEP_PIN, Z_DIR_PIN);

AccelStepper stepper[] = {AccelStepper (1, X_STEP_PIN, X_DIR_PIN), AccelStepper (1, Y_STEP_PIN, Y_DIR_PIN), AccelStepper (1, Z_STEP_PIN, Z_DIR_PIN) };

int MIN_Switch[] = {X_MIN_PIN, Y_MIN_PIN, Z_MIN_PIN};
int MAX_Switch[] = {X_MAX_PIN, Y_MAX_PIN, Z_MAX_PIN};

//String x;
//int pushButton = 53;
//int estado = 0;
//int marcaEstado = 0;
//
//int LED_rojo = 52;
//int LED_verde = 51;

char posicion[10];
int fila, columna;

// La lista de posiciones se hace de tal forma que se ubica la posicion final
// del robot en lista_posiciones
// lista_posiciones[cant_lugares][coordenadas(x,y,z)]
// lugar 16 es la posicion inicial
// lugar 17 es la posicion de entrega de medicamentos
// lugar 18 es la posicion de la cinta
float lista_posiciones[19][3] = { { 0, 0, 0},// 0
                            { 0, 0, 0},// 1
                            { 0, 0, 0},// 2
                            { 0, 0, 0},// 3
                            { 0, 0, 0},// 4
                            { 0, 0, 0},// 5
                            { 0, 0, 0},// 6
                            { 0, 0, 0},// 7
                            { 0, 0, 0},// 8
                            { 0, 0, 0},// 9
                            { 0, 0, 0},// 10
                            { 0, 0, 0},// 11
                            { 0, 0, 0},// 12
                            { 0, 0, 0},// 13
                            { 0, 0, 0},// 14
                            { 0, 0, 0},// 15
                            { 0, 0, 0},// 16
                            { 0, 0, 0},// 17 
                            { 0, 0, 0} };// 18
int posicion_final[3];

void setup() {
  stepper[0].setEnablePin(X_ENABLE_PIN);
  stepper[0].setPinsInverted(false, false, true);
  stepper[0].enableOutputs();

  stepper[1].setEnablePin(Y_ENABLE_PIN);
  stepper[1].setPinsInverted(false, false, true);
  stepper[1].enableOutputs();

  stepper[2].setEnablePin(Z_ENABLE_PIN);
  stepper[2].setPinsInverted(false, false, true);
  stepper[2].enableOutputs();
  
  stepper[0].setMaxSpeed(350);
  stepper[1].setMaxSpeed(350);
  stepper[2].setMaxSpeed(2000);
 
  pinMode(X_MIN_PIN, INPUT);
  pinMode(Y_MIN_PIN, INPUT);
  pinMode(Z_MIN_PIN, INPUT);

  pinMode(X_MAX_PIN, INPUT);
  pinMode(Y_MAX_PIN, INPUT);
  pinMode(Z_MAX_PIN, INPUT);

//  stepper[0].setCurrentPosition(0);
//  stepper[1].setCurrentPosition(0);
//  stepper[2].setCurrentPosition(0);

  Serial.begin(9600);

  pinMode(ENA,OUTPUT);
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
}


// FUNCIONES

void moveStepper (int i, double cant, int vel){
   done = 0 ;
   
  stepper[i].moveTo(cant);
  while ( done == 0) {
    if(digitalRead(MAX_Switch[i]) == LOW){
      stepper[i].stop();
      done = 1;
    }
    else if (stepper[i].distanceToGo() != 0){
      stepper[i].setSpeed(vel);
      stepper[i].run();
    }
    else 
      done = 1;
  }
}


void homeStepper (){
      //Y
     done = 0;
    stepper[1].moveTo(-2000);
    while ( done == 0) {
      if(digitalRead(MIN_Switch[1]) == LOW){
        stepper[1].stop();
        stepper[1].setCurrentPosition(0);
        done = 1;
      }
      else if (stepper[1].distanceToGo() != 0){
        stepper[1].setSpeed(-250);
        stepper[1].run();
      }
      else 
        done = 1;
    }

    //Z
    done = 0;
    stepper[2].moveTo(-60000);
    while ( done == 0) {
      if(digitalRead(MIN_Switch[2]) == LOW){
        stepper[2].stop();
        stepper[2].setCurrentPosition(0);
        done = 1;
      }
      else if (stepper[2].distanceToGo() != 0){
        stepper[2].setSpeed(-1000);
        stepper[2].run();
      }
      else 
        done = 1;
    }

    //X
    done = 0;
    stepper[0].moveTo(4000);
    while ( done == 0) {
      if(digitalRead(MIN_Switch[0]) == LOW){
        stepper[0].stop();
        stepper[0].setCurrentPosition(0);
        done = 1;
      }
      else if (stepper[0].distanceToGo() != 0){
        stepper[0].setSpeed(250);
        stepper[0].run();
      }
      else 
        done = 1;
    }
  }
  //delay(1500);
//
//  done = 0 ;
//  stepper[i].moveTo(-cant);
//  while ( done == 0) {
//    if(digitalRead(MIN_Switch[i]) == LOW){
//      stepper[i].stop();
//      stepper[i].setCurrentPosition(0);
//      done = 1;
//    }
//    else if (stepper[i].distanceToGo() != 0){
//      stepper[i].setSpeed(350);
//      stepper[i].run();
//    }
//    else 
//      done = 1;
//  }
//delay(1500);


void loop() {
  if (Serial.available()){
   String sx = Serial.readStringUntil(';');
   Serial.println("X: "+ sx);
   String sy = Serial.readStringUntil(';');
   Serial.println("Y: "+ sy);
   String sz = Serial.readStringUntil(';');
   Serial.println("Z: "+ sz);
   String sdz = Serial.readStringUntil(';');
   Serial.println("dZ: "+ sdz);
   
//   Serial.println("X: ");
//   sx = Serial.read();
//   Serial.println("Y: ");
//   sy = Serial.read();
//   Serial.println("Z: ");
//   sz = Serial.read();

   int x = sx.toInt();
   int y = sy.toInt();
   double z = sz.toDouble();
   double dz = sdz.toDouble();
   
   homeStepper();

//   digitalWrite(motor1pin1, LOW);
//   digitalWrite(motor1pin2, HIGH);
//
//   analogWrite(ENA, 80); 
//   delay(5000);
//   
//    digitalWrite(motor1pin1, LOW);
//   digitalWrite(motor1pin2, LOW);
   
   moveStepper(0, x, -350); // 0 is stepperX
   //delay(1000);
   moveStepper(2, z, 1000); // 2 is stepperZ
   //delay(1000);
   moveStepper(1, y, 350); // 1 is stepperY
   //delay(1000); 
   moveStepper(2, dz, -1000); // 2 is stepperZ

   homeStepper();
  }
}
