import pandas as pd
import plotly.express as px
import streamlit as st
import duckdb

# =========================================================
# 1. Page Config & Custom Styling (Global Design System)
# =========================================================
st.set_page_config(
    page_title="Logistics Analytics Console - 5G Express",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Design System CSS
st.markdown(
    """
    <style>
    .stApp { background-color: #f8f9fa; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* KPI Card System */
    .kpi-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px 22px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        margin-bottom: 12px;
    }
    .kpi-title { font-size: 13px; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 26px; font-weight: 700; color: #1a1d20; margin-top: 4px; margin-bottom: 2px; }
    .kpi-sub { font-size: 12px; color: #43CD80; font-weight: 500; }
    .kpi-sub-risk { font-size: 12px; color: #EE0000; font-weight: 500; }
    
    /* Section Headers */
    .section-header {
        font-size: 16px;
        font-weight: 700;
        color: #212529;
        margin-top: 5px;
        margin-bottom: 15px;
        border-left: 4px solid #EE0000;
        padding-left: 10px;
    }
    
    /* Utility Styles */
    div[data-testid="stMetricValue"] { font-size: 24px; font-weight: 700; }
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

# Helper Function สำหรับรัน SQL อย่างปลอดภัย
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
    rev_val = (
        run_query(
            f"SELECT SUM(f.revenue) FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
        ).iloc[0, 0]
        or 0
    )
    delivery_count = (
        run_query(
            f"SELECT COUNT(*) FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
        ).iloc[0, 0]
        or 0
    )
    trip_count = (
        run_query(
            f"SELECT COUNT(*) FROM fact_trips f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
        ).iloc[0, 0]
        or 0
    )
    fuel_cost = (
        run_query(
            f"SELECT SUM(f.total_cost) FROM fact_fuel f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
        ).iloc[0, 0]
        or 0
    )

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

    # 2. Monthly / Yearly Fuel Cost Trend (Req 2.2)
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
                color_discrete_sequence=["#EE0000"],
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

    # 3. Full Pie Chart for On-Time Ratio (Req 2.1 - No Donut)
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
                hole=0,  # Full Pie Chart (No Donut)
                color="status",
                color_discrete_map={
                    "ตรงเวลา (On Time)": "#43CD80",
                    "ล่าช้า (Late)": "#EE0000",
                },
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
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
    st.caption("เจาะลึกที่มารายได้เปรียบเทียบรายปี ลูกค้าหลัก และเส้นทางยอดนิยม")
    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic Top Customer & Top Route (Req 3.1, 3.2, 3.3)
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

    # Top Section Summary (Req 3.4 Layout)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        rev_tot = (
            run_query(
                f"SELECT SUM(f.revenue) FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
            ).iloc[0, 0]
            or 0
        )
        render_kpi_card("รายได้รวมตามตัวกรอง", f"฿{rev_tot:,.2f}", "Total Revenue")
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
            color_discrete_sequence=["#43CD80"],
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
        color_discrete_sequence=["#43CD80"],
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

    # Local Year & Month Filter (Req 4.2, 4.3)
    st.markdown(
        '<div class="section-header">ตัวกรองเวลาค่าซ่อมบำรุง (Maintenance Filter)</div>',
        unsafe_allow_html=True,
    )
    col_f1, col_f2 = st.columns(2)

    df_maint_years = run_query(
        "SELECT DISTINCT year FROM dim_date WHERE year IS NOT NULL ORDER BY year DESC"
    )
    maint_years = (
        df_maint_years["year"].tolist() if not df_maint_years.empty else [2026]
    )
    maint_years.insert(0, "ทั้งหมด")

    with col_f1:
        sel_maint_year = st.selectbox("เลือกปี (Year)", maint_years, key="m_year")

    maint_month_clause = ""
    with col_f2:
        df_maint_months = run_query(
            "SELECT DISTINCT month_name, month FROM dim_date ORDER BY month"
        )
        months_list = (
            df_maint_months["month_name"].tolist()
            if not df_maint_months.empty
            else []
        )
        months_list.insert(0, "ทั้งหมด")
        sel_maint_month = st.selectbox(
            "เลือกเดือน (Month)", months_list, key="m_month"
        )

    # Local Clause Setup
    m_year_clause = (
        "" if sel_maint_year == "ทั้งหมด" else f"AND d.year = {sel_maint_year}"
    )
    m_month_clause = (
        ""
        if sel_maint_month == "ทั้งหมด"
        else f"AND d.month_name = '{sel_maint_month}'"
    )

    # KPI Calculation (Req 4.2)
    maint_cost_val = (
        run_query(f"""
        SELECT SUM(f.total_cost) 
        FROM fact_maintenance f 
        JOIN dim_date d ON f.date_key = d.date_key 
        WHERE 1=1 {m_year_clause} {m_month_clause}
    """).iloc[0, 0]
        or 0
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

    # Top 10 Trucks with Vertical Bar Chart (Req 4.1)
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
            x="Truck_ID",  # Vertical Bar Chart Requirement
            y="total_maint_cost",
            text_auto=".3s",
            color_discrete_sequence=["#EE0000"],
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

    # Fleet & Driver Analysis Section (Req 4.4)
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
            color_discrete_sequence=["#43CD80"],
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

    # Full Pie Chart for Delivery On-time vs Delayed (Req 5)
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
        WHERE 1=1 {year_clause}
        GROUP BY f.is_on_time
    """)

    if not df_delivery_pie.empty:
        fig_del_pie = px.pie(
            df_delivery_pie,
            names="status",
            values="count",
            hole=0,  # Full Pie Chart Requirement
            color="status",
            color_discrete_map={
                "ตรงเวลา (On Time)": "#43CD80",
                "ล่าช้า (Delayed)": "#EE0000",
            },
        )
        fig_del_pie.update_traces(
            textposition="inside", textinfo="percent+label"
        )
        fig_del_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_del_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="section-header">คลังสินค้า/สถานที่ (Facilities) ที่มีเคสจัดส่งล่าช้าสูงสุด</div>',
            unsafe_allow_html=True,
        )
        df_fac_late = run_query(f"""
            SELECT fac.facility_name, COUNT(*) as late_count
            FROM fact_delivery f 
            JOIN dim_facilities fac ON f.facility_key = fac.facility_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE f.is_on_time = False {year_clause}
            GROUP BY fac.facility_name ORDER BY late_count DESC LIMIT 10
        """)
        fig_fac = px.bar(
            df_fac_late,
            x="late_count",
            y="facility_name",
            orientation="h",
            text_auto=True,
            color_discrete_sequence=["#EE0000"],
            labels={
                "late_count": "จำนวนเคสที่ล่าช้า",
                "facility_name": "ชื่อคลังสินค้า",
            },
        )
        fig_fac.update_layout(
            yaxis={"categoryorder": "total ascending"},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_fac, use_container_width=True)

    with col2:
        st.markdown(
            '<div class="section-header">การกระจายตัวของเวลาส่งล่าช้า (Delay Variance)</div>',
            unsafe_allow_html=True,
        )
        df_delay = run_query(f"""
            SELECT delay_minutes 
            FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key
            WHERE f.is_on_time = False {year_clause}
        """)
        if not df_delay.empty:
            fig_delay = px.histogram(
                df_delay,
                x="delay_minutes",
                nbins=25,
                color_discrete_sequence=["#EE0000"],
                labels={"delay_minutes": "ความล่าช้า (นาที)"},
            )
            fig_delay.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_delay, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลความล่าช้า")


