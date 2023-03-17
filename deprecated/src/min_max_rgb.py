# print(img[dot_y : dot_y + dot_size, dot_x : dot_x + dot_size])
# def find_min_rgb(img, dot_x, dot_y, dot_size, color):
#     min_rgb = 255
#     for y_pixel in range(dot_y, dot_y + dot_size):
#         for x_pixel in range(dot_x, dot_x + dot_size):
#             curr_pixel = img[y_pixel][x_pixel][color]
#             if curr_pixel > min_rgb:
#                 min_rgb = curr_pixel
#     return min_rgb

# def find_max_rgb(img_, dot_x_, dot_y_, dot_size_, color_):
#     max_rgb = 0
#     for y_pixel in range(dot_y_, dot_y_ + dot_size_):
#         for x_pixel in range(dot_x_, dot_x_ + dot_size_):
#             curr_pixel = img_[y_pixel][x_pixel][color_]
#             if curr_pixel > max_rgb:
#                 max_rgb = curr_pixel
#     return max_rgb