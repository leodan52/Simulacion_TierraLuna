# Herramientas para simulación tierra luna
# Este módulo contiene:
# 1. Conversión a unidades más convenientes para método RK$
# 2. El programa define a mano las siguientes condiciones iniciales en polares
# 	r, phi_inicial, Vphi para algún t inicial, con V : velocidad
# 	por lo que otra función de este modulo calcula la velocidad Vr mediente la excentricidad.

import math

def cambiounidad(m1,m2,G,perigeo,Vt,n,m):

	# Equivalencias para los cambios de unidad

	UML = m2/10**n  		#kg, 10^n UML masa de la tierra, Unidad de Masa Local
	ULL = perigeo/10**m 	#km, 10^m ULL distancia entre tierra Luna, Unidad de Longitud Local
	dia = 86400.0 			#s, la cantidad de segundos que tiene un día

	# Operadores para cambios de unidades

	m2km = 1.0/1000.0
	km2ULL = 1.0/ULL
	m2ULL = m2km*km2ULL
	kg2UML = 1.0/UML
	s2dia = 1.0/dia

	# Cambios de unidades

	m1_ = m1*kg2UML
	m2_ = 10**n   						# Conversión de Kg a UML
	G_ = G*m2ULL**3/(kg2UML*s2dia**2)	# Conversion de m^3/kg*s^2 a ULL^3/ULL*dia^2
	perigeo_ = perigeo*km2ULL			# Conversion de km a ULL
	Vt_ = Vt*km2ULL/s2dia				# Conversion de km/s a ULL/dia

	return m1_,m2_,G_,perigeo_,Vt_

def velocidadradial(m1,m2,G,perigeo,Vt,excen):
	M = m1 + m2		# Masa total
	mu = m1*m2/M	# Masa reducida
	alpha = G*m1*m2
	Momento = mu*perigeo*Vt
	Energia = (mu*(alpha**2)/(2*(Momento**2)))*(excen**2 - 1)
	Vr = math.sqrt(abs((2/mu)*(Energia + alpha/perigeo)-Vt**2))
	Periodo = math.pi*alpha*math.sqrt(mu/(2*abs(Energia)**3))
	return Vr,Energia,Momento,Periodo

