import streamlit as st
from google import genai
from PIL import Image
import pandas as pd
import plotly.express as px
import datetime
import os


MY_API_KEY = "AIzaSyB_hX7phr0Azu5R96ziEQOJ3kZoEwiJa3E"
client = genai.Client(api_key=MY_API_KEY)
LOG_FILE = "food_log.csv"

st.set_page_config(page_title="NutriSnap Pro", layout="wide")

# Initialize the log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["Date", "Food", "Calories", "Protein", "Carbs", "Fat"])
    df.to_csv(LOG_FILE, index=False)

# --- 2. SIDEBAR MATH ---
with st.sidebar:
    st.header("📊 Daily Progress")
    goal = st.number_input("Goal (kcal)", value=2000)
    
    # Read the log to calculate totals
    log_df = pd.read_csv(LOG_FILE)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_data = log_df[log_df['Date'] == today]
    
    total_consumed = today_data['Calories'].sum()
    remaining = goal - total_consumed
    
    st.metric("Consumed", f"{total_consumed} kcal")
    st.metric("Remaining", f"{remaining} kcal", delta_color="inverse")
    st.progress(min(total_consumed / goal, 1.0))


st.title("🥗 NutriSnap Pro")

col1, col2 = st.columns([1, 1])

with col1:
    picture = st.camera_input("Snap your meal")
    if picture:
        img = Image.open(picture)
        if st.button("Analyze & Prepare Log"):
            try:
                
                prompt = """Identify the food. Return ONLY these values separated by commas: 
                Food Name, Calories (number only), Protein (grams only), Carbs (grams only), Fat (grams only).
                Example: Pizza, 300, 12, 35, 10"""
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt, img]
                )
                
                # Split the AI's response into variables
                data = response.text.split(',')
                st.session_state['last_analysis'] = {
                    "Date": today,
                    "Food": data[0].strip(),
                    "Calories": int(data[1].strip()),
                    "Protein": int(data[2].strip()),
                    "Carbs": int(data[3].strip()),
                    "Fat": int(data[4].strip())
                }
                st.success(f"Identified: {data[0]}")
            except Exception as e:
                st.error(f"Analysis failed: {e}")

with col2:
    if 'last_analysis' in st.session_state:
        results = st.session_state['last_analysis']
        st.subheader(f"Results for {results['Food']}")
        
       
        c1, c2, c3 = st.columns(3)
        c1.metric("Protein", f"{results['Protein']}g")
        c2.metric("Carbs", f"{results['Carbs']}g")
        c3.metric("Fat", f"{results['Fat']}g")

        
        chart_data = pd.DataFrame({
            "Nutrient": ["Protein", "Carbs", "Fat"],
            "Grams": [results['Protein'], results['Carbs'], results['Fat']]
        })
        fig = px.pie(chart_data, values='Grams', names='Nutrient', title="Macro Distribution", hole=.3)
        st.plotly_chart(fig, use_container_width=True)

       
        if st.button("✅ Save to Daily Log"):
            new_row = pd.DataFrame([results])
            new_row.to_csv(LOG_FILE, mode='a', header=False, index=False)
            st.success("Saved! Refreshing totals...")
            st.rerun()


st.divider()
st.subheader("📝 Today's History")
st.dataframe(today_data, use_container_width=True)