from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import NumberInput

from Modelo import ModeloAgentes
from mesa.visualization.modules import CanvasGrid, ChartModule

NUMERO_CELDAS = 20

PIXELES_CANVAS_X = 1400
PIXELES_CANVAS_Y = 1100

parametrosSimulacion = {
    "numero_agentes": NumberInput(
        "Cuantos agentes quieres poner en batalla?", value=NUMERO_CELDAS
    ),
    "width": NUMERO_CELDAS,
    "height": NUMERO_CELDAS,
}

nombres_guerreros = {
    0 : "Normal",
    1 : "Samurai",
    2 : "Minion",
    3 : "Ninja"
}

def imagenAgente(agente):
    # Si el agente esta enterrado lo pone de color blanco para que parezca que desaparecio
    if agente.enterrado:
        imagen = {
            "Shape": "circle",
            "Filled": "true",
            "Color": "white",
            "r": 0.01,
            "text": "",
            "Layer": 0,
            "text_color": "black",
        }
        return imagen
    
    #si se pudre lo ponemos cafe
    if agente.podrido:
        imagen = {
            "Shape": "circle",
            "Filled": "true",
            "Color": "brown",
            "r": 0.1,
            "Layer": 6
        }
        return imagen

    # Como se debe ver comunmente un agente
    imagen = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "text": f"{agente.vida} tipo: {nombres_guerreros[agente.tipo]}",
        "text_color": "black",
    }

    # Si esta muerto el agente lo ponemos de color negro
    if agente.muerto:
        imagen["Shape"] = "rect"
        imagen["w"] = 0.2
        imagen["h"] = 0.2
        imagen["Color"] = "black"
        imagen["Layer"] = 1

        return imagen
    
    

    # Si el agente esta vivo, ajustamos su tamaño color y demas caracteristicas segun su tipo
    if agente.tipo == 0:
        imagen["r"] = 0.2
        if agente.curacion != None:
            imagen["r"] = 1
            imagen["Color"] = "gray"
            imagen["text"] = f"vida : {agente.vida} tipo: sanador: {agente.curacion}"
        if agente.inmortal:
            imagen["r"] = 0.5
            imagen["Color"] = "purple"
            imagen["text"] = f"vida : {agente.vida} tipo: sepulturero"

    elif agente.tipo == 1:
        imagen["r"] = 0.4

    elif agente.tipo == 2:
        imagen["r"] = 0.6

    elif agente.tipo == 3:
        imagen["r"] = 0.8
    


    # Si el agente tiene mas de 50 de vida su color es verde, sino es rojo, avisando del peligro de muerte
    if agente.vida > 50 and agente.curacion == None and agente.inmortal == False:
        imagen["Color"] = "green"
        imagen["Layer"] = 1

    else: # si tienen menos de 50 de vida
        imagen["Color"] = "red"
        imagen["Layer"] = 2
        
        #si es sanador
        if agente.curacion != None and agente.vida > 50:
            imagen["Color"] = "orange"
            imagen["Layer"] = 3
        #si es inmortal
        if agente.inmortal:
            imagen["Color"] = "purple"
            imagen["Layer"] = 4

    return imagen


grid = CanvasGrid(
    imagenAgente,
    NUMERO_CELDAS,
    NUMERO_CELDAS,
    PIXELES_CANVAS_X,
    PIXELES_CANVAS_Y,
)

grafica_datos = ChartModule(
    [
        {"Label": "Agentes con vida", "Color": "green"},
        {"Label": "Agentes Muertos", "Color": "red"},
        {"Label": "Sanadores Vivos", "Color": "gray"}
    ],
    canvas_height=300,
    data_collector_name="recolectorInformacion"
)


servidor_juego = ModularServer(
    ModeloAgentes, [grid, grafica_datos], "Modelo Lucha", parametrosSimulacion
)
servidor_juego.port = 8521
servidor_juego.launch()
