import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# Inisialisasi data
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Tanggal", "Lokasi", "pH", "Debit (L/detik)"])

st.title("📊 Pencatatan pH dan Debit Air")

# Form input
with st.form("input_form"):
    tanggal = st.date_input("Tanggal", datetime.today())
    lokasi = st.selectbox("Lokasi", ["power plan", "plan garage", "drain A", "drain B", "drain D"])
    ph = st.number_input("Nilai pH", min_value=0.0, max_value=14.0, step=0.1)
    debit = st.number_input("Debit (L/detik)", min_value=0.0, step=0.1)

    submit = st.form_submit_button("Simpan Data")

# Simpan data
if submit:
    new_data = pd.DataFrame([[tanggal, lokasi, ph, debit]], columns=st.session_state["data"].columns)
    st.session_state["data"] = pd.concat([st.session_state["data"], new_data], ignore_index=True)
    st.success("✅ Data berhasil disimpan!")

# Tampilkan tabel
st.subheader("📑 Data Pencatatan")
st.dataframe(st.session_state["data"], use_container_width=True)

# Hitung rata-rata pH
if not st.session_state["data"].empty:
    avg_ph = st.session_state["data"]["pH"].mean()
    st.metric("📌 Rata-rata pH", f"{avg_ph:.2f}")

# Fungsi export ke Excel
def to_excel_per_lokasi(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for lokasi, data_lokasi in df.groupby("Lokasi"):
            # Pastikan format tanggal
            data_lokasi["Tanggal"] = pd.to_datetime(data_lokasi["Tanggal"])
            
            # Ambil bulan (anggap 1 bulan dalam sekali export)
            bulan = data_lokasi["Tanggal"].dt.to_period("M").iloc[0]
            
            # Hitung rata-rata pH bulanan
            rata_ph = data_lokasi["pH"].mean().round(2)
            
            # Data harian
            data_harian = data_lokasi[["Tanggal", "pH", "Debit"]].copy()
            
            # Tambah baris ringkasan
            summary = pd.DataFrame({
                "Tanggal": [f"Rata-rata pH Bulan {bulan}"],
                "pH": [rata_ph],
                "Debit": [None]
            })
            final_df = pd.concat([data_harian, summary], ignore_index=True)
            
            # Simpan ke sheet sesuai nama lokasi
            final_df.to_excel(writer, sheet_name=lokasi, index=False)
    return output.getvalue()

excel_file = to_excel(st.session_state["data"])

# Tombol download
st.download_button(
    label="⬇ Download Excel",
    data=excel_file,
    file_name="data_ph_debit.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)







