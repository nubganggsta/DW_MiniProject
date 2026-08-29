# DW_MiniProject
for do midterm project

# Introduce our group
Nattida Jantasopa 673020044-1

Chutima Boottanai 673020248-5

Jinrada Sai-Udta 673020489-3

Nanadda Rattanasri 673020490-8

Thitisuda Daengseeda 673020491-6

Phlapapon Kulto 673020626-9

## 🏗 Architecture & Design Principles

การออกแบบสถาปัตยกรรมข้อมูลในโปรเจกต์นี้ปฏิบัติตามมาตรฐาน **Kimball Data Warehousing Methodology**:

1. **Strict Star Schema Boundaries:** แยกตารางอย่างเด็ดขาดระหว่าง **Dimension Tables** และ **Fact Tables**
2. **No Fact-to-Fact Joins:** ป้องกันปัญหา *Fan Trap* และ *Double Counting* โดยยกเลิกการเชื่อมต่อความสัมพันธ์ระหว่าง Fact Tables โดยตรง แต่เชื่อมโยงผ่าน Shared (Conformed) Dimensions แทน
3. **Degenerate Dimensions:** คงค่ารหัสธุรกรรม เช่น `Trip_ID` และ `Load_ID` ไว้ใน Fact Tables เป็น Degenerate Keys เพื่อประโยชน์ในการ Traceability และ Drill-through Analysis
4. **Conformed Dimensions:** ใช้ `Dim_Date`, `Dim_Truck`, `Dim_Driver`, และ `Dim_Customer` ร่วมกันในหลาย Fact Tables เพื่อให้วิเคราะห์ข้อมูลข้ามโดเมนได้ (เช่น เปรียบเทียบรายได้ ค่าน้ำมัน และอุบัติเหตุต่อ Truck/Driver)

---
## Business Questions
1. รายได้รวมของบริษัทในแต่ละปีมีแนวโน้มอย่างไร และธุรกิจเติบโตขึ้นหรือไม่
2. เดือนหรือช่วงเวลาใดสร้างรายได้สูงที่สุด 
3. ลูกค้ารายใดสร้างรายได้ให้บริษัทมากที่สุด
4. เส้นทางใดมีปริมาณงานสูงที่สุด
5. รถบรรทุกคันใดมีประสิทธิภาพการใช้งานสูงสุดที่สุดและต่ำที่สุด เมื่อพิจารณาจากระยะทาง จำนวนเที่ยว และเวลาที่ใช้งาน
6. คนขับคนใดมีประสิทธิภาพในการทำงานสูงที่สุด เมื่อพิจารณาจากจำนวนเที่ยว ระยะทาง การส่งตรงเวลา และรายได้ที่สร้าง
7. ต้นทุนน้ำมันของบริษัทในแต่ละเดือนและแต่ละปีเป็นอย่างไร
8. รถบรรทุกคันใดมีค่าใช้จ่ายค่าน้ำมันมากที่สุด
9. รถบรรทุกคันใดมีค่าใช้จ่ายในการซ่อมบำรุงสูงที่สุด
10. ค่าใช้จ่ายในการซ่อมบำรุงรวมของบริษัทในแต่ละปีเป็นเท่าไร
11. บริษัทมีอัตราการส่งสินค้าตรงเวลา คิดเป็นกี่เปอร์เซ็นต์
12. ศูนย์กระขายสินค้าใดมีจำนวนการส่งสินค้าล่าช้ามากที่สุด
13. ระยะเวลาส่งจริงมีความแตกต่างจากเวลาที่วางแผนไว้โดยเฉลี่ยกี่นาที
14. ปีใดมีจำนวน Safety Incident มากที่สุด
15. Safety Incident ประเภทใดเกิดขึ้นบ่อยที่สุด
    

## Data Model Diagram
<img width="1942" height="1301" alt="Logistic_DataWarehouse-ER_OLTP" src="https://github.com/user-attachments/assets/fc02de57-2230-4ca9-8df6-9b931b5ad4cd" />

