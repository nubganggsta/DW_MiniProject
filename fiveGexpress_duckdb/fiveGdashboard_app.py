import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px

# ---------------------------------------------------------
# 1. Page Config & Custom Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Logistics Analytics Console - 5G Express",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .kpi-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px 22px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }
    .kpi-title { font-size: 13px; color: #6c757d; font-weight: 600; }
    .kpi-value { font-size: 26px; font-weight: 700; color: #1a1d20; margin-top: 4px; }
    .kpi-sub { font-size: 12px; color: #22c55e; font-weight: 500; margin-top: 2px; }
    
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #212529;
        margin-bottom: 15px;
        border-left: 4px solid #ff4b4b;
        padding-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. Database Connection
# ---------------------------------------------------------
@st.cache_resource
def get_connection():
    return duckdb.connect("dev.duckdb", read_only=True)

try:
    conn = get_connection()
except Exception as e:
    st.error(f"⚠️ ไม่สามารถเชื่อมต่อกับ Data Warehouse ได้: {e}")
    st.stop()


# ---------------------------------------------------------
# 3. Sidebar Navigation & Global Filters
# ---------------------------------------------------------
with st.sidebar:
    st.title("🚚 5G Express")
    st.caption("Data Warehouse Analytics Console")
    st.markdown("---")
    
    menu = st.radio(
        "📌 เลือกหมวดหมู่การวิเคราะห์:",
        [
            "📈 ภาพรวมผู้บริหาร (Overview)",
            "💰 รายได้และลูกค้า (Revenue & Customers)",
            "🚛 กองรถและการซ่อมบำรุง (Fleet & Maintenance)",
            "⏱️ การจัดส่งและความตรงต่อเวลา (Delivery)",
            "⛽ การใช้น้ำมันและความปลอดภัย (Fuel & Safety)"
        ]
    )
    
    st.markdown("---")
    st.subheader("🔍 ตัวกรองข้อมูล (Filters)")
    
    # ดึงรายการปีที่มีในระบบ
    years_available = conn.query("SELECT DISTINCT year FROM dim_date ORDER BY year DESC").df()['year'].tolist()
    years_available.insert(0, "ทั้งหมด")
    selected_year = st.selectbox("เลือกปี (Year)", years_available)
    
    # เงื่อนไข SQL Filter
    year_clause = "" if selected_year == "ทั้งหมด" else f"AND d.year = {selected_year}"
    year_clause_where = "" if selected_year == "ทั้งหมด" else f"WHERE d.year = {selected_year}"


# ---------------------------------------------------------
# Page 1: ภาพรวมผู้บริหาร (Overview)
# ---------------------------------------------------------
if menu == "📈 ภาพรวมผู้บริหาร (Overview)":
    st.title("📈 ภาพรวมการดำเนินงาน (Executive Overview)")
    st.caption("สรุปดัชนีชี้วัดผลงานหลัก (KPIs) และแนวโน้มภาพรวมขององค์กร")
    st.markdown("<br>", unsafe_allow_html=True)

    # คำนวณ KPIs
    rev_val = conn.query(f"SELECT SUM(f.revenue) FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}").fetchone()[0] or 0
    delivery_count = conn.query(f"SELECT COUNT(*) FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}").fetchone()[0] or 0
    trip_count = conn.query(f"SELECT COUNT(*) FROM fact_trips f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}").fetchone()[0] or 0
    fuel_cost = conn.query(f"SELECT SUM(f.total_cost) FROM fact_fuel f JOIN dim_date d ON f.date_key = d.date_key WHERE 1=1 {year_clause}").fetchone()[0] or 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">รายได้รวมทั้งหมด</div><div class="kpi-value">${rev_val:,.2f}</div><div class="kpi-sub">Total Revenue</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">จำนวนการจัดส่งสินค้า</div><div class="kpi-value">{delivery_count:,}</div><div class="kpi-sub">Total Deliveries</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">จำนวนเที่ยววิ่งทั้งหมด</div><div class="kpi-value">{trip_count:,}</div><div class="kpi-sub">Total Trips</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-title">ค่าใช้จ่ายน้ำมันรวม</div><div class="kpi-value">${fuel_cost:,.2f}</div><div class="kpi-sub">Total Fuel Expense</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([1.8, 1])
    with col_chart1:
        st.markdown('<div class="section-header">แนวโน้มรายได้รายเดือน (Monthly Revenue Trend)</div>', unsafe_allow_html=True)
        df_rev = conn.query(f"""
            SELECT d.year_month, SUM(f.revenue) as monthly_revenue
            FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY d.year_month ORDER BY d.year_month
        """).df()
        
        if not df_rev.empty:
            fig = px.line(df_rev, x="year_month", y="monthly_revenue", markers=True, color_discrete_sequence=["#ff4b4b"],
                          labels={"year_month": "เดือน", "monthly_revenue": "รายได้ ($)"})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=10,b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลในช่วงเวลาที่เลือก")

    with col_chart2:
        st.markdown('<div class="section-header">สัดส่วนการส่งตรงเวลา (On-Time Ratio)</div>', unsafe_allow_html=True)
        df_ontime = conn.query(f"""
            SELECT CASE WHEN f.is_on_time THEN 'ตรงเวลา (On Time)' ELSE 'ล่าช้า (Late)' END as status, COUNT(*) as count
            FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY f.is_on_time
        """).df()
        if not df_ontime.empty:
            fig_pie = px.pie(df_ontime, names="status", values="count", hole=0.5, color_discrete_sequence=["#22c55e", "#ff4b4b"])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)


# ---------------------------------------------------------
# Page 2: รายได้และลูกค้า (Revenue & Customers)
# ---------------------------------------------------------
elif menu == "💰 รายได้และลูกค้า (Revenue & Customers)":
    st.title("💰 การวิเคราะห์รายได้และพฤติกรรมลูกค้า")
    st.caption("เจาะลึกที่มารายได้เปรียบเทียบรายปี ลูกค้าหลัก และเส้นทางยอดนิยม")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">เปรียบเทียบรายได้รวมในแต่ละปี</div>', unsafe_allow_html=True)
        df_y_rev = conn.query("""
            SELECT d.year::VARCHAR as year, SUM(f.revenue) as total_revenue
            FROM fact_loads f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year ORDER BY d.year
        """).df()
        fig_y = px.bar(df_y_rev, x="year", y="total_revenue", text_auto='.3s', color_discrete_sequence=["#e63946"],
                       labels={"year": "ปี", "total_revenue": "รายได้รวม ($)"})
        st.plotly_chart(fig_y, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">10 อันดับลูกค้าที่สร้างรายได้สูงสุด</div>', unsafe_allow_html=True)
        df_cust = conn.query(f"""
            SELECT c.customer_name, SUM(f.revenue) as total_revenue
            FROM fact_loads f 
            JOIN dim_customers c ON f.customer_key = c.customer_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY c.customer_name ORDER BY total_revenue DESC LIMIT 10
        """).df()
        fig_cust = px.bar(df_cust, x="total_revenue", y="customer_name", orientation='h', text_auto='.3s',
                          color_discrete_sequence=["#1a1d20"], labels={"total_revenue": "รายได้ ($)", "customer_name": "ชื่อลูกค้า"})
        fig_cust.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cust, use_container_width=True)

    st.markdown('<div class="section-header">เส้นทางขนส่ง (Route) ที่มีจำนวน Load สูงสุด 10 อันดับแรก</div>', unsafe_allow_html=True)
    df_route = conn.query(f"""
        SELECT r.route_id, COUNT(f.load_key) as total_loads
        FROM fact_loads f 
        JOIN dim_route r ON f.route_key = r.route_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY r.route_id ORDER BY total_loads DESC LIMIT 10
    """).df()
    fig_route = px.bar(df_route, x="route_id", y="total_loads", text_auto=True, color_discrete_sequence=["#ff4b4b"],
                       labels={"route_id": "รหัสเส้นทาง", "total_loads": "จำนวน Load"})
    st.plotly_chart(fig_route, use_container_width=True)


# ---------------------------------------------------------
# Page 3: กองรถและการซ่อมบำรุง (Fleet & Maintenance)
# ---------------------------------------------------------
elif menu == "🚛 กองรถและการซ่อมบำรุง (Fleet & Maintenance)":
    st.title("🚛 การบริหารจัดการกองรถและการซ่อมบำรุง")
    st.caption("ติดตามการใช้งานรถบรรทุก สถิติการวิ่ง และต้นทุนการบำรุงรักษา")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">10 อันดับ รถบรรทุกที่มีการใช้งานวิ่งเที่ยวสูงสุด (Trips)</div>', unsafe_allow_html=True)
        df_truck_trips = conn.query(f"""
            SELECT t.Truck_ID, COUNT(f.trip_key) as total_trips
            FROM fact_trips f 
            JOIN dim_trucks t ON f.truck_key = t.truck_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY t.Truck_ID ORDER BY total_trips DESC LIMIT 10
        """).df()
        fig_truck_t = px.bar(df_truck_trips, x="Truck_ID", y="total_trips", text_auto=True, color_discrete_sequence=["#e63946"],
                             labels={"Truck_ID": "รหัสรถบรรทุก", "total_trips": "จำนวน Trips"})
        st.plotly_chart(fig_truck_t, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">10 อันดับ รถบรรทุกที่มีค่าซ่อมบำรุงสูงสุด</div>', unsafe_allow_html=True)
        df_truck_maint = conn.query(f"""
            SELECT t.Truck_ID, SUM(f.total_cost) as total_maint_cost
            FROM fact_maintenance f 
            JOIN dim_trucks t ON f.truck_key = t.truck_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY t.Truck_ID ORDER BY total_maint_cost DESC LIMIT 10
        """).df()
        fig_truck_m = px.bar(df_truck_maint, x="total_maint_cost", y="Truck_ID", orientation='h', text_auto='.3s', color_discrete_sequence=["#ff4b4b"],
                             labels={"total_maint_cost": "ค่าซ่อมบำรุง ($)", "Truck_ID": "รหัสรถบรรทุก"})
        fig_truck_m.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_truck_m, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">พนักงานขับรถที่มีสถิติการวิ่งสูงสุด 10 อันดับแรก</div>', unsafe_allow_html=True)
        df_driver = conn.query(f"""
            SELECT dr.full_name, COUNT(f.trip_key) as total_trips
            FROM fact_trips f 
            JOIN dim_drivers dr ON f.driver_key = dr.driver_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE 1=1 {year_clause}
            GROUP BY dr.full_name ORDER BY total_trips DESC LIMIT 10
        """).df()
        fig_drv = px.bar(df_driver, x="total_trips", y="full_name", orientation='h', text_auto=True, color_discrete_sequence=["#1a1d20"],
                         labels={"total_trips": "จำนวน Trips", "full_name": "ชื่อพนักงานขับรถ"})
        fig_drv.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_drv, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">สรุปค่าซ่อมบำรุงรวมในแต่ละปี</div>', unsafe_allow_html=True)
        df_maint_year = conn.query("""
            SELECT d.year::VARCHAR as year, SUM(f.total_cost) as total_cost
            FROM fact_maintenance f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year ORDER BY d.year
        """).df()
        fig_my = px.bar(df_maint_year, x="year", y="total_cost", text_auto='.3s', color_discrete_sequence=["#6c757d"],
                        labels={"year": "ปี", "total_cost": "ค่าซ่อมบำรุง ($)"})
        st.plotly_chart(fig_my, use_container_width=True)


# ---------------------------------------------------------
# Page 4: การจัดส่งและความตรงต่อเวลา (Delivery)
# ---------------------------------------------------------
elif menu == "⏱️ การจัดส่งและความตรงต่อเวลา (Delivery)":
    st.title("⏱️ ประสิทธิภาพการจัดส่งและความตรงต่อเวลา")
    st.caption("วิเคราะห์คลังสินค้า ความล่าช้า และผลต่างระหว่างเวลาจริงเทียบกับแผน")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">คลังสินค้า/สถานที่ (Facilities) ที่มีเคสจัดส่งล่าช้าสูงสุด</div>', unsafe_allow_html=True)
        df_fac_late = conn.query(f"""
            SELECT fac.facility_name, COUNT(*) as late_count
            FROM fact_delivery f 
            JOIN dim_facilities fac ON f.facility_key = fac.facility_key
            JOIN dim_date d ON f.date_key = d.date_key
            WHERE f.is_on_time = False {year_clause}
            GROUP BY fac.facility_name ORDER BY late_count DESC LIMIT 10
        """).df()
        fig_fac = px.bar(df_fac_late, x="late_count", y="facility_name", orientation='h', text_auto=True, color_discrete_sequence=["#e63946"],
                         labels={"late_count": "จำนวนเคสที่ล่าช้า", "facility_name": "ชื่อคลังสินค้า"})
        fig_fac.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_fac, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">การกระจายตัวของเวลาส่งล่าช้า (Delay Variance)</div>', unsafe_allow_html=True)
        # ตรวจสอบคอลัมน์ delay ในตาราง
        df_delay = conn.query(f"""
            SELECT delay_minutes 
            FROM fact_delivery f JOIN dim_date d ON f.date_key = d.date_key
            WHERE f.is_on_time = False {year_clause}
        """).df()
        if not df_delay.empty:
            fig_delay = px.histogram(df_delay, x="delay_minutes", nbins=25, color_discrete_sequence=["#ff4b4b"],
                                     labels={"delay_minutes": "ความล่าช้า (นาที)"})
            st.plotly_chart(fig_delay, use_container_width=True)
        else:
            st.info("ไม่พบข้อมูลความล่าช้า")


# ---------------------------------------------------------
# Page 5: การใช้น้ำมันและความปลอดภัย (Fuel & Safety)
# ---------------------------------------------------------
elif menu == "⛽ การใช้น้ำมันและความปลอดภัย (Fuel & Safety)":
    st.title("⛽ ตัวชี้วัดการใช้น้ำมันและความปลอดภัยในการขนส่ง")
    st.caption("ตรวจสอบค่าใช้จ่ายน้ำมันเชื้อเพลิงและอุบัติเหตุที่เกิดขึ้น")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">ค่าใช้จ่ายน้ำมันเชื้อเพลิงรวมในแต่ละปี</div>', unsafe_allow_html=True)
        df_fuel_y = conn.query("""
            SELECT d.year::VARCHAR as year, SUM(f.total_cost) as fuel_cost
            FROM fact_fuel f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year ORDER BY d.year
        """).df()
        fig_fy = px.bar(df_fuel_y, x="year", y="fuel_cost", text_auto='.3s', color_discrete_sequence=["#e63946"],
                        labels={"year": "ปี", "fuel_cost": "ค่าน้ำมัน ($)"})
        st.plotly_chart(fig_fy, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">จำนวนอุบัติเหตุและความปลอดภัย (Incidents) ในแต่ละปี</div>', unsafe_allow_html=True)
        df_inc_y = conn.query("""
            SELECT d.year::VARCHAR as year, COUNT(*) as incident_count
            FROM fact_safety_incidents f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year ORDER BY d.year
        """).df()
        fig_iy = px.bar(df_inc_y, x="year", y="incident_count", text_auto=True, color_discrete_sequence=["#1a1d20"],
                        labels={"year": "ปี", "incident_count": "จำนวนครั้ง"})
        st.plotly_chart(fig_iy, use_container_width=True)

    st.markdown('<div class="section-header">สัดส่วนประเภทของอุบัติเหตุ/เหตุการณ์ความปลอดภัย (Incident Types)</div>', unsafe_allow_html=True)
    df_inc_type = conn.query(f"""
        SELECT f.incident_type, COUNT(*) as count
        FROM fact_safety_incidents f JOIN dim_date d ON f.date_key = d.date_key
        WHERE 1=1 {year_clause}
        GROUP BY f.incident_type ORDER BY count DESC
    """).df()
    fig_it = px.pie(df_inc_type, names="incident_type", values="count", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_it, use_container_width=True)