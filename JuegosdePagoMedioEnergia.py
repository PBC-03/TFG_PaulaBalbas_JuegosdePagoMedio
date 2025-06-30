import random
from fractions import Fraction
import math


#Definimos el TOP, este es el valor siguiente a MG

TOP = 'T'

#Definimos la clase para saturar los signos de menor, menor o igual, resta y comparaciones con la cota T

class Value:
    """
    Esta clase satura los símbolos menos, menor y menor igual usando la cota MG que viene definida por el juego de energía.
    Además, hace que el 'infinito'sea denotado por T.
    """
    def __init__(self, val, MG):
        self.val = val
        self.MG = MG
    
    def __sub__(self, w):
        """
        Aplica el operador ominus como si fuese la resta cotidiana.
        """
        if self.val == TOP or self.val - w > self.MG:
            return Value(TOP, self.MG)
        else:
            return Value(max(0, self.val - w), self.MG)
    
    def __lt__(self, otro):
        """
        Esta función modifica el operador menor que (<) como el operador de orden total estricto.
        """
        if not isinstance(otro, Value):
            otro = Value(otro, self.MG)
        if self.val == TOP: #T es mayor o igual que todo, por tanto, T < otra cosa es siempre False
            return False
        if otro.val == TOP:
            return True
        return self.val < otro.val
    
    def __le__(self, otro):
        """
        Esta función modifica el operador menor o igual que (<=) como el operador de orden total.
        """
        if not isinstance(otro, Value):
            otro = Value(otro, self.MG)
        if self.val == TOP: #T es mayor o igual que todo, por tanto, hay que ver si el otro elemento es tmabién T
            return otro.val == TOP
        if otro.val == TOP:
            return True
        return self.val <= otro.val
    
    def __repr__(self):
        """
        Hace que el 'infinito' se represente como T y si no, que devuelva el valor en número.
        """
        if self.val == TOP:
            return "⊤"  
        else:
            return str(self.val)
        
    def is_top(self):
        """
        Con esta función se puede comprobar si el valor es T o no.
        """
        return self.val == TOP
    
#Una vez realizados los cambios oportunos en los operadores, se va a pasar a la construcción del alñgoritmo que resuelve juegos de energía.

class EnergyGameAlg1:
    """
    Esta clase genera la jugada posicional óptima del jugador 1 del juego de pago medio mediante la resolución del juego de energía.
    """
    def __init__(self, nodos, arcos, V1, V2):
        self.nodos = nodos
        self.V1 = V1
        self.V2 = V2

        #Calculo de sucesores y predecesores
        #Lista de los sucesores de cada uno y sus respectivos pesos
        self.suc  = {n: [] for n in nodos}
        #Lista de predecesores con sus respectivos pesos
        self.pred = {n: [] for n in nodos}
        for u, v, w in arcos:
            self.suc[u].append((v, w))
            self.pred[v].append((u, w))
        self.MG = self.calc_MG()

    def calc_MG(self):
        return sum(max(-w, 0) for u in self.nodos for (_, w) in self.suc[u])
    
    def algoritmo1(self):
        """
        Esta función calcula y soluciona las incosistencias existentes.
        """
        L = []
        #print(f"L inicial:", L)
        #Inicializar L 
        #Si u pertenece al J1: Se mira si TODAS las aristas salientes de u son negativas
        #Si u pertenece al J2: Se mira si ALGUNA de las salientes es negativa
        for u in self.V1: 
            if not self.suc[u] or all(w < 0 for (_, w) in self.suc[u]): 
                L.append(u)
        for u in self.V2:
            if any(w < 0 for (_, w) in self.suc[u]):
                L.append(u)

        #Inicializar f y count
        f = {u: Value(0, self.MG) for u in self.nodos}
        #print(f"f inicial:", f)
        count = {u: 0 for u in self.V1}
        #print(f"count inicial:", count)
        for u in self.V1:
            if u not in L:
                for (v, w) in self.suc[u]:
                    if (f[v] - w) <= f[u]:
                        count[u] += 1

        #Bucle donde se actualizan los valores de L, es decir, las inconsistencias
        while L:
            u = L.pop(0)
            old = f[u]

            #Aplicación del operador lifting
            candidatos = [f[v] - w for (v, w) in self.suc[u]]
            if u in self.V1:
                f[u] = min(candidatos)
            else:
                f[u] = max(candidatos)

            #Actualización del contador si u pertenece al J1
            if u in self.V1:
                count[u] = sum(1 for (v, w) in self.suc[u] if (f[v] - w) <= f[u])

            #Actualización de nuevas inconsistencias a los predecesores del nodo del que se le ha solucionado esta
            for (p, w) in self.pred[u]:
                if f[p] < (f[u] - w):
                    if p in self.V1:
                        if (old - w) <= f[p]:
                            count[p] -= 1
                        if count[p] <= 0 and p not in L:
                            L.append(p)
                    elif p not in L:
                        L.append(p)
            # print("Estudiando inconsistencias en", u)
            # print("L actual:",L)
            # print("f actual:",f)
            # print("count actual:",count)
        return f    
    
    def estrategia(self, f):
        """
        Una vez calculadas las inconsistencias, se calcula la estrategia óptima posicional de cada nodo del jugador 1.
        """
        sigma = {}
        for u in self.V1:
            #Si f[u] llega al tope, este no será candidato a ser opción en la jugada
            if not f[u].is_top():
                candidatos = []
                for (v, w) in self.suc[u]:
                    if not f[v].is_top():
                        candidatos.append((v, f[v] - w))

                    if candidatos:
                        #Comparamos los pesos de los candidatos
                        sigma[u] = min(candidatos, key=lambda x: x[1])[0]
        return sigma
    

