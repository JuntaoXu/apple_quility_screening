import os
from tqdm import tqdm


def main(file_origin, file_destination):
    for filename in tqdm(os.listdir(file_origin)):
        print("file " + filename + "altered to unix format")
        if filename.endswith(".txt"):
            f = open(file_origin + filename, "rb")
            g = open(file_destination + filename, "wb")
            for line in f:
                g.write(line[:-3] + line[-1:])
            f.close()
            g.close()

file_origin = "D:/darknet-master/apple_quality_screening_release/data_augmentation_origin/"
file_destination = "D:/darknet-master/apple_quality_screening_release/data_augmentation_destination/"

main(file_origin, file_destination)