import pandas as pd
import math

advent = pd.read_table("advent3.txt", header=None, names=['col'])


def trees(right_marker_value, bottom_marker_value, file_input):
    # setup the df to be wide enough first - at least right_marker_value times as wide as it is long
    multiplier = math.ceil(len(file_input) * right_marker_value / len(advent.col[0]))
    file_input['col'] = file_input['col'].apply(lambda x: x * multiplier)

    # initialize values for first iteration
    right_marker = 0
    bottom_marker = bottom_marker_value
    counter = 0

    for i, row in file_input.iterrows():
        if i % bottom_marker != 0:
            continue
        elif row[0][right_marker] == '#':
            counter += 1
        right_marker += right_marker_value
    return counter


# First part of the challenge
print(trees(3, 1, advent))

# Second part of the challenge
print(math.prod(trees(*init, advent)
                for init in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]))
