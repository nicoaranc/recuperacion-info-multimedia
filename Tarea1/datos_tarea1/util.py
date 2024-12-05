# CC5213 - TAREA 1 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 11 de agosto de 2024
# Alumno: Nicolás Arancibia

# este archivo es usado por tarea1-buscar.py y tarea1-buscar.py
# permite tener funciones compartidas entre ambos programas
import os
import pickle
import cv2
import numpy
import math

# Retorna tods los archivos .jpg que estan en una carpeta
def listar_archivos_en_carpeta(imagenes_dir):
    lista = []
    for archivo in os.listdir(imagenes_dir):
        # los que terminan en .jpg se agregan a la lista de nombres
        if archivo.endswith(".jpg"):
            lista.append(archivo)
    lista.sort()
    return lista


# escribe el objeto de python en un archivo binario
def guardar_objeto(objeto, carpeta, nombre_archivo):
    # asegura que la carpeta exista
    os.makedirs(carpeta, exist_ok=True)
    # nombre completo
    archivo = "{}/{}".format(carpeta, nombre_archivo)
    # usa la librería pickle para escribir el objeto en un archivo binario
    # ver https://docs.python.org/3/library/pickle.html
    with open(archivo, 'wb') as handle:
        pickle.dump(objeto, handle, protocol=pickle.HIGHEST_PROTOCOL)


# reconstruye el objeto de python que está guardado en un archivo
def leer_objeto(carpeta, nombre_archivo):
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



