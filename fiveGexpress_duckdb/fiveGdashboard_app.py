import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb

# ==========================================
# 1. การตั้งค่าหน้าเพจหลัก
# ==========================================
st.set_page_config(
    page_title="5G Express - Logistics Dashboard",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ปรับแต่งสีและสไตล์เบื้องต้นด้วย CSS
st.markdown("""
    <style>
    .main {background-color: #F8F9FA;}
    h1, h2, h3 {color: #1E3A8A;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ฟังก์ชันดึงข้อมูลจาก DuckDB
# ==========================================
# กรุณาเปลี่ยนชื่อไฟล์ DuckDB ให้ตรงกับโปรเจกต์ของคุณ
DB_PATH = 'fiveGexpress.duckdb' 

@st.cache_data(ttl=600) # Cache ข้อมูล 10 นาทีเพื่อความรวดเร็ว
def run_query(query):
    try:
        # เชื่อมต่อ DuckDB และรัน Query
        with duckdb.connect(database=DB_PATH, read_only=True) as con:
            df = con.execute(query).df()
        return df
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
        return pd.DataFrame() # คืนค่า DataFrame ว่างถ้าดึงข้อมูลไม่ได้

# ==========================================
# 3. เมนูนำทาง (Sidebar Navigation)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2766/2766156.png", width=100)
st.sidebar.title("เมนูหลัก (Navigation)")
page = st.sidebar.radio("เลือกหน้ารายงาน:", [
    "📊 ภาพรวมรายได้และลูกค้า (Revenue & Customers)",
    "🚚 การจัดส่งและพนักงาน (Operations & Drivers)",
    "🛠️ ซ่อมบำรุงและสมรรถนะ (Maintenance & Fleet)",
    "⛽ น้ำมันและความปลอดภัย (Fuel & Safety)"
])

st.sidebar.markdown("---")
st.sidebar.info("Dashboard สำหรับวิเคราะห์ข้อมูลจาก Data Warehouse โครงการ 5G Express")

# ==========================================
# 4. ส่วนแสดงผลตามหน้าที่เลือก
# ==========================================

# ---------------------------------------------------------
# หน้าที่ 1: ภาพรวมรายได้และลูกค้า
# ---------------------------------------------------------
if page == "📊 ภาพรวมรายได้และลูกค้า (Revenue & Customers)":
    st.title("📊 ภาพรวมรายได้และลูกค้า")
    st.markdown("วิเคราะห์รายได้ตามช่วงเวลา ลูกค้ารายใหญ่ และเปรียบเทียบประเภทตู้พ่วง")

    # ดึงข้อมูลรายได้รายเดือน
    df_rev_monthly = run_query("""
        SELECT 
            CAST(d.year AS VARCHAR) || '-' || LPAD(CAST(d.month AS VARCHAR), 2, '0') AS month_year,
            SUM(t.revenue) as total_revenue
        FROM fact_trips_operations t
        JOIN dim_date d ON t.date_key = d.date_key
        GROUP BY 1 ORDER BY 1
    """)

    # ดึงข้อมูลลูกค้ารายใหญ่
    df_top_customers = run_query("""
        SELECT 
            c.customer_name, 
            c.primary_freight_type,
            COUNT(t.trip_key) as total_trips,
            SUM(t.revenue) as total_revenue
        FROM fact_trips_operations t
        JOIN dim_customers c ON t.customer_key = c.customer_key
        GROUP BY 1, 2 ORDER BY total_trips DESC LIMIT 10
    """)

    # สร้าง Metrics สรุป
    if not df_rev_monthly.empty:
        total_rev = df_rev_monthly['total_revenue'].sum()
        col1, col2, col3 = st.columns(3)
        col1.metric("รายได้สะสมทั้งหมด (Total Revenue)", f"${total_rev:,.2f}")
        col2.metric("จำนวนลูกค้าที่ใช้บริการ (Active Customers)", len(df_top_customers))
        col3.metric("เดือนที่มีรายได้สูงสุด", df_rev_monthly.iloc[df_rev_monthly['total_revenue'].idxmax()]['month_year'])

        # กราฟรายได้
        st.subheader("แนวโน้มรายได้รายเดือน")
        fig_rev = px.area(df_rev_monthly, x='month_year', y='total_revenue', markers=True, color_discrete_sequence=['#1E3A8A'])
        st.plotly_chart(fig_rev, use_container_width=True)

    # แบ่งครึ่งแสดงลูกค้าและตู้พ่วง
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("🏆 ลูกค้าที่มีปริมาณจ้างขนส่งสูงสุด 10 อันดับ")
        if not df_top_customers.empty:
            st.dataframe(df_top_customers, use_container_width=True)
            
    with col_c2:
        st.subheader("❄️ รายได้: ตู้เย็น (Reefer) vs ตู้แห้ง (Dry Van)")
        df_trailer = run_query("""
            SELECT tr.trailer_type, AVG(t.revenue) as avg_revenue_per_trip
            FROM fact_trips_operations t
            JOIN dim_trailers tr ON t.trailer_key = tr.trailer_key
            GROUP BY 1
        """)
        if not df_trailer.empty:
            fig_trailer = px.bar(df_trailer, x='trailer_type', y='avg_revenue_per_trip', color='trailer_type')
            st.plotly_chart(fig_trailer, use_container_width=True)


# ---------------------------------------------------------
# หน้าที่ 2: การจัดส่งและพนักงาน
# ---------------------------------------------------------
elif page == "🚚 การจัดส่งและพนักงาน (Operations & Drivers)":
    st.title("🚚 ประสิทธิภาพการจัดส่งและพนักงาน")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⏱️ อัตราการจัดส่งตรงเวลา (On-Time Delivery)")
        df_ontime = run_query("""
            SELECT 
                CASE WHEN on_time_flag THEN 'ตรงเวลา (On-Time)' ELSE 'ล่าช้า (Delayed)' END as status,
                COUNT(*) as count
            FROM fact_trips_operations
        """)
        if not df_ontime.empty:
            fig_ontime = px.pie(df_ontime, names='status', values='count', hole=0.4, color='status', 
                                color_discrete_map={'ตรงเวลา (On-Time)':'#2CA02C', 'ล่าช้า (Delayed)':'#D62728'})
            st.plotly_chart(fig_ontime, use_container_width=True)

    with col2:
        st.subheader("🛑 จุดกระจายสินค้าที่เป็นคอขวด (Top Bottlenecks)")
        df_bottleneck = run_query("""
            SELECT f.facility_name, AVG(t.detention_minutes) as avg_wait_time
            FROM fact_trips_operations t
            JOIN dim_facilities f ON t.facility_key = f.facility_key
            GROUP BY 1 ORDER BY 2 DESC LIMIT 5
        """)
        if not df_bottleneck.empty:
            fig_bottle = px.bar(df_bottleneck, y='facility_name', x='avg_wait_time', orientation='h', color='avg_wait_time', color_continuous_scale='Reds')
            st.plotly_chart(fig_bottle, use_container_width=True)

    st.markdown("---")
    st.subheader("🌟 Top 10 พนักงานขับรถดีเด่น (วัดจากจำนวนรอบวิ่ง)")
    df_drivers = run_query("""
        SELECT d.first_name || ' ' || d.last_name as driver_name, COUNT(t.trip_key) as total_trips
        FROM fact_trips_operations t
        JOIN dim_drivers d ON t.driver_key = d.driver_key
        GROUP BY 1 ORDER BY 2 DESC LIMIT 10
    """)
    if not df_drivers.empty:
        fig_driver = px.bar(df_drivers, x='total_trips', y='driver_name', orientation='h')
        fig_driver.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_driver, use_container_width=True)


# ---------------------------------------------------------
# หน้าที่ 3: ซ่อมบำรุงและสมรรถนะ
# ---------------------------------------------------------
elif page == "🛠️ ซ่อมบำรุงและสมรรถนะ (Maintenance & Fleet)":
    st.title("🛠️ การซ่อมบำรุงและสมรรถนะรถบรรทุก")
    
    st.subheader("ภาพรวมการซ่อมบำรุงตามช่วงเวลา")
    df_maint_time = run_query("""
        SELECT 
            CAST(d.year AS VARCHAR) || '-' || LPAD(CAST(d.month AS VARCHAR), 2, '0') AS month_year,
            SUM(m.maintenance_cost) as total_cost,
            SUM(m.downtime_hours) as total_downtime
        FROM fact_maintenance m
        JOIN dim_date d ON m.date_key = d.date_key
        GROUP BY 1 ORDER BY 1
    """)
    if not df_maint_time.empty:
        fig_mtime = px.line(df_maint_time, x='month_year', y=['total_cost', 'total_downtime'], markers=True)
        st.plotly_chart(fig_mtime, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔧 ยี่ห้อรถที่มีค่าใช้จ่ายและ Downtime สูงสุด")
        df_make = run_query("""
            SELECT tr.make, SUM(m.maintenance_cost) as cost, SUM(m.downtime_hours) as downtime
            FROM fact_maintenance m
            JOIN dim_trucks tr ON m.truck_key = tr.truck_key
            GROUP BY 1 ORDER BY cost DESC
        """)
        if not df_make.empty:
            fig_make = px.scatter(df_make, x='downtime', y='cost', size='cost', color='make', hover_name='make')
            st.plotly_chart(fig_make, use_container_width=True)

    with col2:
        st.subheader("⚙️ ประเภทการซ่อมบำรุงที่พบบ่อย (สัดส่วน %)")
        df_mtype = run_query("""
            SELECT maintenance_type, COUNT(*) as freq
            FROM fact_maintenance
            GROUP BY 1 ORDER BY 2 DESC
        """)
        if not df_mtype.empty:
            fig_mtype = px.pie(df_mtype, names='maintenance_type', values='freq')
            st.plotly_chart(fig_mtype, use_container_width=True)


# ---------------------------------------------------------
# หน้าที่ 4: น้ำมันและความปลอดภัย
# ---------------------------------------------------------
elif page == "⛽ น้ำมันและความปลอดภัย (Fuel & Safety)":
    st.title("⛽ ต้นทุนเชื้อเพลิงและความปลอดภัย")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⛽ เส้นทางที่มีต้นทุนเชื้อเพลิงเฉลี่ยสูงสุด")
        df_fuel_route = run_query("""
            SELECT r.origin_city || ' -> ' || r.destination_city as route, 
                   AVG(t.fuel_gallons_used) as avg_gallons
            FROM fact_trips_operations t
            JOIN dim_routes r ON t.route_key = r.route_key
            GROUP BY 1 ORDER BY 2 DESC LIMIT 5
        """)
        if not df_fuel_route.empty:
            fig_froute = px.bar(df_fuel_route, x='avg_gallons', y='route', orientation='h', color='avg_gallons')
            fig_froute.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_froute, use_container_width=True)

    with col2:
        st.subheader("⚠️ ประเภทอุบัติเหตุ (Incident Types)")
        df_incident = run_query("""
            SELECT incident_type, COUNT(*) as count
            FROM fact_safety_incidents
            GROUP BY 1 ORDER BY 2 DESC
        """)
        if not df_incident.empty:
            fig_inc = px.bar(df_incident, x='incident_type', y='count', color='incident_type')
            st.plotly_chart(fig_inc, use_container_width=True)

    st.markdown("---")
    st.subheader("🚨 เส้นทางที่เกิดอุบัติเหตุบ่อยที่สุด (High-Risk Routes)")
    df_danger_route = run_query("""
        SELECT r.origin_city || ' -> ' || r.destination_city as route, 
               COUNT(s.incident_key) as total_incidents
        FROM fact_safety_incidents s
        JOIN dim_routes r ON s.route_key = r.route_key
        GROUP BY 1 ORDER BY 2 DESC LIMIT 5
    """)
    if not df_danger_route.empty:
        st.dataframe(df_danger_route, use_container_width=True)