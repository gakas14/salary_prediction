from predict_page import show_predict_page
import streamlit as st
from explore_page import show_explore_page


# set page width

st.sidebar.markdown("<div> <img src='https://mrinalusc.files.wordpress.com/2020/12/capture.png' width=300/> <h1 style='display:inline-block'> Salary Analysis </h1> </div>", unsafe_allow_html=True)
st.sidebar.markdown("This page allows us to  Explore software engineer salaries and also make a Salary Prediction base on Country, Education level, Age, and Year of experience.")
page = st.sidebar.selectbox("To get Started Select Explore Or Predict", ("Predict", "Explore"))

if page == 'Predict':
    show_predict_page()
else:
    show_explore_page()







