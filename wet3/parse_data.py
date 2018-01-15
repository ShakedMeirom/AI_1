import pandas as pd
import numpy as np

# Consts:
TARGET_LABEL = 'classification'
INPUT_FILE = 'flare.csv'


def parse_data_to_table():

    data = pd.read_csv(INPUT_FILE)

    target = data[TARGET_LABEL]
    data = data.drop(TARGET_LABEL, axis = 1)
    return data, target


def parse_data_to_lists():
    data, target = parse_data_to_table()
    x = data.values.tolist()
    y = target.values.tolist()
    return x, y

