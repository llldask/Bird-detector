from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo,showerror, askyesno
from tkinter import filedialog
import view


class MainWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.button_position={"padx":10, "pady":5, "anchor":"w","side":"left"}

        list_name=view.get_project_name()
        self.list_name_v=self.list_to_variable(list_name)

        self.frame_to_button=Frame(self,height=35)
        self.button_delete = ttk.Button(self.frame_to_button,text="Удалить",command=self.button_click_delete)
        self.button_create_report = ttk.Button(self.frame_to_button,text="Создать отчет",command= self.button_click_create_report)
        self.button_create_report_image = ttk.Button(self.frame_to_button,text="Создать отчет с фото",command= self.button_click_create_image_report)
        self.frame_to_listbox=Frame(self)
        self.scroll=Scrollbar(self.frame_to_listbox,orient=VERTICAL,relief=FLAT)
        self.listbox_project_name = Listbox(self.frame_to_listbox,listvariable=self.list_name_v,selectmode=EXTENDED,yscrollcommand=self.scroll.set,relief=GROOVE)
        self.button_new_project = ttk.Button(self,text="Создать новый проект",command=lambda: controller.show_frame("ParameterNewProjectWindow"))

        self.scroll.config(command=self.listbox_project_name.yview)
        self.listbox_project_name.bind("<<ListboxSelect>>",func=lambda event:self.selected_listbox())

        self.frame_to_button.pack(fill=X)
        self.button_delete.pack_forget()
        self.button_create_report.pack_forget()
        self.button_create_report_image.pack_forget()
        self.scroll.pack(side=RIGHT,fill=Y)
        self.frame_to_listbox.pack(fill=X,pady=10,padx=10)
        self.listbox_project_name.pack(fill=BOTH)
        self.listbox_project_name.pack(fill=BOTH)
        self.button_new_project.pack(padx=10,pady=5)
        
    def update_window(self):
        list_name=view.get_project_name()
        print(list_name)
        self.list_name_v=self.list_to_variable(list_name)
        self.listbox_project_name.config(listvariable=self.list_name_v)
    def list_to_variable(self,list_name):
        return Variable(value=list_name)
    def selected_listbox(self):
        selected_indices =self.listbox_project_name.curselection()
        if len(selected_indices)>1:
            self.button_create_report.pack_forget()
            self.button_create_report_image.pack_forget()
        elif len(selected_indices)==1:
            self.button_delete.pack(**self.button_position)
            self.button_create_report.pack(**self.button_position)
            self.button_create_report_image.pack(**self.button_position)
        else:
            self.button_delete.pack_forget()
            self.button_create_report.pack_forget()
            self.button_create_report_image.pack_forget()

    def button_click_delete(self):
        result = askyesno(title="Подтвержение операции", message="Действительно хотите удалить?")
        if result: 
            selected_indices =self.listbox_project_name.curselection()
            selected_indices_reverse=list(selected_indices)
            selected_indices_reverse.reverse()
            for i in selected_indices_reverse:
                name=self.listbox_project_name.get(i)
                view.remove_project(name)
                self.listbox_project_name.delete(i)
            self.button_delete.pack_forget()
    def button_click_create_report(self):
        output_path=filedialog.asksaveasfilename(defaultextension=".*",filetypes = (("HTML files",".html"),))
        if output_path !="":
            selected_indices =self.listbox_project_name.curselection()
            name=self.listbox_project_name.get( selected_indices[0])
            try:
                view.create_report(name,output_path)
            except:
                showerror(title="Ошибка", message="Ошибка при сохранении файла!")
                return
            showinfo(title="Информация", message="Файл успешно сохранен!")

    def button_click_create_image_report(self):
        output_path=filedialog.asksaveasfilename(defaultextension=".*",filetypes = (("HTML files",".html"),))
        if output_path !="":
            selected_indices =self.listbox_project_name.curselection()
            name=self.listbox_project_name.get( selected_indices[0])
            try:
                view.create_image_report(name,output_path)
            except:
                showerror(title="Ошибка", message="Ошибка при сохранении файла!")
                return
            showinfo(title="Информация", message="Файл успешно сохранен! В директории с файлом была создана папка с фотографиями, ее название совпадает с названием проекта.")

