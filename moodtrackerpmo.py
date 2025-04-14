import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Admin password check function
def check_password():
    entered_password = st.sidebar.text_input("Enter admin password to enable download option", type="password")
    if entered_password == ADMIN_PASSWORD:
        return True
    else:
        return False

# Check if user is admin
is_admin = check_password()

# App title
st.title("Mood Tracker App 😊")

# App description
st.write("Track your mood and reflect on your day.")

# Multiple mood selection!
moods = ["Happy", "Sad", "Anxious", "Excited", "Tired", "Stressed", "Calm", "Angry", "Neutral"]
selected_moods = st.multiselect("Select your current mood(s):", moods)

# Additional input
notes = st.text_area("Any additional notes you'd like to add:")

# Submit button
if st.button("Submit"):
    if not selected_moods:
        st.warning("Please select at least one mood.")
    else:
        # Prepare data
        mood_str = ', '.join(selected_moods)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame({
            "Timestamp": [timestamp],
            "Mood": [mood_str],
            "Notes": [notes]
        })

        # Save to CSV
        if os.path.exists("mood_tracker.csv"):
            existing_data = pd.read_csv("mood_tracker.csv")
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_csv("mood_tracker.csv", index=False)

        st.success("Your mood has been recorded! ✅")

# Show data
if os.path.exists("mood_tracker.csv"):
    st.subheader("Mood Entries")
    data = pd.read_csv("mood_tracker.csv")
    st.dataframe(data)

    # Download button for admin only
    if is_admin:
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="mood_tracker.csv", mime="text/csv")