class MeanPayoffEnergyGameAlg2:
    """
    Clase que resuelve el juego de pago medio en base a los juegos de energía mediante la clase anterior.
    """
    def __init__(self, nodos, arcos, V1, V2):
        self.nodos = nodos
        self.arcos = arcos
        self.W = max(abs(w) for _, _, w in arcos) if arcos else 0 #Añado el 0 porque si no da error al llamar a un subgrafo vacío
        #Generar S
        self.S = self.gen_S()
        #print("S=",self.S)
        self.V1 = V1
        self.V2 = V2

    def gen_S(self):
        S=set()
        for m in range(1, len(self.nodos) + 1):
            for p in range(-m * self.W, m * self.W + 1):
                S.add(Fraction(p,m))
        return sorted(S)

    def calcular_a1_a2(self, frac1, frac2):
        a1_aux = set()
        a2_aux = set()
        for l in range(1, len(self.nodos)+1):
            min_q1 = math.ceil(l * frac1)
            max_q1 = math.floor((l * frac1 + l * frac2) / 2)
            min_q2 = math.ceil((l * frac1 + l * frac2) / 2)
            max_q2 = math.floor(l * frac2)
            for q in range(min_q1, max_q1 + 1):
                a1_aux.add(Fraction(q, l))
            for q in range(min_q2, max_q2 + 1):
                a2_aux.add(Fraction(q, l))
        #Si no se han añadido valores de a1 o a2, devuelvo el valor fraci
        a1 = max(a1_aux) if a1_aux else frac1
        a2 = min(a2_aux) if a2_aux else frac2
        return a1, a2

    def reponderar(self, l, q, invertir=False, arcos=None):
        """
        Función para reponderar los grafos y cambiar los conjuntos de vértices, si fuera necesario.
        """
        if arcos is None:
            arcos_n = self.arcos
        else:
            arcos_n = arcos
        if invertir:
            return [(u, v, -l * w + q) for (u, v, w) in arcos_n]
        else:
            return [(u, v, l * w - q) for (u, v, w) in arcos_n]

    def algoritmo2(self, frac1, frac2, valores=None, estrategia_J1=None, estrategia_J2=None, nodos=None, arcos=None, V1=None, V2=None):
        """
        Función cuerpo del algortimo 2 que susa el 1 para el cálculo de los valores del juego y su respectiva estrategia.
        """
        #Primero damos valores si estos parámetros fueran vacíos, como ocurre en la primera iteración
        if valores is None:
            valores = {}
        if estrategia_J1 is None:
            estrategia_J1 = {}
        if estrategia_J2 is None:
            estrategia_J2 = {}
        if nodos is None:
            nodos = list(self.nodos)
        if arcos is None:
            arcos = list(self.arcos)
        if V1 is None:
            V1 = self.V1
        if V2 is None:
            V2 = self.V2

        #Calculamos los límites de las particiones de S
        a1, a2 = self.calcular_a1_a2(frac1, frac2)
        #print(f"Intervalo actual:[{a1},{a2}]")
        
        #Añadimos esta condición para evitar recursiones infinitas
        if a1 == frac1 and a2 == frac2:
            return valores, estrategia_J1, estrategia_J2

        #Construcción del juego de energía para aplicar el algortimo 1
        l1, q1 = a1.denominator, a1.numerator
        l2, q2 = a2.denominator, a2.numerator

        G1 = EnergyGameAlg1(nodos, self.reponderar(l1, q1, False, arcos), V1, V2)
        f1 = G1.algoritmo1()
        sigma1_a1 = G1.estrategia(f1)

        G2 = EnergyGameAlg1(nodos, self.reponderar(l1, q1, True, arcos), V2, V1)
        f2 = G2.algoritmo1()
        sigma2_a1 = G2.estrategia(f2)  

        G3 = EnergyGameAlg1(nodos, self.reponderar(l2, q2, False, arcos), V1, V2)
        f3 = G3.algoritmo1()
        sigma1_a2 = G3.estrategia(f3)

        G4 = EnergyGameAlg1(nodos, self.reponderar(l2, q2, True, arcos), V2, V1)
        f4 = G4.algoritmo1()
        sigma2_a2 = G4.estrategia(f4)
        for u in nodos:
            if not f1[u].is_top() and not f2[u].is_top():
                valores[u] = a1
                if u in V1 and u in sigma1_a1:
                    estrategia_J1[u] = sigma1_a1[u]
                if u in V2 and u in sigma2_a1:
                    estrategia_J2[u] = sigma2_a1[u]
            elif not f3[u].is_top() and not f4[u].is_top():
                valores[u] = a2
                if u in V1 and u in sigma1_a2:
                    estrategia_J1[u] = sigma1_a2[u]
                if u in V2 and u in sigma2_a2:
                    estrategia_J2[u] = sigma2_a2[u]

        #Creamos los subconjuntos para la recursión
        V_menor_a1 = {u for u in nodos if f1[u].is_top()}
        V_mayor_a2 = {u for u in nodos if f4[u].is_top()}

        V1_menor_a1 = [v for v in V1 if v in V_menor_a1]
        V2_menor_a1 = [v for v in V2 if v in V_menor_a1]
        V1_mayor_a2 = [v for v in V1 if v in V_mayor_a2]
        V2_mayor_a2 = [v for v in V2 if v in V_mayor_a2]

        if V_menor_a1 and a1 > frac1:
            sub_arcos = [(u, v, w) for (u, v, w) in arcos if u in V_menor_a1 and v in V_menor_a1]
            #print(f"V_menor_a1={list(V_menor_a1)} con arcos={sub_arcos}")
            self.algoritmo2(frac1, a1, valores, estrategia_J1, estrategia_J2, list(V_menor_a1), sub_arcos, V1_menor_a1, V2_menor_a1)

        if V_mayor_a2 and a2 < frac2:
            sub_arcos = [(u, v, w) for (u, v, w) in arcos if u in V_mayor_a2 and v in V_mayor_a2]
            #print(f"V_mayor_a2={list(V_mayor_a2)} con arcos={sub_arcos}")
            self.algoritmo2(a2, frac2, valores, estrategia_J1, estrategia_J2, list(V_mayor_a2), sub_arcos, V1_mayor_a2, V2_mayor_a2)

        return valores, estrategia_J1, estrategia_J2
