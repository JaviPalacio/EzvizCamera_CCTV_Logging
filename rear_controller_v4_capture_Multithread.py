# Write your code here :-)
#https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
import cv2
import numpy as np
import time
import os
import psutil
import threading
import math

output = []



def find_oldest_file(folder):

    os.chdir(folder)
    files = os.listdir()
    oldest_file = []
    oldest_date = float('inf')
    for f in files:
        stat = os.stat(f)
        if stat.st_mtime< oldest_date:
            oldest_file=f
            oldest_date=stat.st_mtime

    return oldest_file

def get_remaining_disk_space(self):
    #'/media/pi/My Passport'
    
    total, used, free, percent = psutil.disk_usage(self)
    return percent


def write_frame(capture):
    #in1=cv2.VideoWriter(file_name, vid_cod, math.floor(counter/capture_time), (fwidth,fheight))
    
    global np
    print('write_frame thread...\n')
    
    
    #time.sleep(10)
    print('Start Writing................\n')
    FPS = 8
    #ret,frame = capture.read()
    #fshape = frame.shape
    fheight = 1080
    fwidth = 1920
    print('Dimensions...\n')
    print(fwidth , fheight)
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    folder_name= r'/media/pi/My Passport/rear_camera/'
    file_name =folder_name+'rear_camera_'+time.strftime("%b %d %Y %H:%M:%S", time.gmtime())+'.avi'
    output = cv2.VideoWriter(file_name, vid_cod, FPS, (fwidth,fheight))
    mem_threshold=95
    hdd_folder = '/media/pi/My Passport/rear_camera'
    folder = '/media/pi/My Passport/rear_camera'    
    num_frame = 0
    while True:
        if get_remaining_disk_space(hdd_folder)>mem_threshold:
            oldest_file = find_oldest_file(folder)
            if len(oldest_file)>0:
                os.remove(oldest_file)

        if len(np)>40:
            lo = len(np)
            print('length of np is...\n',len(np))



            for f in range(lo):
                output.write(np[f])
#                 print('type of np \n',type(np))
#                 
#                 print('type of np[f]\n',type(np[f]))
#                 
#                 print('shape np[f]\n ',np[f].shape)
                
                
                
                
                #input('Press Enter to continue... this is what was written\n')
                #print(np[f])
                num_frame = num_frame + 1
                #print('Write frame f...%i.\n'%f)


                if num_frame == 4000:
                    print('Weeeeee 50 frames\n ')
                    output.release()
                    file_name =folder_name+'rear_camera_'+time.strftime("%b %d %Y %H:%M:%S", time.gmtime())+'.avi'
                    output = cv2.VideoWriter(file_name, vid_cod, FPS, (fwidth,fheight))
                    print('Video Written...\n', file_name)
                    num_frame = 0
            print('Delete the written frames')        
            del np[0:lo]
        else:
            pass

def grab_video(capture):

    
    global np
    counter = 0
    counter_recap = 0
    counter_grabbed = 0
    counter_retrieved = 0
    #FPS = capture.ge
    print('Start Grab Video\n')
    while True:
        old_time=time.time()

        #print('New loop \n')
        capture_time = 20
        
            

        #time1=time.time()
        retval = capture.grab()


        if retval:
            counter_grabbed = counter_grabbed + 1
            retrieved,frame = capture.retrieve()
            #print('len(frame)......\n',len(frame))
            if retrieved:
                counter=counter+1
                #print('\n',ret)
                #time2=time.time()
                #output.write(frame)
                #print(type(frame))
                time.sleep(0.1)
                np.append(frame)
            else:
                #print('Frame not captured!!!!\n')
                capture = cv2.VideoCapture('rtsp://admin:CameraPass@CameraIP/1')
                counter_recap = counter_recap + 1 
                
        else:
            #print('Frame not captured!!!!\n')
            capture = cv2.VideoCapture('rtsp://admin:CameraPass@CameraIP/1')
            counter_recap = counter_recap + 1 
        #print('number of frames retrieved....\n', counter)

print(os.getcwd())


##capture = cv2.VideoCapture('rtsp://username:password@192.168.1.64/1')

attempts_limit = 100
current_attempts = 0

while current_attempts <attempts_limit:
    try:
        ##capture = cv2.VideoCapture('rtsp://username:password@192.168.1.64/1')


        capture = cv2.VideoCapture('rtsp://admin:CameraPass@CameraIP/1')
        ret,frame = capture.read()
        if ret:
                break


    except:
        current_attempts=current_attempts+1
        time.sleep(5)   

#output = cv2.VideoWriter("videos/cam_video.mp4")
print('capture***************\n')

ret,frame = capture.read()
fshape = frame.shape
fheight = fshape[0]
fwidth = fshape[1]
print('Dimensions...\n')
print(fwidth , fheight)
vid_cod = cv2.VideoWriter_fourcc(*'XVID')
folder_name= r'/media/pi/My Passport/rear_camera/'
#folder_name= '/home/pi/Desktop/CodeTesting/VIDEOS'
file_name =folder_name+'rear_camera_'+time.strftime("%b_%d_%Y_%H_%M_%S", time.gmtime())+'.avi'

original_time = time.time()

#capture = cv2.VideoCapture('rtsp://admin:CameraPass@CameraIP/1')






np = []        
    #output = cv2.VideoWriter(file_name, vid_cod, math.floor(counter/capture_time), (fwidth,fheight)),
firstThread = threading.Thread(target=grab_video, args=(capture,))

print('Start first thread...\n')
firstThread.start()

secondThread = threading.Thread(target=write_frame, args=(capture,))
print('Start second thread...\n')
secondThread.start()

    
#     print('CounterRetrieved... FPS..recaptured...grabbed...\n',counter,FPS,counter_recap,counter_grabbed)
#     time_before_writing = time.time()
# #     for f in np:
# #         output.write(f)
#     np=[]
#     time_after_writing_clearing = time.time()
#     print('Writing time is...\n',time_after_writing_clearing - time_before_writing)
    #output.release()
    
#capture.release()
#cv2.destroyAllWindows()
