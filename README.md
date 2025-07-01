# TFG Paula Balbás Corbacho: Juegos de pago medio

## Modelado y estrategias algorítmicas para la toma de decisiones mediante juegos de pago medio

El Trabajo de Fin de Grado, TFG, desarrollado trata sobre el estudio de los juegos de pago medio, juegos de dos jugadores sobre grafos dirigidos que constituyen una solución ampliamente validada y utilizada en la resolución de problemas cotidianos.

A lo largo de la memoria, no solo se analiza y explica la base teórica, sino que también se proponen una serie de algortimos que resuelven este tipo de casuísticas. Siendo, el presente repositorio, el lugar donde se publican los *scripts*, que se listan a continuación:

- JuegosdePagoMedioZwickPaterson.py
- JuegosdePagoMedioEnergia.py

Por otro lado, las librerías utilizadas en este proyecto son parte de la biblioteca *estándar* de Python, por lo que haría falta instalar ninguna con `pip`. No obstante, se adjunta un listado con ellas:

- random
- fractions
- math
- itertools

----------------------------------------

## Estructura del repositorio

El repositorio, cuenta con las siguientes carpetas:
```
README.md
TFG_PaulaBalbas/
|
|-JuegosdePagoMedioEjemplo.py
|-JuegosdePagoMedioZwickPaterson.py
|-JuegosdePagoMedioEnergia.py
|-Docs/
```

La carpeta `Docs` contiene la documentación generada con la librería `Sphinx`. No se detalla la estructura de sus elementos, ya que únicamente es necesario ejecutar el siguiente comando para visualizar la documentación:
```bash
start .\Docs\build\html\index.html
```
Comando que debe ejecutarse en la terminal desde la raíz del proyecto.

Por otro lado, en el código `JuegosdePagoMedio.py` quedan recogidos los algoritmos usados para ejemplificar los juegos de pago medio a lo largo del TFG.

Cabe recalcar que, previo a la ejecución del ejemplo 4 (logística supermercado), se deben ajustar, si se desea:

- Los parámetros a los que se quiera escalar
- El porcentaje de nodos y arcos que se quiera eliminar

Por otro lado, este código no cuenta con documentación *pyDoc*, al tratarse de ejemplos simples que austan los pesos de los nodos.

No obstante, cada ejemplo debe incluir:

- Una lista con los nodos de ejemplo. Que deben tener la forma 'estado.numerojugador'. Por ejemplo, un nodo asociado al jugador 1 con estado 'a', se denotará por 'a.1'
- El conjunto de arcos con los pesos asociados. Cada arco tiene la forma ('nodo', 'nodo', peso), por ejemplo, ('a.1', 'b.2', 3).



