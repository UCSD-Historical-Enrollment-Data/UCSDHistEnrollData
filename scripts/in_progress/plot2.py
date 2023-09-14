from datetime import datetime, timedelta
from os import listdir, mkdir
from os.path import exists, join
import sys
from typing import List, Tuple, TypeVar
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from math import floor
from multiprocessing import Process
import gc

# Settings for input/output, basic plot stuff
GENERAL_SETTINGS = {
    'id': 'general',
    'overall_plot_folder': 'plot_overall',
    'section_plot_folder': 'plot_section',

    'figure_size': (17, 7),
    'num_ticks': 50
}

WIDE_SETTINGS = {
    'id': 'wide',
    'overall_plot_folder': 'plot_overall_wide',
    'section_plot_folder': 'plot_section_wide',

    'figure_size': (60, 15),
    'num_ticks': 200
}

OVERALL_FOLDER = 'overall'
SECTION_FOLDER = 'section'

# For the plotconfig.py file
MARKERS = "markers"
MARKER_DATES = 'd'
MARKER_TIME = 't'
LINE_STYLE = 'l'
LINE_COLOR = 'c'
NAME_OF_MARKER = 'n'
CONFIG_SETTINGS = 'settings'
SHADE = 's'
MARKER_ID = 'i'

REGIONS = "regions"
START_ID = 's'
END_ID = 'e'
REGION_NAME = 'n'
REGION_COLOR = 'c'
R_HIDE = 'h'

# Multiprocessing options
CHUNK_SIZE = 20
WIDE_CHUNK_SIZE = 10
PROCESS_COUNT = 10

T = TypeVar('T')
def subsets_with_limits(arr: List[T], num_subsets: int, max_per_elem: int) -> List[List[T]]:
    arr.reverse()
    subsets = []
    len_to_use = max(0, len(arr) - max_per_elem * num_subsets)
    idx = 0
    while len(arr) > len_to_use:
        if idx < len(subsets):
            subsets[idx].append(arr.pop())
            idx = (idx + 1) % num_subsets
            continue 

        subsets.append([arr.pop()])
        idx = (idx + 1) % num_subsets
    
    arr.reverse()
    return subsets

