<p align="center">
  <img src="https://github.com/ewang2002/UCSDHistEnrollData/blob/master/misc/assets/project_banner.png?raw=true"  alt="Project Banner"/>
</p>

<p align="center">
  <a href="https://github.com/ewang2002/webweg">webweg</a> |
  <a href="https://github.com/ewang2002/webreg_scraper">webreg_scraper</a> |
  <b>UCSDHistEnrollmentData</b>
</p>

A repository that 
- branches out to multiple children repositories containing enrollment data for multiple terms at UC San Diego.
- contains some other other UCSD-related [data files](https://github.com/ewang2002/UCSDHistEnrollData/tree/master/data) that may be helpful.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Data](#data)
  - [Full Data](#full-data)
  - [Incomplete & Limited Data](#incomplete--limited-data)
- [Documentation](#documentation)
- [Third-Party Projects](#third-party-projects)
- [Contacting Us](#contacting-us)
- [License](#license)

  
## Data
> [!TIP]
> If you just want to see some third-party projects that are using the data that we collect, see the [Third-Party Projects](#third-party-projects) section at the bottom.

You can find historical enrollment data linked below. Documentation can be found further below. To see the other UCSD-related data files, go to the [`data`](https://github.com/ewang2002/UCSDHistEnrollData/tree/master/data) folder.

> [!NOTE]
> This repository contains a number of random scripts to help me clean up and process the enrollment data, documentation regarding how the CSV files are structured, and links to the sibling repositories. **Each child repository** contains CSV files which contains information regarding the number of seats available at some time for certain classes. There are also some scripts designed to help clean and analyze the data. Additionally, there are pre-generated plots of each course that is being tracked.

### Full Data
Starting with FA22, 
- enrollment and drop data are integrated into one term folder. 
- graduate courses from specific departments will be collected[^1].
- all undergraduate courses will be collected.

| Term | Information | Data Collected | Link |
| ---- | ----------- | -------------- | ---- |
| FA22 | Fall 2022 Enrollment & Drop Data (Undergraduate Only) | All undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022Fall) |
| FA22G | Fall 2022 Enrollment & Drop Data (Graduate Only) | CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022FallGrad) |
| WI23 | Winter 2023 Enrollment & Drop Data (Undergraduate Only) | All undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2023Winter) |
| WI23G | Winter 2023 Enrollment & Drop Data (Graduate Only) | CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2023WinterGrad) |
| SP23 | Spring 2023 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2023Spring) |
| FA23 | Fall 2023 Enrollment | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2023Fall) |
| WI24 | Winter 2024 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2024Winter) |
| SP24 | Spring 2024 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2024Spring) |
| S124 | Summer I 2024 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2024Summer1) |
| S224 | Summer II 2024 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2024Summer2) |
| S324 | Special Summer 2024 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2024Summer3) |
| FA24 | Fall 2024 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2024Fall) |
| WI25 | Winter 2025 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2025Winter) |
| SP25 | Spring 2025 Enrollment & Drop Data | All undergraduate courses & CSE, COGS, MATH, ECE graduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2025Spring) |

### Incomplete & Limited Data 

<details>
<summary>Incomplete Data</summary>
<br> 

Below, you can find incomplete data. Incomplete data is defined as data with a significant number of missing datapoints (essentially rendering them significantly less valuable than regular datasets).

| Term | Information | Data Collected | Link |
| ---- | ----------- | -------------- | ---- |
| S123 | Summer I 2023 Raw Data | All undergraduate courses (raw data only, see repository for more info) | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2023Summer1) |
| S223 | Summer II 2023 Raw Data | All undergraduate courses (raw data only, see repository for more info) | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2023Summer2) |

</details>

<details>
<summary>Limited Data (Prior to FA22)</summary>
<br> 

The following repositories only contain _limited_ data, and were intended to be long-term test runs to see if the project was feasible. Note that Spring 2022 enrollment data is formatted differently from the data found in other data repositories.

