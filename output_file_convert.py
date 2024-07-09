from yattag import Doc
import os
import json
import shutil

class bird_name:
    group={
        0:"Accipitriformes",
        1:"Columbiformes",
        2:"Passeriformes",
        3:"Psittaciformes",
        4:"Struthioniformes"
    }
    name={
        0:{
            0:"BALD EAGLE",
            1:"GOLDEN EAGLE",
            2:"OSPREY",
            3:"PEREGRINE FALCON"
        },

        2:{
            0:"COMMON GRACKLE",
            1:"HOUSE FINCH",
            2:"HOUSE SPARROW",
            3:"NORTHERN CARDINAL"
        }
    }

def read_json(path_to_file):
    with open(path_to_file, "r") as fh:
        b=json.load(fh)
    return b

def create_html(name_project):
    num_file=0
    doc, tag, text = Doc().tagtext()
    with tag('html'):
                with tag('head'):
                    with tag('title'):
                        text(name_project)
                    with tag('style',type="text/css"):
                        doc.asis("TABLE {width: 300px;border-collapse: collapse;}TD, TH {padding: 3px;border: 1px solid black;}")
                    with tag('table'):
                        with tag('tr'):
                            with tag('th'):
                                text("Дата")
                            with tag('th'):
                                text("Отряд")
                            with tag('th'):
                                text("Название")
                        while True:
                            path_to_file=name_project+"/"+str(num_file)+".json"
                            if os.path.isfile(path_to_file):
                                f=read_json(path_to_file)
                                with tag('tr'):
                                    with tag('td'):
                                        text(f["Date"])
                                    with tag('td'):    
                                            text("")
                                    with tag('td'):    
                                            text("")
                                for item in f["Birds"]:
                                    if len(item["group"])==1:
                                        with tag('tr'):
                                            with tag('td'):
                                                text("")
                                            with tag('td'):
                                                t=int(list(item["group"].keys())[0])
                                                p=list(item["group"].values())[0]
                                                text(bird_name.group[t]+" "+str(p))
                                            if len(item["name"])!=0:
                                                with tag('td'):
                                                    t1=int(list(item["name"].keys())[0])
                                                    p1=list(item["name"].values())[0]
                                                    text(bird_name.name[t][int(t1)]+" "+str(p1))
                                            else:
                                                with tag('td'):
                                                    text("")
                                        for n in range(1,len(list(item["name"].keys()))):
                                            with tag('tr'):
                                                with tag('td'):
                                                    text("")
                                                with tag('td'):
                                                    text("")
                                                with tag('td'):
                                                    t1=int(list(item["name"].keys())[n])
                                                    p1=list(item["name"].values())[n]
                                                    text(bird_name.name[t][int(t1)]+" "+str(p1))   
                                    else:
                                        for key, value in item["group"].items():
                                            with tag('tr'):
                                                with tag('td'):
                                                    text("")
                                                with tag('td'):
                                                    text(bird_name.group[int(key)]+" "+str(value))  
                                                with tag('td'):
                                                    text("")             
                                    with tag('tr'): 
                                        with tag('td'):    
                                            text("")  
                                        with tag('td'):    
                                            text("")
                                        with tag('td'):    
                                            text("")     
                                        
                                num_file+=1
                            else:
                                break
    return doc.getvalue()
