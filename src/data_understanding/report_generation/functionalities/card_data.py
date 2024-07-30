import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def load_card_data(file):
    return pd.read_csv(file)

def get_unique_cardholders(df):
    return df['cardholder_id'].nunique()

def get_unique_cards(df):
    return df['card_id'].nunique()

def cardholder_card_count(df):
    new_df = df.groupby('cardholder_id')['card_id'].count().reset_index(name='card_id_count')
    value_counts = new_df['card_id_count'].value_counts().reset_index()
    value_counts.columns = ['card_count', 'unique_cardholder_count']
    return value_counts

def daily_cardholder_enrollment(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_7_days = datetime.now() - timedelta(days=7)
    df_last_7_days = df[df['created_at'] >= last_7_days]
    daily_enrollment = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date).size().reset_index(name='count')
    fig = px.bar(daily_enrollment, x='created_at', y='count', title='Daily Cardholder Enrollment for the Last 7 Days')
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of Enrollments')
    return fig
