import model
import os
import json

def bird_to_dict(bird):
    d={}
    d["group"]=bird.group
    d["name"]=bird.name
    d["path"]=bird.path
    return d
def get_predict_and_save(path_to_main_photo,date_time):
    dir_name=path_to_main_photo.split(".")
    os.mkdir(dir_name[0])
    model.detect_bird(path_to_main_photo,dir_name[0])
    birds=model.classify_bird(path_to_main_photo,dir_name[0])
    b_json=[]
    for b in birds:
        b_json.append(bird_to_dict(b))
    d={"Date":date_time,"Path":path_to_main_photo,"Birds":b_json}
    with open(dir_name[0]+".json", "a+") as fh:
        json.dump(d, fh)

    
