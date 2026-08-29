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
## ETL หรือ ELT Process

## Data Warehouse Database

## Interactive Dashboard
