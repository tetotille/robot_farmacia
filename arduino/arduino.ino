#include <ctime>

String x;
int pushButton = 53;
int estado = 0;
int marcaEstado = 0;

int LED_rojo = 52;
int LED_verde = 51;

int cinta = 50;
char uart_python[10];

char posicion[10];
int fila, columna;

// La lista de posiciones se hace de tal forma que se ubica la posicion final
// del robot en lista_posiciones
// lista_posiciones[cant_lugares][coordenadas(x,y,z)]
// lugar 16 es la posicion inicial
// lugar 17 es la posicion de entrega de medicamentos
// lugar 18 es la posicion de la cinta
lista_posiciones[19][3] = { { 0, 0, 0},// 0
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

// variables del motor (NO DEFINITIVO)
int motor_x=0,motor_y=0,motor_z=0;


void empujar_hasta_que_caiga(void){
    int a = 0;
    return;
}


void setup() {
    Serial.begin(115200);
    pinMode(pushButton, INPUT);
    pinMode(LED_rojo, OUTPUT);
    pinMode(LED_verde, OUTPUT);
    pinMode(cinta, OUTPUT);
}


//-----------------------MAIN-------------------------
void loop() {
    // Pedido de Medicamento
    // 1. Primero debe verificar si hay pedidos
    posicion = Serial.read();
    digitalWrite(LED_rojo, LOW);
    digitalWrite(LED_verde, HIGH);
    
    if (posicion){
        digitalWrite(LED_rojo, HIGH);
        digitalWrite(LED_verde, LOW);
        
        fila = (int) posicion[1];
        columna = (int) posicion[3];
        posicion_final = lista_posiciones[4*fila+columna][:];
        
        // 2. Se mueven los motores de a 1 para no forzarle demasiado al sistema
        //motor_y ponele tiene que llegar primero
        while (posi_y < posicion_final[1]){
                motor_y = 255;
        }
        motor_y = 0;
        
        //motor_x se mueve segundo
        while (posi_x < posicion_final[0]){
                motor_x = 255;
        }
        motor_x = 0;
        
        //motor_z se mueve tercero
        while (posi_z < posicion_final[2]){
                motor_z = 255;
        }
        motor_z = 0;
        
        
        //3. Se hace el proceso de levantar el medicamento
        // Primero se mete el robot bajo el palé
        //Entra
        while (posi_x < posicion_final[0]+dx){
                motor_x = 255;
        }
        motor_x = 0;
        
        //Levanta
        while (posi_z < posicion_final[2]+dz){
            motor_z = 255;
        }
        motor_z = 0;
        
        //Retrocede
        while (posi_x > posicion_final[0]){
            motor_x = -255;
        }
        motor_x = 0;
        
        // 4. Lleva el medicamento en la posicion de entrega de medicamentos
        posicion_final = lista_posiciones[17];
        
        //motor_z se mueve primero
        while (posi_z > posicion_final[2]){
                motor_z = -255;
                
        }
        motor_z = 0;
        
        //motor_x se mueve segundo
        while (posi_x > posicion_final[0]){
                motor_x = -255;
        }
        motor_x = 0;
        
        //motor_y se mueve tercero
        while (posi_y > posicion_final[1]){
                motor_y = -255;
        }
        motor_y = 0;
        
        // Se empuja el medicamento para que caiga
        empujar_hasta_que_caiga();
        
        // 5. Se vuelve a la posición inicial
        posicion_final = lista_posiciones[16];
        
        //motor_z se mueve primero
        while (posi_z > posicion_final[2]){
                motor_z = -255;
                
        }
        motor_z = 0;
        
        //motor_x se mueve segundo
        while (posi_x > posicion_final[0]){
                motor_x = -255;
        }
        motor_x = 0;
        
        //motor_y se mueve tercero
        while (posi_y > posicion_final[1]){
                motor_y = -255;
        }
        motor_y = 0;
    }

    // Reposición de medicamentos
    // 1. Primero se verifica si se presionó el botón
    if (digitalRead(pushButton) == HIGH){
        digitalWrite(LED_rojo, HIGH);
        digitalWrite(LED_verde, LOW);
        
        // 2. Se empieza a mover la cinta y se verifica si llegó al punto de escaneo
        // El mensaje de escaneo es "escaneo"
        int bandera_scan = 0;
        time_t init_time;
        time_t current_time;
        while(true){
            uart_python = Serial.read();
            digitalWrite(cinta, HIGH);
            delay(15);
            if (uart_python == "escaneo"){
                bandera_scan = 1;
                init_time = time(NULL);
                posicion = Serial.read();
            }
            // Se hace más lenta la cinta al principio y dp de escanear a toda puta
            if (bandera_scan == 0){
                digitalWrite(cinta,LOW);
                delay(15);
            }
            
            // Se espera 5 segundos para que llegue el remedio en su lugar
            current_time = time(NULL) - init_time;
            if (current_time < 100 && current_time > 4){
                break;
            }

        }
        
        // 3. El robot lleva el medicamento donde debe ser
        fila = (int) posicion[1];
        columna = (int) posicion[3];
        posicion_final = lista_posiciones[4*fila+columna][:];
        while (posi_y < posicion_final[1]){
                motor_y = 255;
        }
        motor_y = 0;
        
        //motor_x se mueve segundo
        while (posi_x < posicion_final[0]){
                motor_x = 255;
        }
        motor_x = 0;
        
        //motor_z se mueve tercero
        while (posi_z < posicion_final[2]){
                motor_z = 255;
        }
        motor_z = 0;
        
    }
}
