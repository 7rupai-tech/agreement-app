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
name = st.text_input("Client Name")
amount = st.text_input("Amount (₹)")
date = st.date_input("Investment Date")

if st.button("Generate Agreement"):

    data = {
        "NAME": name,
        "AMOUNT": amount,
        "INVESTMENT_DATE": date.strftime("%d/%m/%Y")
    }

    data = process_data(data)

    doc_file = generate_doc(data)
    pdf_file = generate_pdf(data)

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
