print('importing cv2...')
import cv2
import sys
import main
import time
import os
import threading
from mpg123 import Mpg123, Out123

if len(sys.argv) < 3:
    print('weird use')
    print('correct use: python3 video.py VIDEO_FILE.mp4 SLEEP_FRAMES')
    sys.exit()

print('getting video')
vidcap = cv2.VideoCapture(sys.argv[1])
totalFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

print('rendering audio...')
os.system('rm image_data/audio.mp3')
os.system(f'ffmpeg -i {sys.argv[1]} -vn -acodec libmp3lame -ac 2 -ab 160k -ar 48000 image_data/audio.mp3')

def audioThread():
    global startTime
    global done
    mp3 = Mpg123('image_data/audio.mp3')
    out = Out123()
    for frame in mp3.iter_frames(out.start):
        if not done:
            startTime = time.time()
            done = True
        out.play(frame)

done = False
threading.Thread(target=audioThread).start()
while not done:
    pass

def getMethod(x, y):
    width, height, _ = image.shape
    # why is it in BGR
    return image[round(y*width), round(x*height)][::-1]

startTime = time.time()
lastFrameIndex = 0
framerate = vidcap.get(cv2.CAP_PROP_FPS)
while True:
    newFrameIndex = round((time.time() - startTime) * framerate)
    if newFrameIndex >= totalFrames: break
    if lastFrameIndex == newFrameIndex: continue

    lastFrameIndex = newFrameIndex
    vidcap.set(1, newFrameIndex)
    success, image = vidcap.read()
    if not success: continue; print(f'problem reading frame{newFrameIndex}')

    print('\033[H'+main.renderFromGetMethod(getMethod))
    time.sleep(1/framerate * float(sys.argv[2]))
