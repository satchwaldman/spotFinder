import cv2
import numpy as np
import ast


# img = cv2.imread('images/trial_1_second_edit.jpg') 

# Define the 2D matrix of coordinates
# coordinates = np.array([[10, 10], [20, 20], [30, 30], [40, 40], [50, 50]])

# coordinates_2d = np.array([[[10, 10], [20, 10], [30, 10]], [[10, 20], [20, 20], [30, 20]], [[10, 30], [20, 30], [30, 30]]])
# coords_2d_flat = coordinates_2d.reshape(-1, 2)
# coordinates = coords_2d_flat

with open('centers.txt', 'r') as file:
    coordinates_str = file.read()

coordinates_tuple = ast.literal_eval(coordinates_str)
# coordinates = [list(elem) for elem in coordinates_tuple]
coordinates = coordinates_tuple

print(coordinates)


# Define the color of the selected pixel
selected_color = (0, 255, 0)  # Green

# Define the function to display the image
def display_image():
    img = cv2.imread('images/trial_1_second_edit.jpg') #np.zeros((100, 100, 3), np.uint8)
    for coord in coordinates:
        img[coord[1], coord[0]] = (0, 0, 255)  # Red
    cv2.imshow('image', img)

# Define the mouse callback function
def mouse_callback(event, x, y, flags, param):
    global selected_index
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_coord = (y, x)  # Reverse the order of x, y
        # selected_coord = [x, y]
        print('Selected pixel:', selected_coord)
        # Map the pixel coordinates to the corresponding index in the 2D matrix
        selected_index = np.argmin(np.sum(np.abs(coordinates - selected_coord), axis=1))
        print('Selected index:', selected_index)
        # Display the selected pixel
        img = cv2.imread('images/trial_1_second_edit.jpg') #np.zeros((100, 100, 3), np.uint8)  # Create a blank image
        img[coordinates[selected_index][0], coordinates[selected_index][1]] = selected_color
        cv2.imshow('image', img)

# Define the keyboard callback function
def keyboard_callback(key):
    global selected_index
    global coordinates
    # Move the selected pixel based on the arrow key pressed
    if key == ord('w'):
        coordinates[selected_index][0] -= 1  # Move up
    elif key == ord('s'):
        coordinates[selected_index][0] += 1  # Move down
    elif key == ord('a'):
        coordinates[selected_index][1] -= 1  # Move left
    elif key == ord('d'):
        coordinates[selected_index][1] += 1  # Move right
    # Update the image to reflect the new position of the selected pixel
    img = cv2.imread('images/trial_1_second_edit.jpg') #np.zeros((100, 100, 3), np.uint8)
    for coord in coordinates:
        img[coord[1], coord[0]] = (0, 0, 255)  # Red
    img[coordinates[selected_index][0], coordinates[selected_index][1]] = selected_color
    cv2.imshow('image', img)

# Display the image
display_image()

# Set up the mouse callback function
cv2.setMouseCallback('image', mouse_callback)

# Set up the keyboard callback function
while True:
    key = cv2.waitKey(0)
    if key == 27:  # Esc key
        break
    keyboard_callback(key)

# Close all windows
cv2.destroyAllWindows()
