import random
import math
import cv2
import numpy as np
from skimage import exposure
from skimage.util import random_noise


# crop
def crop_img_bboxes(img, bboxes):
    '''
    裁剪后图片要包含所有的框
    输入：
        img：图像array
        bboxes：该图像包含的所有boundingboxes，一个list，每个元素为[x_min,y_min,x_max,y_max]
                要确保是数值
    输出：
        crop_img：裁剪后的图像array
        crop_bboxes：裁剪后的boundingbox的坐标，list
    '''
    # ------------------ 裁剪图像 ------------------
    w = img.shape[1]
    h = img.shape[0]

    x_min = w
    x_max = 0
    y_min = h
    y_max = 0
    for bbox in bboxes:
        x_min = min(x_min, bbox[0])
        y_min = min(y_min, bbox[1])
        x_max = max(x_max, bbox[2])
        y_max = max(y_max, bbox[3])

    # 包含所有目标框的最小框到各个边的距离
    d_to_left = x_min
    d_to_right = w - x_max
    d_to_top = y_min
    d_to_bottom = h - y_max

    # 随机扩展这个最小范围
    crop_x_min = int(x_min - random.uniform(0, d_to_left))
    crop_y_min = int(y_min - random.uniform(0, d_to_top))
    crop_x_max = int(x_max + random.uniform(0, d_to_right))
    crop_y_max = int(y_max + random.uniform(0, d_to_bottom))

    # 确保不出界
    crop_x_min = max(0, crop_x_min)
    crop_y_min = max(0, crop_y_min)
    crop_x_max = min(w, crop_x_max)
    crop_y_max = min(h, crop_y_max)

    crop_img = img[crop_y_min:crop_y_max, crop_x_min:crop_x_max]

    # ------------------ 裁剪bounding boxes ------------------
    crop_bboxes = list()
    for bbox in bboxes:
        crop_bboxes.append([bbox[0] - crop_x_min, bbox[1] - crop_y_min,
                            bbox[2] - crop_x_min, bbox[3] - crop_y_min])

    return crop_img, crop_bboxes


# pan
def shift_pic_bboxes(img, bboxes):
    '''
    平移后需要包含所有的框
    参考资料：https://blog.csdn.net/sty945/article/details/79387054
    输入：
        img：图像array
        bboxes：该图像包含的所有boundingboxes，一个list，每个元素为[x_min,y_min,x_max,y_max]
                要确保是数值
    输出：
        shift_img：平移后的图像array
        shift_bboxes：平移后的boundingbox的坐标，list
    '''
    # ------------------ 平移图像 ------------------
    w = img.shape[1]
    h = img.shape[0]

    x_min = w
    x_max = 0
    y_min = h
    y_max = 0
    for bbox in bboxes:
        x_min = min(x_min, bbox[0])
        y_min = min(y_min, bbox[1])
        x_max = max(x_max, bbox[2])
        y_max = max(x_max, bbox[3])

    # 包含所有目标框的最小框到各个边的距离，即每个方向的最大移动距离
    d_to_left = x_min
    d_to_right = w - x_max
    d_to_top = y_min
    d_to_bottom = h - y_max

    # 在矩阵第一行中表示的是[1,0,x],其中x表示图像将向左或向右移动的距离，如果x是正值，则表示向右移动，如果是负值的话，则表示向左移动。
    # 在矩阵第二行表示的是[0,1,y],其中y表示图像将向上或向下移动的距离，如果y是正值的话，则向下移动，如果是负值的话，则向上移动。
    x = random.uniform(-(d_to_left / 3), d_to_right / 3)
    y = random.uniform(-(d_to_top / 3), d_to_bottom / 3)
    M = np.float32([[1, 0, x], [0, 1, y]])

    # 仿射变换
    shift_img = cv2.warpAffine(img, M,
                               (img.shape[1], img.shape[0]))  # 第一个参数表示我们希望进行变换的图片，第二个参数是我们的平移矩阵，第三个希望展示的结果图片的大小

    # ------------------ 平移boundingbox ------------------
    shift_bboxes = list()
    for bbox in bboxes:
        shift_bboxes.append([bbox[0] + x, bbox[1] + y, bbox[2] + x, bbox[3] + y])

    return shift_img, shift_bboxes


# alter exposure
def alterLight(img):
    '''
    adjust_gamma(image, gamma=1, gain=1)函数:
    gamma>1时，输出图像变暗，小于1时，输出图像变亮
    输入：
        img：图像array
    输出：
        img：改变亮度后的图像array
    '''
    flag = random.uniform(0.5, 1.5)  ##flag>1为调暗,小于1为调亮
    return exposure.adjust_gamma(img, flag)