def plot_group(group_num: int, files_to_plot: List[str], \
               from_folder: str, out_folder: str, settings, config):
    
    completed = 0
    for file in files_to_plot:
        df = pd.read_csv(join(from_folder, file))
        # Map the time (e.g., 2023-05-25T01:14:46) to a datetime object
        # supported by pandas
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S')

        # Set the figure size for the final plot
        plt.figure(figsize=settings['figure_size'])

        sns.lineplot(data=df, x='time', y='total', color='purple', label='Total Seats', linestyle='--', linewidth=4)
        sns.lineplot(data=df, x='time', y='waitlisted', color='blue', label='Waitlisted', linewidth=1)
        sns.lineplot(data=df, x='time', y='enrolled', color='red', label='Enrolled', linewidth=2)
        max_y = max(df['enrolled'].max(), df['total'].max(), df['waitlisted'].max())

        plot = plt.gca()
        # Modify plot properties to make it more readable
        title = file.replace('.csv', '')
        if '_' in title:
            course, section = title.split('_')
            title = f'{course}, Section {section}'
        
        plot.set_title(title + f' ({config[CONFIG_SETTINGS]["termName"]})')
        plot.set_xlabel('Time')
        plot.set_ylabel('Seats')
        plot.grid(True)
        plot.margins(0)

        # Set bottom-left corner to (0, 0)
        plt.ylim(ymin=0, ymax=max(1.05*max_y, 1))

        # Set the x-axis to be more readable (show once per day)
        loc = mdates.AutoDateLocator(interval_multiples=True)
        loc.intervald[mdates.DAILY] = [max(floor(len(df) / settings['num_ticks']), 1)]
        plot.xaxis.set_major_locator(loc)
        plot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # To make the x-axis more readable, purposely hide some dates and then
        # adjust the labels appropriately
        plt.setp(plot.xaxis.get_majorticklabels(), rotation=45, ha="right")

        # https://matplotlib.org/2.0.2/users/legend_guide.html
        plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
        # Adjusts the padding
        plt.tight_layout()
        # Then, saves the figure and closes it to save memory
        fig = plot.get_figure()
        fig.savefig(join(out_folder, file.replace('.csv', '')))
        # Clear the plot, close it, and clear the memory
        plot.cla()
        plt.clf()
        plt.cla()
        plt.close('all')
        del plot
        del fig
        del df
        gc.collect()
        completed += 1
        print(f"\t\t[{group_num}] Finished {file} (Completed {completed}/{len(files_to_plot)}).")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: plot.py <'s', 'o', 'sw', 'ow'>")
        print("\twhere the argument is one of:")
        print("\t\t's' (section)")
        print("\t\t'o' (overall)")
        print("\t\t'sw' (section, wide display)")
        print("\t\t'ow' (overall, wide display)")
        sys.exit(1)

    # Get the type of data to process
    data_type = sys.argv[-1]
    if data_type not in ['s', 'o', 'sw', 'ow']:
        print(f"Invalid data type '{data_type}' - must be one of:")
        print("\t's' (section)")
        print("\t'o' (overall)")
        print("\t'sw' (section, wide display)")
        print("\t'ow' (overall, wide display)")
        sys.exit(1)

    # Get config file
    try:
        with open('plotconfig.txt', 'r') as f:
            config = eval(f.read())
    except:
        print(f'This folder does not contain a plotconfig.txt file. Please set one up and then try again.')
        exit(1)

    if data_type in ['s', 'o']:
        settings_obj = GENERAL_SETTINGS
        chunk_size = CHUNK_SIZE
    elif data_type in ['sw', 'ow']:
        settings_obj = WIDE_SETTINGS
        chunk_size = WIDE_CHUNK_SIZE

    plot_folder = join(settings_obj['overall_plot_folder'] if data_type in ['o', 'ow'] else settings_obj['section_plot_folder'])
    if not exists(plot_folder):
        mkdir(plot_folder)

    in_folder = join(OVERALL_FOLDER if data_type in ['o', 'ow'] else SECTION_FOLDER)
    all_files = listdir(in_folder)

    # If we're working with sections, we only want the files that appear more than once
    # Categorize each file by the class that they represent.
    if data_type == 's':
        # The key is the course (e.g. CSE 100.csv) and the value is a list
        # of all sections (e.g. CSE 100_A.csv)
        file_secs = {}
        for file in all_files:
            f_name = file.split('_')[0]
            if f_name not in file_secs:
                file_secs[f_name] = [file]
            else:
                file_secs[f_name].append(file)

        all_files = []
        for f_name in file_secs:
            if len(file_secs[f_name]) > 1:
                all_files += file_secs[f_name]

    print(f'Processing {len(all_files)} files into chunks of {chunk_size} files each.')
    print(f'\tWide?           {data_type == "sw" or data_type == "ow"}')
    print(f'\tInput Folder:   {in_folder}')
    print(f'\tPlot Folder:    {plot_folder}')
    print(f'\tProcesses:      {PROCESS_COUNT}')

    len_of_files = len(all_files)
    completed = 0
    while len(all_files) > 0:
        files_to_process = subsets_with_limits(all_files, PROCESS_COUNT, chunk_size)
        processes = []
        # Limit ourselves to PROCESS_COUNT processes, or else we might
        # end up crashing the host device with too many processes.
        for (i, chunk) in enumerate(files_to_process):
            print(f'Starting process {i} (with count {len(chunk)}).')
            # Create a process to process the chunk
            p = Process(target=plot_group, args=(i, \
                chunk, \
                in_folder, \
                plot_folder, \
                settings_obj, \
                config))
            p.start()
            processes.append(p)
        
        # Wait for all processes to finish
        for p in processes:
            p.join()
        completed += sum(len(x) for x in files_to_process)
        print(f'\t\tCompleted {completed}/{len_of_files} files ({len(all_files)} left).')