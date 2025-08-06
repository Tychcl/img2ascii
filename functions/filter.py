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

def sobel2(path2img, spread=10):
    gray = np.array(Image.open(path2img).convert('L')).astype(np.float32) / 255.0
    height, width = gray.shape

    # Вычисляем шаг дискретизации (аналог _AsciiStep)
    step = max(1, int(round(min(height, width) / spread)))
    if step < 1:
        step = 1

    # Инициализация выходных градиентов
    gradient_map = np.zeros_like(gray)

    # Проходим по центральным пикселям с учетом шага
    for y in range(step, height - step):
        for x in range(step, width - step):
            # Вычисление горизонтального градиента (Sobel X)
            gx = (
                    -1.0 * gray[y - step, x - step]
                    - 2.0 * gray[y, x - step]
                    - 1.0 * gray[y + step, x - step]
                    + 1.0 * gray[y - step, x + step]
                    + 2.0 * gray[y, x + step]
                    + 1.0 * gray[y + step, x + step]
            )

            # Вычисление вертикального градиента (Sobel Y)
            gy = (
                    -1.0 * gray[y - step, x - step]
                    - 2.0 * gray[y - step, x]
                    - 1.0 * gray[y - step, x + step]
                    + 1.0 * gray[y + step, x - step]
                    + 2.0 * gray[y + step, x]
                    + 1.0 * gray[y + step, x + step]
            )

            # Комбинирование градиентов
            gradient_map[y, x] = np.sqrt(gx ** 2 + gy ** 2)

    # Нормализация и возврат результата
    return (gradient_map * 255).clip(0, 255).astype(np.uint8)

def sobel(path2img):
    image = Image.open(path2img)

    gray = np.array(image.convert('L'))
    gray = gray.astype(np.float32) / 255.0

    h, w = gray.shape

    step = 1

    top_left = gray[:-2 * step, :-2 * step]
    left = gray[step:-step, :-2 * step]
    bottom_left = gray[2 * step:, :-2 * step]

    top_right = gray[:-2 * step, 2 * step:]
    right = gray[step:-step, 2 * step:]
    bottom_right = gray[2 * step:, 2 * step:]

    #top = gray[:-2 * step, :-step]
    #middle = gray[step:-step, 2 * step:]

    gx = -top_left - 2 * left - bottom_left + top_right + 2 * right + bottom_right
    gy = -top_left - 2 * gray[:-2 * step, step:-step] - top_right + bottom_left + 2 * gray[2 * step:,step:-step] + bottom_right

    grad = np.sqrt(gx ** 2 + gy ** 2)
    result = np.zeros_like(gray)
    result[step:h - step, step:w - step] = grad

    Image.fromarray((result * 255).clip(0, 255).astype(np.uint8)).show()
