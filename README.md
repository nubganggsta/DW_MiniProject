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
