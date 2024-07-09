from ultralytics import YOLO
from PIL import Image
import os
detect_model=YOLO('model/detect.pt')
classif_group_model=YOLO('model/cls-main-general.pt')
classif_Acc_model=YOLO('model/cls-Acc-general.pt')
classif_Pas_model=YOLO('model/cls-Pas-general.pt')
classif_Pas_gray_model=YOLO('model/cls-Pas-gray.pt')
wb_model=YOLO('model/gray-color1.pt')

class bird:
    group_bird={
        0:"Accipitriformes",
        1:"Columbiformes",
        2:"Passeriformes",
        3:"Psittaciformes",
        4:"Struthioniformes"
    }
    name_Acc={
        0:"BALD EAGLE",
        1:"GOLDEN EAGLE",
        2:"OSPREY",
        3:"PEREGRINE FALCON"
    }
    name_Pas={
        0:"COMMON GRACKLE",
        1:"HOUSE FINCH",
        2:"HOUSE SPARROW",
        3:"NORTHERN CARDINAL"
    }
    def __init__(self):
        self.group={}
        self.name={}
        self.path=""
    def print_bird(self):
        print(self.path)
        for key, value in self.group.items():
                 print(self.group_bird[key],key," perc=", value)
        if len(self.group)==1:
            if(list(self.group.keys())[0]==0):
                for key, value in self.name.items():
                     print(self.name_Acc[key],key," perc=", value)
            elif(list(self.group.keys())[0]==2):
                for key, value in self.name.items():
                     print(self.name_Pas[key],key," perc=", value)
        print()
coef_dif=0.09
count=2
def add_name_bird(b,result):
    for r in result:
        first_p=round(float(r.probs.top5conf[0]),2)
        b.name[int(r.probs.top5[0])]=first_p
        for i in range(1,count+1):
            if first_p - round(float(r.probs.top5conf[i]),2)<coef_dif:
                first_p=round(float(r.probs.top5conf[i]),2)
                b.name[int(r.probs.top5[i])]=first_p
            else:
                break
coef_dif_gr=0.09
coef_suff=0.7
count_gr=2
def add_group_bird(b,result):
    for r in result:
        first_p=round(float(r.probs.top1conf),2)
        b.group[int(r.probs.top1)]=first_p
        if first_p >=coef_suff:
            return True
        else:
            for i in range(1,count_gr+1):
                if first_p - round(float(r.probs.top5conf[i]),2)<coef_dif_gr:
                    first_p=round(float(r.probs.top5conf[i]),2)
                    b.group[int(r.probs.top5[i])]=first_p
                else:
                    break
            return False
def detect_bird(path_to_main_photo,path_to_dir):
    path=path_to_main_photo
    output=path_to_dir
    result=detect_model(source=path,show=False,conf=0.4,save=False,verbose=False)
    c=0
    for r in result:
        boxes=r.boxes.xyxy.tolist()
    for b in boxes:
        im = Image.open(path)
        im = im.convert('RGB')
        im.crop((b[0], b[1], b[2], b[3])).save(output+"/"+str(c)+".jpg")
        c+=1
def classify_bird(path_to_main_photo,path_to_dir):
    path=path_to_main_photo
    output=path_to_dir
    file_list = os.listdir(output)
    birds=[]
    for f in file_list:
        ex=os.path.splitext(f)
        if ex[1]==".jpg":
            p=output+'/'+f
            birdy=bird()
            birdy.path=output+'/'+f
            result=classif_group_model(source=p,show=False,conf=0.4,save=False,verbose=False)
            fl_group=add_group_bird(birdy,result)
            if(fl_group==True):
                if(list(birdy.group.keys())[0]==0):
                    result=classif_Acc_model(source=p,show=False,conf=0.4,save=False,verbose=False)
                    add_name_bird(birdy,result)
                elif(list(birdy.group.keys())[0]==2):
                    result=wb_model(source=p,show=False,conf=0.4,save=False,verbose=False)
                    for r in result:
                        if r.probs.top1==0:
                            result=classif_Pas_model(source=p,show=False,conf=0.4,save=False,verbose=False)
                            add_name_bird(birdy,result)
                        else:
                            result=classif_Pas_gray_model(source=p,show=False,conf=0.4,save=False,verbose=False )
                            add_name_bird(birdy,result)
            birds.append(birdy)
    return birds




