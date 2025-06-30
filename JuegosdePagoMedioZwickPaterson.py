import random
from fractions import Fraction

random.seed(1)

class MeanPayoffDiGraph:
    """
    Esta clase se define para relaizar operaciones básicas al grafo, como puede ser, calcular sus sucesores
    """
    def __init__(self, nodos=None, arcos=None):
        self.nodos = list(nodos) if nodos else []
        self.nodo_ind = {n: i for i, n in enumerate(self.nodos)}
        self.ind_nodo = {i: n for n, i in self.nodo_ind.items()}
        self.n = len(self.nodos)
        #Matriz con la lista de los sucesores
        self.matriz_ady = [[] for _ in range(self.n)]
        self.pesos = dict()
        if arcos:
            for u, v, w in arcos:
                self.agregar_arco(u, v, w)

    def agregar_arco(self, u, v, w):
        """
        Función auxiliar para actualizar los arcos al nuevo dígrafo que se crea
        """
        i, j = self.nodo_ind[u], self.nodo_ind[v]
        self.matriz_ady[i].append((j, w))
        self.pesos[(u, v)] = w

    def _copiar(self):
        """
        Función auxliar para crear un dígrafo ponderado auxliar análogo
        """
        arcos = [(self.ind_nodo[i], self.ind_nodo[j], w) for i, lst in enumerate(self.matriz_ady) for j, w in lst]
        return MeanPayoffDiGraph(self.nodos, arcos)

    def _eliminar_arcos(self, lista_uv):
        """
        Función auxliar para eliminar arcos de los dígrafos
        """
        conj = {(self.nodo_ind[u], self.nodo_ind[v]) for u, v in lista_uv}
        n = [[] for _ in range(self.n)]
        for i in range(self.n):
            for j, w in self.matriz_ady[i]:
                if (i, j) not in conj:
                    n[i].append((j, w))
        self.matriz_ady = n

    #Las siguientes dos funciones son auxiliares; disponibles para modificar el dígrafo de entrada y que se asemeje más a la realidad

    def eliminar_nodos_aleatorios(self, porcentaje):
        cantidad = int(len(self.nodos) * porcentaje)
        if cantidad != 0:
            nodos_eliminar = set(random.sample(self.nodos, cantidad))
            self.nodos = [n for n in self.nodos if n not in nodos_eliminar]
            self.nodo_ind = {n: i for i, n in enumerate(self.nodos)}
            self.ind_nodo = {i: n for n, i in self.nodo_ind.items()}
            self.n = len(self.nodos)
            nueva_matriz = [[] for _ in range(self.n)]
            nuevos_pesos = dict()
            for (u, v), w in self.pesos.items():
                if u in self.nodo_ind and v in self.nodo_ind:
                    i, j = self.nodo_ind[u], self.nodo_ind[v]
                    nueva_matriz[i].append((j, w))
                    nuevos_pesos[(u, v)] = w
            self.matriz_ady = nueva_matriz
            self.pesos = nuevos_pesos
    
    def eliminar_arcos_aleatorias(self, porcentaje):
        total_arcos = list(self.pesos.keys())
        cantidad = int(len(total_arcos) * porcentaje)
        if cantidad == 0:
            return
        a_eliminar = set(random.sample(total_arcos, cantidad))
        self._eliminar_arcos(list(a_eliminar))
        self.pesos = {k: w for k, w in self.pesos.items() if k not in a_eliminar}


def racionalizar(valor_fraccion, n):
    """
    Esta función se usa para racionalizar el valor del juego, cumpliendo que el denominador no puede ser mayor que n.
    """
    return valor_fraccion.limit_denominator(n)


class AlgoritmoZwickPaterson:
    """
    Clase que cálcula los valores del juego de pago medio mediante el algoritmo de Zwick y Paterson.
    """
    def __init__(self, mpg):
        self.mpg = mpg
        self.k = self._calc_k()
        self.vk = [0] * self.mpg.n
        self.v = {}
        self.calcular_vk()
        self.calcular_v()

    def _calc_k(self):
        W = max(abs(w) for w in self.mpg.pesos.values())
        return 4 * (self.mpg.n ** 3) * W

    def calcular_vk(self):
        v = [0] * self.mpg.n
        for _ in range(self.k):
            v_temp = [0] * self.mpg.n
            for i in range(self.mpg.n):
                nodo = self.mpg.ind_nodo[i]
                sucesores = self.mpg.matriz_ady[i]
                if not sucesores:
                    v_temp[i] = v[i]
                else:
                    if (nodo.endswith('.1') if isinstance(nodo, str) else nodo[0].endswith('.1')): 
                        v_temp[i] = max(w + v[j] for j, w in sucesores)
                    else:
                        v_temp[i] = min(w + v[j] for j, w in sucesores)
            v = v_temp
        self.vk = v

    def calcular_v(self):
        n = self.mpg.n
        self.v = {
            self.mpg.ind_nodo[i]: racionalizar(Fraction(self.vk[i], self.k), n)
            for i in range(n)
        }

    def calc_v(self, nodo):
        return self.v.get(nodo, None)

    def aux(self, mpg_actual, nodo):
        #print(f"Nodo actual:", nodo)
        v = self.calc_v(nodo)
        i = mpg_actual.nodo_ind[nodo]
        suc = [(mpg_actual.ind_nodo[i],mpg_actual.ind_nodo[j], w) for j, w in mpg_actual.matriz_ady[i]]
        #print(f"d^+({nodo})=",len(suc))
        if len(suc) == 1:
            return suc[0]

        cant = len(suc) // 2
        arcos_a_eliminar = random.sample(suc, cant)
        arcos_conservadas = [e for e in suc if e not in arcos_a_eliminar]
        #print("Arcos en uso: ",arcos_conservadas)

        copia = mpg_actual._copiar()
        copia._eliminar_arcos([(u, v) for u, v, _ in arcos_a_eliminar])
        nuevo_calc = AlgoritmoZwickPaterson(copia)
        v_prima = nuevo_calc.calc_v(nodo)

        if v_prima == v:
            return self.aux(copia, nodo)
        else:
            alternativo = mpg_actual._copiar()
            alternativo._eliminar_arcos([(u, v) for u, v, _ in arcos_conservadas])
            #print("Arcos en uso: ",arcos_a_eliminar)
            return self.aux(alternativo, nodo)

    def estrategia_pos_optima(self, jugador):
        """
        Esta función llama al algoritmo que calcula la estrategia en base a la variación de los valores del juego, reduciendo el digrafo
        """
        end = '.1' if jugador == 1 else '.2'
        nodos = [n for n in self.mpg.nodos if (n.endswith(end) if isinstance(n, str) else n[0].endswith(end))]
        return {n: self.aux(self.mpg, n) for n in nodos}
