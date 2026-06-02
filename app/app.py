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
district_risk = pd.read_csv(
    r"D:\GeoShield-Kashmir\data\processed\district_risk.csv"
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

critical = len(
    district_risk[district_risk['threat_level']=="CRITICAL"]
)

high = len(
    district_risk[district_risk['threat_level']=="HIGH"]
)

elevated = len(
    district_risk[district_risk['threat_level']=="ELEVATED"]
)

low = len(
    district_risk[district_risk['threat_level']=="LOW"]
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("🔴 Critical", critical)
c2.metric("🟠 High", high)
c3.metric("🟡 Elevated", elevated)
c4.metric("🟢 Low", low)
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
import pandas as pd
import streamlit as st

st.header("🛡️ Threat Intelligence Center")

st.subheader("Top 10 High Risk Districts")

st.dataframe(
    district_risk.sort_values(
        'threat_index',
        ascending=False
    ).head(10)
)
st.subheader("🔍 District Intelligence Search")

district = st.selectbox(
    "Select District",
    district_risk['city'].unique()
)

selected = district_risk[
    district_risk['city'] == district
]

if not selected.empty:

    row = selected.iloc[0]

    st.success(
        f"""
District: {row['city']}

Threat Index: {round(row['threat_index'],2)}

Threat Level: {row['threat_level']}

Future Outlook 2028: {row['future_outlook_2028']}
"""
    )

    if 'intel_report' in selected.columns:
        st.text(row['intel_report'])

st.subheader("🚨 Threat Level Overview")

critical_df = district_risk[
    district_risk['threat_level'] == "CRITICAL"
]

high_df = district_risk[
    district_risk['threat_level'] == "HIGH"
]

elevated_df = district_risk[
    district_risk['threat_level'] == "ELEVATED"
]

low_df = district_risk[
    district_risk['threat_level'] == "LOW"
]

st.error(
    f"🔴 Critical Districts: {', '.join(critical_df['city'].tolist())}"
)

st.warning(
    f"🟠 High Risk Districts: {', '.join(high_df['city'].tolist())}"
)

st.info(
    f"🟡 Elevated Districts: {', '.join(elevated_df['city'].tolist())}"
)

st.success(
    f"🟢 Low Risk Districts: {', '.join(low_df['city'].tolist())}"
)

# ==========================================
# THREAT ANALYTICS
# ==========================================

import plotly.express as px

st.subheader("📊 Threat Level Distribution")

fig = px.pie(
    district_risk,
    names="threat_level",
    title="Threat Level Distribution Across Districts"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# EXECUTIVE SUMMARY
# ==========================================

highest_risk = district_risk.sort_values(
    "threat_index",
    ascending=False
).iloc[0]["city"]

st.subheader("🛡️ Executive Intelligence Summary")

st.info(
    f"""
Highest Risk District: {highest_risk}

Total Districts Analysed: {len(district_risk)}

Critical Districts: {critical}

High Risk Districts: {high}

Elevated Districts: {elevated}

Low Risk Districts: {low}
"""
)

# ==========================================
# DOWNLOAD REPORT
# ==========================================

st.download_button(
    label="📥 Download Intelligence Report",
    data=district_risk.to_csv(index=False),
    file_name="trinetra_intelligence_report.csv",
    mime="text/csv"
)