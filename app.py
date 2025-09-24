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
def to_excel(df):
    output = BytesIO()
    df_copy = df.copy()

    # Pastikan tanggal dalam format datetime
    df_copy["Tanggal"] = pd.to_datetime(df_copy["Tanggal"])

    # Hitung rata-rata per bulan
    df_copy["Bulan"] = df_copy["Tanggal"].dt.to_period("M").astype(str)
    monthly_avg = df_copy.groupby("Bulan")["pH"].mean().reset_index()
    monthly_avg.rename(columns={"pH": "Rata-rata pH"}, inplace=True)

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Sheet 1: Data asli
        df_copy.to_excel(writer, index=False, sheet_name="Data")
        # Sheet 2: Rata-rata per bulan
        monthly_avg.to_excel(writer, index=False, sheet_name="Rata-rata Bulanan")

    return output.getvalue()

excel_file = to_excel(st.session_state["data"])

# Tombol download
st.download_button(
    label="⬇ Download Excel",
    data=excel_file,
    file_name="data_ph_debit.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)



