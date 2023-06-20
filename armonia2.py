import random
 # Codificar la melodía
#melodia = [60, 62, 64, 65, 67, 69, 71, 72]
melodia = [60, 62, 64, 65, 67, 69, 71, 72]

 # Inversiones de los acordes
inversiones = [
    [[60, 64, 67], [64, 67, 72], [67, 72, 76]],
    [[62, 65, 69], [65, 69, 74], [69, 74, 77]],
    [[64, 67, 71], [67, 71, 76], [71, 76, 79]],
    [[65, 69, 72], [69, 72, 77], [72, 77, 81]],
    [[67, 71, 74], [71, 74, 79], [74, 79, 83]],
    [[69, 72, 76], [72, 76, 81], [76, 81, 84]],
    [[71, 74, 77], [74, 77, 82], [77, 82, 86]],
    [[72, 76, 79], [76, 79, 84], [79, 84, 88]],
]

# Rangos de las voces
rangos = {
    "soprano": (64, 84),
    "alto": (55, 76),
    "tenor": (45, 69),
    "bajo": (36, 60),
}

# Crear la población inicial
def generar_armonia():
    soprano = melodia
    alto = []
    tenor = []
    bajo = []
    for _ in range(len(melodia)):
        notas_alto = []
        notas_tenor = []
        notas_bajo = []
        for inversion in inversiones:
            for nota in inversion:
                if rangos["alto"][0] <= nota[0] <= rangos["alto"][1]:
                    notas_alto.append(nota[0])
                if rangos["tenor"][0] <= nota[0] <= rangos["tenor"][1]:
                    notas_tenor.append(nota[0])
                if rangos["bajo"][0] <= nota[0] <= rangos["bajo"][1]:
                    notas_bajo.append(nota[0])
        alto.append(random.choice(notas_alto))
        tenor.append(random.choice(notas_tenor))
        bajo.append(random.choice(notas_bajo))
    return (soprano, alto, tenor, bajo)

poblacion = [generar_armonia() for _ in range(10)]
 # Evaluar la población
def calcular_puntaje(armonia):
    soprano, alto, tenor, bajo = armonia
    puntaje = 0
    
    # Regla 1: La nota más aguda de cada acorde debe ser la nota del soprano
    for i in range(len(soprano)):
        acorde = [soprano[i], alto[i], tenor[i], bajo[i]]
        if max(acorde) != soprano[i]:
            puntaje -= 1
    
    # Regla 2: El intervalo entre el bajo y el soprano no debe ser mayor a una décima
    #for i in range(len(soprano)):
    #    intervalo = abs(bajo[i] - soprano[i])
    #    if intervalo > 14:
    #        puntaje -= 1
    
    # Regla 3: La distancia entre el alto y el soprano debe ser menor a una octava
    for i in range(len(soprano)):
        intervalo = abs(alto[i] - soprano[i])
        if intervalo > 12:
            puntaje -= 1
    
    # Regla 4: La distancia entre el tenor y el soprano debe ser menor a una octava
    for i in range(len(soprano)):
        intervalo = abs(tenor[i] - soprano[i])
        if intervalo > 12:
            puntaje -= 1
    
    # Regla 5: Evitar cuartas y quintas paralelas
    for i in range(1, len(soprano)):
        acorde1 = [soprano[i-1], alto[i-1], tenor[i-1], bajo[i-1]]
        acorde2 = [soprano[i], alto[i], tenor[i], bajo[i]]
        intervalos1 = [acorde1[j+1] - acorde1[j] for j in range(len(acorde1)-1)]
        intervalos2 = [acorde2[j+1] - acorde2[j] for j in range(len(acorde2)-1)]
        if intervalos1 == intervalos2 and (intervalos1[0] == 5 or intervalos1[0] == -5 or intervalos1[0] == 7 or intervalos1[0] == -7):
            puntaje -= 1
    
    # Regla 6: Evitar octavas paralelas
    for i in range(1, len(soprano)):
        acorde1 = [soprano[i-1], alto[i-1], tenor[i-1], bajo[i-1]]
        acorde2 = [soprano[i], alto[i], tenor[i], bajo[i]]
        intervalos1 = [acorde1[j+1] - acorde1[j] for j in range(len(acorde1)-1)]
        intervalos2 = [acorde2[j+1] - acorde2[j] for j in range(len(acorde2)-1)]
        if intervalos1 == intervalos2 and intervalos1[0] == 12:
            puntaje -= 1
    
    return puntaje

