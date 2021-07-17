root_path = '.'
lista_medicamentos = []

class Medicamento():
    '''
    Clase Medicamento

    Atributos
    -------------
    nombre   : nombre del medicamento
    fila     : 0<=fila<=3, fila en el rack
    columna  : 0<=columna<=3, columna en el rack

    Métodos
    -------------
    ver_lugar: imprime en la consola la posición del medicamento
    '''
    def __init__(self, nombre, fila, columna):
        self.nombre = nombre
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return self.nombre
    
    def ver_lugar(self):
        return "("+str(self.fila)+","+str(self.columna)+")"


def inicializar_lista(lista_medicamentos):
    f = open(f"{root_path}/data.txt", "r")

    datos = f.read().split("\n")
    for dato in datos:
        if "(" in dato:
            n = dato.find("(")
            fila = dato[n+1]
            columna = dato[n+3]
            lista_medicamentos.append(Medicamento(dato[0:n-1],fila,columna))

    f.close()

def actualizar_lista(lista_medicamentos):
    f = open(f"{root_path}/data.txt", "w")
    
    writer = ""
    for medicamento in lista_medicamentos:
        writer += str(medicamento) + " (" + str(medicamento.fila) + "," + str(medicamento.columna) + ")\n"
    f.write(writer)
    f.close()
    
def buscar_medicamento(nombre):
    lugar = None
    for medicamento in lista_medicamentos:
        lugar = medicamento.ver_lugar() if str(medicamento)==nombre else lugar
    return lugar


inicializar_lista(lista_medicamentos)
