import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title='Netlix Dashboard', layout='wide')
st.header('Netflix Dashboard')

def load_data():
    df = pd.read_csv(r"C:\Users\Karan\Downloads\netflix_titles.csv")
    # st.write(df)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

st.sidebar.header('Dashboard Filters')
content_type = st.sidebar.multiselect(label='Content Type', options=df['type'].dropna().unique(), default=df['type'].dropna().unique())
country = st.sidebar.multiselect(label='Country', options=df['country'].str.split(',').explode().replace('',np.nan).dropna().str.strip()
                                 .sort_values().unique())
rating = st.sidebar.multiselect(label='Rating', options=df['rating'].dropna().sort_values().unique())
relyear = st.sidebar.slider(label='Release Year', min_value=df['release_year'].min(), max_value=df['release_year'].max(), value=(2000,2020))

#filtering data
fil_df = df[df['type'].isin(content_type)]
if country:
    fil_df = fil_df[fil_df['country'].apply(lambda x: any(c.strip() in country for c in x.split(',')) if isinstance(x, str) else False)] 
    #fil_df = fil_df[fil_df['country'].isin(country)] ^^ the above checks for movies/tv shows that are in multiple countries
if rating:
    fil_df = fil_df[fil_df['rating'].isin(rating)]
if relyear:
    fil_df = fil_df[(fil_df['release_year'] >= relyear[0]) & (fil_df['release_year'] <= relyear[1])]

#key metrics
col1, col2, col3, col4 = st.columns(4)
total_titles = len(fil_df)
total_country = len(country)
total_movie = len(fil_df[fil_df['type']=='Movie'])
total_shows = len(fil_df[fil_df['type']=='TV Show'])
col1.metric('Total Titles', total_titles)
col2.metric('Movies', total_movie)
col3.metric('TV Shows', total_shows)
col4.metric('Countries', total_country)
st.divider()

col1,col2 = st.columns(2)
with col1:
    st.subheader('Movies vs TV Shows')
    data = fil_df['type'].value_counts()
    fig = px.pie(data, names=data.index, values=data.values, color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig, width='stretch')

with col2:
    st.subheader('Content Added Over Years')
    data = fil_df['release_year'].value_counts().sort_index()
    fig = px.line(data, x= data.index, y=data.values, markers=True)
    fig.update_layout(xaxis_title='Years',yaxis_title='Titles')
    st.plotly_chart(fig, width='stretch')