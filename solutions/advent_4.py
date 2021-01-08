#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd


# In[16]:



# Opening the data correctly needed to be done using the regular Python open function as the read_csv failed to use \n\n correctly
with open('../inputs/advent4.txt') as file:
    data = file.read()

passport_lines = data.split('\n\n')

passport_lines_clean = [line.replace('\n',' ') for line in passport_lines]

df = pd.DataFrame({'raw':passport_lines_clean})

df


# In[17]:


# Creating a column for each of the potential variables
def detect_pattern(df, col, pattern):
    regex = pattern + ":(\S+)"
    df = df[col].str.extract(regex)
    return df


# In[18]:



patterns = ['ecl','pid','eyr','hcl','byr','iyr','cid','hgt']

for pattern in patterns:
    df[pattern] = detect_pattern(df, 'raw', pattern)

df
    


# In[19]:


# Check which values are missing aka not valid
missings = ~df.isnull()

# Count the fields present in mandatory columns
valid_cols = ['ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt']
df['valid_cols'] = missings[valid_cols].sum(axis=1)
df['is_valid'] = df.apply(lambda x: x['valid_cols'] == 7, axis=1)
df


# In[20]:


# Part A Answer
df['is_valid'].sum()


# In[21]:


# Part B - adding the more complex rules to the password detection

# For HGT, we first need to deconstruct the value into a regex that verifies whether there is a in or cm
# and between 2 and 3 digits
hgt_values = df['raw'].str.extract('hgt:(?P<hgt_value>\d{2,3})(?P<hgt_system>in|cm)')
df = pd.concat([df, hgt_values], axis=1)


# In[37]:


# Transform integer variables into int's instead of strings
df[['pid','eyr','byr','iyr','cid','hgt_value']] = df[['pid','eyr','byr','iyr','cid','hgt_value']].apply(pd.to_numeric, errors='coerce')

df['valid_byr'] = df['byr'].between(1920, 2002)
df['valid_iyr'] = df['iyr'].between(2010, 2020)
df['valid_eyr'] = df['eyr'].between(2020, 2030)

# (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# Create the function that will determine whether the height is valid
def get_hgt_validity(df):
    if df['hgt_system'] == 'cm' and 150 <= df['hgt_value'] <= 193:
        return True
    elif df['hgt_system'] == 'in' and 59 <= df['hgt_value'] <= 76:
        return True
    else:
        return False
                                      
df['valid_hgt'] = df.apply(get_hgt_validity, axis=1)

# (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
#df['valid_hcl'] = df['raw'].str.contains('hcl:#(?:[\d]|[a-f]){6}', regex = True)
df['valid_hcl'] = df['raw'].str.contains('hcl:#[a-z0-9]{6}', regex = True)
    
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# df['valid_ecl'] = df['raw'].str.contains('ecl:(?:amb|blu|brn|gry|grn|hzl|oth){1}', regex = True)
df['valid_ecl'] = df['raw'].str.contains('ecl:(?:amb|blu|brn|gry|grn|hzl|oth)', regex = True)


# a nine-digit number, including leading zeroes
#df['valid_pid'] = df['raw'].str.contains('pid:(?:\d){9}[^\d]', regex = True)
df['valid_pid'] = df['raw'].str.contains('pid:\d{9}\\b', regex = True)

valid_cols = ['valid_ecl', 'valid_pid', 'valid_eyr', 'valid_hcl', 'valid_byr', 'valid_iyr', 'valid_hgt']

df['valid_cols'] = df[valid_cols].sum(axis=1)
df['is_valid_b'] = df.apply(lambda x: x['valid_cols'] == 7, axis=1)
pd.options.display.float_format = '{:20.0f}'.format
df[['pid' ,'valid_pid']]


# In[38]:


df['is_valid_b'].sum()


# In[ ]:




