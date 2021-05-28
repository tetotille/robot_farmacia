

lista_medicamentos = []

class Medicamento():
    def __init__(self, nombre, fila, columna):
        self.nombre = nombre
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return self.nombre


def inicializar_lista(lista_medicamentos):
    f = open("data.txt", "r")

    datos = f.read().split("\n")
    for dato in datos:
        if "(" in dato:
            n = dato.find("(")
            fila = dato[n+1]
            columna = dato[n+3]
            lista_medicamentos.append(Medicamento(dato[0:n-1],fila,columna))

    f.close()

def actualizar_lista(lista_medicamentos):
    f = open("data.txt", "w")
    
    writer = ""
    for medicamento in lista_medicamentos:
        writer += str(medicamento) + " (" + str(medicamento.fila) + "," + str(medicamento.columna) + ")\n"
    f.write(writer)
    f.close()

inicializar_lista(lista_medicamentos)