### รายละเอียดชุดข้อมูล 
ชุดข้อมูล Logistics Operations Database (2022–2024) บน Kaggle เป็นฐานข้อมูลจำลองการทำงานจริงของบริษัทรถบรรทุกขนาดใหญ่ (Class 8) ในสหรัฐฯ ครอบคลุมระยะเวลา 3 ปี รวมกว่า 85,000 ระเบียนใน 14 ตารางที่เชื่อมโยงกัน ออกแบบจากประสบการณ์จริง 12 ปีในสายงานโลจิสติกส์ เพื่อแก้ปัญหาความขาดแคลนชุดข้อมูลที่ซับซ้อนสมจริงโดยไม่ติดปัญหาความลับทางธุรกิจ (NDA)
### โครงสร้างข้อมูล 14 ตาราง
ข้อมูลอ้างอิงหลัก (Core Entities): Drivers (คนขับ 150 คน), Trucks (รถบรรทุก 120 คัน), Trailers (หางลาก/รถพ่วง 180 คัน), Customers (ลูกค้า 200 ราย), Facilities (ศูนย์กระจายสินค้า/คลัง 50 แห่ง), Routes (เส้นทาง 60+ เส้นทาง)
รายการปฏิบัติการ (Transactions): Loads (รายการรับสินค้า 57k+ รายการ), Trips (เที่ยววิ่ง 57k+ รายการ), Fuel Purchases (การเติมน้ำมัน 131k+ รายการ), Maintenance (ประวัติซ่อมบำรุง 6.5k+ รายการ), Delivery Events (สถานะการส่งมอบ 114k+ รายการ), Incidents (อุบัติเหตุ/ข้อผิดพลาด 114 รายการ)
ข้อมูลสรุปเพื่อการวิเคราะห์ (Aggregated Metrics): Driver Monthly Metrics (สรุปรายเดือนคนขับ 5.4k+ รายการ), Truck Utilization Metrics (สรุปการใช้รถ 3.8k+ รายการ)
#### โครงสร้างฐานข้อมูลแบ่งตามหน้าที่ทางธุรกิจออกเป็น 3 กลุ่มหลัก รวม 14 ตาราง โดยมีรายละเอียดตารางและ Attributes ดังนี้
1. กลุ่มข้อมูลหลักและทรัพยากร (Master & Entity Data) เก็บข้อมูลพื้นฐานของทรัพย์สิน บุคลากร ลูกค้า และเส้นทาง เพื่อใช้อ้างอิงในกิจกรรมอื่นๆ
Customers (ข้อมูลลูกค้า/ผู้ว่าจ้าง)
Customer_id: รหัสลูกค้า (PK)
Customer_name / Customer_type: ชื่อลูกค้า และประเภทธุรกิจลูกค้า
Credit_terms_days: ระยะเวลาเครดิตเทอมชำระเงิน (วัน)
Primary_freight_type: ประเภทสินค้าหลักที่ว่าจ้างขนส่ง
Account_status: สถานะบัญชีลูกค้า (เช่น Active, Inactive)
Contract_starts_date: วันเริ่มสัญญา
Annual_revenue_potential: ประมาณการรายได้ต่อปีจากลูกค้ารายนี้

Facilities (ศูนย์กระจายสินค้า/คลังสินค้า)
Facility_id: รหัสสถานที่ (PK)
Facility_name: ชื่อศูนย์/คลังสินค้า
City / State: เมือง และรัฐที่ตั้ง
Latitude / Longitude: พิกัดภูมิศาสตร์
Dock_doors: จำนวนช่องโหลดสินค้า
Operating_hours: เวลาทำการ
Routes (เส้นทางขนส่งมาตรฐาน)
Route_id: รหัสเส้นทาง (PK)
Origin_city / Origin_state: เมืองและรัฐต้นทาง
Destination_city / Destination_state: เมืองและรัฐปลายทาง
Typical_distance_miles: ระยะทางมาตรฐาน (ไมล์)
Base_rate_per_mile: ค่าบริการพื้นฐานต่อไมล์
Fuel_surcharge_rate: อัตราค่าธรรมเนียมน้ำมันผันแปร
Typical_transit_days: ระยะเวลาเดินทางมาตรฐาน (วัน)

