# take in picture (pd/numpy readfile)
    # turns picture into list of (rgb tuples?)
# take picture and make it 100% contrast to seperate circles from background
# pass a kernal over the image
    # at each step, check if there is a "circle" (just an enclosed collection of pixels) that is within some predefined threshold
        # this can be done without machine learning by defining some threshold for how many "on" (i.e., colored) pixexed should be within this region
    # next, check if the any identified circles have already been identified
        # If not, mark the center and add the coordinates of the center to centers_list
# once the kernal is finished, convert the centers_list into the .xeo format (syntax)

## Import Libraries
from tkinter import image_types
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
import cv2 as cv



## Instantiate Parameters
subplot_width = 2
subplot_height = 2

plt.figure(figsize=(15, 8))

## Import Image
img = Image.open("images/edited_dots_on_paper_1.jpg")
img = np.asarray(img)

## Print each color in a subplot

def get_color_mat(img_, color_):
    height, width = len(img_), len(img_[0])

    # create a new 2D matrix with the same dimensions as the image
    rgb_values = [[0 for _ in range(width)] for _ in range(height)]

    # loop through each pixel of the image and extract the red value
    for i in range(height):
        for j in range(width):
            rgb_values[i][j] = img_[i][j][color_]  # red value is at index 0
    return rgb_values

print('1')
img_red = get_color_mat(img, 0)
print('2')
img_green = get_color_mat(img, 1)
print('3')
img_blue = get_color_mat(img, 2)
print('4')

## Plot one grayscale image

img_pil = Image.fromarray(np.array(img))
img_grayscale = ImageOps.grayscale(img_pil)

## Plot Many -- see script

## Plot just one grayscale image
threshold = 190
img_grayscale = img_grayscale.point(lambda p: p >threshold and 255)
img_gray_show = plt.imshow(img_grayscale, cmap='gray')

plt.show()

## Subplots
# plt.subplot(subplot_width, subplot_height, 1)
# plt.imshow(img)

# plt.subplot(subplot_width, subplot_height, 2)
# plt.imshow(img_red)

# plt.subplot(subplot_width, subplot_height, 3)
# plt.imshow(img_green)

# plt.subplot(subplot_width, subplot_height, 4)
# plt.imshow(img_blue)

# plt.show()


