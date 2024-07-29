import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pytz
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
import matplotlib.ticker as ticker

# Define the PDFGenerator class here
class PDFGenerator:
    def __init__(self):
        self.p_width, self.p_height = letter

    def text(self, obj, x, y, txt, f_size=12, angle=0, color=(0, 0, 0), fontfamily='Helvetica'):
        r, g, b = color
        obj.setFillColorRGB(r, g, b)
        obj.setFont(fontfamily, f_size)
        obj.drawString(x, y, txt)

    def add_borders_and_page_number(self, c, page_num):
        c.setLineWidth(1)
        c.rect(30, 30, self.p_width - 60, self.p_height - 60)  # Draw border
        c.setFont("Helvetica", 10)
        c.drawString(self.p_width - 100, 20, f"Page {page_num} @Pulse iD AI")  # Add page number

    def get_file_created_time(self, csv_file_path):
        created_time = os.path.getctime(csv_file_path)
        created_time_dt = datetime.utcfromtimestamp(created_time)
        sri_lanka_tz = pytz.timezone('Asia/Colombo')
        japan_tz = pytz.timezone('Asia/Tokyo')
        created_time_utc = pytz.utc.localize(created_time_dt)
        created_time_sl = created_time_utc.astimezone(sri_lanka_tz)
        created_time_jp = created_time_sl.astimezone(japan_tz)
        return created_time_jp

    def daily_cardholder_enrollment(self, df, filename='daily_enrollment_plot.png'):
        df['created_at'] = pd.to_datetime(df['created_at'])
        last_7_days = datetime.now() - timedelta(days=7)
        df_last_7_days = df[df['created_at'] >= last_7_days]
        daily_enrollment = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date).size()
        plt.figure(figsize=(10, 6))
        ax = daily_enrollment.plot(kind='bar', color='skyblue')
        plt.xlabel('Date')
        plt.ylabel('Number of Enrollments')
        plt.title('Daily Cardholder Enrollment for the Last 7 Days')
        plt.xticks(rotation=45)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        plt.tight_layout()
        plt.savefig(filename)

    def daily_redemptions_value(self, df, filename='daily_redemptions_value_plot.png'):
        df['created_at'] = pd.to_datetime(df['created_at'])
        last_7_days = datetime.now() - timedelta(days=7)
        df_last_7_days = df[df['created_at'] >= last_7_days]
        daily_redemptions = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date)['cashback_amount'].sum()
        plt.figure(figsize=(10, 6))
        ax = daily_redemptions.plot(kind='bar', color='skyblue')
        plt.xlabel('Date')
        plt.ylabel('Total Redemption Value')
        plt.title('Daily Redemptions Value for the Last 7 Days')
        plt.xticks(rotation=45)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        plt.tight_layout()
        plt.savefig(filename)

    def daily_redemptions_count(self, df, filename='daily_redemptions_count_plot.png'):
        df['created_at'] = pd.to_datetime(df['created_at'])
        last_7_days = datetime.now() - timedelta(days=7)
        df_last_7_days = df[df['created_at'] >= last_7_days]
        daily_redemptions = df_last_7_days.groupby(df_last_7_days['created_at'].dt.date).size()
        plt.figure(figsize=(10, 6))
        ax = daily_redemptions.plot(kind='bar', color='skyblue')
        plt.xlabel('Date')
        plt.ylabel('Number of Redemptions')
        plt.title('Daily Redemptions Count for the Last 7 Days')
        plt.xticks(rotation=45)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        plt.tight_layout()
        plt.savefig(filename)

    def create_pdf(self, filename, header, stats, table_data, image_path=None, third_page_table=None, bar_plot_path=None, fifth_page_table=None, fifth_page_table2=None, fifth_page_table3=None, bar_plot_path2=None):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        page_num = 1

        if image_path:
            self.add_image(c, image_path)

        # Add header
        self.text(c, 150, self.p_height - 300, header, f_size=16)

        # Add statistics
        y_pos = self.p_height - 350
        for stat in stats:
            self.text(c, 50, y_pos, stat, f_size=12)
            y_pos -= 20

        csv_file_path = 'Visa Japan Cards.csv'  # Replace with your CSV file path
        created_time_jp_for_Latitude_Cards = self.get_file_created_time(csv_file_path)
        created_time_jp_for_Latitude_Cards = created_time_jp_for_Latitude_Cards.strftime('%H:%M:%S')
        # Add table description
        y_pos -= 40  # Adjust y position to ensure space between text and table
        self.text(c, 50, y_pos, f'Card Count Analysis (Cards per Cardholder)... (Generated @ {created_time_jp_for_Latitude_Cards} JST)', f_size=14)

        # Convert table data to reportlab Table format
        table_data.insert(0, ['Card Count', 'Unique Cardholder Count'])
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Draw the table
        table.wrapOn(c, self.p_width - 100, self.p_height - 100)
        table.drawOn(c, 150, y_pos - 250)  # Adjust table position

        # Add borders and page number to the first page
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        self.daily_cardholder_enrollment(pd.read_csv('Visa Japan Cards.csv'), 'daily_cardholder_enrollment_plot.png')
        self.add_bar_plot(c, page_num, "Daily Cardholder Enrollment Plot", 'daily_cardholder_enrollment_plot.png')
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        # Generate and add donut chart to the next page
        self.add_donut_chart(c, page_num, "Cardholder Distribution by Card Count", "Req-2-cardholder_distribution_pie.png")
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        # Add third page with the new table
        self.add_third_page_table(c, page_num, third_page_table)
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        # Add fourth page with the bar plot
        self.add_bar_plot(c, page_num, "Top Issuers Analysis", bar_plot_path)
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        # Add fifth page with the new table
        self.add_fifth_page_table(c, page_num, fifth_page_table)
        self.add_borders_and_page_number(c, page_num)

        self.add_fifth_page_table2(c, page_num, fifth_page_table2)
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        self.daily_redemptions_value(pd.read_csv('Visa Japan Redemptions.csv'), 'daily_redemptions_for_past_7_days.png')


        self.add_bar_plot(c, page_num, "Daily Redemptions Value Plot", 'daily_redemptions_for_past_7_days.png')
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        self.daily_redemptions_count(pd.read_csv('Visa Japan Redemptions.csv'), 'daily_redemptions_count_for_past_7_days.png')
        self.add_bar_plot(c, page_num, "Daily Redemptions Count Plot", 'daily_redemptions_count_for_past_7_days.png')
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        self.add_fifth_page_table3(c, page_num, fifth_page_table3)
        self.add_borders_and_page_number(c, page_num)
        c.showPage()
        page_num += 1

        # Add last page with the bar plot
        self.add_bar_plot(c, page_num, "Total Redemptions Value By Merchants", bar_plot_path2)
        self.add_borders_and_page_number(c, page_num)

        c.showPage()
        page_num += 1

        c.save()

        with open(filename, 'wb') as f:
            f.write(buffer.getvalue())

        print(f"PDF file '{filename}' created successfully with data table, description, borders, and page numbers.")

    def add_image(self, c, image_path):
        img = ImageReader(image_path)
        img_width, img_height = img.getSize()
        x = (self.p_width - img_width) / 2
        y = self.p_height - img_height - 50  # Adjust vertical position
        if y < 30:
            y = 30  # Minimum margin from top
        c.drawImage(image_path, x, y, width=img_width, height=img_height)

    def add_donut_chart(self, c, page_num, title, image_path):
        img = ImageReader(image_path)
        img_width, img_height = img.getSize()
        max_width = self.p_width - 60  # Leave margin on each side
        max_height = self.p_height - 180  # Leave margin on top and bottom
        if img_width > max_width or img_height > max_height:
            scale = min(max_width / img_width, max_height / img_height)
            img_width *= scale
            img_height *= scale
        x = (self.p_width - img_width) / 2
        y = (self.p_height - img_height) / 2  # Center vertically
        c.drawImage(image_path, x, y, width=img_width, height=img_height)
        self.text(c, 150, self.p_height - 100, title, f_size=16, color=(0, 0, 0))

    def add_third_page_table(self, c, page_num, table_data):
        csv_file_path = 'Visa Japan Cards.csv'  # Replace with your CSV file path
        created_time_jp_for_Latitude_Cards = self.get_file_created_time(csv_file_path)
        created_time_jp_for_Latitude_Cards = created_time_jp_for_Latitude_Cards.strftime('%H:%M:%S')
        y_pos = self.p_height - 350
        self.text(c, 50, self.p_height - 100, f'Top Issuers Analysis... (Generated @ {created_time_jp_for_Latitude_Cards} JST)', f_size=14)
        table_data.insert(0, ['Bank Name', 'Card ID Count'])
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table.wrapOn(c, self.p_width - 100, self.p_height - 100)
        table.drawOn(c, 120, y_pos - 250)  # Adjust table position

    def add_bar_plot(self, c, page_num, title, image_path):
        img = ImageReader(image_path)
        img_width, img_height = img.getSize()
        max_width = self.p_width - 60  # Leave margin on each side
        max_height = self.p_height - 180  # Leave margin on top and bottom
        if img_width > max_width or img_height > max_height:
            scale = min(max_width / img_width, max_height / img_height)
            img_width *= scale
            img_height *= scale
        x = (self.p_width - img_width) / 2
        y = (self.p_height - img_height) / 2  # Center vertically
        c.drawImage(image_path, x, y, width=img_width, height=img_height)
        self.text(c, 150, self.p_height - 100, title, f_size=16, color=(0, 0, 0))

    def add_fifth_page_table(self, c, page_num, table_data):
        csv_file_path = 'Visa Japan Eligible Transactions.csv'  # Replace with your CSV file path
        created_time_jp_for_Latitude_Cards = self.get_file_created_time(csv_file_path)
        created_time_jp_for_Latitude_Cards = created_time_jp_for_Latitude_Cards.strftime('%H:%M:%S')
        y_pos = self.p_height - 270
        self.text(c, 50, self.p_height - 100, f'Authorized & Eligible Transactions Analysis (Generated @ {created_time_jp_for_Latitude_Cards} JST)', f_size=14)
        table_data.insert(0, ['Metrics', 'Value'])
        table = Table(table_data)
        col_widths = [220, 200]
        row_heights = [30] * len(table_data)
        table = Table(table_data, colWidths=col_widths, rowHeights=row_heights)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table.wrapOn(c, self.p_width - 100, self.p_height - 100)
        table.drawOn(c, 120, y_pos - 40)

    def add_fifth_page_table2(self, c, page_num, table_data):
        csv_file_path = 'Visa Japan Redemptions.csv'  # Replace with your CSV file path
        created_time_jp_for_Latitude_Cards = self.get_file_created_time(csv_file_path)
        created_time_jp_for_Latitude_Cards = created_time_jp_for_Latitude_Cards.strftime('%H:%M:%S')
        y_pos = self.p_height - 500
        self.text(c, 50, self.p_height - 400, f'Redemption Analysis (Generated @ {created_time_jp_for_Latitude_Cards})', f_size=14)
        table_data.insert(0, ['Metrics', 'Value'])
        table = Table(table_data)
        col_widths = [200, 200]
        row_heights = [30] * len(table_data)
        table = Table(table_data, colWidths=col_widths, rowHeights=row_heights)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table.wrapOn(c, self.p_width - 100, self.p_height - 100)
        table.drawOn(c, 120, y_pos - 60)

    def add_fifth_page_table3(self, c, page_num, table_data):
        csv_file_path = 'Visa Japan Redemptions.csv'  # Replace with your CSV file path
        created_time_jp_for_Latitude_Cards = self.get_file_created_time(csv_file_path)
        created_time_jp_for_Latitude_Cards = created_time_jp_for_Latitude_Cards.strftime('%H:%M:%S')
        y_pos = self.p_height - 270
        self.text(c, 50, self.p_height - 100, f'Merchant-wise Total Redemption Analysis (Generated @ {created_time_jp_for_Latitude_Cards})', f_size=14)
        table_data.insert(0, ['Metrics', 'Value'])
        table = Table(table_data)
        col_widths = [200, 200]
        row_heights = [30] * len(table_data)
        table = Table(table_data, colWidths=col_widths, rowHeights=row_heights)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table.wrapOn(c, self.p_width - 50, self.p_height - 50)
        table.drawOn(c, 120, y_pos - 120)

