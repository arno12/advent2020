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

advent = pd.read_table("../inputs/advent5.txt", header=None, names=['raw'])
advent['row'] = [x[:7] for x in advent['raw']]
advent['col'] = [x[7:10] for x in advent['raw']]
advent


# +
def get_row_number(df, col, rows, front_letter, back_letter):
    #print(df[col])
    lower_bound = 0
    upper_bound = ref_bound = rows
    for letter in df[col]:
        ref_bound /= 2
        #print(letter)
        #print("ref bound: {}".format(ref_bound))
        if letter == front_letter:
            upper_bound -= ref_bound
            #print("lower_bound: {}".format(lower_bound))
            #print("upper_bound: {}".format(upper_bound))
        elif letter == back_letter:
            lower_bound += ref_bound
            #print("lower_bound: {}".format(lower_bound))
            #print("upper_bound: {}".format(upper_bound))
    #print(upper_bound - lower_bound)
    return upper_bound - 1

# get_row_number(advent['row'], 128)

advent['row_nr'] = advent.apply(get_row_number, args = ('row', 128, 'F', 'B'), axis=1)
advent['col_nr'] = advent.apply(get_row_number, args = ('col', 8, 'L', 'R'), axis=1)

advent['seat_nr'] = (advent['row_nr'] * 8) + advent['col_nr']

advent
# -

# Part A - return the highest seat number
max(advent['seat_nr'])

# +
# Part B - find the missing seat in the middle of the plane (not in the very front or very back)

seats_list = [int(a) for a in advent['seat_nr']]

seats_list_incomplete = set(seats_list)

seats_list_full = set(range(min(seats_list),max(seats_list)+1))

seats_list_full - seats_list_incomplete
