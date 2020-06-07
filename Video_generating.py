import multiprocessing

import cv2
import os
from os import listdir
from os.path import isfile, join
import concurrent.futures
import time
from moviepy.editor import VideoFileClip



def generate_timestamps(args):
    video_path = args[0]
    working_dir = args[1]
    face_size = args[2]

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    print('starting video')

    video480_dir =  os.path.dirname(os.path.realpath(video_path))
    video720_dir = os.path.dirname(os.path.realpath(video480_dir)) + '\\v720\\'

    times_dir = working_dir + '\\times\\'
    partitions_dir = working_dir + '\\partitions\\'

    cap = cv2.VideoCapture(video_path)
    count = 0
    first_face = True
    times = ""
    face = True
    new_face = False
    while 1:
        ret, img = cap.read()
        if ret :
            millis = cap.get(cv2.CAP_PROP_POS_MSEC)
            faces = face_cascade.detectMultiScale(img, 1.3, 10)
            millis = int(millis)
            if(face != new_face):
                #print(millis)
                times += str(millis) + '\n'
            face = new_face
            new_face = False
            for (x, y, w, h) in faces:
                if(first_face):
					pass
                    #width = w - 15
                    #height = h - 15
                    #face_size = min(width,height)
                    first_face = False
                    print(face_size)
                if(w >face_size and h>face_size):
                    new_face = True
        else:
            break

    cap.release()

    with open(times_dir + video_name+ "_test.txt", "w") as opened_file:
        opened_file.write(times)

    time_stamps_list = []
    with open(times_dir + video_name + "_test.txt", 'rb') as f:
        lines = [x.decode('utf8').strip() for x in f.readlines()]

    stamps = ""

    for x in range(1, len(lines)):
        z = float(lines[x]) - float(lines[x - 1])
        if (z < 240):
            lines[x] = "0"
            lines[x - 1] = "0"

    z = +1

    for x in range(1, len(lines)):
        if (lines[x] != "0"):
            s = float(lines[x]) / 1000
            s = s + z * 0.01
            z = z * -1
            s = round(s, 2)
            stamps += str(s) + "\n"

    with open(times_dir + video_name + "_out.txt", "w") as opened_file:
        opened_file.write(stamps)

    myvideo = VideoFileClip(video720_dir + video_name + '.mp4')

    with open(times_dir + video_name + "_out.txt", 'r') as f:
        lines = [x for x in f.readlines()]

    for x in range(0, len(lines), 2):
        new = myvideo.subclip(float(lines[x]), float(lines[x + 1]))
        new.write_videofile(partitions_dir+ video_name+ '_' +str(int(x / 2)) + '.mp4')

    print('Finished video')


if __name__ == "__main__":

    multiprocessing.freeze_support()
    part_name = input("Enter the part name: ")
    face_size = int(input("Enter the size of the face: "))

    working_dir = os.path.dirname(os.path.realpath(os.getcwd()))
    #working_dir = os.getcwd()

    video_dir = working_dir + '\\videos\\' + part_name + '\\v480\\'

    videos = [(video_dir+f,working_dir,face_size) for f in listdir(video_dir) if isfile(join(video_dir, f))]

    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(generate_timestamps, videos)

    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} second(s)')

    input("Press Enter to exit")
    '''
    generate_timestamps(videos[0])

    generate_timestamps(videos[0])
    D:\Abueideh\Testing
    os.path.splitext(f)[0]
    for s in videos:
        print(s)
    
    
    Downloading playlist
    '''