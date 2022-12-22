[← Go Back](https://github.com/ewang2002/UCSDHistEnrollData)

# Setup
Below are instructions on how you can generate your own plots.

### Required & Optional Software
Make sure to get the latest versions of the required software.

#### Required
- [Python](https://www.python.org/).
- [PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell)

#### Optional
- [git](https://git-scm.com/).

### Instructions
1. Obtain a copy of the following files from this repository:
    - `clean_raw_csvs.py`
    - `enroll_data_cleaner.py`
    - `fix_inconsistent_csv.py`
    - `list_all_files.ps1`
    - `plot.py`
    - `run.ps1`

2. Download, or clone, one of the data repositories. You can find a link to each data repository in the main README file in this repository.

3. Next, put all the files mentioned in the first step, **except** the `run.ps1` file, in the root directory of the data repository folder. Put the `run.ps1` file outside of the data repository folder. 

    After completing this step, you should have a file structure that looks something like this: 


    ```
    Desktop
    ├─ run.ps1
    └─ 2022Fall (Data Repository)
        ├─ clean_raw_csvs.py
        ├─ enroll_data_cleaner.py
        ├─ fix_inconsistent_csv.py
        ├─ list_all_files.ps1
        ├─ plot.py
        |  (remaining items are from the repository)
        ├─ raw
        ├─ overall
        ├─ section
        .
        .
        .
        └─ plotconfig.txt
        
    ```

4. Install the relevant Python dependencies (`pandas`, `seaborn`, `matplotlib`). A `requirements.txt` file is provided in this directory that you can use to help you install those dependencies.

5. Make the appropriate modifications to the files.
    - In [`plot.py`](https://github.com/ewang2002/UCSDHistEnrollData/blob/master/plot.py), you should modify the value for `PROCESS_COUNT` if you're planning on running this program on a significantly weaker system (e.g., instead of `10`, use a value like `5`). If you're running `plot.py` in an environment that doesn't support running multiple processes, you will need to make the appropriate modifications to the code.
    - Make adjustments to the `plotconfig.txt` file as needed.

6. Finally, run `run.ps1` to start the cleaning & processing & plotting process.

These instructions are not comprehensive, nor were they meant to be; thus, if you need any help, please create an issue [here](https://github.com/ewang2002/UCSDHistEnrollData/issues). 
