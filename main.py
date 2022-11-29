# Método númerico para Simulación del sistema Tierra-Luna
# Usando el método númerico Runge-Kutta 4
# Para r_1 y r_2 (vectores) que posicionan ambos cuerpos con sendas masas m1 y m2
# Se realiza el siguiente cambio de variable
#
# r_1 - r_2 = r			, r vector que ve de r_2 a r_1
# m1*r_1 + m2*r_2 = 0	, centro de masa en el origen
#
# Por: Santiago, L. D.

import math
from random import uniform,randint
import time
from metodosnum import Rk4_f as rk
from herramientas import cambiounidad,velocidadradial

# Orden para definir una nueva unidad de masa y otra de longitud

n = 2		# Para masa, 10^n
m = 1		# Para longitud, 10^m

# |-----------------------------------------------------------------------------------------------|
#					Definición de las constantes del sistema como variables globales
# |-----------------------------------------------------------------------------------------------|

# constantes para el sistema Luna-Tierra

G = 6.674e-11			# N*m^2/kg^2 o m^3/kg*s^2
m1 = 7.349e22			# kg, masa Luna
m2 = 5.9736e24			# kg, masa Tierra
perigeo = 356410.0 + 1737.1 + 6371.0 # km, distancia durante perigeo
		  # distancia entre superficies + radio luna + radio tierra
Vt = 1.08 				# km/s, velocidad radial
excen = 0.054			# excentricidad del sistema

# Cambiando unidades de km a ULL, Kg a UML y s a dias
# Ver herramientas.py para más detalles

m1,m2,G,perigeo,Vt = cambiounidad(m1,m2,G,perigeo,Vt,n,m)

# Constantes convenientes

M = m1 + m2		# Masa total
mu = m1*m2/M	# Masa reducida

Vr,Energia,Momento,Periodo = velocidadradial(m1,m2,G,perigeo,Vt,excen)
#		Tenemos velocidad tangencial, y para calcular la V radial nos
#		basaremos en la excentricidad del sistema
# 		Ver herramientas.py para más detalles

print(mu*perigeo*Vt,0.5*mu*(Vr**2+Vt**2)-G*m1*m2/perigeo,Periodo)

# |----------------------------------------------------------------------------------------------|
# 				Sistema de ecuaciones diferenciales que describen el problema
# |----------------------------------------------------------------------------------------------|

def funcion(q,t): # Necesario para el método Runge-Kutta
	f1 = q[2]
	f2 = q[3]
	f3 = q[0]*q[3]**2 - G*M/(q[0]**2)
	f4 = -2*q[2]*q[3]/q[0]

	h=[ f1, f2, f3, f4 ]
	return h
# |----------------------------------------------------------------------------------------------|
#			 						Cuerpo del programa
# |----------------------------------------------------------------------------------------------|

def main():
	print("Problema de los dos cuerpos")

	# Parámetros de la simulación

	t0 = 0			# Días, Tiempo inicial
	T = Periodo    	# Días, Tiempo final
	h = 1/60

	# Condiciones iniciales del sistema en coordenadas polares

	r0 = perigeo		 	# ULL, posicion inicial en r
	phi0 = 0   				# rad, posicion inicial en phi, posicionado en perigeo
	vr0 = Vr  				# rad/dias, velocidad radial
	vphi0 = Vt/perigeo 		# rad/dias, velocidad tangencial

	# Aplicaciones del método runge-kutta 4

	out1 = open("datosenbruto.dat","w")
	q0 = [ r0, phi0, vr0, vphi0]

	n = rk.rk4(q0,t0,T,h,funcion,out1)	# rk4() escribe resultados de forma directa en out1
									# en este caso particular en coordenadas polares
	out1.close()					# rk4 está definido en Rk4_f

	# Salidad de datos en coordenadas Cartesianas

	out = open("datos.dat","w")
	in1 = open("datosenbruto.dat", "r") # Se vuelve a abrir datosenbruto.dat
										# para convertir los datos en cartecianas
	for i in range(n):
		aux = in1.readline()
		q = aux[:-1].split("\t")
		x = float(q[0])*math.cos(float(q[1])) #Conversion
		y = float(q[0])*math.sin(float(q[1]))

		x1 = (m2/M)*x    	# r representa la distancia entre m1 y m2, r_1 - r_2 = r (vectores)
		y1 = (m2/M)*y       # Este bloque regresa a las coodenadas dadas por r_1 y r_2 (vectores)
		x2 = -(m1/M)*x
		y2 = -(m1/M)*y
		print(x1,y1,x2,y2,q[-1], sep="\t", file=out)

	in1.close()
	out.close()
#	graficar("datos.dat",2,"grafg.m",h,60,60)


def graficar(archivo,numbolas,matlabm,h,l,a):
	out = open(matlabm,"w")
	print("clear\n\nentrada=load('"+ archivo + "');\n", file=out)

	for i in range(1,numbolas+1):
		print("x"+ str(i)+"=entrada(:,"+ str(2*i-1)+");", file=out)
		print("y"+ str(i)+"=entrada(:,"+ str(2*i)+");", file=out)
	print("\n",file=out)

	print("n=length(x1);\n" + "loop1=" + str(h) + ";", file=out)
	print("l=" + str(l) + ";\n" + "a=" + str(a) + ";\n", file=out)

	print("for i=1:1:n", file=out)
	for i in range(1,numbolas+1):
		if i == 1:
			print("\tplot(x"+str(i)+"(i),y"+str(i)+"(i),'o'", file=out,end="")
		else:
			print("\n\t\tx"+str(i)+"(i),y"+str(i)+"(i),'o'", file=out,end="")
		if i < numbolas:
			print(",", end="", file=out)
	print(")",file=out)
	print("\taxis([ -l l -a a])\n\tpause(loop1)", file=out)
	print("end",file=out)
	out.close()

main()
