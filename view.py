import os
import system_name as s
import file_manager
import output_file_convert
import stream_video_manager
import video
import MyException
import time as t


def get_project_name():
    file_list = os.listdir(s.system_name.output_dir)
    result_list=[]
    for f in file_list:
        if os.path.isdir(s.system_name.output_dir+'/'+f):
            result_list.append(f)
    return result_list

def remove_project(name):
    file_manager.remove_project(s.system_name.output_dir+"/"+name)
def create_report(name,output):
    output_file_convert.save_html(s.system_name.output_dir+"/"+name,output)

def create_image_report(name,output):
    """
    out=output+"/"+"image_report_"+name+".html"
    if os.path.isfile(out) and fl==0:
        raise MyException.FileExist()
    output_file_convert.save_html_with_image(s.system_name.output_dir+"/"+name,out)
    return os.path.abspath(out)
    """
    output_file_convert.save_html_with_image(s.system_name.output_dir+"/"+name,output,s.system_name.ext_image)

def check_exists_project_dir(name):
    return file_manager.check_exists_project_dir(s.system_name.output_dir,name)
def check_name_dir(name):
    return file_manager.check_name_dir(name)
def check_link(link):
    return file_manager.check_link(link)
def check_path(path):
    return file_manager.check_path(path)
def create_project_dir(name):
    file_manager.create_project_dir(s.system_name.output_dir,name)
def time_convert(h,m,s):
    res=int(h)*3600+int(m)*60+int(s)
    return(res)


def get_url_stream(url): 
    return video.get_url_stream(url)
def check_is_stream(url):
    return video.check_is_stream(url)
def check_time_video(url):
    return video.check_time_video(url)

def start_stream(name,url,time,id,tm,fl):
    try:
        if not check_is_stream(url):
            fl[0]=2
            return
        url=video.get_url(url)
        out=file_manager.create_project_dir(s.system_name.output_dir,name)
        tm.start(id)
        fl[0]=1
    except:
        fl[0]=3
        return
    stream_video_manager.start_stream(out,url,time,id,s.system_name.ext_image,tm)
def stop_stream(tm,id):
    tm.stop(id)

def delete_video_folder():
    file_manager.delete_everything_in_folder(s.system_name.download_video_dir)

def start_video(name,path,time,fl_load):
    try:
        fl=False
        if file_manager.check_link(path):
            dp=s.system_name.download_video_dir+"/"+s.system_name.download_video_name+s.system_name.ext_video
            if check_is_stream(path):
                fl_load[0]=5
                return
            if check_time_video(path) < time:
                fl_load[0]=6
                return
            try:
                video.download_video(dp,path)
            except:
                print("не скачалось")
                delete_video_folder()
                remove_project(name)
                fl_load[0]=2
                return
            path=dp
            fl=True
        else:
            if not file_manager.check_exists_file(path):
                fl_load[0]=4
                return
        try:
            out=file_manager.create_project_dir(s.system_name.output_dir,name)
            interval_list=video.save_frame_from_video(path,time,out,s.system_name.ext_image)
            stream_video_manager.processing_video(out,interval_list,s.system_name.ext_image)
        except:
            delete_video_folder()
            remove_project(name)
            fl_load[0]=3
            print("не обработалось")
            return
        if fl:
            delete_video_folder()
        fl_load[0]=1
    except:
        fl_load[0]=7
    

def initialization():
    file_manager.system_dir(s.system_name.output_dir)
    delete_video_folder()

    

