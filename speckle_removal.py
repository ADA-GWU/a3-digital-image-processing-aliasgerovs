import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

def crimmins_speckle_removal(image):
    new_image = image.copy()
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    for _ in range(4): 
        eroded = cv2.erode(new_image, se)
        temp = np.maximum(eroded, new_image + 1)
        new_image = np.where(new_image > temp, new_image - 1, new_image)

    for _ in range(4):
        dilated = cv2.dilate(new_image, se)
        temp = np.minimum(dilated, new_image - 1)
        new_image = np.where(new_image < temp, new_image + 1, new_image)

    return new_image

def process_and_display_image(image_path):
    image = cv2.imread(image_path, 0)
    if image is None:
        print(f"Could not read image: {image_path}")
        return

    crimmins_filtered_image = crimmins_speckle_removal(image)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(crimmins_filtered_image, cmap='gray')
    plt.title('Crimmins Filtered')
    plt.axis('off')
    plt.show()

image_folder_path = 'noisy/speckle/'
image_files = [f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))]
parser = argparse.ArgumentParser()
parser.add_argument('number_of_images', type=int, help='Number of images to process')
args = parser.parse_args()
number_of_images = args.number_of_images

for image_name in sorted(image_files)[:number_of_images+1]:
    image_path = os.path.join(image_folder_path, image_name)
    process_and_display_image(image_path)