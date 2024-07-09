from tkinter import *
from tkinter import font as tkfont
from tkinter.messagebox import showerror, askyesno
import MainWindow as MW
import ParameterNewProjectWindow as PNPW
import ParameterStreamProjectWindow as PSPW
import StreamWindow as SW
import VideoWindow as VW
import Data
import view


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Birdy")     
        self.geometry("700x400")  
        self.iconbitmap(default="icon/sparrow.ico")  
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.initialization_dir()

        self.data=Data.Data()
        self.windows_list=[]
        self.frames = {}
        
        for F in (MW.MainWindow,PNPW.ParameterNewProjectWindow,SW.StreamWindow,PSPW.ParameterStreamProjectWindow,VW.VideoWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("MainWindow")
        self.protocol("WM_DELETE_WINDOW", self.close_window)
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    def initialization_dir(self):
        try:
            view.initialization()
        except:
            showerror(title="Ошибка", message="Непредвиденная ошибка!")
            self.destroy()
    def close_window(self):
        result = askyesno(title="Подтвержение операции", message="Вы действительно хотите закрыть приложение?")
        if result: 
            for item in self.windows_list:
                item.destroy()
            self.destroy()
