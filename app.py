import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from io import BytesIO

st.title("📊 Monitoring pH & Debit Air")

# Daftar lokasi
lokasi_list = ["Power Plant", "Plant Garage", "Drain A", "Drain B", "Drain C"]

# Input data harian
st.subheader("✍ Input Data Harian")
tanggal = st.date_input("Tanggal pengukuran")
lokasi = st.selectbox("Pilih lokasi:", lokasi_list)
ph = st.number_input("Masukkan nilai pH", min_value=0.0, step=0.01)
debit = st.number_input("Masukkan nilai debit (L/detik)", min_value=0.0, step=0.01)

# Simpan data ke session_state
if "data" not in st.session_state:
    st.session_state.data = {loc: [] for loc in lokasi_list}

if st.button("Simpan Data"):
    st.session_state.data[lokasi].append({
        "Tanggal": tanggal,
        "pH": ph,
        "Debit": debit
    })
    st.success(f"Data untuk {lokasi} berhasil disimpan!")

# Tampilkan data sementara
st.subheader("📋 Data Tersimpan")
for loc, records in st.session_state.data.items():
    if records:
        st.write(f"### {loc}")
        st.dataframe(pd.DataFrame(records))

# Fungsi buat file Excel dengan nama lokasi di atas tabel
def buat_file_excel(data_dict):
    output = BytesIO()
    wb = Workbook()
    wb.remove(wb.active)  # hapus sheet default

    for loc, records in data_dict.items():
        if not records:
            continue
        ws = wb.create_sheet(title=loc)

        df = pd.DataFrame(records)
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])

        # Hitung rata-rata pH
        rata_ph = df["pH"].mean()

        # Tambahkan kolom kosong rata-rata
        df["Rata-rata pH"] = ""

        # Tambahkan baris total
        total_row = {
            "Tanggal": "TOTAL",
            "pH": "",
            "Debit": "",
            "Rata-rata pH": round(rata_ph, 2)
        }
        df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

        # Tambahkan judul lokasi di baris pertama
        ws.append([f"Lokasi: {loc}"])
        ws.append([])  # baris kosong

        # Tulis DataFrame ke sheet
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)

    wb.save(output)
    output.seek(0)
    return output

# Tombol download
if st.button("Download Excel"):
    excel_file = buat_file_excel(st.session_state.data)
    st.download_button(
        label="⬇ Download File Excel",
        data=excel_file,
        file_name="monitoring_ph_debit.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

        

















