from cmath import nan
from datetime import date
import streamlit as st
from helper import data, seconddata, match_elements, describe, outliers, drop_items, download_data, filter_data, num_filter_data, rename_columns, clear_image_cache, handling_missing_values, data_wrangling
import numpy as np
import pandas as pd

st.set_page_config(
     page_title="Data Analysis Web App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/everydaycodings/Data-Analysis-Web-App',
         'Report a bug': "https://github.com/everydaycodings/Data-Analysis-Web-App/issues/new",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
)

st.sidebar.title("Data Analysis Web App")

file_format_type = ["csv", "txt", "xls", "xlsx", "ods", "odt"]
functions = ["Overview", "Outliers", "Drop Columns", "Drop Categorical Rows", "Drop Numeric Rows", "Rename Columns", "Display Plot", "Handling Missing Data", "Data Wrangling"]
excel_type =["vnd.ms-excel","vnd.openxmlformats-officedocument.spreadsheetml.sheet", "vnd.oasis.opendocument.spreadsheet", "vnd.oasis.opendocument.text"]

uploaded_file = st.sidebar.file_uploader("Upload Your file", type=file_format_type)

if uploaded_file is not None:

    file_type = uploaded_file.type.split("/")[1]
    
    if file_type == "plain":
        seperator = st.sidebar.text_input("Please Enter what seperates your data: ", max_chars=5) 
        data = data(uploaded_file, file_type,seperator)

    elif file_type in excel_type:
        data = data(uploaded_file, file_type)

    else:
        data = data(uploaded_file, file_type)
    
    describe, shape, columns, num_category, str_category, null_values, dtypes, unique, str_category, column_with_null_values = describe(data)

    multi_function_selector = st.sidebar.multiselect("Enter Name or Select the Column which you Want To Plot: ",functions, default=["Overview"])

    st.subheader("Dataset Preview")
    st.dataframe(data)

    st.text(" ")
    st.text(" ")
    st.text(" ")

    if "Overview" in multi_function_selector:
        st.subheader("Dataset Description")
        st.write(describe)

        st.text(" ")
        st.text(" ")
        st.text(" ")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text("Basic Information")
            st.write("Dataset Name")
            st.text(uploaded_file.name)

            st.write("Dataset Size(MB)")
            number = round((uploaded_file.size*0.000977)*0.000977,2)
            st.write(number)

            st.write("Dataset Shape")
            st.write(shape)
            
        with col2:
            st.text("Dataset Columns")
            st.write(columns)
        
        with col3:
            st.text("Numeric Columns")
            st.dataframe(num_category)
        
        with col4:
            st.text("String Columns")
            st.dataframe(str_category)
            

        col5, col6, col7, col8= st.columns(4)

        with col6:
            st.text("Columns Data-Type")
            st.dataframe(dtypes)
        
        with col7:
            st.text("Counted Unique Values")
            st.write(unique)
        
        with col5:
            st.write("Counted Null Values")
            st.dataframe(null_values)

# ==================================================================================================
    if "Outliers" in multi_function_selector:

        outliers_selection = st.multiselect("Enter or select Name of the columns to see Outliers:", num_category)
        outliers = outliers(data, outliers_selection)
        
        for i in range(len(outliers)):
            st.image(outliers[i])
# ===================================================================================================

    if "Drop Columns" in multi_function_selector:
        
        multiselected_drop = st.multiselect("Please Type or select one or Multipe Columns you want to drop: ", data.columns)
        
        droped = drop_items(data, multiselected_drop)
        st.write(droped)
        
        drop_export = download_data(droped, label="Droped(edited)")

# =====================================================================================================================================
    if "Drop Categorical Rows" in multi_function_selector:

        filter_column_selection = st.selectbox("Please Select or Enter a column Name: ", options=data.columns)
        filtered_value_selection = st.multiselect("Enter Name or Select the value which you don't want in your {} column(You can choose multiple values): ".format(filter_column_selection), data[filter_column_selection].unique())
        
        filtered_data = filter_data(data, filter_column_selection, filtered_value_selection)
        st.write(filtered_data)
        
        filtered_export = download_data(filtered_data, label="filtered")

# =============================================================================================================================

    if "Drop Numeric Rows" in multi_function_selector:

        option = st.radio(
        "Which kind of Filteration you want",
        ('Delete data inside the range', 'Delete data outside the range'))

        num_filter_column_selection = st.selectbox("Please Select or Enter a column Name: ", options=num_category)
        selection_range = data[num_filter_column_selection].unique()

        for i in range(0, len(selection_range)) :
            selection_range[i] = selection_range[i]
        selection_range.sort()

        selection_range = [x for x in selection_range if np.isnan(x) == False]

        start_value, end_value = st.select_slider(
        'Select a range of Numbers you want to edit or keep',
        options=selection_range,
        value=(min(selection_range), max(selection_range)))
        
        if option == "Delete data inside the range":
            st.write('We will be removing all the values between ', int(start_value), 'and', int(end_value))
            num_filtered_data = num_filter_data(data, start_value, end_value, num_filter_column_selection, param=option)
        else:
            st.write('We will be Keeping all the values between', int(start_value), 'and', int(end_value))
            num_filtered_data = num_filter_data(data, start_value, end_value, num_filter_column_selection, param=option)

        st.write(num_filtered_data)
        num_filtered_export = download_data(num_filtered_data, label="num_filtered")


