from mesa import Agent
import math

DAÑO_ATAQUE = 50
VIDA_INICIAL = 100
POCION_CURACION = 20
CURACION_CURANDERO = 50

ESTRATEGIA = 1

ESTRATEGIA_ENTERRADOR = 1


def ajustar_tipo_agente(agente, tipo):
    """Ajusta los valores que usa este agente para su desarrollo

    parametros:
        agente (Agentes): El agente en cuestion
        tipo (int): el tipo de agente
    """
    if tipo == 1: #guerreros con el doble de vida y doble de daño
        agente.vida = 2 * VIDA_INICIAL
        agente.daño_ataque = 2 * DAÑO_ATAQUE
    if tipo == 2: #guerreros con la mitad de vida y mitad de daño
        agente.vida = math.ceil(VIDA_INICIAL / 2)
        agente.daño_ataque = math.ceil(DAÑO_ATAQUE / 2)
    if tipo == 3: #guerreros con un cuarto de la vida inicial y 4 veces el daño por defecto
        agente.vida = math.ceil(VIDA_INICIAL / 4)
        agente.daño_ataque = DAÑO_ATAQUE * 4


class AgenteLuchador(Agent):
    """Un agente que se desenvuelve peleando"""

    def __init__(self, unique_id, model, tipo):
        super().__init__(unique_id, model)
        self.tipo = tipo
        self.vida = VIDA_INICIAL
        self.daño_ataque = DAÑO_ATAQUE
        self.he_sido_atacado = False
        self.muerto = False
        self.contador_tiempo_muerto = 0
        self.enterrado = False
        self.curacion = None
        self.inmortal = False
        self.podrido = False
        ajustar_tipo_agente(self, tipo)

    def step(self) -> None:
        """Realiza una accion por pasos
        Creamos los estados y sus caracteristicas
        """
        # No hace nada si esta enterrado
        if self.enterrado:
            return

        # Si esta muerto por mucho tiempo se pudre
        if self.contador_tiempo_muerto > 50:
            self.podrido = True
            return

        # si esta muerto pero no enterrado aumentamos el contador de cuanto tiempo (pasos) lleva muerto
        if self.muerto and not self.enterrado:
            self.contador_tiempo_muerto += 1
            return

        # Cuando un agente fue atacado necesita un turno para volver a atacar
        if self.he_sido_atacado:
            self.he_sido_atacado = False
            return

        self.moverse()

    def atacar_o_moverse(self, celdasConAgentes, celdasDisponibles) -> None:
        """Vamos a decidir de manera pseudoaleatoria si el personaje ataca o se mueve
       

        Parametros:
            celdasConAgentes (list[Agentes]): Lista de los Agentes que esten cerca
            celdasDisponibles (list[Coordenadas]): Lista de las posibles celdas a las que puede ir
        """
        deberia_atacar = self.random.randint(0, 1)
        if deberia_atacar:
            self.atacar(celdasConAgentes)
            return

        print("He decidido el camino de la paz!")
        nueva_ubicacion = self.random.choice(celdasDisponibles)
        self.model.grid.move_agent(self, nueva_ubicacion)

    def atacar(self, celdasConAgentes) -> None:
        """Controlamos que pasa cuando un agente ataca
        Buscara agentes cercanos y elige uno random al cual atacar

        Parametros:
            celdasConAgentes (list[Agentes]): La lista de cuando busca agentes cercanos a su celda
        """
        agentePorAtacar = self.random.choice(celdasConAgentes)
        if agentePorAtacar.inmortal == False:
            agentePorAtacar.vida -= self.daño_ataque
        agentePorAtacar.he_sido_atacado = True
        if agentePorAtacar.vida <= 0:
            agentePorAtacar.muerto = True
        print("Guerraaaaaaa!!!!!")

    def moverse(self) -> None:
        """Controlamos como sera el movimiento o siguiente accion
        Puede moverse, atacar o curarse
        """

        tomar_pocion = self.random.randint(0, 100)
        if tomar_pocion == 1:
            self.vida += POCION_CURACION
            print("Mmm deliciosa pocion! *Sonido de honguito de mario*")
            return

        celdasDisponibles = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        celdasConAgentes = []
        # buscamos agentes alrededor de la celda del agente que se esta moviendo
        for celda in celdasDisponibles:
            lista_otros_agentes = self.model.grid.get_cell_list_contents([celda])
            if len(lista_otros_agentes):
                for agente in lista_otros_agentes:
                    if not agente.muerto:
                        celdasConAgentes.append(agente)

        # Si existe algun agente vecino al agente que se esta moviendo
        if len(celdasConAgentes):
            if ESTRATEGIA == 1:
                self.atacar_o_moverse(celdasConAgentes, celdasDisponibles)
            else:
                self.atacar(celdasConAgentes)
        else:
            nueva_posicion = self.random.choice(celdasDisponibles)
            self.model.grid.move_agent(self, nueva_posicion)


