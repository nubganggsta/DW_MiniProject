import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Logistic", layout="wide")

# Inject Custom CSS ปรับดีไซน์ให้ออกมาเหมือนในรูป
st.markdown("""
<style>
    /* พื้นหลังหลักโทนเทาอ่อน */
    .stApp {
        background-color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    
    /* การ์ดขอบมน สีขาว + เงา Soft Shadow */
    div[data-testid="stBlock"] {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }

    /* KPI Card โทนสีแดง/ส้ม Highlight แบบในภาพ */
    .kpi-highlight {
        background: linear-gradient(135deg, #ff4b4b 0%, #e63946 100%);
        color: white !important;
        border-radius: 14px;
        padding: 16px 20px;
    }
    .kpi-highlight .title { color: #ffe6e6; font-size: 13px; }
    .kpi-highlight .val { color: white; font-size: 26px; font-weight: bold; }

    /* KPI Card ปกติสีขาว */
    .kpi-white {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 16px 20px;
        border: 1px solid #f0f0f0;
    }
    .kpi-white .title { color: #8c8c8c; font-size: 13px; }
    .kpi-white .val { color: #1f1f1f; font-size: 26px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- Top Navigation Bar ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("Dashboard Logistic")
    st.caption("Here's analytic details for your business here")
with col_head2:
    st.button("📥 Download Report", type="primary")

# --- KPI Cards Row ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
        <div class="kpi-highlight">
            <div class="title">Total Revenue</div>
            <div class="val">$4,912.93</div>
            <small>▲ 2.5% from last month</small>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
        <div class="kpi-white">
            <div class="title">Total Shipment</div>
            <div class="val">19,329</div>
            <small style="color: #ff4b4b;">▼ 1.2% from last month</small>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
        <div class="kpi-white">
            <div class="title">Needs Filled</div>
            <div class="val">389</div>
            <small style="color: #22c55e;">▲ 4.8% from last month</small>
        </div>
    """, unsafe_allow_html=True)

# --- Chart & Map Section ---
c1, c2 = st.columns([1.5, 1])

with c1:
    st.subheader("Logistics Performance")
    # Area Chart สีส้ม/แดง แบบเติมไล่เฉด Gradient
    df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        "Revenue": [25000, 35000, 50000, 48000, 75000, 80000, 95000]
    })
    fig = px.area(df, x="Month", y="Revenue", color_discrete_sequence=["#ff4b4b"])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Geofencing Alert")
    # สามารถนำ PyDeck มาใส่แผนที่สไตล์ Light Theme ได้
    st.info("📍 Next Stop: Destination | Traffic: 42% | Distance: 120km/1h50m")