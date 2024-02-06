import xml.etree.ElementTree as ET
import xmltodict
import json
from utility import printInLog,config

def xml_element_to_dict(element):
    result = {}
    for child in element:
        result[child.tag] = xml_element_to_dict(child) if len(child) > 0 else child.text
    return result

def xml_tree_to_dict_list(xml):
    root = ET.fromstring(xml)
    return [xml_element_to_dict(element) for element in root]





def checkNewTicket(array1, array2):
    return any(item not in array1 for item in array2)



def XMLtoJson(xml):
    xml_dict_list = xml_tree_to_dict_list(xml)
    return xml_dict_list

def getTicketNumberArray(ticketjson):
    ticketarray = []
    try:
        for i in range(len(ticketjson)):
            ticketarray.append(ticketjson[i]["number"])

    except Exception as e:
        printInLog(f"{e}","error","GLOBAL")

    return ticketarray

def find_different_elements(array1, array2):

    return list(set(array1) ^ set(array2))

#Function searches for tickets
#tag is for example number and value ITASK1312
#args is for setting output 
def findTicket(ticketjson,tag,value,args = ["all"]):    
    tickets = []
    tmpobj = []
    for item in ticketjson:
        if(item[tag] == value):
                if(args[0] == "all"):
                    
                    tickets.append(item)  
                else:
                    for arg in args:
                        tmpobj.append(item[arg])
                tickets.append(tmpobj)
    return tickets
                        
                       
        





def convertPriorityToName(prio):
    names ["critical","high","medium","low"]
    return names[prio]
