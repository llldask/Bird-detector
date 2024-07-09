from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.messagebox import showinfo,showerror, askyesno
import view
import Data
import Thread_Manager
import datetime
import threading



class StreamWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.frame_name_id={}
        self.tm=Thread_Manager.thread_manager()
        self.fl_loading=[0]

        self.frame_for_button=Frame(self)
        self.button_start_stream = ttk.Button(self.frame_for_button,text="Запустить обработку еще одной трансляции",command=self.button_click_start_stream)
        self.button_back = ttk.Button(self.frame_for_button,text="Вернуться в меню",command=self.button_click_back)


        self.frame_for_button.pack(fill=X,side=BOTTOM,pady=30,padx=15)
        self.button_start_stream.pack(ipadx=10,side=RIGHT)
        self.button_back.pack(ipadx=10,side=LEFT)

    def load_data(self,data):
        self.start_stream(data)
    def error(self,id,num):
        text={
            2: "Видео не является прямой трансляцией!",
            3: "Непредвиденная ошибка!"
        }
        showerror(title="Ошибка", message=text[num])
        self.frame_name_id[id].delete_self()
    def anim(self,id,state=0):
        if self.fl_loading[0]==1:
            self.stream_continue(id)
        elif self.fl_loading[0]==0:
            try:
                if state==0:
                    self.frame_name_id[id].label.config(text=" ..")
                    state+=1
                else:
                    self.frame_name_id[id].label.config(text=".. ")
                    state-=1
            except:
                pass
            self.controller.after(500,self.anim,id,state)
        else:
            self.error(id,self.fl_loading[0])
    
    def start_stream(self,data):
        self.fl_loading[0]=0
        id=self.add_nameFrame()
        nm=NameFrame(self,data.name,id,data.link,data.time)
        nm.pack(anchor="nw",padx=15,pady=20,fill=X)
        self.frame_name_id[id]=nm
        self.controller.show_frame("StreamWindow")
        threading.Thread(target=view.start_stream,args=(data.name,data.link,data.time,id,self.tm,self.fl_loading),daemon=True).start()
        self.anim(id)  
    def stream_continue(self,id):
        if(len(self.frame_name_id)==1):
            threading.Thread(target= self.update_time,daemon=True).start()
        self.frame_name_id[id].start_time()
        self.fl_loading[0]=1
    def add_nameFrame(self):
        if len(self.frame_name_id)==0:
            return 0
        else:
            for i in range(3):
                if i not in self.frame_name_id.keys():
                    return i
    def delete_nameFrame(self,id):
         view.stop_stream(self.tm,id)
         self.frame_name_id.pop(id)
    def clear(self):
        for key,value in  list(self.frame_name_id.items()):
            view.stop_stream(self.tm,key)
            value.delete_self()
        self.frame_name_id.clear()
    def finish(self):
        result = askyesno(title="Подтвержение операции", message="Вы действительно хотите вернуться на главный экран? Все обработки трансляций будут остановлены.")
        if result: 
            self.clear()
            self.destroy()
    def update_time(self):
        if (len(self.frame_name_id)==0):
            return
        try:
            for item in self.frame_name_id.values():
                if item.fl_start:
                    t=datetime.datetime.now()-item.start_time
                    item.label.config(text=datetime.timedelta(seconds=int(t.total_seconds())))
        except:
            pass
        
        self.controller.after(1000,self.update_time)
    def button_click_start_stream(self):
        if self.fl_loading[0]==0:
            showinfo(title="Информация", message="Подождите, идет подготовка.")
            return
        if len(self.frame_name_id)==3:
            showinfo(title="Информация", message="Возможно обрабатывть только 3 трансляции одновременно.")
            return
        self.controller.show_frame("ParameterStreamProjectWindow")
    def button_click_back(self):
        result = askyesno(title="Подтвержение операции", message="Вы действительно хотите вернуться в меню? Все обработки трансляций будут остановлены.")
        if result: 
            self.clear()
            self.controller.frames["MainWindow"].update_window()
            self.controller.show_frame("MainWindow")

   
                
class NameFrame(Frame):
    def __init__(self, parent,name,num,link,t):
        Frame.__init__(self, parent)
        self.parent=parent
        self.config(borderwidth=1,relief=SOLID)

        self.fl_start=False
        self.num=num

        label = Label(self,text= name)
        label.pack(side=LEFT,pady=10,padx=10)

        self.label = Label(self,text="00:00:00")
        button_stop = ttk.Button(self,text="Остановить",command=self.delete_self)
        button_info = ttk.Button(self,text="Показать информацию",command=lambda: self.button_click_info(name,link,t))

        button_stop.pack(side=RIGHT,pady=10,padx=10)
        button_info.pack(side=RIGHT,pady=10,padx=10)
        self.label.pack(side=RIGHT,pady=10,padx=10)
    
    def delete_self(self):
        self.parent.delete_nameFrame(self.num)
        self.fl=False
        self.destroy()
    def create_label(self,w,text):
        label=Label(w, text=text)
        label.pack(anchor="sw",padx=15)
    def create_entry(self,w,text):
        entry=ttk.Entry(w)
        entry.insert(0,text)
        entry.config(state="readonly")
        entry.pack(anchor="sw",fill=X,padx=15)
    def close_info_window(self,window):
        self.parent.controller.windows_list.remove(window)
        window.destroy()
    def button_click_info(self,name,link,t):
        window = Tk()
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_info_window(window))
        self.parent.controller.windows_list.append(window)
        window.title("Информация")
        w = self.parent.controller.winfo_x()
        h = self.parent.controller.winfo_y()
        window.geometry(f'700x300+{w}+{h}')
        self.create_label(window,"Имя:")
        self.create_entry(window,name)
        self.create_label(window,"Ссылка:")
        self.create_entry(window,link)
        self.create_label(window,"Временной интервал:")
        self.create_entry(window,t)
    def start_time(self):
        self.start_time = datetime.datetime.now()
        self.fl_start=True
   





