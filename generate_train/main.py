import os


def generate_txt(p_dir, train_dir):
    f = open(train_dir + "train.txt", "w+")
    for file in os.listdir(p_dir):
        if file.endswith(".jpg"):
            f.write(p_dir + file + "\n")
    f.close()

picture_dir = "E:/apple_quality_screening_release/v2.2/data/"
train_file_location = "E:/apple_quality_screening_release/v2.2/"
generate_txt(picture_dir, train_file_location)
