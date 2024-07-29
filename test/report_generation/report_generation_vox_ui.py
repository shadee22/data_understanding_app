import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pytz
import os
from io import BytesIO
import matplotlib.ticker as ticker

# Function to get the file created time in JST
def get_file_created_time(csv_file_path):
    created_time = os.path.getctime(csv_file_path)
    created_time_dt = datetime.utcfromtimestamp(created_time)
    sri_lanka_tz = pytz.timezone('Asia/Colombo')
    japan_tz = pytz.timezone('Asia/Tokyo')
    created_time_utc = pytz.utc.localize(created_time_dt)
    created_time_sl = created_time_utc.astimezone(sri_lanka_tz)
    created_time_jp = created_time_sl.astimezone(japan_tz)
    return created_time_jp

# Function to generate daily cardholder enrollment plot
def daily_cardholder_enrollment(df, filename='./plots/daily_enrollment_plot.png'):
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_7_days = datetime.now() - timedelta(days=7)
    df_last_7_days = df[df['created_at'] >= last_7_days]
    daily_enrollment = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date).size()
    plt.figure(figsize=(10, 6))
    ax = daily_enrollment.plot(kind='bar', color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Number of Enrollments')
    plt.title('Daily Cardholder Enrollment for the Last 7 Days')
    plt.xticks(rotation=45)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.tight_layout()
    plt.savefig(filename)

# Function to generate daily redemptions value plot
def daily_redemptions_value(df, filename='./plots/daily_redemptions_value_plot.png'):
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_7_days = datetime.now() - timedelta(days=7)
    df_last_7_days = df[df['created_at'] >= last_7_days]
    daily_redemptions = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date)['cashback_amount'].sum()
    plt.figure(figsize=(10, 6))
    ax = daily_redemptions.plot(kind='bar', color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Total Redemption Value')
    plt.title('Daily Redemptions Value for the Last 7 Days')
    plt.xticks(rotation=45)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.tight_layout()
    plt.savefig(filename)

# Function to generate daily redemptions count plot
def daily_redemptions_count(df, filename='./plots/daily_redemptions_count_plot.png'):
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_7_days = datetime.now() - timedelta(days=7)
    df_last_7_days = df[df['created_at'] >= last_7_days]
    daily_redemptions = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date).size()
    plt.figure(figsize=(10, 6))
    ax = daily_redemptions.plot(kind='bar', color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Number of Redemptions')
    plt.title('Daily Redemptions Count for the Last 7 Days')
    plt.xticks(rotation=45)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.tight_layout()
    plt.savefig(filename)

# Add file input for card data
st.sidebar.header('Upload Data Files')
card_data = st.sidebar.file_uploader("Upload Card Data", type=['csv'])
# Add file input for transaction data
transaction_data = st.sidebar.file_uploader("Upload Transaction Data", type=['csv'])
# Add file input for redemption data
redemption_data = st.sidebar.file_uploader("Upload Redemption Data", type=['csv'])

if card_data and transaction_data and redemption_data:
    card_df = pd.read_csv(card_data)
    transaction_df = pd.read_csv(transaction_data)
    redemption_df = pd.read_csv(redemption_data)

    # Generate the required plots
    daily_cardholder_enrollment(card_df)
    daily_redemptions_value(redemption_df)
    daily_redemptions_count(redemption_df)

    # Process and display the data
    num_unique_cardholders = card_df['cardholder_id'].nunique()
    num_unique_cards = card_df['card_id'].nunique()
    new_df = card_df.groupby('cardholder_id')['card_id'].count().reset_index(name='card_id_count')
    value_counts = new_df['card_id_count'].value_counts().reset_index()
    value_counts.columns = ['card_count', 'unique_cardholder_count']

    st.title("VISA Japan Campaign Analysis July 25 2024")
    st.markdown("**Report generated Date: 2024 July 25**")
    st.markdown("**Card and Cardholder Information Analysis (Generated at: 12:13 pm JST)**")
    st.write(f"Number of unique Cardholders: **{num_unique_cardholders}**")
    st.write(f"Number of unique Cards: **{num_unique_cards}**")

    # Card Count Analysis
    st.header("Card Count Analysis (Cards per Cardholder)")
    st.table(value_counts)

    # Cardholder Distribution by Card Count Pie Chart
    fig = px.pie(value_counts, values="unique_cardholder_count", names="card_count", title="Cardholder Distribution by Card Count")
    st.plotly_chart(fig)

    # Top Issuer Analysis
    st.header("Top Issuer Analysis (Generated at: 12:13 pm JST)")
    new_df = card_df.groupby('issuer_bin')['card_id'].nunique().reset_index(name='card_id_count')
    new_df = new_df.sort_values(by='card_id_count', ascending=False)
    new_df["issuer_bin"] = new_df["issuer_bin"].astype(str)
    new_df["first_4_digits"] = new_df["issuer_bin"].str[:4]
    grouped_df = new_df.groupby("first_4_digits")["card_id_count"].sum().reset_index()
    grouped_df = grouped_df.sort_values(by="card_id_count", ascending=False).reset_index(drop=True)
    bank_mapping = {
        '4980': 'Sumitomo Mitsui Card Company Limited',
        '4708': 'YES BANK, LTD.',
        '4297': 'RAKUTEN KC CO., LTD.',
        '4537': 'WELLS FARGO BANK, N.A.',
        '4205': 'AEON CREDIT SERVICE CO., LTD.',
        '4534': 'DC CARD CO., LTD.',
        '4541': 'REDIT SAISON CO., LTD.',
        '4363': 'UNITED COMMERCIAL BANK',
        '4649': 'YAMAGIN CREDIT CO., LTD.',
        '4616': 'U.S. BANK N.A. ND',
        '4986': 'MITSUBISHI UFJ FINANCIAL GROUP, INC.',
        '4539': 'OSTGIROT BANK AB',
        '4097': 'CAJA AHORROS GERONA',
        '4924': 'BANK OF AMERICA, N.A.',
        '4987': 'YAMAGIN CREDIT CO., LTD.',
        '4162': 'UNKNOWN',
        '4721': 'WELLS FARGO BANK IOWA, N.A.',
        '4538': 'MITSUBISHI UFJ FINANCIAL GROUP, INC.',
        '4984': 'BANCO DO BRASIL, S.A.',
        '4122': 'UNITED BANK, LTD.',
        '4901': 'OMC CARD, INC.'
    }
    grouped_df['Bank Name'] = grouped_df['first_4_digits'].map(bank_mapping)
    grouped_df = grouped_df[['Bank Name', 'card_id_count']][:10]
    st.table(grouped_df)

    fig = px.bar(grouped_df, x="card_id_count", y="Bank Name", orientation='h', title="Card ID Counts by Top Issuers")
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)

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
    st.table(transaction_metrics_df)

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
    st.table(redemption_metrics_df)

    # Daily Redemptions for last 7 days
    st.header("Daily Redemptions for last 7 days")
    daily_redemptions_value_plot = "daily_redemptions_value_plot.png"
    if os.path.exists(daily_redemptions_value_plot):
        st.image(daily_redemptions_value_plot)

    st.header("Daily Redemption Count for last 7 days")
    daily_redemptions_count_plot = "daily_redemptions_count_plot.png"
    if os.path.exists(daily_redemptions_count_plot):
        st.image(daily_redemptions_count_plot)

    # Merchant-wise Total Redemption Analysis
    st.header("Merchant-wise Total Redemption Analysis (Generated at: 12:14 pm JST)")
    new_df = redemption_df.groupby('name')['cashback_amount'].sum().reset_index()
    new_df.columns = ['Merchant Name', 'Sum of cashback']
    new_df = new_df.sort_values(by='Sum of cashback', ascending=False)
    st.table(new_df)
    fig = px.bar(new_df, x="Merchant Name", y="Sum of cashback", title="Total Redemption by Merchants")
    st.plotly_chart(fig)