import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def load_redemption_data(file):
    return pd.read_csv(file)

def redemption_metrics(df):
    metrics_data = {
        'Metrics': [
            'Total Redemption Count',
            'Total Cashback Given',
            'Average Cashback Given'
        ],
        'Value': [
            str(int(df['transaction_id'].nunique())),
            '¥' + str(int(df['cashback_amount'].sum())),
            '¥' + str(round(df['cashback_amount'].mean(), 2))
        ]
    }
    return pd.DataFrame(metrics_data)

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

def merchant_wise_redemption(df):
    new_df = df.groupby('name')['cashback_amount'].sum().reset_index()
    new_df.columns = ['Merchant Name', 'Sum of cashback']
    new_df = new_df.sort_values(by='Sum of cashback', ascending=False)
    return new_df
