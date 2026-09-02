import duckdb
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st

import streamlit as st

st.set_page_config(layout="wide")

# =========================================================
# CUSTOM SIDEBAR STYLING (RED THEME)
# =========================================================
st.markdown(
    """
    <style>
    /* 1. เปลี่ยนสีพื้นหลัง Sidebar เป็นสีแดง (Gradient ลุคพรีเมียม) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #B30000 0%, #800000 100%) !important;
    }

    /* 2. ปรับแต่งข้อความทั่วไปใน Sidebar ให้เป็นสีขาว */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* 3. ปรับแต่งหัวข้อหลักและ Header ใน Sidebar */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.3);
    }

    /* 4. ปรับแต่ง Radio Button (ตัวเลือกหมวดหมู่) ให้สวยงาม */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 6px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* เมื่อเอาเมาส์ไปชี้ที่ตัวเลือก */
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.25);
        cursor: pointer;
    }

    /* 5. ปรับแต่ง Dropdown (Selectbox ตัวกรองปี) */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 8px;
        border: none !important;
    }
    
    /* ตัวอักษรภายใน Dropdown ให้เป็นสีเข้มเพื่อให้เห็นชัดเจน */
    [data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #1A1D20 !important;
        font-weight: 600;
    }

    /* 6. เส้นแบ่ง Divider ให้เป็นสีขาวโปร่งแสง */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 1. Page Config & Custom Styling (Global Design System)
# =========================================================
st.set_page_config(
    page_title="Logistics Analytics Console - 5G Express",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# ตั้งค่า Font Kanit ให้กับ Plotly Charts ทุกรูปในระบบ
# ---------------------------------------------------------
pio.templates.default = "plotly"
pio.templates["plotly"].layout.font.family = "Kanit, sans-serif"

# Custom Design System CSS (รวม Kanit Font, Color Palette & Layout)
st.markdown(
    """
    <style>
    /* Import Google Font - Kanit */
    @import url('https://fonts.googleapis.com/css2?family=Kanit:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

    /* บังคับใช้ Kanit กับทุกองค์ประกอบ */
    * {
        font-family: 'Kanit', sans-serif !important;
    }
   
    html, body, [class*="css"], .stApp, button, input, select, textarea, div, span, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Kanit', sans-serif !important;
    }

    .stApp {
        background-color: #f8f9fa;
    }
   
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
   
    /* Header Image Styling */
    .main-header-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 100%;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* KPI Card System */
    .kpi-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px 22px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        margin-bottom: 12px;
    }
    .kpi-title {
        font-size: 13px;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Kanit', sans-serif !important;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #1a1d20;
        margin-top: 4px;
        margin-bottom: 2px;
        font-family: 'Kanit', sans-serif !important;
    }
    /* โทนสีเขียว #8CC7C4 */
    .kpi-sub {
        font-size: 12px;
        color: #8CC7C4;
        font-weight: 600;
        font-family: 'Kanit', sans-serif !important;
    }
    /* โทนสีแดง #DB1A1A */
    .kpi-sub-risk {
        font-size: 12px;
        color: #4FB7B3;
        font-weight: 600;
        font-family: 'Kanit', sans-serif !important;
    }
   
    /* Section Headers */
    .section-header {
        font-size: 16px;
        font-weight: 700;
        color: #212529;
        margin-top: 5px;
        margin-bottom: 15px;
        border-left: 4px solid #DB1A1A;
        padding-left: 10px;
        font-family: 'Kanit', sans-serif !important;
    }
   
    /* Utility Styles */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 700;
        font-family: 'Kanit', sans-serif !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)




# Reusable Helper Component for KPI Cards
def render_kpi_card(
    title: str, value: str, subtext: str, is_risk: bool = False
):
    sub_class = "kpi-sub-risk" if is_risk else "kpi-sub"
    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="{sub_class}">{subtext}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# =========================================================
# 2. Database Connection & Global Filters
# =========================================================
@st.cache_resource
def get_connection():
    return duckdb.connect("dev.duckdb", read_only=True)


try:
    conn = get_connection()
except Exception as e:
    st.error(f"⚠️ ไม่สามารถเชื่อมต่อกับ Data Warehouse ได้: {e}")
    st.stop()


# Helper Function สำหรับรัน SQL
def run_query(sql_query):
    try:
        return conn.query(sql_query).df()
    except Exception as err:
        st.error(f"SQL Query Error: {err}")
        return pd.DataFrame()


# Global Sidebar Filter
with st.sidebar:
    st.title("🚚 5G Express")
    st.caption("Data Warehouse Analytics Console")
    st.markdown("---")

    menu = st.radio(
        "📌 เลือกหมวดหมู่การวิเคราะห์:",
        [
            "📈 ภาพรวมการดำเนินงาน (Executive Overview)",
            "💰 การวิเคราะห์รายได้และพฤติกรรมลูกค้า",
            "🚛 การบริหารจัดการกองรถและการซ่อมบำรุง",
            "⏱️ ประสิทธิภาพการจัดส่งและความตรงต่อเวลา",
            "⛽ ตัวชี้วัดการใช้น้ำมันและความปลอดภัยในการขนส่ง",
        ],
    )

    st.markdown("---")
    st.subheader("🔍 ตัวกรองข้อมูลหลัก (Global Filter)")

    # Fetch available years
    df_years = run_query(
        "SELECT DISTINCT year FROM dim_date WHERE year IS NOT NULL ORDER BY year DESC"
    )
    years_available = (
        df_years["year"].tolist() if not df_years.empty else [2026]
    )
    years_available.insert(0, "ทั้งหมด")
    selected_year = st.selectbox("เลือกปี (Year)", years_available)

    # Clause filters
    year_clause = (
        "" if selected_year == "ทั้งหมด" else f"AND d.year = {selected_year}"
    )


