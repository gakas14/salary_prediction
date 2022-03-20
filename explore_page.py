import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os.path


st.set_page_config(layout='wide')


def country_cutoff(column, cutoff_num):
    categories_map = dict()
    for i in range(len(column)):
        if column.values[i] >= cutoff_num:
            categories_map[column.index[i]] = column.index[i]
        else:
            categories_map[column.index[i]] = 'Other'
    return categories_map


def clean_year_of_coding(year):
    if year == 'More than 50 years':
        return 50
    if year == 'Less than 1 year':
        return 0.5
    return float(year)


def clean_education(edu):
    if 'Bachelor’s degree'in edu:
        return 'Bachelor’s degree'
    elif 'Master’s degree' in edu:
        return 'Master’s degree'
    elif 'Professional degree'in edu or 'doctoral degree' in edu:
        return 'Post grad'
    else:
        return 'Less than a Bachelors'


# Let's clean the country's name
def clean_country_name(name):
    if name == 'Iran, Islamic Republic of...':
        return 'Iran'
    elif name == 'United Kingdom of Great Britain and Northern Ireland':
        return 'UK'
    elif name == 'Russian Federation':
        return 'Russia'
    elif name == 'United States of America':
        return 'USA'
    else:
        return name


# Let's replace Prefer not to say to the mode age
def age_replace(age, m):
    if age == 'Prefer not to say':
        # print(age)
        return m
    else:
        return age


# Function to load the dataframe
@st.cache
def load_file():
    df = pd.read_csv('survey_results_public.csv')

    # Select only the follow 6 conlumns to do the prediction
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly', 'Age']]
    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)

    # Drop the missing entries in salary
    df = df[df['Salary'].notnull()]
    df = df.dropna()

    # Keep only entries with full-time
    df = df[df['Employment'] == 'Employed full-time']
    df = df.drop('Employment', axis=1)

    # Cut of the countries with less then 250 entries
    country_map = country_cutoff(df['Country'].value_counts(), 250)
    df['Country'] = df['Country'].map(country_map)

    # Remove outliers where salary is bigger than 200000 and smaller the 10000
    df = df[df.Salary <= 200000]
    df = df[df.Salary > 10000]
    df = df[df['Country'] != 'Other']

    #  Call the function to clean the codding years
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_year_of_coding)
    df.EdLevel = df.EdLevel.apply(clean_education)

    # call clean country name function
    df.Country = df.Country.apply(clean_country_name)

    # Call the function to replace ''Prefer not to say'' in age column
    m = df['Age'].mode()[0]
    df.Age = df.Age.apply(lambda x: age_replace(x, m))

    return df


#df = pd.read_csv('clean_survey_results_public.csv')
#st.write(df)
if os.path.exists('survey_results_public.csv'):
    df = load_file()

    #st.write('file exist')
else:
    #st.write('file does not exist')
    df = pd.read_csv('clean_survey_results_public.csv')
   


def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write("""### Stack Overflow Developer Survey 2020 """)

    data = df['Country'].value_counts()

    #plot a pie chart
    #fig1, ax1 = plt.subplots()
    #ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    #ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Plot pie chart with plotly
    fig1 = px.pie(data, values=data.values, names=data.index, hole=0.1, height=600, title='Data entries by country')
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

    #st.write(""" ### Number of Data from different countries""")
    #st.pyplot(fig1)

    # Add Bar chart
    st.write(""" 
    ### Mean Salary Based On Country 
    """)

    data = round(df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True), 1)
    #st.write(data)

    fig2 = px.bar(data, x=data.index, y=data.values, labels={'y': 'Salary in $'}, color=data.values, height=600)

    #st.bar_chart(data)
    st.plotly_chart(fig2, use_container_width=True)



    # Add line chart
    st.write("""
    ### Mean Salary Based On Experience
    """)

    line_data = round(df.groupby(['YearsCodePro'])['Salary'].mean(), 1)
    line_data.index = line_data.index.sort_values(ascending=True)
    #st.line_chart(data, use_container_width=True)

    # Line chart with plotly
    fig3 = px.line(line_data, x=line_data.index, y='Salary', markers=True, height=600)
    st.plotly_chart(fig3, use_container_width=True)
