from PIL import Image, ImageDraw, ImageFont
import os

global OriginalImage, ResizedImage, GrayScaleImage, FileInfo, CharSet, Background, Foreground
OriginalImage: Image
ResizedImage: Image
GrayScaleImage: Image
FileInfo: dict

CharSet = " .:coP0?@■"
Background: tuple
Foreground: tuple

FontRatioX = {"cour.ttf":1 , "consolas.ttf":0.80108695652}
CharSize = {"x" : 8, "y" : 8}

def ResizeImage(Size: tuple) -> Image:
    if Size is None:
        return OriginalImage.resize((round(OriginalImage.width/CharSize["x"]), round(OriginalImage.height/CharSize["y"])), Image.LANCZOS)
    else:
        return OriginalImage.resize(Size, Image.LANCZOS)
    
def MonoImage() -> Image:
    return ResizedImage.convert("L")

def AsciiImage() -> str:
    AsciiStr = ""
    DV = 255 / (len(CharSet)-1) #Перменная делителя
    for y in range(GrayScaleImage.height):
        for x in range(GrayScaleImage.width):
            AsciiStr += CharSet[round(GrayScaleImage.getpixel((x,y))/DV)]
        AsciiStr += "\n"
    return AsciiStr

def ConvertImage(Path2Image: str, ColorInvert: bool = False, CharSetInvert: bool = False, Resize: bool = True, Size: tuple = None):
    global OriginalImage, ResizedImage, GrayScaleImage, FileInfo, CharSet, Background, Foreground
    if not os.path.exists(Path2Image):
        return None
    
    File = Path2Image.split("/")[-1].split(".")
    FileInfo = {"Name" : File[0], "Format" : File[1]}
    CharSet = CharSet[::-1 if not CharSetInvert else 1]
    if ColorInvert:
        Background = (255, 255, 255) 
        Foreground = (0, 0, 0) 
    else:
        Background = (0, 0, 0)
        Foreground = (255, 255, 255) 

    OriginalImage = Image.open(Path2Image)
    ResizedImage = ResizeImage(Size) if Resize else OriginalImage
    GrayScaleImage = MonoImage()

    AsciiStr = AsciiImage()

    os.mkdir(f"result/{FileInfo["Name"]}")
    txt = f"result/{FileInfo["Name"]}/{FileInfo["Name"]}.txt"
    with open(txt, "w", encoding="utf-8") as f:
        f.write(AsciiStr)
    print(f"txt: {os.path.abspath(txt)}")


