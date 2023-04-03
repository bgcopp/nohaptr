from pyzkaccess import ZKAccess
from datetime import datetime
from colorama import Fore, Back, Style
from time import sleep
import threading
import configparser
import time, json
import logging, logging.handlers
import requests  #Importamos la librería requests
import socket
import sys

'''
TimedRotatingFileHandler Constructor declaration 
class logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None)
filename  Log file name prefix 
when  Log name change time unit 
 'S' Seconds
 'M' Minutes
 'H' Hours
 'D' Days
 'W0'-'W6' Weekday (0=Monday)
 'midnight' Roll over at midnight
interval  Interval time refers to waiting N A when Automatically rebuild files after units of time 
backupCount  Keep the maximum number of log files, exceed the limit, delete the first file created; Default value 0 Indicates no restrictions. 
delay  Delay file creation until the 1 Secondary call emit() Method to create a log file 
atTime  At the specified time ( datetime.time Format to create a log file. 
'''

config = configparser.ConfigParser()
config.read('config.ini')

cadena = config['DEFAULT']['TCP_STR']

# funcion para presentacion de log's
def printLog(str):
    print(Back.BLUE  + Fore.WHITE + f"[{datetime.now()}] " + Style.RESET_ALL + str)

#camara entrada
def tarea(bandera):
    #zk.doors[int(config['DEFAULT']['DOOR'])].relays.switch_on(int(config['DEFAULT']['TIME_ON_DOOR']))
    print(Back.GREEN  + Fore.WHITE + f"[{datetime.now()}] " + Style.RESET_ALL + "Entro del hilo camara entrada")
    i = 0
    ultimafecha = "01/01/2017 08:00:00" #= #datetime.strptime("01/01/2017 08:00:00", "%d/%m/%Y %H:%M:%S")
    while True:
        global stop_threads
        i = i + 1
        #if (i%5)==0:
        #    zk.doors[int(config['DEFAULT']['DOOR'])].relays.switch_on(int(config['DEFAULT']['TIME_ON_DOOR']))
        URLLPRNOHA = ""
        URLLPRNOHA = config['DEFAULT']['URL_CAM1SRV']
        try:
            #consulta servicio de camara
            response = requests.get(URLLPRNOHA)
            if response.status_code == 200:
                objcamgen = json.loads(response.text)
                #s = str(objcamgen["Data"]).replace("\'", "\"")
                #s = str()
                try:
                    objcam = objcamgen #json.loads(s)  
                    plate = str(objcam["Plate"])  
                except:
                    plate = "QQQAAAXXX"

                printLog("Lectura Placa- entrada: " + plate)
                dt_object1 = str(objcam["DateHour"])
                
                #procesa la placa
                if (plate != "QQQAAAXXX") & (plate != "*") & (ultimafecha != dt_object1):
                    ultimafecha = dt_object1
                    URLLPRNOHA = config['DEFAULT']['URL_NOHAAPIINALT']
                    response = requests.post(URLLPRNOHA + "/" + plate  )
                    if response.status_code == 200:
                        obj = json.loads(response.text)
                        if obj["Resultado"] == True :
                            # open door1
                            zk.doors[int(config['DEFAULT']['DOOR'])].relays.switch_on(int(config['DEFAULT']['TIME_ON_DOOR']))
                            time.sleep(5.1)
                            URLCAM = ""
                            URLCAM = config['DEFAULT']['URL_CAM1SRV']
                            printLog("Abrir camara 1 ok placa =>" + plate)
                                #URLPAINOHA = config['DEFAULT']['URL_NOHAAPIOUT']
                            try:
                                #limpia lecturas 
                                #response = requests.post(URLCAM)
                                i1=0
                            except Exception  as ex:
                                printLog("erro limpiando entrada" + str(ex)) 
                        else :
                            printLogErr("error verify:  " + "card" + " - " + plate + " => " +  json.dumps(obj))
                    else :
                        printLogErr("error: api " + "card" + " - " + plate + " => " + response.text)
                else:
                    i1=0
                    #printLogErr("Placa: Placa vacia o repite placa " + plate + " => " + ultimafecha)
                #fin
            else:
                printLogErr("error: api " + response.text)
        except BaseException  as e:
            printLogErr("error: consultando servicio camara. Servicio no disponible " + URLLPRNOHA + str(e))
            #continue        
                
        time.sleep(0.1)
        if stop_threads:
            break
    print(Back.GREEN  + Fore.WHITE + f"[{datetime.now()}] " + Style.RESET_ALL + "Salir del hilo")
   
        