# =========================================================
# PAGE 5 — FUEL & SAFETY ANALYSIS
# =========================================================
elif menu == "⛽ ตัวชี้วัดการใช้น้ำมันและความปลอดภัยในการขนส่ง":
    st.title("⛽ ตัวชี้วัดการใช้น้ำมันและความปลอดภัยในการขนส่ง")
    st.caption("ตรวจสอบค่าใช้จ่ายน้ำมันเชื้อเพลิงและอุบัติเหตุที่เกิดขึ้น")
    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic Top Truck by Fuel Cost (Req 6.1)
    df_top_fuel_truck = run_query(f"""
        SELECT t.Truck_ID, SUM(f.total_cost) as total_fuel_cost
        FROM fact_fuel f
        JOIN dim_trucks t ON f.truck_key = t.truck_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY t.Truck_ID ORDER BY total_fuel_cost DESC LIMIT 1
    """)

    top_truck_id = (
        df_top_fuel_truck.iloc[0]["Truck_ID"]
        if not df_top_fuel_truck.empty
        else "N/A"
    )
    top_truck_cost = (
        df_top_fuel_truck.iloc[0]["total_fuel_cost"]
        if not df_top_fuel_truck.empty
        else 0
    )

    tot_fuel_val = (
        run_query(
            f"SELECT SUM(f.total_cost) FROM fact_fuel f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}"
        ).iloc[0, 0]
        or 0
    )

    col_fkpi1, col_fkpi2 = st.columns(2)
    with col_fkpi1:
        render_kpi_card(
            "ค่าใช้จ่ายน้ำมันรวม (Total Fuel Cost)",
            f"฿{tot_fuel_val:,.2f}",
            "Fuel Expense",
            is_risk=True,
        )
    with col_fkpi2:
        render_kpi_card(
            "รถบรรทุกที่มีค่าน้ำมันสูงสุด (Top Truck by Fuel)",
            f"Truck ID: {top_truck_id}",
            f"Fuel Cost: ฿{top_truck_cost:,.2f}",
            is_risk=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Fuel Cost Ranking by Truck (Req 6.2)
    st.markdown(
        '<div class="section-header">อันดับค่าใช้จ่ายน้ำมันแบ่งตามรถบรรทุก (Fuel Cost Ranking by Truck)</div>',
        unsafe_allow_html=True,
    )
    df_truck_fuel_rank = run_query(f"""
        SELECT t.Truck_ID, SUM(f.total_cost) as total_fuel_cost
        FROM fact_fuel f
        JOIN dim_trucks t ON f.truck_key = t.truck_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY t.Truck_ID ORDER BY total_fuel_cost DESC LIMIT 10
    """)

    if not df_truck_fuel_rank.empty:
        fig_fuel_rank = px.bar(
            df_truck_fuel_rank,
            x="Truck_ID",
            y="total_fuel_cost",
            text_auto=".3s",
            color_discrete_sequence=["#EE0000"],
            labels={
                "total_fuel_cost": "ค่าน้ำมัน (฿)",
                "Truck_ID": "รหัสรถบรรทุก",
            },
        )
        fig_fuel_rank.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_fuel_rank, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Safety Analysis Section (Req 6.3)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="section-header">ค่าใช้จ่ายน้ำมันเชื้อเพลิงรวมในแต่ละปี</div>',
            unsafe_allow_html=True,
        )
        df_fuel_y = run_query("""
            SELECT d.year::VARCHAR as year, SUM(f.total_cost) as fuel_cost
            FROM fact_fuel f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year ORDER BY d.year
        """)
        fig_fy = px.bar(
            df_fuel_y,
            x="year",
            y="fuel_cost",
            text_auto=".3s",
            color_discrete_sequence=["#EE0000"],
            labels={"year": "ปี", "fuel_cost": "ค่าน้ำมัน (฿)"},
        )
        fig_fy.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_fy, use_container_width=True)

    with col2:
        st.markdown(
            '<div class="section-header">จำนวนอุบัติเหตุและความปลอดภัย (Incidents) ในแต่ละปี</div>',
            unsafe_allow_html=True,
        )
        df_inc_y = run_query("""
            SELECT d.year::VARCHAR as year, COUNT(*) as incident_count
            FROM fact_safety_incidents f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year ORDER BY d.year
        """)
        fig_iy = px.bar(
            df_inc_y,
            x="year",
            y="incident_count",
            text_auto=True,
            color_discrete_sequence=["#1a1d20"],
            labels={"year": "ปี", "incident_count": "จำนวนครั้ง"},
        )
        fig_iy.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_iy, use_container_width=True)

    st.markdown(
        '<div class="section-header">สัดส่วนประเภทของอุบัติเหตุ/เหตุการณ์ความปลอดภัย (Incident Types)</div>',
        unsafe_allow_html=True,
    )
    df_inc_type = run_query(f"""
        SELECT f.incident_type, COUNT(*) as count
        FROM fact_safety_incidents f JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY f.incident_type ORDER BY count DESC
    """)
    if not df_inc_type.empty:
        fig_it = px.pie(
            df_inc_type,
            names="incident_type",
            values="count",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu,
        )
        fig_it.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_it, use_container_width=True)