# =========================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# =========================================================
if menu == "📈 ภาพรวมการดำเนินงาน (Executive Overview)":
    st.title("📈 ภาพรวมการดำเนินงาน (Executive Overview)")
    st.caption("สรุปดัชนีชี้วัดผลงานหลัก (KPIs) และแนวโน้มภาพรวมขององค์กร")
    st.markdown("<br>", unsafe_allow_html=True)

    # 1. KPI Calculation
    rev_res = run_query(
        f"SELECT COALESCE(SUM(f.revenue), 0) FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
    )
    rev_val = rev_res.iloc[0, 0] if not rev_res.empty else 0

    del_res = run_query(
        f"SELECT COUNT(*) FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
    )
    delivery_count = del_res.iloc[0, 0] if not del_res.empty else 0

    trip_res = run_query(
        f"SELECT COUNT(*) FROM fact_trips f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
    )
    trip_count = trip_res.iloc[0, 0] if not trip_res.empty else 0

    fuel_res = run_query(
        f"SELECT COALESCE(SUM(f.total_cost), 0) FROM fact_fuel f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
    )
    fuel_cost = fuel_res.iloc[0, 0] if not fuel_res.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            "รายได้รวมทั้งหมด", f"฿{rev_val:,.2f}", "Total Revenue"
        )
    with c2:
        render_kpi_card(
            "จำนวนการจัดส่งสินค้า", f"{delivery_count:,}", "Total Deliveries"
        )
    with c3:
        render_kpi_card(
            "จำนวนเที่ยววิ่งทั้งหมด", f"{trip_count:,}", "Total Trips"
        )
    with c4:
        render_kpi_card(
            "ค่าใช้จ่ายน้ำมันรวม",
            f"฿{fuel_cost:,.2f}",
            "Total Fuel Expense",
            is_risk=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([1.6, 1])

    # 2. Monthly Fuel Cost Trend
    with col_chart1:
        st.markdown(
            '<div class="section-header">แนวโน้มค่าใช้จ่ายน้ำมันรายเดือน (Monthly Fuel Cost Trend)</div>',
            unsafe_allow_html=True,
        )

        df_fuel_trend = run_query(f"""
            SELECT d.month_name, d.month, SUM(f.total_cost) as monthly_fuel_cost
            FROM fact_fuel f
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY d.month_name, d.month
            ORDER BY d.month
        """)

        if not df_fuel_trend.empty:
            fig_fuel = px.line(
                df_fuel_trend,
                x="month_name",
                y="monthly_fuel_cost",
                markers=True,
                color_discrete_sequence=["#DB1A1A"],
                labels={
                    "month_name": "เดือน",
                    "monthly_fuel_cost": "ค่าน้ำมัน (฿)",
                },
            )
            fig_fuel.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0),
            )
            st.plotly_chart(fig_fuel, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลค่าใช้จ่ายน้ำมันในช่วงเวลาที่เลือก")

    # 3. On-Time Ratio
    with col_chart2:
        st.markdown(
            '<div class="section-header">สัดส่วนการส่งตรงเวลา (On-Time Ratio)</div>',
            unsafe_allow_html=True,
        )
        df_ontime = run_query(f"""
            SELECT
                CASE WHEN f.is_on_time THEN 'ตรงเวลา (On Time)' ELSE 'ล่าช้า (Late)' END as status,
                COUNT(*) as count
            FROM fact_delivery f
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY f.is_on_time
        """)

        if not df_ontime.empty:
            fig_pie = px.pie(
                df_ontime,
                names="status",
                values="count",
                hole=0,
                color="status",
                color_discrete_map={
                    "ตรงเวลา (On Time)": "#8CC7C4",
                    "ล่าช้า (Late)": "#DB1A1A",
                },
            )
            fig_pie.update_traces(
                textposition="inside", textinfo="percent+label"
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0),
            )
            st.plotly_chart(fig_pie, use_container_width=True)


