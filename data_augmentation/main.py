import data_augmentation
import cv2
import os
from tqdm import tqdm


def main():
    origin_dir = input("original picture and txt located in directory: ")
    saving_dir = input("save augmented picture and txt to directory: ")
    try:
        os.chdir(origin_dir)
        os.chdir(saving_dir)
    except:
        print("input directory not found")
        main()

    print("please pick the strategy of data augmentation")
    choices = ["crop_img_bboxes", "shift_pic_bboxes", "alterLight", "addNoise", "rotate_img_bboxes", "flip_pic_bboxes"]
    i = 0
    for choice in choices:
        print("enter " + str(i) + " for " + choice)
        i += 1


if __name__ == '__main__':
    print('here')
    main()
