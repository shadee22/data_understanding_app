import streamlit as st
import pandas as pd
from functionalities.card_data import load_card_data, get_unique_cardholders, get_unique_cards, cardholder_card_count, daily_cardholder_enrollment
from functionalities.transaction_data import load_transaction_data, transaction_metrics
from functionalities.redemption_data import load_redemption_data, redemption_metrics, daily_redemptions_value, daily_redemptions_count, merchant_wise_redemption
from functionalities import top_issuers
from datetime import datetime
import pytz
import os
import plotly.express as px
from other.helper_components  import spacer

def generate_header_text(base_text, session_key):
    return f"**{base_text} (Generated at: {st.session_state[session_key]} JST)**" if session_key in st.session_state and st.session_state[session_key] else base_text

# Initialize session state variables if they don't exist
if 'generated_cardholder' not in st.session_state:
    st.session_state['generated_cardholder'] = ''
if 'generated_transactions' not in st.session_state:
    st.session_state['generated_transactions'] = ''
if 'generated_redemptions' not in st.session_state:
    st.session_state['generated_redemptions'] = ''

tab1, tab2 = st.sidebar.tabs(["Upload Data Files", "Generated Time"])

with tab1:
    st.header('Upload Data Files')
    card_data = st.file_uploader("Upload Card Data", type=['csv'])
    transaction_data = st.file_uploader("Upload Transaction Data", type=['csv'])
    redemption_data = st.file_uploader("Upload Redemption Data", type=['csv'])

with tab2:
    st.header('Data Source Generated Time ')
    st.session_state['generated_cardholder'] = st.text_input("Generated Cardholder Time", value=st.session_state['generated_cardholder'])
    st.session_state['generated_transactions'] = st.text_input("Generated Transactions Time", value=st.session_state['generated_transactions'])
    st.session_state['generated_redemptions'] = st.text_input("Generated Redemptions Time", value=st.session_state['generated_redemptions'])
    st.markdown('[Time Converter](https://savvytime.com/converter/sri-lanka-colombo-to-japan-ueno-ebisumachi)')

if card_data and transaction_data and redemption_data:
    card_df = load_card_data(card_data)
    transaction_df = load_transaction_data(transaction_data)
    redemption_df = load_redemption_data(redemption_data)

    num_unique_cardholders = get_unique_cardholders(card_df)
    num_unique_cards = get_unique_cards(card_df)
    value_counts = cardholder_card_count(card_df)

    current_date = datetime.now().strftime("%B %d, %Y")

    st.image('./other/assets/banner+pulse+id.png')
    st.title(f"VISA Japan Campaign Analysis {current_date}")

    st.header(generate_header_text("Card and Cardholder Information Analysis", 'generated_cardholder'))
    st.write(f"Number of unique Cardholders: **{num_unique_cardholders:,}**")
    st.write(f"Number of unique Cards: **{num_unique_cards:,}**")
    st.header("Card Count Analysis (Cards per Cardholder)")
    # rename column name
    value_counts = value_counts.rename(columns={'card_count': 'Card Count'})
    value_counts = value_counts.rename(columns={'unique_cardholder_count': 'Unique Cardholder Count'})
    value_counts['Percentage'] = (value_counts['Unique Cardholder Count'] / value_counts['Unique Cardholder Count'].sum()) * 100
    value_counts['Percentage'] = value_counts['Percentage'].apply(lambda x: f"{x:.2f}%")
    st.dataframe(value_counts, use_container_width=True, hide_index=True)

    spacer(1)
    fig2 = px.pie(value_counts, values="Unique Cardholder Count", names="Card Count", title="Cardholder Distribution by Card Count", hole=0.5)
    st.plotly_chart(fig2)
    st.plotly_chart(daily_cardholder_enrollment(card_df))
    
    spacer(1)

    st.header("Top Issuer Analysis")
    grouped_df = top_issuers.top_issuer_analysis(card_df=card_df)
    grouped_df = grouped_df.rename(columns={'card_id_count': 'Card Count'})

    st.dataframe(grouped_df, use_container_width=True, hide_index=True)
    # st.table(grouped_df.reset_index(drop=True))
    grouped_df = grouped_df.sort_values(by='Card Count', ascending=True)

    spacer(1)
    st.divider()
    fig3 = px.bar(grouped_df, x="Card Count", y="Bank Name", orientation='h', title="Card ID Counts by Top Issuers")
    st.plotly_chart(fig3, use_container_width=True)
    
    st.header(generate_header_text("Transaction Analysis", 'generated_transactions'))
    transaction_metrics_df = transaction_metrics(transaction_df)
    st.dataframe(transaction_metrics_df, use_container_width=True, hide_index=True)

    st.header(generate_header_text("Redemption Analysis", 'generated_redemptions'))
    redemption_metrics_df = redemption_metrics(redemption_df)
    st.dataframe(redemption_metrics_df, use_container_width=True, hide_index=True)
    st.divider()

    st.plotly_chart(daily_redemptions_value(redemption_df))
    st.plotly_chart(daily_redemptions_count(redemption_df))

    spacer(1)
    st.header(generate_header_text("Merchant-wise Total Redemption Analysis", 'generated_redemptions'))
    merchant_redemptions_df = merchant_wise_redemption(redemption_df)
    st.dataframe(merchant_redemptions_df, use_container_width=True, hide_index=True)

    fig = px.bar(merchant_redemptions_df, x="Merchant Name", y="Sum of cashback", title="Total Redemption by Merchants")
    st.plotly_chart(fig)
