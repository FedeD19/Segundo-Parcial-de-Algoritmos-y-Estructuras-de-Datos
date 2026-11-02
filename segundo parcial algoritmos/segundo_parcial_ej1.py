from tree import BinaryTree
from queue_ import Queue
from lista_pokemon import pokemons


arbol_nombre = BinaryTree()
arbol_numero = BinaryTree()
arbol_tipo = BinaryTree()
  
def cargar_tipo(arbol, tipo, nombre):
    nodo = arbol.search(tipo)
    if nodo is None:
        arbol.insert_node(tipo, [nombre])
    else:
        nodo.other_values.append(nombre)
  
for pokemon in pokemons:
    arbol_nombre.insert_node(pokemon['nombre'], pokemon)
    arbol_numero.insert_node(pokemon['numero'], pokemon)
    for tipo in pokemon['tipos']:
        cargar_tipo(arbol_tipo, tipo, pokemon['nombre'])


#Funciones auxiliares
def inorden(root, accion):
    if root is not None:
        inorden(root.left, accion)
        accion(root)
        inorden(root.right, accion)
  
def contar(root, condicion):
    if root is None:
        return 0
    cantidad = 1 if condicion(root.other_values) else 0
    return cantidad + contar(root.left, condicion) + contar(root.right, condicion)
 
def mostrar_pokemon(pokemon):
    print(f"  #{pokemon['numero']} {pokemon['nombre']}")
    print(f"     Tipos: {', '.join(pokemon['tipos'])}")
    print(f"     Debilidades: {', '.join(pokemon['debilidades'])}")
    print(f"     Mega evolución: {'Sí' if pokemon['mega_evolucion'] else 'No'}")
    print(f"     Gigamax: {'Sí' if pokemon['gigamax'] else 'No'}")


#Datos de un Pokémon por número (búsqueda exacta en el árbol por número)
def mostrar_por_numero(numero):
    nodo = arbol_numero.search(numero)
    if nodo is not None:
        mostrar_pokemon(nodo.other_values)
    else:
        print(f"  No hay ningún Pokémon con el número {numero}")
 
 
#Datos de un Pokémon por nombre, con búsqueda por proximidad
def mostrar_por_nombre(texto):
    texto = texto.lower()
    encontrados = []
 
    def accion(nodo):
        if texto in nodo.value.lower():
            encontrados.append(nodo.other_values)
 
    inorden(arbol_nombre.root, accion)
 
    if encontrados:
        for pokemon in encontrados:
            mostrar_pokemon(pokemon)
    else:
        print(f"  Ningún nombre comienza o contiene '{texto}'")
 
 
#Nombres de los Pokémon de un tipo
def mostrar_nombres_por_tipo(tipo):
    nodo = arbol_tipo.search(tipo)
    if nodo is not None:
        print(f"  {tipo} ({len(nodo.other_values)}): {', '.join(nodo.other_values)}")
    else:
        print(f"  No hay Pokémon de tipo {tipo}")
 
 
#Listados ascendentes por número y por nombre
def listar_por_numero():
    inorden(arbol_numero.root, lambda n: print(f"  {n.value:>4} - {n.other_values['nombre']}"))
 
 
def listar_por_nombre():
    inorden(arbol_nombre.root, lambda n: print(f"  {n.value} (#{n.other_values['numero']})"))
 
 
#Listado por nivel del árbol de nombres (recorrido por amplitud con una cola)
def listar_por_nivel(arbol):
    pendientes = Queue()
    if arbol.root is not None:
        pendientes.arrive((arbol.root, 0))
    nivel_actual = -1
    while pendientes.size() > 0:
        nodo, nivel = pendientes.attention()
        if nivel != nivel_actual:
            nivel_actual = nivel
            print(f"\n  Nivel {nivel}:")
        print(f"    {nodo.value}")
        if nodo.left is not None:
            pendientes.arrive((nodo.left, nivel + 1))
        if nodo.right is not None:
            pendientes.arrive((nodo.right, nivel + 1))
 
 
#Pokémon débiles frente a otro Pokémon (frente a alguno de sus tipos)
def mostrar_debiles_frente_a(nombre):
    nodo = arbol_nombre.search(nombre)
    if nodo is None:
        print(f"  {nombre} no está cargado")
        return
    tipos_atacante = nodo.other_values['tipos']
    print(f"  {nombre} es de tipo: {', '.join(tipos_atacante)}")
 
    debiles = []
 
    def accion(n):
        if any(tipo in n.other_values['debilidades'] for tipo in tipos_atacante):
            debiles.append(n.value)
 
    inorden(arbol_nombre.root, accion)
    print(f"  Débiles frente a {nombre} ({len(debiles)}): {', '.join(debiles)}")
 
 
#Todos los tipos y cuántos Pokémon hay de cada uno
def mostrar_tipos_y_cantidades():
    inorden(arbol_tipo.root, lambda n: print(f"  {n.value:10} {len(n.other_values)}"))
 
 
#Cantidad con megaevolución / con gigamax
def contar_megaevoluciones():
    return contar(arbol_nombre.root, lambda p: p['mega_evolucion'])
 
def contar_gigamax():
    return contar(arbol_nombre.root, lambda p: p['gigamax'])


#Ejecución 
print("Datos de un Pokémon por NÚMERO")
mostrar_por_numero(25)
mostrar_por_numero(1)
 
print("Datos por NOMBRE (búsqueda por proximidad)")
print("Búsqueda: 'bul'")
mostrar_por_nombre("bul")
print("Búsqueda: 'sa'")
mostrar_por_nombre("sa")
 
print("Nombres de Pokémon por tipo")
for tipo in ["Fantasma", "Fuego", "Acero", "Eléctrico"]:
    mostrar_nombres_por_tipo(tipo)
 
print("Listado ascendente por NÚMERO")
listar_por_numero()
 
print("Listado ascendente por NOMBRE")
listar_por_nombre()
 
print("Listado por NIVEL (árbol de nombres)")
listar_por_nivel(arbol_nombre)
 
print("Débiles frente a Jolteon, Lycanroc y Tyrantrum")
for atacante in ["Jolteon", "Lycanroc", "Tyrantrum"]:
    mostrar_debiles_frente_a(atacante)
    print()
 
print("Tipos y cantidad de Pokémon de cada uno")
mostrar_tipos_y_cantidades()
 
print("Pokémon con megaevolución")
print(f"  Total: {contar_megaevoluciones()}")
 
print("Pokémon con forma gigamax")
print(f"  Total: {contar_gigamax()}")