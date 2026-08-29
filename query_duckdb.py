import duckdb
import pandas as pd
from pathlib import Path

# 1. กำหนด Base Path และโฟลเดอร์ต่างๆ แบบ Absolute Path ป้องกันปัญหา Relative Path หลุด
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "fiveGexpress_duckdb" / "dev.duckdb"
DATASETS_DIR = BASE_DIR / "fiveGexpress_duckdb" / "datasets"

# เชื่อมต่อ Database
conn = duckdb.connect(str(DB_PATH))

# 2. ตั้งค่า search_path ใน DuckDB ให้ชี้ไปยังโฟลเดอร์ datasets โดยตรง
conn.execute(f"SET FILE_SEARCH_PATH = '{DATASETS_DIR.as_posix()}'")

all_tables_df = conn.execute(
    """
    SELECT table_schema, table_name, table_type
    FROM information_schema.tables
    WHERE table_schema = 'main'
      AND table_name NOT LIKE 'sqlite_%'
    ORDER BY table_name
    """
).fetch_df()

print("Tables in dev.duckdb:")
print(all_tables_df.to_string(index=False))

print("\n" + "=" * 80)
print("CSV files in datasets folder:")
print("=" * 80)
if DATASETS_DIR.exists():
    for csv_file in sorted(DATASETS_DIR.glob("*.csv")):
        print(f"  - {csv_file.name}")
else:
    print(f"Directory not found: {DATASETS_DIR}")

print("\n" + "=" * 80)
print("Preview: stg_customers")
print("=" * 80)

try:
    result = conn.execute('SELECT * FROM "main"."stg_customers" LIMIT 20').fetchall()
except Exception as e:
    msg = str(e)
    if "No files found that match the pattern" in msg or "IO Error" in msg:
        # ค้นหาไฟล์ customers.csv จากโฟลเดอร์ datasets แบบเจาะจง
        candidates = list(DATASETS_DIR.glob("*customer*.csv")) + list(DATASETS_DIR.glob("*customers*.csv"))
        if not candidates:
            raise RuntimeError(f"ไม่พบไฟล์ CSV ของ customers ใน {DATASETS_DIR}") from e
        
        csv_path = candidates[0].resolve()
        # Recreate View โดยใช้ Absolute Path (as_posix() เพื่อรองรับ Slash ของทุก OS)
        conn.execute(
            f'CREATE OR REPLACE VIEW "main"."stg_customers" AS SELECT * FROM read_csv_auto(\'{csv_path.as_posix()}\')'
        )
        result = conn.execute('SELECT * FROM "main"."stg_customers" LIMIT 20').fetchall()
    else:
        raise

df = pd.DataFrame(result, columns=[desc[0] for desc in conn.description])
print(df)

conn.close()