# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: Nicolás Arancibia

import sys
import os
import pandas as pd
import util as util


def tarea2_deteccion(archivo_ventanas_similares, archivo_detecciones):
    if not os.path.isfile(archivo_ventanas_similares):
        print("ERROR: no existe archivo {}".format(archivo_ventanas_similares))
        sys.exit(1)
    elif os.path.exists(archivo_detecciones):
        print("ERROR: ya existe archivo {}".format(archivo_detecciones))
        sys.exit(1)
    #
    # Implementar la tarea con los siguientes pasos:
    #
    #  1-leer el archivo archivo_ventanas_similares (fue creado por tarea2_busqueda)
    #    puede servir la funcion util.leer_objeto() que está definida en util.py

    carpeta = archivo_ventanas_similares[0:27]
    nombre = archivo_ventanas_similares[28:len(archivo_ventanas_similares)]

    archivo = util.leer_objeto(carpeta, nombre)

    #  2-crear un algoritmo para buscar secuencias similares entre audios
    #    ver slides de la semana 5 y 7
    #    identificar grupos de ventanas de Q y R que son similares y pertenecen a las mismas canciones con el mismo desfase

    tabla_resultados = []
    k = 7
    minimo = 3

    for i in range(len(archivo)):
        linea = archivo[i]
        rad = linea[0]
        radio = rad[0:(len(rad)-4)]
        t_inicio_r = linea[1]
        # t_final_r = linea[2]
        can = linea[3]
        cancion = can[0:(len(can)-4)]
        t_inicio_c = linea[4]
        # t_final_c = linea[5]

        # confianza = 0
        inicio = t_inicio_r
        largo = 0
        desfase = abs(t_inicio_r-t_inicio_c)

        encontradas = 0
        no_encontradas = 0

        for j in range(i, len(archivo)):
            ventana = archivo[j]
            des = abs(ventana[1]-ventana[4])
            rad_aux = ventana[0]
            radio_aux = rad_aux[0:(len(rad_aux)-4)]
            can_aux = ventana[3]
            cancion_aux = can_aux[0:(len(can_aux)-4)]
            if radio_aux != radio:
                break
            if des == desfase and cancion_aux == cancion:
                no_encontradas = 0
                encontradas += 1
                largo = ventana[2] - inicio
            else:
                no_encontradas += 1
                if no_encontradas == k:
                    break

        if largo >= minimo:
            tabla_resultados.append([radio, inicio, largo, cancion, encontradas])

    final = []
    aceptados = []

    for linea in tabla_resultados:
        par = linea[0], linea[3]
        if par not in aceptados:
            aceptados.append(par)
            final.append(linea)


    #  3-escribir las detecciones encontradas en archivo_detecciones, en un archivo con 5 columnas:
    #    columna 1: nombre de archivo Q (nombre de archivo en carpeta radio)
    #    columna 2: tiempo de inicio (número, tiempo medido en segundos de inicio de la emisión)
    #    columna 3: largo de la detección (número, tiempo medido en segundos con el largo de la emisión)
    #    columna 4: nombre de archivo R (nombre de archivo en carpeta canciones)
    #    columna 5: confianza (número, mientras más alto mayor confianza de la respuesta)
    #   le puede servir la funcion util.escribir_lista_de_columnas_en_archivo() que está definida util.py

    util.escribir_lista_de_columnas_en_archivo(final, archivo_detecciones)

    #
    # borrar las siguientes lineas
    # print("ERROR: tarea2_deteccion no implementado!")
    # sys.exit(1)


# inicio de la tarea
if len(sys.argv) != 3:
    print("Uso: {} [archivo_ventanas_similares] [archivo_detecciones]".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
archivo_ventanas_similares = sys.argv[1]
archivo_detecciones = sys.argv[2]

# llamar a la tarea
tarea2_deteccion(archivo_ventanas_similares, archivo_detecciones)
