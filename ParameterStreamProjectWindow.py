from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
import view
import Data
class ParameterStreamProjectWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.position = {"padx":15, "pady":2, "anchor":"nw"}
        self.max_lenght_entry=70

        self.fl_entry_name=False
        self.fl_entry_path=False

        self.text_label_path=["Введите ссылку на трансляцию с youtube:"]
        self.hour_var=StringVar(value="0")
        self.minute_var=StringVar(value="0")
        self.second_var=StringVar(value="0")

        self.frame_name=Frame(self)
        self.entry_name = ttk.Entry(self.frame_name)
        self.label_entry_name_error=Label(self.frame_name, foreground="#B71C1C")
        self.frame_path=Frame(self)
        self.entry_path = ttk.Entry(self.frame_path)
        self.label_entry_path_error=Label(self.frame_path, foreground="#B71C1C",justify=LEFT)
        self.frame_time=Frame(self)
        self.spinbox_hour = ttk.Spinbox(self.frame_time,from_=0, to=24,state="readonly",textvariable=self.hour_var)
        self.spinbox_minute = ttk.Spinbox(self.frame_time,from_=0, to=60,state="readonly",textvariable=self.minute_var)
        self.spinbox_second = ttk.Spinbox(self.frame_time,from_=0, to=60,increment=10,state="readonly",textvariable=self.second_var)
        self.frame_button=Frame(self)
        self.button_clear = ttk.Button(self.frame_button,text="Очистить",command=self.clear)
        self.button_create = ttk.Button(self.frame_button,text="Создать",command= self.button_click_create_project)
        self.button_back = ttk.Button(self.frame_button,text="Назад",command=self.button_click_back)
        self.label_path = Label(self, text=self.text_label_path[0])

        label = Label(self, text="Введите название проекта:")
        label.pack(**self.position)
        self.frame_name.pack(fill=X,**self.position)
        self.entry_name.pack(fill=X)
        label = Label(self, text="Укажите источник:")
        label.pack(**self.position)
        self.label_path.pack(**self.position) 
        self.frame_path.pack(**self.position,fill=X)
        self.entry_path.pack(fill=X)
        label = Label(self, text="Укажите переодичность времени для снимка:")
        label.pack(**self.position)
        self.frame_time.pack(**self.position)
        self.spinbox_hour.pack(side=LEFT)
        label = Label(self.frame_time, text="ч        ")
        label.pack(side=LEFT)
        self.spinbox_minute.pack(side=LEFT)
        label = Label(self.frame_time, text="мин        ")
        label.pack(side=LEFT)
        self.spinbox_second.pack(side=LEFT)
        label = Label(self.frame_time, text="сек")
        label.pack(side=LEFT )
        self.frame_button.pack(side=BOTTOM,fill=X)
        self.button_clear.pack(padx=15,pady=20,side=LEFT)
        self.button_create.pack(padx=15,pady=20,side=RIGHT)
        self.button_back.pack(padx=15,pady=20,anchor=E)

        
        self.entry_name.bind("<FocusOut>",func=lambda event:self.focus_out_entry_name())
        self.entry_path.bind("<FocusOut>",func=lambda event:self.focus_out_entry_path())

    def clear(self):
        self.entry_name.delete(0,END)
        self.entry_path.delete(0,END)
        self.hour_var.set(0)
        self.minute_var.set(0)
        self.second_var.set(0)
        self.label_entry_name_error.pack_forget()
        self.label_entry_path_error.pack_forget()

    def button_click_back(self):
        self.clear()
        self.controller.frames["MainWindow"].update_window()
        self.controller.show_frame("MainWindow")
    def button_click_create_project(self):
        time_fl=not (self.hour_var.get()=="0" and self.minute_var.get()=="0" and self.second_var.get()=="0")
        if self.fl_entry_name==False or self.fl_entry_path==False or time_fl==False:
            showerror(title="Ошибка", message="Не все поля заполнены или заполнены неправильно!")
            return
        self.controller.frames["StreamWindow"].load_data(Data.Data(self.entry_name.get(),view.time_convert(self.hour_var.get(),self.minute_var.get(),self.second_var.get()),self.entry_path.get()))
        self.clear()
    def check_entry(self,label,entry_name,text):
        value=entry_name.get().strip()
        entry_name.delete(0,END)
        entry_name.insert(0,value)
        if  entry_name.get()=="":
            label.config(text=text)
            label.pack(anchor="nw")
            return True
        return False
    def focus_out_entry_name(self):
        text_label=["Имя проекта уже существует",'Имя проекта не должно содержать следующих знаков: \\/:*?"<>|',"Имя не указано","Имя слишком длинное"]
        if self.check_entry(self.label_entry_name_error,self.entry_name,text_label[2]):
            self.fl_entry_name=False
            return
        if len(self.entry_name.get())>self.max_lenght_entry:
            self.fl_entry_name=False
            self.label_entry_name_error.config(text=text_label[3])
            self.label_entry_name_error.pack(anchor="nw")
            return
        if not view.check_name_dir(self.entry_name.get()):
            self.fl_entry_name=False
            self.label_entry_name_error.config(text=text_label[1])
            self.label_entry_name_error.pack(anchor="nw")
            return
        if view.check_exists_project_dir(self.entry_name.get()):
            self.fl_entry_name=True
            self.label_entry_name_error.pack_forget()
        else:
           self.fl_entry_name=False
           self.label_entry_name_error.config(text=text_label[0])
           self.label_entry_name_error.pack(anchor="nw")
    def focus_out_entry_path(self):
        text_label=["Имя не указано","Ссылка указана неверно,\nВерный формат ссылки: https://www.youtube.com/watch?v=..."]
        if self.check_entry(self.label_entry_path_error,self.entry_path,text_label[0]):
            self.fl_entry_path=False
            return

        if not view.check_link(self.entry_path.get()):
            self.fl_entry_path=False
            self.label_entry_path_error.config(text=text_label[1])
            self.label_entry_path_error.pack(anchor="nw")
        else:
            self.fl_entry_path=True
            self.label_entry_path_error.pack_forget()     
       
