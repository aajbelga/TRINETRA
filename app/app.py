import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import joblib
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="GeoShield Kashmir",
    layout="wide"
)

st.title("GeoShield Kashmir")
st.subheader("AI-Powered Conflict Risk Forecasting System")

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv(
    r"D:\GeoShield-Kashmir\data\raw\gtd.csv",
    low_memory=False
)

india_df = df[
    df['country_txt'] == 'India'
]

jk_df = india_df[
    india_df['provstate'] == 'Jammu and Kashmir'
]

jk_df = jk_df[
    [
        'iyear',
        'imonth',
        'iday',
        'latitude',
        'longitude',
        'city',
        'attacktype1_txt',
        'weaptype1_txt',
        'nkill'
    ]
]

jk_df = jk_df.dropna(
    subset=['latitude', 'longitude']
)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("Filters")

selected_year = st.sidebar.slider(
    "Select Year",
    int(jk_df['iyear'].min()),
    int(jk_df['iyear'].max()),
    2010
)

filtered_df = jk_df[
    jk_df['iyear'] == selected_year
]

# -----------------------------
# KPI SECTION
# -----------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Incidents",
    len(filtered_df)
)

col2.metric(
    "Total Fatalities",
    int(filtered_df['nkill'].sum())
)

col3.metric(
    "Affected Cities",
    filtered_df['city'].nunique()
)

# -----------------------------
# HEATMAP
# -----------------------------

st.subheader("Conflict Heatmap")

m = folium.Map(
    location=[34.0837, 74.7973],
    zoom_start=7
)

heat_data = filtered_df[
    ['latitude', 'longitude']
].values.tolist()

HeatMap(heat_data).add_to(m)

st_folium(
    m,
    width=1200,
    height=600
)

# -----------------------------
# YEARLY TREND
# -----------------------------

st.subheader("Yearly Incident Trend")

yearly_counts = jk_df.groupby('iyear').size()

fig, ax = plt.subplots(figsize=(10,5))

yearly_counts.plot(ax=ax)

ax.set_xlabel("Year")
ax.set_ylabel("Incidents")

st.pyplot(fig)

# -----------------------------
# TOP CITIES
# -----------------------------

st.subheader("Top Conflict Cities")

top_cities = jk_df['city'].value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(10,5))

top_cities.plot(
    kind='bar',
    ax=ax2
)

st.pyplot(fig2)