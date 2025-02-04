import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.signal import convolve2d
import math
n=4
def filterImage(image, filter_matrix):
    """Applies the Hadamard product to filter an image."""
    return image * filter_matrix

def createFilter(size, type="gaussian"):
    """Creates a filter of the specified type."""
    match type:
        case "average":
            return np.ones((size, size)) / (size * size)
        case "gaussian":
            # Create a Gaussian filter
            sigma = size / 6.0  # Standard deviation
            ax = np.linspace(-(size - 1) / 2., (size - 1) / 2., size)
            xx, yy = np.meshgrid(ax, ax)
            kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))
            return kernel / np.sum(kernel)
        case "sobel-h":
            return np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        case "sobel-v" | "sobel":
            return np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        case _:
            return np.ones((size, size)) / (size * size)

def createF1(image, n=n, filter_size=7):
    """Generates the Hadamard blurring filter F1."""
    blurred = convolve2d(image, createFilter(filter_size, "gaussian"), mode='same', boundary='symm')
    image_safe = np.maximum(image, 1e-5)  # Avoid division by zero
    return np.power(blurred / image_safe, 1 / (n+1))

# Load the image and convert to grayscale
image = Image.open("image2.png").convert('L')  # Convert to grayscale
image = np.array(image, dtype=float)

# Create the filter
F1 = createF1(image)

# Apply the Hadamard blurring recursively
filtered_images = [image]
mean_intensities = [np.mean(image)]
std_devs = [np.std(image)]

for i in range(n):
    filtered_image = filterImage(filtered_images[-1], F1)
    filtered_images.append(filtered_image)
    mean_intensities.append(np.mean(filtered_image))
    std_devs.append(np.std(filtered_image))

# Display the results
titles = ["Original Image", "First Filter", "Second Filter", "Third Filter", "Fourth Filter", "Fifth Filter"]
for i, img in enumerate(filtered_images):
    plt.imshow(img, cmap='gray')
    plt.title(f"{titles[i]}\nMean: {mean_intensities[i]:.2f}, Std: {std_devs[i]:.2f}")
    plt.axis("off")
    plt.show()


mean_intensities = [float(i) for i in mean_intensities]
std_devs = [float(i) for i in std_devs]
print("Mean Intensities:", mean_intensities)
print("Standard Deviations:", std_devs)