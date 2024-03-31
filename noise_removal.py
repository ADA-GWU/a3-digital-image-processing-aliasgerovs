import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def apply_morphological_operations(image):
    dilation_kernel = np.ones((3, 3), np.uint8)
    erosion_kernel = np.ones((2, 2), np.uint8)
    dilated_image = cv2.dilate(image, dilation_kernel, iterations=10)
    eroded_image = cv2.erode(dilated_image, erosion_kernel, iterations=12)
    return eroded_image

def apply_mean_filter(image):
    kernel_size = (2, 2)
    mean_filtered_image = cv2.blur(image, kernel_size)
    return mean_filtered_image

def apply_median_filter(image):
    median_filtered_image = cv2.medianBlur(image, 1)
    return median_filtered_image

def apply_bilateral_filter(image):
    bilateral_filtered_image = cv2.bilateralFilter(image, 9, 75, 75)
    return bilateral_filtered_image

def apply_conservative_smoothing(image, size=3):
    temp_image = image.copy()
    pad_size = size // 2
    padded_image = cv2.copyMakeBorder(temp_image, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT)
    for i in range(pad_size, padded_image.shape[0] - pad_size):
        for j in range(pad_size, padded_image.shape[1] - pad_size):
            neighborhood = padded_image[i - pad_size:i + pad_size + 1, j - pad_size:j + pad_size + 1]
            max_val, min_val = neighborhood.max(), neighborhood.min()
            if temp_image[i - pad_size, j - pad_size] > max_val:
                temp_image[i - pad_size, j - pad_size] = max_val
            elif temp_image[i - pad_size, j - pad_size] < min_val:
                temp_image[i - pad_size, j - pad_size] = min_val
    return temp_image

def apply_low_pass_filter(image):
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2 

    mask = np.zeros((rows, cols, 2), np.uint8)
    mask[crow-30:crow+30, ccol-30:ccol+30] = 1

    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    return img_back

def apply_high_pass_filter(image):
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols, 2), np.uint8)
    r = 30  
    center = [crow, ccol]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
    mask[mask_area] = 0
    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    return img_back

def apply_gaussian_smoothing(image):
    gaussian_smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)
    return gaussian_smoothed_image

def apply_laplacian_filter(image):
    laplacian_filtered_image = cv2.Laplacian(image, cv2.CV_64F)
    return laplacian_filtered_image

def apply_unsharp_filter(image):
    gaussian_blur = cv2.GaussianBlur(image, (9, 9), 10.0)
    unsharp_image = cv2.addWeighted(image, 1.5, gaussian_blur, -0.5, 0, image)
    return unsharp_image

parser = argparse.ArgumentParser()
parser.add_argument('number_of_images', type=int, help='Number of images to process')
args = parser.parse_args()

image_folder_path = 'noisy/chemical/'

image_files = [f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))]
image_files = sorted(image_files)[:args.number_of_images]

for image_name in image_files:
    image_path = os.path.join(image_folder_path, image_name)
    image = cv2.imread(image_path, 0)

    morphological = apply_morphological_operations(image)
    mean_filtered_image = apply_mean_filter(image)
    median_filtered_image = apply_median_filter(image)
    gaussian_smoothed_image = apply_gaussian_smoothing(image)
    bilateral_filtered_image = apply_bilateral_filter(image)
    conservative_smoothed_image = apply_conservative_smoothing(image)
    low_pass_filtered_image = apply_low_pass_filter(image)
    high_pass_filtered_image = apply_high_pass_filter(image)
    laplacian_filtered_image = apply_laplacian_filter(image)
    unsharp_image = apply_unsharp_filter(image)

    titles = ['Original', 'Morphological', 'Mean Filter', 'Median Filter', 'Gaussian Smoothing',
              'Conservative Smoothing', 'Low-Pass Filter', 'High Pass Filter', 'Laplacian', 'Unsharp Masking', 'Bilateral Filter']
    images = [image, morphological, mean_filtered_image, median_filtered_image, gaussian_smoothed_image,
              conservative_smoothed_image, low_pass_filtered_image, high_pass_filtered_image, laplacian_filtered_image, unsharp_image, bilateral_filtered_image]

    plt.figure(figsize=(18, 12))
    for i in range(len(images)):
        plt.subplot(3, 4, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()