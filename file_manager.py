import os
import re
import shutil
import re


def check_exists_project_dir(output_dir,name_input_user):
     output_path=output_dir+'/'+name_input_user
     if os.path.exists(output_path):
          return False
     return True

def check_exists_file(path):
     return os.path.isfile(path)

def check_name_dir(name):
     if re.search(r"[\\/:*?\"<>|]",name)==None:
          return True
     return False
def check_link(link):
     if re.fullmatch(r"https://www\.youtube\.com/watch\?v=[^\.]+",link):
          return True
     return False
def check_path(path):
     if re.fullmatch(r"[A-Z]:/([^:*?\"<>|\\/.]+/)*[^\:*?\"<>|\\/\.]+\.(mp4|avi|mkv|mov)",path):
          return True
     return False

def create_project_dir(output_dir,name_input_user):
            output_path=output_dir+'/'+name_input_user
            os.mkdir(output_path)
            return output_path



def default_name_project(output_dir):
    defaul_name="project"
    file_list = os.listdir(output_dir)
    num=1
    for f in file_list:
         if re.fullmatch("project\\d{1,4}", f)!=None:
              new_num=int(f.replace("project",""))
              if new_num>num:
                   num=new_num
    return defaul_name+str(num+1)


def system_dir(output_dir): 
    if not os.path.exists(output_dir):
         os.mkdir(output_dir)


def remove_project(path):
    shutil.rmtree(path)

def delete_everything_in_folder(folder_path):
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)

