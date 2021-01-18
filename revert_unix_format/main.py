import os

# dir
route = "G:/apple_quality_screening/apple_quality_screening_release/v2.2-tiny-linux/data"
for root, dirs, files in os.walk(route):
    for name in files:
        # file type
        if name.endswith(".txt") == "txt":
            # combine dir with filename
            catalog = os.path.join(root, name)
            # replace all change line with "\n"
            fp = open(catalog, "rU+")
            # read file and save
            strings = fp.read()
            fp.close()
            # write file with binary
            fp1 = open(catalog, "wb")
            fp1.seek(0)
            fp1.write(strings)
            fp1.flush()
            fp1.close()
