import cv2

def mouse_callback(event, x, y, flags, param):
    global img, pixel_coords, drawing, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 0, 255), 1)
            cv2.imshow("image", img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 255), -1)
        x1, y1 = min(ix, x), min(iy, y)
        x2, y2 = max(ix, x), max(iy, y)
        for coord in pixel_coords:
            if x1 <= coord[0] <= x2 and y1 <= coord[1] <= y2:
                pixel_coords.remove(coord)
        cv2.imshow("image", img)

if __name__ == '__main__':
    # Load the image and pixel coordinates
    img = cv2.imread('images/img_with_mask.jpg')
    pixel_coords = [(100, 100), (200, 200), (300, 300), (400, 400)]

    # Create a window to display the image
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_callback)

    # Initialize variables
    drawing = False
    ix, iy = -1, -1

    while True:
        cv2.imshow("image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
