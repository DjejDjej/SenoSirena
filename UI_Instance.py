import tkinter as tk
from PIL import Image, ImageTk

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