#camara salida
def tarea2(bandera):
    #zk.doors[int(config['DEFAULT']['DOOR'])].relays.switch_on(int(config['DEFAULT']['TIME_ON_DOOR']))
    print(Back.GREEN  + Fore.WHITE + f"[{datetime.now()}] " + Style.RESET_ALL + "Entro del hilo camara salida")
    i = 0
    ultimafecha = "01/01/2017 08:00:00" #= #datetime.strptime("01/01/2017 08:00:00", "%d/%m/%Y %H:%M:%S")
    while True:
        global stop_threads
        i = i + 1
        #if (i%5)==0:
        #    zk.doors[int(config['DEFAULT']['DOOR'])].relays.switch_on(int(config['DEFAULT']['TIME_ON_DOOR']))
        URLLPRNOHA = ""
        URLLPRNOHA = config['DEFAULT']['URL_CAM2SRV']
        try:
            #consulta servicio de camara
            response = requests.get(URLLPRNOHA)
            if response.status_code == 200:
                objcamgen = json.loads(response.text)
                #s = str(objcamgen["Data"]).replace("\'", "\"")
                #s = str()
                try:
                    objcam = objcamgen #json.loads(s)  
                    plate = str(objcam["Plate"])  
                except:
                    plate = "QQQAAAXXX"

                printLog("Lectura Placa salida: " + plate)
                dt_object1 = str(objcam["DateHour"])
                
                #procesa la placa
                if (plate != "QQQAAAXXX") & (plate != "*") & (ultimafecha != dt_object1):
                    ultimafecha = dt_object1
                    URLLPRNOHA = config['DEFAULT']['URL_NOHAAPIOUTALT']
                    response = requests.post(URLLPRNOHA + "/" + plate  )
                    if response.status_code == 200:
                        obj = json.loads(response.text)
                        if obj["Resultado"] == True :
                            # open door1
                            zk.doors[int(config['DEFAULT']['DOOR'])].relays.switch_on(int(config['DEFAULT']['TIME_ON_DOOR']))
                            time.sleep(5.1)
                            URLCAM = ""
                            URLCAM = config['DEFAULT']['URL_CAM1SRV']
                            printLog("Abrir camara 2 ok placa =>" + plate)
                                #URLPAINOHA = config['DEFAULT']['URL_NOHAAPIOUT']
                            try:
                                #limpia lecturas
                                #response = requests.post(URLCAM)
                                i1=0
                            except Exception  as ex:
                                printLog("erro limpiando salida" + str(ex)) 
                                
                        else :
                            printLogErr("error verify:  " + "card" + " - " + plate + " => " +  json.dumps(obj))
                    else :
                        printLogErr("error: api " + "card" + " - " + plate + " => " + response.text)
                else:
                    i1=0
                    #printLogErr("Placa vacia o repite placa " + plate + " => " + ultimafecha)
                #fin
            else:
                printLogErr("error: api " + response.text)
        except BaseException  as e:
            printLogErr("error: consultando servicio camara. Servicio no disponible " + URLLPRNOHA + str(e))
            #continue        
                
        time.sleep(0.1)
        if stop_threads:
            break
    print(Back.GREEN  + Fore.WHITE + f"[{datetime.now()}] " + Style.RESET_ALL + "Salir del hilo")
   
