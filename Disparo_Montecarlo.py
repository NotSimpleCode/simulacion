import Montecarlo as MC


class DisparoMontecarloClass():
    def __init__(self):
        self.valores_probabilidad_disparo = {
            80 : 1,  #80 % de probabilidad de crear agente guerrero
            15 : 2,  #15 % de probabilidad de crear agente curandero
            5 : 3  #5 % de probabilidad de crear agente sepulturero
        }
        self.mimonte = MC.run(self.valores_probabilidad_disparo, 100000) #100 mil datos seran 100 mil agentes creados como maximo - seran suficientes? :D
    

    def obtenerDisparo(self):
        if self.mimonte!=None: 
            return self.mimonte.calcularResultado() 
        else: return 0

    def cambiar_probabilidades(self,probs):
        self.valores_probabilidad_disparo = probs
        self.mimonte = self.mimonte.cambiarProbabilidades(self.valores_probabilidad_disparo)