import pandas
import random

root_path = "./src/data"

def save_box(ID):
    """
    Asigna una posición en el rack para el guardado

    Entrada
    -------------
    ID          : ID del medicamento (obtenido del QR)

    Salida
    -------------
    Tupla que corresponde a la posición en la que se
    guarda el medicamento. None si no hay lugares
    libres o no se encuentra registrado el medicamento.
    """
    rack = pandas.read_csv(f"{root_path}/rack.csv", index_col = 0)
    lista = pandas.read_csv(f"{root_path}/lista.csv", index_col = 0)
    try:
        [med, qty, w, h] = lista.loc[ID].tolist()
    except KeyError: # se necesita registrar el medicamento
        print(f"Medicamento de ID {ID} no encontrado.")
        return None
    busy = rack[["pos_x", "pos_y"]].to_numpy().tolist()
    free = [[x,y] for x in range(4) for y in range(4)
            if [x,y] not in busy]
    try:
        choice = random.choice(free)
        rack = rack.append(pandas.Series(name = 7,
                                         index = ["pos_x", "pos_y"],
                                         data = choice))
        rack.to_csv(f"{root_path}/rack.csv")
        return choice
    except IndexError:
        print(f"No hay espacio para guardar el medicamento de ID {ID}.")
        return None

def search_box(ID):
    """
    Busca el medicamento en el rack

    Entrada
    -------------
    ID          : ID del medicamento (obtenido del QR)

    Salida
    -------------
    Tupla que corresponde a la posición en la que se
    encuentra el medicamento. None si no se encuentra
    el medicamento o el mismo no existe.
    """
    lista = pandas.read_csv(f"{root_path}/lista.csv", index_col = 0)
    rack = pandas.read_csv(f"{root_path}/rack.csv", index_col = 0)
    if ID not in lista.index:
        print(f"Medicamento de ID {ID} no registrado.")
        return None
    try:
        x,y = rack.loc[ID].iloc[0].tolist()
        rack[(rack.pos_x != x) | (rack.pos_y != y)]
        return (x,y)
    except KeyError:
        print(f"El medicamento de ID {ID} no está en el rack.")
        return None