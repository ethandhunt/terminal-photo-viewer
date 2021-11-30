print('importing cv2...')
import cv2
import sys
import main
import time
import os
import threading

if len(sys.argv) < 3:
    print('weird use')
    print('correct use: python3 video.py VIDEO_FILE.mp4 SLEEP_FRAMES')
    sys.exit()

vidcap = cv2.VideoCapture(sys.argv[1])
count = 0
totalFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
lastUpdateTime = time.time()
updateInterval = 0.1
print('Getting video frames...')
while True:
    if time.time() - lastUpdateTime > updateInterval:
        print(f'\033[100D{count}/{totalFrames}', end='', flush=True)
        lastUpdateTime = time.time()
    success, image = vidcap.read()
    if not success:
        break
    cv2.imwrite(f'image_data/frame_{count}.jpg', image)
    count += 1

print('\033[100Ddone        \nrendering frames...')
renderedFrames = []
nextFrameUpdate = 0
lastUpdateTime = time.time()
for i in range(count):
    renderedFrames.append(main.render(f'image_data/frame_{i}.jpg'))
    if time.time() - lastUpdateTime > updateInterval:
        print(f'\033[100D{i}/{totalFrames}', end='', flush=True)
        lastUpdateTime = time.time()

print('\033[100Ddone        \nrendering audio...')
os.system('rm image_data/audio.mp3')
os.system(f'ffmpeg -i {sys.argv[1]} -vn -acodec libmp3lame -ac 2 -ab 160k -ar 48000 image_data/audio.mp3')

def audioThread():
    os.system('mpg123 image_data/audio.mp3')

startTime = time.time()
threading.Thread(target=audioThread).start()
lastFrameIndex = 0
framerate = vidcap.get(cv2.CAP_PROP_FPS)
while True:
    newFrameIndex = round((time.time() - startTime) * framerate)
    if lastFrameIndex == newFrameIndex: continue
    lastFrameIndex = newFrameIndex
    print('\033[H'+renderedFrames[newFrameIndex])
    time.sleep(1/framerate * float(sys.argv[2]))
