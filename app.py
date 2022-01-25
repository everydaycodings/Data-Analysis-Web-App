import streamlit as st
from helper import data, describe, outliers

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

    st.subheader("Dataset Description")
    describe, shape, columns, num_category, str_category, null_values = describe(data)
    st.write(describe)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write("Dataset Shape")
        st.write(shape)
        
    with col2:
        st.write("Dataset Columns")
        st.write(columns)
    
    with col3:
        st.write("Numeric Columns")
        st.dataframe(num_category)
    
    with col4:
        st.write("String Columns")
        st.dataframe(str_category)
        
    with col5:
        st.write("Counted Null Values")
        st.dataframe(null_values)

    outliers = outliers(data)
    st.image(outliers)