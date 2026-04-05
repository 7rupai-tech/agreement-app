import streamlit as st

USERS = {
    "admin": "1234",
    "aditya": "1234"
}

def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state["logged_in"] = True
            st.success("Login successful")
        else:
            st.error("Invalid credentials")
