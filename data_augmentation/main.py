import data_augmentation
import cv2
import os
from tqdm import tqdm


def process_with_choice(user_choice, img, bboxes):
    # crop_img_bboxes
    if user_choice == 0:
        img, bboxes = data_augmentation.crop_img_bboxes(img, bboxes)
    # shift_pic_bboxes
    elif user_choice == 1:
        img, bboxes = data_augmentation.shift_pic_bboxes(img, bboxes)
    # alterLight
    elif user_choice == 2:
        img = data_augmentation.alterLight(img)
    # addNoise
    elif user_choice == 3:
        img = data_augmentation.addNoise(img)
    # rotate_clockwise_90
    elif user_choice == 4:
        img, bboxes = data_augmentation.rotate_clockwise_90(img, bboxes)
    # rotate_anticlockwise_90
    elif user_choice == 5:
        img, bboxes = data_augmentation.rot_anticlockwise_90(img, bboxes)
    # flip_pic_bboxes
    elif user_choice == 6:
        img, bboxes = data_augmentation.flip_pic_bboxes(img, bboxes)

    return img, bboxes


def read(dir, pic_name, txt_name):
    img = cv2.imread(dir + "/" + pic_name)
    f = open(dir + "/" + txt_name, "r")
    bbox_type = []
    bboxes = []
    for line in f:
        bbox = []
        for coordinate in line.split(" "):
            bbox.append(float(coordinate.strip("\n")))
        bbox_type.append(int(bbox[0]))
        bboxes.append(bbox[1:])
    f.close()

    return img, bbox_type, bboxes


def write(dir, img_name, txt_name, img, bbox_type, bboxes):
    cv2.imwrite(dir + "/" + img_name, img)
    i = 0
    f = open(dir + "/" + txt_name, "w+")
    while i < len(bbox_type):
        f.write(str(bbox_type[i]) + " ")
        for coordinate in bboxes[i]:
            f.write(str(coordinate) + " ")
        f.write("\n")
        i += 1
    f.close()


def main():
    origin_dir = "E:/apple_quality_screening_release/data_augmentation_origin"
    saving_dir = "E:/apple_quality_screening_release/data_augmentation_destination"
    try:
        os.chdir(origin_dir)
        os.chdir(saving_dir)
    except:
        print("input directory not found")
        exit()

    choices = ["crop_img_bboxes", "shift_pic_bboxes", "alterLight", "addNoise", "rotate_img_bboxes", "flip_pic_bboxes"]
    user_choice = 4

    if user_choice in [0, 1, 2, 3, 4, 5, 6]:
        print("Both input valid")
    else:
        print("invalid input")
        exit()

    for img_name in tqdm(os.listdir(origin_dir)):
        if img_name.endswith(".jpg"):
            txt_name = img_name.split(".", -1)[0] + ".txt"
            img, bbox_type, bboxes = read(origin_dir, img_name, txt_name)
            # cv2.imshow("jpg", img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # print(bbox_type)
            # print(bboxes)
            img, bboxes = process_with_choice(user_choice, img, bboxes)
            cv2.imshow("jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print(bbox_type)
            print(bboxes)
            write(saving_dir, img_name, txt_name, img, bbox_type, bboxes)


main()
