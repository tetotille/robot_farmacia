#include <AccelStepper.h>
#include <SoftwareSerial.h>
#include <Servo.h>

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

#define servopin            1

//#define motor1pin1          5
//#define motor1pin2          6
//#define ENA                 4

#define LED_rojo           50
#define LED_verde          52
#define pushbutton         A11

//boolean x_done, y_done, z_done, done;

int motor1pin1 = 5;
int motor1pin2 = 6;
int ENA =       4;

AccelStepper stepperX = AccelStepper(1, X_STEP_PIN, X_DIR_PIN);
AccelStepper stepperY = AccelStepper(1, Y_STEP_PIN, Y_DIR_PIN);
AccelStepper stepperZ = AccelStepper(1, Z_STEP_PIN, Z_DIR_PIN);

AccelStepper stepper[] = {AccelStepper (1, X_STEP_PIN, X_DIR_PIN), AccelStepper (1, Y_STEP_PIN, Y_DIR_PIN), AccelStepper (1, Z_STEP_PIN, Z_DIR_PIN) };

int MIN_Switch[] = {X_MIN_PIN, Y_MIN_PIN, Z_MIN_PIN};
int MAX_Switch[] = {X_MAX_PIN, Y_MAX_PIN, Z_MAX_PIN};

Servo myservo;

String x;
int estado = 0;
int marcaEstado = 0;
int done = 0;
double dz = 4000;

int vel_cinta = 100;
char uart_python[10];

String posicion;
int fila, columna;

// La lista de posiciones se hace de tal forma que se ubica la posicion final
// del robot en lista_posiciones
// lista_posiciones[cant_lugares][coordenadas(x,y,z)]
// lugar 16 es la posicion inicial
// lugar 17 es la posicion de entrega de medicamentos
// lugar 18 es la posicion de la cinta
double lista_posiciones[19][3] = { { -310, 1100, 3600},// 0
                            { -895, 1100, 3600},// 1
                            { -1485, 1100, 3600},// 2
                            { -2040, 1100, 3600},// 3
                            { -310, 1100, 15400},// 4
                            { -895, 1100, 15400},// 5
                            { -1485, 1100, 15400},// 6
                            { -2040, 1100, 15400},// 7
                            { -310, 1100, 27200},// 8
                            { -895, 1100, 27200},// 9
                            { -1485, 1100, 27200},// 10
                            { -2040, 1100, 27200},// 11
                            { -310, 1100, 38500},// 12
                            { -895, 1100, 38500},// 13
                            { -1485, 1100, 38500},// 14
                            { -2040, 1100, 38500},// 15
                            { 0, 0, 0},// 16 //final de carrera minimo
                            { 0, 0, 0},// 17 //final de carrera minimo
                            { 0, 0, 0} };// 18 //final de carrera maximo
double posicion_final[3];


void entregarRemedio(){
    done = 0;
    stepper[0].moveTo(-4000);
    while ( done == 0) {
      if(digitalRead(MAX_Switch[0]) == LOW){
        stepper[0].stop();
        done = 1;
      }
      else if (stepper[0].distanceToGo() != 0){
        stepper[0].setSpeed(-250);
        stepper[0].run();
      }
      else 
        done = 1;
    }

    // mover servo
    int posServo = 0;
    for (posServo = 0; posServo <= 180; posServo += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
      myservo.write(posServo);              // tell servo to go to position in variable 'pos'
      delay(500);                       // waits 15ms for the servo to reach the position
    }
    for (posServo = 180; posServo >= 0; posServo -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(posServo);              // tell servo to go to position in variable 'pos'
      delay(500);                       // waits 15ms for the servo to reach the position
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

void mover_cinta(){
   digitalWrite(motor1pin1, LOW);
   digitalWrite(motor1pin2, HIGH);

   analogWrite(ENA, vel_cinta); 
   delay(7000);
   
    digitalWrite(motor1pin1, LOW);
   digitalWrite(motor1pin2, LOW);
  }


int integerButton(int val){
  int bandera;
  //int percent = map(val, 0, 1023, 0, 100);
  if (val > 900){
    bandera = 1;
    return bandera;
  }
  else{
    bandera = 0;
    return bandera;
  }
}


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
  
    Serial.begin(115200);
    
    //pinMode(pushButton, INPUT);
    pinMode(LED_rojo, OUTPUT);
    pinMode(LED_verde, OUTPUT);
    //pinMode(cinta, OUTPUT);

    pinMode(ENA,OUTPUT);
    pinMode(motor1pin1, OUTPUT);
    pinMode(motor1pin2, OUTPUT);
}


//-----------------------MAIN-------------------------
void loop() {
    // Despacho de Medicamento///////////////////////////////////////////
    // 1. Primero debe verificar si hay pedidos
    posicion = Serial.readString();
    digitalWrite(LED_rojo, LOW);
    digitalWrite(LED_verde, HIGH);
    
    homeStepper();
    
    if (posicion!=""){
        digitalWrite(LED_rojo, HIGH);
        digitalWrite(LED_verde, LOW);

        posicion_final[0] = lista_posiciones[posicion.toInt()][0];
        posicion_final[1] = lista_posiciones[posicion.toInt()][1];
        posicion_final[2] = lista_posiciones[posicion.toInt()][2];
        
        // 2. Se mueven los motores de a 1 para no forzarle demasiado al sistema
  
         moveStepper(0, posicion_final[0], -350); // 0 is stepperX
         delay(500);
         moveStepper(2, posicion_final[2], 1000); // 2 is stepperZ
         delay(500);
         moveStepper(1, posicion_final[1], 350); // 1 is stepperY
         delay(500); 

         //3. Se hace el proceso de levantar el medicamento
        // Primero se mete el robot bajo el palé
         moveStepper(2, posicion_final[2]+dz, 1000); // 2 is stepperZ
        
        // 4. Lleva el medicamento en la posicion de entrega de medicamentos
        entregarRemedio();
         
        // 5. Se vuelve a la posición inicial
        homeStepper();
    }

    // Reposición de medicamentos////////////////////////////////////////////////
    // 1. Primero se verifica si se presionó el botón
     int value = analogRead(pushbutton);
    int boton = integerButton(value);
    if (boton == HIGH){
        digitalWrite(LED_rojo, HIGH);
        digitalWrite(LED_verde, LOW);
        mover_cinta();

        posicion =Serial.readString();
        
        // 2. El robot lleva el medicamento donde debe ser
        posicion_final[0] = lista_posiciones[posicion.toInt()][0];
        posicion_final[1] = lista_posiciones[posicion.toInt()][1];
        posicion_final[2] = lista_posiciones[posicion.toInt()][2];
  
         moveStepper(0, posicion_final[0], -350); // 0 is stepperX
         delay(500);
         moveStepper(2, posicion_final[2]+dz, 1000); // 2 is stepperZ
         delay(500);
         moveStepper(1, posicion_final[1], 350); // 1 is stepperY
         delay(500); 
         moveStepper(2, posicion_final[2], -1000); // 2 is stepperZ

       // 3. Se vuelve a la posición inicial
        homeStepper();
        
    }
}