# Add file input for card data
st.sidebar.header('Upload Data Files')
card_data = st.sidebar.file_uploader("Upload Card Data", type=['csv'])
# Add file input for transaction data
transaction_data = st.sidebar.file_uploader("Upload Transaction Data", type=['csv'])
# Add file input for redemption data
redemption_data = st.sidebar.file_uploader("Upload Redemption Data", type=['csv'])

if card_data and transaction_data and redemption_data:
    card_df = pd.read_csv(card_data)
    transaction_df = pd.read_csv(transaction_data)
    redemption_df = pd.read_csv(redemption_data)

    pdf_generator = PDFGenerator()

    # Use the class methods to generate the required plots
    pdf_generator.daily_cardholder_enrollment(card_df)
    pdf_generator.daily_redemptions_value(redemption_df)
    pdf_generator.daily_redemptions_count(redemption_df)

    # Process and display the data
    num_unique_cardholders = card_df['cardholder_id'].nunique()
    num_unique_cards = card_df['card_id'].nunique()
    new_df = card_df.groupby('cardholder_id')['card_id'].count().reset_index(name='card_id_count')
    value_counts = new_df['card_id_count'].value_counts().reset_index()
    value_counts.columns = ['card_count', 'unique_cardholder_count']

    st.title("VISA Japan Campaign Analysis July 25 2024")
    st.markdown("**Report generated Date: 2024 July 25**")
    st.markdown("**Card and Cardholder Information Analysis (Generated at: 12:13 pm JST)**")
    st.write(f"Number of unique Cardholders: **{num_unique_cardholders}**")
    st.write(f"Number of unique Cards: **{num_unique_cards}**")

    # Card Count Analysis
    st.header("Card Count Analysis (Cards per Cardholder)")
    st.table(value_counts)

    # Cardholder Distribution by Card Count Pie Chart
    fig = px.pie(value_counts, values="unique_cardholder_count", names="card_count", title="Cardholder Distribution by Card Count")
    st.plotly_chart(fig)

    # Top Issuer Analysis
    st.header("Top Issuer Analysis (Generated at: 12:13 pm JST)")
    new_df = card_df.groupby('issuer_bin')['card_id'].nunique().reset_index(name='card_id_count')
    new_df = new_df.sort_values(by='card_id_count', ascending=False)
    new_df["issuer_bin"] = new_df["issuer_bin"].astype(str)
    new_df["first_4_digits"] = new_df["issuer_bin"].str[:4]
    grouped_df = new_df.groupby("first_4_digits")["card_id_count"].sum().reset_index()
    grouped_df = grouped_df.sort_values(by="card_id_count", ascending=False).reset_index(drop=True)
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
    grouped_df['Bank Name'] = grouped_df['first_4_digits'].map(bank_mapping)
    grouped_df = grouped_df[['Bank Name', 'card_id_count']][:10]
    st.table(grouped_df)

    fig = px.bar(grouped_df, x="card_id_count", y="Bank Name", orientation='h', title="Card ID Counts by Top Issuers")
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)

    # Transaction Analysis
    st.header("Transaction Analysis (Generated at: 12:13 pm JST)")
    metrics_data = {
        'Metrics': [
            'Authorized & Eligible Total Transaction Count',
            'Authorized & Eligible Total Transaction Value',
            'Authorized & Eligible Average Transaction Value',
            'Authorized & Eligible Total Cashback',
            'Authorized & Eligible Average Cashback'
        ],
        'Value': [
            str(int(transaction_df['transaction_id'].nunique())),
            '¥' + str(int(transaction_df['transaction_amount'].sum())),
            '¥' + str(round(transaction_df['transaction_amount'].mean(), 2)),
            '¥' + str(int(transaction_df['cashback_amount'].sum())),
            '¥' + str(round(transaction_df['cashback_amount'].mean(), 2))
        ]
    }
    transaction_metrics_df = pd.DataFrame(metrics_data)
    st.table(transaction_metrics_df)

    # Redemption Analysis
    st.header("Redemption Analysis (Generated at: 12:13 pm JST)")
    redemption_metrics_data = {
        'Metrics': [
            'Total Redemption Count',
            'Total Cashback Given',
            'Average Cashback Given'
        ],
        'Value': [
            str(int(redemption_df['transaction_id'].nunique())),
            '¥' + str(int(redemption_df['cashback_amount'].sum())),
            '¥' + str(round(redemption_df['cashback_amount'].mean(), 2))
        ]
    }
    redemption_metrics_df = pd.DataFrame(redemption_metrics_data)
    st.table(redemption_metrics_df)

    # Daily Redemptions for last 7 days
    st.header("Daily Redemptions for last 7 days")
    pdf_generator.daily_redemptions_value(redemption_df)
    daily_redemptions_value_plot = "daily_redemptions_value_plot.png"
    if os.path.exists(daily_redemptions_value_plot):
        st.image(daily_redemptions_value_plot)

    st.header("Daily Redemption Count for last 7 days")
    pdf_generator.daily_redemptions_count(redemption_df)
    daily_redemptions_count_plot = "daily_redemptions_count_plot.png"
    if os.path.exists(daily_redemptions_count_plot):
        st.image(daily_redemptions_count_plot)

    # Merchant-wise Total Redemption Analysis
    st.header("Merchant-wise Total Redemption Analysis (Generated at: 12:14 pm JST)")
    new_df = redemption_df.groupby('name')['cashback_amount'].sum().reset_index()
    new_df.columns = ['Merchant Name', 'Sum of cashback']
    new_df = new_df.sort_values(by='Sum of cashback', ascending=False)
    st.table(new_df)
    fig = px.bar(new_df, x="Merchant Name", y="Sum of cashback", title="Total Redemption by Merchants")
    st.plotly_chart(fig)


