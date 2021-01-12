import os
import shutil
from tqdm import tqdm


def rename_file(dir, dstdir, i):
    for filename in tqdm(os.listdir(dir)):
        if filename.endswith(".jpg"):
            shutil.copy(dir + "/" + filename, dstdir + "/" + str(i) + ".jpg")
            shutil.copy(dir + "/" + filename.split(".", -1)[0] + ".txt", dstdir + "/" + str(i) + ".txt")
            # print(file + "renamed as " + str(i) + ".jpg")
            i += 1


if __name__ == '__main__':
    i = 3709   # new file will be named as number.jpg starting from 0
    dir = "E:/apple_quality_screening_release/data_augmentation_destination"     # from
    dstdir = "E:/apple_quality_screening_release/v2.2/data"     # to
    rename_file(dir, dstdir, i)

