import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import plotly.express as px
from streamlit_plotly_events import plotly_events
import numpy as np
import plotly.graph_objects as go
# ============================================================
# PART 6 : DASHBOARD HEADER
# ============================================================
import streamlit as st

st.set_page_config(
    page_title="West Bengal Air Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>

/* Remove Streamlit top padding */
.block-container{
    padding-top:2rem;
}

/* ===========================
      HERO SECTION
=========================== */

.hero{
    position:relative;
    overflow:hidden;
    padding:55px;
    border-radius:28px;

    background:
    radial-gradient(circle at top right,#38bdf833 0%,transparent 30%),
    radial-gradient(circle at bottom left,#06b6d433 0%,transparent 30%),
    linear-gradient(-45deg,#020617,#0f172a,#172554,#1e3a8a,#0f172a);

    background-size:400% 400%;

    animation:gradientMove 18s ease infinite;

    border:1px solid rgba(255,255,255,.08);

    box-shadow:
    0 15px 35px rgba(0,0,0,.45),
    inset 0 0 25px rgba(255,255,255,.03);
}

/* Animated background */

@keyframes gradientMove{

0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}

}

/* Floating particles */

.hero::before{

content:"";

position:absolute;

width:900px;
height:900px;

background:
radial-gradient(#38bdf8 1.2px, transparent 1.2px);

background-size:40px 40px;

opacity:.15;

animation:float 50s linear infinite;

top:-250px;
left:-200px;

}

@keyframes float{

0%{transform:translateY(0px);}
100%{transform:translateY(-120px);}

}

/* Layout */

.hero-content{

display:flex;

align-items:center;

gap:35px;

position:relative;

z-index:2;

}

/* Globe */

.globe{

font-size:90px;

animation:spin 20s linear infinite;

filter:drop-shadow(0 0 25px #38bdf8);

}

@keyframes spin{

from{transform:rotate(0deg);}
to{transform:rotate(360deg);}

}

/* Title */

.hero-title{

font-size:52px;

font-weight:800;

color:white;

line-height:1.2;

text-shadow:
0 0 15px rgba(56,189,248,.4);

}

/* Subtitle */

.hero-sub{

margin-top:14px;

font-size:19px;

color:#d1d5db;

line-height:1.7;

max-width:900px;

}

/* Badge */

.hero-badge{

display:inline-block;

margin-top:25px;

padding:10px 20px;

border-radius:999px;

background:rgba(56,189,248,.15);

border:1px solid rgba(56,189,248,.35);

color:#7dd3fc;

font-weight:600;

backdrop-filter:blur(10px);

}

/* Divider */

.hero-divider{

margin-top:25px;

height:2px;

background:linear-gradient(to right,#38bdf8,transparent);

width:320px;

}

/* Hover */

.hero:hover{

transform:translateY(-2px);

transition:.4s;

box-shadow:
0 18px 45px rgba(0,0,0,.5),
0 0 30px rgba(56,189,248,.15);

}

</style>
""", unsafe_allow_html=True)

st.markdown("""

<div class="hero">

<div class="hero-content">

<div class="globe">
🌍
</div>

<div>

<div class="hero-title">

West Bengal Air Quality Dashboard

</div>

<div class="hero-divider"></div>

<div class="hero-sub">

An interactive <b>GIS-based Environmental Monitoring Platform</b> for
visualizing air quality across monitoring stations in West Bengal.
Explore spatial patterns, analyze pollution trends, and gain actionable
environmental insights through interactive maps and analytics.

</div>

<div class="hero-badge">

🛰️ GIS • 📊 Interactive Analytics • 🌱 Environmental Intelligence • 📍 Real-Time Monitoring

</div>

</div>

</div>

</div>

""", unsafe_allow_html=True)
from datetime import datetime

st.caption(
    f"🕒 Last Updated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
)

#DATA****************
data = pd.read_csv("daily_air_quality.csv")
month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

available_months = [
    month for month in month_order
    if month in data["Month"].unique()
]



# ============================================================
# PART 3.5 : INITIALIZE FILTER STATES
# ============================================================

if "selected_month" not in st.session_state:
    st.session_state.selected_month = "All"

if "selected_district" not in st.session_state:
    st.session_state.selected_district = "All"

if "selected_location" not in st.session_state:
    st.session_state.selected_location = "All Stations"

if "aqi_range" not in st.session_state:
    st.session_state.aqi_range = (
        int(data["AQI"].min()),
        int(data["AQI"].max())
    )


# ============================================================
# RESET FILTERS FUNCTION
# ============================================================

def reset_filters():

    st.session_state.selected_month = "All"
    st.session_state.selected_district = "All"
    st.session_state.selected_location = "All Stations"

    st.session_state.aqi_range = (
        int(data["AQI"].min()),
        int(data["AQI"].max())
    )

# ===============================
# SIDEBAR FILTERS
# ===============================
# ============================================================
# PREMIUM SIDEBAR CSS
# ============================================================

st.sidebar.markdown(
    """
<style>

/* ============================================================
   SIDEBAR BACKGROUND
============================================================ */

section[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #07111f 0%,
        #0b1728 45%,
        #111827 100%
    );
    border-right:1px solid rgba(56,189,248,.15);
}

/* ============================================================
   REMOVE DEFAULT PADDING
============================================================ */

section[data-testid="stSidebar"] > div{
    padding-top:1rem;
    padding-left:1rem;
    padding-right:1rem;
}

/* ============================================================
   SCROLLBAR
============================================================ */

section[data-testid="stSidebar"]::-webkit-scrollbar{
    width:8px;
}

section[data-testid="stSidebar"]::-webkit-scrollbar-track{
    background:transparent;
}

section[data-testid="stSidebar"]::-webkit-scrollbar-thumb{
    background:#38bdf8;
    border-radius:20px;
}

/* ============================================================
   HEADINGS
============================================================ */

.filter-heading{

    font-size:16px;
    font-weight:700;
    color:white;

    margin-top:18px;
    margin-bottom:10px;

    padding-bottom:8px;

    border-bottom:1px solid rgba(255,255,255,.08);

    letter-spacing:.5px;

}

/* ============================================================
   LABELS
============================================================ */

section[data-testid="stSidebar"] label{

    color:#E5E7EB !important;
    font-weight:600 !important;
    font-size:14px;

}

/* ============================================================
   TEXT INPUT
============================================================ */

section[data-testid="stSidebar"] input{

    background:rgba(15,23,42,.85)!important;

    color:white!important;

    border-radius:14px!important;

    border:1px solid rgba(56,189,248,.25)!important;

    transition:.25s;

}

section[data-testid="stSidebar"] input:focus{

    border:1px solid #38bdf8!important;

    box-shadow:0 0 14px rgba(56,189,248,.30)!important;

}

/* ============================================================
   SELECT BOX
============================================================ */

section[data-testid="stSidebar"] div[data-baseweb="select"]{

    background:rgba(15,23,42,.85)!important;

    border-radius:14px!important;

    border:1px solid rgba(56,189,248,.25)!important;

    transition:.25s;

}

section[data-testid="stSidebar"] div[data-baseweb="select"]:hover{

    border:1px solid #38bdf8!important;

    box-shadow:0 0 12px rgba(56,189,248,.20)!important;

}

/* ============================================================
   MULTISELECT
============================================================ */

section[data-testid="stSidebar"] div[data-baseweb="tag"]{

    background:#0ea5e9!important;

    color:white!important;

}

/* ============================================================
   SLIDER
============================================================ */

section[data-testid="stSidebar"] .stSlider{

    padding-top:8px;
    padding-bottom:8px;

}

/* ============================================================
   BUTTON
============================================================ */

section[data-testid="stSidebar"] button{

    width:100%;

    border:none!important;

    border-radius:14px!important;

    background:linear-gradient(
        135deg,
        #0284c7,
        #0ea5e9
    )!important;

    color:white!important;

    font-weight:700!important;

    transition:.25s;

}

section[data-testid="stSidebar"] button:hover{

    transform:translateY(-2px);

    box-shadow:0 0 18px rgba(14,165,233,.35);

}

/* ============================================================
   DIVIDER
============================================================ */

.sidebar-divider{

    height:1px;

    margin:22px 0;

    background:rgba(255,255,255,.08);

}

/* ============================================================
   GLASS CARD
============================================================ */

.sidebar-card{

    background:rgba(255,255,255,.05);

    border:1px solid rgba(255,255,255,.08);

    border-radius:18px;

    padding:18px;

    margin-bottom:18px;

    backdrop-filter:blur(14px);

    transition:.25s;

}

.sidebar-card:hover{

    border-color:#38bdf8;

    box-shadow:0 0 18px rgba(56,189,248,.18);

    transform:translateY(-2px);

}

/* ============================================================
   SMALL TEXT
============================================================ */

.sidebar-small{

    color:#94A3B8;

    font-size:12px;

}

/* ============================================================
   METRIC VALUE
============================================================ */

.metric-value{

    color:white;

    font-size:28px;

    font-weight:700;

}

</style>
""",
    unsafe_allow_html=True
)
# ============================================================
# PREMIUM SIDEBAR HEADER
# ============================================================
# ============================================================
# SIDEBAR HEADER
# ============================================================

st.sidebar.markdown("""
<style>
.sidebar-header{
    background:linear-gradient(135deg,#0284c7,#2563eb);
    padding:18px;
    border-radius:18px;
    text-align:center;
    border:1px solid rgba(255,255,255,.10);
    margin-bottom:18px;
}

.sidebar-title{
    color:white;
    font-size:22px;
    font-weight:700;
    margin-bottom:4px;
}

.sidebar-subtitle{
    color:#dbeafe;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.container().markdown(
"""
<div class="sidebar-header">

# 🌍

<div class="sidebar-title">
Air Quality Dashboard
</div>

<div class="sidebar-subtitle">
West Bengal Monitoring System
</div>

</div>
""",
unsafe_allow_html=True
)

# ============================================================
# PART 3 : TIME FILTER
# ============================================================

st.sidebar.markdown(
    """
    <div class="filter-heading">
        📅 Time Filter
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Month Order
# --------------------------

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

available_months = [
    month for month in month_order
    if month in data["Month"].dropna().unique()
]

selected_month = st.sidebar.selectbox(
    "Select Month",
    options=["All"] + available_months,
    key="selected_month"
)

st.sidebar.markdown(
    """
    <div class="sidebar-divider"></div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PART 4 : STATION SEARCH
# ============================================================

st.sidebar.markdown(
    """
    <div class="filter-heading">
        🔍 Search Monitoring Station
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------
# Get all stations
# ---------------------------------------

locations = sorted(data["Location"].dropna().unique())

# ---------------------------------------
# Search Box
# ---------------------------------------

search_station = st.sidebar.text_input(
    "",
    placeholder="Search like Google Maps...",
    key="station_search"
)

# ---------------------------------------
# Live Search
# ---------------------------------------

if search_station.strip():

    matched_locations = [
        location
        for location in locations
        if search_station.lower() in location.lower()
    ]

else:

    matched_locations = locations

# ---------------------------------------
# If nothing found
# ---------------------------------------

if len(matched_locations) == 0:

    st.sidebar.warning("No matching station found.")

    matched_locations = ["All Stations"]

# ---------------------------------------
# Station Dropdown
# ---------------------------------------

selected_location = st.sidebar.selectbox(
    "Choose Station",
    options=["All Stations"] + matched_locations,
    key="selected_location"
)

# ---------------------------------------
# Station Information
# ---------------------------------------

if selected_location != "All Stations":

    station_records = data[
        data["Location"] == selected_location
    ]

    district = station_records["District"].iloc[0]

    latest_aqi = round(
        station_records["AQI"].mean(),
        1
    )

    st.sidebar.markdown(
        f"""
        <div style="
            background:rgba(17,24,39,.75);
            border:1px solid rgba(56,189,248,.18);
            border-radius:14px;
            padding:12px;
            margin-top:10px;
            margin-bottom:10px;
        ">

        <div style="font-size:16px;font-weight:700;color:white;">
        📍 {selected_location}
        </div>

        <div style="font-size:13px;color:#cbd5e1;margin-top:6px;">
        District
        </div>

        <div style="font-size:15px;color:#38bdf8;font-weight:600;">
        {district}
        </div>

        <div style="font-size:13px;color:#cbd5e1;margin-top:10px;">
        Average AQI
        </div>

        <div style="font-size:22px;font-weight:700;color:white;">
        {latest_aqi}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown(
    """
    <div class="sidebar-divider"></div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PART 5 : AQI FILTER
# ============================================================

st.sidebar.markdown(
    """
    <div class="filter-heading">
        🌫 AQI Filter
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# AQI Minimum & Maximum
# ------------------------------------------------

aqi_min = int(data["AQI"].min())
aqi_max = int(data["AQI"].max())

# ------------------------------------------------
# AQI Slider
# ------------------------------------------------

aqi_range = st.sidebar.slider(
    "Select AQI Range",
    min_value=aqi_min,
    max_value=aqi_max,
    value=(aqi_min, aqi_max),
    key="aqi_range"
)

# ------------------------------------------------
# AQI Legend
# ------------------------------------------------

st.sidebar.markdown("""

<div style="margin-top:15px;">

<div style="font-size:14px;
font-weight:600;
margin-bottom:10px;
color:white;">
AQI Categories
</div>

<div style="display:flex;
align-items:center;
margin-bottom:8px;">

<div style="
width:14px;
height:14px;
border-radius:50%;
background:#22c55e;
margin-right:10px;
"></div>

<div style="font-size:13px;color:#e5e7eb;">
Good (0–50)
</div>

</div>

<div style="display:flex;
align-items:center;
margin-bottom:8px;">

<div style="
width:14px;
height:14px;
border-radius:50%;
background:#eab308;
margin-right:10px;
"></div>

<div style="font-size:13px;color:#e5e7eb;">
Moderate (51–100)
</div>

</div>

<div style="display:flex;
align-items:center;
margin-bottom:8px;">

<div style="
width:14px;
height:14px;
border-radius:50%;
background:#f97316;
margin-right:10px;
"></div>

<div style="font-size:13px;color:#e5e7eb;">
Poor (101–200)
</div>

</div>

<div style="display:flex;
align-items:center;
margin-bottom:8px;">

<div style="
width:14px;
height:14px;
border-radius:50%;
background:#ef4444;
margin-right:10px;
"></div>

<div style="font-size:13px;color:#e5e7eb;">
Very Poor (201–300)
</div>

</div>

<div style="display:flex;
align-items:center;">

<div style="
width:14px;
height:14px;
border-radius:50%;
background:#7f1d1d;
margin-right:10px;
"></div>

<div style="font-size:13px;color:#e5e7eb;">
Severe (301+)
</div>

</div>

</div>

""", unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <div class="sidebar-divider"></div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PART 6 : APPLY FILTERS
# ============================================================

# ----------------------------------------
# Start with the full dataset
# ----------------------------------------

filtered_data = data.copy()

# ----------------------------------------
# Apply Month Filter
# ----------------------------------------

if selected_month != "All":

    filtered_data = filtered_data[
        filtered_data["Month"] == selected_month
    ]

# ----------------------------------------
# Apply Station Filter
# ----------------------------------------

if selected_location != "All Stations":

    filtered_data = filtered_data[
        filtered_data["Location"] == selected_location
    ]

# ----------------------------------------
# Apply AQI Filter
# ----------------------------------------

filtered_data = filtered_data[
    (filtered_data["AQI"] >= aqi_range[0]) &
    (filtered_data["AQI"] <= aqi_range[1])
]

# ----------------------------------------
# Reset Index
# ----------------------------------------

filtered_data = filtered_data.reset_index(drop=True)

# ----------------------------------------
# Handle Empty Dataset
# ----------------------------------------

if filtered_data.empty:

    st.warning("⚠ No data available for the selected filters.")

    st.stop()

# ============================================================
# PART 7 : CURRENT SELECTION
# ============================================================

st.sidebar.markdown(
    """
    <div class="filter-heading">
        📊 Current Selection
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# Calculate Statistics
# ------------------------------------------------

total_stations = filtered_data["Location"].nunique()

total_records = len(filtered_data)

average_aqi = filtered_data["AQI"].mean()

average_temp = filtered_data["TEMPERATURE (°C)"].mean()

average_humidity = filtered_data["REL HUMI (%)"].mean()

# ------------------------------------------------
# Handle Empty Values
# ------------------------------------------------

if filtered_data.empty:

    average_aqi = 0
    average_temp = 0
    average_humidity = 0

# ------------------------------------------------
# Premium Cards
# ------------------------------------------------

st.sidebar.markdown(
    f"""
    
<div style="
background:rgba(17,24,39,.80);
border:1px solid rgba(56,189,248,.15);
border-radius:16px;
padding:15px;
margin-bottom:12px;
">

<div style="font-size:13px;color:#94a3b8;">
📍 Monitoring Stations
</div>

<div style="
font-size:28px;
font-weight:700;
color:white;
margin-top:5px;
">
{total_stations}
</div>

</div>

<div style="
background:rgba(17,24,39,.80);
border:1px solid rgba(56,189,248,.15);
border-radius:16px;
padding:15px;
margin-bottom:12px;
">

<div style="font-size:13px;color:#94a3b8;">
📄 Total Records
</div>

<div style="
font-size:28px;
font-weight:700;
color:white;
margin-top:5px;
">
{total_records:,}
</div>

</div>

<div style="
background:rgba(17,24,39,.80);
border:1px solid rgba(56,189,248,.15);
border-radius:16px;
padding:15px;
margin-bottom:12px;
">

<div style="font-size:13px;color:#94a3b8;">
🌫 Average AQI
</div>

<div style="
font-size:28px;
font-weight:700;
color:white;
margin-top:5px;
">
{average_aqi:.1f}
</div>

</div>

<div style="
background:rgba(17,24,39,.80);
border:1px solid rgba(56,189,248,.15);
border-radius:16px;
padding:15px;
margin-bottom:12px;
">

<div style="font-size:13px;color:#94a3b8;">
🌡 Average Temperature
</div>

<div style="
font-size:28px;
font-weight:700;
color:white;
margin-top:5px;
">
{average_temp:.1f}°C
</div>

</div>

<div style="
background:rgba(17,24,39,.80);
border:1px solid rgba(56,189,248,.15);
border-radius:16px;
padding:15px;
margin-bottom:10px;
">

<div style="font-size:13px;color:#94a3b8;">
💧 Average Humidity
</div>

<div style="
font-size:28px;
font-weight:700;
color:white;
margin-top:5px;
">
{average_humidity:.1f}%
</div>

</div>

""",
unsafe_allow_html=True
)

st.sidebar.markdown(
"""
<div class="sidebar-divider"></div>
""",
unsafe_allow_html=True
)

# ============================================================
# PART 8 : RESET FILTERS
# ============================================================
st.sidebar.button(
    "🔄 Reset All Filters",
    use_container_width=True,
    on_click=reset_filters
)

# ============================================================
# SIDEBAR FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.markdown("#### 🌍 Air Quality Dashboard")

st.sidebar.caption("West Bengal Air Quality Monitoring System")

st.sidebar.caption(
    "Powered by Streamlit • Plotly • Folium"
)

st.sidebar.caption("© 2026 Spandan Dutta")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# =====================================
# KPI STATUS FUNCTIONS
# =====================================

def get_aqi_status(aqi):
    if aqi <= 50:
        return "🟢 Good", "#22c55e", "rgba(34,197,94,.18)"
    elif aqi <= 100:
        return "🟡 Moderate", "#facc15", "rgba(250,204,21,.18)"
    elif aqi <= 150:
        return "🟠 USG", "#fb923c", "rgba(251,146,60,.18)"
    elif aqi <= 200:
        return "🔴 Unhealthy", "#ef4444", "rgba(239,68,68,.18)"
    elif aqi <= 300:
        return "🟣 Very Unhealthy", "#a855f7", "rgba(168,85,247,.18)"
    else:
        return "⚫ Hazardous", "#991b1b", "rgba(153,27,27,.18)"


def get_temp_status(temp):
    if temp < 20:
        return "🟢 Cool", "#3b82f6", "rgba(59,130,246,.18)"
    elif temp < 30:
        return "🟢 Pleasant", "#22c55e", "rgba(34,197,94,.18)"
    elif temp < 35:
        return "🟠 Warm", "#f59e0b", "rgba(245,158,11,.18)"
    else:
        return "🔴 Hot", "#ef4444", "rgba(239,68,68,.18)"


def get_humidity_status(h):
    if h < 40:
        return "🟠 Dry", "#f97316", "rgba(249,115,22,.18)"
    elif h <= 70:
        return "🟢 Comfortable", "#22c55e", "rgba(34,197,94,.18)"
    else:
        return "🔵 Humid", "#38bdf8", "rgba(56,189,248,.18)"

# =====================================
# KPI VALUES
# =====================================

stations = filtered_data["Location"].nunique()

records = len(filtered_data)

avg_aqi = filtered_data["AQI"].mean()

avg_temp = filtered_data["TEMPERATURE (°C)"].mean()

avg_humidity = filtered_data["REL HUMI (%)"].mean()


aqi_status, aqi_text, aqi_bg = get_aqi_status(avg_aqi)

temp_status, temp_text, temp_bg = get_temp_status(avg_temp)

humidity_status, humidity_text, humidity_bg = get_humidity_status(avg_humidity)

# ===============================
# LAST UPDATED
# ===============================

filtered_data["Date"] = pd.to_datetime(
    filtered_data["Date"],
    format="mixed",
    dayfirst=True
)
last_updated = filtered_data["Date"].max().strftime("%d %b %Y")
st.markdown("""
<style>
.kpi-container{
display:grid;
grid-template-columns:repeat(5,1fr);
gap:20px;
margin-bottom:35px;
}

.kpi-card{

position:relative;

overflow:hidden;

padding:24px;

border-radius:22px;

background:rgba(17,24,39,.72);

backdrop-filter:blur(18px);

-webkit-backdrop-filter:blur(18px);

border:1px solid rgba(255,255,255,.08);

box-shadow:

0 10px 35px rgba(0,0,0,.35),

inset 0 1px 1px rgba(255,255,255,.05);

transition:.4s ease;

}

.kpi-card:hover{

transform:translateY(-10px);

border:1px solid rgba(56,189,248,.4);

box-shadow:

0 20px 45px rgba(56,189,248,.22),

0 0 35px rgba(56,189,248,.18),

inset 0 1px 1px rgba(255,255,255,.08);

}

.kpi-card::before{

content:"";

position:absolute;

left:0;

top:0;

height:5px;

width:100%;

background:linear-gradient(
90deg,
var(--accent),
#38bdf8,
#818cf8);

}

.kpi-icon{

font-size:38px;

display:inline-block;

animation:pulseIcon 2.2s infinite;

filter:drop-shadow(0 0 10px rgba(56,189,248,.35));

}

@keyframes pulseIcon{

0%{

transform:scale(1);

}

50%{

transform:scale(1.15);

}

100%{

transform:scale(1);

}

}

.kpi-title{

margin-top:10px;

font-size:13px;

font-weight:600;

letter-spacing:1px;

text-transform:uppercase;

color:#94a3b8;

}

.kpi-value{

margin-top:8px;

font-size:34px;

font-weight:700;

color:white;

}

.kpi-status{

margin-top:14px;

display:inline-flex;

align-items:center;

gap:8px;

padding:7px 14px;

border-radius:999px;

background:var(--badge-bg);

color:var(--badge-color);

font-size:12px;

font-weight:700;

}

.live-dot{

width:9px;

height:9px;

border-radius:50%;

background:#22c55e;

animation:blink 1.3s infinite;

box-shadow:0 0 12px #22c55e;

}

@keyframes blink{

0%{

opacity:.3;

transform:scale(.8);

}

50%{

opacity:1;

transform:scale(1.25);

}

100%{

opacity:.3;

transform:scale(.8);

}

}

.kpi-footer{

margin-top:18px;

padding-top:14px;

border-top:1px solid rgba(255,255,255,.08);

display:flex;

justify-content:space-between;

align-items:center;

font-size:11px;

color:#94a3b8;

}

.update{

display:flex;

align-items:center;

gap:6px;

}

@media(max-width:1400px){

.kpi-container{

grid-template-columns:repeat(3,1fr);

}

}

@media(max-width:900px){

.kpi-container{

grid-template-columns:repeat(2,1fr);

}

}

@media(max-width:600px){

.kpi-container{

grid-template-columns:1fr;

}

}
</style>
""", unsafe_allow_html=True)

st.markdown("## 📊 Dashboard Overview")

st.markdown(f"""

<div class="kpi-container">

<!-- Monitoring Stations -->
<div class="kpi-card" style="--accent:#38bdf8; --badge-bg:rgba(56,189,248,.18); --badge-color:#7dd3fc;">
<div style="position:absolute;width:220px;height:220px;right:-110px;top:-110px;border-radius:50%;background:radial-gradient(circle,var(--accent),transparent 70%);opacity:.12;"></div>

<div class="kpi-icon">📍</div>
<div class="kpi-title">Monitoring Stations</div>
<div class="kpi-value">{stations}</div>

<div class="kpi-status">🟢 Active</div>

<div class="kpi-footer">
<div class="update">
<div class="live-dot"></div>
<span>Updated just now</span>
</div>
<div>📅 {last_updated}</div>
</div>

</div>


<!-- Total Records -->
<div class="kpi-card" style="--accent:#22c55e; --badge-bg:rgba(34,197,94,.18); --badge-color:#4ade80;">
<div style="position:absolute;width:220px;height:220px;right:-110px;top:-110px;border-radius:50%;background:radial-gradient(circle,var(--accent),transparent 70%);opacity:.12;"></div>

<div class="kpi-icon">📝</div>
<div class="kpi-title">Total Records</div>
<div class="kpi-value">{records:,}</div>

<div class="kpi-status">📊 Complete Dataset</div>

<div class="kpi-footer">
<div class="update">
<div class="live-dot"></div>
<span>Updated just now</span>
</div>
<div>📅 {last_updated}</div>
</div>

</div>


<!-- Average AQI -->
<div class="kpi-card" style="--accent:{aqi_text}; --badge-bg:{aqi_bg}; --badge-color:{aqi_text};">
<div style="position:absolute;width:220px;height:220px;right:-110px;top:-110px;border-radius:50%;background:radial-gradient(circle,var(--accent),transparent 70%);opacity:.12;"></div>

<div class="kpi-icon">🌫️</div>
<div class="kpi-title">Average AQI</div>
<div class="kpi-value">{avg_aqi:.1f}</div>

<div class="kpi-status">{aqi_status}</div>

<div class="kpi-footer">
<div class="update">
<div class="live-dot"></div>
<span>Updated just now</span>
</div>
<div>📅 {last_updated}</div>
</div>

</div>


<!-- Temperature -->
<div class="kpi-card" style="--accent:{temp_text}; --badge-bg:{temp_bg}; --badge-color:{temp_text};">
<div style="position:absolute;width:220px;height:220px;right:-110px;top:-110px;border-radius:50%;background:radial-gradient(circle,var(--accent),transparent 70%);opacity:.12;"></div>

<div class="kpi-icon">🌡️</div>
<div class="kpi-title">Average Temperature</div>
<div class="kpi-value">{avg_temp:.1f}°C</div>

<div class="kpi-status">{temp_status}</div>

<div class="kpi-footer">
<div class="update">
<div class="live-dot"></div>
<span>Updated just now</span>
</div>
<div>📅 {last_updated}</div>
</div>

</div>


<!-- Humidity -->
<div class="kpi-card" style="--accent:{humidity_text}; --badge-bg:{humidity_bg}; --badge-color:{humidity_text};">
<div style="position:absolute;width:220px;height:220px;right:-110px;top:-110px;border-radius:50%;background:radial-gradient(circle,var(--accent),transparent 70%);opacity:.12;"></div>

<div class="kpi-icon">💧</div>
<div class="kpi-title">Average Humidity</div>
<div class="kpi-value">{avg_humidity:.1f}%</div>

<div class="kpi-status">{humidity_status}</div>

<div class="kpi-footer">
<div class="update">
<div class="live-dot"></div>
<span>Updated just now</span>
</div>
<div>📅 {last_updated}</div>
</div>

</div>

</div>

""", unsafe_allow_html=True)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Most polluted district
polluted_district = (
    filtered_data.groupby("District")["AQI"]
    .mean()
    .idxmax()
)

# Most polluted station
polluted_station = filtered_data.loc[
    filtered_data["AQI"].idxmax()
]

# Cleanest station
cleanest_station = filtered_data.loc[
    filtered_data["AQI"].idxmin()
]

# Average AQI
avg_aqi = filtered_data["AQI"].mean()

# Highest PM2.5
max_pm25 = filtered_data["PM 2.5 AVG (µg/m³)"].max()

# Highest PM10
max_pm10 = filtered_data["PM 10 AVG (µg/m³)"].max()

# Average Temperature
avg_temp = filtered_data["TEMPERATURE (°C)"].mean()

# Average Humidity
avg_humidity = filtered_data["REL HUMI (%)"].mean()

# Month with highest AQI
highest_month = (
    filtered_data.groupby("Month")["AQI"]
    .mean()
    .idxmax()
)

corr = filtered_data[
    [
        "AQI",
        "PM 2.5 AVG (µg/m³)",
        "PM 10 AVG (µg/m³)",
        "TEMPERATURE (°C)",
        "REL HUMI (%)"
    ]
].corr()

corr_no_diag = corr.where(~np.eye(corr.shape[0], dtype=bool))

strongest = corr_no_diag.abs().stack().idxmax()

corr_value = corr.loc[strongest]

# ============================
# DASHBOARD INSIGHTS
# ============================

# Status Functions
def aqi_status(aqi):
    if aqi <= 50:
        return "🟢 Good", "#22c55e"
    elif aqi <= 100:
        return "🟡 Moderate", "#eab308"
    elif aqi <= 150:
        return "🟠 USG", "#f97316"
    elif aqi <= 200:
        return "🔴 Unhealthy", "#ef4444"
    elif aqi <= 300:
        return "🟣 Very Unhealthy", "#8b5cf6"
    else:
        return "⚫ Hazardous", "#7f1d1d"


def temp_status(temp):
    if temp < 20:
        return "🟢 Cool", "#3b82f6"
    elif temp <= 30:
        return "🟡 Pleasant", "#22c55e"
    elif temp <= 35:
        return "🟠 Warm", "#f59e0b"
    else:
        return "🔴 Hot", "#ef4444"


def humidity_status(h):
    if h < 40:
        return "🟠 Dry", "#f97316"
    elif h <= 70:
        return "🟢 Comfortable", "#22c55e"
    else:
        return "🔵 Humid", "#06b6d4"


# Badge values
aqi_badge, aqi_color = aqi_status(avg_aqi)
clean_badge, clean_color = aqi_status(cleanest_station["AQI"])
polluted_badge, polluted_color = aqi_status(polluted_station["AQI"])
temp_badge, temp_color = temp_status(avg_temp)
humidity_badge, humidity_color = humidity_status(avg_humidity)


# CSS
st.markdown("""
<style>

.insight-container{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
    gap:18px;
    margin-top:15px;
}

.insight-card{
    background:linear-gradient(145deg,#1e293b,#0f172a);
    border-radius:18px;
    padding:20px;
    border:1px solid rgba(255,255,255,.08);
    transition:.35s;
    box-shadow:0 8px 25px rgba(0,0,0,.35);
}

.insight-card:hover{
    transform:translateY(-6px);
    box-shadow:0 10px 30px rgba(56,189,248,.25);
}

.insight-card::before{
    content:"";
    position:absolute;
    left:0;
    top:0;
    width:6px;
    height:100%;
    background:var(--accent);
}

.icon{
    font-size:30px;
}

.title{
    color:#94A3B8;
    font-size:14px;
    text-transform:uppercase;
    margin-top:8px;
}

.value{
    color:white;
    font-size:24px;
    font-weight:bold;
    margin-top:8px;
}

.subtitle{
    color:#38BDF8;
    font-size:15px;
    margin-top:6px;
}

.badge{
    display:inline-block;
    margin-top:12px;
    padding:6px 12px;
    border-radius:20px;
    color:white;
    font-size:13px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)


st.subheader("📌 Dashboard Insights")

st.markdown(f"""

<div class="insight-container">

<div class="insight-card" style="--accent:#ef4444">
<div class="icon">🏭</div>
<div class="title">Most Polluted District</div>
<div class="value">{polluted_district}</div>
</div>

<div class="insight-card" style="--accent:#22c55e">
<div class="icon">🌿</div>
<div class="title">Cleanest Station</div>
<div class="value">{cleanest_station['Location']}</div>
<div class="subtitle">AQI {cleanest_station['AQI']:.1f}</div>
<div class="badge" style="background:{clean_color};">{clean_badge}</div>
</div>

<div class="insight-card" style="--accent:#f97316">
<div class="icon">📍</div>
<div class="title">Most Polluted Station</div>
<div class="value">{polluted_station['Location']}</div>
<div class="subtitle">AQI {polluted_station['AQI']:.1f}</div>
<div class="badge" style="background:{polluted_color};">{polluted_badge}</div>
</div>

<div class="insight-card" style="--accent:#06b6d4">
<div class="icon">📊</div>
<div class="title">Average AQI</div>
<div class="value">{avg_aqi:.1f}</div>
<div class="badge" style="background:{aqi_color};">{aqi_badge}</div>
</div>

<div class="insight-card" style="--accent:#3b82f6">
<div class="icon">🌬️</div>
<div class="title">Highest PM2.5</div>
<div class="value">{max_pm25:.1f}</div>
<div class="subtitle">µg/m³</div>
</div>

<div class="insight-card" style="--accent:#8b5cf6">
<div class="icon">🌫️</div>
<div class="title">Highest PM10</div>
<div class="value">{max_pm10:.1f}</div>
<div class="subtitle">µg/m³</div>
</div>

<div class="insight-card" style="--accent:#eab308">
<div class="icon">🌡️</div>
<div class="title">Average Temperature</div>
<div class="value">{avg_temp:.1f}°C</div>
<div class="badge" style="background:{temp_color};">{temp_badge}</div>
</div>

<div class="insight-card" style="--accent:#14b8a6">
<div class="icon">💧</div>
<div class="title">Average Humidity</div>
<div class="value">{avg_humidity:.1f}%</div>
<div class="badge" style="background:{humidity_color};">{humidity_badge}</div>
</div>

<div class="insight-card" style="--accent:#ec4899">
<div class="icon">📅</div>
<div class="title">Highest AQI Month</div>
<div class="value">{highest_month}</div>
</div>

<div class="insight-card" style="--accent:#38bdf8">
<div class="icon">📈</div>
<div class="title">Strongest Correlation</div>
<div class="value">{strongest[0]}</div>
<div class="subtitle">↔ {strongest[1]} ({corr_value:.2f})</div>
</div>

</div>

""", unsafe_allow_html=True)
# ===============================
# INTERACTIVE MAP
# ===============================

# ============================================================
# PART 8 : AIR QUALITY MONITORING MAP
# ============================================================

st.markdown("---")

with st.expander("🗺 Air Quality Monitoring Map", expanded=True):

    st.markdown(
        """
        <h2 style='margin-bottom:5px;'>
        🗺 Air Quality Monitoring Map
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Explore the locations of air quality monitoring stations across West Bengal. "
        "Use the map to identify station locations and view their latest Air Quality Index (AQI) values."
    )

    # ============================================================
    # CREATE MAP
    # ============================================================

    m = folium.Map(
        location=[
            filtered_data["Latitude"].mean(),
            filtered_data["Longitude"].mean()
        ],
        zoom_start=7,
        tiles=None,
        control_scale=True
    )

    # ============================================================
    # BASEMAPS
    # ============================================================

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="🗺 OpenStreetMap"
    ).add_to(m)

    folium.TileLayer(
        tiles="CartoDB Positron",
        name="🌐 CartoDB Positron"
    ).add_to(m)

    folium.TileLayer(
        tiles="CartoDB Dark_Matter",
        name="🌙 CartoDB Dark Matter"
    ).add_to(m)

    folium.TileLayer(
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr="© OpenTopoMap contributors",
        name="⛰ OpenTopoMap"
    ).add_to(m)

    folium.TileLayer(
        tiles="https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="🛰 Esri World Imagery"
    ).add_to(m)

    folium.TileLayer(
        tiles="https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="🏔 Esri World Topographic"
    ).add_to(m)
    
    marker_cluster = MarkerCluster(
        name="📍 AQI Stations"
    ).add_to(m)
    # One record per station
    map_data = (
        filtered_data
        .sort_values("Date")
        .drop_duplicates(subset="Location", keep="last")
    )

    for _, row in map_data.iterrows():

        aqi = row["AQI"]

        if aqi <= 50:
            marker_color = "green"
        elif aqi <= 100:
            marker_color = "lightgreen"
        elif aqi <= 200:
            marker_color = "orange"
        elif aqi <= 300:
            marker_color = "red"
        elif aqi <= 400:
            marker_color = "purple"
        else:
            marker_color = "darkred"

        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=row["Location"],
            popup=f"""
            <b>Station:</b> {row['Location']}<br>
            <b>District:</b> {row['District']}<br>
            <b>AQI:</b> {round(row['AQI'],2)}<br>
            <b>PM2.5:</b> {round(row['PM 2.5 AVG (µg/m³)'],2)}<br>
            <b>PM10:</b> {round(row['PM 10 AVG (µg/m³)'],2)}<br>
            <b>Temperature:</b> {round(row['TEMPERATURE (°C)'],2)} °C<br>
            <b>Humidity:</b> {round(row['REL HUMI (%)'],2)} %
            """,
            icon=folium.Icon(
                color=marker_color,
                icon="info-sign"
            )
        ).add_to(marker_cluster)

    legend_html = """
    <div style="
    position: fixed;
    bottom: 50px;
    right: 50px;
    z-index:9999;
    background:black;
    padding:15px;
    border:2px solid grey;
    border-radius:8px;
    box-shadow:2px 2px 8px rgba(0,0,0,0.3);
    font-size:14px;
    ">

    <b style="font-size:16px;">AQI Legend</b>
    <hr>

    <div><span style="color:green;">●</span> Good (0–50)</div>
    <div><span style="color:lightgreen;">●</span> Satisfactory (51–100)</div>
    <div><span style="color:orange;">●</span> Moderate (101–200)</div>
    <div><span style="color:red;">●</span> Poor (201–300)</div>
    <div><span style="color:purple;">●</span> Very Poor (301–400)</div>
    <div><span style="color:darkred;">●</span> Severe (>400)</div>

    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl(collapsed=False).add_to(m)

    st_folium(
    m,
    use_container_width=True,
    height=750
    )
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ============================================================
# PART 9 : DASHBOARD ANALYTICS
# ============================================================

st.markdown("---")

st.header("📊 Dashboard Analytics")

st.markdown(
"""
Explore interactive charts to understand air quality patterns,
pollution trends, and weather relationships across West Bengal.
"""
)
#Data load
monthly_aqi = (
    filtered_data
    .groupby("Month")["AQI"]
    .mean()
    .reset_index()
)

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_aqi["Month"] = pd.Categorical(
    monthly_aqi["Month"],
    categories=month_order,
    ordered=True
)

monthly_aqi = monthly_aqi.sort_values("Month")

# Monthly Average AQI Trend
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 District-wise Monthly AQI Trend")
    
    # Get a sorted list of unique districts from your dataset
    districts = sorted(filtered_data["District"].dropna().unique().tolist())
    
    # Set default dropdown index to Cooch Behar if it exists in the data
    default_index = districts.index("Cooch Behar") if "Cooch Behar" in districts else 0
    
    # Add a dropdown button to select the district
    selected_district = st.selectbox("Select District:", districts, index=default_index)
    
    # Filter the data for the selected district and calculate the monthly mean
    district_data = filtered_data[filtered_data["District"] == selected_district]
    district_monthly_aqi = (
        district_data.groupby("Month")["AQI"]
        .mean()
        .reset_index()
    )
    
    # Ensure the months are in chronological order rather than alphabetical
    district_monthly_aqi["Month"] = pd.Categorical(
        district_monthly_aqi["Month"],
        categories=month_order,
        ordered=True
    )
    district_monthly_aqi = district_monthly_aqi.sort_values("Month")
    
    # Plot the filtered line chart
    fig = px.line(
        district_monthly_aqi,
        x="Month",
        y="AQI",
        markers=True,
        title=f"Monthly Average AQI for {selected_district}"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        title_x=0.5,
        xaxis_title="Month",
        yaxis_title="Average AQI"
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:
    st.subheader("🌡️ Monthly Average AQI Heatmap")

    # Month order
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Calculate monthly average AQI
    heatmap_data = (
        filtered_data.groupby(["District", "Month"])["AQI"]
        .mean()
        .reset_index()
    )

    # Make month categorical for proper ordering
    heatmap_data["Month"] = pd.Categorical(
        heatmap_data["Month"],
        categories=month_order,
        ordered=True
    )

    # Pivot table
    heatmap_pivot = heatmap_data.pivot(
        index="District",
        columns="Month",
        values="AQI"
    )

    # Reorder columns
    heatmap_pivot = heatmap_pivot.reindex(columns=month_order)

    # Create heatmap
    fig = px.imshow(
        heatmap_pivot,
        text_auto=".1f",
        color_continuous_scale="RdYlGn_r",
        aspect="auto",
        labels=dict(
            x="Month",
            y="District",
            color="Average AQI"
        ),
        title="Monthly Average AQI by District"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        title_x=0.5,
        coloraxis_colorbar=dict(
            title="AQI"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
# ============================================================
# AQI CATEGORY DISTRIBUTION
# ============================================================
# 1. Define a unified color map (Standard AQI breaks)
aqi_color_map = {
    "Good": "#00E400",
    "Satisfactory": "#92D050",
    "Moderate": "#FFFF00",
    "Poor": "#FF7E00",
    "Very Poor": "#FF0000",
    "Severe": "#800080"
}
# Define AQI bins and labels to match the color map
aqi_bins = [0, 50, 100, 200, 300, 400, float('inf')]
aqi_labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]

# Create a temporary column to categorize the AQI values
categorized_aqi = pd.cut(filtered_data["AQI"], bins=aqi_bins, labels=aqi_labels)

# Calculate the count for each category and format it for the pie chart
category_count = categorized_aqi.value_counts().reset_index()
category_count.columns = ["Category", "Count"]

# Filter out categories that have a count of 0 so they don't crowd the pie chart
category_count = category_count[category_count["Count"] > 0]
# Create columns for the distribution charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🍩 AQI Category Distribution")
    
    fig1 = px.pie(
        category_count,
        names="Category",
        values="Count",
        hole=0.5,
        color="Category",
        color_discrete_map=aqi_color_map
    )

    # Hide the legend here to avoid duplication
    fig1.update_layout(
        template="plotly_dark",
        showlegend=False,
        annotations=[
            dict(
                text="AQI",
                x=0.5,
                y=0.5,
                font_size=24,
                showarrow=False
            )
        ],
        margin=dict(t=30, b=30, l=30, r=30)
    )
    
    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True
        }
    )

with col2:
    st.subheader("📊 AQI Distribution")

    # Create histogram data
    counts, bins = np.histogram(filtered_data["AQI"], bins=30)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Map AQI values strictly to our unified color map breakpoints
    bar_colors = []
    for aqi in bin_centers:
        if aqi <= 50:
            bar_colors.append(aqi_color_map["Good"])
        elif aqi <= 100:
            bar_colors.append(aqi_color_map["Satisfactory"])
        elif aqi <= 200:
            bar_colors.append(aqi_color_map["Moderate"])
        elif aqi <= 300:
            bar_colors.append(aqi_color_map["Poor"])
        elif aqi <= 400:
            bar_colors.append(aqi_color_map["Very Poor"])
        else:
            bar_colors.append(aqi_color_map["Severe"])

    fig2 = go.Figure()

    # Add the main histogram trace
    fig2.add_trace(
        go.Bar(
            x=bin_centers,
            y=counts,
            width=np.diff(bins),
            marker_color=bar_colors,
            marker_line_color="white",
            marker_line_width=1,
            hovertemplate="<b>AQI</b>: %{x:.1f}<br><b>Frequency</b>: %{y}<extra></extra>",
            showlegend=False
        )
    )
    
    # Add dummy traces to build the single, unified dashboard legend
    legend_labels = {
        "Good (0-50)": aqi_color_map["Good"],
        "Satisfactory (51-100)": aqi_color_map["Satisfactory"],
        "Moderate (101-200)": aqi_color_map["Moderate"],
        "Poor (201-300)": aqi_color_map["Poor"],
        "Very Poor (301-400)": aqi_color_map["Very Poor"],
        "Severe (401+)": aqi_color_map["Severe"]
    }

    for name, color in legend_labels.items():
        fig2.add_trace(go.Bar(
            x=[None], y=[None],
            name=name,
            marker_color=color,
            showlegend=True
        ))

    fig2.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="AQI",
        yaxis_title="Number of Records",
        bargap=0.02,
        margin=dict(t=50, b=30, l=30, r=30),
        legend=dict(
            title="AQI Categories",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# 2. Process Monthly Data
monthly_aqi = (
    filtered_data
    .groupby("Month")["AQI"]
    .mean()
    .reset_index()
)

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_aqi["Month"] = pd.Categorical(
    monthly_aqi["Month"],
    categories=month_order,
    ordered=True
)

monthly_aqi = monthly_aqi.sort_values("Month")


# ============================================================
# AVERAGE AQI BY DISTRICT
# ============================================================
# ============================================================
# CHART 3 : DRILL-DOWN DISTRICT -> STATIONS
# ============================================================
district_aqi = (
    filtered_data
    .groupby("District")["AQI"]
    .mean()
    .reset_index()
    .sort_values("AQI", ascending=True)
)

col1, col2 = st.columns(2)

# -----------------------------
# LEFT : District Chart
# -----------------------------
with col1:
    st.subheader("🌍 Average AQI by District")

    fig = px.bar(
        district_aqi,
        x="AQI",
        y="District",
        orientation="h",
        color="AQI",
        color_continuous_scale="RdYlGn_r",
        text_auto=".1f"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        coloraxis_showscale=False,
        xaxis_title="Average AQI",
        yaxis_title="District",
        margin=dict(t=20) # Tightened top margin since we are using a subheader now
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Average AQI: %{x:.1f}<extra></extra>"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# RIGHT : Station Chart
# -----------------------------
with col2:
    st.subheader("📍 Station-wise AQI Breakdown")
    
    district_list = district_aqi["District"].tolist()
    default_index = district_list.index("Cooch Behar") if "Cooch Behar" in district_list else 0

    # District selector moved to the right side
    selected_district = st.selectbox(
        "Select a District to view stations",
        district_list,
        index=default_index
    )

    station_aqi = (
        filtered_data[
            filtered_data["District"] == selected_district
        ]
        .groupby("Location")["AQI"]
        .mean()
        .reset_index()
        .sort_values("AQI")
    )

    fig2 = px.bar(
        station_aqi,
        x="AQI",
        y="Location",
        orientation="h",
        color="AQI",
        color_continuous_scale="RdYlGn_r",
        text_auto=".1f"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=412, # Slightly reduced height to account for the selectbox above it
        coloraxis_showscale=False,
        xaxis_title="Average AQI",
        yaxis_title="Monitoring Station",
        margin=dict(t=20)
    )

    fig2.update_traces(
        hovertemplate="<b>%{y}</b><br>Average AQI: %{x:.1f}<extra></extra>"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )
# 10 most amd low polluted
col1, col2 = st.columns(2)
with col1:
    st.subheader("🔥 Top 10 Most Polluted Monitoring Stations")

    top10 = (
        filtered_data
            .groupby("Location")["AQI"]
            .mean()
            .reset_index()
            .sort_values("AQI", ascending=False)
            .head(10)
    )
    fig = px.bar(
        top10,
        x="AQI",
        y="Location",
        orientation="h",
        color="AQI",
        color_continuous_scale="Reds",
        text_auto=".1f",
        title="Top 10 Most Polluted Stations"
    )
    
    fig.update_layout(
        template="plotly_dark",
        height=500,
        title_x=0.5,
        coloraxis_showscale=False,
        xaxis_title="Average AQI",
        yaxis_title=""
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🌿 Top 10 Cleanest Monitoring Stations")
    
    clean10 = (
        filtered_data
            .groupby("Location")["AQI"]
            .mean()
            .reset_index()
            .sort_values("AQI")
            .head(10)
    )
    fig = px.bar(
        clean10,
        x="AQI",
        y="Location",
        orientation="h",
        color="AQI",
        color_continuous_scale="Greens_r",
        text_auto=".1f",
        title="Top 10 Cleanest Stations"
    )
    fig.update_layout(
        template="plotly_dark",
        height=500,
        title_x=0.5,
        coloraxis_showscale=False,
        xaxis_title="Average AQI",
        yaxis_title=""
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

# ============================================================
# LEFT : PM2.5 vs PM10 Correlation
# ============================================================
with col1:
    st.subheader("🌫️ Particulate Matter Correlation")
    st.caption("Larger, redder dots indicate a higher overall AQI.")

    fig1 = px.scatter(
        filtered_data,
        x="PM 2.5 AVG (µg/m³)",
        y="PM 10 AVG (µg/m³)",
        color="AQI",
        size="AQI",
        hover_name="Location",
        color_continuous_scale="RdYlGn_r",
        trendline="ols" # Adds a visual trendline to explain the relationship
    )

    fig1.update_layout(
        template="plotly_dark",
        height=550,
        margin=dict(t=30),
        coloraxis_colorbar=dict(title="AQI Level")
    )
    
    fig1.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>PM 2.5: %{x} µg/m³<br>PM 10: %{y} µg/m³<br>AQI: %{marker.color}<extra></extra>"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# RIGHT : Temperature vs AQI
# ============================================================
with col2:
    st.subheader("🌡️ Weather Impact on AQI")
    st.caption("Dot size reflects PM2.5 concentration. Color represents humidity.")

    fig2 = px.scatter(
        filtered_data,
        x="TEMPERATURE (°C)",
        y="AQI",
        size="PM 2.5 AVG (µg/m³)",
        color="REL HUMI (%)",
        hover_name="Location",
        color_continuous_scale="Turbo"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=550,
        margin=dict(t=30),
        coloraxis_colorbar=dict(title="Humidity (%)")
    )
    
    fig2.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Temp: %{x} °C<br>AQI: %{y}<br>Humidity: %{marker.color}%<extra></extra>"
    )

    st.plotly_chart(fig2, use_container_width=True)


st.subheader("📊 Correlation Heatmap")

corr_data = filtered_data[[
    "AQI",
    "PM 2.5 AVG (µg/m³)",
    "PM 10 AVG (µg/m³)",
    "TEMPERATURE (°C)",
    "REL HUMI (%)"
]].corr()

fig = px.imshow(
    corr_data,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    aspect="auto",
    title="Correlation Between Air Quality Variables"
)

fig.update_layout(
    template="plotly_dark",
    height=650,
    title_x=0.5,
    coloraxis_colorbar=dict(title="Correlation")
)

st.plotly_chart(fig, use_container_width=True)
col1, col2 = st.columns(2)

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# ============================================================
# LEFT : PM2.5 Trend
# ============================================================
with col1:
    st.subheader("🌬️ Monthly PM2.5 Trend")

    pm25 = (
        filtered_data
        .groupby("Month")["PM 2.5 AVG (µg/m³)"]
        .mean()
        .reset_index()
    )

    pm25["Month"] = pd.Categorical(
        pm25["Month"],
        categories=month_order,
        ordered=True
    )

    pm25 = pm25.sort_values("Month")

    fig1 = px.line(
        pm25,
        x="Month",
        y="PM 2.5 AVG (µg/m³)",
        markers=True
    )

    fig1.update_traces(
        line=dict(color="#00BFFF", width=4),
        marker=dict(size=9)
    )

    fig1.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(t=30),
        xaxis_title="Month",
        yaxis_title="PM2.5 (µg/m³)"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# RIGHT : PM10 Trend
# ============================================================
with col2:
    st.subheader("🌫️ Monthly PM10 Trend")

    pm10 = (
        filtered_data
        .groupby("Month")["PM 10 AVG (µg/m³)"]
        .mean()
        .reset_index()
    )

    pm10["Month"] = pd.Categorical(
        pm10["Month"],
        categories=month_order,
        ordered=True
    )

    pm10 = pm10.sort_values("Month")

    fig2 = px.line(
        pm10,
        x="Month",
        y="PM 10 AVG (µg/m³)",
        markers=True
    )

    fig2.update_traces(
        line=dict(color="#FF7F0E", width=4),
        marker=dict(size=9)
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(t=30),
        xaxis_title="Month",
        yaxis_title="PM10 (µg/m³)"
    )

    st.plotly_chart(fig2, use_container_width=True)
#Humidity vs AQI
st.subheader("💧 Humidity vs AQI")

fig = px.scatter(
    filtered_data,
    x="REL HUMI (%)",
    y="AQI",
    color="AQI",
    size="PM 2.5 AVG (µg/m³)",
    hover_name="Location",
    color_continuous_scale="RdYlGn_r",
    title="Humidity vs AQI"
)

fig.update_layout(
    template="plotly_dark",
    height=600,
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

# ============================================================
# LEFT : Temperature Distribution
# ============================================================
with col1:
    st.subheader("🌡 Temperature Distribution")

    fig1 = px.histogram(
        filtered_data,
        x="TEMPERATURE (°C)",
        nbins=20,
        color_discrete_sequence=["orange"]
    )

    fig1.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(t=30),
        xaxis_title="Temperature (°C)",
        yaxis_title="Count"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# RIGHT : Humidity Distribution
# ============================================================
with col2:
    st.subheader("💧 Humidity Distribution")

    fig2 = px.histogram(
        filtered_data,
        x="REL HUMI (%)",
        nbins=20,
        color_discrete_sequence=["deepskyblue"]
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(t=30),
        xaxis_title="Relative Humidity (%)",
        yaxis_title="Count"
    )

    st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

# ============================================================
# LEFT : Average Temperature by District
# ============================================================
with col1:
    st.subheader("🌡 Average Temperature by District")

    temp = filtered_data.groupby("District")["TEMPERATURE (°C)"].mean().reset_index()

    fig1 = px.bar(
        temp,
        x="TEMPERATURE (°C)",
        y="District",
        orientation="h",
        color="TEMPERATURE (°C)",
        color_continuous_scale="Turbo"
    )

    fig1.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(t=30),
        xaxis_title="Temperature (°C)",
        yaxis_title="District"
    )

    fig1.update_yaxes(autorange="reversed")

    st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# RIGHT : Average Humidity by District
# ============================================================
with col2:
    st.subheader("💧 Average Humidity by District")

    hum = filtered_data.groupby("District")["REL HUMI (%)"].mean().reset_index()

    fig2 = px.bar(
        hum,
        x="REL HUMI (%)",
        y="District",
        orientation="h",
        color="REL HUMI (%)",
        color_continuous_scale="Blues"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(t=30),
        xaxis_title="Relative Humidity (%)",
        yaxis_title="District"
    )

    fig2.update_yaxes(autorange="reversed")

    st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# ============================================================
# LEFT : Monthly Temperature Trend
# ============================================================
with col1:
    st.subheader("📈 Monthly Temperature Trend")

    monthly_temp = (
        filtered_data
        .groupby("Month")["TEMPERATURE (°C)"]
        .mean()
        .reset_index()
    )
    
    # Sort months chronologically
    monthly_temp["Month"] = pd.Categorical(
        monthly_temp["Month"],
        categories=month_order,
        ordered=True
    )
    monthly_temp = monthly_temp.sort_values("Month")

    fig1 = px.line(
        monthly_temp,
        x="Month",
        y="TEMPERATURE (°C)",
        markers=True
    )
    
    fig1.update_traces(
        line=dict(color="orange", width=4),
        marker=dict(size=9)
    )

    fig1.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(t=30),
        xaxis_title="Month",
        yaxis_title="Temperature (°C)"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# RIGHT : Monthly Humidity Trend
# ============================================================
with col2:
    st.subheader("📈 Monthly Humidity Trend")

    monthly_hum = (
        filtered_data
        .groupby("Month")["REL HUMI (%)"]
        .mean()
        .reset_index()
    )
    
    # Sort months chronologically
    monthly_hum["Month"] = pd.Categorical(
        monthly_hum["Month"],
        categories=month_order,
        ordered=True
    )
    monthly_hum = monthly_hum.sort_values("Month")

    fig2 = px.line(
        monthly_hum,
        x="Month",
        y="REL HUMI (%)",
        markers=True
    )
    
    fig2.update_traces(
        line=dict(color="deepskyblue", width=4),
        marker=dict(size=9)
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(t=30),
        xaxis_title="Month",
        yaxis_title="Relative Humidity (%)"
    )

    st.plotly_chart(fig2, use_container_width=True)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ============================================================
# AIR QUALITY DATA EXPLORER
# ============================================================
# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown("---")

st.markdown("""
<h2 style='margin-bottom:0px;'>
📋 Air Quality Data Explorer
</h2>
""", unsafe_allow_html=True)

st.caption(
    "Explore, search, filter and download air quality records."
)

# ============================================================
# TOP TOOLBAR
# ============================================================

toolbar1, toolbar2, toolbar3 = st.columns([2,1,1])

# ------------------------------------------------------------
# Search
# ------------------------------------------------------------

with toolbar1:

    search_text = st.text_input(
        "🔍 Search Records",
        placeholder="Search Location, District, Date, AQI...",
        key="table_search"
    )

# ------------------------------------------------------------
# Rows
# ------------------------------------------------------------

with toolbar2:

    row_options = {
        "10":10,
        "25":25,
        "50":50,
        "100":100,
        "All":len(filtered_data)
    }

    selected_rows = st.selectbox(
        "Rows",
        list(row_options.keys()),
        index=1
    )

    num_rows = row_options[selected_rows]

# ------------------------------------------------------------
# Download
# ------------------------------------------------------------

with toolbar3:

    st.write("")
    st.write("")

    st.download_button(
        "📥 CSV",
        filtered_data.to_csv(index=False).encode("utf-8"),
        file_name="Filtered_Air_Quality.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("")

# ============================================================
# GLOBAL SEARCH
# ============================================================

table_data = filtered_data.copy()

if search_text:

    query = search_text.lower()

    table_data = table_data[
        table_data.astype(str)
        .apply(
            lambda col: col.str.lower().str.contains(query, na=False)
        )
        .any(axis=1)
    ]

st.info(
    f"📊 Showing **{len(table_data):,}** records after search."
)

# ============================================================
# GOOGLE STYLE FILTERS
# ============================================================

st.markdown("### 🔎 Advanced Filters")

f1, f2, f3 = st.columns(3)

# ============================================================
# DISTRICT FILTER
# ============================================================

with f1:

    district_options = sorted(
        table_data["District"].dropna().unique().tolist()
    )

    selected_districts = st.multiselect(
        "🏛 District",
        options=district_options,
        default=[],
        placeholder="Search or select district...",
        key="table_district"
    )

# Filter by district
if selected_districts:

    table_data = table_data[
        table_data["District"].isin(selected_districts)
    ]


# ============================================================
# LOCATION FILTER (Dynamic)
# ============================================================

with f2:

    location_options = sorted(
        table_data["Location"].dropna().unique().tolist()
    )

    selected_locations = st.multiselect(
        "📍 Location",
        options=location_options,
        default=[],
        placeholder="Search or select location...",
        key="table_location"
    )

if selected_locations:

    table_data = table_data[
        table_data["Location"].isin(selected_locations)
    ]


# ============================================================
# AQI CATEGORY
# ============================================================

# Create AQI Category

table_data = table_data.copy()

table_data["AQI Category"] = table_data["AQI"].apply(
    lambda x:
        "Good" if x <= 50 else
        "Moderate" if x <= 100 else
        "Poor" if x <= 200 else
        "Very Poor" if x <= 300 else
        "Severe"
)

with f3:

    selected_category = st.multiselect(
        "🌫 AQI Category",
        [
            "Good",
            "Moderate",
            "Poor",
            "Very Poor",
            "Severe"
        ],
        default=[],
        placeholder="Select category...",
        key="table_aqi_category"
    )

if selected_category:

    table_data = table_data[
        table_data["AQI Category"].isin(selected_category)
    ]


# ============================================================
# FILTER SUMMARY
# ============================================================

st.caption(
    f"📊 Showing **{len(table_data):,}** matching records"
)

# ============================================================
# DISPLAY OPTIONS
# ============================================================

st.markdown("---")
st.markdown("### ⚙ Display Options")

# ---------------- Layout ----------------

left, right = st.columns([2, 1])

# ---------------- Column Selector ----------------

with left:

    all_columns = [
        "Location",
        "District",
        "AQI",
        "PM 2.5 AVG (µg/m³)",
        "PM 10 AVG (µg/m³)",
        "TEMPERATURE (°C)",
        "REL HUMI (%)",
        "Latitude",
        "Longitude",
        "Date",
        "Week",
        "Month",
        "Year"
    ]

    default_columns = [
        "Location",
        "District",
        "AQI",
        "PM 2.5 AVG (µg/m³)",
        "PM 10 AVG (µg/m³)",
        "Date"
    ]

    selected_columns = st.multiselect(
        "📑 Columns to Display",
        options=all_columns,
        default=default_columns,
        placeholder="Search or select columns..."
    )

# ---------------- Table Height ----------------

with right:

    table_height = st.slider(
        "📏 Table Height",
        min_value=300,
        max_value=900,
        value=550,
        step=50
    )

# ============================================================
# DOWNLOAD CENTER
# ============================================================

st.markdown("### 📥 Download Center")

download1, download2 = st.columns(2)

with download1:

    st.download_button(
        "📄 Download CSV",
        table_data.to_csv(index=False).encode("utf-8"),
        file_name="Filtered_Air_Quality.csv",
        mime="text/csv",
        use_container_width=True
    )

with download2:

    excel_data = table_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📊 Export Data",
        excel_data,
        file_name="Filtered_Air_Quality_Data.csv",
        mime="text/csv",
        use_container_width=True
    )

# ============================================================
# DATA SUMMARY
# ============================================================

summary1, summary2, summary3, summary4 = st.columns(4)

summary1.metric(
    "📄 Records",
    f"{len(table_data):,}"
)

summary2.metric(
    "🏛 Districts",
    table_data["District"].nunique()
)

summary3.metric(
    "📍 Locations",
    table_data["Location"].nunique()
)

summary4.metric(
    "🌫 Avg AQI",
    round(table_data["AQI"].mean(), 1)
)

st.markdown("---")

# ============================================================
# INTERACTIVE DATA TABLE
# ============================================================

st.markdown("### 📊 Interactive Air Quality Table")

if len(selected_columns) == 0:

    st.warning("Please select at least one column.")

else:

    display_table = table_data[selected_columns].head(num_rows)

    st.dataframe(
        display_table,
        use_container_width=True,
        hide_index=True,
        height=table_height
    )

st.caption(
    f"Displaying {min(num_rows, len(table_data)):,} of {len(table_data):,} filtered records."
)

# ============================================================
# PREMIUM INTERACTIVE TABLE
# ============================================================

st.markdown("---")
st.markdown("## 📊 Interactive Air Quality Table")

display_table = table_data[selected_columns].head(num_rows).copy()

# ============================================================
# FORMAT NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "AQI",
    "PM 2.5 AVG (µg/m³)",
    "PM 10 AVG (µg/m³)",
    "TEMPERATURE (°C)",
    "REL HUMI (%)"
]

for col in numeric_columns:
    if col in display_table.columns:
        display_table[col] = display_table[col].round(2)

# ============================================================
# COLOR AQI VALUES
# ============================================================

styler = display_table.style

if "AQI" in display_table.columns:

    styler = styler.background_gradient(
        subset=["AQI"],
        cmap="RdYlGn_r"
    )

# PM2.5

if "PM 2.5 AVG (µg/m³)" in display_table.columns:

    styler = styler.background_gradient(
        subset=["PM 2.5 AVG (µg/m³)"],
        cmap="Oranges"
    )

# PM10

if "PM 10 AVG (µg/m³)" in display_table.columns:

    styler = styler.background_gradient(
        subset=["PM 10 AVG (µg/m³)"],
        cmap="Purples"
    )

# Temperature

if "TEMPERATURE (°C)" in display_table.columns:

    styler = styler.background_gradient(
        subset=["TEMPERATURE (°C)"],
        cmap="coolwarm"
    )

# ============================================================
# DISPLAY TABLE
# ============================================================

st.dataframe(
    styler,
    use_container_width=True,
    hide_index=True,
    height=table_height
)

st.caption(
    f"Displaying {len(display_table):,} of {len(table_data):,} filtered records."
)

summary1, summary2, summary3, summary4 = st.columns(4)

summary1.metric(
    "📄 Records",
    f"{len(table_data):,}"
)

summary2.metric(
    "🏛 Districts",
    table_data["District"].nunique()
)

summary3.metric(
    "📍 Stations",
    table_data["Location"].nunique()
)

summary4.metric(
    "🌫 Avg AQI",
    f"{table_data['AQI'].mean():.1f}"
)


st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:
    st.info(
        f"Highest AQI : **{table_data['AQI'].max():.0f}**"
    )

with c2:
    st.success(
        f"Lowest AQI : **{table_data['AQI'].min():.0f}**"
    )

with c3:
    st.warning(
        f"Median AQI : **{table_data['AQI'].median():.1f}**"
    )



st.markdown("""
<style>

/* ==============================
   Premium Footer
============================== */

.footer {
    margin-top: 60px;
    padding: 25px 35px;
    border-radius: 18px;
    background: linear-gradient(135deg,#0f172a,#1e293b);
    border: 1px solid rgba(255,255,255,0.12);
    color: #f8fafc;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
}

.footer-title{
    font-size:24px;
    font-weight:700;
    color:#38bdf8;
    margin-bottom:8px;
}

.footer-subtitle{
    font-size:15px;
    color:#cbd5e1;
    margin-bottom:20px;
}

.footer-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:20px;
}

.footer-card{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;
    padding:15px;
}

.footer-card h4{
    color:#7dd3fc;
    margin-bottom:10px;
    font-size:16px;
}

.footer-card p{
    margin:4px 0;
    font-size:14px;
    color:#e2e8f0;
}

.footer-bottom{
    margin-top:25px;
    padding-top:15px;
    border-top:1px solid rgba(255,255,255,0.12);
    text-align:center;
    font-size:13px;
    color:#94a3b8;
}

</style>

<div class="footer">

<div class="footer-title">
🌍 West Bengal Air Quality Dashboard
</div>

<div class="footer-subtitle">
Real-Time Air Quality Monitoring & Geospatial Analytics Platform
</div>

<div class="footer-grid">

<div class="footer-card">
<h4>Developer</h4>
<p><b>Spandan Dutta</b></p>
<p>M.Sc. Geoinformatics</p>
<p>Adamas University</p>
</div>

<div class="footer-card">
<h4>Technologies</h4>
<p>Python</p>
<p>Streamlit</p>
<p>Folium</p>
<p>Plotly</p>
<p>Pandas</p>
</div>

<div class="footer-card">
<h4>Features</h4>
<p>Interactive Maps</p>
<p>AQI Analytics</p>
<p>Data Visualization</p>
<p>Download Reports</p>
</div>

</div>

<div class="footer-bottom">
© 2026 Spandan Dutta • M.Sc. Geoinformatics • Adamas University • Built with ❤️ using Python & Streamlit
</div>

</div>

""", unsafe_allow_html=True)