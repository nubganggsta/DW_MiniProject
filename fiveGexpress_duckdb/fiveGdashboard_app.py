import duckdb
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from pathlib import Path
from plotly.subplots import make_subplots

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

# Banner Image
BANNER_IMAGE_URL = "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=2070&auto=format&fit=crop"

# CSS Styling
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:ital,wght@0,300;0,400;0,500;0,600;0,700&display=swap');

    * {{
        font-family: 'Kanit', sans-serif !important;
    }}

    .stApp {{
        background-color: #F8FAFC;
    }}

    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    
    /* Header โปร่งใส */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    /* ซ่อนเฉพาะเมนู/ปุ่ม Deploy ห้ามซ่อม stToolbar ทั้งก้อน เพราะปุ่มเปิด sidebar อยู่ข้างใน */
    [data-testid="stMainMenu"],
    [data-testid="stAppDeployButton"],
    [data-testid="stDeployButton"],
    .stDeployButton {{
        display: none !important;
    }}
    header [data-testid="stDecoration"] {{
        display: none !important;
    }}

    /* Sidebar Style */
    section[data-testid="stSidebar"] {{
        background-color: #DB1A1A !important;
        background-image: linear-gradient(180deg, #DB1A1A 0%, #A01212 100%) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.25) !important;
        border-right: none !important;
        z-index: 100 !important;
    }}
    /* Sidebar Default Text Color */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {{
        color: #FFFFFF;
    }}

    /* ปุ่มเปิด Sidebar (ตอน sidebar ถูกปิด): ให้เห็นและกดได้เสมอ ทุกเวอร์ชันของ Streamlit */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {{
        visibility: visible !important;
        z-index: 1000001 !important;
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }}
    [data-testid="stExpandSidebarButton"] *,
    [data-testid="stSidebarCollapsedControl"] *,
    [data-testid="collapsedControl"] * {{
        visibility: visible !important;
        color: #DB1A1A !important;
        fill: #DB1A1A !important;
    }}

    /* Navigation Radio Buttons */
    [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label {{
        padding: 10px 16px !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
        width: 100% !important;
        border: 1px solid transparent !important;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background-color: rgba(255, 255, 255, 0.22) !important;
        transform: translateX(4px);
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
        background-color: rgba(255, 255, 255, 0.32) !important;
        border-left: 5px solid #FFFFFF !important;
        border-radius: 4px 8px 8px 4px !important;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label p {{
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #FFFFFF !important;
        margin: 0 !important;
    }}

    /* Brand Header in Sidebar */
    .sidebar-brand-box {{
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.25);
        margin-bottom: 20px;
    }}

    .sidebar-brand-title {{
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #FFFFFF !important;
    }}

    /* Tag สีขาว ตัวอักษรสีแดง */
    .sidebar-tag {{
        display: inline-block;
        font-size: 11.5px;
        padding: 3px 10px;
        border-radius: 12px;
        background-color: #FFFFFF !important;
        color: #DB1A1A !important;
        font-weight: 700;
        margin-top: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }}

    .sidebar-tag * {{
        color: #DB1A1A !important;
    }}

    /* Header Banner styling */
    .brand-banner-image {{
        background-image: url('{BANNER_IMAGE_URL}');
        background-size: cover;
        background-position: center;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}

    .banner-overlay {{
        background-color: rgba(0, 0, 0, 0.6); 
        padding: 35px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        height: 100%;
    }}

    .brand-title {{
        color: #FFFFFF !important;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 4px;
    }}

    .brand-subtitle {{
        color: #E0E0E0 !important;
        font-size: 14.5px;
    }}

    .system-badge {{
        background-color: #DB1A1A;
        color: white !important;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13.5px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }}

    /* KPI Cards */
    .kpi-container {{
        background: linear-gradient(135deg, #DB1A1A 0%, #A31313 100%);
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid rgba(219, 26, 26, 0.25);
        box-shadow: 0 4px 14px rgba(219, 26, 26, 0.16);
        margin-bottom: 16px;
        color: #FFFFFF !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}

    .kpi-container:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(219, 26, 26, 0.26);
    }}

    .kpi-title {{
        font-size: 11.5px;
        color: #FEE2E2 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }}

    .kpi-value {{
        font-size: 25px;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-top: 5px;
        margin-bottom: 3px;
        letter-spacing: -0.3px;
    }}

    .kpi-sub {{
        font-size: 12px;
        font-weight: 500;
        color: #FFFFFF !important;
    }}

    /* Typography Hierarchy */
    /* Main Page Heading (ใหญ่ที่สุด) */
    .main-page-header {{
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-top: 10px !important;
        margin-bottom: 20px !important;
        border-left: 5px solid #DB1A1A !important;
        padding-left: 14px !important;
        line-height: 1.3 !important;
    }}

    /* Section Titles (เล็กกว่าชื่อหน้าหลัก) */
    .section-header {{
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-top: 18px !important;
        margin-bottom: 14px !important;
        border-left: 4px solid #DB1A1A !important;
        padding-left: 12px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        line-height: 1.3 !important;
    }}

    /* Chart Titles / Subheadings (เล็กกว่า Section Title) */
    h5 {{
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #1E293B !important;
        margin-top: 12px !important;
        margin-bottom: 8px !important;
    }}

    /* Insights Box */
    .insight-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 0px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
    }}

    .insight-title {{
        font-size: 13px;
        font-weight: 700;
        color: #DB1A1A !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
        border-bottom: 2px solid #FEE2E2;
        padding-bottom: 6px;
    }}

    .insight-item {{
        display: flex;
        justify-content: space-between;
        font-size: 12.5px;
        margin-bottom: 5px;
    }}

    .insight-label {{ color: #64748B !important; }}
    .insight-val {{ font-weight: 600; color: #0F172A !important; }}

    .filter-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }}
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
        db_file = Path(DB_PATH)
        if not db_file.exists():
            db_file = Path(__file__).resolve().parent / DB_PATH

        if not db_file.exists():
            st.error(
                f"ไม่พบไฟล์ฐานข้อมูล DuckDB: {db_file}\n"
                "กรุณาวาง fiveGexpress.duckdb ไว้ในโฟลเดอร์เดียวกับ dashboard_app.py"
            )
            return pd.DataFrame()

        # กำหนด project root ให้ DuckDB ใช้ค้นหา relative file paths
        # เช่น datasets/customers.csv
        project_root = Path(__file__).resolve().parent

        with duckdb.connect(database=str(db_file), read_only=True) as con:
            con.execute(
                f"SET file_search_path = '{project_root.as_posix()}'"
            )
            return con.execute(query).df()

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูลจากระบบ: {e}")
        return pd.DataFrame()

# UI Component Helpers
def render_kpi(title: str, value: str, subtext: str = "", status: str = "neutral"):
    sub_color = {
        "good": "#FEF08A",
        "risk": "#FECACA",
        "neutral": "#F1F5F9"
    }.get(status, "#F1F5F9")

    html = (
        f'<div class="kpi-container">'
        f'<div class="kpi-title">{title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub" style="color: {sub_color};">{subtext}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_section_title(title: str, is_main: bool = False):
    header_class = "main-page-header" if is_main else "section-header"
    st.markdown(f'<div class="{header_class}">{title}</div>', unsafe_allow_html=True)

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
    if color_map:
        fig = px.pie(df, names=names, values=values, hole=0.62, color=names, color_discrete_map=color_map)
    else:
        fig = px.pie(df, names=names, values=values, hole=0.62, color_discrete_sequence=DONUT_PALETTE)

    fig.update_traces(
        textinfo='none',
        hoverinfo='label+percent+value',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig.update_layout(
        template="plotly_white",
        height=height,
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Kanit, sans-serif"),
        annotations=[]
    )
    return fig

def render_donut_summary(df: pd.DataFrame, names: str, values: str, title: str, color_map: dict = None, unit: str = "ครั้ง", suffix_text: str = "ของทั้งหมด", is_currency: bool = False):
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
        sub_desc = f"{pct:.1f}% {suffix_text}" if suffix_text else f"{pct:.1f}%"
        
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

# สีของกราฟสัดส่วนอุบัติเหตุ
INCIDENT_PALETTE = [
    '#9B1C1C',
    '#E4572E',
    '#F2A65A',
    '#64748B',
    '#334155',
    '#0F766E',
    '#B08968',
    '#94A3B8',
]

def build_incident_donut(df, names_col='incident_type', values_col='count', height=420):
    """Donut chart พร้อม Data Labels (ชื่อ + จำนวน + %) และ Legend (ตรงกลางว่างตาม requirement)"""
    categories = sorted(df[names_col].astype(str).unique())
    color_map = {c: INCIDENT_PALETTE[i % len(INCIDENT_PALETTE)] for i, c in enumerate(categories)}

    fig = go.Figure(
        go.Pie(
            labels=df[names_col].astype(str),
            values=df[values_col],
            hole=0.55,
            sort=False,
            direction='clockwise',
            marker=dict(
                colors=[color_map[str(n)] for n in df[names_col]],
                line=dict(color='#FFFFFF', width=2),
            ),
            texttemplate='<b>%{label}</b><br>%{value:,} ครั้ง (%{percent})',
            textposition='outside',
            insidetextorientation='horizontal',
            hovertemplate='<b>%{label}</b><br>จำนวน: %{value:,} ครั้ง<br>สัดส่วน: %{percent}<extra></extra>',
        )
    )

    fig = style_chart(fig, height=height)
    fig.update_layout(
        showlegend=True,
        legend=dict(
            title=dict(text="ประเภทอุบัติเหตุ"),
            orientation='h',
            yanchor='top',
            y=-0.05,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#E5E7EB',
            borderwidth=1,
            font=dict(size=12),
        ),
        margin=dict(t=40, b=70, l=40, r=40),
        annotations=[]
    )
    fig.update_traces(automargin=True)
    return fig


def render_top_filters(page_prefix: str, show_facility: bool = False):
    df_years = run_query("SELECT DISTINCT year FROM dim_date ORDER BY year DESC")
    available_years = ["ภาพรวมทั้งหมด (All)"] + (df_years['year'].astype(str).tolist() if not df_years.empty else [])
    
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    if show_facility:
        col_f1, col_f2, col_f3 = st.columns([1.2, 1.5, 2])
    else:
        col_f1, col_f2, _ = st.columns([1.5, 1.8, 2.5])
    
    with col_f1:
        selected_year = st.selectbox(
            "เลือกปี (Year):",
            available_years,
            key=f"{page_prefix}_year"
        )
        
    with col_f2:
        trend_axis = st.selectbox(
            "แสดงแกนเวลาตาม (Trend Granularity):",
            ["ไตรมาส (Quarter)", "เดือน (Month)", "สัปดาห์ (Week)", "วัน (Day)", "ปี (Year)"],
            key=f"{page_prefix}_axis"
        )
        
    selected_facility = "ทุกสาขา/ศูนย์กระจายสินค้า (All)"
    if show_facility:
        df_facilities = run_query("SELECT facility_name FROM dim_facilities ORDER BY facility_name")
        facility_list = ["ทุกสาขา/ศูนย์กระจายสินค้า (All)"] + (df_facilities['facility_name'].tolist() if not df_facilities.empty else [])
        with col_f3:
            selected_facility = st.selectbox(
                "สาขา/ศูนย์กระจายสินค้า (Facility):",
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
# 3. Floating Red Sidebar & Navigation
# ==========================================
NAV_OPTIONS = [
    "◧ ภาพรวมรายได้และลูกค้า",
    "⚲ การจัดส่งและประสิทธิภาพ",
    "⚙ การซ่อมบำรุงยานพาหนะ",
    "⛨ เชื้อเพลิงและความปลอดภัย"
]

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-title">❖ 5G Express Console</div>
            <span class="sidebar-tag">● ระบบเชื่อมต่อเรียบร้อย</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "หมวดหมู่การวิเคราะห์:",
        NAV_OPTIONS,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.25);'>", unsafe_allow_html=True)
    st.caption("คลังข้อมูลโลจิสติกส์ v3.0 • DuckDB Analytics Engine")

# ==========================================
# 4. Banner Header
# ==========================================
st.markdown(
    """
    <div class="brand-banner-image">
        <div class="banner-overlay">
            <div>
                <div class="brand-title">5G EXPRESS LOGISTICS INTELLIGENCE</div>
                <div class="brand-subtitle">แดชบอร์ดบริหารจัดการปฏิบัติการขนส่ง • ข้อมูลเชื่อมต่อ DuckDB Data Warehouse</div>
            </div>
            <div class="system-badge">Executive Edition</div>
        </div>
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
if page == "◧ ภาพรวมรายได้และลูกค้า":
    render_section_title("ภาพรวมสถานะการเงินและพอร์ตลูกค้า (Financial & Customer Overview)", is_main=True)
 
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
 
    # (Top Customers query ย้ายไปอยู่ในหัวข้อที่ 6 เพราะต้องรอค่าจาก Select Box ประเภทสินค้าหลักก่อน)
 
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
        st.markdown(f"##### แนวโน้มรายได้ (Revenue Trend - {trend_axis.split(' ')[0]})")
        fig_rev = px.area(
            df_rev_trend, x='time_axis', y='total_revenue',
            color_discrete_sequence=['#DB1A1A'], markers=True
        )
        fig_rev.update_traces(fillcolor='rgba(219, 26, 26, 0.08)', line=dict(width=3, color='#DB1A1A'))
        fig_rev.update_layout(xaxis_title="", yaxis_title="รายได้ (USD)", yaxis=dict(tickformat="$,.0f"))
        st.plotly_chart(style_chart(fig_rev, height=320), width="stretch")
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        # 5. Revenue Distribution + Insight (Donut on Left, Summary on Right)
        st.markdown("##### สัดส่วนรายได้แยกตามประเภทตู้ขนส่ง (Revenue by Trailer Type)")
 
        # กำหนดสีเพียง 2 สี: สีที่ 1 = #7BCFBE, สีที่ 2 = #DB1A1A (ผูกสีกับประเภทตู้ขนส่งแต่ละประเภท)
        TRAILER_PALETTE = ['#7BCFBE', '#DB1A1A']
        trailer_colors = (
            {t: TRAILER_PALETTE[i % len(TRAILER_PALETTE)] for i, t in enumerate(df_trailer['trailer_type'].tolist())}
            if not df_trailer.empty else {}
        )
 
        col_donut_chart, col_donut_insight = st.columns([1, 1])
 
        with col_donut_chart:
            if not df_trailer.empty:
                fig_trailer = create_donut_chart(
                    df_trailer, names='trailer_type', values='total_revenue', color_map=trailer_colors
                )
                fig_trailer.update_traces(
                    texttemplate='%{label} %{percent:.1%}',
                    textposition='outside',
                    marker=dict(colors=[trailer_colors.get(t) for t in df_trailer['trailer_type']]),
                )
                fig_trailer.update_layout(
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5),
                    margin=dict(l=40, r=40),
                )
                st.plotly_chart(fig_trailer, width="stretch")
 
        with col_donut_insight:
            if not df_trailer.empty:
                render_donut_summary(
                    df_trailer,
                    names='trailer_type',
                    values='total_revenue',
                    title="สรุปสัดส่วนรายได้แยกตามประเภทตู้ขนส่ง",
                    color_map=trailer_colors,
                    unit="USD",
                    suffix_text="ของรายได้ทั้งหมด",
                    is_currency=True
                )
 
        st.markdown("---")
 
        # 6. Top 10 Customers (Ranking Chart on Top + Data Table Below)
        render_section_title("10 อันดับลูกค้าที่มีประสิทธิภาพรายได้สูงสุด (Top Customers by Revenue Efficiency: Revenue / Trip)")
 
        # 6.1 Select Box: ประเภทสินค้าหลัก (Primary Product Type) อยู่ติดกับกราฟที่ควบคุม
        ALL_FREIGHT = "All / ทั้งหมด"
        df_freight_types = run_query(
            "SELECT DISTINCT primary_freight_type FROM dim_customers "
            "WHERE primary_freight_type IS NOT NULL ORDER BY primary_freight_type"
        )
        freight_options = [ALL_FREIGHT] + (
            df_freight_types.iloc[:, 0].astype(str).tolist() if not df_freight_types.empty else []
        )
 
        col_c_space, col_c_filter = st.columns([1.8, 1.2])
        with col_c_filter:
            selected_freight = st.selectbox(
                "ประเภทสินค้าหลัก (Primary Product Type):",
                freight_options,
                index=0,
                key="p1_freight_type_selectbox"
            )
 
        # เงื่อนไข SQL ตามประเภทสินค้าที่เลือก (ต่อท้าย WHERE_SQL เดิม)
        freight_where = ""
        if selected_freight != ALL_FREIGHT:
            freight_safe = selected_freight.replace("'", "''")
            freight_where = f" AND c.primary_freight_type = '{freight_safe}'"
 
        if WHERE_SQL and WHERE_SQL.strip():
            customer_where = f"{WHERE_SQL} {freight_where}"
        else:
            customer_where = f"WHERE 1=1 {freight_where}"
 
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
            {customer_where}
            GROUP BY 1, 2
            ORDER BY "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)" DESC
            LIMIT 10
        """)
 
        if not df_top_customers.empty:
            if selected_freight == ALL_FREIGHT:
                share_base_rev = tot_rev
            else:
                df_freight_total = run_query(f"""
                    SELECT SUM(t.revenue) AS freight_revenue
                    FROM fact_trips_operations t
                    JOIN dim_customers c ON t.customer_key = c.customer_key
                    JOIN dim_date d ON t.date_key = d.date_key
                    {customer_where}
                """)
                share_base_rev = (
                    df_freight_total.iloc[0, 0]
                    if not df_freight_total.empty and df_freight_total.iloc[0, 0] is not None
                    else 0
                )
 
            df_top_customers["สัดส่วนรายได้ (Revenue Share %)"] = (
                df_top_customers["รายได้รวม (USD)"] / share_base_rev * 100 if share_base_rev and share_base_rev > 0 else 0
            )
 
            df_c_sort = df_top_customers.sort_values(by="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)", ascending=True).copy()
            df_c_sort["ลูกค้า — ประเภทสินค้า"] = (
                df_c_sort["ชื่อลูกค้า"].astype(str) + " — " + df_c_sort["ประเภทสินค้าหลัก"].astype(str)
            )
            df_c_sort["ป้ายข้อมูล"] = df_c_sort.apply(
                lambda r: f"{r['สัดส่วนรายได้ (Revenue Share %)']:.1f}% | ${r['รายได้เฉลี่ยต่อเที่ยว (USD/Trip)']:,.0f} / Trip",
                axis=1
            )
 
            fig_top_c = px.bar(
                df_c_sort,
                y="ลูกค้า — ประเภทสินค้า",
                x="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                orientation='h',
                color="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                color_continuous_scale=[[0, '#FCA5A5'], [1, '#B91C1C']],
                text="ป้ายข้อมูล",
                hover_data=["จำนวนเที่ยว (Trips)", "รายได้รวม (USD)", "สัดส่วนรายได้ (Revenue Share %)"]
            )
            fig_top_c.update_traces(textposition='outside', cliponaxis=False)
 
            eff_min = df_c_sort["รายได้เฉลี่ยต่อเที่ยว (USD/Trip)"].min()
            eff_max = df_c_sort["รายได้เฉลี่ยต่อเที่ยว (USD/Trip)"].max()
            x_min = 3000
            x_max = 3300
            if eff_min < x_min:
                x_min = int(eff_min // 50) * 50
            if eff_max > x_max:
                x_max = int(-(-eff_max // 50)) * 50
 
            fig_top_c.update_layout(
                coloraxis_showscale=False,
                yaxis_title="",
                xaxis_title="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                xaxis=dict(range=[x_min, x_max], tickformat="$,.0f", dtick=50 if (x_max - x_min) <= 500 else None),
            )
            fig_top_c = style_chart(fig_top_c, height=340)
            fig_top_c.update_layout(margin=dict(r=170))
            st.plotly_chart(fig_top_c, width="stretch")
 
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
                width="stretch",
                hide_index=True
            )
        else:
            st.info(f"ไม่พบข้อมูลลูกค้าสำหรับประเภทสินค้า '{selected_freight}' ในช่วงเวลาที่เลือก")


# -----------------------------------------------------------------------------
# หน้า 2: การจัดส่งและประสิทธิภาพ
# -----------------------------------------------------------------------------
elif page == "⚲ การจัดส่งและประสิทธิภาพ":
    render_section_title("ประสิทธิภาพการส่งมอบและพนักงานขับรถ (Delivery & Fleet Performance)", is_main=True)

    MIN_TRIPS_FOR_HUB_RANK = 30
    MIN_DRIVER_TRIPS = 20
    DRIVER_ID_COL = "driver_id"

    # 1. Global Filter Bar with Facility Filter
    selected_year, trend_axis, selected_facility, WHERE_SQL, time_expr, group_expr = render_top_filters("page2", show_facility=True)

    if WHERE_SQL and WHERE_SQL.strip():
        flag_where = f"{WHERE_SQL} AND t.on_time_flag IS NOT NULL"
    else:
        flag_where = "WHERE t.on_time_flag IS NOT NULL"

    # 2. On-Time Query
    df_ontime = run_query(f"""
        SELECT
            CASE WHEN t.on_time_flag THEN 'ตรงเวลา (On-Time)' ELSE 'ล่าช้า (Delayed)' END AS status,
            COUNT(*) AS count
        FROM fact_trips_operations t
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {flag_where}
        GROUP BY 1
    """)

    df_null_flag = run_query(f"""
        SELECT COUNT(*) FILTER (WHERE t.on_time_flag IS NULL) AS n_null
        FROM fact_trips_operations t
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
    """)
    try:
        n_null_flag = int(df_null_flag.iloc[0, 0] or 0)
    except Exception:
        n_null_flag = 0

    # 3. Bottleneck Query
    df_bottleneck_all = run_query(f"""
        SELECT
            f.facility_name AS "จุดกระจายสินค้า / คลัง",
            COALESCE(SUM(t.detention_minutes), 0) AS "เวลารอรวม (นาที)",
            COUNT(t.trip_key) AS "เที่ยวที่เข้าใช้บริการ",
            COALESCE(SUM(t.detention_minutes), 0) / COUNT(t.trip_key) AS "เวลารอต่อเที่ยว (นาที/Trip)"
        FROM fact_trips_operations t
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY 1
    """)

    # 4. Driver Performance Query
    df_drivers = run_query(f"""
        SELECT
            dr.first_name || ' ' || dr.last_name AS "พนักงานขับรถ",
            dr.{DRIVER_ID_COL} AS "รหัสพนักงาน",
            COUNT(t.trip_key) AS "จำนวนเที่ยววิ่ง (Trips)",
            SUM(t.revenue) AS "รายได้ที่สร้าง (USD)",
            SUM(t.revenue) / COUNT(t.trip_key) AS "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)"
        FROM fact_trips_operations t
        JOIN dim_drivers dr ON t.driver_key = dr.driver_key
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
        GROUP BY dr.driver_key, 1, 2
        HAVING COUNT(t.trip_key) >= {MIN_DRIVER_TRIPS}
        ORDER BY "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)" DESC
        LIMIT 10
    """)

    df_rev_total = run_query(f"""
        SELECT SUM(t.revenue) AS total_revenue
        FROM fact_trips_operations t
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
    """)
    total_revenue_all = (
        df_rev_total.iloc[0, 0]
        if not df_rev_total.empty and df_rev_total.iloc[0, 0] is not None
        else 0
    )

    sys_wait_total = 0
    sys_trips_total = 0
    sys_wait_per_trip = 0
    top5_wait_share = 0
    df_bottleneck = df_bottleneck_all
    worst_fc = "ไม่มีข้อมูล"
    worst_wait = 0

    if not df_bottleneck_all.empty:
        sys_wait_total = df_bottleneck_all["เวลารอรวม (นาที)"].sum()
        sys_trips_total = df_bottleneck_all["เที่ยวที่เข้าใช้บริการ"].sum()
        sys_wait_per_trip = (sys_wait_total / sys_trips_total) if sys_trips_total > 0 else 0

        df_bottleneck = (
            df_bottleneck_all.sort_values(by="เวลารอรวม (นาที)", ascending=False).head(5).copy()
        )
        df_bottleneck["สัดส่วนเวลารอ (% ของทั้งระบบ)"] = (
            df_bottleneck["เวลารอรวม (นาที)"] / sys_wait_total * 100 if sys_wait_total > 0 else 0
        )
        df_bottleneck["เทียบเฉลี่ยระบบ (%)"] = (
            (df_bottleneck["เวลารอต่อเที่ยว (นาที/Trip)"] / sys_wait_per_trip - 1) * 100 if sys_wait_per_trip > 0 else 0
        )
        top5_wait_share = df_bottleneck["สัดส่วนเวลารอ (% ของทั้งระบบ)"].sum()

        eligible = df_bottleneck_all[df_bottleneck_all["เที่ยวที่เข้าใช้บริการ"] >= MIN_TRIPS_FOR_HUB_RANK]
        if eligible.empty:
            eligible = df_bottleneck_all
        worst_row = eligible.loc[eligible["เวลารอต่อเที่ยว (นาที/Trip)"].idxmax()]
        worst_fc = worst_row["จุดกระจายสินค้า / คลัง"]
        worst_wait = worst_row["เวลารอต่อเที่ยว (นาที/Trip)"]

    if df_ontime.empty:
        st.warning("ไม่พบข้อมูลสำหรับการจัดส่งในช่วงเวลาหรือสาขาที่เลือก")
    else:
        tot_shipments = df_ontime['count'].sum()
        ontime_row = df_ontime[df_ontime['status'].str.contains('On-Time')]
        ontime_qty = ontime_row['count'].sum() if not ontime_row.empty else 0
        delayed_qty = tot_shipments - ontime_qty
        ontime_rate = (ontime_qty / tot_shipments * 100) if tot_shipments > 0 else 0
        delay_rate = 100.0 - ontime_rate

        # Top KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi("เที่ยวจัดส่งทั้งหมด", f"{tot_shipments:,.0f} เที่ยว", f"สาขา: {selected_facility.split('/')[0]}", "neutral")
        with k2:
            render_kpi("อัตราส่งตรงเวลา (On-Time)", f"{ontime_rate:.1f}%", f"{ontime_qty:,.0f} เที่ยวตรงเวลา", "good" if ontime_rate >= 90 else "risk")
        with k3:
            render_kpi("อัตราส่งล่าช้า (Delayed)", f"{delay_rate:.1f}%", f"{delayed_qty:,.0f} เที่ยวติดปัญหา", "risk" if delay_rate > 10 else "good")
        with k4:
            render_kpi("เวลารอคอยต่อเที่ยวสูงสุด", f"{worst_wait:.1f} นาที/Trip", f"{str(worst_fc)[:22]}", "risk")

        if n_null_flag > 0:
            st.caption(f"ℹ️ ไม่รวม {n_null_flag:,.0f} เที่ยวที่ไม่มีสถานะตรงเวลา/ล่าช้า ในการคำนวณอัตราด้านบน")

        # Row 1: On-Time Donut (Left) + Summary (Right)
        col_sla, col_sla_summary = st.columns([1, 1])

        with col_sla:
            st.markdown("##### สัดส่วนความตรงเวลา (On-Time Delivery Share)")
            sla_colors = {'ตรงเวลา (On-Time)': '#1E293B', 'ล่าช้า (Delayed)': '#DB1A1A'}

            df_sla_plot = df_ontime.sort_values(by='status', ascending=True)
            fig_sla = create_donut_chart(df_sla_plot, names='status', values='count', color_map=sla_colors)
            fig_sla.update_traces(
                texttemplate='%{label}<br>%{percent:.1%}',
                textposition='outside',
                sort=False,
                marker=dict(colors=[sla_colors.get(s, '#94A3B8') for s in df_sla_plot['status']]),
            )
            fig_sla.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5),
                margin=dict(l=40, r=40),
            )
            st.plotly_chart(fig_sla, width="stretch")

        with col_sla_summary:
            render_donut_summary(
                df_ontime,
                names='status',
                values='count',
                title=f"สรุปความตรงเวลา (สาขา: {selected_facility.split('/')[0]})",
                color_map=sla_colors,
                unit="เที่ยว",
                suffix_text="ของการจัดส่งทั้งหมด"
            )

        with st.container():
            st.markdown("##### จุดกระจายสินค้าที่มีเวลารอคอยสูงสุด (Bottleneck Ranking)")
            if not df_bottleneck.empty:
                st.caption("Top 5 จุดที่มีเวลารอรวมสูงสุด | ความยาวแท่ง = เวลารอเฉลี่ยต่อเที่ยว | เส้นประ = ค่าเฉลี่ยทั้งระบบ")
                if len(df_bottleneck_all) == 1:
                    st.caption("ℹ️ ตัวกรองสาขาเลือกไว้ 1 แห่ง จึงแสดงเพียงจุดเดียว เลือก 'ทุกสาขา' เพื่อเปรียบเทียบระหว่างจุด")

                df_b_sort = df_bottleneck.sort_values(by="เวลารอต่อเที่ยว (นาที/Trip)", ascending=True).copy()
                df_b_sort["ป้ายข้อมูล"] = df_b_sort.apply(
                    lambda r: f"{r['เวลารอต่อเที่ยว (นาที/Trip)']:.1f} นาที ({r['เทียบเฉลี่ยระบบ (%)']:+.0f}%)",
                    axis=1
                )
                fig_bot = px.bar(
                    df_b_sort,
                    y="จุดกระจายสินค้า / คลัง",
                    x="เวลารอต่อเที่ยว (นาที/Trip)",
                    orientation='h',
                    color="เวลารอต่อเที่ยว (นาที/Trip)",
                    color_continuous_scale=[[0, '#FCA5A5'], [1, '#991B1B']],
                    text="ป้ายข้อมูล",
                    hover_data=["เที่ยวที่เข้าใช้บริการ", "เวลารอรวม (นาที)", "สัดส่วนเวลารอ (% ของทั้งระบบ)"]
                )
                fig_bot.update_traces(textposition='outside', cliponaxis=False)
                if sys_wait_per_trip > 0:
                    fig_bot.add_vline(
                        x=sys_wait_per_trip,
                        line_dash="dash",
                        line_color="#1E293B",
                        annotation_text=f"เฉลี่ยระบบ {sys_wait_per_trip:.1f}",
                        annotation_position="top"
                    )
                fig_bot.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="เวลารอต่อเที่ยว (นาที/Trip)")
                fig_bot = style_chart(fig_bot, height=260)
                fig_bot.update_layout(margin=dict(r=110))
                st.plotly_chart(fig_bot, width="stretch")

                # Table (Below)
                st.dataframe(
                    df_bottleneck.style.format({
                        "เวลารอรวม (นาที)": "{:,.0f} นาที",
                        "เที่ยวที่เข้าใช้บริการ": "{:,.0f}",
                        "เวลารอเฉลี่ย (นาที)": "{:.1f} นาที",
                        "เวลารอต่อเที่ยว (นาที/Trip)": "{:.1f} นาที",
                        "สัดส่วนเวลารอ (% ของทั้งระบบ)": "{:.1f}%",
                        "เทียบเฉลี่ยระบบ (%)": "{:+.0f}%"
                    }),
                    width="stretch",
                    hide_index=True
                )

                worst_gap = ((worst_wait / sys_wait_per_trip - 1) * 100) if sys_wait_per_trip > 0 else 0
                render_summary_box(
                    title="สรุปสำหรับผู้บริหาร (Bottleneck)",
                    items=[
                        ("จุดที่รอนานสุดต่อเที่ยว", str(worst_fc)),
                        ("เวลารอต่อเที่ยวของจุดนี้", f"{worst_wait:.1f} นาที ({worst_gap:+.0f}% เทียบเฉลี่ยระบบ)"),
                        ("เวลารอเฉลี่ยทั้งระบบ", f"{sys_wait_per_trip:.1f} นาที/Trip"),
                        ("Top 5 คิดเป็นเวลารอรวม", f"{top5_wait_share:.1f}% ของทั้งระบบ"),
                        ("เวลารอสะสมทั้งระบบ", f"{sys_wait_total / 60:,.0f} ชั่วโมง"),
                    ]
                )

        st.markdown("---")

        # Driver Performance (Chart on Top + Table Below)
        render_section_title("10 อันดับพนักงานขับรถที่มีประสิทธิภาพรายได้สูงสุด (Top Drivers by Revenue Efficiency)")
        if not df_drivers.empty:
            st.caption(f"จัดอันดับเฉพาะพนักงานที่วิ่งอย่างน้อย {MIN_DRIVER_TRIPS} เที่ยว | สัดส่วนรายได้ = รายได้ของพนักงาน ÷ รายได้รวมทุกเที่ยวในช่วงเวลา/สาขาที่เลือก")

            df_drivers["สัดส่วนรายได้ (Revenue Share %)"] = (
                df_drivers["รายได้ที่สร้าง (USD)"] / total_revenue_all * 100 if total_revenue_all > 0 else 0
            )

            df_drivers["ชื่อบนกราฟ"] = "รหัส " + df_drivers["รหัสพนักงาน"].astype(str)

            df_d_chart = df_drivers.sort_values(by="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)", ascending=True).copy()
            df_d_chart["ป้ายข้อมูล"] = df_d_chart.apply(
                lambda r: f"${r['รายได้เฉลี่ยต่อเที่ยว (USD/Trip)']:,.0f} / Trip | {r['จำนวนเที่ยววิ่ง (Trips)']:,.0f} เที่ยว",
                axis=1
            )
            fig_dr = px.bar(
                df_d_chart,
                y="ชื่อบนกราฟ",
                x="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                orientation='h',
                color="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)",
                color_continuous_scale=[[0, '#FCA5A5'], [1, '#B91C1C']],
                text="ป้ายข้อมูล",
                hover_data=["พนักงานขับรถ", "จำนวนเที่ยววิ่ง (Trips)", "รายได้ที่สร้าง (USD)", "สัดส่วนรายได้ (Revenue Share %)"]
            )
            fig_dr.update_traces(textposition='outside', cliponaxis=False)
            fig_dr.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="รายได้เฉลี่ยต่อเที่ยว (USD/Trip)")
            fig_dr = style_chart(fig_dr, height=320)
            fig_dr.update_layout(margin=dict(r=170))
            st.plotly_chart(fig_dr, width="stretch")

            df_d_display = df_drivers.drop(columns=["ชื่อบนกราฟ"]).copy()
            _first_cols = ["รหัสพนักงาน", "พนักงานขับรถ"]
            df_d_display = df_d_display[_first_cols + [c for c in df_d_display.columns if c not in _first_cols]]
            df_d_display.insert(0, 'อันดับ', [f"#{i+1}" for i in range(len(df_d_display))])

            st.dataframe(
                df_d_display.style.format({
                    "จำนวนเที่ยววิ่ง (Trips)": "{:,.0f} เที่ยว",
                    "รายได้ที่สร้าง (USD)": "${:,.2f}",
                    "รายได้เฉลี่ยต่อเที่ยว (USD/Trip)": "${:,.2f}",
                    "สัดส่วนรายได้ (Revenue Share %)": "{:.2f}%"
                }),
                width="stretch",
                hide_index=True
            )
        else:
            st.info(f"ไม่พบพนักงานขับรถที่วิ่งอย่างน้อย {MIN_DRIVER_TRIPS} เที่ยวในช่วงเวลา/สาขาที่เลือก (ปรับค่า MIN_DRIVER_TRIPS ได้)")

    # Hub Expansion Analysis
    LONG_WAIT_PERCENTILE = 0.75
    HUB_LOAD_WARN = 1.25
    HUB_WAIT_WARN = 1.25
    HUB_LOAD_CRIT = 1.50
    HUB_WAIT_CRIT = 1.50

    render_section_title("ศูนย์กระจายสินค้าที่มีภาระงานสูงและเวลารอคอยสูง (Hub Expansion Analysis)")

    df_pct = run_query(f"""
        SELECT quantile_cont(t.detention_minutes, {LONG_WAIT_PERCENTILE}) AS p
        FROM fact_trips_operations t
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        JOIN dim_date d ON t.date_key = d.date_key
        {WHERE_SQL}
    """)
    try:
        LONG_WAIT_THRESHOLD_MIN = max(1, int(round(float(df_pct.iloc[0, 0]))))
    except Exception:
        LONG_WAIT_THRESHOLD_MIN = 30

    df_hub_base = run_query(f"""
        SELECT
            COALESCE(f.city, 'ไม่ระบุพื้นที่') AS city_name,
            COALESCE(f.facility_name, 'เส้นทางทั่วไป') AS fac_name,
            COUNT(t.trip_key) AS trips,
            SUM(CASE WHEN t.detention_minutes > {LONG_WAIT_THRESHOLD_MIN} THEN 1 ELSE 0 END) AS long_trips
        FROM fact_trips_operations t
        JOIN dim_date d ON t.date_key = d.date_key
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        {WHERE_SQL}
        GROUP BY 1, 2
    """)
    if not df_hub_base.empty and df_hub_base["trips"].sum() > 0:
        base_avg_trips = df_hub_base["trips"].mean()
        base_wait_rate = df_hub_base["long_trips"].sum() / df_hub_base["trips"].sum() * 100
    else:
        base_avg_trips = 0
        base_wait_rate = 0

    top_pct_label = int(round((1 - LONG_WAIT_PERCENTILE) * 100))
    render_summary_box(
        title="เกณฑ์ที่ใช้ประเมินในส่วนนี้",
        items=[
            ("เที่ยวรอนาน คือ", f"รอเกิน {LONG_WAIT_THRESHOLD_MIN} นาที (ช้าสุด {top_pct_label}% แรกของทุกเที่ยว)"),
            ("อัตราเที่ยวรอนานทั้งระบบ", f"{base_wait_rate:.1f}% ของเที่ยวทั้งหมด"),
            ("ภาระงานเฉลี่ยต่อศูนย์", f"{base_avg_trips:,.0f} เที่ยว"),
            ("🟠 หนาแน่นสูง เมื่อ", f"ภาระงาน หรือ เที่ยวรอนาน ≥ {HUB_LOAD_WARN:g} เท่าของค่าเฉลี่ย"),
            ("🔴 วิกฤต เมื่อ", f"ทั้งภาระงาน และ เที่ยวรอนาน ≥ {HUB_LOAD_CRIT:g} เท่าของค่าเฉลี่ย"),
        ]
    )
    st.caption("หมายเหตุ: เวลารอใช้ detention_minutes เป็นตัวแทน (ยังไม่ยืนยันว่าเป็นเวลารอที่คลังต้นทางโดยเฉพาะ)")

    df_cities = run_query("SELECT DISTINCT city FROM dim_facilities WHERE city IS NOT NULL ORDER BY city")
    available_cities = ["ทุกพื้นที่/เมือง (All Cities)"] + (df_cities['city'].tolist() if not df_cities.empty else [])

    col_title_space, col_city_filter = st.columns([1.8, 1.2])
    with col_city_filter:
        selected_city = st.selectbox(
            "เลือกเมือง/พื้นที่วิเคราะห์ (City):",
            available_cities,
            index=0,
            key="p2_city_selectbox"
        )

    city_where = ""
    if selected_city != "ทุกพื้นที่/เมือง (All Cities)":
        city_safe = selected_city.replace("'", "''")
        city_where = f" AND f.city = '{city_safe}'"

    if WHERE_SQL and WHERE_SQL.strip():
        route_where = f"{WHERE_SQL} {city_where}"
    else:
        route_where = f"WHERE 1=1 {city_where}"

    df_route_trend = run_query(f"""
        SELECT
            COALESCE(f.city, 'ไม่ระบุพื้นที่') AS city_name,
            COALESCE(f.facility_name, 'เส้นทางทั่วไป') AS route_name,
            {time_expr} AS time_axis,
            COUNT(t.trip_key) AS total_trips,
            SUM(t.revenue) AS total_revenue,
            AVG(t.detention_minutes) AS avg_wait_min,
            AVG(CASE WHEN t.detention_minutes > {LONG_WAIT_THRESHOLD_MIN} THEN 100.0 ELSE 0 END) AS origin_wait_pct
        FROM fact_trips_operations t
        JOIN dim_date d ON t.date_key = d.date_key
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        {route_where}
        GROUP BY f.city, f.facility_name, {group_expr}
        ORDER BY {group_expr} ASC, total_trips DESC
    """)

    df_route_summary = run_query(f"""
        SELECT
            COALESCE(f.city, 'ไม่ระบุพื้นที่') AS "เมือง/พื้นที่",
            COALESCE(f.facility_name, 'เส้นทางทั่วไป') AS "ศูนย์กระจายสินค้า",
            COUNT(t.trip_key) AS "ปริมาณงานรวม (เที่ยว)",
            SUM(t.revenue) AS "รายได้รวม (USD)",
            AVG(CASE WHEN t.on_time_flag THEN 0 WHEN NOT t.on_time_flag THEN 100.0 END) AS "อัตราล่าช้า (%)",
            AVG(t.detention_minutes) AS "เวลารอเฉลี่ย/Detention (นาที)",
            AVG(CASE WHEN t.detention_minutes > {LONG_WAIT_THRESHOLD_MIN} THEN 100.0 ELSE 0 END) AS "สัดส่วนเที่ยวรอนาน (%)"
        FROM fact_trips_operations t
        JOIN dim_date d ON t.date_key = d.date_key
        JOIN dim_facilities f ON t.facility_key = f.facility_key
        {route_where}
        GROUP BY 1, 2
        ORDER BY "ปริมาณงานรวม (เที่ยว)" DESC
    """)

    growth_col = "การเติบโตของปริมาณงาน (%)"
    growth_caption = ""
    if not df_route_trend.empty and not df_route_summary.empty:
        periods = list(dict.fromkeys(df_route_trend['time_axis'].tolist()))
        if len(periods) >= 2:
            last_p, prev_p = periods[-1], periods[-2]
            g = df_route_trend.pivot_table(
                index=['city_name', 'route_name'], columns='time_axis',
                values='total_trips', aggfunc='sum'
            )
            growth_s = ((g[last_p] / g[prev_p] - 1) * 100).replace([float('inf'), float('-inf')], float('nan'))
            df_growth = (
                growth_s.rename(growth_col).reset_index()
                .rename(columns={"city_name": "เมือง/พื้นที่", "route_name": "ศูนย์กระจายสินค้า"})
            )
            df_route_summary = df_route_summary.merge(df_growth, on=["เมือง/พื้นที่", "ศูนย์กระจายสินค้า"], how="left")
            growth_caption = (
                f"การเติบโต = ปริมาณงานช่วง {last_p} เทียบกับ {prev_p} "
                "(ถ้าช่วงล่าสุดยังไม่จบ ตัวเลขอาจต่ำกว่าความเป็นจริง)"
            )
        else:
            df_route_summary[growth_col] = float('nan')
            growth_caption = "การเติบโต: ต้องมีข้อมูลอย่างน้อย 2 ช่วงเวลา (ปรับแกนเวลาในตัวกรองด้านบน)"

    def evaluate_hub_need(trips, wait_pct):
        if base_avg_trips <= 0:
            return "🟢 ปกติ (ขีดความจุพอเพียง)"
        load_idx = trips / base_avg_trips
        wait_idx = (wait_pct / base_wait_rate) if base_wait_rate > 0 else 0
        if load_idx >= HUB_LOAD_CRIT and wait_idx >= HUB_WAIT_CRIT:
            return "🔴 วิกฤตคลังแออัด (เปิด DC ด่วน)"
        elif load_idx >= HUB_LOAD_WARN or wait_idx >= HUB_WAIT_WARN:
            return "🟠 หนาแน่นสูง (เตรียมแผนเปิด DC)"
        else:
            return "🟢 ปกติ (ขีดความจุพอเพียง)"

    if not df_route_trend.empty and not df_route_summary.empty:
        col_chart, col_recommend = st.columns([2.1, 1])

        with col_chart:
            st.markdown(f"##### ปริมาณงานและ % เที่ยวรอนานใน {selected_city} ({trend_axis.split(' ')[0]})")

            fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

            df_tmp = df_route_trend.copy()
            df_tmp['long_wait_trips'] = df_tmp['origin_wait_pct'] * df_tmp['total_trips'] / 100.0
            df_trend_grouped = df_tmp.groupby('time_axis', sort=False).agg(
                total_trips=('total_trips', 'sum'),
                long_wait_trips=('long_wait_trips', 'sum')
            ).reset_index()
            df_trend_grouped['origin_wait_pct'] = (
                df_trend_grouped['long_wait_trips'] / df_trend_grouped['total_trips'] * 100
            ).fillna(0)

            fig_dual.add_trace(
                go.Bar(
                    x=df_trend_grouped['time_axis'],
                    y=df_trend_grouped['total_trips'],
                    name="ปริมาณงาน (เที่ยว)",
                    marker_color="#7BCFBE",
                    opacity=0.75
                ),
                secondary_y=False
            )

            fig_dual.add_trace(
                go.Scatter(
                    x=df_trend_grouped['time_axis'],
                    y=df_trend_grouped['origin_wait_pct'],
                    name=f"% เที่ยวรอนาน (>{LONG_WAIT_THRESHOLD_MIN} นาที)",
                    mode="lines+markers",
                    line=dict(color="#DB1A1A", width=3),
                    marker=dict(size=7)
                ),
                secondary_y=True
            )

            fig_dual.update_xaxes(title_text="")
            fig_dual.update_yaxes(title_text="ปริมาณงาน (เที่ยว)", secondary_y=False)
            fig_dual.update_yaxes(
                title_text=f"% เที่ยวที่รอเกิน {LONG_WAIT_THRESHOLD_MIN} นาที",
                ticksuffix="%",
                secondary_y=True
            )

            fig_dual.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=30, b=20)
            )

            st.plotly_chart(style_chart(fig_dual, height=360), width="stretch", key="chart_p2_route_wait_dual")

        with col_recommend:
            top_route = df_route_summary.iloc[0]
            top_route_name = top_route["ศูนย์กระจายสินค้า"]
            top_route_city = top_route["เมือง/พื้นที่"]
            top_route_trips = top_route["ปริมาณงานรวม (เที่ยว)"]
            top_route_wait_min = top_route["เวลารอเฉลี่ย/Detention (นาที)"]
            top_route_wait_pct = top_route["สัดส่วนเที่ยวรอนาน (%)"]
            top_route_growth = top_route[growth_col]

            hub_status = evaluate_hub_need(top_route_trips, top_route_wait_pct)
            top_load_idx = (top_route_trips / base_avg_trips) if base_avg_trips > 0 else 0
            top_wait_idx = (top_route_wait_pct / base_wait_rate) if base_wait_rate > 0 else 0

            if hub_status.startswith("🟢"):
                hub_advice = "ยังไม่จำเป็นต้องเปิด Sub-DC เพิ่มในขณะนี้"
            else:
                hub_advice = f"พิจารณาเปิด Sub-DC รองรับพื้นที่ {top_route_name}"

            growth_text = f"{top_route_growth:+.1f}%" if top_route_growth == top_route_growth else "ไม่มีข้อมูลเทียบ"

            df_grow_rank = df_route_summary[df_route_summary["ปริมาณงานรวม (เที่ยว)"] >= MIN_TRIPS_FOR_HUB_RANK].dropna(subset=[growth_col])
            if not df_grow_rank.empty:
                fg = df_grow_rank.loc[df_grow_rank[growth_col].idxmax()]
                fastest_text = f"{fg['ศูนย์กระจายสินค้า']} ({fg[growth_col]:+.1f}%)"
            else:
                fastest_text = "ไม่มีข้อมูลเทียบ"

            render_summary_box(
                title=f"คำแนะนำการขยายคลัง/Hub ({selected_city})",
                items=[
                    ("เมือง/พื้นที่", str(top_route_city)),
                    ("ศูนย์ภาระงานสูงสุด", str(top_route_name)),
                    ("ปริมาณงานสะสม", f"{top_route_trips:,.0f} เที่ยว ({top_load_idx:.2f}x ของค่าเฉลี่ยศูนย์)"),
                    ("เวลารอเฉลี่ย (Detention)", f"{top_route_wait_min:.1f} นาที"),
                    ("สัดส่วนเที่ยวรอนาน", f"{top_route_wait_pct:.1f}% ({top_wait_idx:.2f}x ของทั้งระบบ)"),
                    ("การเติบโตของปริมาณงาน", growth_text),
                    ("ศูนย์ที่เติบโตเร็วสุด", fastest_text),
                    ("คำแนะนำเชิงกลยุทธ์", hub_status),
                    ("ข้อเสนอแนะพื้นที่", hub_advice),
                ]
            )

        st.markdown("##### ตารางวิเคราะห์ภาระงาน สัดส่วนเที่ยวรอนาน การเติบโต และความเร่งด่วนในการเปิดศูนย์กระจายสินค้า")
        if growth_caption:
            st.caption(growth_caption)

        df_summary_display = df_route_summary.copy()
        df_summary_display["ดัชนีภาระงาน (x)"] = (
            df_summary_display["ปริมาณงานรวม (เที่ยว)"] / base_avg_trips if base_avg_trips > 0 else 0
        )
        df_summary_display["รอนานเทียบระบบ (x)"] = (
            df_summary_display["สัดส่วนเที่ยวรอนาน (%)"] / base_wait_rate if base_wait_rate > 0 else 0
        )
        df_summary_display["สถานะขีดความจุ Hub"] = df_summary_display.apply(
            lambda r: evaluate_hub_need(r["ปริมาณงานรวม (เที่ยว)"], r["สัดส่วนเที่ยวรอนาน (%)"]),
            axis=1
        )
        df_summary_display.insert(0, 'อันดับความหนาแน่น', [f"#{i+1}" for i in range(len(df_summary_display))])

        st.dataframe(
            df_summary_display.style.format({
                "ปริมาณงานรวม (เที่ยว)": "{:,.0f} เที่ยว",
                "รายได้รวม (USD)": "${:,.2f}",
                "อัตราล่าช้า (%)": "{:.1f}%",
                "เวลารอเฉลี่ย/Detention (นาที)": "{:.1f} นาที",
                "สัดส่วนเที่ยวรอนาน (%)": "{:.1f}%",
                growth_col: "{:+.1f}%",
                "ดัชนีภาระงาน (x)": "{:.2f}x",
                "รอนานเทียบระบบ (x)": "{:.2f}x",
            }, na_rep="–"),
            width="stretch",
            hide_index=True
        )
    else:
        st.info(f"ไม่พบข้อมูลศูนย์กระจายสินค้าสำหรับพื้นที่ '{selected_city}' ในช่วงเวลาที่เลือก")
        
# -----------------------------------------------------------------------------
# หน้า 3: การซ่อมบำรุงยานพาหนะ
# -----------------------------------------------------------------------------
elif page == "⚙ การซ่อมบำรุงยานพาหนะ":
    render_section_title("การซ่อมบำรุงและสมรรถนะของฝูงรถ (Maintenance & Fleet Health)", is_main=True)

    # 1. Global Filter Bar
    selected_year, trend_axis, _, WHERE_SQL, time_expr, group_expr = render_top_filters("page3", show_facility=False)

    try:
        _tr_df = run_query(
            "SELECT column_name FROM information_schema.columns WHERE lower(table_name) = 'dim_trucks'"
        )
        _tr_cols = {str(c).lower(): str(c) for c in _tr_df['column_name']}
    except Exception:
        _tr_cols = {}

    city_expr = None
    for _cn in ["city", "home_city", "base_city", "terminal_city", "location_city", "home_terminal"]:
        if _cn in _tr_cols:
            city_expr = f"tr.{_tr_cols[_cn]}"
            break
    city_select_sql = f'{city_expr} AS "เมือง (City)",' if city_expr else ""
    city_group_sql = f", {city_expr}" if city_expr else ""
    if city_expr is None:
        st.info("ไม่พบคอลัมน์เมือง (เช่น home_terminal) ใน dim_trucks จึงไม่สามารถแสดงข้อมูลเมืองได้")

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

    df_make_type = run_query(f"""
        WITH t AS (
            SELECT
                tr.make AS make_name,
                m.maintenance_type AS mtype,
                COUNT(m.maintenance_key) AS cnt
            FROM fact_maintenance m
            JOIN dim_trucks tr ON m.truck_key = tr.truck_key
            JOIN dim_date d ON m.date_key = d.date_key
            {WHERE_SQL}
            GROUP BY 1, 2
        ),
        tot AS (
            SELECT make_name, SUM(cnt) AS total_cnt FROM t GROUP BY 1
        ),
        ranked AS (
            SELECT
                t.make_name, t.mtype, t.cnt, tot.total_cnt,
                ROW_NUMBER() OVER (PARTITION BY t.make_name ORDER BY t.cnt DESC, t.mtype) AS rn
            FROM t
            JOIN tot ON t.make_name = tot.make_name
        )
        SELECT
            make_name AS "ยี่ห้อรถ (Make)",
            mtype AS "ประเภทงานซ่อมที่พบมากที่สุด (Most Common Type)",
            ROUND(cnt * 100.0 / total_cnt, 1) AS "สัดส่วนประเภทหลัก (%)"
        FROM ranked
        WHERE rn = 1
    """)

    if not df_truck_brands.empty:
        df_truck_brands = df_truck_brands.merge(df_make_type, on="ยี่ห้อรถ (Make)", how="left")
        df_truck_brands["ประเภทงานซ่อมที่พบมากที่สุด (Most Common Type)"] = \
            df_truck_brands["ประเภทงานซ่อมที่พบมากที่สุด (Most Common Type)"].fillna("-")

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
        st.markdown(f"##### แนวโน้มค่าใช้จ่ายซ่อมบำรุง (Maintenance Cost Trend - {trend_axis.split(' ')[0]})")
        fig_m = px.line(
            df_maint_trend, x='time_axis', y='total_cost',
            markers=True, color_discrete_sequence=['#DB1A1A']
        )
        fig_m.update_traces(line=dict(width=3, color='#DB1A1A'), marker=dict(size=7, color='#991B1B'))
        fig_m.update_layout(xaxis_title="", yaxis_title="ค่าซ่อม (USD)", yaxis=dict(tickformat="$,.0f"))
        st.plotly_chart(style_chart(fig_m, height=310), width="stretch")

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. Maintenance Type Distribution + Insight (Donut on Left, Summary on Right)
        st.markdown("##### สัดส่วนประเภทงานซ่อมบำรุง (Maintenance Type Distribution)")
        col_m_donut, col_m_insight = st.columns([1, 1])

        P3_TYPE_COLORS = ['#991B1B', '#334155', '#D97706', '#0F766E',
                          '#2563EB', '#7C3AED', '#94A3B8', '#BE185D']

        with col_m_donut:
            if not df_mtype.empty:
                fig_type = px.pie(
                    df_mtype,
                    names='maintenance_type',
                    values='job_count',
                    hole=0.55,
                    color_discrete_sequence=P3_TYPE_COLORS
                )
                fig_type.update_traces(
                    sort=False,
                    textposition='outside',
                    texttemplate='<b>%{label}</b><br>%{value:,} ครั้ง | %{percent:.1%}',
                    marker=dict(line=dict(color='#FFFFFF', width=2)),
                    hovertemplate="<b>%{label}</b><br>%{value:,} ครั้ง (%{percent:.1%})<extra></extra>"
                )
                fig_type = style_chart(fig_type, height=420)
                fig_type.update_layout(
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="top", y=-0.08, xanchor="center", x=0.5, title_text=""),
                    margin=dict(l=40, r=40, t=40, b=60),
                    annotations=[]
                )
                st.plotly_chart(fig_type, width="stretch", key="chart_maint_type_donut")

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
        render_section_title("อันดับค่าใช้จ่ายและความถี่ในการซ่อมบำรุงแยกตามยี่ห้อรถ (Truck Make Analysis)")
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
                hover_data=["ความถี่ในการซ่อม (Job Count)", "ค่าซ่อมเฉลี่ย/ครั้ง (USD)", "เวลาจอดเสียรวม (ชม.)",
                            "ประเภทงานซ่อมที่พบมากที่สุด (Most Common Type)", "สัดส่วนประเภทหลัก (%)"]
            )
            fig_brand.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="ค่าใช้จ่ายซ่อมรวม (USD)")

            st.plotly_chart(style_chart(fig_brand, height=230), width="stretch", key="chart_truck_brand_cost")

            df_tb_display = df_truck_brands.copy()
            df_tb_display.insert(0, 'อันดับ', [f"#{i+1}" for i in range(len(df_tb_display))])

            st.dataframe(
                df_tb_display.style.format({
                    "ความถี่ในการซ่อม (Job Count)": "{:,.0f} ครั้ง",
                    "ค่าใช้จ่ายรวม (USD)": "${:,.2f}",
                    "ค่าซ่อมเฉลี่ย/ครั้ง (USD)": "${:,.2f}",
                    "เวลาจอดเสียรวม (ชม.)": "{:,.1f} ชม.",
                    "เวลาจอดเสียเฉลี่ย/ครั้ง (ชม.)": "{:,.2f} ชม.",
                    "สัดส่วนประเภทหลัก (%)": "{:,.1f}%"
                }, na_rep="-"),
                width="stretch",
                hide_index=True
            )

        # 6. Top Trucks by Downtime
        st.markdown("---")
        col_title, col_filter = st.columns([2, 1])
        with col_title:
            render_section_title("10 อันดับรถบรรทุกที่มีระยะเวลาจอดเสีย (Downtime) มากที่สุด")
        with col_filter:
            status_filter = st.selectbox(
                "กรองตามสถานะรถ:",
                options=["ทั้งหมด", "Active", "Maintenance"],
                index=0,
                key="p3_downtime_status_selectbox"
            )

        status_where = ""
        if status_filter == "Active":
            status_where = " AND LOWER(tr.status) LIKE '%active%'"
        elif status_filter == "Maintenance":
            status_where = " AND (LOWER(tr.status) LIKE '%maint%' OR LOWER(tr.status) LIKE '%maintenance%')"

        df_top_downtime = run_query(f"""
            SELECT 
                tr.truck_id AS "รหัสรถบรรทุก",
                tr.make AS "ยี่ห้อ",
                {city_select_sql}
                tr.status AS "สถานะปัจจุบัน",
                SUM(m.downtime_hours) AS "เวลาจอดเสียรวม (ชม.)",
                SUM(m.maintenance_cost) AS "ค่าใช้จ่ายรวม (USD)",
                SUM(m.maintenance_count) AS "จำนวนครั้งที่ซ่อม (ครั้ง)"
            FROM fact_maintenance m
            JOIN dim_trucks tr ON m.truck_key = tr.truck_key
            JOIN dim_date d ON m.date_key = d.date_key
            {WHERE_SQL} {status_where}
            GROUP BY tr.truck_id, tr.make, tr.status{city_group_sql}
            ORDER BY "เวลาจอดเสียรวม (ชม.)" DESC
            LIMIT 10
        """)

        if not df_top_downtime.empty:
            col_chart, col_insight = st.columns([2.2, 1])

            with col_chart:
                df_dt_sort = df_top_downtime.sort_values(by="เวลาจอดเสียรวม (ชม.)", ascending=True)

                fig_downtime = px.bar(
                    df_dt_sort,
                    y="รหัสรถบรรทุก",
                    x="เวลาจอดเสียรวม (ชม.)",
                    orientation='h',
                    color="เวลาจอดเสียรวม (ชม.)",
                    color_continuous_scale=[[0, '#FCA5A5'], [1, '#991B1B']],
                    text="เวลาจอดเสียรวม (ชม.)",
                    hover_data=["ยี่ห้อ", "สถานะปัจจุบัน", "ค่าใช้จ่ายรวม (USD)", "จำนวนครั้งที่ซ่อม (ครั้ง)"]
                )

                fig_downtime.update_traces(
                    texttemplate=' <b>%{text:,.0f} ชม.</b>',
                    textposition='outside',
                    hovertemplate="<b>รหัสรถ:</b> %{y}<br>" +
                                  "<b>ยี่ห้อ:</b> %{customdata[0]}<br>" +
                                  "<b>สถานะ:</b> %{customdata[1]}<br>" +
                                  "<b>Downtime สะสม:</b> %{x:,.0f} ชม.<br>" +
                                  "<b>ค่าซ่อมสะสม:</b> $%{customdata[2]:,.2f}<br>" +
                                  "<b>เข้าซ่อม:</b> %{customdata[3]:,.0f} ครั้ง<extra></extra>"
                )

                fig_downtime.update_layout(
                    coloraxis_showscale=False,
                    yaxis_title="",
                    xaxis_title="ระยะเวลาจอดเสียสะสม (ชั่วโมง)",
                    xaxis=dict(range=[0, df_top_downtime['เวลาจอดเสียรวม (ชม.)'].max() * 1.25])
                )

                st.plotly_chart(style_chart(fig_downtime, height=340), width="stretch", key="chart_top_truck_downtime")

            with col_insight:
                top_dt_truck = df_top_downtime.iloc[0]
                render_summary_box(
                    title=f"รถที่มี Downtime สูงสุด ({status_filter})",
                    items=[
                        ("รหัสรถบรรทุก", str(top_dt_truck['รหัสรถบรรทุก'])),
                        ("ยี่ห้อ / แบรนด์", str(top_dt_truck['ยี่ห้อ'])),
                        ("สถานะปัจจุบัน", str(top_dt_truck['สถานะปัจจุบัน'])),
                        ("เวลาจอดเสียรวม", f"{top_dt_truck['เวลาจอดเสียรวม (ชม.)']:,.0f} ชั่วโมง"),
                        ("ค่าซ่อมบำรุงรวม", f"${top_dt_truck['ค่าใช้จ่ายรวม (USD)']:,.2f}"),
                        ("จำนวนครั้งที่เข้าซ่อม", f"{top_dt_truck['จำนวนครั้งที่ซ่อม (ครั้ง)']:,.0f} ครั้ง"),
                    ]
                )

            df_dt_display = df_top_downtime.copy()
            df_dt_display.insert(0, 'อันดับ', [f"#{i+1}" for i in range(len(df_dt_display))])

            st.dataframe(
                df_dt_display.style.format({
                    "เวลาจอดเสียรวม (ชม.)": "{:,.1f} ชม.",
                    "ค่าใช้จ่ายรวม (USD)": "${:,.2f}",
                    "จำนวนครั้งที่ซ่อม (ครั้ง)": "{:,.0f} ครั้ง"
                }),
                width="stretch",
                hide_index=True
            )
        else:
            st.info(f"ไม่พบข้อมูลรถบรรทุกสถานะ '{status_filter}' ในช่วงเวลาที่เลือก")

        # 7. City Analysis
        st.markdown("---")
        render_section_title("วิเคราะห์การซ่อมบำรุงและรถเสียตามเมือง (City Analysis)")

        C_CITY = "เมือง (City)"
        C_TRUCKS = "รถที่ได้รับผลกระทบ (Unique Trucks)"
        C_EVENTS = "เหตุการณ์ซ่อม (Maintenance Events)"
        C_DT = "เวลาจอดเสียรวม (ชม.)"
        C_AVG_DT = "เวลาจอดเสียเฉลี่ย/ครั้ง (ชม.)"
        C_COST = "ค่าซ่อมรวม (USD)"

        df_city = None
        if city_expr:
            df_city = run_query(f"""
                SELECT
                    COALESCE(CAST({city_expr} AS VARCHAR), 'ไม่ระบุ') AS "{C_CITY}",
                    COUNT(DISTINCT tr.truck_id) AS "{C_TRUCKS}",
                    COUNT(m.maintenance_key) AS "{C_EVENTS}",
                    SUM(m.downtime_hours) AS "{C_DT}",
                    ROUND(AVG(m.downtime_hours), 2) AS "{C_AVG_DT}",
                    SUM(m.maintenance_cost) AS "{C_COST}"
                FROM fact_maintenance m
                JOIN dim_trucks tr ON m.truck_key = tr.truck_key
                JOIN dim_date d ON m.date_key = d.date_key
                {WHERE_SQL}
                GROUP BY 1
                ORDER BY "{C_EVENTS}" DESC
            """)

        if df_city is None:
            st.info("ไม่สามารถแสดง City Analysis ได้ เนื่องจากไม่พบคอลัมน์เมืองใน Dataset")
        elif df_city.empty:
            st.info("ไม่พบข้อมูลเมืองสำหรับเงื่อนไขที่เลือก")
        else:
            df_city_display = df_city.copy()
            df_city_display.insert(0, 'อันดับ', [f"#{i+1}" for i in range(len(df_city_display))])
            st.dataframe(
                df_city_display.style.format({
                    C_TRUCKS: "{:,.0f} คัน",
                    C_EVENTS: "{:,.0f} ครั้ง",
                    C_DT: "{:,.1f} ชม.",
                    C_AVG_DT: "{:,.2f} ชม.",
                    C_COST: "${:,.2f}"
                }, na_rep="-"),
                width="stretch",
                hide_index=True
            )
            st.caption("จำนวนรถนับจาก truck_id ที่ไม่ซ้ำกัน ส่วนเหตุการณ์ซ่อมนับจากจำนวนรายการซ่อม รถ 1 คันอาจมีหลายเหตุการณ์")

        # 8. Data-driven Recommendations
        st.markdown("---")
        st.markdown("##### คำแนะนำจากข้อมูล (Data-driven Recommendations)")

        recs = []

        if df_city is not None and len(df_city) > 1:
            tot_ev_city = df_city[C_EVENTS].sum()
            tot_dt_city = df_city[C_DT].sum()

            r_ev = df_city.sort_values(C_EVENTS, ascending=False).iloc[0]
            share_ev = (r_ev[C_EVENTS] / tot_ev_city * 100) if tot_ev_city else 0
            recs.append(
                f"เมือง {r_ev[C_CITY]} มี Maintenance Events สูงสุด {r_ev[C_EVENTS]:,.0f} ครั้ง "
                f"({share_ev:,.1f}% ของเหตุการณ์ซ่อมทั้งหมด) จึงควรตรวจสอบประเภทงานซ่อมที่เกิดขึ้นบ่อยในพื้นที่ดังกล่าว"
            )

            r_tr = df_city.sort_values(C_TRUCKS, ascending=False).iloc[0]
            recs.append(
                f"เมือง {r_tr[C_CITY]} มีจำนวนรถที่ได้รับผลกระทบ (Unique Trucks) สูงสุด {r_tr[C_TRUCKS]:,.0f} คัน "
                f"จากเหตุการณ์ซ่อม {r_tr[C_EVENTS]:,.0f} ครั้ง"
            )

            r_dt = df_city.sort_values(C_DT, ascending=False).iloc[0]
            share_dt = (r_dt[C_DT] / tot_dt_city * 100) if tot_dt_city else 0
            recs.append(
                f"เมือง {r_dt[C_CITY]} มี Downtime รวมสูงสุด {r_dt[C_DT]:,.1f} ชั่วโมง "
                f"({share_dt:,.1f}% ของ Downtime รวม) ควรตรวจสอบสาเหตุของ Downtime และประเภทงานซ่อมที่เกี่ยวข้องเพิ่มเติม"
            )
        elif df_city is not None and len(df_city) == 1:
            r_one = df_city.iloc[0]
            recs.append(
                f"เมือง {r_one[C_CITY]} มี Maintenance Events {r_one[C_EVENTS]:,.0f} ครั้ง "
                f"จากรถ {r_one[C_TRUCKS]:,.0f} คัน และมี Downtime รวม {r_one[C_DT]:,.1f} ชั่วโมง "
                f"(เฉลี่ย {r_one[C_AVG_DT]:,.2f} ชั่วโมง/ครั้ง)"
            )

        if not df_mtype.empty:
            tot_type_jobs = df_mtype['job_count'].sum()
            r_type = df_mtype.sort_values('job_count', ascending=False).iloc[0]
            share_type = (r_type['job_count'] / tot_type_jobs * 100) if tot_type_jobs else 0
            recs.append(
                f"ประเภทงานซ่อม {r_type['maintenance_type']} มีสัดส่วนสูงสุด {share_type:,.1f}% "
                f"({r_type['job_count']:,.0f} จาก {tot_type_jobs:,.0f} งาน)"
            )

        if not df_truck_brands.empty:
            r_mk = df_truck_brands.sort_values("ความถี่ในการซ่อม (Job Count)", ascending=False).iloc[0]
            mk_type = r_mk["ประเภทงานซ่อมที่พบมากที่สุด (Most Common Type)"]
            mk_share = r_mk["สัดส่วนประเภทหลัก (%)"]
            mk_txt = f"ยี่ห้อ {r_mk['ยี่ห้อรถ (Make)']} มีความถี่ในการซ่อมสูงสุด {r_mk['ความถี่ในการซ่อม (Job Count)']:,.0f} ครั้ง"
            if mk_type != "-" and mk_share == mk_share:
                mk_txt += f" โดยประเภท {mk_type} เป็นประเภทหลักในสัดส่วน {mk_share:,.1f}% จึงควรติดตามรูปแบบการบำรุงรักษาของรถกลุ่มนี้"
            recs.append(mk_txt)

            dfm = df_truck_brands.dropna(subset=["สัดส่วนประเภทหลัก (%)"])
            if not dfm.empty:
                r_sh = dfm.sort_values("สัดส่วนประเภทหลัก (%)", ascending=False).iloc[0]
                recs.append(
                    f"ยี่ห้อ {r_sh['ยี่ห้อรถ (Make)']} มีประเภทงานซ่อมประเภทเดียวสูงสุดที่ {r_sh['สัดส่วนประเภทหลัก (%)']:,.1f}% "
                    f"({r_sh['ประเภทงานซ่อมที่พบมากที่สุด (Most Common Type)']}) "
                    f"จากงานซ่อมทั้งหมด {r_sh['ความถี่ในการซ่อม (Job Count)']:,.0f} ครั้ง"
                )

        if recs:
            st.markdown("\n".join([f"- {t}" for t in recs]))
        else:
            st.info("ข้อมูลไม่เพียงพอสำหรับการสร้างคำแนะนำ")

# -----------------------------------------------------------------------------
# หน้า 4: เชื้อเพลิงและความปลอดภัย
# -----------------------------------------------------------------------------
elif page == "⛨ เชื้อเพลิงและความปลอดภัย" or page == "เชื้อเพลิงและความปลอดภัย":
    render_section_title("การบริหารต้นทุนเชื้อเพลิงและสถิติความปลอดภัย (Fuel & Operational Safety)", is_main=True)
 
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
 
        cost_per_trip = tot_fuel_cost / tot_trips if tot_trips > 0 else 0
        avg_fuel_price = tot_fuel_cost / tot_gallons if tot_gallons > 0 else 0
        total_incidents = df_incident_pie['count'].sum() if not df_incident_pie.empty else 0
 
        COL_ROUTE = "เส้นทาง (Route)"
        COL_TRIPS = "จำนวนเที่ยว (Trips)"
        COL_AVG_GAL = "การใช้เชื้อเพลิงเฉลี่ย/เที่ยว (Gallons)"
        COL_TOT_GAL = "การใช้เชื้อเพลิงรวม (Gallons)"
        COL_AVG_COST = "ต้นทุนเชื้อเพลิงเฉลี่ย/เที่ยว (USD/Trip)"
        COL_TOT_COST = "ต้นทุนเชื้อเพลิงรวมโดยประมาณ (USD)"
 
        df_fuel_route = run_query(f"""
            SELECT
                r.origin_city || ' -> ' || r.destination_city AS "{COL_ROUTE}",
                COUNT(t.trip_key) AS "{COL_TRIPS}",
                AVG(t.fuel_gallons_used) AS "{COL_AVG_GAL}",
                SUM(t.fuel_gallons_used) AS "{COL_TOT_GAL}",
                (AVG(t.fuel_gallons_used) * {avg_fuel_price}) AS "{COL_AVG_COST}",
                (SUM(t.fuel_gallons_used) * {avg_fuel_price}) AS "{COL_TOT_COST}"
            FROM fact_trips_operations t
            JOIN dim_routes r ON t.route_key = r.route_key
            JOIN dim_date d ON t.date_key = d.date_key
            {WHERE_SQL}
            GROUP BY 1
            ORDER BY "{COL_AVG_COST}" DESC
            LIMIT 5
        """)
 
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
            render_kpi("ต้นทุนค่าเชื้อเพลิงรวม", f"${tot_fuel_cost:,.2f}", "Total Fuel Purchased", "neutral")
        with k2:
            render_kpi("ต้นทุนเชื้อเพลิงเฉลี่ย/เที่ยว", f"${cost_per_trip:,.2f}", "Fuel Cost / Completed Trip", "good")
        with k3:
            render_kpi("ปริมาณเชื้อเพลิงรวม", f"{tot_gallons:,.0f} gal", f"เฉลี่ย ${avg_fuel_price:.2f} / gal", "neutral")
        with k4:
            render_kpi("อุบัติเหตุและเหตุการณ์เสี่ยง", f"{total_incidents:,.0f} ครั้ง", "Safety Incidents", "risk" if total_incidents > 0 else "good")
 
        # 3. Fuel Cost Trend (Top Chart)
        st.markdown(f"##### แนวโน้มต้นทุนเชื้อเพลิง (Fuel Cost Trend - {trend_axis.split(' ')[0]})")
        fig_ftrend = px.line(
            df_fuel_trend, x='time_axis', y='total_fuel_cost',
            markers=True, color_discrete_sequence=['#DB1A1A']
        )
        fig_ftrend.update_traces(line=dict(width=3, color='#DB1A1A'), marker=dict(size=7, color='#991B1B'))
        fig_ftrend.update_layout(xaxis_title="", yaxis_title="ค่าเชื้อเพลิง (USD)", yaxis=dict(tickformat="$,.0f"))
        st.plotly_chart(style_chart(fig_ftrend, height=310), width="stretch")
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        # 4. Incident Distribution + Insight (Donut on Left, Summary on Right)
        st.markdown("##### สัดส่วนประเภทอุบัติเหตุและความเสี่ยง (Incident Type Distribution)")
        col_inc_donut, col_inc_insight = st.columns([1, 1])
 
        with col_inc_donut:
            if not df_incident_pie.empty:
                fig_inc_donut = build_incident_donut(df_incident_pie, names_col='incident_type', values_col='count')
                st.plotly_chart(fig_inc_donut, width="stretch")
            else:
                st.success("ไม่พบรายงานอุบัติเหตุในช่วงเวลานี้")
 
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
            render_section_title("5 เส้นทางที่มีต้นทุนเชื้อเพลิงเฉลี่ยต่อเที่ยวสูงสุด (Fuel Cost / Trip)")
            if not df_fuel_route.empty:
                df_fr_sort = df_fuel_route.sort_values(by=COL_AVG_COST, ascending=True)
                fig_fr = px.bar(
                    df_fr_sort,
                    y=COL_ROUTE,
                    x=COL_AVG_COST,
                    orientation='h',
                    color=COL_AVG_COST,
                    color_continuous_scale=[[0, '#FCA5A5'], [1, '#B91C1C']],
                    text_auto='$,.2f'
                )
                fig_fr.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="ต้นทุนเชื้อเพลิงเฉลี่ยต่อเที่ยว (USD/Trip)")
                st.plotly_chart(style_chart(fig_fr, height=220), width="stretch")
 
                st.dataframe(
                    df_fuel_route.style.format({
                        COL_TRIPS: "{:,.0f}",
                        COL_AVG_GAL: "{:.1f} gal",
                        COL_TOT_GAL: "{:,.0f} gal",
                        COL_AVG_COST: "${:,.2f}",
                        COL_TOT_COST: "${:,.2f}"
                    }),
                    width="stretch",
                    hide_index=True
                )
 
        with c_r2:
            render_section_title("5 เส้นทางที่มีความเสี่ยงอุบัติเหตุสูงสุด (Accident Prone Routes)")
            if not df_danger_route.empty:
                tot_danger_inc = df_danger_route["จำนวนอุบัติเหตุ (ครั้ง)"].sum()
                df_danger_route["สัดส่วนอุบัติเหตุ (Share %)"] = (df_danger_route["จำนวนอุบัติเหตุ (ครั้ง)"] / tot_danger_inc * 100) if tot_danger_inc > 0 else 0
 
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
                st.plotly_chart(style_chart(fig_dr, height=220), width="stretch")
 
                st.dataframe(
                    df_danger_route.style.format({
                        "จำนวนอุบัติเหตุ (ครั้ง)": "{:,.0f} ครั้ง",
                        "สัดส่วนอุบัติเหตุ (Share %)": "{:.1f}%"
                    }),
                    width="stretch",
                    hide_index=True
                )