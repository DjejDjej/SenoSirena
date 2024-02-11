import json
import logging
from datetime import datetime
import signal
import sys
import os
import platform
import re


def handle_terminate_signal(signum, frame):
        print("Exit from terminal")
        # Perform cleanup operations here if needed
        print_current_pid(True)

        sys.exit(0)


def print_current_pid(isnull):
    with open(config["log_folder"] + "/process.pid", 'w') as file:
        if(isnull == False):
      
            file.write(str(os.getpid()))
        else:file.write(str(""))


def printToFile_rm(path,message):
      with open(path,'w') as file:
            file.write(message + "\n")



def TerminateHandler():
    signal.signal(signal.SIGTERM, handle_terminate_signal)


#Loads json from path. 
def loadjson(file_path): 

    with open(file_path, 'r') as file:
        loadedjson = json.load(file)

    return loadedjson

#Returns config file
def loadcfg():
    return loadjson("cfg/settings.json")
config = loadcfg()

#Function used for logging things, looks nice, the loging style kinda stolen from WAS, please dont sue me
def printInLog(message,logType,instance):
    log_folder = config["log_folder"]
    log_level = config["log_level"]
    logging.basicConfig(filename= log_folder + '/error.log', level=logging.ERROR)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if(logType == "instance_init"):printToFile_rm(log_folder + "/instances",instance)
    if(logType == "error"):
        print(f"{current_datetime}: [ERROR]: {instance}  {message} ----------------- \n \n \n ")        
        logging.error(f"{current_datetime}: [ERROR]: {instance}  {message}",exc_info=True)   #Errors from directly from python, hard to read. really hard
    if(logType == "status_handler"):
        printToFile(f"{log_folder}/{instance}_status.log",f"{current_datetime} [STATUS]: [{instance}] {message}")  #Used for comunication with GUI
    if(logType == "info" and log_level >= 1):
        printToFile(log_folder + "/out.log",f"{current_datetime} [INFO]: [{instance}]: {message}")      #Info for paranoid people
    if(logType == "verbose"and log_level >= 2):
        printToFile(log_folder + "/out.log",f"{current_datetime} [VERBOSE]: [{instance}]: {message}")   #Info for curious people
    if(logType == "verbose+"and log_level>= 3):
        printToFile(log_folder + "/out.log",f"{current_datetime} [VERBOSE+]: [{instance}]: {message}") #Info for me or for not GUI users (S/O to you)
        


#This will write content into file and also into console (For no GUI users <3)
def printToFile(file_path, content):
    print(content)
    try:
        with open(file_path, 'a+') as file:
            file.seek(0)
            is_empty = not file.read(1)
            if is_empty:
                file.write('\n')
            file.write(content + '\n')
    except Exception as e:
        logging.error(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: + {e}",exc_info=True)

#This has to be here. 
printInLog("CFG loaded","info","GLOBAL")


def decodeConditions(strcondition):

    return re.findall(r'\[([^]]+)\]', strcondition)


def getConditionBool(strcondition,ticket):
    
        
        try:
            
        
            condArray = strcondition.split(",")
            print(str(ticket[condArray[0]]) in condArray[2])
            print(condArray[2] in str(ticket[condArray[0]]))
            if condArray[1] == "is" and str(ticket[condArray[0]]) == condArray[2]:
                    return True
            if condArray[1] == "contains" and condArray[2] in str(ticket[condArray[0]]):
                    return True
            if condArray[1] == "startswith" and str(ticket[condArray[0]]).startswith(condArray[2]):
                    return True
            if condArray[1] == "endswith" and str((ticket[condArray[0]])).endswith(condArray[2]):
                    return True
            if condArray[1] == "notcontains" and  str((ticket[condArray[0]])) not in condArray[2]:
                    return True
            if condArray[1] == ">" and int(ticket[condArray[0]]) > int(condArray[2]):
                    return True
            if condArray[1] == "<" and int(ticket[condArray[0]]) < int(condArray[2]):
                    return True

        except Exception as e:
            printInLog("Error syntax profile  - "+ strcondition,"error,","GLOBAL")
        return False
        


def getProfileBool(conditions,ticket):
    
    decoded = decodeConditions(conditions)

    for item in decoded:
        
        conditions = conditions.replace(item,str(getConditionBool(item,ticket))).replace("[","").replace("]","")
    
    
    return eval(conditions)   


def getCorrectProfile(profileArray,ticket):
    ticket = ticket[0]

    if(len(profileArray) > 1 ):

        for i in range(1,len(profileArray)):
            if(getProfileBool(profileArray[i].conditions,ticket) == True):
                return i
    else: return 0  
    return 0
        

