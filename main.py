from cookieProcess import addCookiesToHeaders, get_cookies_after_manual_login
import requests
import time
from ticketProcess import XMLtoJson,getTicketNumberArray,find_different_elements,findTicket,checkNewTicket
from utility import config, loadcfg ,loadjson,printInLog
from instances import Instance
from utility import config,handle_terminate_signal,TerminateHandler,print_current_pid,getCorrectProfile

#This is the main file, it looks horrible

def main():

 printInLog("Script started","info","GLOBAL")
 config = loadcfg()
 print_current_pid(False)

 ticketNumberArray = []
 instancesArray = []
#Get instance names from cfg, I dont want the script to sniff in your filesystem. 
 names = config["instances_file_names"].split(",") 
#This loop creates instance object for every instance configured
 for i in range (len(names)):
        instancesArray.append(Instance(names[i])) 
        try:
                instancesArray[i].cookies = get_cookies_after_manual_login(instancesArray[i].url)
                printInLog("Cookies loaded","info",instancesArray[i].instance_name)
                
        except Exception as e:
                #The error is not logged for the security reasons.
                printInLog(f"error fetching cookies: ","error",instancesArray[i].instance_name) 
        
        printInLog(instancesArray[i].instance_name,"instance_init",instancesArray[i].instance_name)

                


 started = False

#Main loop which does all the magic
 while (True):
        if(started == False):
         printInLog("Script started","info","GLOBAL")
         
        #This loop cycles between Insances
        for item in instancesArray:
        #This creates request to the SNOW, it creates the url which exports XML file and adds headers with cookies. 
         response = requests.get(item.fetch_url + item.url_addon, headers=addCookiesToHeaders(item.headers,item.cookies))
        #Checks if the response is ok and if there are tickets.
         if response.ok and len(response.text) != 46: 
                item.ticketjson = XMLtoJson(response.text)
                printInLog("Status OK","status_handler",item.instance_name)
                #This looks horrible but it compares array with tickets from last cycle and new array.If new tickets are detected, for loop will create notifications
                if(checkNewTicket(item.ticketNumberArray,getTicketNumberArray(item.ticketjson))):
                        for ticket in getTicketNumberArray(item.ticketjson):
                                item.sendNotification(item.profilesArray[getCorrectProfile(item.profilesArray,findTicket(item.ticketjson,"number",ticket))],
                                findTicket(item.ticketjson,"number",ticket)) ##THIS IS DISCUSTING
                                                                  
                else:
                        #Logging stuff.
                        printInLog("No new ticket","verbose",item.instance_name)
                        printInlog(item.ticketNumberArray,"verbose+",item.instance_name)
                #Rewrites the array with active tickets. 
                item.ticketNumberArray = getTicketNumberArray(item.ticketjson)
         #When the XML file is long 46 chars it means that there is 0 tickets. 
         elif len(response.text) == 46:
                
          printInLog("Status OK","status_handler",item.instance_name)

          printInLog("0 tickets","verbose",item.instance_name)
          #Clears the array
          item.ticketNumberArray.clear()
         else:
                #Logging errors
                printInLog("Failed fetching url in  " + str(response),"error",item.instance_name)
                printInLog("Disconnected","status_handler",item.instance_name)

        #Waits for next cycle 
        #This is needed for the script to not be DOS
        time.sleep(int(config["tickets_refresh_time"]))
        #Loging stuff, not needed but i like it
        if(started == False):
         printInLog("First loop completed, Open for Alerting","info","GLOBAL")
         started = True


if __name__ == "__main__":
    try:
        TerminateHandler()
        main()
    except Exception as e:
        #If this happends something went really wrong.
        printInLog(f"{e}","error","GLOBAL")

