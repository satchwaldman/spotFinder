# # Standard imports
# import cv2
# import numpy as np;
 
# # Read image
# im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)
 
# # Set up the detector with default parameters.
# detector = cv2.SimpleBlobDetector()
 
# # Detect blobs.
# keypoints = detector.detect(im)
 
# # Draw detected blobs as red circles.
# # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
# im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# # Show keypoints
# cv2.imshow("Keypoints", im_with_keypoints)
# cv2.waitKey(0)

#### ------------------------------------------

# #!/usr/bin/python

# # Standard imports
# import cv2
# import numpy as np;

# # Read image
# im = cv2.imread("images/edited_dots_on_paper_1.jpg")

# # Setup SimpleBlobDetector parameters.
# params = cv2.SimpleBlobDetector_Params()

# # Change thresholds
# params.minThreshold = 10
# params.maxThreshold = 200


# # Filter by Area.
# params.filterByArea = True
# params.minArea = 1500

# # Filter by Circularity
# params.filterByCircularity = True
# params.minCircularity = 0.1

# # Filter by Convexity
# params.filterByConvexity = True
# params.minConvexity = 0.87

# # Filter by Inertia
# params.filterByInertia = True
# params.minInertiaRatio = 0.01

# # Create a detector with the parameters
# # OLD: detector = cv2.SimpleBlobDetector(params)
# detector = cv2.SimpleBlobDetector_create(params)


# # Detect blobs.
# keypoints = detector.detect(im)

# # Draw detected blobs as red circles.
# # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# # the size of the circle corresponds to the size of blob

# im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# # Show blobs
# cv2.imshow("Keypoints", im_with_keypoints)
# cv2.waitKey(0)

## -----------------------------------------

import cv2
from importlib_metadata import unique_everseen
import numpy as np

def is_black(pixel):
    black_bool = [False, False, False]
    for rgb_idx in range(3):
        if pixel[rgb_idx] <= 20:
            black_bool[rgb_idx] = True
    return black_bool[0] and black_bool[1] and black_bool[2]

def detect_connected_pixels(image):
    # Initialize an empty list to store the centers of the connected pixels.
    centers = []

    # Define a helper function to recursively find all connected pixels.
    def find_connected_pixels(pixel, visited):
        # Check if the pixel is within the bounds of the image and hasn't been visited yet.
        row, col = pixel
        if (0 <= row < len(image)) and (0 <= col < len(image[0])) and (pixel not in visited):
            # Check if the pixel is black 
            if is_black(image[row][col]): 
                # Mark the pixel as visited.
                visited.add(pixel)
                # Recursively find all connected pixels.
                connected_pixels = [
                    (row - 1, col),  # north
                    (row + 1, col),  # south
                    (row, col - 1),  # west
                    (row, col + 1),  # east
                ]
                for p in connected_pixels:
                    find_connected_pixels(p, visited)
                # Once all connected pixels have been found, calculate the center.
                center_row = sum([p[0] for p in visited]) // len(visited)
                center_col = sum([p[1] for p in visited]) // len(visited)
                centers.append((center_row, center_col))

    # Iterate through each pixel in the image and find all connected pixels.
    visited = set()
    for i in range(len(image)):
        for j in range(len(image[0])):
            find_connected_pixels((i, j), visited)

    return centers

image = cv2.imread('images/thresh_blue_with_mask.jpg')
image_list = image.tolist()
print(np.shape(image_list))
# print(image[100])


# Detect all sets of connected pixels and store their center in an array.
centers = detect_connected_pixels(image_list)

# Print the resulting centers.

dt=np.dtype('int,int')
np_centers = np.array(centers,dtype=dt)
# print(unique_centers)

# create an image of the centers
blank_img = np.zeros((918, 1398, 3)) + 255
for red_dot in np_centers:
    blank_img[red_dot[0]][red_dot[1]] = [0, 0, 255]

cv2.imshow("Image with Centers", blank_img)
cv2.waitKey(0)


## --------------------------------------------------------

# import cv2
# import numpy as np

# def detect_connected_pixels(image):
#     # Convert the image to grayscale.
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply adaptive thresholding to binarize the image.
#     _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

#     # Find contours of connected components in the binarized image.
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Compute the centers of the contours.
#     centers = []
#     for contour in contours:
#         M = cv2.moments(contour)
#         if M["m00"] != 0:
#             cx = int(M["m10"] / M["m00"])
#             cy = int(M["m01"] / M["m00"])
#             centers.append((cy, cx))

#     return centers

# image = cv2.imread('images/thresh_blue_with_mask.jpg')

# # Detect all sets of connected pixels and store their center in an array.
# centers = detect_connected_pixels(image)

# # create an image of the centers
# blank_img = np.zeros_like(image)
# for center in centers:
#     cv2.circle(blank_img, center, 3, (0, 0, 255), -1)

# cv2.imshow("Image with Centers", blank_img)
# cv2.waitKey(5000)
