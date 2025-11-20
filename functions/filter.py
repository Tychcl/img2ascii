from PIL import Image, ImageFilter, ImageDraw, ImageOps
import numpy as np
import time

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

def sobel(array: np.ndarray):
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
    vector = (vector / np.max(vector)) * 255

    #Image.fromarray(magnitude * vector * 255).show()

#sobel(DoG(image=Image.open('C:\\Users\\lox\\Desktop\\projects\\py\\img2ascii\\resources\\examples\\Dog.jpg'), th=2))