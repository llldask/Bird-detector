import threading
import time
import processing_model
import video
import os
import datetime
from time import monotonic
import file_manager

class system_name:
    main_path=""
    output_dir=main_path+"output"
    download_video_dir=main_path+"video"
    ext_image=".jpg"
    ext_video=".mp4"
    download_video_name="video"





"""

def processing_video(output_path, interval_list):
    for i in range (len(interval_list)):
        processing_model.get_predict_and_save(output_path+'/'+str(i)+system_name.ext_image,str(datetime.timedelta(seconds=interval_list[i][1])))



def menu(num_thread):
        system_name.manager_thread[num_thread]=True
        while True: 
            try:
                output_path=file_manager.get_name_project(system_name.output_dir)
            except FileExistsError:
                print ("Папка уже существует")
            except:
                print ("Непредвиденная ошибка")
            else:
                break

        print("Введите режим")
        r_input_user=int(input())
        if r_input_user==0:#трансляция
            url_input_user="https://www.youtube.com/watch?v=c2SXDkaNOU4"
            try:
                url_translation=video.get_url(url_input_user)
            except:
                print("Неверный url")
            time_user_input=30
            threading.Thread(target=processing_stream,args=(output_path,time_user_input,url_translation,num_thread)).start()
        elif r_input_user==1:#скачать видео и разрезать
            video_path=system_name.download_video_dir+"/"+system_name.download_video_name+system_name.ext_video
            url_input_user_d="https://www.youtube.com/watch?v=YlKUDj3P2x0"
            time_user_input=5
            try:
                video.download_video(video_path,url_input_user_d)
            except:
                print("Неверный url")
            interval_list=video.save_frame_from_video(system_name.download_video_dir+'/'+system_name.download_video_name+system_name.ext_video,time_user_input,output_path,system_name.ext_image)
            processing_video(output_path,interval_list)
            file_manager.remove(system_name.download_video_dir+"/"+system_name.download_video_name+system_name.ext_video)
        elif r_input_user==2:#разезать видео пользователя
            path_to_video_user="6.mp4"
            time_user_input=5
            try:
                interval_list=video.save_frame_from_video(path_to_video_user,time_user_input,output_path,system_name.ext_image)
            except:
                print("Видео не найдено")
            processing_video(output_path,interval_list)




initialization()



"""
"""

file_manager.system_dir(system_name.output_dir,system_name.download_video_dir)
print(threading.enumerate())
while True:
    i=int(input())
    if i>=1 and i<=3:
        menu(i-1)
    elif i>=4 and i<=6:
        system_name.manager_thread[i-4]=False
    elif i==11:
        print(threading.enumerate())
    else:
        print(threading.enumerate())
        exit()
"""