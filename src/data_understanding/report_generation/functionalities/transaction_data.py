import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def load_transaction_data(file):
    return pd.read_csv(file)

def transaction_metrics(df):
    metrics_data = {
        'Metrics': [
            'Authorized & Eligible Total Transaction Count',
            'Authorized & Eligible Total Transaction Value',
            'Authorized & Eligible Average Transaction Value',
            'Authorized & Eligible Total Cashback',
            'Authorized & Eligible Average Cashback'
        ],
        'Value': [
            f"{df['transaction_id'].nunique():,}",
            '¥' + f"{df['transaction_amount'].sum():,}",
            '¥' + f"{round(df['transaction_amount'].mean(), 2):,}",
            '¥' + f"{df['cashback_amount'].sum():,}",
            '¥' + f"{round(df['cashback_amount'].mean(), 2):,}"
        ]
    }
    return pd.DataFrame(metrics_data)
