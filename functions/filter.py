from PIL import Image, ImageFilter, ImageDraw, ImageOps
import numpy as np

def normalize(array: np.ndarray, alpha: float = 0, beta: float = 1.0) -> np.ndarray:
    min_val = np.min(array)
    max_val = np.max(array)
    if max_val == min_val:
        return np.zeros_like(array)
    norm = (beta - alpha) * (array - min_val) / (max_val - min_val) + alpha
    return norm

def DoG(image: Image, sigma: float = 1) -> Image:
    k = 1.6
    sigma2 = k * sigma
    image = image.convert('L')
    # Применяем размытие
    I1 = np.array(image.filter(ImageFilter.GaussianBlur(sigma)))
    I2 = np.array(image.filter(ImageFilter.GaussianBlur(sigma2)))
    dog = (I1 - I2) + image#* (image - I2 * I1)
    dog = normalize(dog)
    median_val = np.median(dog)
    threshold = max(0.1, median_val * 0.5)
    binary_edges = (dog > threshold).astype(np.uint8) * 255
    # Обнуляем отрицательные значения и нормализуем
    #dog = np.maximum(dog, 0)
    #dog = np.minimum(dog, 1)
    
    #dog = dog / np.max(dog)
    #np.savetxt("test.txt", dog.astype(int), delimiter="", fmt='%d')
    img = Image.fromarray((binary_edges).astype(np.uint8))
    img.show()
    img.save("test.jpg")


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
    y = np.sum(windows * kernel_y, axis=(2, 3))

    th = 2
    magnitude = np.sqrt(x ** 2 + y ** 2)
    magnitude = magnitude > th
    magnitude = magnitude / np.max(magnitude)

    vector = (np.arctan2(y, x) / np.pi) * 0.5 + 0.5
    vector = vector / np.max(vector)

    np.savetxt('magnitude.txt', magnitude, delimiter=',')
    Image.fromarray(vector * 255).show()

    #for y in range(height):
    #    for x in range(width):
    #        if magnitude[y,x] == 0:
    #            image.putpixel((x, y), 255)
    #        else:
    #            image.putpixel((x, y), 0)
    #image.show()

DoG(Image.open('C:/Users/lox/Desktop/projects/py/img2ascii/resources/examples/maxresdefault.jpg'))