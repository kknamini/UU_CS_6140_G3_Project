#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 12:58:03 2023

@author: grace
"""

# Notes
# Gender and ethnicity each add up to 582,484, not 582,462
# Use overall homeless
# Row 175 male + female adds up to more than the overall

# Imports
import matplotlib.pyplot as plt
import pandas as pd

#%% Read 2022 sheet

year = pd.read_excel("2007-2022-PIT-Counts-by-CoC.xlsx", sheet_name = "2022", skiprows = [388, 389, 390, 391]).drop(175)
year["Binary"] = year["Overall Homeless - Female, 2022"] + year["Overall Homeless - Male, 2022"]
#year["Over18"] = year["Overall Homeless - Age 18 to 24, 2022"] + year["Overall Homeless - Over 24, 2022"]

#%% Define functions

def write_csv(col1, col2, v1, v2):
    df = pd.DataFrame([year[col1] / year["Overall Homeless, 2022"], year[col2] / year["Overall Homeless, 2022"]], index = [v1, v2]).T
    df.index = year["CoC Number"]
    df.to_csv(f"intermediate_report_data/{v1}_{v2}.csv")
    return df

def plot(df, v1, v2):
    plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
    plt.title(f"Overall homeless, {v1} vs. {v2}")
    plt.xlabel(f"Proportion {v1}")
    plt.ylabel(f"Proportion {v2}")
    plt.show()

#%% Under 18 vs. white

under18_white = write_csv("Overall Homeless - Under 18, 2022", "Overall Homeless - White, 2022", "under18", "white")
plot(under18_white, "under 18", "white")

#%% Under 18 vs. binary

under18_binary = write_csv("Overall Homeless - Under 18, 2022", "Binary", "under18", "binary")
plot(under18_binary, "under 18", "binary")

#%% White vs. binary

white_binary = write_csv("Overall Homeless - White, 2022", "Binary", "white", "binary")
plot(white_binary, "white", "binary")

#%% Age splits

age_splits = pd.DataFrame([year["Overall Homeless - Under 18, 2022"] / year["Overall Homeless, 2022"], year["Overall Homeless - Age 18 to 24, 2022"] / year["Overall Homeless, 2022"], year["Overall Homeless - Over 24, 2022"] / year["Overall Homeless, 2022"]], index = ["under18", "between", "over24"]).T
age_splits.index = year["CoC Number"]
age_splits.to_csv("intermediate_report_data/age_splits.csv")

fig = plt.figure()
ax = fig.add_subplot(projection =  "3d")
ax.scatter(age_splits["under18"], age_splits["between"], age_splits["over24"], s = 3)
ax.set_title("Overall homeless, split into three age groups")
ax.set_xlabel("Proportion under 18")
ax.set_ylabel("Proportion 18-24")
ax.set_zlabel("Proportion over 24")
ax.set_box_aspect(aspect = None, zoom=0.89)
plt.show()