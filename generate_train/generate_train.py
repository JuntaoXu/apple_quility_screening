import os


def generate_txt(p_dir, train_dir):
    f = open(train_dir + "train.txt", "w+")
    for file in os.listdir(p_dir):
        if file.endswith(".jpg"):
            f.write(p_dir + file + "\n")
    f.close()


if __name__ == '__main__':
    picture_dir = 'F:/apple_quiality_filter/data/12-12/data/'
    train_file_location = "F:/apple_quiality_filter/data/12-12/"
    generate_txt(picture_dir, train_file_location)