# =======================================================================================================================================

    if "Rename Columns" in multi_function_selector:

        if 'rename_dict' not in st.session_state:
            st.session_state.rename_dict = {}

        rename_dict = {}
        rename_column_selector = st.selectbox("Please Select or Enter a column Name you want to rename: ", options=data.columns)
        rename_text_data = st.text_input("Enter the New Name for the {} column".format(rename_column_selector), max_chars=50)


        if st.button("Draft Changes", help="when you want to rename multiple columns/single column  so first you have to click Save Draft button this updates the data and then press Rename Columns Button."):
            st.session_state.rename_dict[rename_column_selector] = rename_text_data
        st.code(st.session_state.rename_dict)

        if st.button("Apply Changes", help="Takes your data and rename the column as your wish."):
            rename_column = rename_columns(data, st.session_state.rename_dict)
            st.write(rename_column)
            export_rename_column = download_data(rename_column, label="rename_column")
            st.session_state.rename_dict = {}

# ===================================================================================================================
 
    if "Display Plot" in multi_function_selector:

        multi_bar_plotting = st.multiselect("Enter Name or Select the Column which you Want To Plot: ", str_category)
        
        for i in range(len(multi_bar_plotting)):
            column = multi_bar_plotting[i]
            st.markdown("#### Bar Plot for {} column".format(column))
            bar_plot = data[column].value_counts().reset_index().sort_values(by=column, ascending=False)
            st.bar_chart(bar_plot)

# ====================================================================================================================    

    if "Handling Missing Data" in multi_function_selector:
        handling_missing_value_option = st.radio("Select What you want to do", ("Drop Null Values", "Filling in Missing Values"))

        if handling_missing_value_option == "Drop Null Values":

            drop_null_values_option = st.radio("Choose your option as suted: ", ("Drop all null value rows", "Only Drop Rows that contanines all null values"))
            droped_null_value = handling_missing_values(data, drop_null_values_option)
            st.write(droped_null_value)
            export_rename_column = download_data(droped_null_value, label="fillna_column")
        
        elif handling_missing_value_option == "Filling in Missing Values":
            
            if 'missing_dict' not in st.session_state:
                st.session_state.missing_dict = {}
            
            fillna_column_selector = st.selectbox("Please Select or Enter a column Name you want to fill the NaN Values: ", options=column_with_null_values)
            fillna_text_data = st.text_input("Enter the New Value for the {} Column NaN Value".format(fillna_column_selector), max_chars=50)

            if st.button("Draft Changes", help="when you want to fill multiple columns/single column null values so first you have to click Save Draft button this updates the data and then press Rename Columns Button."):     
                
                if fillna_column_selector in num_category:
                    try:
                        st.session_state.missing_dict[fillna_column_selector] = float(fillna_text_data)
                    except:
                        st.session_state.missing_dict[fillna_column_selector] = int(fillna_text_data)
                else:
                    st.session_state.missing_dict[fillna_column_selector] = fillna_text_data

            st.code(st.session_state.missing_dict)

            if st.button("Apply Changes", help="Takes your data and Fill NaN Values for columns as your wish."):

                fillna_column = handling_missing_values(data,handling_missing_value_option, st.session_state.missing_dict)
                st.write(fillna_column)
                export_rename_column = download_data(fillna_column, label="fillna_column")
                st.session_state.missing_dict = {}

# ==========================================================================================================================================

    if "Data Wrangling" in multi_function_selector:
        data_wrangling_option = st.radio("Choose your option as suted: ", ("Merging On Index", "Concatenating On Axis"))

        if data_wrangling_option == "Merging On Index":
            data_wrangling_merging_uploaded_file = st.file_uploader("Upload Your Second file you want to merge", type=uploaded_file.name.split(".")[1])

            if data_wrangling_merging_uploaded_file is not None:

                second_data = seconddata(data_wrangling_merging_uploaded_file, file_type=data_wrangling_merging_uploaded_file.type.split("/")[1])
                same_columns = match_elements(data, second_data)
                merge_key_selector = st.selectbox("Select A Comlumn by which you want to merge on two Dataset", options=same_columns)
                
                merge_data = data_wrangling(data, second_data, merge_key_selector, data_wrangling_option)
                st.write(merge_data)
                download_data(merge_data, label="merging_on_index")

        if data_wrangling_option == "Concatenating On Axis":

            data_wrangling_concatenating_uploaded_file = st.file_uploader("Upload Your Second file you want to Concatenate", type=uploaded_file.name.split(".")[1])

            if data_wrangling_concatenating_uploaded_file is not None:

                second_data = seconddata(data_wrangling_concatenating_uploaded_file, file_type=data_wrangling_concatenating_uploaded_file.type.split("/")[1])
                concatenating_data = data_wrangling(data, second_data, None, data_wrangling_option)
                st.write(concatenating_data)
                download_data(concatenating_data, label="concatenating_on_axis")
        
# ==========================================================================================================================================
    st.sidebar.info("After using this app please Click Clear Cache button so that your all data is removed from the folder.")
    if st.sidebar.button("Clear Cache"):
        clear_image_cache()

else:
    with open('samples/sample.zip', 'rb') as f:
        st.sidebar.download_button(
                label="Download Sample Data and Use It",
                data=f,
                file_name='smaple_data.zip',
                help = "Download some sample data and use it to explore this web app."
            )