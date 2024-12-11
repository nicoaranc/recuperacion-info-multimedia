# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 20 septiembre de 2024
# Alumno: Nicolás Arancibia

# este archivo se puede importar en los .py 
# para tener funciones compartidas entre todos los  programas
import os
import pickle
import subprocess
import librosa
import numpy


class Ventana:
    def __init__(self, nombre_archivo, segundos_desde, segundos_hasta):
        self.nombre_archivo = nombre_archivo
        self.segundos_desde = segundos_desde
        self.segundos_hasta = segundos_hasta

    def __str__(self):
        return "{} [{:6.3f}-{:6.3f}]".format(self.nombre_archivo, self.segundos_desde, self.segundos_hasta)

def calcular_descriptores_mfcc(archivo_wav, sample_rate, samples_por_ventana, samples_salto, dimension):
    # leer audio
    samples, sr = librosa.load(archivo_wav, sr=None)
    # print("audio samples={} samplerate={} segundos={:.1f}".format(len(samples), sr, len(samples) / sr))
    # calcular MFCC
    mfcc = librosa.feature.mfcc(y=samples, sr=sr, n_mfcc=dimension, n_fft=samples_por_ventana, hop_length=samples_salto)
    # convertir a descriptores por fila
    descriptores = mfcc.transpose()
    # se puede modificar la matriz de descriptores (ej: borrar alguna columna)
    return descriptores

def calcular_mfcc_archivo(archivo_audio, sample_rate, samples_por_ventana, samples_salto, dimension, dir):
    archivo_wav = convertir_a_wav(archivo_audio, sample_rate, dir)
    descriptores = calcular_descriptores_mfcc(archivo_wav, sample_rate, samples_por_ventana, samples_salto, dimension)
    return descriptores


def lista_ventanas(nombre_archivo, numero_descriptores, sample_rate, samples_por_ventana):
    # tantas ventanas como numero de descriptores
    tiempos = []
    for i in range(0, samples_por_ventana * numero_descriptores, samples_por_ventana):
        # tiempo de inicio de la ventana
        segundos_desde = i / sample_rate
        # tiempo de fin de la ventana
        segundos_hasta = (i + samples_por_ventana - 1) / sample_rate
        # crear objeto
        v = Ventana(nombre_archivo, segundos_desde, segundos_hasta)
        # agregar a la lista
        tiempos.append(v)
    return tiempos

def calcular_mfcc_varios_archivos(lista_archivos, sample_rate, samples_por_ventana, samples_salto, dimension, dir):
    descriptores_mfcc = []
    descriptores_ventanas = []
    for nombre_archivo in lista_archivos:
        audio_mfcc = calcular_mfcc_archivo(nombre_archivo, sample_rate, samples_por_ventana, samples_salto, dimension, dir)
        audio_ventanas = lista_ventanas(nombre_archivo, audio_mfcc.shape[0], sample_rate, samples_por_ventana)
        # print("  descriptores: {}".format(audio_mfcc.shape))
        if len(descriptores_mfcc) == 0:
            descriptores_mfcc = audio_mfcc
        else:
            # agregar como filas
            descriptores_mfcc = numpy.vstack([descriptores_mfcc, audio_mfcc])
        # agregar al final
        descriptores_ventanas.extend(audio_ventanas)
    return descriptores_ventanas, descriptores_mfcc


# funcion que recibe un nombre de archivo y llama a FFmpeg para crear un archivo wav
# requiere que el comando ffmpeg esté disponible
def convertir_a_wav(archivo_audio, sample_rate, dir_temporal):
    archivo_wav = "{}.wav".format(archivo_audio)
    if os.path.isfile(archivo_wav):
        return archivo_wav
    os.makedirs(dir_temporal, exist_ok=True)
    comando = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", archivo_audio, "-ac", "1", "-ar", str(sample_rate),
               archivo_wav]
    # print("  {}".format(" ".join(comando)))
    code = subprocess.call(comando)
    if code != 0:
        raise Exception("ERROR en comando: " + " ".join(comando))
    return archivo_wav


# Retorna todos los archivos que terminan con el parametro extension
# ejemplo: listar_archivos_con_extension(dir, ".m4a") retorna los nombres de archivos .m4a en dir
def listar_archivos_con_extension(carpeta, extension):
    lista = []
    for archivo in os.listdir(carpeta):
        # los que terminan con la extension se agregan a la lista de nombres
        if archivo.endswith(extension):
            lista.append(archivo)
    lista.sort()
    return lista


# escribe el objeto de python en un archivo binario
def guardar_objeto(objeto, carpeta, nombre_archivo):
    if carpeta == "" or carpeta == "." or carpeta is None:
        archivo = nombre_archivo
    else:
        archivo = "{}/{}".format(carpeta, nombre_archivo)
        # asegura que la carpeta exista
        os.makedirs(carpeta, exist_ok=True)
    # usa la librería pickle para escribir el objeto en un archivo binario
    # ver https://docs.python.org/3/library/pickle.html
    with open(archivo, 'wb') as handle:
        pickle.dump(objeto, handle, protocol=pickle.HIGHEST_PROTOCOL)


# reconstruye el objeto de python que está guardado en un archivo
def leer_objeto(carpeta, nombre_archivo):
    if carpeta == "" or carpeta == "." or carpeta is None:
        archivo = nombre_archivo
    else:
        archivo = "{}/{}".format(carpeta, nombre_archivo)
    with open(archivo, 'rb') as handle:
        objeto = pickle.load(handle)
    return objeto


# Recibe una lista de listas y lo escribe en un archivo separado por \t
# Por ejemplo:
# listas = [
#           ["dato1a", "dato1b", "dato1c"],
#           ["dato2a", "dato2b", "dato2c"],
#           ["dato3a", "dato3b", "dato3c"] ]
# al llamar:
#   escribir_lista_de_columnas_en_archivo(listas, "archivo.txt")
# escribe un archivo de texto con:
# dato1a  dato1b   dato1c
# dato2a  dato2b   dato3c
# dato2a  dato2b   dato3c
def escribir_lista_de_columnas_en_archivo(lista_con_columnas, archivo_texto_salida):
    with open(archivo_texto_salida, 'w') as handle:
        for columnas in lista_con_columnas:
            textos = []
            for col in columnas:
                textos.append(str(col))
            texto = "\t".join(textos)
            print(texto, file=handle)
