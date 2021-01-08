import data_augmentation
import cv2
import os
from tqdm import tqdm


def read(dir):
    for name in tqdm(os.listdir(dir)):
        if name.endswith(".jpg"):
            print("name for img is " + name)
            img = cv2.imread(dir + "/" + name)
            # cv2.imshow("jpg", img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            try:
                txt_content = []
                print("name for txt is " + name.split(".", -1)[0] + ".txt")
                f = open(dir + "/" + name.split(".", -1)[0] + ".txt")
                for line in f:
                    txt_content.append(line)
                return img, txt_content
            except:
                print("cannot find correspondent txt for image")


def main():
    origin_dir = "E:/apple_quality_screening_release/v2.2/test_origin"
    saving_dir = "E:/apple_quality_screening_release/v2.2/test_destination"
    try:
        os.chdir(origin_dir)
        os.chdir(saving_dir)
    except:
        print("input directory not found")
        main()
    read(origin_dir)

    print("pick the strategy of data augmentation")
    choices = ["crop_img_bboxes", "shift_pic_bboxes", "alterLight", "addNoise", "rotate_img_bboxes", "flip_pic_bboxes"]
    i = 0
    for choice in choices:
        print("enter " + str(i) + " for " + choice)
        i += 1

    user_choice = input("which to perform: ")

    # crop_img_bboxes
    data_augmentation.crop_img_bboxes()
    # shift_pic_bboxes
    data_augmentation.shift_pic_bboxes()
    # alterLight
    data_augmentation.alterLight()
    # addNoise
    data_augmentation.addNoise()
    # rotate_img_boxes
    data_augmentation.rotate_img_bboxes()
    # flip_pic_bboxes
    data_augmentation.flip_pic_bboxes()


main()
