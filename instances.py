from utility import loadjson
from plyer import notification
import time
from playsound import playsound
from utility import config
import json
#Disclaimer this file contains A LOT of OOP stuff, nothing interesting. 


#Creates profiles for filtering the tickets
class Profile:
    def __init__(self,
    id,name,
    conditions,
    sound,
    notification_suppress,
    notification_title,
    notification_message,
    notification_timeout):

        self.id = id
        self.name = name
        self.conditions = conditions
        self.notification_suppress = notification_suppress
        self.notification_title = notification_title
        self.notification_message = notification_message
        self.sound = sound
        self.notification_timeout = notification_timeout


    def printInfo(self):
        print(f"\nProfile: {self.name}")
        print(f"Conditions: {self.conditions}")
        print(f"Sound: {self.sound}")
        print(f"Notification Suppress: {self.notification_suppress}")
        print(f"Notification Title: {self.notification_title}")
        print(f"Notification Message: {self.notification_message}")
        print(f"notification Timeout: {self.notification_timeout}")

#Creates instance for the script to be able to monitor multiple instances, Created for NUBO,DOMO usage
class Instance:
    def __init__(self,name):
        self.name = name
        self.path = config["instances_path"] + name + ".json"
        self.json_data = loadjson(self.path)
        self.settings =  self.json_data.get("settings", {})
        self.instance_name =  self.settings.get("instance_name", "")
        self.url = self.settings.get("url", "")
        self.fetch_url =  self.settings.get("fetch_url", "")
        self.url_addon =  self.settings.get("url_addon", "")
        self.profiles = self.json_data.get("profiles", {})
        self.headers = self.settings.get("headers_json", {})
        self.cookies= ""
        self.ticketNumberArray = []
        self.ticketjson = {}
        self.profilesArray = []
        self.createProfiles()
#Send notification to your OS, I hope this is compatible with most enviroments, on Gnome it works

    def sendNotification(self,profile,ticket):
        ticket = ticket[0]
        notification.notify(
            title=profile.notification_title.format(**ticket),
            message=profile.notification_message.format(**ticket),     
            timeout=profile.notification_timeout
            
        )   
        playsound(profile.sound)

   



    def createProfiles(self):
        i = 0
        for profile_name, profile_data in self.profiles.items():
            self.profilesArray.append(Profile(
            i,
            profile_name,
            profile_data.get("conditions",""),
            profile_data.get("sound", ""),
            profile_data.get("notification_suppress", 0),
            profile_data.get("notification_title", ""),             
            profile_data.get("notification_message", ""),
            profile_data.get("notification_timeout", "")))
            
            
            i+=1

    def printInfo(self):
        print("Settings:")
        print(f"Instance Name: {self.instance_name}")
        print(f"URL: {self.url}")
        print(f"Fetch URL: {self.fetch_url}")
        print(f"URL Addon: {self.url_addon}")
        for item in self.profilesArray:
            item.printInfo()
            
        
