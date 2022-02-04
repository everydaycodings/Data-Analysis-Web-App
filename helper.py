from sys import prefix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime, pytz
import glob, os


excel_type =["vnd.ms-excel","vnd.openxmlformats-officedocument.spreadsheetml.sheet", "vnd.oasis.opendocument.spreadsheet", "vnd.oasis.opendocument.text"]


def data(data, file_type, seperator=None):

    if file_type == "csv":
        data = pd.read_csv(data)

   # elif file_type == "json":
    #    data = pd.read_json(data)
    #    data = (data["devices"].apply(pd.Series))
    
    elif file_type in excel_type:
        data = pd.read_excel(data)
        st.sidebar.info("If you are using Excel file so there could be chance of getting minor error(temporary sollution: avoid the error by removing overview option from input box) so bear with it. It will be fixed soon")
    
    elif file_type == "plain":
        try:
            data = pd.read_table(data, sep=seperator)
        except ValueError:
            st.info("If you haven't Type the separator then dont worry about the error this error will go as you type the separator value and hit Enter.")

    return data

def seconddata(data, file_type, seperator=None):

    if file_type == "csv":
        data = pd.read_csv(data)

   # elif file_type == "json":
    #    data = pd.read_json(data)
    #    data = (data["devices"].apply(pd.Series))
    
    elif file_type in excel_type:
        data = pd.read_excel(data)
        st.sidebar.info("If you are using Excel file so there could be chance of getting minor error(temporary sollution: avoid the error by removing overview option from input box) so bear with it. It will be fixed soon")
    
    elif file_type == "plain":
        try:
            data = pd.read_table(data, sep=seperator)
        except ValueError:
            st.info("If you haven't Type the separator then dont worry about the error this error will go as you type the separator value and hit Enter.")

    return data


def match_elements(list_a, list_b):
    non_match = []
    for i in list_a:
        if i  in list_b:
            non_match.append(i)
    return non_match


def download_data(data, label):
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    current_time = "{}.{}-{}-{}".format(current_time.date(), current_time.hour, current_time.minute, current_time.second)
    export_data = st.download_button(
                        label="Download {} data as CSV".format(label),
                        data=data.to_csv(),
                        file_name='{}{}.csv'.format(label, current_time),
                        mime='text/csv',
                        help = "When You Click On Download Button You can download your {} CSV File".format(label)
                    )
    return export_data


def describe(data):
    global num_category, str_category
    num_category = [feature for feature in data.columns if data[feature].dtypes != "O"]
    str_category = [feature for feature in data.columns if data[feature].dtypes == "O"]
    column_with_null_values = data.columns[data.isnull().any()]
    return data.describe(), data.shape, data.columns, num_category, str_category, data.isnull().sum(),data.dtypes.astype("str"), data.nunique(), str_category, column_with_null_values


def outliers(data, num_category_outliers):
    plt.figure(figsize=(6,2))
    flierprops = dict(marker='o', markerfacecolor='purple', markersize=6,
                    linestyle='none', markeredgecolor='black')
    
    path_list = []
    for i in range(len(num_category_outliers)):
        
        column = num_category_outliers[i]
        plt.xlim(min(data[column]), max(data[column])) 
        plt.title("Checking Outliers for {} Column".format(column))
        plot = sns.boxplot(x=column, flierprops=flierprops, data=data)
        fig = plot.get_figure()

        path = 'temp/pic{}.png'.format(i)
        fig.savefig(path)
        path_list.append(path)

    return path_list



def drop_items(data, selected_name):
    droped = data.drop(selected_name, axis = 1)
    return droped


def filter_data(data, selected_column, selected_name):
    if selected_name == []:
        filtered_data = data
    else:
        filtered_data = data[~ data[selected_column].isin(selected_name)]
    return filtered_data


def num_filter_data(data, start_value, end_value, column, param):
    if param == "Delete data inside the range":
        if column in num_category:
            num_filtered_data = data[~data[column].isin(range(int(start_value), int(end_value)+1))]
    else:
        if column in num_category:
            num_filtered_data = data[data[column].isin(range(int(start_value), int(end_value)+1))]
    
    return num_filtered_data


def rename_columns(data, column_names):
    rename_column = data.rename(columns=column_names)
    return rename_column


def handling_missing_values(data, option_type, dict_value=None):
    if option_type == "Drop all null value rows":
        data = data.dropna()

    elif option_type == "Only Drop Rows that contanines all null values":
        data = data.dropna(how="all")
    
    elif option_type == "Filling in Missing Values":
        data = data.fillna(dict_value)
    
    return data


def data_wrangling(data1, data2, key, usertype):
    if usertype == "Merging On Index":
        data = pd.merge(data1, data2, on=key, suffixes=("_extra", "_extra0"))
        data = data[data.columns.drop(list(data.filter(regex='_extra')))]
        return data
    
    elif usertype == "Concatenating On Axis":
        data = pd.concat([data1, data2], ignore_index=True)
        return data



def clear_image_cache():
    removing_files = glob.glob('temp/*.png')
    for i in removing_files:
        os.remove(i)