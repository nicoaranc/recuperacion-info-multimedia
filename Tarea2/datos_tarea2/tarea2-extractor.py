# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: Nicolás Arancibia

import sys
import os
import util as util


def tarea2_extractor(carpeta_audios_entrada, carpeta_descriptores_salida):
    if not os.path.isdir(carpeta_audios_entrada):
        print("ERROR: no existe {}".format(carpeta_audios_entrada))
        sys.exit(1)
    elif os.path.exists(carpeta_descriptores_salida):
        print("ERROR: ya existe {}".format(carpeta_descriptores_salida))
        sys.exit(1)
    #
    # Implementar la tarea con los siguientes pasos:
    #
    #  1-leer los archivos con extension .m4a que están carpeta_audios_entrada
    #    puede servir la funcion util.listar_archivos_con_extension() que está definida en util.py

    archivos_m4a = util.listar_archivos_con_extension(carpeta_audios_entrada, ".m4a")

    #
    #  2-convertir cada archivo de audio a wav (guardar los wav temporales en carpeta_descriptores_salida)
    #    puede servir la funcion util.convertir_a_wav() que está definida en util.py

    archivos_wav = []
    sample_rate = 44100

    for archivo in archivos_m4a:
        archivo = carpeta_audios_entrada+archivo
        archivo = util.convertir_a_wav(archivo, sample_rate, carpeta_descriptores_salida)
        archivos_wav.append(archivo)

    #
    #  3-calcular descriptores del archivo wav

    samples_ventana = 8192*2
    samples_salto = 8192*2
    dimension = 130

    ventanas_conocidos, mfcc_conocidos = util.calcular_mfcc_varios_archivos(archivos_wav, sample_rate, samples_ventana,
                                                                            samples_salto, dimension, carpeta_audios_entrada)

    #
    #  4-escribir en carpeta_descriptores_salida los descriptores de cada archivo
    #    puede servir la funcion util.guardar_objeto() que está definida en util.py

    util.guardar_objeto(ventanas_conocidos, carpeta_descriptores_salida, "ventanas_conocidas")
    util.guardar_objeto(mfcc_conocidos, carpeta_descriptores_salida, "mfcc_conocidas")

    #
    # borrar las siguientes lineas
    # print("ERROR: tarea2_extractor no implementado!")
    # sys.exit(1)


# inicio de la tarea
if len(sys.argv) != 3:
    print("Uso: {} [carpeta_audios_entrada] [carpeta_descriptores_salida]".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
carpeta_audios_entrada = sys.argv[1]
carpeta_descriptores_salida = sys.argv[2]

# llamar a la tarea
tarea2_extractor(carpeta_audios_entrada, carpeta_descriptores_salida)
