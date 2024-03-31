import os
import pydicom
from pydicom.data import get_testdata_files
import matplotlib.pyplot as plt

def load_mri_slices(directory):
    slices = [pydicom.dcmread(os.path.join(directory, f)) for f in os.listdir(directory) if f.endswith('.dcm')]
    slices.sort(key=lambda x: int(x.InstanceNumber))
    return slices

def print_metadata(dicom_slice):
    print('Metadata : ', dicom_slice)


def visualize_slices(slices):
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.pixel_array, cmap='gray')
        axes[i].axis('off')
    plt.show()

dicom_directory = 'mri/Brain Tumor Train/00002/T1wCE'
mri_slices = load_mri_slices(dicom_directory)

print_metadata(mri_slices[0])
visualize_slices(mri_slices[30:35])