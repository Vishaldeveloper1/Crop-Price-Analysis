import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

from weather import get_weather

from api import (
    get_mandi_data,
    get_states,
    get_districts
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Smart Farmer Assistant",
    layout="wide"
)

# =====================================
# LOAD MODEL
# =====================================

model = pickle.load(
    open("models/model_v2.pkl", "rb")
)

# =====================================
# TITLE
# =====================================

st.title("Smart Farmer Decision Support System")

st.markdown(
    "AI-Based Crop Price Prediction & Farmer Assistance Platform"
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🌱 Farmer Inputs")

# =====================================
# STATE
# =====================================

states = get_states()

if len(states) == 0:

    st.error(
        "API not working or no data found"
    )

    st.stop()

selected_state = st.sidebar.selectbox(
    "Select State",
    states
)

# =====================================
# DISTRICT
# =====================================

districts = get_districts(selected_state)

selected_district = st.sidebar.selectbox(
    "Select District",
    districts
)

# =====================================
# OTHER INPUTS
# =====================================

# =====================================
# INDIA CURRENT DATE & TIME
# =====================================

india = pytz.timezone('Asia/Kolkata')

current_time = datetime.now(india)

current_year = current_time.year
current_month = current_time.month
current_day = current_time.day
current_clock = current_time.strftime("%H:%M:%S")

st.sidebar.markdown("## 🇮🇳 Current India Time")

st.sidebar.write(f"Date: {current_day}-{current_month}-{current_year}")
st.sidebar.write(f"Time: {current_clock}")
# =====================================
# FUTURE SELLING DATE
# =====================================

future_date = st.sidebar.date_input(
    "Select Future Selling Date"
)

future_year = future_date.year
future_month = future_date.month

min_price = st.sidebar.number_input(
    "Minimum Price (₹)",
    0
)

max_price = st.sidebar.number_input(
    "Maximum Price (₹)",
    0
)

production = st.sidebar.number_input(
    "Production (Quintals)",
    0
)

area = st.sidebar.number_input(
    "Area (in hectares)",
    0
)

cost = st.sidebar.number_input(
    "Total Farming Cost(₹)",
    0
)

quantity = st.sidebar.number_input(
    "Quantity (Quintals) you want to sell",
    1
)


# =====================================
# WEATHER
# =====================================

temp, humidity = get_weather(selected_district)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🌡 Temperature",
        f"{temp} °C"
    )

with col2:
    st.metric(
        "💧 Humidity",
        f"{humidity}%"
    )

# =====================================
# SEASON FUNCTION
# =====================================

def get_season(month):

    if month in [6,7,8,9]:
        return 1

    elif month in [10,11,12,1]:
        return 2

    else:
        return 3

season = get_season(future_month)

# =====================================
# PREDICTION BUTTON
# =====================================

if st.button("Predict Crop Price"):

    # =================================
    # MODEL PREDICTION
    # =================================

    features = np.array([[
        future_year,
        future_month,
        min_price,
        max_price,
        production,
        area,
        season,
        50,
        temp
    ]])

    prediction = model.predict(features)

    predicted_price = prediction[0]
    # =====================================
    # FUTURE PRICE ADJUSTMENT
    # =====================================

    month_difference = (
        (future_year - current_year) * 12
        +
        (future_month - current_month)
    )

    future_growth = 1 + (0.02 * month_difference)

    future_predicted_price = predicted_price * future_growth

    st.success(
    f" Predicted Future Crop Price: ₹ {future_predicted_price:.2f}"
    )

    st.info(
    f" Predicted for: {future_date}"
)

    # =================================
    # SELL / HOLD ADVICE
    # =================================

    avg_price = (
        min_price + max_price
    ) / 2

    if predicted_price > avg_price:

        st.info(
            " सलाह: कुछ समय इंतजार करें, कीमत बढ़ सकती है"
        )

    else:

        st.warning(
            " सलाह: अभी बेच देना बेहतर हो सकता है"
        )

    # =================================
    # PROFIT ANALYSIS
    # =================================

    profit = (
        predicted_price * quantity
    ) - cost

    st.subheader(" Profit Analysis")

    st.write(
        f"Estimated Profit: ₹ {profit:.2f}"
    )

    # =================================
    # CROP RECOMMENDATION
    # =================================

    st.subheader(" Crop Recommendation")

    if temp > 30:

        st.success(
            "Recommended Crop: Rice"
        )

    elif humidity > 70:

        st.success(
            "Recommended Crop: Sugarcane"
        )

    else:

        st.success(
            "Recommended Crop: Wheat"
        )

    # =================================
    # LIVE MANDI DATA
    # =================================

    st.subheader(" Live Mandi Prices")

    mandi_data = get_mandi_data(
        selected_state,
        selected_district
    )

    if mandi_data.empty:

        st.warning(
            "No mandi data available"
        )

    else:

        mandi_display = mandi_data[[
            'Price Date',
            'market',
            'commodity',
            'modal_price',
            'min_price',
            'max_price'
        ]]

        st.dataframe(mandi_display)

        # =============================
        # BEST MARKET
        # =============================

        mandi_display[
            'modal_price'
        ] = mandi_display[
            'modal_price'
        ].astype(float)

        best_market = mandi_display.loc[
            mandi_display[
                'modal_price'
            ].idxmax()
        ]

        future_best_price = (
            float(best_market['modal_price'])
            * future_growth
        )

        st.success(
            f" Best Future Market: {best_market['market']} "
            f"Expected Price on {future_date}: ₹ {future_best_price:.2f}"
        )

        # =============================
        # CHART
        # =============================

        fig = px.bar(
            mandi_display,
            x='market',
            y='modal_price',
            color='commodity',
            title="Mandi Price Comparison"
        )

        st.plotly_chart(fig)

# =====================================
# HELP SECTION
# =====================================

with st.expander(" Complete User Guide"):

    st.markdown("""

    ## How To Use This System

    This platform helps farmers predict crop prices,
    compare mandi prices, and make better selling decisions.

    ---

    ## Step 1 — Select State

    Choose your state from the dropdown list.

    Example:
    - Uttar Pradesh
    - Punjab
    - Haryana

    ---

    ## Step 2 — Select District

    Select your district.

    Weather and mandi data will automatically update.

    Example:
    - Lucknow
    - Kanpur
    - Ludhiana

    ---

    ## Step 3 — Enter Year & Month

    Enter:
    - Current Year
    - Current Month

    Example:
    - Year: 2026
    - Month: 7

    ---

    ## Step 4 — Enter Price Details

    ### Minimum Price
    Lowest mandi price of crop
    Unit:
    ₹ per Quintal

    ### Maximum Price
    Highest mandi price of crop
    Unit:
    ₹ per Quintal

    ---

    ## Step 5 — Enter Production

    Total crop production.

    Unit:
    Quintal

    Example:
    100 Quintal

    ---

    ## Step 6 — Enter Land Area

    Total farming land area.

    Unit:
    Hectare

    Example:
    2 Hectare

    ---

    ## Step 7 — Enter Farming Cost

    Total farming expense.

    Include:
    - seeds
    - fertilizer
    - irrigation
    - labor

    Unit:
    ₹ Rupees

    ---

    ## Step 8 — Enter Selling Quantity

    Amount of crop you want to sell.

    Unit:
    Quintal

    ---

    ## Step 9 — Click Predict Button

    System will:
    ✅ Predict crop price
    ✅ Show weather
    ✅ Show mandi prices
    ✅ Suggest best market
    ✅ Calculate estimated profit
    ✅ Recommend suitable crops

    

    """)