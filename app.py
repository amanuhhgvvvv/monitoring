import streamlit as st
import pandas as pd
import openpyxl
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

# Fungsi buat file Excel
def buat_file_excel(data_dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for loc, records in data_dict.items():
            if not records:
                continue
            df = pd.DataFrame(records)
            df["Tanggal"] = pd.to_datetime(df["Tanggal"])

            # Hitung rata-rata pH
            rata_ph = df["pH"].mean()

            # Tambahkan kolom kosong rata-rata
            df["Rata-rata pH"] = ""

            # Tambahkan baris rata-rata
            total_row = {
                "Tanggal": "TOTAL",
                "pH": "",
                "Debit": "",
                "Rata-rata pH": round(rata_ph, 2)
            }
            df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

            # Simpan ke Excel
            df.to_excel(writer, sheet_name=loc, index=False)

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
        
        
   
        

     
   
  


