| Term | Information | Data Collected | Link |
| ---- | ----------- | -------------- | ---- |
| SP22 | Spring 2022 Enrollment Data | CSE, COGS, MATH, ECE undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022Spring) |
| SP22D | Spring 2022 Drop Data | CSE, COGS, MATH, ECE undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022SpringDrop) |
| S122 | Summer I 2022 Enrollment Data | CSE, COGS, MATH, ECE undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022Summer1) |
| S122D | Summer I 2022 Drop Data | CSE, COGS, MATH, ECE undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022Summer1Drop) |
| S222 | Summer II 2022 Enrollment Data | CSE, COGS, MATH, ECE undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022Summer2) |
| S222D | Summer II 2022 Drop Data | CSE, COGS, MATH, ECE undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022Summer2Drop) |
| S322 | Summer III 2022 Data | CSE, COGS, MATH, ECE undergraduate courses | [Here](https://github.com/UCSD-Historical-Enrollment-Data/2022Summer3) |

</details>

## Documentation
Below, you can find some documentation to get you started.
- [Background and Acknowledgements](https://github.com/ewang2002/UCSDHistEnrollData/blob/master/docs/background.md)
- [CSV Information and Structure](https://github.com/ewang2002/UCSDHistEnrollData/blob/master/docs/csv_info.md)
- [Data Repository Information and Structure](https://github.com/ewang2002/UCSDHistEnrollData/blob/master/docs/data_repo_info.md)
- [Scripts](https://github.com/ewang2002/UCSDHistEnrollData/blob/master/docs/scripts.md)
- [Setup](https://github.com/ewang2002/UCSDHistEnrollData/blob/master/docs/setup.md)


## Third-Party Projects
Below are a list of **third-party websites** using our data in some way.

| Website | Features |
| ------- | -------- |
| [UC San Diego Course Registration Trend](https://www.ucsdregistration.com/) | A website that can display enrollment trends of multiple courses across different terms in one graph. See this [Reddit post](https://www.reddit.com/r/UCSD/comments/1gjuo36/i_made_a_website_to_help_make_course_registration/) for a synopsis of this website. |
| [TritonSEA](http://triton-sea.com/) | A website designed to simplify your planning and help you make informed decisions, all in one place, including features like importing your degree audit and getting personalized class recommendations, viewing stats and enrollment information for clases in previous quarters, and more. See this [Reddit post](https://www.reddit.com/r/UCSD/comments/1io9qqa/enrollment_made_easier_tritonsea_spring_2025/) for a synopsis of this website. |

Keep in mind that the maintainers of this project (`UCSDHistEnrollData`, and any other repositories under the `UCSD-Historical-Enrollment-Data` organization) do not necessarily endorse these third-party projects. However, we believe they may be more useful for the _general public_ than the raw data that we store in this organization. 

## Contacting Us
There are two ways you can contact the project maintainers.
- Any general questions or comments about the project can be directed to [the discussion tab](https://github.com/orgs/UCSD-Historical-Enrollment-Data/discussions). 
- To contact the maintainers directly, you may reach out to:

  | Name                  | Contact Email                |
  | --------------------- | ---------------------------- |
  | Ryan Batubara         | rbatubara at UCSD's domain   |
  | Edward Wang           | ewang20027 at gmail's domain |

  It is recommended that you email Ryan directly and CC Edward.

## License
**All files here and in the data repositories are licensed under the MIT license.** If you'd like an explicit LICENSE file in the data repositories, please let me[^2] know.

You're free to use this data for your own projects, but please be sure to cite this [repository](https://github.com/UCSD-Historical-Enrollment-Data/UCSDHistEnrollData/) when using data found here so other people can use the data for their own projects.

As an aside, you do _not_ need to contact us if you plan on using the data that we collect, although we do love hearing how people are using our data! 

[^1]: Graduate courses are not formally supported. Once I stop collecting undergraduate course enrollment data, I will also stop collecting graduate course enrollment data, which means some data (e.g., drop with W deadline) will not be collected.

[^2]: Edward is bad. 
