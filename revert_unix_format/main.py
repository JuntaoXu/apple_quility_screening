import os
import sys


def main(file_dir, cmd):
    for filename in os.listdir(file_dir):
        print(filename)
        if filename.endswith(".txt"):
            f = open(file_dir + filename, "w")
            for line in f:
                sys.stdout.write, (line[:-2] + '/n')

file_path = "D:/darknet-master/apple_quality_screening_release/data_augmentation_origin/"
cmd = "python -c " + "import sys; map(sys.stdout.write, (l[:-2] + '/n' for l in sys.stdin.readlines())) "
print(cmd)

main(file_path, cmd)