import system_name
import threading
import time
import processing_model
import video
import os
import datetime
from time import monotonic
import file_manager
import MyException





def processing_stream(output_path, tSleep, url, num_thread,ext_image,tm):
    try:
        num_frame=0
        t = monotonic()
        while tm.thread_list[num_thread]==True:
            if monotonic() - t > tSleep or num_frame==0:
                video.save_frame_from_stream(url,output_path+'/'+str(num_frame)+ext_image)
                current_time = datetime.datetime.now()
                processing_model.get_predict_and_save(output_path+'/'+str(num_frame)+ext_image, current_time.strftime("%d.%m.%Y %H:%M:%S"))
                num_frame+=1
                t = monotonic()
            time.sleep(0.1)
    except:
        pass



def start_stream(output_path,url_translation,time_user_input,num_thread,ext_image,tm):
    tm.start(num_thread)
    threading.Thread(target=processing_stream,args=(output_path,time_user_input,url_translation,num_thread,ext_image,tm),daemon=True).start()






def processing_video(output_path, interval_list,ext_image):
    for i in range (len(interval_list)):
        processing_model.get_predict_and_save(output_path+'/'+str(i)+ext_image,str(datetime.timedelta(seconds=interval_list[i][1])))
