import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import os
from functionalities import top_issuers


def get_file_created_time(csv_file_path):
    created_time = os.path.getctime(csv_file_path)
    created_time_dt = datetime.utcfromtimestamp(created_time)
    sri_lanka_tz = pytz.timezone('Asia/Colombo')
    japan_tz = pytz.timezone('Asia/Tokyo')
    created_time_utc = pytz.utc.localize(created_time_dt)
    created_time_sl = created_time_utc.astimezone(sri_lanka_tz)
    created_time_jp = created_time_sl.astimezone(japan_tz)
    return created_time_jp

def daily_cardholder_enrollment(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_7_days = datetime.now() - timedelta(days=7)
    df_last_7_days = df[df['created_at'] >= last_7_days]
    daily_enrollment = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date).size().reset_index(name='count')
    fig = px.bar(daily_enrollment, x='created_at', y='count', title='Daily Cardholder Enrollment for the Last 7 Days')
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of Enrollments')
    return fig

def daily_redemptions_value(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_7_days = datetime.now() - timedelta(days=7)
    df_last_7_days = df[df['created_at'] >= last_7_days]
    daily_redemptions = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date)['cashback_amount'].sum().reset_index(name='total_value')
    fig = px.bar(daily_redemptions, x='created_at', y='total_value', title='Daily Redemptions Value for the Last 7 Days')
    fig.update_layout(xaxis_title='Date', yaxis_title='Total Redemption Value')
    return fig

def daily_redemptions_count(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_7_days = datetime.now() - timedelta(days=7)
    df_last_7_days = df[df['created_at'] >= last_7_days]
    daily_redemptions = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date).size().reset_index(name='count')
    fig = px.bar(daily_redemptions, x='created_at', y='count', title='Daily Redemptions Count for the Last 7 Days')
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of Redemptions')
    return fig

st.sidebar.header('Upload Data Files')
card_data = st.sidebar.file_uploader("Upload Card Data", type=['csv'])
transaction_data = st.sidebar.file_uploader("Upload Transaction Data", type=['csv'])
redemption_data = st.sidebar.file_uploader("Upload Redemption Data", type=['csv'])

if card_data and transaction_data and redemption_data:
    card_df = pd.read_csv(card_data)
    transaction_df = pd.read_csv(transaction_data)
    redemption_df = pd.read_csv(redemption_data)

    num_unique_cardholders = card_df['cardholder_id'].nunique()
    num_unique_cards = card_df['card_id'].nunique()
    new_df = card_df.groupby('cardholder_id')['card_id'].count().reset_index(name='card_id_count')
    value_counts = new_df['card_id_count'].value_counts().reset_index()
    value_counts.columns = ['card_count', 'unique_cardholder_count']

    a_time = get_file_created_time("../../data/visa_3/Visa Japan Cards.csv")
    formatted_time = a_time.strftime("%I:%M %p")
    st.title("VISA Japan Campaign Analysis July 25 2024")
    st.markdown("**Report generated Date: 2024 July 25**")
    st.markdown("**Card and Cardholder Information Analysis (Generated at: 12:13 pm JST)**")
    st.write(f"Number of unique Cardholders: **{num_unique_cardholders}**")
    st.write(f"Number of unique Cards: **{num_unique_cards}**")

    # Card Count Analysis
    st.header("Card Count Analysis (Cards per Cardholder)")
    st.dataframe(value_counts)
    
    fig2 = px.pie(value_counts, values="unique_cardholder_count", names="card_count", title="Cardholder Distribution by Card Count", hole=0.5)
    st.plotly_chart(fig2)
    
    st.plotly_chart(daily_cardholder_enrollment(card_df))

    # Top Issuer Analysis
    st.header("Top Issuer Analysis (Generated at: 12:13 pm JST)")
    grouped_df = top_issuers.top_issuer_analysis(card_df=card_df)

    st.dataframe(grouped_df)
    fig3 = px.bar(grouped_df, x="card_id_count", y="Bank Name", orientation='h', title="Card ID Counts by Top Issuers")
    st.plotly_chart(fig3, use_container_width=True)

    # Transaction Analysis
    st.header("Transaction Analysis (Generated at: 12:13 pm JST)")
    metrics_data = {
        'Metrics': [
            'Authorized & Eligible Total Transaction Count',
            'Authorized & Eligible Total Transaction Value',
            'Authorized & Eligible Average Transaction Value',
            'Authorized & Eligible Total Cashback',
            'Authorized & Eligible Average Cashback'
        ],
        'Value': [
            str(int(transaction_df['transaction_id'].nunique())),
            '¥' + str(int(transaction_df['transaction_amount'].sum())),
            '¥' + str(round(transaction_df['transaction_amount'].mean(), 2)),
            '¥' + str(int(transaction_df['cashback_amount'].sum())),
            '¥' + str(round(transaction_df['cashback_amount'].mean(), 2))
        ]
    }
    transaction_metrics_df = pd.DataFrame(metrics_data)
    st.dataframe(transaction_metrics_df)

    # Redemption Analysis
    st.header("Redemption Analysis (Generated at: 12:13 pm JST)")
    redemption_metrics_data = {
        'Metrics': [
            'Total Redemption Count',
            'Total Cashback Given',
            'Average Cashback Given'
        ],
        'Value': [
            str(int(redemption_df['transaction_id'].nunique())),
            '¥' + str(int(redemption_df['cashback_amount'].sum())),
            '¥' + str(round(redemption_df['cashback_amount'].mean(), 2))
        ]
    }
    redemption_metrics_df = pd.DataFrame(redemption_metrics_data)
    st.dataframe(redemption_metrics_df)

    st.plotly_chart(daily_redemptions_value(redemption_df))

    st.plotly_chart(daily_redemptions_count(redemption_df))

    # Merchant-wise Total Redemption Analysis
    st.header("Merchant-wise Total Redemption Analysis (Generated at: 12:14 pm JST)")
    new_df = redemption_df.groupby('name')['cashback_amount'].sum().reset_index()
    new_df.columns = ['Merchant Name', 'Sum of cashback']
    new_df = new_df.sort_values(by='Sum of cashback', ascending=False)
    st.table(new_df)
    fig = px.bar(new_df, x="Merchant Name", y="Sum of cashback", title="Total Redemption by Merchants")
    st.plotly_chart(fig)