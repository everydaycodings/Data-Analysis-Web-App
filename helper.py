import pandas as pd


def data(data):
    data = pd.read_csv(data)
    return data


def describe(data):
    return data.describe()