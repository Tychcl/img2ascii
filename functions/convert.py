from PIL import Image, ImageDraw, ImageFont
import os

FontRatioX = {"cour.ttf":1 , "consolas.ttf":0.80108695652}
CharSize = {"x" : 8, "y" : 8} #8x8
OriginalCharSet = " .:coP0?@■"
RatioY = 6 / 13 #ширина / высота
RatioX = 13 / 6 #Высота / Ширина
dv = 255 / (len(OriginalCharSet)-1)

def Image2Mono(Path2Img: str, Resize: bool = True, Size: tuple = None):
    Img = Image.open(Path2Img).convert("L")
    if Size is not None and len(Size) == 2:
        Img = Img.resize((Size[0], Size[1]), Image.LANCZOS)
        return Img
    if Resize:
        Img = Img.resize((round(Img.width/CharSize["x"]*RatioX), round(Img.height/CharSize["y"])), Image.LANCZOS)
    return Img

def Image2Ascii(Img: Image, CharSet: str):
    AsciiStr = ""
    for y in range(Img.height):
        for x in range(Img.width):
            AsciiStr += CharSet[round(Img.getpixel((x,y))/dv)]
        AsciiStr += "\n"
    return AsciiStr
    
def Ascii2Image(AsciiStr: str, FileInfo:dict, ColorInvert: bool = False):
    Background = (255, 255, 255) if ColorInvert else (0, 0, 0)
    Foreground = (0, 0, 0) if ColorInvert else (255, 255, 255)
    lines = [line.rstrip() for line in AsciiStr.split('\n') if line.strip()]
    if not lines:
        return None
    max_line_length = max(len(line) for line in lines)
    height = len(lines)
    font = "cour.ttf"
    img = Image.new("RGB", (round(max_line_length * 10 * FontRatioX[font]), height * CharSize["y"]), Background)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(f"Fonts/{font}", CharSize["x"])
    for y, line in enumerate(lines):
        position = (0, y * CharSize["y"])
        draw.text(position, line, fill=Foreground, font=font)
    save = f"Result/{FileInfo["Name"]}.{FileInfo["Format"]}"
    os.makedirs(os.path.dirname(save), exist_ok=True)
    img.save(save)
    return save

def ConvertImage(Path2Img: str, Resize: bool = True, Size: tuple = None, ColorInvert: bool = False, SymbolsInvert: bool = False):
    if not os.path.exists(Path2Img):
        return None
    File = Path2Img.split("/")[-1].split(".")
    FileInfo = {"Name" : File[0], "Format" : File[1]}
    Invert = -1 if not SymbolsInvert else 1
    CharSet = OriginalCharSet[::Invert]
    Img = Image2Mono(Path2Img, Resize, Size)
    AsciiStr = Image2Ascii(Img, CharSet)
    txt = f"Result/{FileInfo["Name"]}.txt"
    with open(txt, "w", encoding="utf-8") as f:
        f.write(AsciiStr)
    print(f"txt: {os.path.abspath(txt)}")
    print(f"img: {Ascii2Image(AsciiStr, FileInfo, ColorInvert)}")