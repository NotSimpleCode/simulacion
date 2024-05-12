import generacion.congruencias as GenCon
import pruebas.fast_test as FT
import math
import random
import time

class riManage():
    def __init__(self):
        self.ri_globales = []

    def leerArchivo(self,file):
        with open(file, 'r') as f:
            lista = [float(line.strip()) for line in f]
        return lista

    def obtenerSemilla(self):
        milliseconds = int(round(time.time() * 1000))
        return milliseconds

    def generarPseudoAleatorios(self,m):

        try:
            xi_generados = GenCon.contruirNumeroEspecificos(self.obtenerSemilla(),m,self.obtenerA(),self.obtenerC(m))
            ri_generados = GenCon.crearRiAvanzadoCon("",m, xi_generados)

        except:
            print("Usando numeros de reserva, cuidado con iteraciones muy largas - SOLO PARA PRUEBAS!")
            ri_generados = self.leerArchivo('ri_pruebas_aprobadas.txt')

        #print(ri_generados)

        FT.doTests(ri_generados)

        ri_aprobados = FT.getPassedData()

        self.ri_globales = ri_aprobados # Esto modificará la lista ri_globales a nivel global


    def obtenerC(self,n):
        while True:
            r = random.randint(2, n)  # Genera un número aleatorio entre 2 y n #Sera la unica ocasion que usemos el .random para obtener un coprimo aleatorio
            if math.gcd(n, r) == 1:   # Si el MCD de n y r es 1, son coprimos
                return r


    def obtenerA(self):
        primos_pequeños = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        return random.choice(primos_pequeños)



    def obtenerRandom(self,m): #metodo Santo Grial de los Ri
        self.generarNumerosHastaPasarPruebas(m)
        tempNum = self.ri_globales[0]
        self.ri_globales.pop(0) #toma el primer dato de la lista y lo borra
        return tempNum 

    def generarNumerosHastaPasarPruebas(self,m):
        while(len(self.ri_globales) == 0 ):
            self.generarPseudoAleatorios(m) 

    # Se define como obtener los aleatorios y retorna una lista.
    def ObtenerCantidadRi(self,cantidad):
        listadoRi = []

        for i in range(cantidad):
            listadoRi.append(self.obtenerRandom()) 

        return listadoRi

    def obtenerRandom50(self):
        moneda = False
        if self.obtenerRandom() >= 0.5: #teoricamente un dato asi (0.5000) no deberia pasar poker
            moneda = True
        return moneda

    """
    def obtenerRandomNormal(self,cantidad):
        return self.crearNiNormales(35,10,ObtenerCantidadRi(cantidad))

    from scipy.stats import norm

    def crearNiNormales(self,media, desv, ri):
        ni = []
        for r in ri:
            ni.append(norm.ppf(r, loc=media, scale=desv))
        return ni
    """