# =========================================================
# PAGE 2 — REVENUE ANALYSIS & TOP MONTH BREAKDOWN
# =========================================================
elif menu == "💰 การวิเคราะห์รายได้และพฤติกรรมลูกค้า":
    st.title("🔍 วิเคราะห์เดือนที่สร้างรายได้สูงสุด (Top Revenue Month Breakdown)")
    st.caption("เจาะลึกข้อมูลรายได้เชิงเปรียบเทียบตามปีและเดือน พร้อมสถิติการจัดส่ง")
    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 1. Dynamic Filters (ปี และ เดือน ที่มีข้อมูลจริงใน DB)
    # ---------------------------------------------------------
    st.markdown(
        '<div class="section-header">🔍 ตัวกรองการวิเคราะห์รายได้ (Revenue Filters)</div>',
        unsafe_allow_html=True,
    )
    col_p2_1, col_p2_2 = st.columns(2)

    with col_p2_1:
        # ดึงรายชื่อปีจาก fact_loads และ dim_date
        df_rev_years = run_query("""
            SELECT DISTINCT d.year
            FROM fact_loads f
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE d.year IS NOT NULL
            ORDER BY d.year DESC
        """)
        rev_years_list = (
            df_rev_years["year"].astype(str).tolist() if not df_rev_years.empty else []
        )
        
        # เพิ่มตัวเลือก "ทั้งหมด" ไว้หน้าสุด
        rev_years_list.insert(0, "ทั้งหมด")
        sel_rev_year = st.selectbox("เลือกปี (year)", rev_years_list, key="p2_year_filter")

    with col_p2_2:
        # ดึงรายชื่อเดือนตามปีที่เลือก
        if sel_rev_year == "ทั้งหมด" or not sel_rev_year:
            year_where_clause = ""
        else:
            year_where_clause = f"WHERE d.year = {sel_rev_year}"

        df_rev_months = run_query(f"""
            SELECT DISTINCT d.month_name, d.month
            FROM fact_loads f
            JOIN dim_date d ON f.date_key = d.date_key
            {year_where_clause}
            ORDER BY d.month
        """)
        rev_months_list = (
            df_rev_months["month_name"].tolist() if not df_rev_months.empty else []
        )

        # เพิ่มตัวเลือก "ทั้งหมด" ไว้หน้าสุด
        rev_months_list.insert(0, "ทั้งหมด")
        sel_rev_month = st.selectbox("เลือกเดือน (month)", rev_months_list, key="p2_month_filter")

    # สร้างเงื่อนไข SQL ตามตัวกรองที่เลือก
    if sel_rev_year == "ทั้งหมด":
        p2_year_clause = ""
    elif sel_rev_year:
        p2_year_clause = f"AND d.year = {sel_rev_year}"
    else:
        p2_year_clause = "AND 1=0"

    p2_month_clause = (
        "" if sel_rev_month == "ทั้งหมด" else f"AND d.month_name = '{sel_rev_month}'"
    )
    p2_filter_clause = f"{p2_year_clause} {p2_month_clause}"

    # ---------------------------------------------------------
    # 2. Key Performance Indicators (KPIs)
    # ---------------------------------------------------------
    # 2.1 คำนวณรายได้รวมจาก fact_loads (เหมือนหน้า 1)
    rev_res_p2 = run_query(f"""
        SELECT COALESCE(SUM(f.revenue), 0) AS total_revenue
        FROM fact_loads f
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {p2_filter_clause}
    """)
    total_rev_p2 = rev_res_p2.iloc[0]["total_revenue"] if not rev_res_p2.empty else 0.0

    # 2.2 คำนวณจำนวนเที่ยวจัดส่งจาก fact_delivery
    del_res_p2 = run_query(f"""
        SELECT COUNT(*) AS total_jobs
        FROM fact_delivery f
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {p2_filter_clause}
    """)
    total_jobs_p2 = del_res_p2.iloc[0]["total_jobs"] if not del_res_p2.empty else 0

    # 2.3 รายได้เฉลี่ยต่อเที่ยว
    avg_rev_per_job = total_rev_p2 / total_jobs_p2 if total_jobs_p2 > 0 else 0.0

    k1, k2, k3 = st.columns(3)
    with k1:
        render_kpi_card(
            "รายได้รวมตามเงื่อนไข",
            f"฿{total_rev_p2:,.2f}",
            f"ปี {sel_rev_year or '-'} ({sel_rev_month})",
        )
    with k2:
        render_kpi_card(
            "จำนวนเที่ยวจัดส่งรวม",
            f"{total_jobs_p2:,} เที่ยว",
            "Total Deliveries",
        )
    with k3:
        render_kpi_card(
            "รายได้เฉลี่ยต่อเที่ยว",
            f"฿{avg_rev_per_job:,.2f}",
            "Avg Revenue / Delivery",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. Visualizations & Breakdown
    # ---------------------------------------------------------
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown(
            f'<div class="section-header">📊 แนวโน้มรายได้รายเดือน (ปี: {sel_rev_year or "-"})</div>',
            unsafe_allow_html=True,
        )
        
        # ปรับการสร้างเงื่อนไข SQL สำหรับกราฟแท่งรายเดือนให้รองรับ "ทั้งหมด (All Years)"
        df_monthly_rev = run_query(f"""
            SELECT d.month, d.month_name, SUM(f.revenue) as monthly_revenue
            FROM fact_loads f
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {p2_year_clause}
            GROUP BY d.month, d.month_name
            ORDER BY d.month
        """)

        if not df_monthly_rev.empty:
            # กราฟแท่งใช้สีแดงสด #DB1A1A
            fig_m_rev = px.bar(
                df_monthly_rev,
                x="month_name",
                y="monthly_revenue",
                text_auto=",sf",
                color_discrete_sequence=["#DB1A1A"],
                labels={"month_name": "เดือน", "monthly_revenue": "รายได้รวม (฿)"},
            )
            fig_m_rev.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_m_rev, width="stretch")
        else:
            st.info("ไม่พบข้อมูลรายได้รายเดือนสำหรับเงื่อนไขที่เลือก")

    with col_chart2:
        st.markdown(
            f'<div class="section-header">🏆 5 อันดับสถานที่/คลังสินค้าที่มีการจัดส่งสูงสุด ({sel_rev_month})</div>',
            unsafe_allow_html=True,
        )
        # สืบค้นสถานที่ส่งจาก dim_facilities และ fact_delivery
        df_top_facilities = run_query(f"""
            SELECT fac.facility_name, COUNT(f.delivery_event_key) as total_trips
            FROM fact_delivery f
            JOIN dim_facilities fac ON f.facility_key = fac.facility_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {p2_filter_clause}
            GROUP BY fac.facility_name
            ORDER BY total_trips DESC
            LIMIT 5
        """)
        
        if not df_top_facilities.empty:
            # กราฟวงกลมใช้โทนสี RdBu
            fig_goods = px.pie(
                df_top_facilities,
                names="facility_name",
                values="total_trips",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu,
            )
            fig_goods.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_goods, width="stretch")
        else:
            st.info("ไม่พบข้อมูลสถานที่จัดส่งตามเงื่อนไขที่เลือก")
