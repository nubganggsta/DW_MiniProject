import duckdb
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ==========================================
# 1. Page Config & Design System
# ==========================================
st.set_page_config(
    page_title="5G Express - Logistics Intelligence",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Unified Color Palette: 5G Express Red Executive Theme
COLOR_PRIMARY = "#DB1A1A"      # 5G Express Brand Red
COLOR_DARK_RED = "#991B1B"     # Deep Crimson Red
COLOR_ACCENT = "#DC2626"       # Bright Crimson
COLOR_LIGHT_RED = "#EF4444"    # Coral / Light Red
COLOR_SOFT_RED = "#F87171"     # Soft Red
COLOR_ROSE_TINT = "#FEE2E2"    # Pale Rose Tint
COLOR_MUTED = "#64748B"        # Slate Gray
COLOR_DARK = "#1E293B"         # Dark Slate
COLOR_BG_CARD = "#FFFFFF"

# Cohesive Palette for Pie/Donut & Categorical Charts
DONUT_PALETTE = ["#DB1A1A", "#DC2626", "#EF4444", "#F87171", "#991B1B", "#7F1D1D", "#FCA5A5", "#475569"]

# Config Font Kanit for Plotly
pio.templates.default = "plotly_white"
pio.templates["plotly_white"].layout.font.family = "Kanit, sans-serif"

# Clean, Modern CSS Injection with Glassmorphism Sidebar and Red Theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:ital,wght@0,300;0,400;0,500;0,600;0,700&display=swap');

    * {
        font-family: 'Kanit', sans-serif !important;
    }

    .stApp {
        background-color: #F8FAFC;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Header Banner styling */
    .brand-banner {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 20px 26px;
        border-radius: 14px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
        border: 1px solid #334155;
        border-left: 6px solid #DB1A1A;
    }

    .brand-title {
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #FFFFFF;
    }

    .brand-subtitle {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 400;
        margin-top: 4px;
    }

    .system-badge {
        background-color: rgba(219, 26, 26, 0.18);
        border: 1px solid #DB1A1A;
        color: #FCA5A5;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    /* Primary Red Theme KPI Cards */
    .kpi-container {
        background: linear-gradient(135deg, #DB1A1A 0%, #A31313 100%);
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid rgba(219, 26, 26, 0.25);
        box-shadow: 0 4px 14px rgba(219, 26, 26, 0.16);
        margin-bottom: 16px;
        color: #FFFFFF;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(219, 26, 26, 0.26);
    }

    .kpi-title {
        font-size: 11.5px;
        color: #FEE2E2;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .kpi-value {
        font-size: 25px;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 5px;
        margin-bottom: 3px;
        letter-spacing: -0.3px;
    }

    .kpi-sub {
        font-size: 12px;
        font-weight: 500;
    }

    /* Section Titles */
    .section-header {
        font-size: 17px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 14px;
        margin-bottom: 16px;
        border-left: 4px solid #DB1A1A;
        padding-left: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Glassmorphism Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.78) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border-right: 1px solid rgba(219, 26, 26, 0.15) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.03) !important;
    }

    /* Sidebar toggle button styling */
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarExpandButton"] {
        color: #DB1A1A !important;
    }

    .sidebar-brand-box {
        padding: 12px 6px 18px 6px;
        border-bottom: 1px solid rgba(219, 26, 26, 0.15);
        margin-bottom: 20px;
    }

    .sidebar-brand-title {
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
    }

    .sidebar-tag {
        display: inline-block;
        font-size: 11px;
        padding: 3px 9px;
        border-radius: 12px;
        background-color: #FEE2E2;
        color: #DB1A1A;
        font-weight: 600;
        margin-top: 6px;
    }

    /* Insights Box */
    .insight-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 0px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
    }
    .insight-title {
        font-size: 13px;
        font-weight: 700;
        color: #DB1A1A;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
        border-bottom: 2px solid #FEE2E2;
        padding-bottom: 6px;
    }
    .insight-item {
        display: flex;
        justify-content: space-between;
        font-size: 12.5px;
        margin-bottom: 5px;
    }
    .insight-label { color: #64748B; }
    .insight-val { font-weight: 600; color: #0F172A; }

    /* Top Page Filter Bar Card */
    .filter-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. Database Helper & Cache Engine
# ==========================================
DB_PATH = 'fiveGexpress.duckdb'

@st.cache_data(ttl=600)
def run_query(query: str) -> pd.DataFrame:
    try:
        with duckdb.connect(database=DB_PATH, read_only=True) as con:
            return con.execute(query).df()
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูลจากระบบ: {e}")
        return pd.DataFrame()

# UI Component Helpers
def render_kpi(title: str, value: str, subtext: str = "", status: str = "neutral"):
    """
    status: 'good', 'risk', 'neutral'
    Red Theme Primary KPI Container with elegant gradient and high contrast
    """
    sub_color = {
        "good": "#FEF08A",     # Warm soft gold
        "risk": "#FECACA",     # Soft light red
        "neutral": "#F1F5F9"   # Soft cloud white/gray
    }.get(status, "#F1F5F9")

    html = (
        f'<div class="kpi-container">'
        f'<div class="kpi-title">{title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub" style="color: {sub_color};">{subtext}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_section_title(title: str):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def render_summary_box(title: str, items: list):
    rows = "".join([
        f'<div class="insight-item"><span class="insight-label">{label}</span><span class="insight-val">{val}</span></div>'
        for label, val in items
    ])
    html = (
        f'<div class="insight-card">'
        f'<div class="insight-title">{title}</div>'
        f'{rows}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def style_chart(fig, height: int = 340):
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(family="Kanit, sans-serif", size=12, color="#1E293B"),
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False)
    )
    return fig

def create_donut_chart(df: pd.DataFrame, names: str, values: str, title: str = "", color_map: dict = None, height: int = 280):
    """
    สร้างกราฟโดนัทสะอาดตาม Requirement:
    1. ไม่มีข้อความ/ตัวเลขทับในโดนัท (textinfo='none')
    2. ไม่มีข้อความตรงกลาง Donut Chart (ตรงกลางว่าง)
    3. ไม่มี Label รอบ ๆ Slice โดยตรง รายละเอียดแสดงในกล่องข้อความสรุปด้านข้าง
    """
    if color_map:
        fig = px.pie(df, names=names, values=values, hole=0.62, color=names, color_discrete_map=color_map)
    else:
        fig = px.pie(df, names=names, values=values, hole=0.62, color_discrete_sequence=DONUT_PALETTE)

    fig.update_traces(
        textinfo='none',             # ห้ามแสดงข้อความ/เปอร์เซ็นต์ด้านในหรือรอบ ๆ โดนัท
        hoverinfo='label+percent+value',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig.update_layout(
        template="plotly_white",
        height=height,
        showlegend=False,            # ซ่อน default legend เพื่อใช้ข้อมูลสรุปด้านข้าง
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Kanit, sans-serif"),
        annotations=[]               # มั่นใจว่าตรงกลาง Donut Chart ว่าง ไม่มีข้อความใด ๆ
    )
    return fig

def render_donut_summary(df: pd.DataFrame, names: str, values: str, title: str, color_map: dict = None, unit: str = "ครั้ง", suffix_text: str = "ของทั้งหมด", is_currency: bool = False):
    """
    แสดงกล่องข้อความสรุปด้านข้าง Donut Chart อย่างถูกต้อง:
    - HTML Render สมบูรณ์ ไม่แสดง code ออกมาเป็น Plain Text
    - ไม่มี <div>, <span> หรือ tag หลุดออกมา
    - สีของจุด/สัญลักษณ์และเปอร์เซ็นต์ตรงกับสีของ Slice ใน Donut Chart
    - ข้อมูล Dynamic คำนวณจาก Query/DataFrame จริง
    """
    if df.empty:
        return
    
    total = df[values].sum()
    items_html = []
    
    for i, (_, row) in enumerate(df.iterrows()):
        cat_name = str(row[names])
        val = row[values]
        pct = (val / total * 100) if total > 0 else 0.0
        
        # สีตรงกับ Slice ใน Donut Chart
        if color_map and cat_name in color_map:
            dot_color = color_map[cat_name]
        else:
            dot_color = DONUT_PALETTE[i % len(DONUT_PALETTE)]
            
        val_str = f"${val:,.2f}" if is_currency else f"{val:,.0f} {unit}".strip()
        sub_desc = f"{pct:.1f}% {suffix_text}" if suffix_text else f"{pct:.1f}%"
        
        # ประกอบ HTML แบบไร้ leading indentation เพื่อป้องกัน Markdown แปลงเป็น Code Block
        item_html = (
            f'<div style="margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px dashed #F1F5F9;">'
            f'<div style="display: flex; align-items: center; gap: 8px; font-size: 13.5px; font-weight: 700; color: #1E293B;">'
            f'<span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: {dot_color}; flex-shrink: 0;"></span>'
            f'<span>{cat_name}</span>'
            f'</div>'
            f'<div style="margin-left: 18px; font-size: 13px; color: #475569; margin-top: 2px;">'
            f'{val_str}'
            f'</div>'
            f'<div style="margin-left: 18px; font-size: 12px; font-weight: 600; color: {dot_color};">'
            f'{sub_desc}'
            f'</div>'
            f'</div>'
        )
        items_html.append(item_html)
        
    card_html = (
        f'<div class="insight-card">'
        f'<div class="insight-title">{title}</div>'
        f'{"".join(items_html)}'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

def render_donut_legend(df: pd.DataFrame, names: str, values: str, color_map: dict = None, unit: str = "", is_currency: bool = False):
    """
    คงฟังก์ชันเดิมไว้เพื่อความเข้ากันได้ และแก้ไขไม่ให้มี whitespace เยื้องเพื่อป้องกัน Markdown Code Block
    """
    if df.empty:
        return
    total = df[values].sum()
    items_html = []
    for i, (_, row) in enumerate(df.iterrows()):
        cat_name = str(row[names])
        val = row[values]
        pct = (val / total * 100) if total > 0 else 0.0
        if color_map and cat_name in color_map:
            dot_color = color_map[cat_name]
        else:
            dot_color = DONUT_PALETTE[i % len(DONUT_PALETTE)]
        val_str = f"${val:,.2f}" if is_currency else f"{val:,.0f} {unit}".strip()
        item = (
            f'<div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed #F1F5F9; font-size: 13px;">'
            f'<div style="display: flex; align-items: center; gap: 8px;">'
            f'<span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: {dot_color}; flex-shrink: 0;"></span>'
            f'<span style="font-weight: 500; color: #1E293B;">{cat_name}</span>'
            f'</div>'
            f'<div style="text-align: right;">'
            f'<span style="font-weight: 700; color: {dot_color};">{pct:.1f}%</span>'
            f'<span style="color: #64748B; font-size: 11.5px; margin-left: 6px;">({val_str})</span>'
            f'</div>'
            f'</div>'
        )
        items_html.append(item)
    legend_html = f'<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px 16px; margin-top: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">{"".join(items_html)}</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

def render_top_filters(page_prefix: str, show_facility: bool = False):
    """
    Global Filter Engine วางไว้ด้านบนของแต่ละหน้า Dashboard:
    [ Year ] [ Time Granularity: Year, Quarter, Month, Week, Day ] [ Branch / Facility (optional) ]
    """
    df_years = run_query("SELECT DISTINCT year FROM dim_date ORDER BY year DESC")
    available_years = ["ภาพรวมทั้งหมด (All)"] + (df_years['year'].astype(str).tolist() if not df_years.empty else [])
    
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    if show_facility:
        col_f1, col_f2, col_f3 = st.columns([1.2, 1.5, 2])
    else:
        col_f1, col_f2, _ = st.columns([1.5, 1.8, 2.5])
    
    with col_f1:
        selected_year = st.selectbox(
            "📅 เลือกปี (Year):",
            available_years,
            key=f"{page_prefix}_year"
        )
        
    with col_f2:
        trend_axis = st.selectbox(
            "⏱️ แสดงแกนเวลาตาม (Trend Granularity):",
            ["ไตรมาส (Quarter)", "เดือน (Month)", "สัปดาห์ (Week)", "วัน (Day)", "ปี (Year)"],
            key=f"{page_prefix}_axis"
        )
        
    selected_facility = "ทุกสาขา/ศูนย์กระจายสินค้า (All)"
    if show_facility:
        df_facilities = run_query("SELECT facility_name FROM dim_facilities ORDER BY facility_name")
        facility_list = ["ทุกสาขา/ศูนย์กระจายสินค้า (All)"] + (df_facilities['facility_name'].tolist() if not df_facilities.empty else [])
        with col_f3:
            selected_facility = st.selectbox(
                "🏢 สาขา/ศูนย์กระจายสินค้า (Facility):",
                facility_list,
                key=f"{page_prefix}_facility"
            )
    st.markdown('</div>', unsafe_allow_html=True)

    # Build SQL WHERE Clause
    where_conds = []
    if selected_year != "ภาพรวมทั้งหมด (All)":
        where_conds.append(f"d.year = {selected_year}")
        
    if show_facility and selected_facility != "ทุกสาขา/ศูนย์กระจายสินค้า (All)":
        fac_safe = selected_facility.replace("'", "''")
        where_conds.append(f"f.facility_name = '{fac_safe}'")
        
    WHERE_SQL = "WHERE " + " AND ".join(where_conds) if where_conds else ""
    
    # Time Granularity Expression for DuckDB
    if trend_axis == "วัน (Day)":
        time_expr = "strftime(d.full_date, '%Y-%m-%d')"
        group_expr = "strftime(d.full_date, '%Y-%m-%d')"
    elif trend_axis == "สัปดาห์ (Week)":
        time_expr = "strftime(d.full_date, '%Y-W%W')"
        group_expr = "strftime(d.full_date, '%Y-W%W')"
    elif trend_axis == "เดือน (Month)":
        time_expr = "CAST(d.year AS VARCHAR) || '-' || LPAD(CAST(d.month AS VARCHAR), 2, '0')"
        group_expr = "d.year, d.month"
    elif trend_axis == "ไตรมาส (Quarter)":
        time_expr = "'Q' || CAST(d.quarter AS VARCHAR) || '-' || CAST(d.year AS VARCHAR)"
        group_expr = "d.year, d.quarter"
    else:  # "ปี (Year)"
        time_expr = "CAST(d.year AS VARCHAR)"
        group_expr = "d.year"
        
    return selected_year, trend_axis, selected_facility, WHERE_SQL, time_expr, group_expr

# ==========================================
# 3. Glassmorphism Sidebar: Navigation Only
# ==========================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-title">🚛 5G Express Console</div>
            <span class="sidebar-tag">● ระบบเชื่อมต่อเรียบร้อย</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "หมวดหมู่การวิเคราะห์:",
        [
            "📊 ภาพรวมรายได้และลูกค้า",
            "🚚 การจัดส่งและประสิทธิภาพ",
            "🛠️ การซ่อมบำรุงยานพาหนะ",
            "⛽ เชื้อเพลิงและความปลอดภัย"
        ],
        index=0
    )

    st.markdown("---")
    st.caption("คลังข้อมูลโลจิสติกส์ v3.0 • DuckDB Analytics Engine")

# Banner Header
st.markdown(
    """
    <div class="brand-banner">
        <div>
            <div class="brand-title">5G EXPRESS LOGISTICS INTELLIGENCE</div>
            <div class="brand-subtitle">แดชบอร์ดบริหารจัดการปฏิบัติการขนส่ง • ข้อมูลเชื่อมต่อ DuckDB Data Warehouse</div>
        </div>
        <div class="system-badge">Executive Edition</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 4. Analytics Pages
# ==========================================

# -----------------------------------------------------------------------------
# หน้า 1: ภาพรวมรายได้และลูกค้า
# -----------------------------------------------------------------------------
if page == "📊 ภาพรวมรายได้และลูกค้า":
    render_section_title("ภาพรวมสถานะการเงินและพอร์ตลูกค้า (Financial & Customer Overview)")

    # 1. Global Filter Bar (Top of page)
    selected_year, trend_axis, _, WHERE_SQL, time_expr, group_expr = render_top_filters("page1", show_facility=False)

    # 2. Data Queries
    df_rev_trend = run_query(f"""
        SELECT
            {time_expr} AS time_axis,
            SUM(t.revenue) AS total_revenue,
            COUNT(t.trip_key) AS total_trips
        FROM fact_trips_operations t
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY {group_expr}
        ORDER BY {group_expr}
    """)

    df_trailer = run_query(f"""
        SELECT 
            tr.trailer_type,
            SUM(t.revenue) AS total_revenue,
            COUNT(t.trip_key) AS total_trips,
            AVG(t.revenue) AS avg_revenue_per_trip
        FROM fact_trips_operations t
        JOIN dim_trailers tr ON t.trailer_key = tr.trailer_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1
        ORDER BY total_revenue DESC
    """)

    # Top Customers: Ranked by Revenue Efficiency (Revenue per Trip)
    df_top_customers = run_query(f"""
        SELECT
            c.customer_name AS "ชื่อลูกค้า",
            c.primary_freight_type AS "ประเภทสินค้าหลัก",
            COUNT(t.trip_key) AS "จำนวนเที่ยว (Trips)",
            SUM(t.revenue) AS "รายได้รวม (USD)",
            SUM(t.revenue) / COUNT(t.trip_key) AS "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)"
        FROM fact_trips_operations t
        JOIN dim_customers c ON t.customer_key = c.customer_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1, 2
        ORDER BY "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)" DESC
        LIMIT 10
    """)

    if df_rev_trend.empty:
        st.warning("ไม่พบข้อมูลสำหรับการกรองที่เลือก")
    else:
        tot_rev = df_rev_trend['total_revenue'].sum()
        tot_trips = df_rev_trend['total_trips'].sum()
        avg_rev = tot_rev / tot_trips if tot_trips > 0 else 0
        peak_row = df_rev_trend.iloc[df_rev_trend['total_revenue'].idxmax()]

        # 3. Top KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi("รายได้รวมสะสม", f"${tot_rev:,.2f}", "Total Cumulative Revenue", "good")
        with k2:
            render_kpi("เที่ยวจัดส่งทั้งหมด", f"{tot_trips:,.0f} เที่ยว", "Total Completed Trips", "neutral")
        with k3:
            render_kpi("รายได้เฉลี่ยต่อเที่ยว", f"${avg_rev:,.2f}", "Avg Revenue / Trip", "good")
        with k4:
            render_kpi("ช่วงที่รายได้สูงสุด", f"{peak_row['time_axis']}", f"${peak_row['total_revenue']:,.0f}", "neutral")

        # 4. Revenue Trend (Top Chart)
        st.markdown(f"##### 📈 แนวโน้มรายได้ (Revenue Trend - {trend_axis.split(' ')[0]})")
        fig_rev = px.area(
            df_rev_trend, x='time_axis', y='total_revenue',
            color_discrete_sequence=['#DB1A1A'], markers=True
        )
        fig_rev.update_traces(fillcolor='rgba(219, 26, 26, 0.08)', line=dict(width=3, color='#DB1A1A'))
        fig_rev.update_layout(xaxis_title="", yaxis_title="รายได้ (USD)", yaxis=dict(tickformat="$,.0f"))
        st.plotly_chart(style_chart(fig_rev, height=320), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 5. Revenue Distribution + Insight (Donut on Left, Summary on Right)
        st.markdown("##### 🍩 สัดส่วนรายได้แยกตามประเภทตู้ขนส่ง (Revenue by Trailer Type)")
        col_donut_chart, col_donut_insight = st.columns([1, 1])

        with col_donut_chart:
            if not df_trailer.empty:
                fig_trailer = create_donut_chart(df_trailer, names='trailer_type', values='total_revenue')
                st.plotly_chart(fig_trailer, use_container_width=True)

        with col_donut_insight:
            if not df_trailer.empty:
                render_donut_summary(
                    df_trailer,
                    names='trailer_type',
                    values='total_revenue',
                    title="สรุปสัดส่วนรายได้แยกตามประเภทตู้ขนส่ง",
                    unit="USD",
                    suffix_text="ของรายได้ทั้งหมด",
                    is_currency=True
                )

        st.markdown("---")

        # 6. Top 10 Customers (Ranking Chart on Top + Data Table Below)
        render_section_title("🏆 10 อันดับลูกค้าที่มีประสิทธิภาพรายได้สูงสุด (Top Customers by Revenue Efficiency: Revenue / Trip)")

        if not df_top_customers.empty:
            df_top_customers["สัดส่วนรายได้ (Revenue Share %)"] = (df_top_customers["รายได้รวม (USD)"] / tot_rev * 100)

            # Chart (Top): Ranked by Revenue per Trip (Efficiency)
            df_c_sort = df_top_customers.sort_values(by="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)", ascending=True)
            fig_top_c = px.bar(
                df_c_sort,
                y="ชื่อลูกค้า",
                x="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                orientation='h',
                color="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                color_continuous_scale=[[0, '#FCA5A5'], [1, '#B91C1C']],
                text_auto='$,.0f',
                hover_data=["จำนวนเที่ยว (Trips)", "รายได้รวม (USD)", "สัดส่วนรายได้ (Revenue Share %)"]
            )
            fig_top_c.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)")
            st.plotly_chart(style_chart(fig_top_c, height=290), use_container_width=True)

            # Data Table (Below)
            df_display = df_top_customers.copy()
            df_display.insert(0, 'อันดับ', [f"#{i+1}" for i in range(len(df_display))])

            st.dataframe(
                df_display.style.format({
                    "จำนวนเที่ยว (Trips)": "{:,.0f} เที่ยว",
                    "รายได้รวม (USD)": "${:,.2f}",
                    "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)": "${:,.2f}",
                    "สัดส่วนรายได้ (Revenue Share %)": "{:.2f}%"
                }),
                use_container_width=True,
                hide_index=True
            )


# -----------------------------------------------------------------------------
# หน้า 2: การจัดส่งและประสิทธิภาพ
# -----------------------------------------------------------------------------
elif page == "🚚 การจัดส่งและประสิทธิภาพ":
    render_section_title("ประสิทธิภาพการส่งมอบและพนักงานขับรถ (Delivery & Fleet Performance)")

    # 1. Global Filter Bar with Facility Filter
    selected_year, trend_axis, selected_facility, WHERE_SQL, time_expr, group_expr = render_top_filters("page2", show_facility=True)

    # 2. On-Time Query (Filtered by Facility & Date)
    df_ontime = run_query(f"""
        SELECT
            CASE WHEN t.on_time_flag THEN 'ตรงเวลา (On-Time)' ELSE 'ล่าช้า (Delayed)' END AS status,
            COUNT(*) AS count
        FROM fact_trips_operations t
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1
    """)

    # 3. Normalized Bottleneck Query: Total Waiting, Trips, Avg Wait, Wait per Trip, Share %
    df_bottleneck = run_query(f"""
        SELECT
            f.facility_name AS "จุดกระจายสินค้า / คลัง",
            SUM(t.detention_minutes) AS "เวลารอรวม (นาที)",
            COUNT(t.trip_key) AS "เที่ยวที่เข้าใช้บริการ",
            AVG(t.detention_minutes) AS "เวลารอเฉลี่ย (นาที)",
            SUM(t.detention_minutes) / COUNT(t.trip_key) AS "เวลารอต่อเที่ยว (นาที/Trip)"
        FROM fact_trips_operations t
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1
        ORDER BY "เวลารอรวม (นาที)" DESC
        LIMIT 5
    """)

    # 4. Driver Performance Query: Ranked by Revenue Efficiency (Revenue / Trip)
    df_drivers = run_query(f"""
        SELECT
            dr.first_name || ' ' || dr.last_name AS "พนักงานขับรถ",
            COUNT(t.trip_key) AS "จำนวนเที่ยววิ่ง (Trips)",
            SUM(t.revenue) AS "รายได้ที่สร้าง (USD)",
            SUM(t.revenue) / COUNT(t.trip_key) AS "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)"
        FROM fact_trips_operations t
        JOIN dim_drivers dr ON t.driver_key = dr.driver_key
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1
        ORDER BY "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)" DESC
        LIMIT 10
    """)

    if df_ontime.empty:
        st.warning("ไม่พบข้อมูลสำหรับการจัดส่งในช่วงเวลาหรือสาขาที่เลือก")
    else:
        tot_shipments = df_ontime['count'].sum()
        ontime_row = df_ontime[df_ontime['status'].str.contains('On-Time')]
        ontime_qty = ontime_row['count'].sum() if not ontime_row.empty else 0
        delayed_qty = tot_shipments - ontime_qty
        ontime_rate = (ontime_qty / tot_shipments * 100) if tot_shipments > 0 else 0
        delay_rate = 100.0 - ontime_rate

        worst_fc = df_bottleneck.iloc[0]['จุดกระจายสินค้า / คลัง'] if not df_bottleneck.empty else "ไม่มีข้อมูล"
        worst_wait = df_bottleneck.iloc[0]['เวลารอต่อเที่ยว (นาที/Trip)'] if not df_bottleneck.empty else 0

        # Top KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi("เที่ยวจัดส่งทั้งหมด", f"{tot_shipments:,.0f} เที่ยว", f"สาขา: {selected_facility.split('/')[0]}", "neutral")
        with k2:
            render_kpi("อัตราส่งตรงเวลา (On-Time)", f"{ontime_rate:.1f}%", f"{ontime_qty:,.0f} เที่ยวตรงเวลา", "good" if ontime_rate >= 90 else "risk")
        with k3:
            render_kpi("อัตราส่งล่าช้า (Delayed)", f"{delay_rate:.1f}%", f"{delayed_qty:,.0f} เที่ยวติดปัญหา", "risk" if delay_rate > 10 else "good")
        with k4:
            render_kpi("เวลารอคอยเฉลี่ยสูงสุด", f"{worst_wait:.1f} นาที/Trip", f"{str(worst_fc)[:22]}", "risk")

        # Row: On-Time Donut (Left) + Summary/Bottleneck (Right)
        col_sla, col_bottle = st.columns([1, 1.2])

        with col_sla:
            st.markdown(f"##### 🍩 สัดส่วนความตรงเวลา (On-Time Delivery Share)")
            sla_colors = {'ตรงเวลา (On-Time)': '#1E293B', 'ล่าช้า (Delayed)': '#DB1A1A'}
            fig_sla = create_donut_chart(df_ontime, names='status', values='count', color_map=sla_colors)
            st.plotly_chart(fig_sla, use_container_width=True)

            render_donut_summary(
                df_ontime,
                names='status',
                values='count',
                title=f"สรุปความตรงเวลา (สาขา: {selected_facility.split('/')[0]})",
                color_map=sla_colors,
                unit="เที่ยว",
                suffix_text="ของการจัดส่งทั้งหมด"
            )

        with col_bottle:
            st.markdown("##### 🛑 จุดกระจายสินค้าที่มีเวลารอคอยสูงสุด (Bottleneck Ranking)")
            if not df_bottleneck.empty:
                tot_waiting_all = df_bottleneck["เวลารอรวม (นาที)"].sum()
                df_bottleneck["สัดส่วนเวลารอ (Wait Share %)"] = (df_bottleneck["เวลารอรวม (นาที)"] / tot_waiting_all * 100) if tot_waiting_all > 0 else 0

                # Chart (Top)
                df_b_sort = df_bottleneck.sort_values(by="เวลารอต่อเที่ยว (นาที/Trip)", ascending=True)
                fig_bot = px.bar(
                    df_b_sort,
                    y="จุดกระจายสินค้า / คลัง",
                    x="เวลารอต่อเที่ยว (นาที/Trip)",
                    orientation='h',
                    color="เวลารอต่อเที่ยว (นาที/Trip)",
                    color_continuous_scale=[[0, '#FCA5A5'], [1, '#991B1B']],
                    text_auto='.1f'
                )
                fig_bot.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="เวลารอต่อเที่ยว (นาที/Trip)")
                st.plotly_chart(style_chart(fig_bot, height=220), use_container_width=True)

                # Table (Below)
                st.dataframe(
                    df_bottleneck.style.format({
                        "เวลารอรวม (นาที)": "{:,.0f} นาที",
                        "เที่ยวที่เข้าใช้บริการ": "{:,.0f}",
                        "เวลารอเฉลี่ย (นาที)": "{:.1f} นาที",
                        "เวลารอต่อเที่ยว (นาที/Trip)": "{:.1f} นาที",
                        "สัดส่วนเวลารอ (Wait Share %)": "{:.1f}%"
                    }),
                    use_container_width=True,
                    hide_index=True
                )

        st.markdown("---")

        # Driver Performance (Chart on Top + Table Below)
        render_section_title("🌟 10 อันดับพนักงานขับรถที่มีประสิทธิภาพรายได้สูงสุด (Top Drivers by Revenue Efficiency)")
        if not df_drivers.empty:
            tot_driver_rev = df_drivers["รายได้ที่สร้าง (USD)"].sum()
            df_drivers["สัดส่วนรายได้ (Revenue Share %)"] = (df_drivers["รายได้ที่สร้าง (USD)"] / tot_driver_rev * 100) if tot_driver_rev > 0 else 0

            # Chart (Top): Ranked by Revenue Efficiency
            df_d_chart = df_drivers.sort_values(by="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)", ascending=True)
            fig_dr = px.bar(
                df_d_chart,
                y="พนักงานขับรถ",
                x="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                orientation='h',
                color="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                color_continuous_scale=[[0, '#FCA5A5'], [1, '#B91C1C']],
                text_auto='$,.0f',
                hover_data=["จำนวนเที่ยววิ่ง (Trips)", "รายได้ที่สร้าง (USD)", "สัดส่วนรายได้ (Revenue Share %)"]
            )
            fig_dr.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)")
            st.plotly_chart(style_chart(fig_dr, height=280), use_container_width=True)

            # Table (Below)
            df_d_display = df_drivers.copy()
            df_d_display.insert(0, 'อันดับ', [f"#{i+1}" for i in range(len(df_d_display))])

            st.dataframe(
                df_d_display.style.format({
                    "จำนวนเที่ยววิ่ง (Trips)": "{:,.0f} เที่ยว",
                    "รายได้ที่สร้าง (USD)": "${:,.2f}",
                    "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)": "${:,.2f}",
                    "สัดส่วนรายได้ (Revenue Share %)": "{:.2f}%"
                }),
                use_container_width=True,
                hide_index=True
            )


# -----------------------------------------------------------------------------
# หน้า 3: การซ่อมบำรุงยานพาหนะ
# -----------------------------------------------------------------------------
elif page == "🛠️ การซ่อมบำรุงยานพาหนะ":
    render_section_title("การซ่อมบำรุงและสมรรถนะของฝูงรถ (Maintenance & Fleet Health)")

    # 1. Global Filter Bar
    selected_year, trend_axis, _, WHERE_SQL, time_expr, group_expr = render_top_filters("page3", show_facility=False)

    # 2. Queries
    df_maint_trend = run_query(f"""
        SELECT
            {time_expr} AS time_axis,
            SUM(m.maintenance_cost) AS total_cost,
            SUM(m.downtime_hours) AS total_downtime,
            COUNT(m.maintenance_key) AS maint_count
        FROM fact_maintenance m
        JOIN dim_date d ON m.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY {group_expr}
        ORDER BY {group_expr}
    """)

    df_mtype = run_query(f"""
        SELECT
            m.maintenance_type,
            COUNT(*) AS job_count,
            SUM(m.maintenance_cost) AS total_cost
        FROM fact_maintenance m
        JOIN dim_date d ON m.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1
        ORDER BY job_count DESC
    """)

    # Multi-dimensional Brand Maintenance Query: Frequency, Cost, Downtime
    df_truck_brands = run_query(f"""
        SELECT
            tr.make AS "ยี่ห้อรถ (Make)",
            COUNT(m.maintenance_key) AS "ความถี่ในการซ่อม (Job Count)",
            SUM(m.maintenance_cost) AS "ค่าใช้จ่ายรวม (USD)",
            ROUND(AVG(m.maintenance_cost), 2) AS "ค่าซ่อมเฉลี่ย/ครั้ง (USD)",
            SUM(m.downtime_hours) AS "เวลาจอดเสียรวม (ชม.)",
            ROUND(AVG(m.downtime_hours), 2) AS "เวลาจอดเสียเฉลี่ย/ครั้ง (ชม.)"
        FROM fact_maintenance m
        JOIN dim_trucks tr ON m.truck_key = tr.truck_key
        JOIN dim_date d ON m.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1
        ORDER BY "ค่าใช้จ่ายรวม (USD)" DESC
    """)

    if df_maint_trend.empty:
        st.warning("ไม่พบข้อมูลการซ่อมบำรุงสำหรับเงื่อนไขที่เลือก")
    else:
        tot_m_cost = df_maint_trend['total_cost'].sum()
        tot_down = df_maint_trend['total_downtime'].sum()
        tot_jobs = df_maint_trend['maint_count'].sum()
        avg_job_cost = tot_m_cost / tot_jobs if tot_jobs > 0 else 0

        # Top KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi("ค่าซ่อมบำรุงรวม", f"${tot_m_cost:,.2f}", "Total Maintenance Cost", "risk")
        with k2:
            render_kpi("เวลาหยุดจอดเสียรวม", f"{tot_down:,.1f} ชม.", "Fleet Downtime", "risk")
        with k3:
            render_kpi("จำนวนงานซ่อมทั้งหมด", f"{tot_jobs:,.0f} ครั้ง", "Total Service Events", "neutral")
        with k4:
            render_kpi("ค่าซ่อมเฉลี่ย/งาน", f"${avg_job_cost:,.2f}", "Avg Cost / Service", "neutral")

        # 3. Maintenance Cost Trend (Top Chart)
        st.markdown(f"##### 📈 แนวโน้มค่าใช้จ่ายซ่อมบำรุง (Maintenance Cost Trend - {trend_axis.split(' ')[0]})")
        fig_m = px.line(
            df_maint_trend, x='time_axis', y='total_cost',
            markers=True, color_discrete_sequence=['#DB1A1A']
        )
        fig_m.update_traces(line=dict(width=3, color='#DB1A1A'), marker=dict(size=7, color='#991B1B'))
        fig_m.update_layout(xaxis_title="", yaxis_title="ค่าซ่อม (USD)", yaxis=dict(tickformat="$,.0f"))
        st.plotly_chart(style_chart(fig_m, height=310), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. Maintenance Type Distribution + Insight (Donut on Left, Summary on Right)
        st.markdown("##### 🍩 สัดส่วนประเภทงานซ่อมบำรุง (Maintenance Type Distribution)")
        col_m_donut, col_m_insight = st.columns([1, 1])

        with col_m_donut:
            if not df_mtype.empty:
                fig_type = create_donut_chart(df_mtype, names='maintenance_type', values='job_count')
                st.plotly_chart(fig_type, use_container_width=True)

        with col_m_insight:
            if not df_mtype.empty:
                render_donut_summary(
                    df_mtype,
                    names='maintenance_type',
                    values='job_count',
                    title="สรุปสัดส่วนประเภทงานซ่อมบำรุง",
                    unit="งาน",
                    suffix_text="ของงานซ่อมทั้งหมด"
                )

        st.markdown("---")

        # 5. Ranking by Truck Brand (Chart on Top + Table Below)
        render_section_title("🚛 อันดับค่าใช้จ่ายและความถี่ในการซ่อมบำรุงแยกตามยี่ห้อรถ (Truck Make Analysis)")
        if not df_truck_brands.empty:
            df_b_sort = df_truck_brands.sort_values(by="ค่าใช้จ่ายรวม (USD)", ascending=True)
            fig_brand = px.bar(
                df_b_sort,
                y="ยี่ห้อรถ (Make)",
                x="ค่าใช้จ่ายรวม (USD)",
                orientation='h',
                color="ค่าใช้จ่ายรวม (USD)",
                color_continuous_scale=[[0, '#FCA5A5'], [1, '#991B1B']],
                text_auto='$,.0f',
                hover_data=["ความถี่ในการซ่อม (Job Count)", "ค่าซ่อมเฉลี่ย/ครั้ง (USD)", "เวลาจอดเสียรวม (ชม.)"]
            )
            fig_brand.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="ค่าใช้จ่ายซ่อมรวม (USD)")
            st.plotly_chart(style_chart(fig_brand, height=230), use_container_width=True)

            df_tb_display = df_truck_brands.copy()
            df_tb_display.insert(0, 'อันดับ', [f"#{i+1}" for i in range(len(df_tb_display))])

            st.dataframe(
                df_tb_display.style.format({
                    "ความถี่ในการซ่อม (Job Count)": "{:,.0f} ครั้ง",
                    "ค่าใช้จ่ายรวม (USD)": "${:,.2f}",
                    "ค่าซ่อมเฉลี่ย/ครั้ง (USD)": "${:,.2f}",
                    "เวลาจอดเสียรวม (ชม.)": "{:,.1f} ชม.",
                    "เวลาจอดเสียเฉลี่ย/ครั้ง (ชม.)": "{:,.2f} ชม."
                }),
                use_container_width=True,
                hide_index=True
            )


# -----------------------------------------------------------------------------
# หน้า 4: เชื้อเพลิงและความปลอดภัย
# -----------------------------------------------------------------------------
elif page == "⛽ เชื้อเพลิงและความปลอดภัย":
    render_section_title("การบริหารต้นทุนเชื้อเพลิงและสถิติความปลอดภัย (Fuel & Operational Safety)")

    # 1. Global Filter Bar
    selected_year, trend_axis, _, WHERE_SQL, time_expr, group_expr = render_top_filters("page4", show_facility=False)

    # 2. Optimized Fuel Queries (Avoiding Cartesian Join)
    df_fuel_totals = run_query(f"""
        SELECT
            SUM(f.fuel_cost) AS total_fuel_cost,
            SUM(f.gallons) AS total_gallons
        FROM fact_fuel_purchases f
        JOIN dim_date d ON f.date_key = d.date_key
        {WHERE_SQL}
    """)

    df_trip_stats = run_query(f"""
        SELECT
            COUNT(t.trip_key) AS total_trips,
            SUM(t.fuel_gallons_used) AS trip_gallons_used
        FROM fact_trips_operations t
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
    """)

    df_fuel_trend = run_query(f"""
        SELECT
            {time_expr} AS time_axis,
            SUM(f.fuel_cost) AS total_fuel_cost,
            SUM(f.gallons) AS total_gallons
        FROM fact_fuel_purchases f
        JOIN dim_date d ON f.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY {group_expr}
        ORDER BY {group_expr}
    """)

    # Safety Incidents Query
    df_incident_pie = run_query(f"""
        SELECT
            s.incident_type,
            COUNT(*) AS count
        FROM fact_safety_incidents s
        JOIN dim_date d ON s.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1
        ORDER BY count DESC
    """)

    if df_fuel_totals.empty or df_fuel_totals.iloc[0]['total_fuel_cost'] is None:
        st.warning("ไม่พบข้อมูลเชื้อเพลิงและความปลอดภัยสำหรับเงื่อนไขที่เลือก")
    else:
        tot_fuel_cost = df_fuel_totals.iloc[0]['total_fuel_cost'] or 0
        tot_gallons = df_fuel_totals.iloc[0]['total_gallons'] or 0
        tot_trips = df_trip_stats.iloc[0]['total_trips'] if not df_trip_stats.empty else 0
        
        # Metric Requirement: Fuel Cost / Trip = Total Fuel Cost / Completed Trips
        cost_per_trip = tot_fuel_cost / tot_trips if tot_trips > 0 else 0
        avg_fuel_price = tot_fuel_cost / tot_gallons if tot_gallons > 0 else 0
        total_incidents = df_incident_pie['count'].sum() if not df_incident_pie.empty else 0

        # Route Fuel Cost Calculation using average price per gallon
        df_fuel_route = run_query(f"""
            SELECT
                r.origin_city || ' -> ' || r.destination_city AS "เส้นทาง (Route)",
                COUNT(t.trip_key) AS "จำนวนเที่ยว (Trips)",
                AVG(t.fuel_gallons_used) AS "การใช้น้ำมันเฉลี่ย/เที่ยว (Gallons)",
                SUM(t.fuel_gallons_used) AS "การใช้น้ำมันรวม (Gallons)",
                (AVG(t.fuel_gallons_used) * {avg_fuel_price}) AS "ต้นทุนน้ำมันเฉลี่ย/เที่ยว (USD/Trip)",
                (SUM(t.fuel_gallons_used) * {avg_fuel_price}) AS "ต้นทุนน้ำมันรวมโดยประมาณ (USD)"
            FROM fact_trips_operations t
            JOIN dim_routes r ON t.route_key = r.route_key
            JOIN dim_date d ON t.date_key = d.date_key
            {WHERE_SQL}
            GROUP BY 1
            ORDER BY "ต้นทุนน้ำมันเฉลี่ย/เที่ยว (USD/Trip)" DESC
            LIMIT 5
        """)

        # Dangerous Routes Query
        df_danger_route = run_query(f"""
            SELECT
                r.origin_city || ' -> ' || r.destination_city AS "เส้นทางเสี่ยง (Route)",
                COUNT(s.incident_key) AS "จำนวนอุบัติเหตุ (ครั้ง)"
            FROM fact_safety_incidents s
            JOIN dim_routes r ON s.route_key = r.route_key
            JOIN dim_date d ON s.date_key = d.date_key
            {WHERE_SQL}
            GROUP BY 1
            ORDER BY "จำนวนอุบัติเหตุ (ครั้ง)" DESC
            LIMIT 5
        """)

        # Top KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi("ต้นทุนค่าน้ำมันรวม", f"${tot_fuel_cost:,.2f}", "Total Fuel Purchased", "neutral")
        with k2:
            render_kpi("ต้นทุนน้ำมันเฉลี่ย/เที่ยว", f"${cost_per_trip:,.2f}", "Fuel Cost / Completed Trip", "good")
        with k3:
            render_kpi("ปริมาณน้ำมันรวม", f"{tot_gallons:,.0f} gal", f"เฉลี่ย ${avg_fuel_price:.2f} / gal", "neutral")
        with k4:
            render_kpi("อุบัติเหตุและเหตุการณ์เสี่ยง", f"{total_incidents:,.0f} ครั้ง", "Safety Incidents", "risk" if total_incidents > 0 else "good")

        # 3. Fuel Cost Trend (Top Chart)
        st.markdown(f"##### 📈 แนวโน้มต้นทุนเชื้อเพลิง (Fuel Cost Trend - {trend_axis.split(' ')[0]})")
        fig_ftrend = px.line(
            df_fuel_trend, x='time_axis', y='total_fuel_cost',
            markers=True, color_discrete_sequence=['#DB1A1A']
        )
        fig_ftrend.update_traces(line=dict(width=3, color='#DB1A1A'), marker=dict(size=7, color='#991B1B'))
        fig_ftrend.update_layout(xaxis_title="", yaxis_title="ค่าน้ำมัน (USD)", yaxis=dict(tickformat="$,.0f"))
        st.plotly_chart(style_chart(fig_ftrend, height=310), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. Incident Distribution + Insight (Donut on Left, Summary on Right)
        st.markdown("##### 🍩 สัดส่วนประเภทอุบัติเหตุและความเสี่ยง (Incident Type Distribution)")
        col_inc_donut, col_inc_insight = st.columns([1, 1])

        with col_inc_donut:
            if not df_incident_pie.empty:
                fig_inc_donut = create_donut_chart(df_incident_pie, names='incident_type', values='count')
                st.plotly_chart(fig_inc_donut, use_container_width=True)
            else:
                st.success("🎉 ไม่พบรายงานอุบัติเหตุในช่วงเวลานี้")

        with col_inc_insight:
            if not df_incident_pie.empty:
                render_donut_summary(
                    df_incident_pie,
                    names='incident_type',
                    values='count',
                    title="ความเสี่ยงที่พบบ่อยที่สุด",
                    unit="ครั้ง",
                    suffix_text="ของอุบัติเหตุทั้งหมด"
                )

        st.markdown("---")

        # 5. Route Rankings: Fuel Cost per Trip & Dangerous Routes (Chart on Top + Table Below)
        c_r1, c_r2 = st.columns(2)

        with c_r1:
            render_section_title("⛽ 5 เส้นทางที่มีต้นทุนเชื้อเพลิงเฉลี่ยต่อเที่ยวสูงสุด (Fuel Cost / Trip)")
            if not df_fuel_route.empty:
                # Chart (Top)
                df_fr_sort = df_fuel_route.sort_values(by="ต้นทุนน้ำมันเฉลี่ย/เที่ยว (USD/Trip)", ascending=True)
                fig_fr = px.bar(
                    df_fr_sort,
                    y="เส้นทาง (Route)",
                    x="ต้นทุนน้ำมันเฉลี่ย/เที่ยว (USD/Trip)",
                    orientation='h',
                    color="ต้นทุนน้ำมันเฉลี่ย/เที่ยว (USD/Trip)",
                    color_continuous_scale=[[0, '#FCA5A5'], [1, '#B91C1C']],
                    text_auto='$,.2f'
                )
                fig_fr.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="ต้นทุนน้ำมันเฉลี่ยต่อเที่ยว (USD/Trip)")
                st.plotly_chart(style_chart(fig_fr, height=220), use_container_width=True)

                # Table (Below)
                st.dataframe(
                    df_fuel_route.style.format({
                        "จำนวนเที่ยว (Trips)": "{:,.0f}",
                        "การใช้น้ำมันเฉลี่ย/เที่ยว (Gallons)": "{:.1f} gal",
                        "การใช้น้ำมันรวม (Gallons)": "{:,.0f} gal",
                        "ต้นทุนน้ำมันเฉลี่ย/เที่ยว (USD/Trip)": "${:,.2f}",
                        "ต้นทุนน้ำมันรวมโดยประมาณ (USD)": "${:,.2f}"
                    }),
                    use_container_width=True,
                    hide_index=True
                )

        with c_r2:
            render_section_title("🚨 5 เส้นทางที่มีความเสี่ยงอุบัติเหตุสูงสุด (Accident Prone Routes)")
            if not df_danger_route.empty:
                tot_danger_inc = df_danger_route["จำนวนอุบัติเหตุ (ครั้ง)"].sum()
                df_danger_route["สัดส่วนอุบัติเหตุ (Share %)"] = (df_danger_route["จำนวนอุบัติเหตุ (ครั้ง)"] / tot_danger_inc * 100) if tot_danger_inc > 0 else 0

                # Chart (Top)
                df_dr_sort = df_danger_route.sort_values(by="จำนวนอุบัติเหตุ (ครั้ง)", ascending=True)
                fig_dr = px.bar(
                    df_dr_sort,
                    y="เส้นทางเสี่ยง (Route)",
                    x="จำนวนอุบัติเหตุ (ครั้ง)",
                    orientation='h',
                    color="จำนวนอุบัติเหตุ (ครั้ง)",
                    color_continuous_scale=[[0, '#FCA5A5'], [1, '#991B1B']],
                    text_auto=',.0f'
                )
                fig_dr.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="จำนวนครั้งที่เกิดเหตุ")
                st.plotly_chart(style_chart(fig_dr, height=220), use_container_width=True)

                # Table (Below)
                st.dataframe(
                    df_danger_route.style.format({
                        "จำนวนอุบัติเหตุ (ครั้ง)": "{:,.0f} ครั้ง",
                        "สัดส่วนอุบัติเหตุ (Share %)": "{:.1f}%"
                    }),
                    use_container_width=True,
                    hide_index=True
                )
