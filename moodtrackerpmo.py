# Install dependencies first:
# pip install streamlit pandas matplotlib streamlit-extras

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_extras.let_it_rain import rain

# --- App Config ---
st.set_page_config(page_title="Office Mood Tracker", page_icon="😊", layout="centered")

# --- App Title ---
st.title("😊 Office Mood Tracker")
st.markdown("### 🌟 Track the team's mood in real-time & boost engagement!")

# --- Mood Options ---
mood_options = {
    "😄 Happy": "Pastel1",
    "😌 Calm": "Pastel2",
    "😓 Stressed": "cool",
    "🔥 On Fire": "autumn",
    "💡 Productive": "summer",
    "😴 Tired": "gray",
    "🙌 Excited": "spring"
}

# --- User Input ---
with st.form("mood_form", clear_on_submit=True):
    name = st.text_input("👤 Enter your name:")
    mood = st.radio("🎯 Select your mood for today:", list(mood_options.keys()))
    submitted = st.form_submit_button("Submit Mood")

if submitted:
    if name:
        df = pd.DataFrame([[name, mood]], columns=["Name", "Mood"])
        try:
            df_existing = pd.read_csv("mood_data.csv")
            df = pd.concat([df_existing, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_csv("mood_data.csv", index=False)

        # Confetti celebration!
        rain(
            emoji="🎉",
            font_size=54,
            falling_speed=5,
            animation_length=2,
        )
        st.success(f"Thank you, {name}! Your mood '{mood}' has been recorded 🌟")
    else:
        st.error("Oops! Please enter your name before submitting.")

# --- Mood Summary ---
st.markdown("---")
st.header("📊 Team Mood Summary")

try:
    df = pd.read_csv("mood_data.csv")
    mood_counts = df['Mood'].value_counts()

    # Pie Chart
    fig, ax = plt.subplots()
    mood_counts.plot.pie(
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Pastel1.colors,
        ax=ax,
        textprops={'fontsize': 10}
    )
    ax.set_ylabel('')
    ax.set_title('Current Team Mood', fontsize=14)
    st.pyplot(fig)

    # Data Table
    with st.expander("🔍 View Raw Mood Data"):
        st.dataframe(df, use_container_width=True)

    # Download Option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Mood Data",
        data=csv,
        file_name='team_mood_summary.csv',
        mime='text/csv',
    )

except FileNotFoundError:
    st.info("No mood data yet. Be the first to submit!")

# --- Footer ---
st.markdown("---")
st.markdown(
    "Made with ❤️ for team vibes by [Poorvi]. "
    "Track, reflect, and brighten up the workday! 🌈"
)
