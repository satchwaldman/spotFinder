def is_black(pixel):
    black_bool = [False, False, False]
    for rgb_idx in range(3):
        if pixel[rgb_idx] <= 20:
            black_bool[rgb_idx] = True
    return black_bool[0] and black_bool[1] and black_bool[2]

pixel_1 = [255, 255, 255]
pixel_2 = [0,0,0]
pixel_3 = [1, 13, 7]
pixel_4 = [240, 255, 234]

print(is_black(pixel_1)) #f
print(is_black(pixel_2)) #t
print(is_black(pixel_3)) #t
print(is_black(pixel_4)) #f
