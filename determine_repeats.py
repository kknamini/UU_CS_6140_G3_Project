import pandas as pd

###########################################################################################
# Change the inpath to match the input filepath for '2007-2022-PIT-Counts-by-CoC.xlsx' file
inpath = r''

# Change the outpath to determine where the output files are written
outpath = r''
###########################################################################################

# Read all sheets in .xlsx file into dictionary of DataFrames
data = pd.read_excel(fr'{inpath}\2007-2022-PIT-Counts-by-CoC.xlsx', sheet_name=None)

# Lambda function to remove ', {year}' from the end of each variable it appears in
slice_colname = lambda x: x if(x.find(',') == -1) else x[:-6]

# Lambda functions to remove slight variations in column names that should be exactly the same
black = lambda x: x if(x.find('Black') == -1) else f"{x[:19]}Black or African American"
asian = lambda x: x if(x.find('Asian') == -1) else f"{x[:19]}Asian or Asian American"
native = lambda x: x if(x.find('American Indian') == -1) else f"{x[:19]}American Indian or Alaska Native"
nonbinary = lambda x: x if(x.find('Singularly') == -1 and x.find('Conforming') == -1) else f"{x[:19]}Nonbinary Gender"

# Apply lambda functions to rename columns for all data tables
for i in data:
    data[i].rename(columns=slice_colname, inplace=True)
    data[i].rename(columns=black, inplace=True)
    data[i].rename(columns=asian, inplace=True)
    data[i].rename(columns=native, inplace=True)
    data[i].rename(columns=nonbinary, inplace=True)

# Function to determine the list of column names in the "data" input dictionary that repeat in range of years selected for analysis
# "data" is a dictionary with 'year' (title of data table) as keys, and a list of column names as the value for each key (column names of each data table)
# 'analysis_years' is the list of keys used to select the years of data tables to include
# The columns that appear in the all selected data tables are returned as a sorted list
def repeat_vars(data, analysis_years):
    repeats = set()
    for i in range(len(analysis_years)):
        if i == 0:
            repeats = set(data[analysis_years[i]])
        else:
            repeats = repeats & set(data[analysis_years[i]])
    repeats = list(repeats)
    repeats.sort()
    return repeats

# Create empty dictionary for each sheet's column names
data_columns = dict()

# Loop through dictionary of DataFrames to update data_columns dictionary with sheet name for each key and list of column names for each value
for i in data:
    data_columns.update({i : data[i].columns.values.tolist()})

# Set the possible years to include in analysis; 2007 is excluded because it contains zero non-ID columns
analysis_years_max = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008']

# Create empty dictionary to contain processed data
newdata = dict()

for i in range(len(analysis_years_max)):
    # This limits the smallest range of years to select, as a result the shortest range will be from 2018-2022
    if i > 3:
        # Create temporary dictionary
        temp = dict()
        # For each dataset
        for j in data:
            try:
                # Create a new entry for temp dict, limiting columns to those that appear in all datasets in the current range of years (determined by i+1)
                temp.update({j : data[j][repeat_vars(data_columns, analysis_years_max[:i+1])]})
            except:
                pass
        # Create new entry for processed data dict, which is also a dict containing all processed annual datasets in the current range of years
        newdata.update({f'{analysis_years_max[i]}-{analysis_years_max[0]}' : temp})

# For each range of years, create a new excel workbook and write each processed annual dataset to a new sheet
for i in newdata:
    with pd.ExcelWriter(fr'{outpath}\{i}_PIT_COC_Repeat_Vars.xlsx') as writer:
        for j in newdata[i]:
            newdata[i][j].to_excel(writer, sheet_name=j)