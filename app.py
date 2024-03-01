# streamlit_app.py
import streamlit as st
import os
import random
from flask import Flask, request, jsonify
from urllib.parse import quote_plus

app = Flask(__name__)

# Generate a unique link
def generate_unique_link(user_data):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    unique_link = ''.join(random.choice(characters) for i in range(20))

    # Save the user data to a file with the unique link
    filename = f"{unique_link}.txt"
    with open(filename, 'w') as file:
        for key, value in user_data.items():
            file.write(f"{key}: {value}\n")

    return unique_link

# Streamlit app
st.title("Stock Form")

user_name = st.text_input("User Name")
user_email = st.text_input("User Email")
stock_name = st.text_input("Stock Name")
current_price = st.number_input("Current Price", step=0.01)
stop_loss = st.number_input("Stop Loss", step=0.01)
target = st.number_input("Target", step=0.01)

if st.button("Generate Unique Link"):
    # Save the form data in a dictionary
    user_data = {
        "User Name": user_name,
        "User Email": user_email,
        "Stock Name": stock_name,
        "Current Price": current_price,
        "Stop Loss": stop_loss,
        "Target": target,
    }

    # Generate a unique link
    with app.app_context():
        unique_link = quote_plus(request.url_root + f"confirm/{generate_unique_link(user_data)}")

    # Display the unique link to the user
    st.success(f"Unique Link Generated: {unique_link}")

# Admin section to check the status of links
st.header("Admin Section")

admin_link = st.text_input("Enter Unique Link:")
if st.button("Check Status"):
    try:
        with app.app_context():
            response = jsonify(requests.post(f"https://predictram-trade-consent-system.streamlit.app/confirm/{admin_link}").text)
            st.success(response)
    except FileNotFoundError:
        st.error("Invalid Unique Link. No data found.")
