import subprocess
import sys
from PIL import Image
import math
import os


class colour:
    def __init__(self, r=None, g=None, b=None, a=None, p='48'):
        self.r = round(r)
        self.g = round(g)
        self.b = round(b)
        self.p = p

    def code(self):
        return u'\033['+self.p+';2;'+str(self.r)+';'+str(self.g)+';'+str(self.b)+'m'

class cell:
    def __init__(self, character=chr(9600), colour1=colour(200, 200, 200), colour2=colour(200, 200, 200)):
        self.colour1 = colour1
        self.colour2 = colour2
        self.colour1.p = '48' #fg
        self.colour2.p = '38' #bg
        self.character = character

    def rendered(self):
        return self.colour1.code() + self.colour2.code() + self.character

class picture:
    def __init__(self, px, srcWidth, srcHeight, blank=False):
        if blank: return
        self.width = math.floor(os.get_terminal_size().columns)
        self.height = math.floor(os.get_terminal_size().lines)
        self.text = []
        for i in range(self.height):
            self.text.append([])
            for j in range(self.width):
                thisIndex1a = min(j*(srcWidth/self.width), srcWidth-1)
                thisIndex2a = min(i*(srcHeight/self.height) + ((srcHeight/self.height)*1), srcHeight-1)
                thisRGBa = px[thisIndex1a, thisIndex2a]
                thisColoura = colour(*thisRGBa)

                thisIndex1b = min(j*(srcWidth/self.width), srcWidth-1)
                thisIndex2b = min(i*(srcHeight/self.height) + ((srcHeight/self.height)/2), srcHeight-1)
                thisRGBb = px[thisIndex1b, thisIndex2b]
                thisColourb = colour(*thisRGBb)
                thisCell = cell(colour1=thisColoura, colour2=thisColourb)
                self.text[i].append(thisCell)

    def rendered(self):
        string = ''
        for i in range(self.height):
            for j in range(self.width):
                string += self.text[i][j].rendered()
            string += u'\033[0m\n'
        return string[:-1]
    
    def fromGetMethod(getMethod):
        self = picture(0, 0, 0, blank=True)
        self.width = math.floor(os.get_terminal_size().columns)
        self.height = math.floor(os.get_terminal_size().lines)
        self.text = []
        for i in range(self.height):
            self.text.append([])
            for j in range(self.width):
                thisColoura = colour(*getMethod(j/self.width, i/self.height))

                thisColourb = colour(*getMethod(j/self.width, i/self.height - 0.5/self.height))

                thisCell = cell(colour1=thisColoura, colour2=thisColourb)

                self.text[i].append(thisCell)
        return self


def render(filePath):
    im = Image.open(filePath)
    return picture(im.load(), im.width, im.height).rendered()

def renderFromGetMethod(get):
    return picture.fromGetMethod(get).rendered()

if __name__ == '__main__':
    print('\033[H', end='')
    print(render(sys.argv[1]))
