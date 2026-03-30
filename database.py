"""
database.py - SQLite database module for Inventory Manager
"""

import sqlite3
import csv
import os
from kivy.utils import platform


def get_db_path():
    if platform == "android":
        from android.storage import app_storage_path  # type: ignore
        return os.path.join(app_storage_path(), "inventory.db")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.db")


PICKER_MAP = {
    101: "SHAMEER OTP",
    102: "NIYAS",
    103: "NIYAS",
    104: "SHAMEER OTP",
    105: "NIYAS",
    106: "NIYAS",
    107: "SHAMEER OTP",
    108: "SHAMEER OTP",
    112: "SAIFUL",
    113: "ASIF",
    114: "ASIF",
    115: "ASIF",
    124: "SAIFUL",
    125: "SHOAIB",
    126: "SHOAIB",
    127: "SHOAIB",
    128: "SAIFUL",
    129: "SAIFUL",
    130: "SHAMEER OTP",
    131: "SALEEM",
    132: "SAIFUL",
    133: "Y BASHEER",
    134: "NIYAS",
    135: "RASHID",
    136: "RASHID",
    137: "RASHID",
    138: "RASHID",
    139: "AZIZ",
    140: "RASIK",
    141: "NIHAL",
    142: "SALEEM",
    143: "VISHNU",
    900: "Y BASHEER",
    146: "NIYAS",
    147: "SAIFUL",
    148: "SAIFUL",
    149: "SAIFUL",
    150: "SAIFUL",
}


def get_connection():
    return sqlite3.connect(get_db_path())


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS item_master (
            item_no TEXT PRIMARY KEY,
            barcode TEXT,
            description TEXT,
            category_code INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS picker_assignments (
            category_code INTEGER PRIMARY KEY,
            picker_name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_no TEXT,
            barcode TEXT,
            description TEXT,
            category_code INTEGER,
            picker_name TEXT,
            from_bin TEXT,
            to_bin TEXT,
            qty REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Populate picker_assignments from PICKER_MAP
    for code, name in PICKER_MAP.items():
        cur.execute(
            "INSERT OR REPLACE INTO picker_assignments (category_code, picker_name) VALUES (?, ?)",
            (code, name),
        )

    conn.commit()
    conn.close()


def import_item_master(csv_path):
    """Import/replace item master from a CSV file.

    CSV must have columns: item_no, barcode, description, category_code
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM item_master")

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append((
                row["item_no"].strip(),
                row["barcode"].strip(),
                row["description"].strip(),
                int(row["category_code"].strip()),
            ))

    cur.executemany(
        "INSERT OR REPLACE INTO item_master (item_no, barcode, description, category_code) VALUES (?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    conn.close()
    return len(rows)


def get_item_by_barcode(barcode):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT item_no, barcode, description, category_code FROM item_master WHERE barcode = ?", (barcode,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"item_no": row[0], "barcode": row[1], "description": row[2], "category_code": row[3]}
    return None


def get_item_by_itemno(item_no):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT item_no, barcode, description, category_code FROM item_master WHERE item_no = ?", (item_no,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"item_no": row[0], "barcode": row[1], "description": row[2], "category_code": row[3]}
    return None


def get_picker_for_category(category_code):
    try:
        code = int(category_code)
    except (ValueError, TypeError):
        return "UNKNOWN"
    return PICKER_MAP.get(code, "UNKNOWN")


def insert_transaction(item_no, barcode, description, category_code, picker_name, from_bin, to_bin, qty):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO transactions
           (item_no, barcode, description, category_code, picker_name, from_bin, to_bin, qty)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (item_no, barcode, description, category_code, picker_name, from_bin, to_bin, qty),
    )
    conn.commit()
    trans_id = cur.lastrowid
    conn.close()
    return trans_id


def get_all_transactions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, item_no, barcode, description, category_code, picker_name,
                  from_bin, to_bin, qty, created_at
           FROM transactions ORDER BY created_at DESC"""
    )
    rows = cur.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "item_no": row[1],
            "barcode": row[2],
            "description": row[3],
            "category_code": row[4],
            "picker_name": row[5],
            "from_bin": row[6],
            "to_bin": row[7],
            "qty": row[8],
            "created_at": row[9],
        })
    return result


def update_transaction(trans_id, from_bin, to_bin, qty):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE transactions SET from_bin=?, to_bin=?, qty=? WHERE id=?",
        (from_bin, to_bin, qty, trans_id),
    )
    conn.commit()
    conn.close()


def delete_transaction(trans_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
    conn.commit()
    conn.close()


def get_analytics():
    """Returns per-picker analytics dict.

    Each entry: {picker_name: {total_items, total_qty, refilled, newly_added}}
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT picker_name,
                  COUNT(*) AS total_items,
                  COALESCE(SUM(qty), 0) AS total_qty,
                  SUM(CASE WHEN from_bin != 'IN0001' THEN 1 ELSE 0 END) AS refilled,
                  SUM(CASE WHEN from_bin = 'IN0001' THEN 1 ELSE 0 END) AS newly_added
           FROM transactions
           GROUP BY picker_name
           ORDER BY total_items DESC"""
    )
    rows = cur.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "picker_name": row[0],
            "total_items": row[1],
            "total_qty": row[2],
            "refilled": row[3],
            "newly_added": row[4],
        })
    return result
