# app.py
import streamlit as st
import os
import random
from flask import Flask, request
from flask_mail import Mail, Message
from urllib.parse import quote_plus

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'

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

    # Send email with the unique link
    subject = "Stock Form Submission"
    body = f"Thank you for submitting the stock form. Click the link to confirm: {request.url_root}confirm/{quote_plus(unique_link)}"
    msg = Message(subject, recipients=[user_email], body=body)
    mail.send(msg)

    st.success("Form submitted successfully. Check your email to confirm.")

# Flask routes
@app.route('/confirm/<unique_link>')
def confirm_submission(unique_link):
    filename = f"{unique_link}.txt"
    if os.path.exists(filename):
        os.remove(filename)
        return "Content received. Thank you!", 200
    else:
        return "Content pending. Invalid link.", 404

if __name__ == "__main__":
    # Run Flask app in the background
    import threading
    threading.Thread(target=app.run, kwargs={'port': 8501}).start()
