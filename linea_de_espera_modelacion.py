# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:22:16 2022

@author: 80157
"""

import itertools
import random
import math
import simpy
import matplotlib.pyplot as plt 
from numpy import maximum
from numpy import arange
from itertools import zip_longest
from itertools import dropwhile


SEMILLA = 30
NUM_SERVIDORES = 1
TIEMPO_SERVICIO_MIN = 0
TIEMPO_SERVICIO_MAX = 1
T_LLEGADAS = 1
TIEMPO_SIMULACION = 60
#TOT_CLIENTES = 959

te  = 0.0 # tiempo de espera total
dt  = 0.0 # duracion de servicio total
fin = 0.0 # minuto en el que finaliza
tiempos_espera = [] #Tiempos de espera en la fila
tiempos_espera2 = []
tiempos_pasa = []
tiempos_deja= []
tiempos_servicio=[]

def cortar(cliente):
	global dt  #Para poder acceder a la variable dt declarada anteriormente
	R = random.random()  # Obtiene un numero aleatorio y lo guarda en R
	tiempo = TIEMPO_SERVICIO_MAX - TIEMPO_SERVICIO_MIN  
	tiempo_corte = TIEMPO_SERVICIO_MIN + (tiempo*R) # Distribucion uniforme
	yield env.timeout(tiempo_corte) # deja correr el tiempo n minutos
	tiempos_servicio.append(tiempo_corte)
	print(" \o/ Servicio listo a %s en %.2f minutos" % (cliente,tiempo_corte))
	dt = dt + tiempo_corte # Acumula los tiempos de uso de la i


def cliente (env, name, personal ):
	global te
	global fin
	llega = env.now # Guarda el minuto de llegada del cliente
	print ("---> %s llego al servicio en el minuto %.2f" % (name, llega))
	with personal.request() as request: # Espera su turno
		yield request # Obtiene turno
		pasa = env.now # Guarda el minuto cuado comienza a ser atendido
		tiempos_pasa.append(llega)
		espera = pasa - llega # Calcula el tiempo que espero
		tiempos_espera.append(espera)
		tiempos_espera2.append(espera)
		te = te + espera # Acumula los tiempos de espera
		print ("**** %s pasa al servidor en el minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
		yield env.process(cortar(name)) # Invoca al proceso cortar
		deja = env.now #Guarda el minuto en que termina el proceso cortar 
		tiempos_deja.append(deja)
		print ("<--- %s deja el servicio en el minuto %.2f" % (name, deja))
		fin = deja # Conserva globalmente el ultimo minuto de la simulacion
	

def principal (env, personal):
	llegada = 0
	i = 0
	while True: # Para n clientes
		R = random.random()
		llegada = -T_LLEGADAS * math.log(R) # Distribucion exponencial
		yield env.timeout(llegada)  # Deja transcurrir un tiempo entre uno y otro
		i += 1
		env.process(cliente(env, 'Cliente %d' % i, personal)) 
 
print ("------------------- Bienvenido Simulacion Linea de Espera ------------------")
random.seed (SEMILLA)  # Cualquier valor
#random.random()
env = simpy.Environment() # Crea el objeto entorno de simulacion
personal = simpy.Resource(env, NUM_SERVIDORES) #Crea los recursos (peluqueros)
env.process(principal(env, personal)) #Invoca el proceso princial
env.run(until = TIEMPO_SIMULACION) #Inicia la simulacion

print ("\n---------------------------------------------------------------------")
print ("\nIndicadores obtenidos: ")

lpc = te / fin
print ("\nLongitud promedio de la cola: %.2f" % lpc)
tep = te / len(tiempos_espera)
print ("Tiempo de espera promedio = %.2f" % tep)
upi = (dt / fin) / NUM_SERVIDORES
print ("Uso promedio de la instalacion = %.2f" % upi)

'''
print ("\n\n Lista de tiempos de espera: ")
tiempos_espera.sort()
for i in range(len(tiempos_espera)):
    print("\nCliente "+str(i+1)+": "+str(tiempos_espera[i]))
'''


print("\n\nTiempos de servicio ordenados: ")
tiempos_servicio.sort()
for i in range(len(tiempos_servicio)):
    print(str(tiempos_servicio[i]))

k=len(tiempos_servicio)
def Estimador(x):
    return x/(k+1)

ans = []
clientes = []
tiempos_servicio.sort()
for i in tiempos_servicio:
    a = Estimador(i)
    ans.append(a)
    
print("\n\nEstimador ordenados: ")
ans.sort()
for i in range(len(ans)):
    clientes.append((i+1)/70)
    print(str(ans[i]))

   
print ("\n\n Lista de tiempos de llegada: ")
for i in range(len(tiempos_pasa)):
    print("\nCliente "+str(i+1)+": "+str(tiempos_pasa[i]))
  
print ("\n\n Lista de tiempos de salida: ")
for i in range(len(tiempos_deja)):
    print("\nCliente "+str(i+1)+": "+str(tiempos_deja[i]))
    
Lista = [] 
L2 = []
L3 = []
L4 = []
L5 = []
   
print("\n Lista Modificada (tiempos de llegada n+1)")
L1 = tiempos_pasa[1:70]

print("\nDiferencias a)\n")
Dif = [x-y for x,y in zip_longest(L1,tiempos_deja)]
for i in Dif:
    print(str(i))

L2 = tiempos_deja.copy()
L2.insert(0,0)
L3 = L2[0:69]
L4 = tiempos_pasa.copy()
L5 = L4[1:70]

print("\nCondicion a)\n")
condicionA = list(filter(lambda n: n>0, Dif))
for j in condicionA:
    print(str(j))

print("\nDiferencias b)\n")
dif = [x-y for x,y in zip_longest(L3,L5)]
for i in dif:
    print(str(i))
    
print("\nCondicion b)\n")
condicionB = list(filter(lambda n: n<0, dif))
for i in condicionB:
    print(str(i))
    
print('\n Lista para ajuste \n')

Ajuste = list(itertools.chain(condicionB,condicionA))
Ajuste.sort()
for p in Ajuste:
    print(str(p))

ajuste = list(filter(lambda n: n>0, Ajuste))
print("\nEstimador de weibul (distrinucion de weibul)\n")
L6 = []
L7 = []

def estimador(X):
    return (X)/(len(Ajuste)+1)

for i in Ajuste:
    J = estimador(i)
    L6.append(J)

for i in range(len(L6)):
    L7.append((i+1)/89)
    print(str(L6[i]))



t_fila = []   
t_fila1 = []   
for i in range(len(tiempos_deja)):
    t_fila.append(tiempos_deja[i]-tiempos_pasa[i])
    t_fila1.append(tiempos_deja[i]-tiempos_pasa[i])
print ("\n\n Tiempo en fila: ") 
for i in range(len(t_fila)):
    print(str(t_fila[i]))


orden = []
persona = []
Espera = []
t_fila.sort()
for i in range(len(t_fila)):
    y = Estimador(i)
    Espera.append(y)

Espera.sort()
print ("\n\n Tiempo en Espera: ")
for i in range(len(Espera)):
    orden.append((i+1)/70)
    persona.append(i+1)
    print(str(Espera[i]))


def F(t):
    return ((t)+ math.pow(math.e,-1)-math.pow(math.e,-1+t))/(math.pow(math.e,-1))

funcion = []
for i in Espera:
    z = F(i)
    funcion.append(z)



print ("\n---------------------------------------------------------------------")

plt.subplot(2,3,1)
plt.plot(tiempos_espera)
plt.title("Gráfica tiempos de espera")

plt.subplot(2,3,2)
plt.scatter(tiempos_servicio,clientes)
plt.title("Gráfica tiempos de servicio")


plt.subplot(2,3,3)
plt.scatter(t_fila, orden) 
plt.title("Gráfico tiempo en fila")

plt.subplot(2,3,4)
plt.plot(Espera, [F(i) for i in Espera])

plt.subplot(2,3,5)
plt.scatter(Ajuste,L7)

plt.subplot(2,3,6)
plt.plot(Ajuste)


plt.show()
