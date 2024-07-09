from tkinter import *
from tkinter import ttk
import threading
from tkinter.messagebox import showinfo,showerror, askyesno
import view

class VideoWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.fl_loading=[0]
        self.text=[""]

        self.label_text=Label(self,text="Подождите, идет обработка видео.",justify="left")
        self.button=ttk.Button(self,text="Вернуться в меню",command=self.button_click)

        self.button.pack_forget()
        self.label_text.pack_forget()
    def load_data(self,data):
        self.start_video(data)
        
    def error(self,id):
        text={
            2:"Ошибка при скачивании видео!",
            3:"Ошибка при обработке видео!",
            4:"Файла не существует!",
            5:"Указанная ссылка ведет на трансляцию!",
            6:"Выбранный интервал больше, чем видео!",
            7:"Непредвиденная ошибка!"
        }
        showerror(title="Ошибка", message=text[id])
        self.exit()
    def anim(self,state=0):
        self.label_text.pack(anchor="center")
        if self.fl_loading[0]==1:
            self.label_text.config(text="Обработка завершена.")
            self.button.pack(anchor="center",padx=15,pady=15)
        elif self.fl_loading[0]==0:
            try:
                if state==0:
                    self.label_text.config(text="Подождите, идет обработка видео..")
                    state+=1
                else:
                    self.label_text.config(text="Подождите, идет обработка видео...")
                    state-=1
            except:
                pass
            self.controller.after(500,self.anim,state)
        else:
            self.error(self.fl_loading[0])
            
    def start_video(self,data):
        self.fl_loading[0]=0
        self.controller.show_frame("VideoWindow")
        threading.Thread(target=view.start_video,args=(data.name,data.link,data.time,self.fl_loading),daemon=True).start()
        self.anim()
    def button_click(self):
        self.exit()
    def exit(self):
        self.button.pack_forget()
        self.label_text.pack_forget()
        self.fl_loading[0]=0
        self.controller.frames["MainWindow"].update_window()
        self.controller.show_frame("MainWindow")
        