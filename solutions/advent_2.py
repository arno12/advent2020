# Challenge: https://adventofcode.com/2020/day/2

import pandas as pd

advent = pd.read_table("advent2.txt", header=None, names=['col'])


def toboggan(input_list):
    df = input_list['col'].str.extract(r'(\d+)-(\d+) ([a-z]): (.*)')
    df.columns = ['min', 'max', 'letter', 'password']
    df[['min', 'max']] = df[['min', 'max']].apply(pd.to_numeric, errors='coerce')

    df['occurrences'] = df.apply(lambda x: x['password'].count(x['letter']), axis=1)

    df['is_valid'] = df.apply(lambda x: x['min'] <= x['occurrences'] <= x['max'], axis=1)

    return df.groupby('is_valid').count()


def toboggan_advanced(input_list):
    df = input_list['col'].str.extract(r'(\d+)-(\d+) ([a-z]): (.*)')
    df.columns = ['min', 'max', 'letter', 'password']
    df[['min', 'max']] = df[['min', 'max']].apply(pd.to_numeric, errors='coerce')

    df['is_in_slot_1'] = df.apply(lambda x: x['password'][x['min'] - 1] == x['letter'], axis=1)
    df['is_in_slot_2'] = df.apply(lambda x: x['password'][x['max'] - 1] == x['letter'], axis=1)

    df['is_valid'] = df.apply(lambda x: x['is_in_slot_1'] + x['is_in_slot_2'] == 1, axis=1)

    return df.groupby('is_valid').count()


if __name__ == '__main__':
    print(toboggan_advanced(advent))
