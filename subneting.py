#!/usr/bin/env python3
from glob import escape
import os
global listas_numero_host
listas_numero_host = list()
global lista_ordenada
def borrarPantalla():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")

def max_hosts(mascara):
    mascara = tratamiento_mascara(mascara)[3]
    hosts = 32 - int(mascara)
    maximo = 2**hosts
    total = maximo -2
    return total, maximo

#Operacion en binario
def suma_binario(ip_binario):
    ip_convertida =separar_ip(ip_binario)
    puntitos = funcion_puntitos(ip_convertida)
    a = "1"
    cuarto_octal = slice(27,36)
    tercer_octal = slice(18,26)

    ip_cuarto_octal = puntitos[cuarto_octal]
    ip_tercer_octal = puntitos[tercer_octal]

    if ip_cuarto_octal == "11111111":
        sumar2 = bin(int(ip_tercer_octal,2)+ int(a,2))[2:].zfill(8)
        remplazar_tercer_octal = puntitos.replace(ip_tercer_octal, sumar2)
        remplazar_cuarto_octal = remplazar_tercer_octal.replace(ip_cuarto_octal, "00000000")
        ip_decimal_definitiva = funcion_decimal(remplazar_cuarto_octal)
        return ip_decimal_definitiva
    else:
        sum = bin(int(ip_cuarto_octal, 2) + int(a,2))[2:]
        remplazar_cuarto_octal =""
        if sum == "11111111":
            sumar2 = bin(int(ip_tercer_octal,2)+ int(a,2))[2:].zfill(8)
            remplazar_tercer_octal = puntitos.replace(ip_tercer_octal, sumar2)
            remplazar_cuarto_octal = remplazar_tercer_octal.replace(ip_cuarto_octal, "00000000")
            ip_decimal_definitiva = funcion_decimal(remplazar_cuarto_octal)
            return ip_decimal_definitiva
        else:
            sum = bin(int(ip_cuarto_octal, 2) + int(a,2))[2:]
            remplazar_cuarto_octal = puntitos.replace(ip_cuarto_octal, sum)
            ip_decimal_definitiva = funcion_decimal(remplazar_cuarto_octal)
            return ip_decimal_definitiva

#MASCARA
#Calcular la nueva mascara para las subredes 
def mascara_nueva_host(mascv2):
    mascara = tratamiento_mascara(mascv2)[3]
    calculo_bits =  32 - int(mascara)
    lista_mascara_barra = list()
    lista_host_maximo = list()
    for hosts in lista_ordenada:
        for bits in range(1,99):
            host_maximo = 2**bits
            if int(hosts) < int(host_maximo):
                restar_old_masc = int(calculo_bits) - int(bits)
                mascara_barra = int(restar_old_masc) + int(mascara) # Se obtiene /masc
                lista_mascara_barra.append(mascara_barra)
                lista_host_maximo.append(host_maximo)
                break
    return lista_mascara_barra, lista_host_maximo


def funcion_puntitos(ip):
    for x in range(8,len(ip),9):
        ip = ip[:x] + '.' + ip[x:]
    return ip

def tratamiento_mascara(primera_mascara):
    primera_mascara = int(str(primera_mascara).replace('/',""))
    unos = añadir_unos_a_mascara(primera_mascara)
    posicion = buscar_posicion(unos)
    mascara_binario = funcion_puntitos(unos)
    return unos, posicion, mascara_binario, primera_mascara

def añadir_unos_a_mascara(mascara):
    mascara_binario = ""
    for x in range(mascara):
        mascara_binario = mascara_binario + "1"
    mascara_binario = str(mascara_binario).ljust(32,'0')
    
    return mascara_binario

def buscar_posicion(mascara):
    posicion = mascara.find('0')
    return posicion




#IP
#separar ip por puntos

def tratamiento_ip(ip,mascara):
    ip_binario = separar_ip(ip)
    red = funcion_red(ip_binario,tratamiento_mascara(mascara)[1])
    decimal_Red = funcion_decimal(red)
    broadcast = funcion_broadcast(ip_binario,tratamiento_mascara(mascara)[1])
    decimal_Broadcast = funcion_decimal(broadcast)
    primer_host = funcion_primer_host(red)
    ultimo_host = funcion_ultimo_host(broadcast)
    return ip_binario, red, decimal_Red, decimal_Broadcast, primer_host, ultimo_host


def funcion_decimal(ip):
    mantener = ""
    sec =""
    for x in ip:
        if x != ".":
            sec += x
        else:
            ip_decimal = sec
            ip_decimal = int(ip_decimal,2)
            mantener += str(ip_decimal)+"."
            sec = ""
    ultimo = int(sec,2)
    mantener += str(ultimo)
    return mantener

def separar_ip(ip):
    ip_binario = ""
    sec = ""
    mantener = "" 
    for x in ip:
        if x != ".":
            sec += x
        else:
            ip_binario = sec
            ip_binario = bin(int(ip_binario))
            ip_binario = ip_binario[2:].zfill(8)
            mantener += str(ip_binario)
            sec = ""
    ultimo = bin(int(sec))
    ultimo = ultimo[2:].zfill(8)
    mantener += ultimo
    return mantener


def funcion_red(ip,posicion_mascara):
    for sustitucion in range(int(posicion_mascara),32):
        l = list(ip)
        l[sustitucion] ="0"
        ip_red = ip = "".join(l)
    introducion_ip_red = funcion_puntitos(ip_red)
    return introducion_ip_red

