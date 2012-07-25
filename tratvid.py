#!/usr/bin/env python

from  glob import iglob
import shutil
import os
import sys
import ConfigParser
import time

def TamanoTotalArchivosEnCarpeta():
	tamanoTotal = 0
	for fichero in os.listdir(rutaActual):
		if os.path.isfile(rutaActual + "/" + fichero):
			tamanoTotal = tamanoTotal + ((os.path.getsize(rutaActual+"/"+fichero) / 1024 ) / 1024)
	return tamanoTotal
 
def ConvertirFichero(fichero):
	print "Convirtiendo el fichero: " + rutaActual + "/" + fichero
	commandOutput = os.system("avconv -i " + rutaActual + "/" + fichero + " -vcodec "+ videoCodec + " -threads "+ threads + " -vb "+ bitrate +" -an -y -s "+ resolucion+" -pass 1 "+ rutaTemporal + fichero + extensionSalida + " 2>> " + rutaLogs + ficheroFinal + ".log")
	commandOutput =	os.system("avconv -i " + rutaActual + "/" + fichero + " -vcodec "+ videoCodec + " -threads "+ threads + " -vb "+ bitrate +" -an -y -s "+ resolucion+" -pass 2 "+ rutaTemporal + fichero + extensionSalida + " 2>> " + rutaLogs + ficheroFinal + ".log")
	if commandOutput == 2:
		exit()

def EliminarFichero(fichero):
	if (cfg.get("opciones","eliminaroriginal") == "1"):
		print "Eliminando el fichero: " + fichero
		os.remove(fichero)

def BorrarTemporal():
	if (cfg.get("opciones","eliminartemporal") == "1"):
		print "Eliminando el directorio temporal"
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
	for name in sorted(os.listdir(rutaActual)):
		if os.path.isfile(rutaActual + "/" + name):
			try:
				ConvertirFichero(name)
			except KeyboardInterrupt:
				print 'Ejecucion cancelada'
				exit()
			EliminarFichero(rutaActual + "/" + name)

def CrearFicheroFinal():
	print "Creando el fichero final: " + rutaFinal + ficheroFinal + extensionSalida
	
	appends = ''
	for filename in sorted(iglob(os.path.join(rutaTemporal,'*'+ extensionSalida))):
		if appends == '':
			appends = ' --load '+ filename
		else:
			appends = appends + ' --append '+ filename
			
	os.system("avidemux2_cli --nogui --force-unpack --force-b-frame --force-alt-h264  --force-smart " + appends +" --save-raw-audio --save-raw-video  --save "+ rutaFinal + ficheroFinal + extensionSalida + " 2>> " + rutaLogs + ficheroFinal + ".log")

def NombreFinal():
	fecha = time.localtime()

	ficheroFinal = ''	

	for i in range(6):
		ficheroFinal = ficheroFinal + str(fecha[i])

	return ficheroFinal	

def Ejecutar():
	NombreFinal()
	CrearCarpetas()
	ConvertirFicherosDelDirectorio()
	CrearFicheroFinal()
	BorrarTemporal()
	
def MostrarMensajeEspera():
	print ""
	print "A la espera...(Puede parar el proceso con Ctrl-C"
	print ""
	print ""

def MostrarParametros():
	print "Numero de parametros erroneo. Uso correcto:"
	print "tratvid Path [-d]"

cfg = ConfigParser.ConfigParser()
if not cfg.read(["/etc/tratvid/tratvid.cfg"]):
	print "No existe el archivo de configuracion"	

if len(sys.argv) > 1:
	rutaActual = os.path.realpath(sys.argv[1])
else:
	rutaActual = ''
resolucion = cfg.get("video","resolucion")
videoCodec = cfg.get("video","codec")
threads = cfg.get("video","threads")
bitrate = cfg.get("video","bitrate")
rutaTemporal = rutaActual + cfg.get("rutas","temporal")
rutaFinal =  rutaActual + cfg.get("rutas","final")
rutaLogs = rutaActual + cfg.get("rutas","logs")
extensionSalida = cfg.get("salida","extension")
ficheroTemporal = cfg.get("salida","ficherotemporal")
ficheroFinal = NombreFinal()

def main():
	try:
		if len(sys.argv) > 1:
			if len(sys.argv) == 3:
				if ( sys.argv[2] == '-d'):
					print "INICIADA LA APLICACION TratVid"
					MostrarMensajeEspera()
					while True:
						time.sleep(int(cfg.get("opciones","tiempoespera")))
						if (TamanoTotalArchivosEnCarpeta() > int(cfg.get("opciones","maxtamano"))): 
							Ejecutar()
							MostrarMensajeEspera()
						else:
							print "Parametro desconocido"
			else:
				Ejecutar()
		else:
			MostrarParametros()
			exit()
	except KeyboardInterrupt:
		print 'Ejecucion cancelada'
		exit()
if __name__ == "__main__":
	main()
