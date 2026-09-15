import streamlit as st
import pandas as pd
import plotly.express as pt

st.set_page_config(page_title='Netlix Dashboard', layout='wide')
st.header('Netflix Dashboard')

def load_data():
    df = pd.read_csv(r"C:\Users\Karan\Downloads\netflix_titles.csv")
    # st.write(df)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()