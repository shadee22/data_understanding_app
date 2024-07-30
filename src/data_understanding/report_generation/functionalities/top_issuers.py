# Code for Top Issuer Analysis

# Import necessary libraries
import pandas as pd

# Define the bank mapping
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

# Function to perform Top Issuer Analysis
def top_issuer_analysis(card_df):
    new_df = card_df.groupby('issuer_bin')['card_id'].nunique().reset_index(name='card_id_count')
    new_df = new_df.sort_values(by='card_id_count', ascending=False)
    new_df["issuer_bin"] = new_df["issuer_bin"].astype(str)
    new_df["first_4_digits"] = new_df["issuer_bin"].str[:4]
    grouped_df = new_df.groupby("first_4_digits")["card_id_count"].sum().reset_index()
    grouped_df = grouped_df.sort_values(by="card_id_count", ascending=False).reset_index(drop=True)
    grouped_df['Bank Name'] = grouped_df['first_4_digits'].map(bank_mapping)
    grouped_df = grouped_df[['Bank Name', 'card_id_count']][:20]
    return  grouped_df