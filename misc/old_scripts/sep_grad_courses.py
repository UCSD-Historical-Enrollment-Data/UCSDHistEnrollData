from genericpath import isfile
from os import listdir
from os.path import join
import sys

def get_base_file_name(f: str) -> str:
    """
    Get the base file name. This will strip off the term
    and the extension.

    For example, if the file name was
        enrollment_2022-08-16T04_23_03_FA22NS.csv
    then
        enrollment_2022-08-16T04_23_03
    will be returned

    :param f: The file name to get the base name from
    :return: The base file name
    """

    # Get last index of '_'
    last_underscore = f.rfind('_')
    return f[:last_underscore]

if len(sys.argv) != 4:
    print("Usage: sep_grad_courses.py <base folder> <ug folder> <g folder>")
    sys.exit(1)

# base_folder is where we'll take the raw CSV files from
base_folder = sys.argv[-3].upper()
# ug_folder is where we'll put the undergrad courses
ug_folder = sys.argv[-2].upper()
# g_folder is where we'll put the grad courses
g_folder = sys.argv[-1].upper()

# Output folders
base_raw_path = join(base_folder, 'raw')
ug_raw_path = join(ug_folder, 'raw')
g_raw_path = join(g_folder, 'raw')

# List all files in the base folder
for f in listdir(base_raw_path):
    print(f"Processing: {f}")
    this_file = join(base_raw_path, f)
    if not isfile(this_file):
        continue
    if f.endswith('_fixed.csv'):
        continue 

    base_name = get_base_file_name(f)
    new_ug_name = f"{base_name}_{ug_folder}.csv"
    new_g_name = f"{base_name}_{g_folder}.csv"

    # Get file contents, begin iteration
    with open(this_file, 'r') as g:
        grad_data = ""
        undergrad_data = ""

        # Note that each line in the all_lines list will
        # have an implicit \n at the end
        all_lines = g.readlines()
        
        # Read first line since this is the CSV header
        line = all_lines[0]
        grad_data = line
        undergrad_data = line
        
        # Iterate through the rest of the lines
        for line in all_lines[1:]:
            course_info = line.split(',')[1]
            course_num = course_info.split(' ')[1]
            # Remove all non-numeric characters from the course number
            course_num = int("".join(c for c in course_num if c.isdigit()))

            # if it's a grad course...
            if course_num >= 200:
                grad_data += line
            else:
                undergrad_data += line

        # Write the undergrad and grad data to their respective files
        with open(join(ug_raw_path, new_ug_name), 'w') as ug:
            ug.write(undergrad_data)
        with open(join(g_raw_path, new_g_name), 'w') as g:
            g.write(grad_data)