def tareaLecturaLoop (bandera):
    print( "hola pic" )
    while True:
        global stop_threads
        if stop_threads:
            break
        zk.aux_inputs.events.refresh()
        for door1_event in zk.aux_inputs[0].events.poll():
            print( "" + door1_event.pin + str(door1_event))

        #time.sleep(0.2)
        #zk.doors.aux_inputs[0].data




def printLogOk(str):
    print(Back.GREEN  + Fore.WHITE + f"[{datetime.now()}] " + Style.RESET_ALL + str)

def printLogErr(str):
    print(Back.RED  + Fore.YELLOW + f"[{datetime.now()}] " + Style.RESET_ALL + str)
    logging.error(str)

def initLog():
    fmt_str = '%(asctime)s[level-%(levelname)s][%(name)s]:%(message)s'
    fileshandle = logging.handlers.TimedRotatingFileHandler('AppLog', when='H', interval=12, backupCount=3)
    fileshandle.suffix = "%Y%m%d_%H%M%S.log"
    fileshandle.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt_str)
    fileshandle.setFormatter(formatter)
    #  Add to the Log Processing Object Collection 
    logging.getLogger('').addHandler(fileshandle)

def processCard(card, entry):
    plate = None
    # Switch on both relays on door 1
    # zk.doors[1].relays.switch_on(5)

    # Wait to read Camera Result Plate
    # requests.get()
    URLLPRNOHA = ""
    if entry == True:
        URLLPRNOHA = config['DEFAULT']['URL_CAM1SRV']
    else:
        URLLPRNOHA = config['DEFAULT']['URL_CAM2SRV']
    try:
        response = requests.get(URLLPRNOHA)
    except:
        printLogErr("error: consultando servicio camara. Servicio no disponible " + URLLPRNOHA)
        quit()

    if response.status_code == 200:
        objcamgen = json.loads(response.text)
        s = str(objcamgen["Data"]).replace("\'", "\"")
        try:
            objcam = json.loads(s)  
            plate = str(objcam["Plate"])  
        except:
            plate = "QQQAAAXXX"
        printLog("Lectura Placa: " + plate)
    else:
        printLogErr("error: api " + response.text)

    # Call to API AUTH NOHA

    #if config['DEFAULT']['TESTPROBE'] == "1":
    #    card = "F0383080A"
    #    plate = "BCF449"
    URLPAINOHA = ""
    if entry == True:
        URLPAINOHA = config['DEFAULT']['URL_NOHAAPIIN']
    else:
        URLPAINOHA = config['DEFAULT']['URL_NOHAAPIOUT']

    #URLPAINOHA = config['DEFAULT']['URL_NOHAAPIOUT']
    response = requests.post(URLPAINOHA + "/" + card + "/" + plate )
    if response.status_code == 200:
        obj = json.loads(response.text)
        if obj["Resultado"] == True :
            # open door1
            zk.doors[int(config['DEFAULT']['DOOR'])].relays.switch_on(int(config['DEFAULT']['TIME_ON_DOOR']))
        else :
            printLogErr("error verify:  " + card + " - " + plate + " => " +  json.dumps(obj))
    else :
        printLogErr("error: api " + card + " - " + plate + " => " + response.text)

initLog()
printLog(config['DEFAULT']['APPTEST'])
#logging.debug("logging.debug")
#logging.info("logging.info")
#logging.warning("logging.warning")
#logging.error("logging.error")


printLog("Cadena CNX: " + cadena)

#connstr = 'protocol=TCP,ipaddress=192.168.1.201,port=4370,timeout=4000,passwd='
connstr = ""
printLog("Nueva ejecución NOHAPTR")
#r"C:\ed proteccion\OC\teko\NOHAPTR\plcommpro.dll"
pathdll = config['DEFAULT']['DLLPATH']
try:
    zk = ZKAccess(connstr=cadena, dllpath= r"" +  str(pathdll) )
