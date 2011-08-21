from  glob import iglob
import shutil
import os
import sys
import ConfigParser
import time

def ConvertirFichero(fichero):
	print "Convirtiendo el fichero: " + rutaActual + "/" + fichero

	os.system("ffmpeg -i " + rutaActual + "/" + fichero + " -an -sameq -y -s "+ resolucion+" "+ rutaTemporal + fichero + extensionSalida + " 2>> " + rutaLogs + ficheroFinal + ".log")

def BorrarTemporal():
	shutil.rmtree(rutaTemporal)

def CrearRutaTemporal():
	if not os.path.exists(rutaTemporal):
		print "Creando el directorio temporal"
		os.mkdir(rutaTemporal)

def CrearRutaFinal():
	if not os.path.exists(rutaFinal):
		print "creando el directorio final"
		os.mkdir(rutaFinal)

def CrearRutaLogs():
	if not os.path.exists(rutaLogs):
		print "creando el directorio de logs"
		os.mkdir(rutaLogs)	

def CrearCarpetas():
	CrearRutaTemporal()
	CrearRutaFinal()
	CrearRutaLogs()

def ConvertirFicherosDelDirectorio():
	for name in os.listdir(rutaActual):
		ConvertirFichero(name)
	
def CrearFicheroFinal():
	print "Creando el fichero final: " + rutaFinal + ficheroFinal
	
	destino = open(rutaTemporal + ficheroTemporal,'wb')

	for filename in iglob(os.path.join(rutaTemporal,'*.avi')):
		shutil.copyfileobj(open(filename,'rb'), destino)

	destino.close()

	os.system("ffmpeg -i " + rutaTemporal + ficheroTemporal + " -sameq " + rutaFinal + ficheroFinal + extensionSalida + " 2>> " + rutaLogs + ficheroFinal + ".log")


def NombreFinal():
	fecha = time.localtime()

	ficheroFinal = ''	

	for i in range(6):
		ficheroFinal = ficheroFinal + str(fecha[i])
	#ficheroFinal = ficheroFinal + ".avi"

	return ficheroFinal	

cfg = ConfigParser.ConfigParser()
if not cfg.read(["./tratvid.cfg"]):
	print "No existe el archivo de configuracion"	

rutaActual		= os.path.realpath(sys.argv[1])
resolucion      = cfg.get("video","resolucion")
rutaTemporal    = rutaActual + cfg.get("rutas","temporal")
rutaFinal		= rutaActual + cfg.get("rutas","final")
rutaLogs		= rutaActual + cfg.get("rutas","logs")
extensionSalida = cfg.get("salida","extension")
ficheroTemporal = cfg.get("salida","ficherotemporal")
ficheroFinal 	= NombreFinal()

NombreFinal()

CrearCarpetas()

ConvertirFicherosDelDirectorio()

CrearFicheroFinal()

BorrarTemporal()
