# CC5213 - TAREA 1 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 11 de agosto de 2024
# Alumno: Nicolás Arancibia

import sys
import os
import util as util

def tarea1_indexar(dir_input_imagenes_R, dir_output_descriptores_R):
    if not os.path.isdir(dir_input_imagenes_R):
        print("ERROR: no existe directorio {}".format(dir_input_imagenes_R))
        sys.exit(1)
    elif os.path.exists(dir_output_descriptores_R):
        print("ERROR: ya existe directorio {}".format(dir_output_descriptores_R))
        sys.exit(1)
    # Implementar la fase offline

    # 1-leer imágenes en dir_input_imagenes
    # puede servir la funcion util.listar_archivos_en_carpeta() que está definida en util.py

    imagenes = util.listar_archivos_en_carpeta(dir_input_imagenes_R)

    # 2-calcular descriptores de imágenes
    # ver codigo de ejemplo publicado en el curso

    descr_hog = util.calcular_descriptores(util.histograma_bordes_por_zona, imagenes, dir_input_imagenes_R, 4, 4, 24)
    descr_flip = util.calcular_descriptores(util.histogramas_por_zonas, imagenes, dir_input_imagenes_R, 1, 8, 16)
    descr_gamma = util.calcular_descriptores(util.vector_de_intensidades_equalizeHist, imagenes, dir_input_imagenes_R, 33, 33, None)
    prom_gamma = util.calcular_valor_promedio(descr_gamma)
    descr_gamma = util.escalar_matriz(descr_gamma, prom_gamma)
    descr_framed = util.calcular_descriptores(util.vector_de_intensidades, imagenes, dir_input_imagenes_R, 33, 33, None)
    prom_framed = util.calcular_valor_promedio(descr_framed)
    descr_framed = util.escalar_matriz(descr_framed, prom_framed)


    # 3-escribir en dir_output_descriptores_R los descriptores calculados en uno o más archivos
    # puede servir la funcion util.guardar_objeto() que está definida en util.py


    util.guardar_objeto(descr_hog, dir_output_descriptores_R, "descriptores_hog")
    util.guardar_objeto(descr_flip, dir_output_descriptores_R, "descriptor_flip")
    util.guardar_objeto(descr_gamma, dir_output_descriptores_R, "descriptor_gamma")
    util.guardar_objeto(descr_framed, dir_output_descriptores_R, "descriptor_framed")


# inicio de la tarea
if len(sys.argv) < 3:
    print("Uso: {} [dir_input_imagenes_R] [dir_output_descriptores_R]".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
dir_input_imagenes_R = sys.argv[1]
dir_output_descriptores_R = sys.argv[2]

# ejecuta la tarea
tarea1_indexar(dir_input_imagenes_R, dir_output_descriptores_R)