# =========================================================
# PAGE 3 — FLEET MANAGEMENT & MAINTENANCE
# =========================================================
elif menu == "🚛 การบริหารจัดการกองรถและการซ่อมบำรุง":
    st.title("🚛 การบริหารจัดการกองรถและการซ่อมบำรุง")
    st.caption("ติดตามการใช้งานรถบรรทุก สถิติการวิ่ง และต้นทุนการบำรุงรักษา")
    st.markdown("<br>", unsafe_allow_html=True)

    # Local Year & Month Filter
    st.markdown(
        '<div class="section-header">ตัวกรองเวลาค่าซ่อมบำรุง (Maintenance Filter)</div>',
        unsafe_allow_html=True,
    )
    col_f1, col_f2 = st.columns(2)

    df_maint_years = run_query(
        "SELECT DISTINCT d.year FROM fact_maintenance f JOIN dim_date d ON f.date_key = d.date_key WHERE d.year IS NOT NULL ORDER BY d.year DESC"
    )
    maint_years = (
        df_maint_years["year"].tolist() if not df_maint_years.empty else []
    )
    maint_years.insert(0, "ทั้งหมด")

    with col_f1:
        sel_maint_year = st.selectbox("เลือกปี (Year)", maint_years, key="m_year")

    m_year_clause = (
        "" if sel_maint_year == "ทั้งหมด" else f"AND d.year = {sel_maint_year}"
    )

    # ดึงเฉพาะเดือนที่มีข้อมูลอยู่จริงตามปีที่เลือก
    with col_f2:
        df_maint_months = run_query(f"""
            SELECT DISTINCT d.month_name, d.month
            FROM fact_maintenance f
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {m_year_clause}
            ORDER BY d.month
        """)
        months_list = (
            df_maint_months["month_name"].tolist()
            if not df_maint_months.empty
            else []
        )
        months_list.insert(0, "ทั้งหมด")
        sel_maint_month = st.selectbox(
            "เลือกเดือน (Month)", months_list, key="m_month"
        )

    m_month_clause = (
        ""
        if sel_maint_month == "ทั้งหมด"
        else f"AND d.month_name = '{sel_maint_month}'"
    )

    # KPI Calculation พร้อมการป้องกัน NaN
    maint_cost_res = run_query(f"""
        SELECT COALESCE(SUM(f.total_cost), 0)
        FROM fact_maintenance f
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {m_year_clause} {m_month_clause}
    """)
    maint_cost_val = (
        maint_cost_res.iloc[0, 0] if not maint_cost_res.empty else 0
    )

    m1, m2, m3 = st.columns(3)
    with m1:
        render_kpi_card(
            "ค่าใช้จ่ายการซ่อมบำรุงรวม",
            f"฿{maint_cost_val:,.2f}",
            "Total Maintenance Cost",
            is_risk=True,
        )
    with m2:
        render_kpi_card(
            "ปีที่เลือก (Selected Year)",
            str(sel_maint_year),
            "Maintenance Filter",
        )
    with m3:
        render_kpi_card(
            "เดือนที่เลือก (Selected Month)",
            str(sel_maint_month),
            "Maintenance Filter",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # กราฟค่าซ่อมบำรุงรายเดือนและรายปี
    # ---------------------------------------------------------
    col_maint_g1, col_maint_g2 = st.columns(2)

    with col_maint_g1:
        st.markdown(
            f'<div class="section-header">ค่าใช้จ่ายการซ่อมบำรุงรวมรายเดือน (ปี {sel_maint_year})</div>',
            unsafe_allow_html=True,
        )
        df_maint_monthly = run_query(f"""
            SELECT d.month, d.month_name, SUM(f.total_cost) as total_maint_cost
            FROM fact_maintenance f
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {m_year_clause}
            GROUP BY d.month, d.month_name
            ORDER BY d.month
        """)
        if not df_maint_monthly.empty:
            fig_m_bar = px.bar(
                df_maint_monthly,
                x="month_name",
                y="total_maint_cost",
                text_auto=".3s",
                color_discrete_sequence=["#DB1A1A"],
                labels={"month_name": "เดือน", "total_maint_cost": "ค่าซ่อมบำรุง (฿)"}
            )
            fig_m_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_m_bar, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลค่าซ่อมบำรุงรายเดือนตามเงื่อนไขที่เลือก")

    with col_maint_g2:
        st.markdown(
            '<div class="section-header">เปรียบเทียบค่าใช้จ่ายการซ่อมบำรุงรวมแต่ละปี (Yearly Trend)</div>',
            unsafe_allow_html=True,
        )
        df_maint_yearly = run_query("""
            SELECT d.year::VARCHAR as year, SUM(f.total_cost) as total_maint_cost
            FROM fact_maintenance f
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE d.year IS NOT NULL
            GROUP BY d.year
            ORDER BY d.year
        """)
        if not df_maint_yearly.empty:
            fig_m_line = px.line(
                df_maint_yearly,
                x="year",
                y="total_maint_cost",
                markers=True,
                color_discrete_sequence=["#1a1d20"],
                labels={"year": "ปี", "total_maint_cost": "ค่าซ่อมบำรุงรวม (฿)"}
            )
            fig_m_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_m_line, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลค่าซ่อมบำรุงรายปี")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # [เพิ่มเติม] KPI SUMMARY BOXES ก่อนเข้าสู่ส่วน TOP 10
    # ---------------------------------------------------------
    # 1. หาอันดับ 1 รถบรรทุกซ่อมบำรุงสูงสุด
    df_top1_maint = run_query(f"""
        SELECT t.Truck_ID, SUM(f.total_cost) as total_cost
        FROM fact_maintenance f
        JOIN dim_trucks t ON f.truck_key = t.truck_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {m_year_clause} {m_month_clause}
        GROUP BY t.Truck_ID ORDER BY total_cost DESC LIMIT 1
    """)
    top1_maint_truck = df_top1_maint.iloc[0]["Truck_ID"] if not df_top1_maint.empty else "-"
    top1_maint_val = df_top1_maint.iloc[0]["total_cost"] if not df_top1_maint.empty else 0

    # 2. หาอันดับ 1 รถบรรทุกวิ่งเที่ยวสูงสุด
    df_top1_truck_trip = run_query(f"""
        SELECT t.Truck_ID, COUNT(f.trip_key) as total_trips
        FROM fact_trips f
        JOIN dim_trucks t ON f.truck_key = t.truck_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY t.Truck_ID ORDER BY total_trips DESC LIMIT 1
    """)
    top1_trip_truck = df_top1_truck_trip.iloc[0]["Truck_ID"] if not df_top1_truck_trip.empty else "-"
    top1_trip_truck_val = df_top1_truck_trip.iloc[0]["total_trips"] if not df_top1_truck_trip.empty else 0

    # 3. หาอันดับ 1 พนักงานขับรถวิ่งเที่ยวสูงสุด
    df_top1_driver_trip = run_query(f"""
        SELECT dr.full_name, COUNT(f.trip_key) as total_trips
        FROM fact_trips f
        JOIN dim_drivers dr ON f.driver_key = dr.driver_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY dr.full_name ORDER BY total_trips DESC LIMIT 1
    """)
    top1_driver_name = df_top1_driver_trip.iloc[0]["full_name"] if not df_top1_driver_trip.empty else "-"
    top1_driver_val = df_top1_driver_trip.iloc[0]["total_trips"] if not df_top1_driver_trip.empty else 0

    # แสดง KPI Cards ทั้ง 3 อันดับสูงสุด
    top_k1, top_k2, top_k3 = st.columns(3)
    with top_k1:
        render_kpi_card(
            "รถที่มีค่าซ่อมบำรุงสูงสุด",
            f"{top1_maint_truck}",
            f"฿{top1_maint_val:,.2f}",
            is_risk=True
        )
    with top_k2:
        render_kpi_card(
            "รถที่มีการใช้งานสูงสุด",
            f"{top1_trip_truck}",
            f"{top1_trip_truck_val:,} เที่ยว"
        )
    with top_k3:
        render_kpi_card(
            "พนักงานขับรถดีเด่น (เที่ยวสูงสุด)",
            f"{top1_driver_name}",
            f"{top1_driver_val:,} เที่ยว"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Top 10 Maintenance Cost
    # ---------------------------------------------------------
    st.markdown(
        '<div class="section-header">10 อันดับ รถบรรทุกที่มีค่าซ่อมบำรุงสูงสุด (Top 10 Maintenance Cost)</div>',
        unsafe_allow_html=True,
    )
    df_truck_maint = run_query(f"""
        SELECT t.Truck_ID, SUM(f.total_cost) as total_maint_cost
        FROM fact_maintenance f
        JOIN dim_trucks t ON f.truck_key = t.truck_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {m_year_clause} {m_month_clause}
        GROUP BY t.Truck_ID
        ORDER BY total_maint_cost DESC
        LIMIT 10
    """)

    if not df_truck_maint.empty:
        fig_truck_m = px.bar(
            df_truck_maint,
            x="Truck_ID",
            y="total_maint_cost",
            text_auto=".3s",
            color_discrete_sequence=["#DB1A1A"],
            labels={
                "total_maint_cost": "ค่าซ่อมบำรุง (฿)",
                "Truck_ID": "รหัสรถบรรทุก",
            },
        )
        fig_truck_m.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_truck_m, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลค่าซ่อมบำรุงตามตัวกรองที่เลือก")

    # Fleet & Driver Analysis Section
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="section-header">10 อันดับ รถบรรทุกที่มีการใช้งานวิ่งเที่ยวสูงสุด (Trips)</div>',
            unsafe_allow_html=True,
        )
        df_truck_trips = run_query(f"""
            SELECT t.Truck_ID, COUNT(f.trip_key) as total_trips
            FROM fact_trips f
            JOIN dim_trucks t ON f.truck_key = t.truck_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY t.Truck_ID ORDER BY total_trips DESC LIMIT 10
        """)
        fig_truck_t = px.bar(
            df_truck_trips,
            x="Truck_ID",
            y="total_trips",
            text_auto=True,
            color_discrete_sequence=["#8CC7C4"],
            labels={"Truck_ID": "รหัสรถบรรทุก", "total_trips": "จำนวน Trips"},
        )
        fig_truck_t.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_truck_t, use_container_width=True)

    with col2:
        st.markdown(
            '<div class="section-header">พนักงานขับรถที่มีสถิติการวิ่งสูงสุด 10 อันดับแรก</div>',
            unsafe_allow_html=True,
        )
        df_driver = run_query(f"""
            SELECT dr.full_name, COUNT(f.trip_key) as total_trips
            FROM fact_trips f
            JOIN dim_drivers dr ON f.driver_key = dr.driver_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY dr.full_name ORDER BY total_trips DESC LIMIT 10
        """)
        fig_drv = px.bar(
            df_driver,
            x="total_trips",
            y="full_name",
            orientation="h",
            text_auto=True,
            color_discrete_sequence=["#1a1d20"],
            labels={
                "total_trips": "จำนวน Trips",
                "full_name": "ชื่อพนักงานขับรถ",
            },
        )
        fig_drv.update_layout(
            yaxis={"categoryorder": "total ascending"},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_drv, use_container_width=True)

