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
    df_copy["Tanggal"] = pd.to_datetime(df_copy["Tanggal"])

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        startrow = 0
        sheet_name = "Data"
        
        for lokasi, data_lokasi in df_copy.groupby("Lokasi"):
            # Hitung rata-rata pH dan Debit lokasi ini
            avg_ph = data_lokasi["pH"].mean()
            avg_debit = data_lokasi["Debit (L/detik)"].mean()

            # Tambahkan kolom rata-rata
            export_df = data_lokasi[["Tanggal", "pH", "Debit (L/detik)"]].copy()
            export_df["Rata-rata pH"] = avg_ph
            export_df["Rata-rata Debit"] = avg_debit

            # Tambahkan header lokasi
            header_df = pd.DataFrame([[f"Lokasi: {lokasi}", "", "", "", ""]],
                                      columns=export_df.columns)

            # Gabungkan header + data
            final_df = pd.concat([header_df, export_df], ignore_index=True)

            # Tulis ke Excel di posisi yang sesuai
            final_df.to_excel(writer, sheet_name=sheet_name,
                              index=False, startrow=startrow)

            # Geser startrow untuk lokasi berikutnya
            startrow += len(final_df) + 3  # kasih jarak 3 baris kosong

    return output.getvalue()

excel_file = to_excel(st.session_state["data"])

# Tombol download
st.download_button(
    label="⬇ Download Excel",
    data=excel_file,
    file_name="data_ph_debit.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)