def create_html_with_image(name_project):
    num_file=0
    doc, tag, text = Doc().tagtext()
    with tag('html'):
                with tag('head'):
                    with tag('title'):
                        text(name_project)
                    with tag('style',type="text/css"):
                        doc.asis("TABLE {width: 300px;border-collapse: collapse;}TD, TH {padding: 3px;border: 1px solid black;}TD >IMG {width: 100px;height: 100px;}")
                    with tag('table'):
                        with tag('tr'):
                            with tag('th'):
                                text("Дата")
                            with tag('th'):
                                text("Отряд")
                            with tag('th'):
                                text("Название")
                            with tag('th'):
                                text("Фото")
                        while True:
                            path_to_file=name_project+"/"+str(num_file)+".json"
                            if os.path.isfile(path_to_file):
                                f=read_json(path_to_file)
                                with tag('tr'):
                                    with tag('td'):
                                        text(f["Date"])
                                    with tag('td'):    
                                            text("")
                                    with tag('td'):    
                                            text("")
                                    with tag('td'):
                                        ph=f["Path"][f["Path"].find("/") + 1 : ]
                                        with tag('image',src=ph):
                                            text("")
                                        with tag("p"):
                                            with tag("a",href=ph):
                                                text("Открыть фото")
                                for item in f["Birds"]:
                                    if len(item["group"])==1:
                                        with tag('tr'):
                                            with tag('td'):
                                                text("")
                                            with tag('td'):
                                                t=int(list(item["group"].keys())[0])
                                                p=list(item["group"].values())[0]
                                                text(bird_name.group[t]+" "+str(p))
                                            if len(item["name"])!=0:
                                                with tag('td'):
                                                    t1=int(list(item["name"].keys())[0])
                                                    p1=list(item["name"].values())[0]
                                                    text(bird_name.name[t][int(t1)]+" "+str(p1))
                                            else:
                                                with tag('td'):
                                                    text("")
                                            with tag('td'):
                                                ph_birdy=item["path"][item["path"].find("/") + 1 : ]
                                                with tag('image',src= ph_birdy):
                                                    text("")
                                                with tag("p"):
                                                    with tag("a",href= ph_birdy):
                                                        text("Открыть фото")
                                        for n in range(1,len(list(item["name"].keys()))):
                                            with tag('tr'):
                                                with tag('td'):
                                                    text("")
                                                with tag('td'):
                                                    text("")
                                                with tag('td'):
                                                    t1=int(list(item["name"].keys())[n])
                                                    p1=list(item["name"].values())[n]
                                                    text(bird_name.name[t][int(t1)]+" "+str(p1))   
                                                with tag('td'):
                                                    text("")
                                    else:
                                        fl=0
                                        for key, value in item["group"].items():
                                            with tag('tr'):
                                                with tag('td'):
                                                    text("")
                                                with tag('td'):
                                                    text(bird_name.group[int(key)]+" "+str(value))  
                                                with tag('td'):
                                                    text("")    
                                                if fl==0:
                                                    with tag('td'):
                                                        ph_birdy=item["path"][item["path"].find("/") + 1 : ]
                                                        with tag('image',src= ph_birdy):
                                                            text("")
                                                        with tag("p"):
                                                            with tag("a",href= ph_birdy):
                                                                text("Открыть фото")
                                                    fl+=1
                                                else:
                                                    with tag('td'):
                                                        text("") 
                                                 
                                    with tag('tr'): 
                                        with tag('td'):    
                                            text("")  
                                        with tag('td'):    
                                            text("")
                                        with tag('td'):    
                                            text("") 
                                        with tag('td'):    
                                            text("")     
                                        
                                num_file+=1
                            else:
                                break
    return doc.getvalue()
def save_html(name_project,out):
    r=create_html(name_project)
    with open(out, 'w') as f:
        f.write(r)
def save_html_with_image(name_project,out,exp):
    r=create_html_with_image(name_project)
    print(out)
    with open(out, 'w') as f:
        f.write(r)
    dir_name=out[:out.rfind("/")+1]+name_project[name_project.rfind("/")+1:]

    print(dir_name)
    os.mkdir(dir_name)
    copy_image(name_project,dir_name,exp)
    
def copy_image(name_project,out,exp):
    file_list = os.listdir
    for f in file_list(name_project):
        file_name=os.path.splitext(f)
        if file_name[1]==exp:
            shutil.copy2(name_project+'/'+f,out+'/'+f)
        elif os.path.isdir(name_project+'/'+f):
            os.mkdir(out+'/'+f)
            copy_image(name_project+'/'+f,out+'/'+f,exp)
    
