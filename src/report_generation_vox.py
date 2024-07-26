import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Dummy data
cardholder_data = {
    "Card count": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    "Cardholder count": [37519, 8489, 2819, 1184, 1004, 64, 17, 7, 2, 1, 2],
    "Percentage": [73.41, 16.61, 5.52, 2.32, 1.96, 0.13, 0.03, 0.01, 0.00, 0.00, 0.00]
}

issuer_data = {
    "Issuer Bank": [
        "Sumitomo Mitsui Card Company Limited", "YES BANK, LTD.", "RAKUTEN KC CO., LTD.",
        "AEON CREDIT SERVICE CO., LTD.", "WELLS FARGO BANK, N.A.", "DC CARD CO., LTD.",
        "REDIT SAISON CO., LTD.", "UNITED COMMERCIAL BANK", "U.S. BANK N.A. ND",
        "YAMAGIN CREDIT CO., LTD.", "MITSUBISHI UFJ FINANCIAL GROUP, INC.", "CAJA AHORROS GERONA",
        "WELLS FARGO BANK IOWA, N.A.", "OSTGIROT BANK AB", "YAMAGIN CREDIT CO., LTD.",
        "YAMAGIN CREDIT CO., LTD.", "MITSUBISHI UFJ FINANCIAL GROUP, INC.", "UNKNOWN",
        "BANCO DO BRASIL, S.A.", "BANK OF AMERICA, N.A."
    ],
    "Count": [
        29454, 11982, 8949, 2416, 2123, 1699, 1516, 1481, 1478, 1330, 1115, 630,
        623, 565, 560, 540, 537, 488, 479, 469
    ]
}

transaction_data = {
    "Metrics": [
        "Authorized & Eligible Total Transaction Count", "Authorized & Eligible Total Transaction Value",
        "Authorized & Eligible Average Transaction Value", "Authorized & Eligible Total Cashback",
        "Authorized & Eligible Average Cashback"
    ],
    "Value": [
        57111, "¥56229180", "¥984.56", "¥8394187", "¥146.98"
    ]
}

redemption_data = {
    "Metrics": ["Total Redemptions count", "Total Cashback (given)", "Average Cashback (given)"],
    "Value": [41028, "¥6181732", "¥150.67"]
}

merchant_redemption_data = {
    "Merchant Name": ["Mcdonalds", "Katsuya", "Sukiya", "Mosburger", "Nakau", "Karayama"],
    "Sum of cashback": [2346745, 1006179, 994933, 724649, 607421, 501805]
}

# Inject custom CSS to handle page breaks
custom_css = """
<style>
@media print {
    .no-page-break {
        page-break-inside: avoid;
    }
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# App layout
st.title("VISA Japan Campaign Analysis July 25 2024")
st.markdown("**Report generated Date: 2024 July 25**")
st.markdown("**Card and Cardholder Information Analysis (Generated at: 12:13 pm JST)**")
st.write(f"Number of unique Cardholders: **51108**")
st.write(f"Number of unique Cards: **72614**")

# Card Count Analysis
st.header("Card Count Analysis (Cards per Cardholder)")
card_count_df = pd.DataFrame(cardholder_data)
st.markdown('<div class="no-page-break">', unsafe_allow_html=True)
st.table(card_count_df)
st.markdown('</div>', unsafe_allow_html=True)

# Cardholder Distribution by Card Count Pie Chart
fig = px.pie(card_count_df, values="Percentage", names="Card count", title="Cardholder Distribution by Card Count")
st.plotly_chart(fig)

# Top Issuer Analysis
st.header("Top Issuer Analysis (Generated at: 12:13 pm JST)")
issuer_df = pd.DataFrame(issuer_data)
st.markdown('<div class="no-page-break">', unsafe_allow_html=True)
st.table(issuer_df)
st.markdown('</div>', unsafe_allow_html=True)

# Issuer Bar Chart
fig = px.bar(issuer_df, x="Count", y="Issuer Bank", orientation='h', title="Card ID Counts by Top Issuers")
fig.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig)

# Transaction Analysis
st.header("Transaction Analysis (Generated at: 12:13 pm JST)")
transaction_df = pd.DataFrame(transaction_data)
st.markdown('<div class="no-page-break">', unsafe_allow_html=True)
st.table(transaction_df)
st.markdown('</div>', unsafe_allow_html=True)

# Redemption Analysis
st.header("Redemption Analysis (Generated at: 12:13 pm JST)")
redemption_df = pd.DataFrame(redemption_data)
st.markdown('<div class="no-page-break">', unsafe_allow_html=True)
st.table(redemption_df)
st.markdown('</div>', unsafe_allow_html=True)

# Daily Redemptions for last 7 days (Dummy Data)
st.header("Daily Redemptions for last 7 days")
daily_redemptions = {
    "Date": ["2024-07-18", "2024-07-19", "2024-07-20", "2024-07-21", "2024-07-22", "2024-07-23", "2024-07-24"],
    "Value": [315058.0, 254270.0, 162553.0, 181372.0, 18406.0, 518536.0, 300000.0]
}
daily_redemptions_df = pd.DataFrame(daily_redemptions)
fig = px.bar(daily_redemptions_df, x="Date", y="Value", title="Daily Redemptions Value for the Last 7 Days")
st.plotly_chart(fig)

# Daily Redemption Count for last 7 days (Dummy Data)
st.header("Daily Redemption Count for last 7 days")
daily_redemption_count = {
    "Date": ["2024-07-18", "2024-07-19", "2024-07-20", "2024-07-21", "2024-07-22", "2024-07-23", "2024-07-24"],
    "Count": [1772, 1591, 1323, 1447, 114, 5189, 4000]
}
daily_redemption_count_df = pd.DataFrame(daily_redemption_count)
fig = px.bar(daily_redemption_count_df, x="Date", y="Count", title="Daily Redemptions Count for the Last 7 Days")
st.plotly_chart(fig)

# Merchant-wise Total Redemption Analysis
st.header("Merchant-wise Total Redemption Analysis (Generated at: 12:14 pm JST)")
merchant_redemption_df = pd.DataFrame(merchant_redemption_data)
st.markdown('<div class="no-page-break">', unsafe_allow_html=True)
st.table(merchant_redemption_df)
st.markdown('</div>', unsafe_allow_html=True)

# Merchant-wise Redemption Bar Chart
fig = px.bar(merchant_redemption_df, x="Merchant Name", y="Sum of cashback", title="Total Redemption by Merchants")
st.plotly_chart(fig)