class AgenteCurador(Agent):
    """Un agente que se desenvuelve curando a aliados"""

    def __init__(self, unique_id, model, tipo):
        super().__init__(unique_id, model)
        self.tipo = tipo
        self.vida = VIDA_INICIAL * 8 #8 veces la vida inicial para que dure mas en el campo de batalla
        self.curacion = CURACION_CURANDERO
        self.he_sido_atacado = False
        self.muerto = False
        self.contador_tiempo_muerto = 0
        self.enterrado = False
        self.inmortal = False
        self.podrido = False
        #ajustar_tipo_agente(self, tipo) #si se quieren hacer varios tipos de curanderos editar

    def step(self) -> None:
        """Realiza una accion por pasos
        Creamos los estados y sus caracteristicas
        """
        # No hace nada si esta enterrado
        if self.enterrado:
            return

        # Si esta muerto por mucho tiempo se pudre
        if self.contador_tiempo_muerto > 50:
            self.podrido = True
            return

        # si esta muerto pero no enterrado aumentamos el contador de cuanto tiempo (pasos) lleva muerto
        if self.muerto and not self.enterrado:
            self.contador_tiempo_muerto += 1
            return

        # Cuando un curandero es atacado debe esperar un turno para volver a curar
        if self.he_sido_atacado:
            self.he_sido_atacado = False
            return

        self.realizar_accion()

    def curar_o_moverse(self, celdasConAgentes, celdasDisponibles) -> None:
        """Vamos a decidir de manera pseudoaleatoria si el personaje cura a alguien o se mueve
       

        Parametros:
            celdasConAgentes (list[Agentes]): Lista de los Agentes que esten cerca
            celdasDisponibles (list[Coordenadas]): Lista de las posibles celdas a las que puede ir
        """
        deberia_curar = self.random.randint(0, 1)
        if deberia_curar:
            self.curar(celdasConAgentes)
            return

        print("He decidido no curar! :(")
        nueva_ubicacion = self.random.choice(celdasDisponibles)
        self.model.grid.move_agent(self, nueva_ubicacion)

    def curar(self, celdasConAgentes) -> None:
        """Controlamos que pasa cuando un agente cura
        Buscara agentes cercanos y elige uno random al cual curar

        Parametros:
            celdasConAgentes (list[Agentes]): La lista de cuando busca agentes cercanos a su celda
        """
        agentePorCurar = self.random.choice(celdasConAgentes)
        agentePorCurar.vida += self.curacion
        agentePorCurar.he_sido_atacado = True #evita que un agente recien curado ataque por un 1 turno
        if agentePorCurar.vida <= 0:
            agentePorCurar.muerto = True
        print("Te he curado")

    def realizar_accion(self) -> None:
        """Controlamos como sera el movimiento o siguiente accion
        Puede moverse o curar
        """

        celdasDisponibles = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        celdasConAgentes = []
        # buscamos agentes alrededor de la celda del agente que se esta moviendo
        for celda in celdasDisponibles:
            lista_otros_agentes = self.model.grid.get_cell_list_contents([celda])
            if len(lista_otros_agentes):
                for agente in lista_otros_agentes:
                    if not agente.muerto:
                        celdasConAgentes.append(agente)

        # Si existe algun agente vecino al agente que se esta moviendo
        if len(celdasConAgentes):
            if ESTRATEGIA == 1:
                self.curar_o_moverse(celdasConAgentes, celdasDisponibles)
            else:
                self.curar(celdasConAgentes)
        else:
            nueva_posicion = self.random.choice(celdasDisponibles)
            self.model.grid.move_agent(self, nueva_posicion)


