# Table of Contents
1. [Problem](README.md#problem)
2. [Input Dataset](README.md#input-dataset-analysis)
3. [Heuristic Method](README.md#heuristic-method)
3. [Tests](README.md#tests)

# Problem

A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years.

As a data engineer, you are asked to create a mechanism to analyze past years data, specifically calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

Your code should be modular and reusable for future. If the newspaper gets data for the year 2019 (with the assumption that the necessary data to calculate the metrics are available) and puts it in the `input` directory, running the `run.sh` script should produce the results in the `output` folder without needing to change the code.

# Input Dataset Analysis

The original task description has a remark:

**Note:** Each year of data can have different columns. Check **File Structure** docs before development.

The name of some field in 2014 dataset are different from the 2017 one. It is reasonable to assume that the fields also can be changed in the coming years. I developed special method to deal with this problem.

# Heuristic Method

Basically I need to identify header indices for just three fields: visa status, occupation, and state.
Occupational name associated with the the Standard Occupational Classification (SOC) System.

The main problem with parsing the data is that the header keys have been changed from year to year. For example keys for visa status are different for 2017 and e.g. 2014. The similar problems are for some other keys.

That become especially important for coming data for 2019 year (we need to take a look at the future!).
To overcome this problem I applied heuristic approach.

To find the occupation I search for some popular occupations. A quick look on the data shows that the occupation description were not changed much.

A search for the state is a bit complicated because for some years (e.g. 2014) there are two states mentioned: an intended and the second state. Out of them the first (intended) state comes the most close to the meaning for the other years. This state comes as the second state field (the first is an employer state). For some years there is also a state for the attorney, but is can be sorted out because attorney was not used in all records. To search for the state I use a list of all U.S. states and territories.

To speedup the heuristic process I tried some header keys that work for some years. Of course, we cannot predict the keys for the 2019.

To carry out heuristic analysis, I read a chunk of lines, typically 1000 lines. For regular processing I read the data over again.

# Tests

I added test with 2014 data.
