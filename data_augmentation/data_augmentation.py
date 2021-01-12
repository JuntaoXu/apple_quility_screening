import random
import math
import cv2
import numpy as np
from skimage import exposure
from skimage.util import random_noise


# crop
def crop_img_bboxes(img, bboxes):
    # get width and height
    w, h = img.shape[:2]

    x_min = w
    x_max = 0
    y_min = h
    y_max = 0
    for bbox in bboxes:
        x_min = min(x_min, bbox[0])
        y_min = min(y_min, bbox[1])
        x_max = max(x_max, bbox[2])
        y_max = max(y_max, bbox[3])

    # largest distance to all edges with all boxed included
    d_to_left = x_min
    d_to_right = w - x_max
    d_to_top = y_min
    d_to_bottom = h - y_max

    # randomly expand smallest area able to crop
    crop_x_min = int(x_min - random.uniform(0, d_to_left))
    crop_y_min = int(y_min - random.uniform(0, d_to_top))
    crop_x_max = int(x_max + random.uniform(0, d_to_right))
    crop_y_max = int(y_max + random.uniform(0, d_to_bottom))

    # avoid out of range
    crop_x_min = max(0, crop_x_min)
    crop_y_min = max(0, crop_y_min)
    crop_x_max = min(w, crop_x_max)
    crop_y_max = min(h, crop_y_max)

    crop_img = img[crop_y_min:crop_y_max, crop_x_min:crop_x_max]

    # crop image
    crop_bboxes = list()
    for bbox in bboxes:
        crop_bboxes.append([bbox[0] - crop_x_min, bbox[1] - crop_y_min,
                            bbox[2] - crop_x_min, bbox[3] - crop_y_min])

    return crop_img, crop_bboxes


# pan
def shift_pic_bboxes(img, bboxes):
    # get width and height
    w, h = img.shape[:2]

    x_min = w
    x_max = 0
    y_min = h
    y_max = 0
    for bbox in bboxes:
        x_min = min(x_min, bbox[0])
        y_min = min(y_min, bbox[1])
        x_max = max(x_max, bbox[2])
        y_max = max(x_max, bbox[3])

    # largest distance to all edges with all boxed included
    d_to_left = x_min
    d_to_right = w - x_max
    d_to_top = y_min
    d_to_bottom = h - y_max

    # line 1, if x > 0, right shift, else left shift
    # line 2, if y > 0, up shift, else down shift
    x = random.uniform(-(d_to_left / 3), d_to_right / 3)
    y = random.uniform(-(d_to_top / 3), d_to_bottom / 3)
    M = np.float32([[1, 0, x], [0, 1, y]])

    # Affine transformation of the img
    shift_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

    # shifting the bounding box
    shift_bboxes = list()
    for bbox in bboxes:
        shift_bboxes.append([bbox[0] + x, bbox[1] + y, bbox[2] + x, bbox[3] + y])

    return shift_img, shift_bboxes


# alter exposure
def alterLight(img):
    flag = random.uniform(0.5, 1.5)  # lighter when flag < 1, darker when flag > 1
    return exposure.adjust_gamma(img, flag)


# add_noise
def addNoise(img):
    # output pixel between 0 and 1, thus need to be multiplied by 255
    return random_noise(img) * 255


# rotate img and bboxes
def rotate_img_bboxes(img, bboxes, degrees):
    # get width and height of the img
    w, h = img.shape[:2]
    # rotate the img by degrees
    rotated = cv2.getRotationMatrix2D((w / 2, h / 2), degrees, 1)
    img = cv2.warpAffine(img, rotated, (w, h))

    # convert degree into radian, positive radian leads to anticlockwise Affine transformation
    rotate_degrees = -1 * math.pi * (degrees/180)
    rotated_bboxes = []
    for bbox in bboxes:
        # change the coordiante center origin to center of the image
        bbox[0] = bbox[0] - 0.5
        bbox[1] = bbox[1] - 0.5
        # get xmin, xmax, ymin, ymax to construct diagonal points A(xmin, ymin) & D(xmax, ymax)
        xmin, ymin = bbox[0] - bbox[2] / 2, bbox[1] - bbox[3] / 2
        xmax, ymax = bbox[0] + bbox[2] / 2, bbox[1] + bbox[3] / 2
        '''
        Affine transformation, anticlockwise with positive rotate_degrees
        x' = cos(degree) * x - sin(degree) * y
        y' = sin(degree) * x + cos(degree) * y
        '''
        # A' & D‘
        Ax = math.cos(rotate_degrees) * xmin - math.sin(rotate_degrees) * ymin + 0.5
        Ay = math.sin(rotate_degrees) * xmin + math.cos(rotate_degrees) * ymin + 0.5
        Dx = math.cos(rotate_degrees) * xmax - math.sin(rotate_degrees) * ymax + 0.5
        Dy = math.sin(rotate_degrees) * xmax + math.cos(rotate_degrees) * ymax + 0.5

        # get xmid', ymid', w, h
        rotated_bboxes.append([(Ax + Dx)/2, (Ay + Dy)/2, abs(Ax - Dx), abs(Ay - Dy)])

    return img, rotated_bboxes


# flip
def flip_pic_bboxes(img, bboxes):
    import copy
    flip_img = copy.deepcopy(img)
    if random.random() < 0.5:
        horizon = True
    else:
        horizon = False
    h, w = img.shape[:2]
    if horizon:  # horizontal flip
        flip_img = cv2.flip(flip_img, 1)
    else:   # vertical flip
        flip_img = cv2.flip(flip_img, 0)
    # modify bboxes
    flip_bboxes = list()
    for bbox in bboxes:
        x_min = bbox[0] - bbox[2]/2
        y_min = bbox[1] - bbox[3]/2
        x_max = bbox[2] + bbox[2]/2
        y_max = bbox[3] = bbox[2]/2
        if horizon:
            flip_bboxes.append([1 - bbox[0], bbox[1], bbox[2], bbox[3]])
        else:
            flip_bboxes.append([bbox[0], 1 - bbox[1], bbox[2], bbox[3]])
    print(flip_bboxes)
    return flip_img, flip_bboxes