Drivers (ข้อมูลพนักงานขับรถ)
Driver_id: รหัสพนักงานขับรถ (PK)
First_name / Last_name: ชื่อ-นามสกุล
Hire_date / Termination_date: วันเข้าทำงาน และวันออก (ถ้ามี)
License_number / License_state: เลขใบขับขี่ และรัฐที่ออกใบอนุญาต
Date_of_birth: วันเกิด
Home_terminal: ศูนย์ปฏิบัติการหลักที่สังกัด
Employment_status: สถานะการทำงาน
Trucks (ข้อมูลรถบรรทุก)
Truck_id: รหัสรถบรรทุก (PK)
Unit_number: หมายเลขประจำรถ
Make / Model_year: ยี่ห้อ และปีที่ผลิต
Vin: เลขตัวรถ (Vehicle Identification Number)
Acquisition_date / Acquisition_mileage: วันที่จัดซื้อ และเลขไมล์ ณ วันซื้อ
Fuel_type / Tank_capacity_gallons: ประเภทน้ำมัน และความจุถังน้ำมัน (แกลลอน)
Status: สถานะรถ (เช่น พร้อมใช้งาน, ซ่อมบำรุง)

Trailers (ข้อมูลหางลาก/ตู้พ่วง)
Trailer_id: รหัสหางลาก (PK)
Trailer_number / Trailer_type: หมายเลขหางลาก และประเภทตู้ (เช่น Dry Van, Reefer)
Length_feet: ความยาวตู้ (ฟุต)
Model_year / Vin: ปีที่ผลิต และเลขตัวถัง
Acquisition_date: วันที่จัดซื้อ
Status / Current_location: สถานะใช้งาน และสถานที่อยู่ปัจจุบัน

3. กลุ่มรายการปฏิบัติการและค่าใช้จ่าย (Transactional Data) บันทึกเหตุการณ์ที่เกิดขึ้นจริงในการทำงานแต่ละวัน
Loads (ใบสั่งงาน/ภาระสินค้า)
Load_id: รหัสใบสั่งงาน (PK)
Load_date: วันที่รับออเดอร์
Load_type: ประเภทการบรรทุก (เช่น Full Truckload - FTL)
Weight_lbs / Pieces: น้ำหนัก (ปอนด์) และจำนวนชิ้นสินค้า
Revenue / Fuel_surcharge / Accessorial_charges: ค่าขนส่งหลัก, ค่าธรรมเนียมน้ำมัน, และค่าบริการเพิ่มเติม

Trips (เที่ยววิ่งจริง)
Trip_id: รหัสเที่ยววิ่ง (PK)
Dispatch_date: วันที่ปล่อยรถออกปฏิบัติงาน
Actual_distance_miles / Actual_duration_hours: ระยะทางจริง (ไมล์) และเวลาที่ใช้จริง (ชั่วโมง)
Fuel_gallons_used / Average_mpg: ปริมาณน้ำมันที่ใช้ และอัตราสิ้นเปลืองเฉลี่ย (ไมล์/แกลลอน)
Idle_time_hours: เวลาที่จอดสตาร์ทเครื่องทิ้งไว้
Trip_status: สถานะเที่ยววิ่ง (เช่น Completed, In Transit)

Delivery_events (สถานะจุดรับ-ส่งสินค้า)
Event_id: รหัสเหตุการณ์ (PK)
Event_type: ประเภทเหตุการณ์ (เช่น Pickup, Delivery)
Scheduled_datetime / Actual_datetime: เวลาที่นัดหมาย และเวลาที่ไปถึงจริง
Detention_minutes: เวลาที่ต้องรอคอย ณ จุดรับส่ง (นาที)
On_time_flag: ตัวชี้วัดการตรงต่อเวลา (Yes/No)
Location_city: เมืองที่เกิดเหตุการณ์

