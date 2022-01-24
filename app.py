import streamlit as st
from helper import data, describe

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



uploaded_file = st.sidebar.file_uploader("Upload Your file")


st.sidebar.title("Data Analysis Web App")

if uploaded_file is not None:
    data = data(uploaded_file)
    st.dataframe(data)
    
    describe = describe(data)
    st.write(describe)