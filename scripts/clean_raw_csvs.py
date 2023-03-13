from datetime import datetime
from genericpath import isfile
from os import listdir, remove
import sys
from os.path import exists, join
import fix_inconsistent_csv

raw_path = 'raw'

# Clean all raw files first
for f in listdir(raw_path):
    if not isfile(join(raw_path, f)) or f.endswith('_fixed.csv'):
        continue
    if f.endswith('.csv'):
        new_file_name = join(raw_path, f.replace('.csv', '_fixed.csv'))
        print(f'Cleaning {f}')
        fix_inconsistent_csv.fix_inconsistent_csv(join(raw_path, f), new_file_name)

cleaned_path = 'cleaned'

# List all files in folder
files = [f for f in listdir(raw_path) if isfile(join(raw_path, f)) and f.endswith('_fixed.csv')]
d = {}
for file in files:
    temp_name = file.replace('enrollment_', '').replace('_fixed.csv', '')
    time = datetime.strptime(temp_name[0:temp_name.rindex('_')], '%Y-%m-%dT%H_%M_%S')
    d[time] = file
times = sorted(list(d.keys()))

# Merge the files together
init = False
with open(join(cleaned_path, 'enrollment.csv'), 'w') as f:
    for time in times:
        file = d[time]
        with open(join(raw_path, file), 'r') as g:
            lines = g.readlines()

            if len(lines) == 0:
                continue

            if init:
                lines.pop(0)
            else:
                f.write(lines[0])
                init = True
                lines.pop(0)

            for line in lines:
                f.write(line)

# And then delete the fixed files from the raw directory
for file in files:
    print(f'Deleting {file}')
    remove(join(raw_path, file))
