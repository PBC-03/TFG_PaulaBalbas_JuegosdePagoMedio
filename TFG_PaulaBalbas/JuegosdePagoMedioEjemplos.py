#En este script se encuentran los ejemplos usados para el TFG
import random 
from itertools import product
import JuegosdePagoMedioZwickPaterson 
import JuegosdePagoMedioEnergia

random.seed(1)

#Ejemplo propio
nodos_ej1 = ['a.1','b.1','c.1','x.2','y.2']
arcos_ej1 = [
    ('a.1','b.1', 3), ('x.2','a.1', 1), ('y.2','b.1', 2),
    ('y.2','x.2', 0), ('x.2','y.2', -5), ('b.1','y.2', -2),
    ('b.1','a.1', 1), ('c.1','x.2', 2), ('c.1','a.1', -2),
]

##############################################################################################
#Ejemplo Central eléctrica y la generación de energía

nodos_ej2 = ['A.1', 'R.1', 'F.1', 'N.1', 'R.2', 'F.2', 'N.2']

arcos_ej2_nombre = [
    ('A.1', 'N.2'), ('N.2', 'N.1'), ('N.2', 'R.1'), ('R.1', 'F.2'), ('R.1', 'N.2'),
    ('R.2', 'R.1'), ('R.2', 'A.1'), ('N.1', 'F.2'), ('F.2', 'N.1'), ('F.2', 'F.1'),
    ('F.1', 'R.2')
]

#Función de coste, según si nodo es del jugador 1 (.1) o 2 (.2)
def fcoste_elect(nodo):
    if nodo.startswith('F'):
        capacidad = random.uniform(350, 400)
        contaminacion = random.uniform(8, 10)
        precio = 80
    elif nodo.startswith('N'):
        capacidad = random.uniform(400, 500)
        contaminacion = random.uniform(4, 7)
        precio = 60
    elif nodo.startswith('R'):
        capacidad = random.uniform(100, 250)
        contaminacion = random.uniform(1, 3)
        precio = 35
    else:  #Apagado
        return -round(random.uniform(0, 20))
    
    if nodo.endswith('.1'):  
        return round(capacidad / contaminacion - precio)
    else:  
        return round(precio * contaminacion  / capacidad * 10)

#Generar arcos con sus costes según las arcos válidas
arcos_ej2 = []
for u, v in arcos_ej2_nombre:
    if u in nodos_ej2 and v in nodos_ej2:
        coste = fcoste_elect(v)
        arcos_ej2.append((u, v, coste))

##############################################################################################
#Ejemplo ciberseguridad

estados = ['S', 'P', 'N', 'D', 'F', 'R']

nodos_ej3= [f"{e}.1" for e in estados] + [f"{e}.2" for e in estados]

transiciones_invalidas = {
    ('S', 'F'), ('S', 'D'), ('S', 'R'),('F', 'S'), ('P', 'S'), ('N', 'F')}

arcos_ej3_nombre = []
for e1 in estados:
    for e2 in estados:
        if (e1, e2) not in transiciones_invalidas:
            arcos_ej3_nombre.append((f"{e1}.1", f"{e2}.2"))
            arcos_ej3_nombre.append((f"{e2}.2", f"{e1}.1"))

def fcoste_ciber(nodo):
    if nodo.startswith('S'):
        return 0
    elif nodo.startswith('P'):
        return 2
    elif nodo.startswith('N'):
        return -3
    elif nodo.startswith('D'):
        return 1
    elif nodo.startswith('F'):
        return 5
    elif nodo.startswith('R'):
        return -1
    else:
        return 0

arcos_ej3 = []
for u, v in  arcos_ej3_nombre:
    coste = fcoste_ciber(v)
    arcos_ej3.append((u, v, coste))

##############################################################################################
#Ejemplo logística de un supermercado
"""
Esta configurado de la manera más simple, se deben cambiar esto parámetros a gusto de cada uno.
"""

nodos_ej4_nombre = ['Aa.1', 'Aa.2', 'Am.1', 'Am.2', 'Ab.1', 'Ab.2',
            'Da.1', 'Da.2', 'Dm.1', 'Dm.2', 'Db.1', 'Db.2',
            'Ea.1', 'Ea.2', 'Em.1', 'Em.2', 'Eb.1', 'Eb.2']

