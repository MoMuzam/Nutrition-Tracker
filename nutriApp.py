import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
import pandas as pd
import plotly.express as px
import datetime

# --- 1. SECURITY & CONFIG ---
# Load the key from the .env file
load_dotenv()
MY_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="NutriSnap Pro", layout="wide", page_icon="🥗")

# The Single, Strict Key Check
if not MY_API_KEY:
    st.error("🚨 Missing API Key! Please check your .env file.")
    st.stop()

# Initialize the AI Client
try:
    client = genai.Client(api_key=MY_API_KEY)
except Exception as e:
    st.error(f"Failed to connect to Google: {e}")
    st.stop()

LOG_FILE = "food_log.csv"

# Initialize the log file if it's missing
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=[
        "Date", "Food", "Calories", "Protein", "Carbs", "Fat", 
        "Score", "Ingredients", "Explanation"
    ])
    df.to_csv(LOG_FILE, index=False)

# --- 2. SIDEBAR (Daily Math) ---
with st.sidebar:
    st.header("📊 Daily Progress")
    goal = st.number_input("Goal (kcal)", value=2000)
    
    log_df = pd.read_csv(LOG_FILE)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_data = log_df[log_df['Date'] == today]
    
    total_consumed = today_data['Calories'].sum()
    remaining = goal - total_consumed
    
    st.metric("Consumed Today", f"{total_consumed} kcal")
    st.metric("Remaining", f"{remaining} kcal", delta_color="inverse")
    st.progress(min(total_consumed / goal, 1.0))

# --- 3. MAIN INTERFACE ---
st.title("🥗 NutriSnap Pro")
st.caption("AI-Powered Nutritionist & Calorie Tracker")

col1, col2 = st.columns([1, 1])
with col1:
    picture = st.camera_input("Snap your meal")
    if picture:
        img = Image.open(picture)
        if st.button("Analyze & Rate Meal"):
            try:
                prompt = """Identify the food in this image. 
                1. Provide a health score from 1-100 (where 100 is super healthy).
                2. List the likely key ingredients.
                3. Give a 1-sentence explanation for the score.

                Return the data in this EXACT format for my app to read:
                Food Name | Calories | Protein | Carbs | Fat | Health Score | Ingredients | Explanation
                """
                
                with st.spinner("Nutritionist is analyzing..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=[prompt, img]
                    )
                    
                    data = response.text.split('|')
                    st.session_state['last_analysis'] = {
                        "Date": today,
                        "Food": data[0].strip(),
                        "Calories": int(data[1].strip()),
                        "Protein": int(data[2].strip()),
                        "Carbs": int(data[3].strip()),
                        "Fat": int(data[4].strip()),
                        "Score": int(data[5].strip()),
                        "Ingredients": data[6].strip(),
                        "Explanation": data[7].strip()
                    }
            except Exception as e:
                st.error("AI formatting error. Please try snapping the photo again!")

with col2:
    if 'last_analysis' in st.session_state:
        res = st.session_state['last_analysis']
        
        st.subheader(f"Results: {res['Food']}")
        
        score = res['Score']
        if score >= 80:
            st.success(f"Health Score: {score}/100 — Excellent!")
        elif score >= 50:
            st.warning(f"Health Score: {score}/100 — Moderate")
        else:
            st.error(f"Health Score: {score}/100 — Highly Processed")
            
        st.write(f"**Ingredients:** {res['Ingredients']}")
        st.info(f"**Why this score?** {res['Explanation']}")

        chart_df = pd.DataFrame({
            "Nutrient": ["Protein", "Carbs", "Fat"],
            "Grams": [res['Protein'], res['Carbs'], res['Fat']]
        })
        fig = px.pie(chart_df, values='Grams', names='Nutrient', hole=.4, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

        if st.button("✅ Log this Meal"):
            new_row = pd.DataFrame([res])
            new_row.to_csv(LOG_FILE, mode='a', header=False, index=False)
            st.success("Saved to your log!")
            st.rerun()

# --- 4. DATA HISTORY ---
st.divider()
st.subheader("📝 Today's Log")
if not today_data.empty:
    st.dataframe(today_data[["Food", "Calories", "Score", "Ingredients"]], use_container_width=True)
else:
    st.write("No meals logged yet today. Time to eat!")