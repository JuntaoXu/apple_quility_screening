import data_augmentation
import cv2
import os
from tqdm import tqdm


def process_with_choice(user_choice, img, txt_content):
        # crop_img_bboxes
        if user_choice == 0:
            data_augmentation.crop_img_bboxes()
        # shift_pic_bboxes
        elif user_choice == 1:
            data_augmentation.shift_pic_bboxes()
        # alterLight
        elif user_choice == 2:
            data_augmentation.alterLight()
        # addNoise
        elif user_choice == 3:
            data_augmentation.addNoise()
        # rotate_img_boxes
        elif user_choice == 4:
            data_augmentation.rotate_img_bboxes()
        # flip_pic_bboxes
        elif user_choice == 5:
            data_augmentation.flip_pic_bboxes()


def read(dir, user_choice):
    for name in tqdm(os.listdir(dir)):
        if name.endswith(".jpg"):
            img = cv2.imread(dir + "/" + name)
            # cv2.imshow("jpg", img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            f = open(dir + "/" + name.split(".", -1)[0] + ".txt")
            txt_content = []
            for line in f:
                bbox = []
                for coordinate in line.split(" "):
                    bbox.append(coordinate.strip("\n"))
                txt_content.append(bbox)
            return img, txt_content


def main():
    origin_dir = "E:/apple_quality_screening_release/v2.2/test_origin"
    saving_dir = "E:/apple_quality_screening_release/v2.2/test_destination"
    try:
        os.chdir(origin_dir)
        os.chdir(saving_dir)
    except:
        print("input directory not found")
        exit()

    choices = ["crop_img_bboxes", "shift_pic_bboxes", "alterLight", "addNoise", "rotate_img_bboxes", "flip_pic_bboxes"]
    user_choice = 0

    if user_choice in [0, 1, 2, 3, 4, 5]:
        print("Both input valid")
    else:
        print("invalid input")
        exit()

    img, txt_content = read(origin_dir, user_choice)
    print(txt_content)


main()
