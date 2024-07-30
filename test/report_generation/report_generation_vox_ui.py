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

# st.sidebar.header('Upload Data Files')
# card_data = st.sidebar.file_uploader("Upload Card Data", type=['csv'])
# transaction_data = st.sidebar.file_uploader("Upload Transaction Data", type=['csv'])
# redemption_data = st.sidebar.file_uploader("Upload Redemption Data", type=['csv'])

tab1, tab2 = st.sidebar.tabs(["Upload Data Files", "Add Dummy Inputs"])

# First tab for uploading data files
with tab1:
    st.header('Upload Data Files')
    card_data = st.file_uploader("Upload Card Data", type=['csv'])
    transaction_data = st.file_uploader("Upload Transaction Data", type=['csv'])
    redemption_data = st.file_uploader("Upload Redemption Data", type=['csv'])

# Second tab for adding dummy inputs
with tab2:
    st.header('Add Dummy Inputs')
    generated_cardholder= st.text_input("generated_cardholder")
    generated_transactions = st.text_input("generated_transactions ")
    generated_redemptions = st.text_input("generated_redemptions ")


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

    st.image('./other/assets/banner+pulse+id.png')  # Replace 'path_to_your_image.jpg' with the actual path to your image

    # Display the title with the current date
    st.title(f"VISA Japan Campaign Analysis {current_date}")
    # st.subheader("**Report generated Date: 2024 July 25**") 
    
    # st.header(f"**Card and Cardholder Information Analysis (Generated at: {formatted_time})**")
    st.header(f"**Card and Cardholder Information Analysis (Generated at: {generated_cardholder })**")

    st.write(f"Number of unique Cardholders: **{num_unique_cardholders}**")
    st.write(f"Number of unique Cards: **{num_unique_cards}**")

    st.header("Card Count Analysis (Cards per Cardholder)")
    st.table(value_counts)
    
    # SPACING
    st.write("#")
    st.write("#")
    
    fig2 = px.pie(value_counts, values="unique_cardholder_count", names="card_count", title="Cardholder Distribution by Card Count", hole=0.5)
    st.plotly_chart(fig2)
    st.plotly_chart(daily_cardholder_enrollment(card_df))

    # SPACING
    st.write("#")

    st.header(f"Top Issuer Analysis")
    #  (Generated at: {formatted_time}) Removed this becuase same time as cardholders
    grouped_df = top_issuers.top_issuer_analysis(card_df=card_df)
    st.dataframe(grouped_df)
    fig3 = px.bar(grouped_df, x="card_id_count", y="Bank Name", orientation='h', title="Card ID Counts by Top Issuers")
    st.plotly_chart(fig3, use_container_width=True)

    # SPACING
    st.write("#")

    st.header(f"Transaction Analysis (Generated at: {generated_transactions})")
    transaction_metrics_df = transaction_metrics(transaction_df)
    st.dataframe(transaction_metrics_df)

    # SPACING
    st.write("#")

    st.header(f"Redemption Analysis (Generated at: {generated_redemptions})")
    redemption_metrics_df = redemption_metrics(redemption_df)
    st.dataframe(redemption_metrics_df)
    st.plotly_chart(daily_redemptions_value(redemption_df))
    st.plotly_chart(daily_redemptions_count(redemption_df))

    st.header(f"Merchant-wise Total Redemption Analysis (Generated at: {generated_redemptions})")
    merchant_redemptions_df = merchant_wise_redemption(redemption_df)
    st.table(merchant_redemptions_df)
    # SPACING
    st.write("#")
    st.write("#")
    st.write("#")
    st.write("#")
    fig = px.bar(merchant_redemptions_df, x="Merchant Name", y="Sum of cashback", title="Total Redemption by Merchants")
    st.plotly_chart(fig)