def vector_de_intensidades(nombre_imagen, imagenes_dir, x, y, bins):
    archivo_imagen = imagenes_dir + "/" + nombre_imagen
    imagen = cv2.imread(archivo_imagen, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise Exception("no puedo abrir: " + archivo_imagen)
    imagen_reducida = cv2.resize(imagen, (x, y), interpolation=cv2.INTER_AREA)
    descriptor_imagen = imagen_reducida.flatten()
    return descriptor_imagen

def vector_de_intensidades_equalizeHist(nombre_imagen, imagenes_dir, x, y, bins):
    archivo_imagen = imagenes_dir + "/" + nombre_imagen
    imagen = cv2.imread(archivo_imagen, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise Exception("no puedo abrir: " + archivo_imagen)
    # ecualizacion
    imagen = cv2.equalizeHist(imagen)
    # se puede cambiar a otra interpolacion, como cv2.INTER_CUBIC
    imagen_reducida = cv2.resize(imagen, (x, y), interpolation=cv2.INTER_AREA)
    # flatten convierte una matriz de nxm en un array de largo nxm
    descriptor_imagen = imagen_reducida.flatten()
    return descriptor_imagen

def vector_de_intensidades_omd(nombre_imagen, imagenes_dir, x, y, bins):
    archivo_imagen = imagenes_dir + "/" + nombre_imagen
    imagen = cv2.imread(archivo_imagen, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise Exception("no puedo abrir: " + archivo_imagen)
    # se puede cambiar a otra interpolacion, como cv2.INTER_CUBIC
    imagen_reducida = cv2.resize(imagen, (x, y), interpolation=cv2.INTER_AREA)
    # flatten convierte una matriz de nxm en un array de largo nxm
    descriptor_imagen = imagen_reducida.flatten()
    # la posicion si se ordenan
    posiciones = numpy.argsort(descriptor_imagen)
    # reemplazar el valor gris por su  posicion
    for i in range(len(posiciones)):
        descriptor_imagen[posiciones[i]] = i
    # mostrar en pantalla, usa la variable global
    return descriptor_imagen

def dibujar_histograma(img, histograma, limites):
    cv2.rectangle(img, (0, 0), (img.shape[1] - 1, img.shape[0] - 1), (255, 200, 120), 1)
    pos_y_base = img.shape[0] - 6
    max_altura = img.shape[0] - 10
    nbins = len(histograma)
    for i in range(nbins):
        desde_x = int(img.shape[1] / nbins * i)
        hasta_x = int(img.shape[1] / nbins * (i + 1))
        altura = int(histograma[i] * max_altura)
        g = int((limites[i] + limites[i + 1]) / 2)
        color = (g, g, g)
        pt1 = (desde_x, pos_y_base + 5)
        pt2 = (hasta_x - 1, pos_y_base - altura)
        cv2.rectangle(img, pt1, pt2, color, -1)
    cv2.line(img, (0, pos_y_base), (img.shape[1] - 1, pos_y_base), (120, 120, 255), 1)


def histograma_por_zona(imagen, imagen_hists, x, y, bins):
    # divisiones
    num_zonas_x = x
    num_zonas_y = y
    num_bins_por_zona = bins
    # procesar cada zona
    descriptor = []
    for j in range(num_zonas_y):
        desde_y = int(imagen.shape[0] / num_zonas_y * j)
        hasta_y = int(imagen.shape[0] / num_zonas_y * (j + 1))
        for i in range(num_zonas_x):
            desde_x = int(imagen.shape[1] / num_zonas_x * i)
            hasta_x = int(imagen.shape[1] / num_zonas_x * (i + 1))
            # recortar zona de la imagen
            zona = imagen[desde_y: hasta_y, desde_x: hasta_x]
            # histograma de los pixeles de la zona
            histograma, limites = numpy.histogram(zona, bins=num_bins_por_zona, range=(0, 255))
            # normalizar histograma (bins suman 1)
            histograma = histograma / numpy.sum(histograma)
            # agregar descriptor de la zona al descriptor global
            descriptor.extend(histograma)
            # dibujar histograma de la zona
            if imagen_hists is not None:
                zona_hist = imagen_hists[desde_y: hasta_y, desde_x: hasta_x]
                dibujar_histograma(zona_hist, histograma, limites)
    return descriptor


def histogramas_por_zonas(nombre_imagen, imagenes_dir, x, y, bins):
    archivo_imagen = imagenes_dir + "/" + nombre_imagen
    imagen = cv2.imread(archivo_imagen, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise Exception("no puedo abrir: " + archivo_imagen)
    # ecualizacion
    imagen = cv2.equalizeHist(imagen)
    imagen_hists = numpy.full((imagen.shape[0], imagen.shape[1], 3), (200, 255, 200), dtype=numpy.uint8)
    descriptor = histograma_por_zona(imagen, imagen_hists, x, y, bins)
    return descriptor

def angulos_en_zona(angulos, mascara):
    # calcular angulos de la zona
    angulos_zona = []
    for row in range(mascara.shape[0]):
        for col in range(mascara.shape[1]):
            if not mascara[row][col]:
                continue
            angulo = round(math.degrees(angulos[row][col]))
            # dejar angulos en el rango -90 a 90
            if angulo < -180 or angulo > 180:
                raise Exception("angulo invalido {}, verificar si funciona la mascara".format(angulo))
            elif angulo <= -90:
                angulo += 180
            elif angulo > 90:
                angulo -= 180
            angulos_zona.append(angulo)
    return angulos_zona


def bordes_por_zona(angulos, mascara, imagen_hists, x, y, bins):
    # divisiones
    num_zonas_x = x
    num_zonas_y = y
    num_bins_por_zona = bins
    # procesar cada zona
    descriptor = []
    for j in range(num_zonas_y):
        desde_y = int(mascara.shape[0] / num_zonas_y * j)
        hasta_y = int(mascara.shape[0] / num_zonas_y * (j + 1))
        for i in range(num_zonas_x):
            desde_x = int(mascara.shape[1] / num_zonas_x * i)
            hasta_x = int(mascara.shape[1] / num_zonas_x * (i + 1))
            # calcular angulos de la zona
            angulos_zona = angulos_en_zona(angulos[desde_y: hasta_y, desde_x: hasta_x],
                                      mascara[desde_y: hasta_y, desde_x: hasta_x])
            # histograma de los angulos de la zona
            histograma, limites = numpy.histogram(angulos_zona, bins=num_bins_por_zona, range=(-90, 90))
            # normalizar histograma (bins suman 1)
            if numpy.sum(histograma) != 0:
                histograma = histograma / numpy.sum(histograma)
            # agregar descriptor de la zona al descriptor global
            descriptor.extend(histograma)
            # dibujar histograma de la zona
            if imagen_hists is not None:
                zona_hist = imagen_hists[desde_y: hasta_y, desde_x: hasta_x]
                limites = (limites + 180) / 360 * 255
                dibujar_histograma(zona_hist, histograma, limites)
    return descriptor


def histograma_bordes_por_zona(nombre_imagen, imagenes_dir, x, y, bins):
    archivo_imagen = imagenes_dir + "/" + nombre_imagen
    imagen = cv2.imread(archivo_imagen, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise Exception("no puedo abrir: " + archivo_imagen)
    # calcular filtro de sobel (usa cv2.GaussianBlur para borrar ruido)
    imagen2 = cv2.GaussianBlur(imagen, (5, 5), 0, 0)
    sobelX = cv2.Sobel(imagen2, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=3)
    sobelY = cv2.Sobel(imagen2, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=3)
    # calcula la magnitud del gradiente en cada pixel de la imagen
    magnitud = numpy.sqrt(numpy.square(sobelX) + numpy.square(sobelY))
    # selecciona los pixeles donde la magnitud del gradiente supera un valor umbral
    threshold_magnitud_gradiente = 100
    th, imagen_bordes = cv2.threshold(magnitud, threshold_magnitud_gradiente, 255, cv2.THRESH_BINARY)
    # definir una mascara donde estan los pixeles de borde
    mascara = imagen_bordes == 255
    # para los pixeles de la mascara calcular el angulo del gradiente
    angulos = numpy.arctan2(sobelY, sobelX, where=mascara)
    # imagen donde se dibujan los histogramas
    imagen_hists = numpy.full((imagen.shape[0], imagen.shape[1], 3), (200, 255, 200), dtype=numpy.uint8)
    # calcular descriptor (histograms de angulos por zonas)
    descriptor = bordes_por_zona(angulos, mascara, imagen_hists, x, y, bins)
    return descriptor

def calcular_descriptores(funcion_descriptor, nombres_imagenes, imagenes_dir, x, y, bins):
    matriz_descriptores = None
    num_fila = 0
    for nombre_imagen in nombres_imagenes:
        descriptor_imagen = funcion_descriptor(nombre_imagen, imagenes_dir, x, y, bins)
        if matriz_descriptores is None:
            matriz_descriptores = numpy.zeros((len(nombres_imagenes), len(descriptor_imagen)), numpy.float32)
        matriz_descriptores[num_fila] = descriptor_imagen
        num_fila += 1
    return matriz_descriptores

def calcular_cercanos(lista_nombres, matriz_distancias):
    numpy.fill_diagonal(matriz_distancias, numpy.inf)
    posiciones_minimas = numpy.argmin(matriz_distancias, axis=1)
    valores_minimos = numpy.amin(matriz_distancias, axis=1)
    tabla_resultados = []
    for i in range(len(matriz_distancias)):
        query = lista_nombres[i]
        distancia = valores_minimos[i]
        mas_cercano = lista_nombres[posiciones_minimas[i]]
        tabla_resultados.append([query, mas_cercano, distancia])
    return tabla_resultados

def calcular_valor_promedio(matriz):
    suma = 0
    cantidad = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            suma += matriz[i][j]
            cantidad += 1
    resultado = suma/cantidad
    return resultado

def escalar_matriz(matriz, valor):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = matriz[i][j]/valor
    return matriz

def sumar_matrices(matriz1, matriz2):
    matriz = []
    for i in range(len(matriz1)):
        row = []
        for j in range(len(matriz1[i])):
            row.append(matriz1[i][j] + matriz2[i][j])
        matriz.append(row)
    return matriz
