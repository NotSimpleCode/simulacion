from mesa import Model
from Agente import AgenteLuchador, AgenteCurador, AgenteSepulturero
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import Disparo_Montecarlo as DMC

class ModeloAgentes(Model):
    """El modelo del agente que estamos construyendo"""

    def __init__(self, numero_agentes, width, height):
        self.numeroAgentes = numero_agentes
        self.grid = MultiGrid(width, height, False)
        self.esquema = RandomActivation(self)
        self.running = True
        self.probabilidades = DMC.DisparoMontecarloClass()

        self.recolectorInformacion = DataCollector(
            {
                "Agentes con vida": ModeloAgentes.agentes_vivos,
                "Agentes Muertos": ModeloAgentes.agentes_muertos,
                "Sanadores Vivos": ModeloAgentes.agentes_curanderos,
                "Enterrados" : ModeloAgentes.agentes_enterrados,
                "Podridos" : ModeloAgentes.agentes_podridos
            }
        )

        # Creando a los agentes
        for i in range(self.numeroAgentes):

            tiro = self.probabilidades.obtenerDisparo()

            print(tiro)

            if tiro == 1:
                agenteTemporal = AgenteLuchador(i, self, self.random.randrange(4)) #4 tipos de guerreros
            elif tiro == 2:
                agenteTemporal = AgenteCurador(i, self, 0) #el tipo cero es el unico que existe
            elif tiro == 3:
                agenteTemporal = AgenteSepulturero(i, self, 0) #el tipo cero es el unico que existe para sepultureros

            self.esquema.add(agenteTemporal)

            # Agrega al agente a una celda random
            posicion_x = self.random.randrange(self.grid.width)
            posicion_y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agenteTemporal, (posicion_x, posicion_y))

    def step(self):
        """Avanza en el modelo paso por paso"""
        self.esquema.step()
        self.recolectorInformacion.collect(self)

        # Buscamos si ya hubo un ganador del combate
        vivos = ModeloAgentes.agentes_vivos(self)

        if vivos == 1:
            self.running = False

    @staticmethod
    def agentes_vivos(model) -> int:
        """Calculamos cuantos guerreros hay en batalla

        Parametros:
            modelo (ModeloAgentes): El modelo de simulacion definido

        Retorna:
            int: Numero de agentes sobre el campo de batalla que estan vivos no son curanderos y no son inmortales
        """
        return sum([1 for agente in model.esquema.agents if agente.vida > 0 and agente.curacion == None and not agente.inmortal])

    @staticmethod
    def agentes_curanderos(model) -> int:
        """Calcula el total de sanadores vivos

        Parametros:
            modelo (ModeloAgentes): El modelo de simulacion definido

        Retorna:
            int: Numero de agentes que son sanadores vivos
        """
        return sum([1 for agente in model.esquema.agents if not agente.muerto and agente.curacion != None])

    @staticmethod
    def agentes_muertos(model) -> int:
        """Calcula el total de luchadores muertos en batalla

        Parametros:
            modelo (ModeloAgentes): El modelo de simulacion definido

        Retorna:
            int: Numero de agentes que perdieron la batalla en el campo
        """
        return sum([1 for agente in model.esquema.agents if agente.muerto])
    
    @staticmethod
    def agentes_enterrados(model) -> int:
        """Calcula el total de agentes que fueron enterrados

        Parametros:
            modelo (ModeloAgentes): El modelo de simulacion definido

        Retorna:
            int: Numero de agentes que fueron enterrados RIP
        """
        return sum([1 for agente in model.esquema.agents if agente.enterrado])
    
    @staticmethod
    def agentes_podridos(model) -> int:
        """Calcula el total de luchadores que se pudrieron en batalla al no ser sepultados

        Parametros:
            modelo (ModeloAgentes): El modelo de simulacion definido

        Retorna:
            int: Numero de agentes que esperaron tanto al sepulturero que se pudrieron
        """
        return sum([1 for agente in model.esquema.agents if agente.podrido])
