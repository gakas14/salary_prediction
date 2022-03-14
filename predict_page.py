import streamlit as st
import pickle
import numpy as np


# Load the model
def load_model():
    with open('save_step.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()
regressor = data['model']
country_label = data['le_country']
edu_label = data['le_education']
age_label = data['le_age']


def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary """)

    countries = ('Sweden', 'Spain', 'Germany', 'Turkey', 'Canada', 'France',
       'Switzerland', 'UK', 'Ruassia', 'Israel', 'Ukraine', 'USA',
       'Brazil', 'Greece', 'Italy', 'Netherlands', 'Poland', 'Austria',
       'Romania', 'Australia', 'Belgium', 'Iran', 'India', 'Denmark',
       'Finland', 'Argentina', 'Portugal', 'South Africa', 'Pakistan',
       'Norway', 'Czech Republic', 'China', 'Mexico', 'New Zealand')

    educations = ('Master’s degree', 'Bachelor’s degree', 'Less than a Bachelors',
       'Post grad')

    ages= ('Under 18 years old','18-24 years old', '25-34 years old', '35-44 years old', '45-54 years old',
       '55-64 years old', '65 years or older')

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", educations)
    age = st.selectbox("Age Range", ages)

    experience = st.slider("Years of Experience", 0, 50, 2)



    calculate = st.button("Calculate Salary")

    if calculate:
        x = np.array([[country, education, experience, age]])
        x[:, 0] = country_label.transform(x[:, 0])
        x[:, 1] = edu_label.transform(x[:, 1])
        x[:, 3] = age_label.transform(x[:, 3])
        x = x.astype(float)

        salary = regressor.predict(x)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")







