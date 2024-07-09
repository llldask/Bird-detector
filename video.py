import yt_dlp
import ffmpeg

class loggerOutputs:
    def error(msg):
        pass
    def warning(msg):
        pass
    def debug(msg):
        pass

def get_url(url):
    ydl_opts = {'forceurl': True, 'noprogress': True, 'verbose': False,'quiet': True, 'simulate': True, 'no_warnings':True,"logger": loggerOutputs}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        received_url=ydl.sanitize_info(info)['url']
    return received_url

def check_is_stream(url):
    ydl_opts = {'forceurl': True, 'noprogress': True, 'verbose': False,'quiet': True, 'simulate': True, 'no_warnings':True,"logger": loggerOutputs}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        live=ydl.sanitize_info(info)['is_live']
    return live

def check_time_video(url):
    ydl_opts = {'forceurl': True, 'noprogress': True, 'verbose': False,'quiet': True, 'simulate': True, 'no_warnings':True,"logger": loggerOutputs}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        s=ydl.sanitize_info(info)['duration']
    return s

def download_video(video_path,video_url):
    #path+'/'+video_name+".mp4"
    ydl_opts = {'outtmpl':video_path,'format_sort': ['ext'],'format': 'bv','noprogress': True, 'verbose': False,'quiet': True,'no_warnings':True,"logger": loggerOutputs}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_url)

def save_frame_from_stream(received_url,output_path):
    out, _ = (
        ffmpeg
        .input(received_url)
        .output(output_path, vframes=1,loglevel="quiet")
        .run(capture_stdout=True)
    )

def save_frame_from_video(input_path,time_interval,output_path,ext):
    probe = ffmpeg.probe(input_path)
    video_time = float(probe['streams'][0]['duration']) #секунды

    parts = (int)(video_time / time_interval)

    interval_list = [(i * time_interval, (i + 1) * time_interval) for i in range(parts)]
    i = 0
    for item in interval_list:
        (
            ffmpeg
            .input(input_path, ss=item[1])
            .output(output_path +'/'+ str(i) + ext, vframes=1,loglevel="quiet")
            .run()
        )
        i += 1
    return interval_list


