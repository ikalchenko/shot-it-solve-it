import cv2
import numpy as np


def get_proportional_dimensions(src_shape, to_max_dim):
    height, width = src_shape
    if height > width:
        width = int((to_max_dim * width) / height)
        height = to_max_dim
    else:
        height = int((to_max_dim * height) / width)
        width = to_max_dim
    return width, height


def wrap_with_border(src, dim):
    height, width = src.shape
    add_to_top = add_to_bottom = int((dim - height) / 2)
    add_to_right = add_to_left = int((dim - width) / 2)
    add_to_top += 1 if add_to_top * 2 + height < dim else 0
    add_to_right += 1 if add_to_right * 2 + width < dim else 0

    return cv2.copyMakeBorder(src,
                              add_to_top,
                              add_to_bottom,
                              add_to_left,
                              add_to_right,
                              borderType=cv2.BORDER_CONSTANT,
                              value=(255, 255, 255))


def del_inclusions(arr):
    arr_clean = [*arr]
    for idx, i in enumerate(arr):
        for j in arr:
            if (i[0] > j[0] and i[1] > j[1]
                and (i[0] + i[2] * 0.8) < (j[0] + j[2])
                and (i[1] + i[3] * 0.8) < (j[1] + j[3])):
                arr_clean[idx] = None
    arr_clean = [coord for coord in arr_clean if coord is not None]
    return arr_clean


def prepare(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, get_proportional_dimensions(image.shape, 500))

    kernel = np.ones((3,3),np.uint8)
    retval, threshold = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    dilated = cv2.erode(threshold, kernel, iterations=1)
    im2, cnts, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_SIMPLE)

    rects = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        if 20 <= h < image.shape[0] - 200:
            rect = (x, y, w, h)
            rects.append(rect)
            # cv2.rectangle(dilated, (x, y), (x+w, y+h), (0, 255, 0), 1)
    rects.sort(key=lambda arr: arr[0])
    images = []
    rects = del_inclusions(rects)
    for rect in rects:
        cropped = dilated[rect[1]:rect[1] + rect[3],
                          rect[0]:rect[0] + rect[2]]
        images.append(cropped)
    resized = []
    for img in images:
        img1 = cv2.resize(img, get_proportional_dimensions(img.shape, 18))
        resized.append(img1)

    final = []
    for rsz in resized:
        fitted = wrap_with_border(rsz, 28)
        fin = cv2.bitwise_not(fitted)
        final.append(fin)

    # for idx, fin in enumerate(final):
    #     cv2.imshow(f'img{idx}', fin)
    # cv2.imshow('dir', dilated)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return final


if __name__ == '__main__':
    prepare('media/photo_2018-12-17_02-29-00.jpg')
