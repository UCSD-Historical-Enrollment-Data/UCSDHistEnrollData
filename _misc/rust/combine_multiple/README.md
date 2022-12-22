# Note
Due to restructuring, this project is no longer in use.

# CombineMultiple
This program combines all [*real cleaned/processed CSV files*](https://github.com/ewang2002/UCSDHistEnrollData#types-of-csv-files) for each course from multiple terms into *one* cleaned/processed CSV file.

For example, let's suppose we have `CSE 11.csv` for the terms FA22UG, FA22NS, and FA22A. That is, we might have the following files:
- `FA22UG/raw/CSE 11.csv`
- `FA22NS/raw/CSE 11.csv`
- `FA22A/raw/CSE 11.csv`

Let's suppose we want to merge these CSV files into one file and put the result in the term folder `FA22`. With this executable, we can combine these three CSV files into one CSV file and put it into said term folder.

## Usage
```
./combine_multiple <term1> <term2> [term3] ... [termN] <target>
```
where
- `<term1>` and `<term2>` are required terms, and
- `[term3]` and any other terms are optional terms.
- `<target>` is the target term. This must be the last argument.

This should be executed in the project's root directory.

## Prerequisites for Program
In order to run this program, the term folders that you choose must meet the following requirements:
- They must each be for the same term.
    - For example, trying to combine data for the Fall 2022 and Spring 2022 term folders **will** lead to undesirable results.
- The data from the real cleaned/processed CSV files must *not* overlap in content or time.
    - For example, if the `CSE 11.csv` file from the `FA22UG` and `FA22NS` term folders had data that overlapped in time (e.g., both CSV files had an entry with the same time), combination of the data will result in duplicate data in the final CSV file.
    - As a remark, this program does attempt to remove duplicates; however, it will not remove duplicates if the data from the duplicate entries differ. 
    - As a remark, the easiest way to check if there are duplicates is to see if there exists duplicate *raw* CSV files (in the `raw` folder) for any two terms.
- The data must be consistent.
    - For example, if `FA22UG` had undergraduate *and* graduate data, and `FA22NS` only had undergraduate, this will lead to incomplete graphs.

Note that the program does not crash if any of the prerequisites aren't met. At most, a warning will be emitted. Thus, it is your responsibility to check and ensure that the prerequisites are met.