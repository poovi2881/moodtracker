import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
admin_password = os.getenv("ADMIN_PASSWORD")

# Page config
st.set_page_config(page_title="Your Streamlit App", layout="wide")

# Title
st.title("Welcome to My Streamlit App 🚀")

# Load your data
df = pd.read_csv("mood_tracker.csv")  # Use your actual file name

# Function to check admin password
def check_password():
    def password_entered():
        if st.session_state["password"] == admin_password:
            st.session_state["password_correct"] = True
            st.success("✅ Access granted to admin panel!")
        else:
            st.session_state["password_correct"] = False
            st.error("😅 Incorrect password!")

    if "password_correct" not in st.session_state:
        st.text_input("Enter admin password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter admin password:", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

# Main function
def main():
    st.write("This is your main app content here.")
    # Add your main app functions here

    # Admin mode trigger (only visible to you, Poorvi)
    if st.checkbox("Admin Mode 🔒"):
        if check_password():
            st.subheader("Admin Panel 🛠️")
            if st.button("Show Data"):
                st.write(df)

            st.download_button(
                label="Download Data as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='data_export.csv',
                mime='text/csv'
            )

# Run the app
if __name__ == '__main__':
    main()

