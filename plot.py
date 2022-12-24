from datetime import datetime, timedelta
from os import listdir, mkdir
from os.path import exists, join
import sys
from typing import List, Tuple, TypeVar
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

FSP_SETTINGS = {
    'id': 'fsp',
    'overall_plot_folder': 'plot_overall_fsp',
    'section_plot_folder': 'plot_section_fsp',

    'figure_size': (17, 7),
    'num_ticks': 50
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

def get_version_of_config(config) -> int:
    return config['version'] if 'version' in config else 1

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

def process_overall(num: int, files: List[str], from_folder: str, out_folder: str, settings, config):
    """
    Processes the folder containing overall data.
    :param num: The process label number (just for identification).
    :param files: List of files to process
    :param from_folder: Folder to read from
    :param out_folder: Folder to write to
    :param settings: Settings to use
    :param config: The configuration object, from the plotconfig.py file.
    """

    # Uncomment if you want to skip the images that were already generated
    # temp_files = [f for f in listdir(out_folder) if exists(join(out_folder, f))]
    completed = 0
    for file in files:
        print(f"\t[{num}] Processing {file}.")
        
        #if file.replace('csv', 'png') in temp_files: 
        #    completed += 1
        #    print(f"\t\t[{num}] Skipped {file} (Completed {completed}/{len(files)}).")
        #    continue 

        # Read in our CSV file
        df = pd.read_csv(join(from_folder, file))
        if settings['id'] == 'fsp' and get_version_of_config(config) == 1:
            if len(config[MARKERS]) == 0 or "end" not in config[MARKERS][-1][NAME_OF_MARKER].lower():
                completed += 1
                print(f'\t\t[{num}] Skipped {file} due to no end marker despite fsp (Completed {completed}/{len(files)}).')
                continue 


            end_date_str = config[MARKERS][-1][MARKER_DATES][-1]
            # Parse this date
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
            # Filter all rows in df so that the date is earlier than the end date, noting that
            # the date in df['time'] needs to be converted first
            df = df[df['time'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S") < end_date)]

        if len(df.index) == 0:
            completed += 1
            print(f"\t\t[{num}] Skipped {file} (Completed {completed}/{len(files)}).")
            continue 

        # Adjust the figure so it's big enough for display
        plt.figure(figsize=settings['figure_size'])

        max_y = 0
        # Plot the number of available & waitlisted seats
        if config[CONFIG_SETTINGS]['showTotal']:
            sns.lineplot(data=df, x='time', y='total', color='purple', label='Total Seats', linestyle='--', linewidth=4)
            max_y = df['total'].max()

        sns.lineplot(data=df, x='time', y='waitlisted', color='blue', label='Waitlisted', linewidth=1)
        max_y = max(max_y, df['waitlisted'].max())
        
        if config[CONFIG_SETTINGS]['useEnrolledTtl']:
            sns.lineplot(data=df, x='time', y='enrolled', color='red', label='Enrolled', linewidth=2)
            max_y = max(df['enrolled'].max(), max_y)
        else:
            sns.lineplot(data=df, x='time', y='available', color='red', label='Available', linewidth=2)
            max_y = max(df['available'].max(), max_y)
        

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
        plt.xlim(xmin=0)
        plt.ylim(ymin=0, ymax=max(1.05*max_y, 1))

        # To make the x-axis more readable, purposely hide some dates and then
        # adjust the labels appropriately
        plt.setp(plot.xaxis.get_majorticklabels(), rotation=45, ha="right")
        # We want NUM_TICKS ticks on the x-axis
        plot.xaxis.set_major_locator(ticker.MultipleLocator(max(floor(len(df) / settings['num_ticks']), 1)))
        plot.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        if config[CONFIG_SETTINGS]['useMarkers']: 
            all_dates = df['time'].tolist()
            # map all dates in all_dates to a tuple of string date and datetime object
            all_dates: Tuple[str, datetime] = list(map(lambda x: (x, datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")), all_dates))
            if get_version_of_config(config) == 1:
                p_max = 2 if config[CONFIG_SETTINGS]['isNormal'] else 1

                spans = []
                spans2 = []
                seen_grades = set()
                
                for marker in config[MARKERS]:
                    # index [0, 1] -> 0 = first pass, 1 = second pass
                    for p in range(0, p_max):
                        hr = marker[MARKER_TIME]
                        date = marker[MARKER_DATES][p]
                        # find the first date in all_dates whose date is equal to date
                        # and has the closest hour to hr
                        axis_date = list(filter(lambda x: x[1].strftime("%Y-%m-%d") == date and (x[1].hour == hr or\
                            x[1].hour == hr + 1 or x[1].hour == hr + 2 or x[1].hour == hr + 3), all_dates))
                        if len(axis_date) == 0:
                            continue

                        if marker[SHADE]:
                            (spans if p == 0 else spans2).append({
                                'start': axis_date[0][0],
                                'color': marker[LINE_COLOR],
                                'legend': marker[NAME_OF_MARKER],
                            })

                        plt.axvline(x=axis_date[0][0], \
                            color=marker[LINE_COLOR], \
                            linestyle=marker[LINE_STYLE], \
                            label=None if marker[NAME_OF_MARKER] in seen_grades else marker[NAME_OF_MARKER])
                        seen_grades.add(marker[NAME_OF_MARKER])

                # Note that the reason why I didn't just combine the lists is because I don't want to add the "End" from first pass
                # to the graph. 

                seen_shades = set()
                # For first-pass stuff
                for i in range(0, len(spans) - 1):
                    # fill plot between combined_spans[i] and combined_spans[i+1]
                    plt.axvspan(spans[i]['start'], \
                        spans[i+1]['start'], \
                        color=spans[i]['color'], \
                        alpha=0.2, \
                        label=None if spans[i]['legend'] in seen_shades else spans[i]['legend'])
                    seen_shades.add(spans[i]['legend'])

                # For second-pass stuff
                for i in range(0, len(spans2) - 1):
                    # fill plot between combined_spans[i] and combined_spans[i+1]
                    plt.axvspan(spans2[i]['start'], \
                        spans2[i+1]['start'], \
                        color=spans2[i]['color'], \
                        alpha=0.2, \
                        label=None if spans2[i]['legend'] in seen_shades else spans2[i]['legend'])
                    seen_shades.add(spans2[i]['legend'])
            else:
                added_lines = {}
                # First, plot all markers    
                for marker in config[MARKERS]:
                    hr = marker[MARKER_TIME]
                    date = marker[MARKER_DATES]
                    # find the first date in all_dates whose date is equal to date
                    # and has the closest hour to hr
                    axis_date = list(filter(lambda x: x[1].strftime("%Y-%m-%d") == date and (x[1].hour == hr or\
                        x[1].hour == hr + 1 or x[1].hour == hr + 2 or x[1].hour == hr + 3), all_dates))
                    if len(axis_date) == 0:
                        continue
    
                    plt.axvline(x=axis_date[0][0], \
                        color=marker[LINE_COLOR], \
                        linestyle=marker[LINE_STYLE], \
                        label=None if R_HIDE in marker else marker[NAME_OF_MARKER])
                    
                    added_lines[marker[MARKER_ID]] = axis_date[0][0]

                for region in config[REGIONS]:
                    if region[START_ID] not in added_lines or region[END_ID] not in added_lines:
                        continue 

                    start_x = added_lines[region[START_ID]]
                    end_x = added_lines[region[END_ID]]
                    plt.axvspan(start_x, \
                        end_x, \
                        color=region[REGION_COLOR], \
                        alpha=0.2, \
                        label=None if R_HIDE in region else region[NAME_OF_MARKER])

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
        print(f"\t\t[{num}] Finished {file} (Completed {completed}/{len(files)}).")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: plot.py <'s', 'o', 'sw', 'ow', 'sfsp', 'ofsp'>")
        sys.exit(1)

    # Get the type of data to process
    dt = sys.argv[-1]
    if dt not in ['s', 'o', 'sw', 'ow', 'sfsp', 'ofsp']:
        print(f"Invalid data type '{dt}' - must be one of:")
        print("\t's' (section)")
        print("\t'o' (overall)")
        print("\t'sw' (section, wide display)")
        print("\t'ow' (overall, wide display)")
        print("\t'sfsp' (section, first/second-pass only)")
        print("\t'ofsp' (overall, first/second-pass only)")
        sys.exit(1)

    # Get config file
    try:
        with open('plotconfig.txt', 'r') as f:
            config = eval(f.read())
    except:
        print(f'This folder does not contain a plotconfig.txt file. Please set one up and then try again.')
        exit(1)

    chunk_size = CHUNK_SIZE
    if dt in ['s', 'o']:
        settings_obj = GENERAL_SETTINGS
    elif dt in ['sw', 'ow']:
        settings_obj = WIDE_SETTINGS
        chunk_size = WIDE_CHUNK_SIZE
    elif dt in ['sfsp', 'ofsp']:
        settings_obj = FSP_SETTINGS

    if get_version_of_config(config) != 1 and dt in ['sfsp', 'ofsp']:
        print(f"First/second-pass plots are only supported for v1 of the config file.")
        exit(1)

    plot_folder = join(settings_obj['overall_plot_folder'] if dt in ['o', 'ow', 'ofsp'] else settings_obj['section_plot_folder'])
    if not exists(plot_folder):
        mkdir(plot_folder)

    in_folder = join(OVERALL_FOLDER if dt in ['o', 'ow', 'ofsp'] else SECTION_FOLDER)
    all_files = listdir(in_folder)

    # If we're working with sections, we only want the files that appear more than once
    # Categorize each file by the class that they represent.
    if dt == 's':
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

    # Begin running
    print(f'Processing {len(all_files)} files into chunks of {chunk_size} files each.')
    print(f'\tWide?           {dt == "sw" or dt == "ow"}')
    print(f'\tInput Folder:   {in_folder}')
    print(f'\tPlot Folder:    {plot_folder}')
    print(f'\tProcesses:      {PROCESS_COUNT}')
    print(f'\tConfig Version: {get_version_of_config(config)}')

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
            p = Process(target=process_overall, args=(i, \
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
    