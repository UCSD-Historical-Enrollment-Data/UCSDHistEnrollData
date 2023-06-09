import os

def get_all_files(dir, target):
    res = ""
    for file in os.listdir(dir):
        # check if the file isa ctually a file
        if not os.path.isfile(os.path.join(dir, file)):
            continue

        # check if file has extension .csv
        if not file.endswith(".csv"):
            continue

        # append file name to res, removing the extension
        res += file[:-4] + "\n"

    # write res to file with encoding UTF-8 
    with open(target, "w", encoding="utf-8") as f:
        f.write(res)


get_all_files("overall", "all_courses.txt")
get_all_files("section", "all_sections.txt")