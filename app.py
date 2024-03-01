# app.py
import streamlit as st
import os
import random
from flask import Flask, request, current_app
from flask_mail import Mail, Message
from urllib.parse import quote_plus

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'support@predictram.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'support@predictram.com'
app.config['MAIL_PASSWORD'] = 'Singh@54812'

mail = Mail(app)

# Generate a unique link
def generate_unique_link():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    unique_link = ''.join(random.choice(characters) for i in range(20))
    return unique_link

# Streamlit app
st.title("Stock Form")

user_name = st.text_input("User Name")
user_email = st.text_input("User Email")
stock_name = st.text_input("Stock Name")
current_price = st.number_input("Current Price", step=0.01)
stop_loss = st.number_input("Stop Loss", step=0.01)
target = st.number_input("Target", step=0.01)

if st.button("Submit"):
    # Save the form data in a dictionary
    form_data = {
        "User Name": user_name,
        "User Email": user_email,
        "Stock Name": stock_name,
        "Current Price": current_price,
        "Stop Loss": stop_loss,
        "Target": target,
    }

    # Save the form data to a file with a unique link
    unique_link = generate_unique_link()
    filename = f"{unique_link}.txt"
    with open(filename, 'w') as file:
        for key, value in form_data.items():
            file.write(f"{key}: {value}\n")

    # Store the unique link in Streamlit app state
    st.session_state.unique_link = unique_link

    # Send email with the unique link
    with app.app_context():
        subject = "Stock Form Submission"
        body = f"Thank you for submitting the stock form. Click the link to confirm: {'http://localhost:8501/confirm/' + quote_plus(unique_link)}"
        msg = Message(subject, recipients=[user_email], body=body)
        mail.send(msg)

    st.success("Form submitted successfully. Check your email to confirm.")
