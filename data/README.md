# Data Folder
This repository contains TSV data files that are not necessarily related to enrollment history, but were created because I was able to get enrollment history.

## TSV Files & Structures
Below, you'll find information on what each file represents, along with their structure.


### Schedule TSV Files
TSV files in the `schedules` folder contain information on section schedules (e.g., the professor, meeting times, etc.). The name of the TSV file represents the term that the file is for (e.g., `WI23.tsv` contains section schedules for Winter 2023).

Each TSV file is structured like so:

| Header Name | Header Information | Example |
| ----------- | ------------------ | ------- |
| `subj_course_id` | The course number | CSE 8A |
| `sec_code` | The section code | A01 |
| `sec_id`| The section ID | 090018 |
| `total_seats` | The total number of seats | 125 |
| `meetings` | Information about all associated meetings |

In particular, the data in `meetings` is structured so that each meeting is separated between a vertical bar (i.e., `|`). Each individual meeting will be formatted like so: 

```
<Meeting Code>,<Meeting Days>,<Meeting Time>,<Meeting Room>
```


In particular,
| Meeting Component | Meaning |
| ----------------- | ------- |
| `<Meeting Code>` | The meeting type (e.g., Final Exam, Lecture, etc.). See the [registrar's website](https://registrar.ucsd.edu/StudentLink/instr_codes.html) for all possible meeting codes. |
| `<Meeting Days>` | The days that the meeting will occur. This will either be a string of days (one or more of `M`, `Tu`, `W`, `Th`, `F`, `Sa`, `Su`) or a date (e.g., `2022-12-09`). |
| `<Meeting Time>` | The meeting start and end time. Times are shown in 24-hour format. |
| `<Meeting Room>` | The location where the meeting will occur. |

<details>
<summary>Click here for an example.</summary>
<br> 

For example, consider the meeting
```
LE,MW,12:00 - 12:50,MOS 0113
```
Here, 
- `<Meeting Code>` is `LE`, which stands for lecture.
- `<Meeting Days>` is `MW`, which stands for Monday and Wednesday meetings.
- `<Meeting Time>` is `12:00 - 12:50`, which stands for 12:00 PM to 12:50 PM.
- `<Meeting Room>` is `MOS 0113`, which stands for Mosaic Room 0113.

Thus, a full meeting schedule may look like
```
LE,MW,18:30 - 19:50,CENTR 105|FI,2022-12-05,19:00 - 21:59,CENTR 105|DI,Th,17:00 - 17:50,CENTR 214
```
Here, there are three different types of meeting: a lecture (LE), final exam (FI), and discussion (DI). 

</details>

To see an example of how you might parse this file, see this [TypeScript example](https://github.com/AWaffleInc/rubot/blob/dd42c7afcdf1b6ff451d29d3727e740f15e90f70/src/Data.ts#L76) and [corresponding types declaration](https://github.com/AWaffleInc/rubot/blob/dd42c7afcdf1b6ff451d29d3727e740f15e90f70/src/definitions/MiscInterfaces.ts#L20).

### CAPE TSV File
> **Note**:
> Because CAPE data is not public (you need a UCSD SSO/AD/Business account), the `CAPEs.tsv` file will not be made public. If you are interested in getting this file, please *email* me[^1] using your UCSD account. 

The `CAPEs.tsv` file has basic information about each CAPE entry. In particular, what you see when you search up a professor or class will be what you see in this file. 

The file is structured as follows:

| Header Name     | Header Information | Example |
| --------------- | ------------------ | ------- |
| `instructor`    | The instructor.    | Micciancio, Daniele |
| `sub_course`    | The course number. | CSE 110 |
| `course`        | The name of the course. | Theory of Computation |
| `term`          | The term.          | FA22 |
| `enroll`        | The number of students enrolled. | 77 |
| `evals_made`    | The number of evaluations made. | 21 |
| `rcmd_class`    | The percent of students who recommended the class. | 97.1 |
| `rcmd_instr`    | The percent of students who recommended the instructor. | 96.6 |
| `study_hr_wk`   | The average number of hours spent studying per week. | 8.3 |
| `avg_grade_exp` | The average GPA expected. | 3.59 |
| `avg_grade_rec` | The average GPA received. `-1` corresponds to `N/A` on CAPEs. | 3.55 |

To see an example of how you might parse this file, see this [TypeScript example](https://github.com/AWaffleInc/rubot/blob/dd42c7afcdf1b6ff451d29d3727e740f15e90f70/src/Data.ts#L172) and [corresponding types declaration](https://github.com/AWaffleInc/rubot/blob/dd42c7afcdf1b6ff451d29d3727e740f15e90f70/src/definitions/MiscInterfaces.ts#L6).

### Courses TSV File
> **Warning**:
> The scraped information is **not** guaranteed to be complete or accurate, so please use at your own risk. Additionally parsing may need to be done. 

The `courses.tsv` file contains scraped information from each of the department's course catalog page. 

| Header Name     | Header Information | Example |
| --------------- | ------------------ | ------- |
| `department`    | The department.    | COGS     |
| `course_number` | The course number. | COGS 108 |
| `course_name`   | The name of the course. | Data Science in Practice |
| `units`         | The number of possible units. | 4 |
| `description`   | The course description. | Data science is multidisciplinary... |

To see an example of how you might parse this file, see this [TypeScript example](https://github.com/AWaffleInc/rubot/blob/dd42c7afcdf1b6ff451d29d3727e740f15e90f70/src/Data.ts#L230) and [corresponding types declaration](https://github.com/AWaffleInc/rubot/blob/dd42c7afcdf1b6ff451d29d3727e740f15e90f70/src/definitions/MiscInterfaces.ts#L53).




[^1]: See the "Contact Me" section of my [profile's](https://github.com/ewang2002) README page for my email.
