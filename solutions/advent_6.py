# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd

# +
# Opening the data correctly needed to be done using the regular Python open function as the read_csv failed to use \n\n correctly
with open('../inputs/advent6.txt') as file:
    data = file.read()

passport_lines = data.split('\n\n')

passport_lines_merged = [line.replace('\n','') for line in passport_lines]
passport_lines_sep = [line.replace('\n','_') for line in passport_lines]

df = pd.DataFrame({'raw':passport_lines_merged, 'sep':passport_lines_sep})

df

# +
# Part A
# The length of a set counts unique occurences of the characters inside it
df['unique_answers'] = df.apply(lambda x: len(set(x['raw'])), axis=1)

sum(df['unique_answers'])

# +
# Part B - 
# You don't need to identify the questions to which anyone answered "yes"; 
# you need to identify the questions to which everyone answered "yes"!
splitted_list = [item.split("_") for item in passport_lines_sep]

def get_common_answers_count(df):
    sub_list = [item for item in df["sep"].split("_")]
    common_letters = set(sub_list[0])
    for item in sub_list[1:]:
        common_letters &= set(item)
    return len(common_letters)

df['common_answers'] = df.apply(get_common_answers_count, axis=1)

df
# -

# This outputs the results - 1 because the last parsed line contains an extra "_"
sum(df['common_answers'])


