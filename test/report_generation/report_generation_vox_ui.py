import streamlit as st
import pandas as pd
from functionalities.card_data import load_card_data, get_unique_cardholders, get_unique_cards, cardholder_card_count, daily_cardholder_enrollment
from functionalities.transaction_data import load_transaction_data, transaction_metrics
from functionalities.redemption_data import load_redemption_data, redemption_metrics, daily_redemptions_value, daily_redemptions_count, merchant_wise_redemption
from functionalities import top_issuers
from datetime import datetime
import pytz
import os

def get_file_created_time(csv_file_path):
    created_time = os.path.getctime(csv_file_path)
    created_time_dt = datetime.utcfromtimestamp(created_time)
    sri_lanka_tz = pytz.timezone('Asia/Colombo')
    japan_tz = pytz.timezone('Asia/Tokyo')
    created_time_utc = pytz.utc.localize(created_time_dt)
    created_time_sl = created_time_utc.astimezone(sri_lanka_tz)
    created_time_jp = created_time_sl.astimezone(japan_tz)
    return created_time_jp

st.sidebar.header('Upload Data Files')
card_data = st.sidebar.file_uploader("Upload Card Data", type=['csv'])
transaction_data = st.sidebar.file_uploader("Upload Transaction Data", type=['csv'])
redemption_data = st.sidebar.file_uploader("Upload Redemption Data", type=['csv'])

if card_data and transaction_data and redemption_data:
    card_df = load_card_data(card_data)
    transaction_df = load_transaction_data(transaction_data)
    redemption_df = load_redemption_data(redemption_data)

    num_unique_cardholders = get_unique_cardholders(card_df)
    num_unique_cards = get_unique_cards(card_df)
    value_counts = cardholder_card_count(card_df)

    a_time = get_file_created_time("../../data/visa_3/Visa Japan Cards.csv")
    formatted_time = a_time.strftime("%I:%M %p")
    st.title("VISA Japan Campaign Analysis July 25 2024")
    st.markdown("**Report generated Date: 2024 July 25**")
    st.markdown("**Card and Cardholder Information Analysis (Generated at: 12:13 pm JST)**")
    st.write(f"Number of unique Cardholders: **{num_unique_cardholders}**")
    st.write(f"Number of unique Cards: **{num_unique_cards}**")

    st.header("Card Count Analysis (Cards per Cardholder)")
    st.dataframe(value_counts)
    fig2 = px.pie(value_counts, values="unique_cardholder_count", names="card_count", title="Cardholder Distribution by Card Count", hole=0.5)
    st.plotly_chart(fig2)
    st.plotly_chart(daily_cardholder_enrollment(card_df))

    st.header("Top Issuer Analysis (Generated at: 12:13 pm JST)")
    grouped_df = top_issuers.top_issuer_analysis(card_df=card_df)
    st.dataframe(grouped_df)
    fig3 = px.bar(grouped_df, x="card_id_count", y="Bank Name", orientation='h', title="Card ID Counts by Top Issuers")
    st.plotly_chart(fig3, use_container_width=True)

    st.header("Transaction Analysis (Generated at: 12:13 pm JST)")
    transaction_metrics_df = transaction_metrics(transaction_df)
    st.dataframe(transaction_metrics_df)

    st.header("Redemption Analysis (Generated at: 12:13 pm JST)")
    redemption_metrics_df = redemption_metrics(redemption_df)
    st.dataframe(redemption_metrics_df)
    st.plotly_chart(daily_redemptions_value(redemption_df))
    st.plotly_chart(daily_redemptions_count(redemption_df))

    st.header("Merchant-wise Total Redemption Analysis (Generated at: 12:14 pm JST)")
    merchant_redemptions_df = merchant_wise_redemption(redemption_df)
    st.table(merchant_redemptions_df)
    fig = px.bar(merchant_redemptions_df, x="Merchant Name", y="Sum of cashback", title="Total Redemption by Merchants")
    st.plotly_chart(fig)
