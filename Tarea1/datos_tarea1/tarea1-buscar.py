# CC5213 - TAREA 1 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 11 de agosto de 2024
# Alumno: Nicolás Arancibia

import sys
import os
import util as util
import scipy


def tarea1_buscar(dir_input_imagenes_Q, dir_input_descriptores_R, file_output_resultados):
    if not os.path.isdir(dir_input_imagenes_Q):
        print("ERROR: no existe directorio {}".format(dir_input_imagenes_Q))
        sys.exit(1)
    elif not os.path.isdir(dir_input_descriptores_R):
        print("ERROR: no existe directorio {}".format(dir_input_descriptores_R))
        sys.exit(1)
    elif os.path.exists(file_output_resultados):
        print("ERROR: ya existe archivo {}".format(file_output_resultados))
        sys.exit(1)
    # Implementar la fase online

    # 1-calcular descriptores de Q para imágenes en dir_input_imagenes_Q
    # ver codigo de ejemplo publicado en el curso

    imagenes = util.listar_archivos_en_carpeta(dir_input_imagenes_Q)

    descr_hog = util.calcular_descriptores(util.histograma_bordes_por_zona, imagenes, dir_input_imagenes_Q, 4, 4, 24)
    prom_hog = util.calcular_valor_promedio(descr_hog)
    descr_hog = util.escalar_matriz(descr_hog, prom_hog)

    descr_framed = util.calcular_descriptores(util.vector_de_intensidades, imagenes, dir_input_imagenes_Q, 33, 33, None)
    prom_framed = util.calcular_valor_promedio(descr_framed)
    descr_framed = util.escalar_matriz(descr_framed, prom_framed)

    descr_gamma = util.calcular_descriptores(util.vector_de_intensidades_equalizeHist, imagenes, dir_input_imagenes_Q, 33, 33, None)
    prom_gamma = util.calcular_valor_promedio(descr_gamma)
    descr_gamma = util.escalar_matriz(descr_gamma, prom_gamma)

    descr_flip = util.calcular_descriptores(util.histogramas_por_zonas, imagenes, dir_input_imagenes_Q, 1, 8, 16)

    descr_gamma_framed = util.sumar_matrices(descr_gamma, descr_framed)


    # 2-leer descriptores de R guardados en dir_input_descriptores_R
    # puede servir la funcion util.leer_objeto() que está definida en util.py

    descr_hogr = util.leer_objeto(dir_input_descriptores_R, "descriptores_hog")
    descr_flipr = util.leer_objeto(dir_input_descriptores_R, "descriptor_flip")
    descr_gammar = util.leer_objeto(dir_input_descriptores_R, "descriptor_gamma")
    descr_framedr = util.leer_objeto(dir_input_descriptores_R, "descriptor_framed")
    descr_gamma_framedr = util.sumar_matrices(descr_gammar, descr_framedr)

    # 3-para cada descriptor q localizar el mas cercano en R

    matriz_distancias_hog = scipy.spatial.distance.cdist(descr_hog, descr_hogr, metric="cityblock")
    prom_hog = util.calcular_valor_promedio(matriz_distancias_hog)
    matriz_distancias_hog = util.escalar_matriz(matriz_distancias_hog, prom_hog)
    resultados_hog = util.calcular_cercanos(imagenes, matriz_distancias_hog)

    matriz_distancias_flip = scipy.spatial.distance.cdist(descr_flip, descr_flipr, metric="cityblock")
    prom_flip_r = util.calcular_valor_promedio(matriz_distancias_flip)
    matriz_distancias_flip = util.escalar_matriz(matriz_distancias_flip, prom_flip_r)
    resultados_flip = util.calcular_cercanos(imagenes, matriz_distancias_flip)

    matriz_distancias_gamma_framed = scipy.spatial.distance.cdist(descr_gamma_framed, descr_gamma_framedr, metric="cityblock")
    prom_gamma_framed_r = util.calcular_valor_promedio(matriz_distancias_gamma_framed)
    matriz_distancias_gamma_framed = util.escalar_matriz(matriz_distancias_gamma_framed, prom_gamma_framed_r*1.4)
    resultados_gamma_framed = util.calcular_cercanos(imagenes, matriz_distancias_gamma_framed)


    resultados = []
    for i in range(len(resultados_flip)):
        row = []
        row.append(resultados_flip[i][0])
        dist = min(resultados_flip[i][2], resultados_gamma_framed[i][2], resultados_hog[i][2])
        if dist == resultados_flip[i][2]:
            row.append(resultados_flip[i][1])
        elif dist == resultados_gamma_framed[i][2]:
            row.append(resultados_gamma_framed[i][1])
        else:
            row.append(resultados_hog[i][1])
        row.append(dist)
        resultados.append(row)


    # 4-escribir en el archivo file_output_resultados un archivo con tres columnas separado por \t:
    # columna 1: imagen_q
    # columna 2: imagen_r
    # columna 3: distancia
    # Puede servir la funcion util.escribir_lista_de_columnas_en_archivo() que está definida util.py

    output = []
    for i in range(len(resultados)):
        row = []
        q, _, d = resultados[i]
        r = resultados[i][1]
        r = r[1:]
        r = 'r'+r
        row.append(q)
        row.append(r)
        row.append(d)
        output.append(row)
    util.escribir_lista_de_columnas_en_archivo(output, file_output_resultados)


# inicio de la tarea
if len(sys.argv) < 4:
    print("Uso: {} [dir_input_imagenes_Q] [dir_input_descriptores_R] [file_output_resultados]".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
dir_input_imagenes_Q = sys.argv[1]
dir_input_descriptores_R = sys.argv[2]
file_output_resultados = sys.argv[3]

# ejecuta la tarea
tarea1_buscar(dir_input_imagenes_Q, dir_input_descriptores_R, file_output_resultados)
