#coding:utf-8
import os
import sys
import time
import random
from mutagen.mp3 import MP3
import var_set
import shutil
import _thread

path = var_set.path
rtmp = var_set.rtmp
live_code = var_set.live_code
deviceType = var_set.deviceType

def get_v():
    if deviceType == "pi":
        return "h264_omx"
    elif deviceType == "vps":
        return "libx264"


while True:
    try:
        files = os.listdir(path+'/downloads')
        files.sort()
        for f in files:
            if((f.find('.mp3') != -1) and (f.find('.download') == -1)):
                print(path+'/downloads/'+f)
                seconds = 600
                bitrate = 0
                try:
                    audio = MP3(path+'/downloads/'+f)
                    seconds=audio.info.length
                    bitrate=audio.info.bitrate
                except Exception as e:
                    print(e)
                    bitrate = 99999999999

                print('mp3 long:'+convert_time(seconds))
                if((seconds > 600) | (bitrate > 400000)):
                    print('too long/too big,delete')
                else:
                    pic_files = os.listdir(path+'/default_pic')
                    pic_files.sort()
                    pic_ran = random.randint(0,len(pic_files)-1)



                    if os.path.isfile(path+'/downloads/'+f.replace(".mp3",'')+'.jpg'):
                        print('ffmpeg -threads 0 -re -loop 1 -r 2 -t '+str(int(seconds))+' -f image2 -i "'+path+'/Song_picture/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f.replace(".mp3",'')+'.jpg'+'[result]" -i "'+path+'/downloads/'+f+'" -map "[result]" -map 2,0 -pix_fmt yuv420p -preset ultrafast -maxrate '+var_set.maxbitrate+'k -acodec copy -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                        os.system('ffmpeg -threads 0 -re -loop 1 -r 2 -t '+str(int(seconds))+' -f image2 -i "'+path+'/Song_picture/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f.replace(".mp3",'')+'.jpg'+'[result]" -i "'+path+'/downloads/'+f+'" -map "[result]" -map 2,0 -pix_fmt yuv420p -preset ultrafast -maxrate '+var_set.maxbitrate+'k -acodec copy -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                break
    except Exception as e:
        print(e)

