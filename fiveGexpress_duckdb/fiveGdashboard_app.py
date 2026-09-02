import duckdb
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st

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
        color: #DB1A1A; 
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

# Banner Header
header_logo_url = "https://via.placeholder.com/1200x180/1a1d20/ffffff?text=5G+EXPRESS+LOGISTICS+ANALYTICS"
st.image(header_logo_url, use_container_width=True)


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
# PAGE 2 — REVENUE & CUSTOMER BEHAVIOR
# =========================================================
elif menu == "💰 การวิเคราะห์รายได้และพฤติกรรมลูกค้า":
    st.title("💰 การวิเคราะห์รายได้และพฤติกรรมลูกค้า")
    st.caption("เจาะลึกที่มารายได้เปรียบเทียบรายปี ลูกค้าหลัก เส้นทางยอดนิยม และเดือนที่ทำรายได้สูงสุด")
    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ตัวกรองเฉพาะหน้า: เลือกปีสำหรับวิเคราะห์เดือนที่รายได้สูงสุด
    # ---------------------------------------------------------
    st.markdown(
        '<div class="section-header">ตัวกรองเลือกปีเพื่อวิเคราะห์เดือนที่รายได้สูงสุด</div>',
        unsafe_allow_html=True,
    )
    df_rev_years = run_query(
        "SELECT DISTINCT d.year FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key WHERE d.year IS NOT NULL ORDER BY d.year DESC"
    )
    rev_years_list = df_rev_years["year"].tolist() if not df_rev_years.empty else [2026]
    
    selected_rev_year = st.selectbox(
        "เลือกปี (Year)", rev_years_list, key="rev_page_year_select"
    )

    # 1. ดึงข้อมูลรายได้ทุกเดือนของปีที่เลือก
    df_monthly_rev = run_query(f"""
        SELECT 
            d.month,
            d.month_name,
            SUM(f.revenue) as monthly_revenue
        FROM fact_loads f
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE d.year = {selected_rev_year}
        GROUP BY d.month, d.month_name
        ORDER BY d.month
    """)

    if not df_monthly_rev.empty:
        # หาเดือนที่รายได้สูงสุด
        top_month_row = df_monthly_rev.loc[df_monthly_rev["monthly_revenue"].idxmax()]
        top_month_name = top_month_row["month_name"]
        top_month_rev = top_month_row["monthly_revenue"]
        
        # รายได้รวมทั้งปี
        total_year_rev = df_monthly_rev["monthly_revenue"].sum()
        top_month_pct = (top_month_rev / total_year_rev * 100) if total_year_rev > 0 else 0
        rest_year_rev = total_year_rev - top_month_rev

        # สร้าง DataFrame สำหรับกราฟเปรียบเทียบ (เดือนสูงสุด VS รายได้รวมทั้งปี)
        df_compare = pd.DataFrame([
            {
                "category": f"เดือนสูงสุด ({top_month_name})",
                "revenue": top_month_rev,
                "percentage": f"{top_month_pct:.1f}% ของทั้งปี"
            },
            {
                "category": f"รายได้รวมทั้งปี {selected_rev_year}",
                "revenue": total_year_rev,
                "percentage": "100.0%"
            }
        ])

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            render_kpi_card(
                f"เดือนที่รายได้สูงสุด ({selected_rev_year})",
                f"{top_month_name}",
                f"Peak Revenue Month",
            )
        with col_m2:
            render_kpi_card(
                f"รายได้เดือน {top_month_name}",
                f"฿{top_month_rev:,.2f}",
                f"คิดเป็น {top_month_pct:.1f}% ของรายได้ทั้งปี",
            )
        with col_m3:
            render_kpi_card(
                f"รายได้รวมทั้งปี {selected_rev_year}",
                f"฿{total_year_rev:,.2f}",
                f"Total Revenue ({selected_rev_year})",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        col_chart_top, col_chart_monthly = st.columns([1, 1.5])

        with col_chart_top:
            st.markdown(
                f'<div class="section-header">เปรียบเทียบรายได้เดือนสูงสุดเทียบกับทั้งปี ({selected_rev_year})</div>',
                unsafe_allow_html=True,
            )
            fig_compare = px.bar(
                df_compare,
                x="category",
                y="revenue",
                text="revenue",
                color="category",
                color_discrete_map={
                    f"เดือนสูงสุด ({top_month_name})": "#DB1A1A",
                    f"รายได้รวมทั้งปี {selected_rev_year}": "#8CC7C4",
                },
                labels={"category": "เปรียบเทียบ", "revenue": "รายได้ (฿)"},
            )
            fig_compare.update_traces(
                texttemplate="฿%{y:,.0f}", textposition="outside"
            )
            fig_compare.update_layout(
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_compare, use_container_width=True)

        with col_chart_monthly:
            st.markdown(
                f'<div class="section-header">รายได้แยกรายเดือนประจำปี {selected_rev_year}</div>',
                unsafe_allow_html=True,
            )
            fig_monthly = px.bar(
                df_monthly_rev,
                x="month_name",
                y="monthly_revenue",
                text_auto=".3s",
                color="month_name",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                labels={"month_name": "เดือน", "monthly_revenue": "รายได้ (฿)"},
            )
            fig_monthly.update_layout(
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_monthly, use_container_width=True)

    else:
        st.info(f"ไม่พบข้อมูลรายได้ในปี {selected_rev_year}")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ส่วนเดิม: ลูกค้าหลัก เส้นทางยอดนิยม และกราฟสรุป
    # ---------------------------------------------------------
    df_top_cust = run_query(f"""
        SELECT c.customer_name, SUM(f.revenue) as total_revenue
        FROM fact_loads f 
        JOIN dim_customers c ON f.customer_key = c.customer_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY c.customer_name ORDER BY total_revenue DESC LIMIT 1
    """)

    top_cust_name = (
        df_top_cust.iloc[0]["customer_name"]
        if not df_top_cust.empty
        else "N/A"
    )
    top_cust_rev = (
        df_top_cust.iloc[0]["total_revenue"] if not df_top_cust.empty else 0
    )

    df_top_route = run_query(f"""
        SELECT r.route_id, COUNT(f.load_key) as total_loads
        FROM fact_loads f 
        JOIN dim_route r ON f.route_key = r.route_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY r.route_id ORDER BY total_loads DESC LIMIT 1
    """)

    top_route_id = (
        df_top_route.iloc[0]["route_id"] if not df_top_route.empty else "N/A"
    )
    top_route_loads = (
        df_top_route.iloc[0]["total_loads"] if not df_top_route.empty else 0
    )

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        rev_tot_res = run_query(
            f"SELECT COALESCE(SUM(f.revenue), 0) FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
        )
        rev_tot = rev_tot_res.iloc[0, 0] if not rev_tot_res.empty else 0
        render_kpi_card(
            "รายได้รวมตามตัวกรองหลัก", f"฿{rev_tot:,.2f}", "Total Revenue"
        )
    with col_kpi2:
        render_kpi_card(
            "ลูกค้าที่สร้างรายได้สูงสุด (Top Customer)",
            top_cust_name,
            f"Revenue: ฿{top_cust_rev:,.2f}",
        )
    with col_kpi3:
        render_kpi_card(
            "เส้นทางยอดนิยม (Top Route by Load)",
            f"Route: {top_route_id}",
            f"Loads: {top_route_loads:,} Loads",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="section-header">เปรียบเทียบรายได้รวมในแต่ละปี</div>',
            unsafe_allow_html=True,
        )
        df_y_rev = run_query("""
            SELECT d.year::VARCHAR as year, SUM(f.revenue) as total_revenue
            FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year ORDER BY d.year
        """)
        fig_y = px.bar(
            df_y_rev,
            x="year",
            y="total_revenue",
            text_auto=".3s",
            color_discrete_sequence=["#8CC7C4"],
            labels={"year": "ปี", "total_revenue": "รายได้รวม (฿)"},
        )
        fig_y.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_y, use_container_width=True)

    with col2:
        st.markdown(
            '<div class="section-header">10 อันดับลูกค้าที่สร้างรายได้สูงสุด</div>',
            unsafe_allow_html=True,
        )
        df_cust = run_query(f"""
            SELECT c.customer_name, SUM(f.revenue) as total_revenue
            FROM fact_loads f 
            JOIN dim_customers c ON f.customer_key = c.customer_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY c.customer_name ORDER BY total_revenue DESC LIMIT 10
        """)
        fig_cust = px.bar(
            df_cust,
            x="total_revenue",
            y="customer_name",
            orientation="h",
            text_auto=".3s",
            color_discrete_sequence=["#1a1d20"],
            labels={
                "total_revenue": "รายได้ (฿)",
                "customer_name": "ชื่อลูกค้า",
            },
        )
        fig_cust.update_layout(
            yaxis={"categoryorder": "total ascending"},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_cust, use_container_width=True)

    st.markdown(
        '<div class="section-header">เส้นทางขนส่ง (Route) ที่มีจำนวน Load สูงสุด 10 อันดับแรก</div>',
        unsafe_allow_html=True,
    )
    df_route = run_query(f"""
        SELECT r.route_id, COUNT(f.load_key) as total_loads
        FROM fact_loads f 
        JOIN dim_route r ON f.route_key = r.route_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY r.route_id ORDER BY total_loads DESC LIMIT 10
    """)
    fig_route = px.bar(
        df_route,
        x="route_id",
        y="total_loads",
        text_auto=True,
        color_discrete_sequence=["#8CC7C4"],
        labels={"route_id": "รหัสเส้นทาง", "total_loads": "จำนวน Load"},
    )
    fig_route.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_route, use_container_width=True)

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
        sel_maint_year = st.selectbox(
            "เลือกปี (Year)", maint_years, key="m_year"
        )

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

    # KPI Calculation
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
    # 1. กราฟแท่งแสดงค่าซ่อมบำรุงรวมที่เปลี่ยนตามตัวเลือก (Filtered Maintenance Cost)
    # ---------------------------------------------------------
    col_m_bar, col_m_line = st.columns(2)

    with col_m_bar:
        st.markdown(
            '<div class="section-header">ค่าใช้จ่ายการซ่อมบำรุงรวม (ตามตัวกรองที่เลือก)</div>',
            unsafe_allow_html=True,
        )

        # dynamic group-by ขึ้นอยู่กับเงื่อนไข filter
        if sel_maint_month != "ทั้งหมด":
            # เลือกเดือนเฉพาะ -> แสดงรายวันในเดือนนั้น
            sql_maint_dyn = f"""
                SELECT d.full_date::VARCHAR as period, SUM(f.total_cost) as total_maint_cost
                FROM fact_maintenance f
                JOIN dim_date d ON f.date_key = d.date_key
                WHERE 1=1 {m_year_clause} {m_month_clause}
                GROUP BY d.full_date ORDER BY d.full_date
            """
            x_label = "วันที่"
        elif sel_maint_year != "ทั้งหมด":
            # เลือกปีเฉพาะ -> แสดงรายเดือนในปีนั้น
            sql_maint_dyn = f"""
                SELECT d.month_name as period, d.month, SUM(f.total_cost) as total_maint_cost
                FROM fact_maintenance f
                JOIN dim_date d ON f.date_key = d.date_key
                WHERE 1=1 {m_year_clause}
                GROUP BY d.month_name, d.month ORDER BY d.month
            """
            x_label = "เดือน"
        else:
            # เลือกทั้งหมด -> แสดงรายปี
            sql_maint_dyn = """
                SELECT d.year::VARCHAR as period, SUM(f.total_cost) as total_maint_cost
                FROM fact_maintenance f
                JOIN dim_date d ON f.date_key = d.date_key
                GROUP BY d.year ORDER BY d.year
            """
            x_label = "ปี"

        df_maint_dyn = run_query(sql_maint_dyn)

        if not df_maint_dyn.empty:
            fig_maint_dyn = px.bar(
                df_maint_dyn,
                x="period",
                y="total_maint_cost",
                text_auto=".3s",
                color_discrete_sequence=["#8CC7C4"],
                labels={
                    "period": x_label,
                    "total_maint_cost": "ค่าซ่อมบำรุง (฿)",
                },
            )
            fig_maint_dyn.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_maint_dyn, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลค่าซ่อมบำรุงตามตัวกรองที่เลือก")

    # ---------------------------------------------------------
    # 2. กราฟเส้นเปรียบเทียบค่าใช้จ่ายการซ่อมบำรุงรวมของแต่ละปี (Yearly Maintenance Trend)
    # ---------------------------------------------------------
    with col_m_line:
        st.markdown(
            '<div class="section-header">แนวโน้มเปรียบเทียบค่าซ่อมบำรุงรวมรายปี (Yearly Trend)</div>',
            unsafe_allow_html=True,
        )
        df_maint_yearly = run_query("""
            SELECT d.year::VARCHAR as year, SUM(f.total_cost) as yearly_maint_cost
            FROM fact_maintenance f
            JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year ORDER BY d.year
        """)

        if not df_maint_yearly.empty:
            fig_maint_line = px.line(
                df_maint_yearly,
                x="year",
                y="yearly_maint_cost",
                markers=True,
                color_discrete_sequence=["#DB1A1A"],
                labels={
                    "year": "ปี",
                    "yearly_maint_cost": "ค่าซ่อมบำรุงรวม (฿)",
                },
            )
            fig_maint_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_maint_line, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลค่าซ่อมบำรุงรายปี")

    st.markdown("<br>", unsafe_allow_html=True)

    # Top 10 Maintenance Cost
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
    st.caption("วิเคราะห์คลังสินค้า ความล่าช้า ประสิทธิภาพรถบรรทุก และผลต่างเวลาจัดส่ง")
    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 1. ตัวกรองหลักเฉพาะหน้า Delivery Performance (ปี & เดือน)
    # ---------------------------------------------------------
    st.markdown(
        '<div class="section-header">🔍 ตัวกรองเวลาสำหรับการวิเคราะห์การจัดส่ง (Delivery Time Filter)</div>',
        unsafe_allow_html=True,
    )
    col_df1, col_df2 = st.columns(2)

    df_del_years = run_query(
        "SELECT DISTINCT d.year FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key WHERE d.year IS NOT NULL ORDER BY d.year DESC"
    )
    del_years = df_del_years["year"].tolist() if not df_del_ye