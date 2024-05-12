import riManage


class MontecarloClass():
    """
    dict_probs_valores : diccionario con los porcentajes y valores que retorna el Montecarlo
    cantidadRi : cantidad de tiros reservados, casi siempre se pierden por pruebas al menos un 40 % de estos datos
    """
    def __init__(self, dict_probs_valores, cantRi):
        self.montecarloProbabilidades = dict_probs_valores
        self.porcentajes_acumulados = []
        self.valores_ord = []
        self.cantidadRi = cantRi
        self.manejoRi = riManage.riManage()

    def calcularEnteroDeRi(self):
        """
        Obtiene valor entero de algun Ri
        """
        return int(100 * self.manejoRi.obtenerRandom(self.cantidadRi))
    
    def construirMontecarlo(self):
        """
        Este metodo construye el Montecarlo y ordena los porcentajes
        Calcula tambien los porcentajes acumulados
        """
        self.valores_ord = dict(sorted(self.montecarloProbabilidades.items()))

        porcentajes = list(self.valores_ord.keys())

        self.porcentajes_acumulados = []

        self.porcentajes_acumulados.append(0)
        self.porcentajes_acumulados.append(porcentajes[0])

        for i in range(len(porcentajes) - 1):

            self.porcentajes_acumulados.append(self.porcentajes_acumulados[i+1] + porcentajes[i+1])
        
        if self.porcentajes_acumulados[len(self.porcentajes_acumulados)-1] != 100:
            return False
        else: 
            return True
    
    def cambiarProbabilidades(self,probs):
        self.montecarloProbabilidades = probs
        if (self.construirMontecarlo):
            return self
        else:
            return None



    def calcularResultado(self):
        """
        Este metodo calcula donde cayó el tiro en el rango definido en el diccionario
        """
        tiro_aleatorio = self.calcularEnteroDeRi()

        #print(tiro_aleatorio)

        for i in range(len(self.porcentajes_acumulados) - 1):
            if tiro_aleatorio >= self.porcentajes_acumulados[i] and tiro_aleatorio <= self.porcentajes_acumulados[i + 1]:
                return list(self.valores_ord.values())[i]

def run(valores, m):
    montecarlo = MontecarloClass(valores, m)
    if montecarlo.construirMontecarlo():

        print("Generando Numeros...")
        
        montecarlo.manejoRi.generarNumerosHastaPasarPruebas(montecarlo.cantidadRi)

        return montecarlo

    else:
        print("Montecarlo mal formulado! -  Debe sumar 100 porciento")
        return None

"""
valores = {
    60 : 1,
    20 : 2,
    15 : 3,
    5 : 6
}

mimonte = run(valores, 100000) #minimo 100 mil, 
if mimonte!=None:
    for i in range(1000):
        print(mimonte.calcularResultado())

    
"""

