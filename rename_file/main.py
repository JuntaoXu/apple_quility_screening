import os
import shutil
from tqdm import tqdm


def rename_file(dir, dstdir):
    i = 3397     # new file will be named as number.jpg starting from 0
    for file in tqdm(os.listdir(dir)):
        if file.endswith(".jpg"):
            shutil.copy(dir + "/" + file, dstdir + "/" + str(i) + ".jpg")
            # print(file + "renamed as " + str(i) + ".jpg")
            i += 1


if __name__ == '__main__':
    dir = "F:/apple_quiality_filter/data/12-9"     # from
    dstdir = "E:/apple_quality_screening_release/v2.2/data"     # to
    rename_file(dir, dstdir)

