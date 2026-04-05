from datetime import datetime, timedelta
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def process_data(data):

    investment_date = datetime.strptime(data["INVESTMENT_DATE"], "%d/%m/%Y")

    start_date = investment_date + timedelta(days=30)

    try:
        end_date = start_date.replace(year=start_date.year + 1) - timedelta(days=1)
    except:
        end_date = start_date + timedelta(days=365) - timedelta(days=1)

    total_days = (end_date - start_date).days
    months = total_days // 30
    days = total_days % 30

    data["START_DATE"] = start_date.strftime("%d/%m/%Y")
    data["END_DATE"] = end_date.strftime("%d/%m/%Y")
    data["DURATION"] = f"{months} Months {days} Days"

    data["LOAN_LINE"] = f"""Loan Amount Rs. {data['AMOUNT']}/- from {data['START_DATE']} to {data['END_DATE']}."""

    return data


def generate_doc(data):
    doc = Document("template.docx")

    for para in doc.paragraphs:
        for key, value in data.items():
            if f"{{{{{key}}}}}" in para.text:
                for run in para.runs:
                    run.text = run.text.replace(f"{{{{{key}}}}}", str(value))

    file_name = f"{data['NAME']}.docx"
    doc.save(file_name)

    return file_name


def generate_pdf(data):
    file_name = f"{data['NAME']}.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph(f"Client: {data['NAME']}", styles["Normal"]))
    content.append(Paragraph(f"Amount: ₹{data['AMOUNT']}", styles["Normal"]))
    content.append(Paragraph(f"Duration: {data['DURATION']}", styles["Normal"]))

    doc.build(content)

    return file_name