except Exception  as ex:
    printLogErr("error: TCP CNX " + str(ex))
    URLCAM = ""
    URLCAM = config['DEFAULT']['URL_CAM1SRV']

        #URLPAINOHA = config['DEFAULT']['URL_NOHAAPIOUT']
    response = requests.post(URLCAM)
    printLogOk("Limpieza Exitosa")
    quit()
printLogOk("Conexión Exitosa")
printLog('Device SN:' + zk.parameters.serial_number + ' IP:' + zk.parameters.ip_address)

# Turn on relays in "lock" group for 5 seconds
#zk.relays.lock.switch_on(5)
# zk.relays[1].switch_on(5)  # By index
#zk.doors[int(config['DEFAULT']['DOOR'])].relays.switch_on(int(config['DEFAULT']['TIME_ON_DOOR']))
URLCAM = ""
URLCAM = config['DEFAULT']['URL_CAM1SRV']

    #URLPAINOHA = config['DEFAULT']['URL_NOHAAPIOUT']
try:
    #limpia lecturas
    response = requests.post(URLCAM)
except Exception  as ex:
    printLog("erro limpiando" + str(ex)) 
    quit()
    
bandera = True
#leer camaras para entrada directa
stop_threads = False
hilo = threading.Thread(target=tarea, args=(True,))
hilo.start()

hilo2 = threading.Thread(target=tarea2, args=(True,))
hilo2.start()

#hilo3 = threading.Thread(target=tareaLecturaLoop, args=(True,))
#hilo3.start()

# Wait for any card will appear on reader of Door 1
card = None
plate = None
entry = False
i = 0
try:
    while i < 50: #not card: # and i < 2:
        printLog("Esperando Tarjeta en el lector")
        for door1_event in zk.events.poll(timeout=120):  
            # if(door1_event.door == 1 & door1_event.card != '0') :            
            #     print("loop afuera")
            #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     server_add = ('192.168.0.87',8060)
            #     print("conectando camara")
            #     sock.connect(server_add)
            #     try:
            #         message = b"$"
            #         sock.sendall(message)
            #     finally:
            #         sock.close()
            # elif (door1_event.door == 2 & door1_event.card != '0'):
            #     print("loop adentro")
            #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     server_add = ('192.168.0.86',8060)
            #     print("conectando camara")
            #     sock.connect(server_add)
            #     try:
            #         message = b"$"
            #         sock.sendall(message)
            #     finally:
            #         sock.close()
        
        # print(str(door1_event) + "-" + str(door1_event.door) )   

            if door1_event.card and door1_event.card != '0':
                if door1_event.entry_exit.value == 1:
                    entry = False
                    printLog("Tajeta Salida " )                
                else:
                    entry = True
                    printLog("Tajeta Entrada ")

                printLog('Got card #' + door1_event.card + " hex -> [ " + hex(int(door1_event.card)) + " ]")
                card = door1_event.card
                #processCard(hex(int(door1_event.card)),entry)
    i= i + 1
except Exception  as ex:
    printLog("erro limpiando" + str(ex)) 

stop_threads = True
hilo.join()
hilo2.join()
#hilo3.join()

printLog("Salida de tarjeta e hilos" )    

URLCAM = ""
URLCAM = config['DEFAULT']['URL_CAM1SRV']

    #URLPAINOHA = config['DEFAULT']['URL_NOHAAPIOUT']
try:
    #limpieza de placas
    response = requests.post(URLCAM)
except Exception  as ex:
    printLog("erro limpiando" + str(ex)) 


# After that restart a device
#zk.restart()
time.sleep(0.5) #ojo BGC
try:
    zk.disconnect()
except:
    printLog("erro limpiando" + str(ex)) 
#Event(time=2022-12-15 23:47:10, pin=0, card=78228050, door=1, event_type=27, entry_exit=PassageDirection.exit, verify_mode=VerifyMode.not_available)
#Got card # 78228050
#Event(time=2022-12-15 22:41:30, pin=0, card=78228050, door=1, event_type=27, entry_exit=PassageDirection.entry, verify_mode=VerifyMode.not_available)
#Got card # 78228050