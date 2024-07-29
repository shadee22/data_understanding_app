import streamlit as st
import pandas as pd
from scipy.stats import skew
import time

def analyze_csv(file):
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Get the first few rows (head)
    head = df.head()
    
    # Data format of every column
    data_format = pd.DataFrame(df.dtypes, columns=['Data Type'])
    
    # Calculate missing values
    missing_values = df.isnull().sum().to_frame('Missing Values')
    missing_percentage = (df.isnull().sum() / len(df) * 100).to_frame('Percentage Missing')
    missing_info = pd.concat([missing_values, missing_percentage], axis=1)
    
    # Duplicate understanding
    duplicate_count = df.duplicated().sum()
    duplicate_columns = df.apply(lambda x: x.duplicated().sum()).to_frame('Duplicate Count')
    
    # Compute basic statistics
    basic_stats = df.describe()
    
    # Row count
    row_count = len(df)
    
    # Identification of qualitative and quantitative attributes
    qualitative_attributes = df.select_dtypes(include=['object', 'category']).columns.tolist()
    quantitative_attributes = df.select_dtypes(include=['number']).columns.tolist()
    
    # Summary reports for qualitative attributes
    summary_reports_qual = {}
    for col in qualitative_attributes:
        frequencies = df[col].value_counts().to_frame('Frequency')
        percentages = (df[col].value_counts(normalize=True) * 100).to_frame('Percentage')
        summary_report = pd.concat([frequencies, percentages], axis=1)
        summary_reports_qual[col] = summary_report
    
    # Summary reports for quantitative attributes
    summary_reports_quant = {}
    for col in quantitative_attributes:
        descriptive_stats = df[col].describe().to_frame().T
        variance = df[col].var()
        std_dev = df[col].std()
        skewness = skew(df[col].dropna())
        
        summary_report = descriptive_stats.copy()
        summary_report['Variance'] = variance
        summary_report['Standard Deviation'] = std_dev
        summary_report['Skewness'] = skewness
        
        summary_reports_quant[col] = summary_report
    
    # Analysis against qualitative and quantitative attributes
    analysis_results = {}
    for qual_col in qualitative_attributes:
        for quant_col in quantitative_attributes:
            group_stats = df.groupby(qual_col)[quant_col].agg([
                'count',
                'mean',
                'std',
                'min',
                lambda x: x.quantile(0.25),
                'median',
                lambda x: x.quantile(0.75),
                'max'
            ]).reset_index()
            group_stats.columns = [qual_col, 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
            analysis_results[f"{quant_col} by {qual_col}"] = group_stats
    
    return (head, data_format, missing_info, duplicate_count, duplicate_columns, basic_stats, 
            row_count, qualitative_attributes, quantitative_attributes, summary_reports_qual, 
            summary_reports_quant, analysis_results)

# Streamlit app
st.title("Data Analysis with CSV")
st.write("🦸‍♂️🛠️ Visa data superhero tool engineered by Pulse AI 🛠️🦸‍♂️")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    progress_bar.progress(10)
    status_text.text("Reading CSV file...")
    
    results = analyze_csv(uploaded_file)
    progress_bar.progress(30)
    status_text.text("Analyzing data format...")
    
    (head, data_format, missing_info, duplicate_count, duplicate_columns, basic_stats, 
     row_count, qualitative_attributes, quantitative_attributes, summary_reports_qual, 
     summary_reports_quant, analysis_results) = results
    
    progress_bar.progress(50)
    status_text.text("Generating summaries and statistics...")
    
    st.subheader("First Few Rows")
    st.dataframe(head)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Format of Each Column")
        st.dataframe(data_format)
        
        st.subheader("Missing Values")
        st.dataframe(missing_info)
    
    with col2:
        st.subheader("Duplicates")
        st.write(f"Total duplicate rows: {duplicate_count}")
        st.dataframe(duplicate_columns)
        
        st.subheader("Basic Statistics")
        st.dataframe(basic_stats)

    progress_bar.progress(70)
    status_text.text("Summarizing qualitative attributes...")
    
    # Additional Information
    st.subheader("Additional Information")
    
    st.write(f"**Row Count:** {row_count}")
    
    st.subheader("Qualitative Attributes")
    st.write(", ".join(qualitative_attributes))
    
    st.subheader("Quantitative Attributes")
    st.write(", ".join(quantitative_attributes))

    progress_bar.progress(90)
    status_text.text("Summarizing quantitative attributes...")
    
    # Summary reports for qualitative attributes
    st.subheader("Summary Reports for Qualitative Attributes")
    for col, report in summary_reports_qual.items():
        st.markdown(f"**{col}**")
        st.dataframe(report)
    
    # Summary reports for quantitative attributes
    st.subheader("Summary Reports for Quantitative Attributes")
    for col, report in summary_reports_quant.items():
        st.markdown(f"**{col}**")
        st.dataframe(report)
    
    st.divider()
    
    # Analysis against qualitative and quantitative attributes
    st.subheader("Analysis of Qualitative vs Quantitative Attributes")
    for analysis, result in analysis_results.items():
        st.markdown(f"**{analysis}**")
        st.dataframe(result)
    
    progress_bar.progress(100)
    status_text.text("Analysis complete!")
    progress_bar.empty()