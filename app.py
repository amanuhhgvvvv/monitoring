import pandas as pd
from openpyxl import load_workbook

# Baca data utama
df = pd.read_excel("data_input.xlsx")  # ganti dengan file data kamu

# Pastikan Tanggal benar jadi datetime
df["Tanggal"] = pd.to_datetime(df["Tanggal"]).dt.date  # hilangkan jam 00:00:00

# Buat file Excel output
with pd.ExcelWriter("output_lokasi.xlsx", engine="openpyxl") as writer:
    for lokasi, data_lokasi in df.groupby("Lokasi"):
        # Urutkan berdasarkan tanggal
        data_lokasi = data_lokasi.sort_values("Tanggal")

        # Hitung rata-rata pH bulanan
        rata_ph = data_lokasi["ph"].mean()

        # Buat salinan data harian
        data_lokasi_out = data_lokasi[["Tanggal", "ph", "debit"]].copy()
        data_lokasi_out["Rata-rata pH Bulan"] = ""

        # Isi rata-rata hanya di baris terakhir
        data_lokasi_out.loc[data_lokasi_out.index[-1], "Rata-rata pH Bulan"] = round(rata_ph, 2)

        # Tulis ke Excel mulai baris ke-2 (biar baris pertama bisa dipakai untuk judul lokasi)
        data_lokasi_out.to_excel(writer, sheet_name=lokasi, index=False, startrow=2)

        # Tambahkan judul lokasi di baris pertama
        ws = writer.sheets[lokasi]
        ws.cell(row=1, column=1).value = f"Lokasi: {lokasi}"
  
        
   
        

     
   
  

