# add_noise
def addNoise(img):
    '''
    输入：
        img：图像array
    输出：
        img：加入噪声后的图像array,由于输出的像素是在[0,1]之间,所以得乘以255
    '''
    return random_noise(img, mode='gaussian', clip=True) * 255


# 随机顺时针旋转90
def rotate_img_bboxes(img, bboxes, rotate_degrees=0.5 * math.pi/2):
    w, h = img.shape[:2]
    rotated = cv2.getRotationMatrix2D((w / 2, h / 2), rotate_degrees, 1)
    img = cv2.warpAffine(img, rotated, (w, h))
    w_rotated, h_rotated = img.shape[:2]

    rotated_bboxes= []
    for bbox in bboxes:
        # change the origin to center of the image
        bbox[0] = bbox[0] * w - w / 2
        bbox[1] = bbox[1] * h - h / 2
        bbox[2] = bbox[2] * w
        bbox[3] = bbox[3] * h
        # get xmin, xmax, ymin, ymax to composite four A, B, C, D point of the bbox
        xmin, ymin = bbox[0] - bbox[2] / 2, bbox[1] - bbox[3] / 2
        xmax, ymax = bbox[0] + bbox[2] / 2, bbox[1] + bbox[3] / 2
        '''
        A: xmin, ymin, B: xmin, ymax, C: xmax, ymin, D: xmax, ymax
        x' = cos(degree) * x - sin(degree) * y
        y' = sin(degree) * x + cos(degree) * y
        '''
        # find x', y' for A', B', C', D'
        Ax = math.cos(rotate_degrees) * xmin - math.sin(rotate_degrees) * ymin
        Ay = math.sin(rotate_degrees) * xmin + math.cos(rotate_degrees) * ymin
        Bx = math.cos(rotate_degrees) * xmin - math.sin(rotate_degrees) * ymax
        By = math.sin(rotate_degrees) * xmin + math.cos(rotate_degrees) * ymax
        Cx = math.cos(rotate_degrees) * xmax - math.sin(rotate_degrees) * ymin
        Cy = math.sin(rotate_degrees) * xmax + math.cos(rotate_degrees) * ymin
        Dx = math.cos(rotate_degrees) * xmax - math.sin(rotate_degrees) * ymax
        Dy = math.sin(rotate_degrees) * xmax + math.cos(rotate_degrees) * ymax
        # seperate x' and y', sort from min to max
        rotated_bbox_x = [Ax, Bx, Cx, Dx]
        rotated_bbox_y = [Ay, By, Cy, Dy]
        rotated_bbox_x.sort()
        rotated_bbox_y.sort()

        xmid = ((rotated_bbox_x[0] + rotated_bbox_x[3]) / 2 + w_rotated/2) / w
        ymid = ((rotated_bbox_y[0] + rotated_bbox_y[3]) / 2 + h_rotated/2) / w
        box_w = abs(rotated_bbox_x[3] - rotated_bbox_x[0]) / w
        box_y = abs(rotated_bbox_y[3] - rotated_bbox_y[0]) / w
        rotated_bboxes.append([xmid, ymid, box_w, box_y])


    print(rotated_bboxes)

    return img, rotated_bboxes


# flip
def flip_pic_bboxes(img, bboxes):
    '''
    参考：https://blog.csdn.net/jningwei/article/details/78753607
    镜像后的图片要包含所有的框
    输入：
        img：图像array
        bboxes：该图像包含的所有boundingboxs,一个list,每个元素为[x_min, y_min, x_max, y_max],要确保是数值
    输出:
        flip_img:镜像后的图像array
        flip_bboxes:镜像后的bounding box的坐标list
    '''
    # ---------------------- 镜像图像 ----------------------
    import copy
    flip_img = copy.deepcopy(img)
    if random.random() < 0.5:
        horizon = True
    else:
        horizon = False
    h, w, _ = img.shape
    if horizon:  # 水平翻转
        flip_img = cv2.flip(flip_img, -1)
    else:
        flip_img = cv2.flip(flip_img, 0)
    # ---------------------- 矫正boundingbox ----------------------
    flip_bboxes = list()
    for bbox in bboxes:
        x_min = bbox[0]
        y_min = bbox[1]
        x_max = bbox[2]
        y_max = bbox[3]
        if horizon:
            flip_bboxes.append([w - x_max, y_min, w - x_min, y_max])
        else:
            flip_bboxes.append([x_min, h - y_max, x_max, h - y_min])

    return flip_img, flip_bboxes