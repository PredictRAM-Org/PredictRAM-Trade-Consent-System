# app.py
import streamlit as st
import os
from flask import Flask, request, render_template
from urllib.parse import quote_plus

app = Flask(__name__)

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
    unique_link = quote_plus(request.url_root + f"confirm/{generate_unique_link(user_data)}")

    # Display the unique link to the user
    st.success(f"Unique Link Generated: {unique_link}")

# Admin section to check the status of links
st.header("Admin Section")

admin_link = st.text_input("Enter Unique Link:")
if st.button("Check Status"):
    try:
        filename = f"{admin_link}.txt"
        with open(filename, 'r') as file:
            user_data = file.read()
            st.success(f"User Data:\n{user_data}")
    except FileNotFoundError:
        st.error("Invalid Unique Link. No data found.")


# Flask routes
@app.route('/confirm/<unique_link>', methods=['GET', 'POST'])
def confirm_submission(unique_link):
    filename = f"{unique_link}.txt"

    if request.method == 'GET':
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                user_data = file.read()
                return render_template('confirm.html', user_data=user_data, unique_link=unique_link)
        else:
            return "Invalid Link", 404

    elif request.method == 'POST':
        status = request.form.get('status')
        result_filename = f"{unique_link}_result.txt"

        with open(result_filename, 'w') as result_file:
            result_file.write(f"Status: {status}")

        return "Result recorded successfully"


if __name__ == "__main__":
    app.run(debug=True)
