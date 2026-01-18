from PIL import Image, ImageFilter, ImageDraw, ImageOps
import numpy as np

char_size: tuple = {"x": 8, "y": 8}

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

def get_edge(array: np.ndarray, filter_value = 0) -> int:
    v, c = np.unique(array[array != filter_value].flatten(), return_counts=True)
    if(len(v) > 0):
        return v[np.argmax(c)]
    else:
        return filter_value

def edges_map(vector: np.ndarray, magnitude: np.ndarray, threshold: float = 0.25):
    y_size, x_size = vector.shape
    c = 1
    columns = round(x_size / char_size["x"])
    rows = round(y_size / char_size["y"])
    
    mask_h = ((vector >= 0.4375) & (vector <= 0.5625)) | (vector <= 0.0625) | (vector >= 0.9375)
    mask_v = ((vector >= 0.1875) & (vector <= 0.3125)) | ((vector >= 0.6875) & (vector <= 0.8125))
    mask_dr = ((vector >= 0.3125) & (vector <= 0.4375)) | ((vector >= 0.5625) & (vector <= 0.6875))
    mask_dl = ((vector >= 0.0625) & (vector <= 0.1875)) | ((vector >= 0.8125) & (vector <= 0.9375))
    
    temp = np.zeros_like(vector, dtype=int)
    temp[mask_h] = -4
    temp[mask_v] = -3
    temp[mask_dl] = -2
    temp[mask_dr] = -1
    temp[(magnitude == False)] = 0
    
    vec_tiles = temp.reshape(rows, char_size["y"], columns, char_size["x"], c).transpose(0, 2, 1, 3, 4)
    
    mag_tiles = magnitude.reshape(rows, char_size["y"], columns, char_size["x"], c).transpose(0, 2, 1, 3, 4)
    mag_map = (mag_tiles.sum(axis=(2, 3, 4)) / char_size["y"] * char_size["x"] * mag_tiles.shape[-1] / 100) > threshold
    
    #vfunc = np.vectorize(lambda x: get_edge(x, filter_value=0), signature='(n)->()')
    vec_map = np.empty((rows, columns), dtype= np.int64)
    for y in range(rows):
        for x in range(columns):
            vec_map[y][x] = get_edge(vec_tiles[y][x], filter_value=0)
    return (vec_map, mag_map)
    
def preprocessing(array: np.ndarray, threshold: float = 0.9):
    return (array > thresh(array, threshold)).astype(np.uint8) * 255

def filter(image: Image, DoG_bool: bool = False, DoG_threshold: float = 0.5,
    preprocessing_bool: bool = False, preprocessing_threshold: float = 0.9,
    sector_threshold:float = 0.25):
    image = image.convert("L")
    image_array = np.array(image)
    if(preprocessing_bool):
        image_array = preprocessing(image_array, preprocessing_threshold)
        image = Image.fromarray(image_array)
    if(DoG_bool):
        image_array = DoG(image, DoG_threshold)
    v, m = sobel(image_array)
    return edges_map(v ,m, sector_threshold)
     
#i = np.array(Image.open("resources/examples/Simple.jpg").convert("L"))
#v, m = sobel(i)
#v, m = edges_map(v ,m)

#Image.fromarray(v * m * 255).resize((round(240 / 8), round(240 / 8))).show()