# =========================================================
# PAGE 4 — DELIVERY PERFORMANCE
# =========================================================
elif menu == "⏱️ ประสิทธิภาพการจัดส่งและความตรงต่อเวลา":
    st.title("⏱️ ประสิทธิภาพการจัดส่งและความตรงต่อเวลา")
    st.caption("วิเคราะห์คลังสินค้า ความล่าช้า และผลต่างระหว่างเวลาจริงเทียบกับแผน")
    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # [ข้อ 3] Filter รายปี / รายเดือน สำหรับหน้าประสิทธิภาพการจัดส่ง
    # ---------------------------------------------------------
    st.markdown(
        '<div class="section-header">🔍 ตัวกรองประสิทธิภาพการจัดส่ง (Delivery Performance Filter)</div>',
        unsafe_allow_html=True,
    )
    col_del_f1, col_del_f2 = st.columns(2)

    df_del_years = run_query("SELECT DISTINCT d.year FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key WHERE d.year IS NOT NULL ORDER BY d.year DESC")
    del_years_list = df_del_years["year"].tolist() if not df_del_years.empty else []
    del_years_list.insert(0, "ทั้งหมด")

    with col_del_f1:
        sel_del_year = st.selectbox("เลือกปี (Delivery Year)", del_years_list, key="del_year_filter")

    del_year_sql = "" if sel_del_year == "ทั้งหมด" else f"AND d.year = {sel_del_year}"

    with col_del_f2:
        df_del_months = run_query(f"""
            SELECT DISTINCT d.month_name, d.month 
            FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key 
            WHERE 1=1 {del_year_sql} ORDER BY d.month
        """)
        del_months_list = df_del_months["month_name"].tolist() if not df_del_months.empty else []
        del_months_list.insert(0, "ทั้งหมด")
        sel_del_month = st.selectbox("เลือกเดือน (Delivery Month)", del_months_list, key="del_month_filter")

    del_month_sql = "" if sel_del_month == "ทั้งหมด" else f"AND d.month_name = '{sel_del_month}'"
    del_combined_clause = f"{del_year_sql} {del_month_sql}"

    st.markdown("<br>", unsafe_allow_html=True)

    # Pie Chart On-Time Ratio ตาม Filter
    st.markdown(
        '<div class="section-header">อัตราการล่าช้าเทียบกับส่งตรงเวลา (On-Time vs Delayed Ratio)</div>',
        unsafe_allow_html=True,
    )

    df_delivery_pie = run_query(f"""
        SELECT
            CASE WHEN f.is_on_time THEN 'ตรงเวลา (On Time)' ELSE 'ล่าช้า (Delayed)' END as status,
            COUNT(*) as count
        FROM fact_delivery f
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {del_combined_clause}
        GROUP BY f.is_on_time
    """)

    if not df_delivery_pie.empty:
        fig_del_pie = px.pie(
            df_delivery_pie,
            names="status",
            values="count",
            hole=0,
            color="status",
            color_discrete_map={
                "ตรงเวลา (On Time)": "#8CC7C4",
                "ล่าช้า (Delayed)": "#DB1A1A",
            },
        )
        fig_del_pie.update_traces(
            textposition="inside", textinfo="percent+label"
        )
        fig_del_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_del_pie, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลการจัดส่งตามตัวกรองที่เลือก")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # [ข้อ 3] เลือกดู Facilities แบบ "ล่าช้า" หรือ "ตรงเวลา"
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="section-header">คลังสินค้า/สถานที่ (Facilities Analysis)</div>',
            unsafe_allow_html=True,
        )
        status_target = st.selectbox(
            "เลือกสถานะการจัดส่งที่ต้องการดู (Facility):",
            ["เคสจัดส่งล่าช้า (Delayed)", "เคสจัดส่งตรงเวลา (On Time)"],
            key="fac_status_select"
        )
        is_on_time_target = "True" if "ตรงเวลา" in status_target else "False"
        bar_color = "#8CC7C4" if "ตรงเวลา" in status_target else "#DB1A1A"

        df_fac_perf = run_query(f"""
            SELECT fac.facility_name, COUNT(*) as delivery_count
            FROM fact_delivery f
            JOIN dim_facilities fac ON f.facility_key = fac.facility_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE f.is_on_time = {is_on_time_target} {del_combined_clause}
            GROUP BY fac.facility_name ORDER BY delivery_count DESC LIMIT 10
        """)
        if not df_fac_perf.empty:
            fig_fac = px.bar(
                df_fac_perf,
                x="delivery_count",
                y="facility_name",
                orientation="h",
                text_auto=True,
                color_discrete_sequence=[bar_color],
                labels={
                    "delivery_count": "จำนวนเคส",
                    "facility_name": "ชื่อคลังสินค้า",
                },
            )
            fig_fac.update_layout(
                yaxis={"categoryorder": "total ascending"},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_fac, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลคลังสินค้าตามเงื่อนไข")

    
    # ---------------------------------------------------------
    # [ข้อ 3] เพิ่มอันดับรถบรรทุกที่มีการจัดส่งล่าช้า/ตรงต่อเวลา พร้อมแสดงชื่ออันดับ 1 ข้างๆ Selectbox
    # ---------------------------------------------------------
    st.markdown(
        '<div class="section-header">🚛 อันดับรถบรรทุกตามประสิทธิภาพการส่งมอบ (Truck Performance Ranking)</div>',
        unsafe_allow_html=True,
    )
    col_tr1, col_tr2 = st.columns([1.2, 2])

    with col_tr1:
        truck_status_sel = st.selectbox(
            "เลือกประเภทสถิติรถบรรทุก:",
            ["จัดส่งล่าช้า (Delayed)", "จัดส่งตรงเวลา (On Time)"],
            key="truck_rank_status"
        )
        truck_on_time_flag = "True" if "ตรงเวลา" in truck_status_sel else "False"

        # Query อันดับ 1
        df_top_truck = run_query(f"""
            SELECT t.Truck_ID, COUNT(*) as status_count
            FROM fact_delivery f
            JOIN dim_trucks t ON f.truck_key = t.truck_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE f.is_on_time = {truck_on_time_flag} {del_combined_clause}
            GROUP BY t.Truck_ID
            ORDER BY status_count DESC
            LIMIT 1
        """)

        top_truck_name = df_top_truck.iloc[0]["Truck_ID"] if not df_top_truck.empty else "N/A"
        top_truck_cnt = df_top_truck.iloc[0]["status_count"] if not df_top_truck.empty else 0

        # แสดงกล่องข้างๆ ตัวเลือก
        render_kpi_card(
            f"🏆 รถบรรทุกอันดับ 1 ({truck_status_sel.split()[0]})",
            f"Truck: {top_truck_name}",
            f"จำนวน: {top_truck_cnt:,} เที่ยว",
            is_risk=("ล่าช้า" in truck_status_sel)
        )

    with col_tr2:
        df_truck_rank = run_query(f"""
            SELECT t.Truck_ID, COUNT(*) as status_count
            FROM fact_delivery f
            JOIN dim_trucks t ON f.truck_key = t.truck_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE f.is_on_time = {truck_on_time_flag} {del_combined_clause}
            GROUP BY t.Truck_ID
            ORDER BY status_count DESC
            LIMIT 10
        """)
        if not df_truck_rank.empty:
            t_bar_color = "#8CC7C4" if "ตรงเวลา" in truck_status_sel else "#DB1A1A"
            fig_trk_rank = px.bar(
                df_truck_rank,
                x="Truck_ID",
                y="status_count",
                text_auto=True,
                color_discrete_sequence=[t_bar_color],
                labels={"Truck_ID": "รหัสรถบรรทุก", "status_count": "จำนวนเที่ยว"},
                title=f"10 อันดับรถบรรทุกที่มีเคส {truck_status_sel}"
            )
            fig_trk_rank.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_trk_rank, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลสถิติรถบรรทุก")


# =========================================================
# PAGE 5 — FUEL & SAFETY ANALYSIS
# =========================================================
elif menu == "⛽ ตัวชี้วัดการใช้น้ำมันและความปลอดภัยในการขนส่ง":
    st.title("⛽ ตัวชี้วัดการใช้น้ำมันและความปลอดภัยในการขนส่ง")
    st.caption("ตรวจสอบค่าใช้จ่ายน้ำมันเชื้อเพลิงและอุบัติเหตุที่เกิดขึ้น")
    st.markdown("<br>", unsafe_allow_html=True)

    # Dictionary สำหรับแปลงตัวเลขเป็นชื่อเดือนภาษาไทย
    month_dict = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    # ---------------------------------------------------------
    # FILTER BAR (แสดงเฉพาะปี/เดือนที่มีข้อมูลจริง)
    # ---------------------------------------------------------
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        # ดึงเฉพาะปีที่มีข้อมูลใน fact_fuel หรือ fact_safety_incidents
        df_opt_years = run_query("""
            SELECT DISTINCT d.year 
            FROM dim_date d
            WHERE d.year IS NOT NULL 
              AND (
                  d.date_key IN (SELECT date_key FROM fact_fuel) 
               OR d.date_key IN (SELECT date_key FROM fact_safety_incidents)
              )
            ORDER BY d.year DESC
        """)
        years_list = ["ทั้งหมด"] + [str(y) for y in df_opt_years["year"].tolist()] if not df_opt_years.empty else ["ทั้งหมด"]
        sel_year = st.selectbox("📅 เลือกปี (Year)", years_list, key="p5_year_select")

    with col_f2:
        # ดึงเฉพาะเดือนที่มีข้อมูลตามปีที่เลือก
        year_filter_sql = f"AND d.year = {sel_year}" if sel_year != "ทั้งหมด" else ""
        df_opt_months = run_query(f"""
            SELECT DISTINCT d.month 
            FROM dim_date d
            WHERE d.month IS NOT NULL {year_filter_sql}
              AND (
                  d.date_key IN (SELECT date_key FROM fact_fuel) 
               OR d.date_key IN (SELECT date_key FROM fact_safety_incidents)
              )
            ORDER BY d.month
        """)
        
        # แสดงชื่อเดือนภาษาไทยใน Selectbox
        months_raw = df_opt_months["month"].tolist() if not df_opt_months.empty else []
        month_options = ["ทั้งหมด"] + [month_dict.get(int(m), str(m)) for m in months_raw]
        sel_month_name = st.selectbox("📆 เลือกเดือน (Month)", month_options, key="p5_month_select")

        # แปลงชื่อเดือนกลับเป็นตัวเลขเพื่อใช้ในการ Query SQL
        sel_month_num = None
        if sel_month_name != "ทั้งหมด":
            for k, v in month_dict.items():
                if v == sel_month_name:
                    sel_month_num = k
                    break

    # สร้าง WHERE Clause จากตัวกรองที่เลือก
    p5_y_clause = f"AND d.year = {sel_year}" if sel_year != "ทั้งหมด" else ""
    p5_m_clause = f"AND d.month = {sel_month_num}" if sel_month_num is not None else ""

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 1. QUERY DATA FOR KPI CARDS
    # ---------------------------------------------------------
    # Top Fuel Truck
    df_top_fuel_truck = run_query(f"""
        SELECT t.Truck_ID, SUM(f.total_cost) as total_fuel_cost
        FROM fact_fuel f
        JOIN dim_trucks t ON f.truck_key = t.truck_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {p5_y_clause} {p5_m_clause}
        GROUP BY t.Truck_ID ORDER BY total_fuel_cost DESC LIMIT 1
    """)
    top_truck_id = df_top_fuel_truck.iloc[0]["Truck_ID"] if not df_top_fuel_truck.empty else "N/A"
    top_truck_cost = df_top_fuel_truck.iloc[0]["total_fuel_cost"] if not df_top_fuel_truck.empty else 0

    # Total Fuel Cost
    tot_fuel_res = run_query(f"SELECT COALESCE(SUM(f.total_cost), 0) FROM fact_fuel f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {p5_y_clause} {p5_m_clause}")
    tot_fuel_val = tot_fuel_res.iloc[0, 0] if not tot_fuel_res.empty else 0

    # Top Incident Type
    df_top_inc_type = run_query(f"""
        SELECT f.incident_type, COUNT(*) as count
        FROM fact_safety_incidents f
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {p5_y_clause} {p5_m_clause}
        GROUP BY f.incident_type ORDER BY count DESC LIMIT 1
    """)
    top_inc_name = df_top_inc_type.iloc[0]["incident_type"] if not df_top_inc_type.empty else "ไม่มีอุบัติเหตุ"
    top_inc_count = df_top_inc_type.iloc[0]["count"] if not df_top_inc_type.empty else 0

    # Top Driver with Most Incidents
    df_top_driver_inc = run_query(f"""
        SELECT COALESCE(dr.driver_id, 'ไม่ระบุ') as driver_id, COUNT(*) as count
        FROM fact_safety_incidents f
        LEFT JOIN dim_drivers dr ON f.driver_key = dr.driver_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {p5_y_clause} {p5_m_clause}
        GROUP BY dr.driver_id ORDER BY count DESC LIMIT 1
    """)
    top_driver_id = df_top_driver_inc.iloc[0]["driver_id"] if not df_top_driver_inc.empty else "N/A"
    top_driver_count = df_top_driver_inc.iloc[0]["count"] if not df_top_driver_inc.empty else 0

    # Render KPI Cards (จัดแบ่ง 2 แถว แถวละ 2 Cards)
    col_fkpi1, col_fkpi2 = st.columns(2)
    with col_fkpi1:
        render_kpi_card("ค่าใช้จ่ายน้ำมันรวม (Total Fuel Cost)", f"฿{tot_fuel_val:,.2f}", "Fuel Expense", is_risk=True)
    with col_fkpi2:
        render_kpi_card("รถบรรทุกที่มีค่าน้ำมันสูงสุด", f"Truck ID: {top_truck_id}", f"Fuel Cost: ฿{top_truck_cost:,.2f}", is_risk=True)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    col_fkpi3, col_fkpi4 = st.columns(2)
    with col_fkpi3:
        render_kpi_card("ประเภทอุบัติเหตุที่พบบ่อยที่สุด", f"{top_inc_name}", f"จำนวน: {top_inc_count:,} ครั้ง", is_risk=True)
    with col_fkpi4:
        render_kpi_card("คนขับที่เกิดอุบัติเหตุสูงสุด", f"Driver: {top_driver_id}", f"จำนวน: {top_driver_count:,} ครั้ง", is_risk=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. FUEL COST RANKING
    # ---------------------------------------------------------
    st.markdown('<div class="section-header">อันดับค่าใช้จ่ายน้ำมันแบ่งตามรถบรรทุก (Top 10 Fuel Cost by Truck)</div>', unsafe_allow_html=True)
    df_truck_fuel_rank = run_query(f"""
        SELECT t.Truck_ID, SUM(f.total_cost) as total_fuel_cost
        FROM fact_fuel f
        JOIN dim_trucks t ON f.truck_key = t.truck_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {p5_y_clause} {p5_m_clause}
        GROUP BY t.Truck_ID ORDER BY total_fuel_cost DESC LIMIT 10
    """)

    if not df_truck_fuel_rank.empty:
        fig_fuel_rank = px.bar(
            df_truck_fuel_rank, x="Truck_ID", y="total_fuel_cost", text_auto=".3s",
            color_discrete_sequence=["#DB1A1A"], labels={"total_fuel_cost": "ค่าน้ำมัน (฿)", "Truck_ID": "รหัสรถบรรทุก"}
        )
        fig_fuel_rank.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fuel_rank, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลค่าน้ำมันในช่วงเวลาที่เลือก")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. YEARLY TRENDS SECTION
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">ค่าใช้จ่ายน้ำมันเชื้อเพลิงรวมในแต่ละปี</div>', unsafe_allow_html=True)
        df_fuel_y = run_query("SELECT d.year::VARCHAR as year, SUM(f.total_cost) as fuel_cost FROM fact_fuel f JOIN dim_date d ON f.date_key = d.date_key GROUP BY d.year ORDER BY d.year")
        if not df_fuel_y.empty:
            fig_fy = px.bar(df_fuel_y, x="year", y="fuel_cost", text_auto=".3s", color_discrete_sequence=["#DB1A1A"], labels={"year": "ปี", "fuel_cost": "ค่าน้ำมัน (฿)"})
            fig_fy.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_fy, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">จำนวนอุบัติเหตุและความปลอดภัย (Incidents) ในแต่ละปี</div>', unsafe_allow_html=True)
        df_inc_y = run_query("SELECT d.year::VARCHAR as year, COUNT(*) as incident_count FROM fact_safety_incidents f JOIN dim_date d ON f.date_key = d.date_key GROUP BY d.year ORDER BY d.year")
        if not df_inc_y.empty:
            fig_iy = px.bar(df_inc_y, x="year", y="incident_count", text_auto=True, color_discrete_sequence=["#1a1d20"], labels={"year": "ปี", "incident_count": "จำนวนครั้ง"})
            fig_iy.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_iy, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 4. INCIDENT ANALYSIS SECTION
    # ---------------------------------------------------------
    col_inc1, col_inc2 = st.columns(2)
    with col_inc1:
        st.markdown('<div class="section-header">สัดส่วนประเภทอุบัติเหตุ (Incident Types)</div>', unsafe_allow_html=True)
        df_inc_type = run_query(f"SELECT f.incident_type, COUNT(*) as count FROM fact_safety_incidents f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {p5_y_clause} {p5_m_clause} GROUP BY f.incident_type ORDER BY count DESC")
        if not df_inc_type.empty:
            fig_it = px.pie(df_inc_type, names="incident_type", values="count", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            fig_it.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_it, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลสัดส่วนอุบัติเหตุในช่วงเวลาที่เลือก")

    with col_inc2:
        st.markdown('<div class="section-header">Top 10 รถบรรทุกที่เกิดอุบัติเหตุบ่อยที่สุด</div>', unsafe_allow_html=True)
        df_inc_truck_rank = run_query(f"SELECT t.Truck_ID, COUNT(*) as incident_count FROM fact_safety_incidents f JOIN dim_trucks t ON f.truck_key = t.truck_key JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {p5_y_clause} {p5_m_clause} GROUP BY t.Truck_ID ORDER BY incident_count DESC LIMIT 10")
        if not df_inc_truck_rank.empty:
            fig_inc_truck = px.bar(df_inc_truck_rank, x="Truck_ID", y="incident_count", text_auto=True, color_discrete_sequence=["#DB1A1A"], labels={"Truck_ID": "รหัสรถบรรทุก", "incident_count": "จำนวนครั้งที่เกิดอุบัติเหตุ"})
            fig_inc_truck.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_inc_truck, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลอุบัติเหตุของรถบรรทุกในช่วงเวลาที่เลือก")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 5. TOP DRIVERS BY INCIDENTS SECTION (ใช้โทนสีแดงเข้ม-ส้มอิฐตามรูปภาพ ตัดสีครีมออก)
    # ---------------------------------------------------------
    st.markdown('<div class="section-header">อันดับคนขับรถที่เกิดอุบัติเหตุมากที่สุด (Top Drivers by Incidents)</div>', unsafe_allow_html=True)
    
    df_driver_inc = run_query(f"""
        SELECT 
            COALESCE(dr.driver_id, 'ไม่ระบุ') as driver_id, 
            COUNT(*) as incident_count
        FROM fact_safety_incidents f
        JOIN dim_date d ON f.date_key = d.date_key
        LEFT JOIN dim_drivers dr ON f.driver_key = dr.driver_key
        WHERE 1=1 {p5_y_clause} {p5_m_clause}
        GROUP BY dr.driver_id
        ORDER BY incident_count DESC
        LIMIT 10
    """)

    if not df_driver_inc.empty and df_driver_inc["incident_count"].sum() > 0:
        # ดึงพาเลตสีโทนแดงส้มตามภาพมาใช้งาน (px.colors.sequential.Reds_r สลับด้านเพื่อเอาสีเข้มขึ้นก่อน และตัดช่วงสีอ่อนมากๆ/สีครีมออก)
        custom_reds = px.colors.sequential.Reds_r[:6]
        
        fig_driver_inc = px.bar(
            df_driver_inc, 
            x="incident_count", 
            y="driver_id", 
            orientation="h", 
            text="incident_count",
            color="incident_count",
            color_continuous_scale=custom_reds,  # Palette สีแดงส้มอิฐเข้มตามภาพ
            labels={
                "incident_count": "จำนวนครั้งที่เกิดอุบัติเหตุ", 
                "driver_id": "รหัสคนขับ (Driver ID)"
            }
        )
        fig_driver_inc.update_layout(
            yaxis={"categoryorder": "total ascending"}, 
            coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)"
        )
        fig_driver_inc.update_traces(textposition="outside")
        st.plotly_chart(fig_driver_inc, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูลอุบัติเหตุของคนขับในช่วงเวลาที่เลือก")