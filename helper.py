import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def data(data):
    data = pd.read_csv(data)
    return data


def describe(data):
    global num_category
    num_category = [feature for feature in data.columns if data[feature].dtypes != "O"]
    str_category = [feature for feature in data.columns if data[feature].dtypes == "O"]
    return data.describe(), data.shape, data.columns, num_category, str_category, data.isnull().sum(),data.dtypes.astype("str"), data.nunique()


def outliers(data):
    plt.figure(figsize=(6,2))
    flierprops = dict(marker='o', markerfacecolor='purple', markersize=6,
                    linestyle='none', markeredgecolor='black')
    
    path_list = []
    for i in range(len(data.columns)):
        if data.columns[i] in num_category:
            plt.xlim(min(data[data.columns[i]]), max(data[data.columns[i]])) 
            plt.title("Checking Outliers for {} Column".format(data.columns[i]))
            plot = sns.boxplot(x=data.columns[i], flierprops=flierprops, data=data)
            fig = plot.get_figure()
            path = 'temp/pic{}.png'.format(i)
            fig.savefig(path)
            path_list.append(path)
    return path_list



def drop_items(data, selected_name):
    droped = data.drop(selected_name, axis = 1)
    return droped