# Script that reads data from a file
# Analyzes it, Generate a formatted pdf using FPDF or Reportlab


import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Function to analyze data and prepare PDF report
def generate_pdf_report(data_path, output_path):
    # Load the data
    try:
        data = pd.read_csv(data_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Perform analysis
    summary_stats = data.describe(include='all')
    missing_values = data.isnull().sum()
    total_rows = data.shape[0]
    total_columns = data.shape[1]

    # Create visualizations
    output_dir = "temp_plots"
    os.makedirs(output_dir, exist_ok=True)

    # Histogram for numerical features
    num_features = data.select_dtypes(include=['float64', 'int64']).columns
    for feature in num_features:
        plt.figure()
        data[feature].hist(bins=20, alpha=0.7)
        plt.title(f"Distribution of {feature}")
        plt.xlabel(feature)
        plt.ylabel("Frequency")
        plt.savefig(f"{output_dir}/{feature}_hist.png")
        plt.close()

    # Generate PDF report
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title Page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Data Analysis Report", ln=True, align='C')
    pdf.ln(10)

    # Dataset Overview
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Dataset Overview", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 6, txt=f"Dataset: {os.path.basename(data_path)}", ln=True)
    pdf.cell(200, 6, txt=f"Total Rows: {total_rows}", ln=True)
    pdf.cell(200, 6, txt=f"Total Columns: {total_columns}", ln=True)
    pdf.ln(10)

    # Summary Statistics Table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Summary Statistics", ln=True)
    pdf.set_font("Arial", size=8)
    pdf.ln(5)
    for col in summary_stats.columns:
        pdf.set_font("Arial", 'B', 8)
        pdf.cell(200, 5, txt=f"{col}", ln=True)
        pdf.set_font("Arial", size=8)
        stats = summary_stats[col].to_dict()
        for key, value in stats.items():
            pdf.cell(200, 5, txt=f"  {key}: {value}", ln=True)
        pdf.ln(3)
    pdf.ln(10)

    # Missing Values Table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Missing Values", ln=True)
    pdf.set_font("Arial", size=10)
    for col, missing in missing_values.items():
        pdf.cell(200, 6, txt=f"{col}: {missing}", ln=True)
    pdf.ln(10)

    # Visualizations
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Visualizations", ln=True)
    for feature in num_features:
        pdf.add_page()
        pdf.cell(200, 10, txt=f"Histogram: {feature}", ln=True)
        pdf.image(f"{output_dir}/{feature}_hist.png", x=10, y=30, w=180)

    # Save the PDF
    pdf.output(output_path)

    # Clean up temporary files
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    os.rmdir(output_dir)

    print(f"PDF report generated: {output_path}")


# Usage example
if __name__ == "__main__":
    data_path = 'data.csv'
    output_path = "report.pdf"
    generate_pdf_report(data_path, output_path)
