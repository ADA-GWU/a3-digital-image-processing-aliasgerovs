import cv2
import matplotlib.pyplot as plt
import numpy as np

def crimmins_speckle_removal(image_path):
    image = cv2.imread(image_path, 0)
    new_image = image.copy()
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    for i in range(4): 
        eroded = cv2.erode(new_image, se)
        temp = np.maximum(eroded, new_image + 1)
        new_image = np.where(new_image > temp, new_image - 1, new_image)

    for i in range(4):
        dilated = cv2.dilate(new_image, se)
        temp = np.minimum(dilated, new_image + 1)
        new_image = np.where(new_image < temp, new_image + 1, new_image)

    return new_image

image_path = 'noisy/speckle/4.png'
image = cv2.imread(image_path, 0)
crimmins_speckle_removal_image = crimmins_speckle_removal(image_path)

plt.figure(figsize=(18, 6))
plt.subplot(1, 2, 1)
plt.imshow(cv2.imread(image_path, 0), cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(crimmins_speckle_removal_image, cmap='gray')
plt.title('Crimmins Filtered')
plt.axis('off')
plt.show()