puntajes = [calcular_puntaje(armonia) for armonia in poblacion]
 # Seleccionar los padres
def seleccionar_padres(poblacion, puntajes):
    padres = []
    min_puntaje = min(puntajes)
    puntajes_normalizados = [puntaje + abs(min_puntaje) + 1 for puntaje in puntajes]
    for _ in range(2):
        indice_padre = random.choices(range(len(poblacion)), weights=puntajes_normalizados)[0]
        padres.append(poblacion[indice_padre])
    return padres
 # Cruzar los padres
def cruzar_padres(padres):
    punto_cruce = random.randint(1, len(melodia) - 1)
    hijo1 = (padres[0][0][:punto_cruce] + padres[1][0][punto_cruce:], 
             padres[0][1][:punto_cruce] + padres[1][1][punto_cruce:], 
             padres[0][2][:punto_cruce] + padres[1][2][punto_cruce:], 
             padres[0][3][:punto_cruce] + padres[1][3][punto_cruce:])
    hijo2 = (padres[1][0][:punto_cruce] + padres[0][0][punto_cruce:], 
             padres[1][1][:punto_cruce] + padres[0][1][punto_cruce:], 
             padres[1][2][:punto_cruce] + padres[0][2][punto_cruce:], 
             padres[1][3][:punto_cruce] + padres[0][3][punto_cruce:])
    return (hijo1, hijo2)
 # Mutar la población
def mutar_poblacion(poblacion, prob_mutacion):
    for i in range(1, len(poblacion)):
        if random.random() < prob_mutacion:
            poblacion[i] = (poblacion[i][0], 
                            [random.choice(inversiones[melodia.index(nota)][random.randint(0, 2)]) if random.random() < 0.5 else poblacion[i][1][j] for j, nota in enumerate(melodia)], 
                            [random.choice(inversiones[melodia.index(nota)][random.randint(0, 2)]) if random.random() < 0.5 else poblacion[i][2][j] for j, nota in enumerate(melodia)], 
                            [random.choice(inversiones[melodia.index(nota)][random.randint(0, 2)]) if random.random() < 0.5 else poblacion[i][3][j] for j, nota in enumerate(melodia)])
    return poblacion
 # Repetir los pasos 3 a 6 varias veces
for generacion in range(10):
    # Seleccionar los padres
    padres = seleccionar_padres(poblacion, puntajes)
     # Cruzar los padres
    hijos = cruzar_padres(padres)
     # Mutar la población
    poblacion = mutar_poblacion(poblacion, 0.1)
     # Evaluar la población
    puntajes = [calcular_puntaje(armonia) for armonia in poblacion]
     # Imprimir cada voz
    for i in range(len(poblacion)):
        print("Generación:", generacion, "Armonía:", i)
        print("Soprano:", poblacion[i][0])
        print("Alto:", poblacion[i][1])
        print("Tenor:", poblacion[i][2])
        print("Bajo:", poblacion[i][3])
        print()
 # Seleccionar la mejor armonía
mejor_armonia = poblacion[puntajes.index(max(puntajes))]
 # Imprimir cada voz de la armonía final
print("Armonía final:")
print("Soprano:", mejor_armonia[0])
print("Alto:", mejor_armonia[1])
print("Tenor:", mejor_armonia[2])
print("Bajo:", mejor_armonia[3])
