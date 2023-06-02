import sys
from os import mkdir
from os.path import exists

# get the current directory
if len(val := sys.path[0].split("\\")) > 1:
    current_dir = val[-1]
else:
    current_dir = val[0]

csv_url = f"https://github.com/UCSD-Historical-Enrollment-Data/{current_dir}/blob/main/URL_TYPE_FILLER/CSV_FILLER"
png_url = f"https://raw.githubusercontent.com/UCSD-Historical-Enrollment-Data/{current_dir}/main/URL_TYPE_FILLER/REG_PNG_FILLER"

# data contains all possible courses in this repository
data = {}
keys = []
subjects = {}

# Open the file with encoding utf-8
with open("all_courses.txt", "r", encoding="utf-8") as f:
    for course in f:
        course = course.strip()
        if course == "":
            continue

        data[course] = {
            "has_overall_png": False,
            "has_overall_wide_png": False,
            "has_overall_csv": True,
            "section": {}
        }

        keys.append(course)

        # Get the subject
        subject = course.split(" ")[0]
        if subject not in subjects:
            subjects[subject] = []
        
        subjects[subject].append(course)

# Check if overall png exists
for course in data:
    if exists("plot_overall") and exists(f"plot_overall/{course}.png"):
        data[course]["has_overall_png"] = True
    if exists("plot_overall_wide") and exists(f"plot_overall_wide/{course}.png"):
        data[course]["has_overall_wide_png"] = True 

# Go through all sections
with open("all_sections.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line == "":
            continue

        if "_" not in line:
            continue

        course, section = line.split("_")
        section = section.strip()
        if course not in data:
            continue

        has_regular_png = exists("plot_section") and exists(f"plot_section/{course}_{section}.png")
        has_wide_png = exists("plot_section_wide") and exists(f"plot_section_wide/{course}_{section}.png")
        has_sec_csv = exists("section") and exists(f"section/{course}_{section}.csv")

        data[course]["section"][section] = {
            "has_regular_png": has_regular_png,
            "has_wide_png": has_wide_png,
            "has_sec_csv": has_sec_csv
        }

# Generate the TOC directory, if it doesn't exist
if not exists("TOC"):
    mkdir("TOC")

# Go through all subjects and create a README for each
for subject in subjects:
    readme = ""
    readme += f"# {subject}\n\n"
    readme += "| Course | Overall | Section |\n"
    readme += "| ------ | ------- | ------- |\n"
    for course in subjects[subject]:
        crsc_data = data[course]

        # Overall
        encoded_course = course.replace(" ", "%20")
        overall_list = []
        if crsc_data["has_overall_csv"]:
            url_base = csv_url.replace('URL_TYPE_FILLER', 'overall') \
                .replace('CSV_FILLER', encoded_course)
            overall_list.append(f"[csv]({url_base}.csv)")

        if crsc_data["has_overall_png"]:
            url_base = png_url.replace('URL_TYPE_FILLER', 'plot_overall') \
                .replace('REG_PNG_FILLER', encoded_course)
            overall_list.append(f"[png]({url_base}.png)")

        if crsc_data["has_overall_wide_png"]:
            url_base = png_url.replace('URL_TYPE_FILLER', 'plot_overall_wide') \
                .replace('REG_PNG_FILLER', encoded_course)
            overall_list.append(f"[wide]({url_base}.png)")

        # Section
        section_list = []
        for section in crsc_data["section"]:
            this_column = f"Section {section}: "

            if crsc_data["section"][section]["has_sec_csv"]:
                url_base = csv_url.replace('URL_TYPE_FILLER', 'section') \
                    .replace('CSV_FILLER', f"{encoded_course}_{section}")
                this_column += f"[csv]({url_base}.csv)"

            if crsc_data["section"][section]["has_regular_png"]:
                url_base = png_url.replace('URL_TYPE_FILLER', 'plot_section') \
                    .replace('REG_PNG_FILLER', f"{encoded_course}_{section}")
                this_column += f", [png]({url_base}.png)"

            if crsc_data["section"][section]["has_wide_png"]:
                url_base = png_url.replace('URL_TYPE_FILLER', 'plot_section_wide') \
                    .replace('REG_PNG_FILLER', f"{encoded_course}_{section}")
                this_column += f", [wide]({url_base}.png)"

            section_list.append(this_column)

        overall_column = ", ".join(overall_list)
        section_column = "<br>".join(section_list)
        # Add row
        readme += f"| {course} | {overall_column} | {section_column} |\n"

    with open(f"TOC/{subject}.md", "w", encoding="utf-8") as f:
        f.write(readme)

# Now, go through all subjects and create a TOC.md which links to each subject MD file
readme = "# Course Listings\n\n"

if len(keys) == 0:
    readme += "At this time, there's no data available."
else: 
    readme += "| Subject | Link to Course Data |\n"
    readme += "| ------- | ------------------- |\n"
    for subject in subjects:
        readme += f"| {subject} | [{subject}](TOC/{subject}.md) |\n"

with open("TOC.md", "w", encoding="utf-8") as f:
    f.write(readme)