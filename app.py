import streamlit as st
import pandas as pd
from io import BytesIO

st.title("📊 Pencatatan pH dan Debit Air")

# --- Inisialisasi session state ---
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Tanggal", "Lokasi", "pH", "Debit"])

# --- Input data ---
tanggal = st.date_input("Tanggal pengukuran:")
lokasi = st.selectbox("Pilih lokasi:", ["Power Plant", "Plant Garage", "Drain A", "Drain B", "Drain C"])
ph = st.number_input("Masukkan nilai pH:", min_value=0.0, step=0.1)
debit = st.number_input("Masukkan debit (L/detik):", min_value=0.0, step=0.1)

if st.button("Simpan Data"):
    new_row = pd.DataFrame({"Tanggal": [tanggal], "Lokasi": [lokasi], "pH": [ph], "Debit": [debit]})
    st.session_state["data"] = pd.concat([st.session_state["data"], new_row], ignore_index=True)
    st.success("✅ Data berhasil disimpan!")

# --- Tampilkan data ---
st.subheader("📑 Data Pencatatan")
st.dataframe(st.session_state["data"])

# --- Fungsi export ke Excel ---
def to_excel_per_lokasi(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for lokasi, data_lokasi in df.groupby("Lokasi"):
            data_lokasi = data_lokasi.copy()
            data_lokasi["Tanggal"] = pd.to_datetime(data_lokasi["Tanggal"])
            
            # Tentukan bulan & rata-rata pH
            bulan = data_lokasi["Tanggal"].dt.to_period("M").iloc[0]
            rata_ph = data_lokasi["pH"].mean().round(2)
            
            # Data harian
            data_harian = data_lokasi[["Tanggal", "pH", "Debit"]]
            
            # Baris ringkasan rata-rata
            summary = pd.DataFrame({
                "Tanggal": [f"Rata-rata pH Bulan {bulan}"],
                "pH": [rata_ph],
                "Debit": [None]
            })
            
            # Gabungkan
            final_df = pd.concat([data_harian, summary], ignore_index=True)
            
            # Simpan ke sheet
            final_df.to_excel(writer, sheet_name=lokasi, index=False)
    return output.getvalue()

# --- Tombol download Excel ---
if not st.session_state["data"].empty:
    excel_file = to_excel_per_lokasi(st.session_state["data"])
    st.download_button(
        "⬇ Download Data Semua Lokasi",
        data=excel_file,
        file_name="pengukuran_semua_lokasi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    
   
  








