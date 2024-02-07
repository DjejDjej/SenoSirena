import tkinter as tk
import subprocess
import threading
import signal
import re
from datetime import datetime,timedelta
import platform
import os
from PIL import Image, ImageTk
from tkinter import ttk
from UI_utility import config,clearLogs
from UI_Elements import *

lastDate = None








def kill_process(process_id):
    try:
        if platform.system() == "Windows":
            os.system(f"taskkill /F /PID {process_id}")
        elif platform.system() == "Linux":
            os.kill(process_id, signal.SIGKILL)
        else:
            print("Unsupported operating system") #If you have mac, buy normal computer LMAO
    except Exception as e:
        print(f"{e}")

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
                # Read the contents of the file into a list
                
                return file.readlines()
    except Exception as e:
        print(f"{e}")



    

def loadInstances(scrollable_frame):
    instancesNames = read_file("logs/instances")
    instancesNames = [element.replace('\n', '') for element in instancesNames]
    instances = []
    for item in instancesNames:
        instances.append(UI_Instance(item,scrollable_frame))
        clearLogs(f"logs/{item}_status.log")


    return instances



def handleConnection(instance):
    global lastDate
    content = read_file(f"logs/{instance.name}_status.log")
    newMessage = content[-1].strip()
    lastDate = datetime.strptime(re.compile(r'\b(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\b').search(newMessage).group(1),"%Y-%m-%d %H:%M:%S")
    current_date = datetime.now()
    print(current_date - lastDate)
    if((current_date - lastDate) < timedelta(minutes =3)):
        instance.changeStatus("good")

    else:
       instance.changeStatus("bad") 

   



# Create the main window
root.title("Percentage Size Rectangle")
def checkStatus(instances):
     for instance in instances:
        handleConnection(instance)


def schedule_function_call(instances):
    
    checkStatus(instances)
    root.after(180000, schedule_function_call,instances)  




button_frame = tk.Frame(root)
button_frame.pack(side="top", fill="x")


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = screen_width * 12 / 100
window_height = screen_height * 30 / 100


btn_startAlerting = tk.Button(button_frame, text="Start monitoring", command=create_subprocess_on_click)
btn_startAlerting.pack(side="left")

btn_terminateAlerting = tk.Button(button_frame, text="Terminate monitoring", command=terminate_subprocess)
btn_terminateAlerting.pack(side="right") 


scrollable_frame = ScrollableLabelFrame(root, relief="sunken", borderwidth=0)
scrollable_frame.pack(fill="both", expand=True)

loadInstances(scrollable_frame)

root.protocol("WM_DELETE_WINDOW", on_closing)


root.geometry(f"{int(window_width)}x{int(window_height)}")
root.resizable(False, False)









root.after(100, schedule_function_call(instances))




root.mainloop()
