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
            str(int(df['transaction_id'].nunique())),
            '¥' + str(int(df['transaction_amount'].sum())),
            '¥' + str(round(df['transaction_amount'].mean(), 2)),
            '¥' + str(int(df['cashback_amount'].sum())),
            '¥' + str(round(df['cashback_amount'].mean(), 2))
        ]
    }
    return pd.DataFrame(metrics_data)
