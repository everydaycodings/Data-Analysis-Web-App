import pandas as pd


def data(data):
    data = pd.read_csv(data)
    return data


def describe(data):
    num_category = [feature for feature in data.columns if data[feature].dtypes != "O"]
    str_category = [feature for feature in data.columns if data[feature].dtypes == "O"]
    return data.describe(), data.shape, data.columns, num_category, str_category