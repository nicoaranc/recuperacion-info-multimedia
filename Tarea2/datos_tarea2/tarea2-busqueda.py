# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: Nicolás Arancibia

import sys
import os
import util as util
import scipy
import numpy


def tarea2_busqueda(carpeta_descriptores_radio_Q, carpeta_descriptores_canciones_R, archivo_ventanas_similares):
    if not os.path.isdir(carpeta_descriptores_radio_Q):
        print("ERROR: no existe {}".format(carpeta_descriptores_radio_Q))
        sys.exit(1)
    elif not os.path.isdir(carpeta_descriptores_canciones_R):
        print("ERROR: no existe {}".format(carpeta_descriptores_canciones_R))
        sys.exit(1)
    elif os.path.exists(archivo_ventanas_similares):
        print("ERROR: ya existe {}".format(archivo_ventanas_similares))
        sys.exit(1)
    #
    # Implementar la tarea con los siguientes pasos:
    #
    #  1-leer Q y R: datos en carpeta_descriptores_radio_Q y carpeta_descritores_canciones_R
    #     esas carpetas fueron creadas por tarea2_extractor con los audios de radio y canciones
    #     puede servir la funcion util.leer_objeto() que está definida en util.py
    #

    ventanas_radio = util.leer_objeto(carpeta_descriptores_radio_Q, "ventanas_conocidas")
    mfcc_radio = util.leer_objeto(carpeta_descriptores_radio_Q, "mfcc_conocidas")

    ventanas_canciones = util.leer_objeto(carpeta_descriptores_canciones_R, "ventanas_conocidas")
    mfcc_canciones = util.leer_objeto(carpeta_descriptores_canciones_R, "mfcc_conocidas")

    #  2-para cada descriptor de Q localizar el más cercano en R
    #     podría usar cdist (ver semana 02) o algún índice de busqueda eficiente (Semanas 03-04)

    matriz_distancias = scipy.spatial.distance.cdist(mfcc_radio, mfcc_canciones, metric='canberra')

    #
    #  3-escribir en el archivo archivo_ventanas_similares una estructura que asocie
    #     cada ventana de Q con su ventana más parecida en R
    #     recuerde guardar el nombre del archivo y los tiempos de inicio y fin que representa cada ventana de Q y R
    #     puede servir la funcion util.guardar_objeto() que está definida en util.py

    posicion_min = numpy.argmin(matriz_distancias, axis=1)
    # minimo = numpy.amin(matriz_distancias, axis=1)
    tabla_resultados = []

    for i in range(len(ventanas_radio)):
        query = ventanas_radio[i]
        nombre_q = query.nombre_archivo
        t_inicio_q = query.segundos_desde
        t_final_q = query.segundos_hasta
        conocido = ventanas_canciones[posicion_min[i]]
        nombre_c = conocido.nombre_archivo
        t_inicio_c = conocido.segundos_desde
        t_final_c = conocido.segundos_hasta
        tabla_resultados.append([nombre_q, t_inicio_q, t_final_q, nombre_c, t_inicio_c, t_final_c])

    carpeta = archivo_ventanas_similares[0:27]
    nombre = archivo_ventanas_similares[28:len(archivo_ventanas_similares)]

    util.guardar_objeto(tabla_resultados, carpeta, nombre)

    #
    # borrar las siguientes lineas
    # print("ERROR: tarea2_busqueda no implementado!")
    # sys.exit(1)


# inicio de la tarea
if len(sys.argv) != 4:
    print(
        "Uso: {} [carpeta_descriptores_radio_Q] [carpeta_descritores_canciones_R] [archivo_ventanas_similares]".format(
            sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
carpeta_descriptores_radio_Q = sys.argv[1]
carpeta_descriptores_canciones_R = sys.argv[2]
archivo_ventanas_similares = sys.argv[3]

# llamar a la tarea
tarea2_busqueda(carpeta_descriptores_radio_Q, carpeta_descriptores_canciones_R, archivo_ventanas_similares)
