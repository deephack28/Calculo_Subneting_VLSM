#!/usr/bin/env python3
global listas_numero_host
listas_numero_host = list()

#Errores
def vacio(dato):
    if dato == "":
        print("Se debe de introducir algún dato")
        exit()

def max_hosts(mascara):
    mascara = tratamiento_mascara(mascara)[3]
    hosts = 32 - int(mascara)
    maximo = 2**hosts
    total = maximo -2
    return total

def comprobar_letra(dato):
    ip_decimal = ""
    try:
        sec =""
        for x in ip:
            if x != ".":
                sec += x
            else:
                ip_decimal = sec
                ip_decimal = int(ip_decimal)
                sec =""
        ip_decimal = int(sec)
    except:
        print("No puede contener letras")
        exit()

def comprobacion_correcta_ip(ip):
    contador = 0
    sec =""
    for x in ip:
        if x != ".":
            sec += x
        else:
            ip_decimal = sec
            contador += 1
        if ip_decimal > 255 or ip_decimal < 0 :
            print("La ip introducida no es correcta")
            exit()
            break
        elif contador != 3 and ip_decimal == "":
            print("La ip introducida no es correcta")
            exit()
            break
def todos_los_errores(dato):
    esta_vacio = vacio(dato)
    letra= comprobar_letra(dato)

    if esta_vacio == True or letra == True:
        print("Se debe de introducir algún dato")
        exit()
    else:
        pass

    return 


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

ip = input("Dime la dirección ip: ")
todos_los_errores(ip)
mascara = input("Dime la mascara: ")
todos_los_errores(ip)
if tratamiento_mascara(mascara)[3] > 30 or tratamiento_mascara(mascara)[3] < 0:
    print("La máscara no es válida")
    exit() 
subredes= input("Cuantas subredes quieres: ")
todos_los_errores(ip)

for veces in range(int(subredes)):
    numero_host= int(input("Cuantos equipos por subred: "))
    listas_numero_host.append(numero_host)

lista_ordenada = sorted(listas_numero_host, reverse=True)


total_host = sum(lista_ordenada)
if int(max_hosts(mascara)) < int(total_host):
    print("La ip proporcionada no puede direccionar a "+ str(total_host) + " hosts")
    exit() 

print("-------------------------------")
print("Datos introducidos: ")
print("Ip: "+ str(ip))
print("Máximo hosts: "+ str(max_hosts(mascara)))
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
