String x;
int pushButton = 53;
int estado = 0;
int marcaEstado = 0;

int LED_rojo = 52;
int LED_verde = 51;


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
