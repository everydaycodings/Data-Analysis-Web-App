from cmath import nan
import streamlit as st
from helper import data, describe, outliers, drop_items, download_data, filter_data, num_filter_data, rename_columns
import numpy as np

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
uploaded_file = st.sidebar.file_uploader("Upload Your file")



if uploaded_file is not None:
    data = data(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(data)

    st.text(" ")
    st.text(" ")
    st.text(" ")

    st.subheader("Dataset Description")
    describe, shape, columns, num_category, str_category, null_values, dtypes, unique, str_category= describe(data)
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

    #outliers = outliers(data)
    #for i in range(len(outliers)):
    #    st.image(outliers[i])

    #multiselected_drop = st.multiselect("Please Type or select one or Multipe Columns you want to drop: ", data.columns)
    #droped = drop_items(data, multiselected_drop)
    #st.write(droped)
    #drop_export = download_data(droped, label="Droped")

# =====================================================================================================================================

    #filter_column_selection = st.selectbox("Please Select or Enter a column Name: ", options=data.columns)
    #filtered_value_selection = st.multiselect("Enter Name or Select the value which you don't want in your {} column(You can choose multiple values): ".format(filter_column_selection), data[filter_column_selection].unique())
    #filtered_data = filter_data(data, filter_column_selection, filtered_value_selection)
    #st.write(filtered_data)
    #filtered_export = download_data(filtered_data, label="filtered")

# =============================================================================================================================

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
    if 'rename_dict' not in st.session_state:
        st.session_state.rename_dict = {}

    rename_dict = {}
    rename_column_selector = st.selectbox("Please Select or Enter a column Name you want to rename: ", options=data.columns)
    rename_text_data = st.text_input("Enter the New Name for the {} column".format(rename_column_selector), max_chars=50)

    if rename_text_data != "":

        if st.button("Draft Changes", help="when you want to rename multiple columns/single column  so first you have to click Save Draft button this updates the data and then press Rename Columns Button."):
            st.session_state.rename_dict[rename_column_selector] = rename_text_data
        st.code(st.session_state.rename_dict)

        if st.button("Rename Columns", help="Takes your data and rename the column as your wish."):
            rename_column = rename_columns(data, st.session_state.rename_dict)
            st.write(rename_column)
            export_rename_column = download_data(rename_column, label="rename_column")
            st.session_state.rename_dict = {}

# ===================================================================================================================
 
    multi_bar_plotting = st.multiselect("Enter Name or Select the Column which you Want To Plot: ", str_category)
    for i in range(len(multi_bar_plotting)):
        column = multi_bar_plotting[i]
        st.markdown("#### Bar Plot for {} column".format(column))
        bar_plot = data[column].value_counts().reset_index().sort_values(by=column, ascending=False)
        st.bar_chart(bar_plot)