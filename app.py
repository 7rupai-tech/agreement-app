import streamlit as st
import json
from engine import process_data, generate_doc, generate_pdf
from auth import login

# Login check
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

st.set_page_config(page_title="Agreement System", layout="wide")

st.title("📄 Client Agreement System")

# INPUT

    }
name = st.text_input("Client Name")
amount = st.text_input("Amount (₹)")
date = st.date_input("Investment Date")

lender = st.text_input("Lender Name")
bank = st.text_input("Bank Account")
mode = st.text_input("Payment Mode")
txn = st.text_input("Transaction ID")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
nominee = st.text_input("Nominee Name")
relation = st.text_input("Relation")
fees = st.text_input("Processing Fees")

generate = st.button("🚀 Generate Agreement")

if generate:

    data = {
        "NAME": name,
        "AMOUNT": amount,
        "INVESTMENT_DATE": date.strftime("%d/%m/%Y"),

        "LENDER_NAME": lender,
        "BANK": bank,
        "MODE": mode,
        "TRANSACTION_ID": txn,
        "EMAIL": email,
        "PHONE": phone,
        "NOMINEE": nominee,
        "RELATION": relation,
        "PROCESSING_FEES": fees
    }
    data = process_data(data)

    doc_file = generate_doc(data)
    pdf_file = generate_pdf(data)

    with open("database.json", "a") as f:
        import json
        f.write(json.dumps(data) + "\n")

    st.success("✅ Agreement Created")

    st.download_button("📄 Download DOCX", open(doc_file, "rb"), doc_file)
    st.download_button("📄 Download PDF", open(pdf_file, "rb"), pdf_file)

    # Save data
    with open("database.json", "a") as f:
        f.write(json.dumps(data) + "\n")

    st.success("✅ Agreement Created")

    # Download buttons
    st.download_button("📄 Download DOCX", open(doc_file, "rb"), doc_file)
    st.download_button("📄 Download PDF", open(pdf_file, "rb"), pdf_file)

    # WhatsApp share
    message = f"Agreement ready for {data['NAME']} Amount ₹{data['AMOUNT']}"
    whatsapp_url = f"https://wa.me/?text={message}"
    st.markdown(f"[📲 Share on WhatsApp]({whatsapp_url})")


# VIEW CLIENTS
st.header("📁 Clients")

try:
    with open("database.json", "r") as f:
        lines = f.readlines()
        for line in lines[::-1]:
            client = json.loads(line)
            st.write(f"👤 {client['NAME']} | ₹{client['AMOUNT']} | {client['START_DATE']} → {client['END_DATE']}")
except:
    st.info("No clients yet")
    lender = st.text_input("Lender Name")
bank = st.text_input("Bank Account")
mode = st.text_input("Payment Mode (UPI/Bank)")
txn = st.text_input("Transaction ID")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
nominee = st.text_input("Nominee Name")
relation = st.text_input("Relation with Nominee")
fees = st.text_input("Processing Fees (₹)")
