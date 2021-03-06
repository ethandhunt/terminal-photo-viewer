# terminal-photo-viewer
view images in the terminal using ansi escape codes and python

![example photo](https://github.com/ethandhunt/terminal-photo-viewer/blob/main/Screenshot%20from%202021-12-01%2010-39-03.png?raw=true)

### !! Only tested on `Ubuntu 20.04.3 LTS` with `python version 3.8.10`

## Dependencies
### `Pillow`
To install:
```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

## How to use from terminal
`python3 main.py imagePath.jpg` renders imagePath.jpg

`python3 video.py videoPath.mp4` renders video then displays it with audio (long time to render, high frame rate, high memory, sometimes crashes on long files)

`python3 videoLo.py videoPath.mp4` displays video without prerendering, also with audio (low frame rate)

`python3 save.py imagePath.jpg outputPath.txt` saves an image in the given output file, if you cat the output file it should display correctly


## `main.render(file_path) -> string`
returns a string of ansi escape codes and characters, if printed should display in terminal

Attempts to use true colour


## `main.renderFromGetMethod(getMethod)`
passes (x, y) values ranging from 0 - 1 to `getMethod` to get an image

expects `getMethod` to return an rgb tuple from 0 - 255

example getMethod
```py
def myMethod(x, y):
  return (255*x, 255*y, 255-255*y)
```
result
![screenshot of method result](https://github.com/ethandhunt/terminal-photo-viewer/blob/main/Screenshot%20from%202021-12-01%2010-50-00.png?raw=true)
