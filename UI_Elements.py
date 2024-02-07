import tkinter as tk
from PIL import Image, ImageTk


process = None
processStarted = False
lastDate = None
root = tk.Tk()
instances = []




class UI_Instance:
    def __init__(self,name,scrollable_frame):
        self.name = name
        self.size = 15
        self.resFolder = "res/icons/"
        self.IMG_connection_bad = ImageTk.PhotoImage(Image.open(self.resFolder + "connection_bad.png").resize((self.size,self.size)))
        self.IMG_connection_unknown= ImageTk.PhotoImage(Image.open(self.resFolder + "connection_unknown.png").resize((self.size,self.size)))
        self.IMG_connection_good= ImageTk.PhotoImage(Image.open(self.resFolder + "connection_good.png").resize((self.size,self.size )))
        self.status = "unknown"

        self.label_frame = tk.Frame(scrollable_frame.frame, padx=10, pady=10)
        self.label_frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.label_frame, text=name)
        self.label.pack(side="left")

        self.image_label = tk.Label(self.label_frame, image=self.IMG_connection_unknown)
        self.image_label.image = self.IMG_connection_unknown
        self.image_label.pack(side="right")
        
    def changeStatus(self,status):

            if(status !=self.status):
                if(status == "good"):
                    new_photo = self.IMG_connection_good     
                elif(status == "bad"):
                    new_photo = self.IMG_connection_bad
                elif(status == "unknown"):
                    new_photo = self.IIMG_connection_unknown
                self.image_label.configure(image=new_photo)
                self.image_label.image = new_photo

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


def on_closing():
 terminate_subprocess()   
 root.destroy()

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
  