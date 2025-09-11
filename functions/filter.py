from PIL import Image, ImageFilter, ImageDraw
import numpy as np

def mega_sobel(path2img):
    image = Image.open(path2img).convert('L')
    width, height = image.size
    #image = image.resize((round(width/8), round(height/8)), Image.LANCZOS)
    #Image.open(path2img).filter(ImageFilter.FIND_EDGES).show()
    img_array = np.array(image)

    kernel_x = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
    kernel_y = np.array([[-3, -10, -3], [0, 0, 0], [3, 10, 3]])

    padded = np.pad(img_array, ((1, 1), (1, 1)), mode='constant')
    x = np.zeros_like(padded)
    y = np.zeros_like(padded)

    windows = np.lib.stride_tricks.sliding_window_view(padded, (3, 3))
    x = np.sum(windows * kernel_x, axis=(2, 3))
    #Image.fromarray(x / np.max(x) * 255).show()
    y = np.sum(windows * kernel_y, axis=(2, 3))
    #Image.fromarray(y / np.max(y) * 255).show()

    th = 2500
    magnitude = np.sqrt(x ** 2 + y ** 2)
    #magnitude = magnitude > th
    magnitude = magnitude / np.max(magnitude)

    vector = (np.arctan2(y, x) / np.pi) * 0.5 + 0.5
    vector = vector / np.max(vector)

    # np.savetxt('vector.txt', vector, delimiter=',')
    # Image.fromarray(vector * 255).show()

    for y in range(height):
        for x in range(width):
            if magnitude[y,x] == 0:
                image.putpixel((x, y), 255)
            else:
                image.putpixel((x, y), 0)
    image.show()