class AgenteSepulturero(Agent):
    """Un agente que se desenvuelve enterrando muertos y quizas algo mas..."""

    def __init__(self, unique_id, model, tipo):
        super().__init__(unique_id, model)
        self.tipo = tipo
        self.vida = VIDA_INICIAL 
        self.curacion = None
        self.he_sido_atacado = False
        self.muerto = False
        self.contador_tiempo_muerto = 0
        self.enterrado = False
        self.podrido = False
        self.inmortal = True
        
        #ajustar_tipo_agente(self, tipo) #si se quieren hacer varios tipos de curanderos editar

    def step(self) -> None:
        """Realiza una accion por pasos
        Creamos los estados y sus caracteristicas en este caso no tiene alteraciones de estado, solo entierra muertos
        """
        global ESTRATEGIA_ENTERRADOR

        if self.he_sido_atacado: #si lo atacan hace cosas raras...
            self.he_sido_atacado = False
            ESTRATEGIA_ENTERRADOR = 2
            self.realizar_accion()
            return

        self.realizar_accion()

    def enterrar_o_moverse(self, celdasConAgentesMuertos, celdasDisponibles) -> None:
        """Vamos a decidir de manera pseudoaleatoria si el personaje entierra a alguien o se mueve
       

        Parametros:
            celdasConAgentesMuertos (list[Agentes]): Lista de los Agentes que esten cerca que ya hayan muerto
            celdasDisponibles (list[Coordenadas]): Lista de las posibles celdas a las que puede ir
        """
        deberia_enterrar = self.random.randint(0, 5) #él tiene muchas ganas de enterrar por lo que solo 1/6 de las veces no enterrará a nadie
        if deberia_enterrar != 5:
            self.enterrar(celdasConAgentesMuertos)
            return

        print("He decidido no enterrar a nadie")
        nueva_ubicacion = self.random.choice(celdasDisponibles)
        self.model.grid.move_agent(self, nueva_ubicacion)

    def enterrar(self, celdasConAgentesMuertos) -> None:
        """Controlamos que pasa cuando un agente entierra
        Buscara agentes cercanos y elige uno random al cual enterrar si esta muerto

        Parametros:
            celdasConAgentes (list[Agentes]): La lista de cuando busca agentes cercanos a su celda
        """
        
        agentePorEnterrar = self.random.choice(celdasConAgentesMuertos)
        
        agentePorEnterrar.enterrado = True
        

        print("Que en paz descanses - RIP")

    def revivir(self, celdasConAgentesMuertos) -> None:
        """Controlamos que pasa cuando un agente sepulturero explota
        Buscara agentes cercanos y elige uno random al cual revivir

        Parametros:
            celdasConAgentesMuertos (list[Agentes]): La lista de cuando busca agentes cercanos a su celda
        """
        
        agentePorRevivir = self.random.choice(celdasConAgentesMuertos)
        
        agentePorRevivir.muerto = False
        agentePorRevivir.vida = VIDA_INICIAL


        print("Benditos sean los calabozos que forjaron mi pala por la cual hoy te elevas!!! :D Bienvenido de vuelta!")

    def realizar_accion(self) -> None:
        """Controlamos como sera el movimiento o siguiente accion
        Puede moverse o enterrar
        """
        global ESTRATEGIA_ENTERRADOR

        celdasDisponibles = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        celdasConAgentesMuertos = []
        # buscamos agentes alrededor de la celda del agente que se esta moviendo
        for celda in celdasDisponibles:
            lista_otros_agentes = self.model.grid.get_cell_list_contents([celda])
            if len(lista_otros_agentes):
                for agente in lista_otros_agentes:
                    if agente.muerto and not agente.enterrado and not agente.podrido:
                        celdasConAgentesMuertos.append(agente)

        # Si existe algun agente vecino al agente que se esta moviendo
        if len(celdasConAgentesMuertos):
            if ESTRATEGIA_ENTERRADOR == 1:
                self.enterrar_o_moverse(celdasConAgentesMuertos, celdasDisponibles)
            elif ESTRATEGIA_ENTERRADOR == 2:
                ESTRATEGIA_ENTERRADOR = 1
                self.revivir(celdasConAgentesMuertos)
            else:
                self.enterrar(celdasConAgentesMuertos)
        else:
            ESTRATEGIA_ENTERRADOR = 1
            nueva_posicion = self.random.choice(celdasDisponibles)
            self.model.grid.move_agent(self, nueva_posicion)