import data_augmentation
import cv2
import os
from tqdm import tqdm


def read(dir):
    for name in os.listdir(dir):
        if name.endswith(".jpg"):
            img = cv2.imread(dir + "/" + name)
            cv2.imshow("jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("here")
            try:
                txt = []
                txt_name = img.split(".", 0) + ".txt"
                print(txt_name)
                f = open(dir + txt_name)
                for line in f:
                    txt.append(line)
                    print(line)
                return img, txt
            except:
                print("cannot find correspondent txt for image")


def main():
    origin_dir = input("original picture and txt located in directory: ")
    # saving_dir = input("save augmented picture and txt to directory: ")
    os.chdir(origin_dir)
    try:
        os.chdir(origin_dir)
        # os.chdir(saving_dir)
    except:
        print("input directory not found")
        main()
    read(origin_dir)

    print("please pick the strategy of data augmentation")
    choices = ["crop_img_bboxes", "shift_pic_bboxes", "alterLight", "addNoise", "rotate_img_bboxes", "flip_pic_bboxes"]
    i = 0
    for choice in choices:
        print("enter " + str(i) + " for " + choice)
        i += 1


if __name__ == '__main__':
    main()