Fuel_purchases (ประวัติการเติมน้ำมัน)
Fuel_purchases_id: รหัสการซื้อน้ำมัน (PK)
Purchase_date: วันที่ซื้อ
Location_city / Location_state: สถานีบริการน้ำมัน (เมือง/รัฐ)
Gallons / Price_per_gallons: จำนวนแกลลอน และราคาต่อแกลลอน
Total_cost: ค่าใช้จ่ายน้ำมันรวม
Maintenance_records (ประวัติการซ่อมบำรุง)
Maintenance_id: รหัสการซ่อมบำรุง (PK)
Maintenance_date / Maintenance_type: วันที่ซ่อม และประเภทการซ่อม (เช่น สี่งซ่อมตามระยะ Preventive, ซ่อมฉุกเฉิน)
Odometer_reading: เลขไมล์ขณะเข้าซ่อม
Labor_hours / Labor_cost / Parts_cost / Total_cost: ชั่วโมงแรงงานช่าง, ค่าแรง, ค่าอะไหล่ และราคารวม
Facility_location: สถานที่ซ่อมบำรุง

Safety_incidents (บันทึกอุบัติเหตุและความเสี่ยง)
Incident_id: รหัสเหตุการณ์อุบัติเหตุ (PK)
Incident_date / Incident_type: วันที่เกิดเหตุ และประเภทอุบัติเหตุ
Location_city: เมืองที่เกิดเหตุ
At_fault_flag: ตัวระบุความผิด (ใช่/ไม่ใช่)
Injury_flag: ตัวระบุการบาดเจ็บ (มี/ไม่มี)
4. กลุ่มข้อมูลสรุปตัววัดผล (Aggregated Analytics Data) ตารางคำนวณสรุปรายเดือนเพื่อใช้ทำ KPI แดชบอร์ด และรายงานผู้บริหาร
Driver_monthly_metrics (สรุปผลงานคนขับรายเดือน)
Driver_id + Month: รหัสพนักงาน และเดือนที่สรุป (Composite Keys)
Trips_completed / Total_miles: จำนวนเที่ยววิ่งที่สำเร็จ และระยะทางรวม
Total_revenue: รายได้รวมที่คนขับทำได้
Average_mpg / Total_fuel_gallons: ประสิทธิภาพประหยัดน้ำมันเฉลี่ย และปริมาณน้ำมันรวม
On_time_delivery_rate: อัตราการส่งสินค้าตรงเวลา (%)
Average_idle_hours: เวลาจอดติดเครื่องเฉลี่ย

Truck_utilization_metrics (สรุปการใช้งานรถบรรทุกรายเดือน)
Truck_id + Month: รหัสรถบรรทุก และเดือนที่สรุป (Composite Keys)
Trips_completed / Total_miles / Total_revenue: งานรวม, ระยะทางรวม, รายได้รวมของรถคันนั้น
Average_mpg: อัตราสิ้นเปลืองน้ำมันเฉลี่ยของรถ
Maintenance_events / Maintenance_cost: จำนวนครั้งเข้าซ่อม และค่าซ่อมบำรุงรวม
Downtime_hours: จำนวนชั่วโมงที่รถต้องจอดซ่อม (ใช้งานไม่ได้)
Utilization_rate: อัตราการถูกนำไปใช้งานจริงเทียบกับเวลาทั้งหมด (%)

### การดำเนินงานของธุรกิจ Logistics
Step 1: ตั้งต้นจากลูกค้าและการจองงาน (Demand Generation)
เริ่มที่ Customers สั่งงานเกิดเป็น Loads ผ่าน Routes และ Facilities

Step 2: การจัดสรรทรัพยากร (Execution Setup)
อธิบายว่า Loads ถูกแปลงเป็น Trips โดยจับคู่ทรัพยากร 3 อย่างเข้าด้วยกันคือ Drivers + Trucks + Trailers

Step 3: บันทึกเหตุการณ์ระหว่างทาง (Operational Events & Expenses)
การวิ่งรถสร้างข้อมูล 3 ด้าน: เวลาจัดส่ง (Delivery Events), ต้นทุนผันแปร (Fuel Purchases), และความเสี่ยง (Maintenance Records & Safety Incidents)

Step 4: การวัดผลทางธุรกิจ (Business Intelligence Output)
สรุปข้อมูลธุรกรรมทั้งหมดกลับมาเป็น Driver Monthly Metrics และ Truck Utilization Metrics เพื่อตอบโจทย์บริหาร เช่น การวัด Fleet Utilization (เฉลี่ย 65%) หรือ Driver Turnover Rate (15%)



## ETL หรือ ELT Process

## Data Warehouse Database

## Interactive Dashboard
