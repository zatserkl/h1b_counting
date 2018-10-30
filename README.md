# Table of Contents
1. [Problem](README.md#problem)
2. [Input Dataset](README.md#input-dataset-analysis)
3. [Method](README.md#method)

# Problem

A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years.

As a data engineer, you are asked to create a mechanism to analyze past years data, specifically calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

Your code should be modular and reusable for future. If the newspaper gets data for the year 2019 (with the assumption that the necessary data to calculate the metrics are available) and puts it in the `input` directory, running the `run.sh` script should produce the results in the `output` folder without needing to change the code.

# Input Dataset Analysis

The original task description has a remark:

**Note:** Each year of data can have different columns. Check **File Structure** docs before development.

The name of some field in 2014 dataset are different from the 2017 one. It is reasonable to assume that the fields also can be changed in the coming years. I developed special method to deal with this problem.

## Method

I need to identify just two fields: occupation and state.
Occupational name associated with the the Standard Occupational Classification (SOC) System.

2014 specification.
__`STATUS`__:	Status associated with the last significant event or decision. Valid values include “Certified,” “Certified-Withdrawn,” Denied,” and “Withdrawn”.
Note that in fact all the fields are in upper case, e.g. "CERTIFIED" for "Certified".

From 2018 specification:
__`WORKSITE_STATE`__: State information of the foreign worker's intended area of employment.
There are two state fields in the 2014 specification:
__`LCA_CASE_WORKLOC1_STATE`__: Address information of the intended are in which the foreign worker is expected to be employed (location of the job opening)
__`LCA_CASE_WORKLOC2_STATE`__: Address information of the second location in which the foreign worker is expected to be employed (location of the job opening).

Compare them we see that the __`LCA_CASE_WORKLOC1_STATE`__ directly corresponds to 2018's __`WORKSITE_STATE`__.

Fields for 2008.
__`State_1`__:	Work state (location of the job opening).
__`Approval_Status`__:	Approval status - certified or denied.