grupos = {
    'A_1': [n for n in nodos_ej4_nombre if n.startswith('A') and n.endswith('.1')],
    'A_2': [n for n in nodos_ej4_nombre if n.startswith('A') and n.endswith('.2')],
    'D_1': [n for n in nodos_ej4_nombre if n.startswith('D') and n.endswith('.1')],
    'D_2': [n for n in nodos_ej4_nombre if n.startswith('D') and n.endswith('.2')],
    'E_1': [n for n in nodos_ej4_nombre if n.startswith('E') and n.endswith('.1')],
    'E_2': [n for n in nodos_ej4_nombre if n.startswith('E') and n.endswith('.2')]
}

# Generar tuplas de nodos
tuplas_1 = list(product(grupos['A_1'], grupos['D_1'], grupos['E_1']))
tuplas_2 = list(product(grupos['A_2'], grupos['D_2'], grupos['E_2']))
todos_nodos = tuplas_1 + tuplas_2

# Funciones auxiliares del modelo logístico
def demanda(D):
    if 'Da' in D: return round(random.uniform(150, 200))
    if 'Dm' in D: return round(random.uniform(80, 120))
    if 'Db' in D: return round(random.uniform(30, 70))

def cantpedido(E):
    if E == 'Ea.2': return round(random.uniform(40, 100))
    if E == 'Em.2': return round(random.uniform(25, 39))
    if E == 'Eb.2': return round(random.uniform(0, 24))

def envio(A, E):
    return 0 if A == 'Ab.2' or E == 'Eb.2' else 5000

def rho(A, D):
    if A == 'Aa.2': return 480 * demanda(D)
    if A == 'Am.2': return 240 * demanda(D)
    if A == 'Ab.2': return 0

def incidencias(A, E):
    if A == 'Aa.1' and E == 'Ea.1': return 0
    if A == 'Am.1' or E == 'Em.1': return 2
    if A == 'Ab.1' and E == 'Eb.1': return 10
    if A == 'Ab.1': return 5
    return 1

def parametro(E):
    return {'Ea.1': 10, 'Em.1': 30, 'Eb.1': 50}.get(E, 20)

def f_coste(A, D, E):
    d = demanda(D)
    if A.endswith('.2'):
        c = cantpedido(E)
        if E == 'Eb.2': return round((70 * c**2)/(2 * d) + 150 * c + rho(A, D))
        if E == 'Em.2': return round((4.6 * c**3)/(2 * d**2) + envio(A, E) + 150 * 0.95 * c + rho(A, D))
        if E == 'Ea.2': return round((4.6 * c**3)/(2 * d**2) + envio(A, E) + 150 * 0.89 * c + rho(A, D))
    else:
        return round(parametro(E) * d + 1000 * incidencias(A, E))


arcos_ej4_sinescalar = []
for u, v in product(todos_nodos, repeat=2):
    if u != v:
        if (u[0].endswith('.1') and v[0].endswith('.2')) or (u[0].endswith('.2') and v[0].endswith('.1')):
            A, D, E = v
            costo = f_coste(A, D, E)
            arcos_ej4_sinescalar.append((u, v, costo))


#Escalar pesos entre A Y B
valores_costes = [w for _, _, w in arcos_ej4_sinescalar]
min_val, max_val = min(valores_costes), max(valores_costes)

def escalar(valor, a, b, A, B):
    if a != b:  
        return round(A + (valor - a) * (B - A) / (b - a)) 
    else:
        return A

# Estas funciones eliminan un porcentaje de arcos y nodos del total para asemejar el ejemplo a la vida real.
def eliminar_arcos(arcos, porcentaje):
    cantidad = int(len(arcos) * porcentaje)
    if cantidad == 0:
        return arcos
    eliminar_uv = random.sample([(u, v) for u, v, _ in arcos], cantidad)
    return [(u, v, w) for (u, v, w) in arcos if (u, v) not in eliminar_uv]

