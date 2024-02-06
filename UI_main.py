import tkinter as tk
import subprocess
import threading
import signal
import re
from datetime import datetime,timedelta
import platform
import os
from PIL import Image, ImageTk
from UI_Instance import UI_Instance
from tkinter import ttk
process = None
processStarted = False
lastDate = None
root = tk.Tk()
instances = []

class ScrollableLabelFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.update_scrollbar_visibility()

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig("self.frame", width=canvas_width)
        self.update_scrollbar_visibility()

    def update_scrollbar_visibility(self):
        canvas_height = self.canvas.winfo_height()
        frame_height = self.frame.winfo_reqheight()

        if frame_height > canvas_height:
            self.vsb.pack(side="right")
        else:
            self.vsb.pack_forget()

def add_element_to_scrollable_frame(scrollable_frame,instance):
    label_frame = tk.Frame(scrollable_frame.frame, padx=10, pady=10)
    label_frame.pack(fill="both", expand=True)

    label = tk.Label(label_frame, text=text)
    label.pack(side="left")

    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(label_frame, image=photo)
    image_label.image = photo
    image_label.pack(side="right")



def update_scrollbar_visibility(self):
        canvas_height = self.canvas.winfo_height()
        frame_height = self.frame.winfo_reqheight()

        if frame_height > canvas_height:
            self.vsb.pack(side="right", fill="y")
        else:
            self.vsb.pack_forget()









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


def create_subprocess_on_click():
    global process
    global processStarted
    global instances
    if(processStarted == False):
        binary_path = "./SenoSirena"
        process = subprocess.Popen([binary_path])
        print("STARTED")
        processStarted = True
        instances = loadInstances(scrollable_frame)


def terminate_subprocess():
    global process
    global processStarted
    try:
        
        if process and process.poll() is None:
            process.terminate()
            print("KILLED")
            processStarted = False
            process = None
            kill_process(int(' '.join(read_file("logs/process.pid")).strip()))


    except Exception as e:
        print(f"{e}")
  
    

def loadInstances(scrollable_frame):
    instancesNames = read_file("logs/instances")
    instancesNames = [element.replace('\n', '') for element in instancesNames]
    instances = []
    for item in instancesNames:
        instances.append(UI_Instance(item,scrollable_frame))
        

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

   
def on_closing():
 terminate_subprocess()   
 root.destroy()


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





root.protocol("WM_DELETE_WINDOW", on_closing)


root.geometry(f"{int(window_width)}x{int(window_height)}")
root.resizable(False, False)









root.after(100, schedule_function_call(instances))




root.mainloop()
