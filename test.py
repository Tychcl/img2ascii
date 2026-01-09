from PIL import Image, ImageDraw
from functions.ascii import convert
img1 = convert("resources\examples\color.png", color=True)
img1[1].show()