def eliminar_nodos_aleatorios(nodos, arcos, porcentaje):
    cantidad = int(len(nodos) * porcentaje)
    if cantidad == 0:
        return nodos, arcos
    nodos_eliminar = set(random.sample(nodos, cantidad))
    nodos_filtrados = [n for n in nodos if n not in nodos_eliminar]
    arcos_filtrados = [(u, v, w) for (u, v, w) in arcos if u in nodos_filtrados and v in nodos_filtrados]
    return nodos_filtrados, arcos_filtrados

#Parámetros para escalar
A = -100
B = 100
porcentaje_nodos = 0.1
arcos_ej4_escalados = [(u, v, escalar(w, min_val, max_val, A, B)) for (u, v, w) in arcos_ej4_sinescalar]

nodos_ej4, arcos_ej4 = eliminar_nodos_aleatorios(todos_nodos, arcos_ej4_escalados, porcentaje_nodos)

porcentaje_arcos = 0.05
arcos_ej4 = eliminar_arcos(arcos_ej4, porcentaje_arcos)


print("Selecciona un ejemplo:")
print("1. Ejemplo propio")
print("2. Central eléctrica")
print("3. Ciberseguridad")
print("4. Logística supermercado")
opcion = input("Introduce el número del ejemplo (1-4) que se quiere comprobar: ")

# Asignar nodos y arcos según la opción
if opcion == '1':
    nodos, arcos = nodos_ej1, arcos_ej1
elif opcion == '2':
    nodos, arcos = nodos_ej2, arcos_ej2
elif opcion == '3':
    nodos, arcos = nodos_ej3, arcos_ej3
elif opcion == '4':
    nodos, arcos = nodos_ej4, arcos_ej4
else:
    raise ValueError("Opción inválida. Debes elegir un número del 1 al 4.")

#Imprimimos que arcos se han creado junto a sus pesos
for u in arcos:
    print(u)

G = JuegosdePagoMedioZwickPaterson.MeanPayoffDiGraph(nodos, arcos)

mpgZP = JuegosdePagoMedioZwickPaterson.AlgoritmoZwickPaterson(G)

V1 = [n for n in nodos if (n.endswith('.1') if isinstance(n, str) else n[0].endswith('.1'))]
V2 = [n for n in nodos if (n.endswith('.2') if isinstance(n, str) else n[0].endswith('.2'))]
EG = JuegosdePagoMedioEnergia.EnergyGameAlg1(nodos, arcos, V1, V2)
f = EG.algoritmo1()

mpgEG= JuegosdePagoMedioEnergia.MeanPayoffEnergyGameAlg2(nodos, arcos, V1, V2)
valores, sigma1, sigma2 = mpgEG.algoritmo2(min(mpgEG.S), max(mpgEG.S))

print("Resultados algortimo de Zwick y Paterson:")
print(f"k=",mpgZP.k)
#Estos bucles informan sobre los valores vk
for i in range (len(nodos)):
    print(f"vk({nodos[i]}):",mpgZP.vk[i])
for i in range (len(nodos)):
    print(f"vk({nodos[i]})/{mpgZP.k}:",mpgZP.vk[i]/mpgZP.k)

print("\nValores del MPG:", mpgZP.v)#
print("\nEstrategia posicional óptima del Jugador 1:")
for nodo, dest in mpgZP.estrategia_pos_optima(1).items():
    print(f"{nodo} -> {dest}")

print("\nEstrategia posicional óptima del Jugador 2:")
for nodo, dest in mpgZP.estrategia_pos_optima(2).items():
    print(f"{nodo} -> {dest}")

print("\nResultados si se aplicara un juego de energía:")
print("M_G =", EG.MG)
for u in nodos:
    print(f"{u}: {f[u]}")
print("Estrategia J1 del EG:", EG.estrategia(f))

print("\nResultados algortimo basado en juegos de energía:")

print("Valores juego de pago medio:")
for u in nodos:
    print(f"{u}: {valores[u]}")
print("Estrategia ganadora de J1:")
for u in sorted(sigma1):
    print(f"sigma1({u}) = {sigma1[u]}")

print("Estrategia ganadora de J2:")
for u in sorted(sigma2):
    print(f"sigm2({u}) = {sigma2[u]}")
