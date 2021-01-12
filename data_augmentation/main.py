import data_augmentation
import cv2
import os
from tqdm import tqdm


def process_with_choice(user_choice, img, bboxes, rotate_degrees):
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
    # rotate_img_bboxes
    elif user_choice == 4:
        img, bboxes = data_augmentation.rotate_img_bboxes(img, bboxes, rotate_degrees)
    # flip_pic_boxes
    elif user_choice == 5:
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
            bbox.append(float(coordinate.strip("\n")))     # remove \n
        bbox_type.append(int(bbox[0]))     # int to avoid 1.0 situations
        bboxes.append(bbox[1:])     # seperate bbox_type and bboxes
    f.close()

    return img, bbox_type, bboxes


def write(dir, img_name, txt_name, img, bbox_type, bboxes):
    cv2.imwrite(dir + "/" + img_name, img)     # write img
    i = 0
    f = open(dir + "/" + txt_name, "w+")     # write txt
    while i < len(bbox_type):
        f.write(str(bbox_type[i]) + " ")
        for coordinate in bboxes[i]:
            f.write(str(coordinate) + " ")
        f.write("\n")
        i += 1
    f.close()


def show_img_with_bbox(img, bboxes):
    h, w = img.shape[:2]     # get height and width
    for bbox in bboxes:
        flag = True     # differentiate beetween x and y
        for coordinate in bbox:
            if flag:
                bbox[bbox.index(coordinate)] = coordinate * w     # turn unit to pixels
                flag = False
            else:
                bbox[bbox.index(coordinate)] = coordinate * h
                flag = True
        xmin, ymin = int(bbox[0] - bbox[2] / 2), int(bbox[1] - bbox[3] / 2)     # get two diagonal points
        xmax, ymax = int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)     # draw rectangle
    cv2.imshow("jpg", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    # user inputs
    origin_dir = "E:/apple_quality_screening_release/data_augmentation_origin"
    saving_dir = "E:/apple_quality_screening_release/data_augmentation_destination"
    choices = ["crop_img_bboxes", "shift_pic_bboxes", "alterLight", "addNoise", "rotate_img_bboxes", "flip_pic_bboxes"]
    user_choice = 5
    rotate_degrees = 90

    print("reading from " + origin_dir)
    print("saving to " + saving_dir)
    print("performing " + choices[user_choice])

    # read all jpg under origin directory
    for img_name in tqdm(os.listdir(origin_dir)):
        if img_name.endswith(".jpg"):
            txt_name = img_name.split(".", -1)[0] + ".txt"

            # read img and txt
            img, bbox_type, bboxes = read(origin_dir, img_name, txt_name)
            print("data read from ", img_name, "&", txt_name)

            # show_img_with_bbox(img, bboxes)

            # alter img, and bboxes
            img, bboxes = process_with_choice(user_choice, img, bboxes, rotate_degrees)
            print("image processed")

            # show_img_with_bbox(img, bboxes)

            # write img and txt into saving directory
            write(saving_dir, img_name, txt_name, img, bbox_type, bboxes)
            print("image saved to saving directory")


main()
