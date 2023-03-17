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
# import cv2

## Instantiate Parameters
subplot_width = 2
subplot_height = 2

dot_x = 157
dot_y = 45
dot_size = 5

plt.figure(figsize=(15, 8))

## Import Image
img = Image.open("images/edited_dots_on_paper_1.jpg")
img = np.asarray(img)

plt.subplot(subplot_width, subplot_height, 1)
img_color_show = plt.imshow(img)

## Create Artificial Point
img_mutable = img.copy()
img_mutable[dot_y : dot_y + dot_size, dot_x : dot_x + dot_size] = [255, 0, 0]  # set the pixel at (500, 500) to red

plt.subplot(subplot_width, subplot_height, 2)
img_color_dot_show = plt.imshow(img_mutable)

## Print all colors (25) from the 5x5 dot

# print(img[dot_y : dot_y + dot_size, dot_x : dot_x + dot_size]) # print img dot 
def find_min_rgb(img, dot_x, dot_y, dot_size):
    min_rgbs = [255, 255, 255]
    for y_pixel in range(dot_y, dot_y + dot_size):
        for x_pixel in range(dot_x, dot_x + dot_size):
            for color in range(3):
                curr_pixel = img[y_pixel][x_pixel][color]
                if curr_pixel < min_rgbs[color]:
                    min_rgbs[color] = curr_pixel
    return min_rgbs

def find_max_rgb(img, dot_x, dot_y, dot_size):
    max_rgbs = [0, 0, 0]
    for y_pixel in range(dot_y, dot_y + dot_size):
        for x_pixel in range(dot_x, dot_x + dot_size):
            for color in range(3):
                curr_pixel = img[y_pixel][x_pixel][color]
                if curr_pixel > max_rgbs[color]:
                    max_rgbs[color] = curr_pixel
    return max_rgbs



# print(find_max_rgb(img, dot_x, dot_y, dot_size))

## Storing different pixel value ranges for yellows

yellow_locations = [(157,45)]

all_yellow_rgb_max = np.array([find_max_rgb(img, x, y, dot_size) for x,y in yellow_locations]).flatten()
all_yellow_rgb_min = np.array([find_min_rgb(img, x, y, dot_size) for x,y in yellow_locations]).flatten()

yellow_rgb_ranges = np.transpose([all_yellow_rgb_min, all_yellow_rgb_max])
# color_range_tuples = [color_range_tuples.append((color_min, color_max)) for color_min, color_max in (all_yellow_rgb_min, all_yellow_rgb_max)]
# for color_min, color_max in zip(all_yellow_rgb_min, all_yellow_rgb_max):
#     color_range_tuples.append((color_min, color_max))


## update pixel values
img_yellow_updates = Image.fromarray(img)
img_yellow_updates = np.array(img_yellow_updates)
for pixel_row in img_yellow_updates:
    for pixel in pixel_row:
        is_yellow = [False, False, False]
        for color in range(3):
            if pixel[color] in yellow_rgb_ranges[color]:
                is_yellow[color] = True
        if is_yellow[0] and is_yellow[1] and is_yellow[2]:
            img_yellow_updates[pixel_row][pixel] = [255,0,0] # set pixel to black




## Plotting grayscale images
plt.subplot(subplot_width, subplot_height, 3)
img_pil = Image.fromarray(img)
img_grayscale = ImageOps.grayscale(img_pil)

## Plot Many -- see script

## Plot just one grayscale image
threshold = 190  
img_grayscale = img_grayscale.point(lambda p: p >threshold and 255)
img_gray_show = plt.imshow(img_grayscale, cmap='gray')

plt.subplot(subplot_width, subplot_height, 4)
plt.imshow(img_yellow_updates)

plt.show()

## Plot Big colored image with red dot seperately 
plt.figure()
plt.figure(figsize=(15, 8))
img_color_dot_show = plt.imshow(img_yellow_updates)
plt.show()



