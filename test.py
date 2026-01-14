from PIL import Image
import numpy as np
img = np.array(Image.open("test.png"))
split = np.dsplit(img, [2,2,3])
print(split[0])
Image.fromarray(split[0]).show()