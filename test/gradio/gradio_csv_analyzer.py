import gradio as gr
import pandas as pd
from scipy.stats import skew

def analyze_csv(file):
    # Read the CSV file
    df = pd.read_csv(file.name)
    
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
    summary_reports_qual = []
    for col in qualitative_attributes:
        frequencies = df[col].value_counts().to_frame('Frequency')
        percentages = (df[col].value_counts(normalize=True) * 100).to_frame('Percentage')
        summary_report = pd.concat([frequencies, percentages], axis=1)
        summary_reports_qual.append((col, summary_report))
    
    # Summary reports for quantitative attributes
    summary_reports_quant = []
    for col in quantitative_attributes:
        descriptive_stats = df[col].describe().to_frame().T
        variance = df[col].var()
        std_dev = df[col].std()
        skewness = skew(df[col].dropna())
        
        summary_report = descriptive_stats.copy()
        summary_report['Variance'] = variance
        summary_report['Standard Deviation'] = std_dev
        summary_report['Skewness'] = skewness
        
        summary_reports_quant.append((col, summary_report))
    
    # Analysis against qualitative and quantitative attributes
    analysis_results = []
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
            analysis_results.append((f"{quant_col} by {qual_col}", group_stats))
    
    return (head, data_format, missing_info, duplicate_count, duplicate_columns, basic_stats, 
            row_count, qualitative_attributes, quantitative_attributes, summary_reports_qual, 
            summary_reports_quant, analysis_results)

def display_results(file):
    results = analyze_csv(file)
    (head, data_format, missing_info, duplicate_count, duplicate_columns, basic_stats, 
     row_count, qualitative_attributes, quantitative_attributes, summary_reports_qual, 
     summary_reports_quant, analysis_results) = results
    
    summary_tables_qual = create_summary_tables(summary_reports_qual)
    summary_tables_quant = create_summary_tables(summary_reports_quant)
    
    return head, data_format, missing_info, str(duplicate_count), duplicate_columns, basic_stats, \
           str(row_count), ", ".join(qualitative_attributes), ", ".join(quantitative_attributes), summary_tables_qual, \
           summary_tables_quant, analysis_results

def create_summary_tables(summary_reports):
    summary_tables = {}
    for col, summary_report in summary_reports:
        summary_tables[col] = summary_report
    return summary_tables

iface = gr.Interface(
    fn=display_results, 
    inputs=gr.File(label="Upload CSV file"), 
    outputs=[
        gr.Dataframe(label="First Few Rows"),
        gr.Dataframe(label="Data Format of Each Column"),
        gr.Dataframe(label="Missing Values"),
        gr.Textbox(label="Total Duplicate Rows"),
        gr.Dataframe(label="Duplicate Columns"),
        gr.Dataframe(label="Basic Statistics"),
        gr.Textbox(label="Row Count"),
        gr.Textbox(label="Qualitative Attributes"),
        gr.Textbox(label="Quantitative Attributes"),
        gr.Dataframe(label="Summary Reports for Qualitative Attributes"),
        gr.Dataframe(label="Summary Reports for Quantitative Attributes"),
        gr.Dataframe(label="Analysis of Qualitative vs Quantitative Attributes")
    ],
    title="Data Analysis with CSV",
    description="🦸‍♂️🛠️ Visa data superhero tool engineered by Pulse AI 🛠️🦸‍♂️"
)

iface.launch(debug=True)