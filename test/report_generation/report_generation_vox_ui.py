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

def get_file_created_time(uploaded_file):
    # Save the uploaded file temporarily to access its metadata
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Get the absolute path of the saved file
    file_path = os.path.abspath(uploaded_file.name)
    
    created_time = os.path.getctime(file_path)
    created_time_dt = datetime.utcfromtimestamp(created_time)
    sri_lanka_tz = pytz.timezone('Asia/Colombo')
    japan_tz = pytz.timezone('Asia/Tokyo')
    created_time_utc = pytz.utc.localize(created_time_dt)
    created_time_sl = created_time_utc.astimezone(sri_lanka_tz)
    created_time_jp = created_time_sl.astimezone(japan_tz)
    
    # Clean up the temporary file
    os.remove(file_path)
    
    return created_time_jp

# Initialize session state variables if they don't exist
if 'generated_cardholder' not in st.session_state:
    st.session_state['generated_cardholder'] = ''
if 'generated_transactions' not in st.session_state:
    st.session_state['generated_transactions'] = ''
if 'generated_redemptions' not in st.session_state:
    st.session_state['generated_redemptions'] = ''

tab1, tab2 = st.sidebar.tabs(["Upload Data Files", "Generated Time"])

# First tab for uploading data files
with tab1:
    st.header('Upload Data Files')
    card_data = st.file_uploader("Upload Card Data", type=['csv'])
    transaction_data = st.file_uploader("Upload Transaction Data", type=['csv'])
    redemption_data = st.file_uploader("Upload Redemption Data", type=['csv'])


def update_ui(input_text):
    st.write(f"You typed: {input_text}")
    
    
with tab2:
    st.header('Data Source Generated Time ')

    # Update session state directly for real-time effect
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

    # Use the uploaded card data file to get the creation time
    a_time = get_file_created_time(card_data)
    formatted_time = a_time.strftime("%I:%M %p %Z")
    
    # Get the current date
    current_date = datetime.now().strftime("%B %d, %Y")

    st.image('./other/assets/banner+pulse+id.png')  
    
    st.title(f"VISA Japan Campaign Analysis {current_date}")
    
    header_text = f"**Card and Cardholder Information Analysis (Generated at: {st.session_state['generated_cardholder']} JST)**" if 'generated_cardholder' in st.session_state and st.session_state['generated_cardholder'] else "Card and Cardholder Information Analysis"
    st.header(header_text)
        
        
    st.write(f"Number of unique Cardholders: **{num_unique_cardholders}**")
    st.write(f"Number of unique Cards: **{num_unique_cards}**")

    st.header("Card Count Analysis (Cards per Cardholder)")
    st.dataframe(value_counts, use_container_width=True)
    
    # SPACING
    st.write("#")
    st.write("#")
    
    fig2 = px.pie(value_counts, values="unique_cardholder_count", names="card_count", title="Cardholder Distribution by Card Count", hole=0.5)
    st.plotly_chart(fig2)
    st.plotly_chart(daily_cardholder_enrollment(card_df))

    # SPACING
    st.write("#")

    st.header(f"Top Issuer Analysis")
    grouped_df = top_issuers.top_issuer_analysis(card_df=card_df)
    st.dataframe(grouped_df, use_container_width=True)
    fig3 = px.bar(grouped_df, x="card_id_count", y="Bank Name", orientation='h', title="Card ID Counts by Top Issuers")
    st.plotly_chart(fig3, use_container_width=True)

    # SPACING
    st.write("#")

    header_text = f"**Transaction Analysis (Generated at: {st.session_state['generated_transactions']} JST)**" if 'generated_transactions' in st.session_state and st.session_state['generated_transactions'] else "Transaction Analysis"
    st.header(header_text)

    # st.header(f"Transaction Analysis (Generated at: {st.session_state['generated_transactions']} JST)")
    transaction_metrics_df = transaction_metrics(transaction_df)
    st.dataframe(transaction_metrics_df, use_container_width=True)

    # SPACING
    st.write("#")

    header_text = f"**Redemption Analysis (Generated at: {st.session_state['generated_redemptions']} JST)**" if 'generated_redemptions' in st.session_state and st.session_state['generated_redemptions'] else "Redemption Analysis"
    st.header(header_text)

    # st.header(f"Redemption Analysis (Generated at: {st.session_state['generated_redemptions']} JST)")
    redemption_metrics_df = redemption_metrics(redemption_df)
    st.dataframe(redemption_metrics_df, use_container_width=True)
    st.plotly_chart(daily_redemptions_value(redemption_df))
    st.plotly_chart(daily_redemptions_count(redemption_df))


    header_text = f"**Merchant-wise Total Redemption Analysis (Generated at: {st.session_state['generated_redemptions']} JST)**" if 'generated_redemptions' in st.session_state and st.session_state['generated_redemptions'] else "Merchant-wise Total Redemption"
    st.header(header_text)
    # st.header(f"Merchant-wise Total Redemption Analysis (Generated at: {st.session_state['generated_redemptions']})")
    merchant_redemptions_df = merchant_wise_redemption(redemption_df)
    st.dataframe(merchant_redemptions_df, use_container_width=True)
    
    # SPACING
    st.write("#")
    st.write("#")
    st.write("#")
    st.write("#")
    fig = px.bar(merchant_redemptions_df, x="Merchant Name", y="Sum of cashback", title="Total Redemption by Merchants")
    st.plotly_chart(fig)