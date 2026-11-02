from graph import Graph
from heap import HeapMin
from lista_starwars import personajes


grafo = Graph(is_dir=False)
 
for personaje in personajes:
    grafo.add_vertex(personaje['nombre'], personaje['episodios'])
 
for i in range(len(personajes)):
    for j in range(i + 1, len(personajes)):
        en_comun = set(personajes[i]['episodios']) & set(personajes[j]['episodios'])
        if len(en_comun) > 0:
            grafo.add_edge(len(en_comun), personajes[i]['nombre'], personajes[j]['nombre'])


def buscar_en_bosque(bosque, vertice):
    """Devuelve la posición del árbol del bosque que contiene al vértice."""
    for indice, arbol in enumerate(bosque):
        if vertice in arbol[0]:
            return indice
  
def arbol_expansion_minimo(grafo, origen):
    # cada árbol del bosque es [conjunto de vértices, lista de aristas elegidas]
    bosque = []
    aristas = HeapMin()
    for vertice in grafo:
        bosque.append([{vertice.value}, []])
        for arista in vertice.edges:
            aristas.arrive([vertice.value, arista.destination], arista.weight)
 
    while len(bosque) > 1 and aristas.size() > 0:
        peso, (desde, hasta) = aristas.attention()
        pos_desde = buscar_en_bosque(bosque, desde)
        pos_hasta = buscar_en_bosque(bosque, hasta)
        if pos_desde != pos_hasta:  # si están en árboles distintos, no forma ciclo
            vertices = bosque[pos_desde][0] | bosque[pos_hasta][0]
            elegidas = bosque[pos_desde][1] + bosque[pos_hasta][1] + [(desde, hasta, peso)]
            bosque.pop(max(pos_desde, pos_hasta))
            bosque.pop(min(pos_desde, pos_hasta))
            bosque.append([vertices, elegidas])
 
    pos_origen = buscar_en_bosque(bosque, origen)
    if pos_origen is None:
        return None
    return bosque[pos_origen][1]


#Árbol de expansión mínimo desde un vértice
def mostrar_arbol_expansion_minimo(grafo, origen):
    aristas = arbol_expansion_minimo(grafo, origen)
    if aristas is None:
        print(f"  {origen} no está en el grafo")
        return
    print(f"  Árbol de expansión mínimo desde {origen}:")
    peso_total = 0
    for desde, hasta, peso in aristas:
        print(f"    {desde} <-> {hasta} ({peso})")
        peso_total += peso
    print(f"  Peso total: {peso_total}")

#Máximo de episodios compartidos por dos personajes y todos los pares que lo cumplen
def mostrar_maximo_episodios_compartidos(grafo):
    maximo = 0
    pares = []
    for vertice in grafo:
        for arista in vertice.edges:
            # al ser no dirigido, cada par aparece dos veces: lo cuento una sola
            if vertice.value < arista.destination:
                if arista.weight > maximo:
                    maximo = arista.weight
                    pares = [(vertice.value, arista.destination)]
                elif arista.weight == maximo:
                    pares.append((vertice.value, arista.destination))
 
    print(f"  Máximo de episodios compartidos: {maximo}")
    for personaje_1, personaje_2 in pares:
        print(f"    {personaje_1} y {personaje_2}")
 
 
#Camino más corto entre dos personajes (Dijkstra)
def mostrar_camino_mas_corto(grafo, origen, destino):
    if not grafo.exist_path(origen, destino):
        print(f"  No hay camino de {origen} a {destino}")
        return
 
    caminos = grafo.dijkstra(origen)  # pila con [vértice, costo, vértice anterior]
 
    actual = destino
    peso_total = None
    camino = []
    while caminos.size() > 0:
        valor = caminos.pop()
        if valor[0] == actual:
            if peso_total is None:
                peso_total = valor[1]
            camino.append(valor[0])
            actual = valor[2]
    camino.reverse()
 
    print(f"  De {origen} a {destino}: {' -> '.join(camino)} (costo {peso_total})")
 
 
#Personajes que aparecieron en los nueve episodios
def mostrar_personajes_en_todos_los_episodios(grafo):
    for vertice in grafo:
        if len(set(vertice.other_values)) == 9:
            print(f"  {vertice.value}")
 
 
#Ejecución
print("Árbol de expansión mínimo desde C-3PO, Yoda y Leia")
for origen in ["C-3PO", "Yoda", "Leia"]:
    mostrar_arbol_expansion_minimo(grafo, origen)
    print()
 
print("Máximo de episodios compartidos entre dos personajes")
mostrar_maximo_episodios_compartidos(grafo)
 
print("Camino más corto")
mostrar_camino_mas_corto(grafo, "C-3PO", "R2-D2")
mostrar_camino_mas_corto(grafo, "Yoda", "Darth Vader")
 
print("Personajes que aparecieron en los nueve episodios")
mostrar_personajes_en_todos_los_episodios(grafo)