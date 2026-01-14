from PIL import Image, ImageFilter, ImageDraw, ImageOps
import numpy as np
import time
from ascii import char_size

def thresh(array: np.ndarray, value = 0.5) -> float:
    """Get optimal threshhold.
    Args:
        array (np.ndarray): array
        value (float): more value - less detail for image array
    Returns:
        float: threshold value
    """
    median_val = np.median(array)
    threshold = max(0.1, median_val * value)
    return threshold

def normalize(array: np.ndarray, alpha: float = 0, beta: float = 1.0) -> np.ndarray:
    """Normalize array by Minimax algorithm.
    Args:
        array (np.ndarray): array
        alpha (float): is the best value that the maximizer currently can guarantee at that level or above.
        beta (float): is the best value that the minimizer currently can guarantee at that level or below.
    Returns:
        np.ndarray: Normalized array
    """
    min_val = np.min(array)
    max_val = np.max(array)
    if max_val == min_val:
        return np.zeros_like(array)
    norm = (beta - alpha) * (array - min_val) / (max_val - min_val) + alpha
    return norm

def DoG(image: Image, sigma: float = 1, th = 0.5) -> np.ndarray:
    """Difference of gaussian func.
    Args:
        image (Image): image
        sigma (float): value of gaussian blur №1
        th (float): threshhold for thresh func
    Returns:
        np.ndarray: w/b mask
    """
    k = 1.6
    sigma2 = k * sigma
    image = image.convert('L')
    I1 = np.array(image.filter(ImageFilter.GaussianBlur(sigma)))
    I2 = np.array(image.filter(ImageFilter.GaussianBlur(sigma2)))
    dog = (I1 - I2) + image
    dog = normalize(dog)
    binary_edges = (dog > thresh(dog, th)).astype(np.uint8) * 255
    return binary_edges

def sobel(array: np.ndarray) -> np.ndarray:
    """Get sobel image.
    Args:
        array (np.ndarray): image array
    """
    kernel_x = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
    kernel_y = np.array([[-3, -10, -3], [0, 0, 0], [3, 10, 3]])

    padded = np.pad(array, ((1, 1), (1, 1)), mode='constant')
    x = np.zeros_like(padded)
    y = np.zeros_like(padded)

    windows = np.lib.stride_tricks.sliding_window_view(padded, (3, 3))
    x = np.sum(windows * kernel_x, axis=(2, 3))
    y = np.sum(windows * kernel_y, axis=(2, 3))

    magnitude = np.sqrt(x ** 2 + y ** 2)
    magnitude = normalize(magnitude)
    magnitude = magnitude > thresh(magnitude)

    vector = (np.arctan2(y, x) / np.pi) * 0.5 + 0.5
    vector = normalize(vector)
    return (vector, magnitude)

def edges_map(vector: np.ndarray, magnitude: np.ndarray, threshold: float = 0.25):
    y_size, x_size = vector.shape
    c = 1
    columns = round(x_size / char_size["x"])
    rows = round(y_size / char_size["y"])
    vec_tiles = vector.reshape(rows, char_size["y"], columns, char_size["x"], c).transpose(0, 2, 1, 3, 4)
    
    mag_tiles = magnitude.reshape(rows, char_size["y"], columns, char_size["x"], c).transpose(0, 2, 1, 3, 4)
    mag_map = (mag_tiles.sum(axis=(2, 3, 4)) / char_size["y"] * char_size["x"] * mag_tiles.shape[-1] / 100) > threshold
    return
    #map = np.empty((rows, columns))
    #for y in range(y_size):
    #    for x in range(x_size):
    #        if(mag_tiles[y][x])
    #Image.fromarray(tiles[0][0]).show()
    #print(len(tiles[0]))
    #split_map = np.dsplit
    
            

def preprocessing(array: np.ndarray, threshold: float = 0.9):
    return (array > thresh(array, threshold)).astype(np.uint8) * 255

def filter(image: Image, DoG_bool: bool = False, DoG_threshold: float = 0.5,
    preprocessing_bool: bool = False, preprocessing_threshold: float = 0.9):
    image = image.convert("L")
    image_array = np.array(image)
    if(preprocessing_bool):
        image_array = preprocessing(image_array, preprocessing_threshold)
        image = Image.fromarray(image_array)
    if(DoG_bool):
        image_array = DoG(image, DoG_threshold)
    image_array = sobel(image_array)
     
i = np.array(Image.open("resources/examples/Simple.jpg").convert("L"))
v, m = sobel(i)
edges_map(v ,m)
#Image.fromarray(v * m * 255).resize((round(240 / 8), round(240 / 8))).show()