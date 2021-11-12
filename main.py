import subprocess
import sys
from PIL import Image
import math
import os


class colour:
    def __init__(self, r=None, g=None, b=None, a=None):
        self.r = round(r)
        self.g = round(g)
        self.b = round(b)

    def code(self):
        return u'\033[48;2;'+str(self.r)+';'+str(self.g)+';'+str(self.b)+'m'

class cell:
    def __init__(self, character='  ', colour=colour(200, 200, 200)):
        self.colour = colour
        self.character = character

    def rendered(self):
        return (u'\033[' + self.colour.code()) + self.character

class picture:
    def __init__(self, im):
        self.width = math.floor(os.get_terminal_size().columns/2)
        self.height = math.floor(os.get_terminal_size().lines)
        self.text = []
        px = im.load()
        for i in range(self.height):
            self.text.append([])
            for j in range(self.width):
                self.text[i].append(cell(colour=colour(*px[j*(im.width/self.width), i*(im.height/self.height)])))
        im.close()

    def rendered(self):
        string = ''
        for i in range(self.height):
            for j in range(self.width):
                string += self.text[i][j].rendered()
            string += u'\033[0m\n'
        return string[:-1]


if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    myCanvas = picture(im)
    print(myCanvas.rendered(), end='', flush=True)

def render(filePath):
    im = Image.open(filePath)
    return picture(im).rendered()
