
import streamlit as st
import sqlite3
from datetime import date, time
from pathlib import Path

st.set_page_config(
    page_title="MediMate",
    page_icon="💊",
    layout="centered"
)

DB_PATH = Path(__file__).with_name("medimate.db")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                start_date TEXT NOT NULL,
                reminder_time TEXT NOT NULL
            )
        """)


def get_medicines():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT id, name, dosage, start_date, reminder_time
            FROM medicines
            ORDER BY start_date, reminder_time
        """).fetchall()


def add_medicine(name, dosage, start_date, reminder_time):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO medicines
            (name, dosage, start_date, reminder_time)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            dosage,
            start_date.isoformat(),
            reminder_time.strftime("%H:%M")
        ))


def delete_medicine(medicine_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM medicines WHERE id = ?",
            (medicine_id,)
        )


init_db()

st.title("💊 MediMate")
st.subheader("Smart Medicine Reminder")
st.write("Organise your medicine schedule in one place.")

st.info("Keep your medicine schedule updated.")

st.markdown("### ➕ Add Medicine")

with st.form("medicine_form", clear_on_submit=True):
    name = st.text_input("Medicine name")
    dosage = st.text_input("Dosage instructions")
    start_date = st.date_input(
        "Start date",
        value=date.today()
    )
    reminder_time = st.time_input(
        "Reminder time",
        value=time(8, 0)
    )

    submitted = st.form_submit_button("Save Reminder")

    if submitted:
        if name.strip() and dosage.strip():
            add_medicine(
                name.strip(),
                dosage.strip(),
                start_date,
                reminder_time
            )
            st.success("Medicine added successfully!")
            st.rerun()
        else:
            st.warning(
                "Enter medicine name and dosage instructions."
            )

st.divider()
st.markdown("### 📋 My Medicines")

search = st.text_input("🔎 Search medicine")
medicines = get_medicines()

if search.strip():
    medicines = [
        med for med in medicines
        if search.lower() in med[1].lower()
    ]

if not medicines:
    st.write(
        "No medicines found. Add your first medicine above."
    )

for med in medicines:
    with st.container(border=True):
        st.markdown(f"**💊 {med[1]}**")
        st.write(f"Dosage: {med[2]}")
        st.write(f"Start date: {med[3]}")
        st.write(f"Reminder time: {med[4]}")

        if st.button("Delete", key=f"delete_{med[0]}"):
            delete_medicine(med[0])
            st.rerun()
          
  
