from PIL import Image, ImageDraw, ImageFont
import os

global OriginalImage, ResizedImage, GrayScaleImage, FileInfo
global CharSet, Background, Foreground

CharSet = " .:coP0?@■"
FontRatioX = {"cour.ttf":1 , "consolas.ttf":0.80108695652}
CharSize = {"x" : 8, "y" : 8}

RatioY = 6 / 13 #ширина / высота
RatioX = 13 / 6 #Высота / Ширина
dv = 255 / (len(CharSet)-1)