def funcion_broadcast(ip,posicion_mascara):
    for sustitucion in range(int(posicion_mascara),32):
        l = list(ip)
        l[sustitucion] ="1"
        ip_broadcast = ip = "".join(l)
    introducion_ip_broadcast = funcion_puntitos(ip_broadcast)

    return introducion_ip_broadcast

def funcion_primer_host(ip):
    l = list(ip)
    l[34] ="1"
    ip_broadcast = ip = "".join(l)
    ip_broadcast = funcion_decimal(ip_broadcast)
    return ip_broadcast

def funcion_ultimo_host(ip):
    l = list(ip)
    l[34] ="0"
    ip_ultimo_host = ip = "".join(l)
    ip_ultimo_host = funcion_decimal(ip_ultimo_host)
    return ip_ultimo_host



#Errores

correcto = False
while not correcto:
    try:
        ip = input("Dime la dirección ip: ")
        guardar =""

        for x in ip:
            if x != ".":
                guardar += x
            else:
                octal = int(guardar)
                guardar =""
                if octal > 255 or octal <= 0:
                    
                    break
                else:
                    correct = True
            
        ultimo = int(guardar)
        if ultimo > 255 or ultimo < 0:
            print("Formato incorrecto")
        else:
            correcto = True
    except (RuntimeError, TypeError, NameError, IndexError, ValueError):
        print("Error, formato incorrecto")

correcto = False
while not correcto:
    try:
        mascara = input("Dime la máscara: ")
        nueva_mascara = tratamiento_mascara(mascara)[3]
        
        if nueva_mascara == "":
            print("No has introducido nada")
            os.system("pause")
            borrarPantalla()
            correcto = False
        elif nueva_mascara <= 0 or nueva_mascara > 32:
            print("La máscara no es correcta")
            os.system("pause")
            borrarPantalla()
            correcto = False
        else:
            nueva_mascara = int(nueva_mascara)
            correcto = True
    except (RuntimeError, TypeError, NameError, IndexError, ValueError):
        print("Error, formato incorrecto")
        os.system("pause")
        borrarPantalla()

correcto = False
while not correcto:
    try:
        subredes = int(input("Cuantas Subrredes quieres: "))
        if subredes == "":
            print("No has introducido nada")
            os.system("pause")
            borrarPantalla()
            correcto = False
        elif subredes <= 0 or subredes > max_hosts(mascara)[1]:
            print("Es imposible calcular todas esas subrredes")
            os.system("pause")
            borrarPantalla()
            correcto = False
        else:
            subredes = int(subredes)
            correcto = True
    except (RuntimeError, TypeError, NameError, IndexError, ValueError):
        print("Error, formato incorrecto")
        os.system("pause")
        borrarPantalla()








correct = False
while not correct:
    try:
        for veces in range(int(subredes)):
            numero_host= int(input("Cuantos equipos por subred: "))
            listas_numero_host.append(numero_host)
            lista_ordenada = sorted(listas_numero_host, reverse=True)
            total_host_introducidos = sum(lista_ordenada)
        if total_host_introducidos > max_hosts(mascara)[0]:
            print("No se pueden introducir tantos equipos")
            os.system("pause")
            borrarPantalla()
            correct = False
        else:
            correct = True
    except (RuntimeError, TypeError, NameError, IndexError, ValueError):
        print("Error, formato incorrecto")
        os.system("pause")
        borrarPantalla()
        

print("-------------------------------")
print("Datos introducidos: ")
print("Ip: "+ str(ip))
print("Máximo hosts: "+ str(max_hosts(mascara)[0]))
print("Dirección red: "+ str(tratamiento_ip(ip,mascara)[2]))
direccion_red = tratamiento_ip(ip,mascara)[2]
print("Primer Host: "+ str(tratamiento_ip(ip,mascara)[4]))
print("Último Host: "+ str(tratamiento_ip(ip,mascara)[5]))
print("Dirección Broadcast: "+ str(tratamiento_ip(ip,mascara)[3]))
print("-------------------------------")
print("SUBREDES")

varias_ips = list()
varias_ips.append(direccion_red)
mascara_v2 = list()
varias_hosts_maximo = list()

#print(lista_ordenada)
contador = 1
for y in mascara_nueva_host(mascara)[0]:
    mascara_v2.append(y)

for z in mascara_nueva_host(mascara)[1]:
    varias_hosts_maximo.append(z)
for x in range(int(subredes)):
    
    print("--------------")
    print("Subred: "+str(contador) )
    print("Hosts: "+ str(lista_ordenada[x]))
    print("Dirección red: "+ str(tratamiento_ip(varias_ips[x],mascara_v2[x])[2])+"/"+ str(mascara_v2[x]))
    print("Primer Host: "+ str(tratamiento_ip(varias_ips[x],mascara_v2[x])[4]))
    ultimo_broadcast = suma_binario(tratamiento_ip(varias_ips[x],mascara_v2[x])[3])
    print("Último Host: "+ str(tratamiento_ip(varias_ips[x],mascara_v2[x])[5]))
    print("Dirección Broadcast: "+ str(tratamiento_ip(varias_ips[x],mascara_v2[x])[3]))
    varias_ips.append(ultimo_broadcast)
    contador += 1