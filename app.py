import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📊 Pencatatan pH dan Debit Air", layout="centered")

st.title("📊 Pencatatan pH dan Debit Air")

# ==========================
# Fungsi Export ke Excel
# ==========================
def to_excel_per_lokasi(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for lokasi, data_lokasi in df.groupby("Lokasi"):
            if data_lokasi.empty:
                continue

            data_lokasi = data_lokasi.copy()
            data_lokasi["Tanggal"] = pd.to_datetime(data_lokasi["Tanggal"])

            # Ambil bulan pertama (anggap data dalam sheet 1 bulan)
            bulan = data_lokasi["Tanggal"].dt.to_period("M").iloc[0]

            # Hitung rata-rata pH bulanan
            rata_ph = data_lokasi["pH"].mean().round(2)

            # Data harian
            df_out = data_lokasi[["Tanggal", "pH", "Debit"]].copy()

            # Tambah kolom rata-rata pH
            df_out["Rata-rata pH Bulan " + str(bulan)] = ""

            # Tambahkan baris rata-rata di bawah
            df_out.loc[len(df_out)] = ["", "", "", rata_ph]

            # Simpan per lokasi ke sheet
            df_out.to_excel(writer, sheet_name=str(lokasi), index=False)

    return output.getvalue()


# ==========================
# Simpan Data di Session
# ==========================
if "data" not in st.session_state:
    st.session_state["data"] = []

# ==========================
# Input Data
# ==========================
tanggal = st.date_input("Tanggal pengukuran:")
lokasi = st.selectbox("Pilih lokasi:", ["Power Plant", "Plant Garage", "Drain A", "Drain B", "Drain C"])
ph = st.number_input("Nilai pH:", min_value=0.0, step=0.01)
debit = st.number_input("Nilai Debit:", min_value=0.0, step=0.01)

if st.button("➕ Tambah Data"):
    st.session_state["data"].append({
        "Tanggal": tanggal,
        "Lokasi": lokasi,
        "pH": ph,
        "Debit": debit
    })
    st.success("Data berhasil ditambahkan!")

# ==========================
# Tampilkan Data
# ==========================
if st.session_state["data"]:
    df = pd.DataFrame(st.session_state["data"])
    st.subheader("📋 Data Tercatat")
    st.dataframe(df)

    # ==========================
    # Download Excel
    # ==========================
    st.subheader("💾 Export ke Excel")
    excel_bytes = to_excel_per_lokasi(df)
    st.download_button(
        label="📥 Download Excel per Lokasi",
        data=excel_bytes,
        file_name="data_lokasi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

        
   
        

     
   
  
















