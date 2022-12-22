import sys
import os
from os.path import exists, join

if len(sys.argv) != 2:
    print('Usage: create_new_folder.py <folder name>')
    sys.exit(1)

folder_name = sys.argv[1].upper()
if exists(folder_name):
    print(f'{folder_name} already exists.')
    sys.exit(1)

# Create the folders
os.mkdir(folder_name)
os.mkdir(join(folder_name, 'raw'))
os.mkdir(join(folder_name, 'cleaned'))

os.mkdir(join(folder_name, 'overall'))
os.mkdir(join(folder_name, 'plot_overall'))

os.mkdir(join(folder_name, 'section'))
os.mkdir(join(folder_name, 'plot_section'))

# and copy over the config file for plotting
if exists('plotconfig_example.py'):
    with open('plotconfig_example.py', 'r') as g:
        with open(join(folder_name, 'plotconfig.py'), 'w') as f:
            f.write(g.read())
else:
    print('No plotconfig_example.py file found. Please create one manually.')

with open(join(folder_name, 'README.md'), 'w') as r:
    r.write('# Term')

with open(join(folder_name, 'plot_overall', 'README.md'), 'w') as r:
    r.write('This README file is here so that the folder appears on GitHub.')

with open(join(folder_name, 'plot_section', 'README.md'), 'w') as r:
    r.write('This README file is here so that the folder appears on GitHub.')

print('Created new folder successfully.')