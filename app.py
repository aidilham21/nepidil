import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import json

st.set_page_config(page_title="Kalkulator Nepi", page_icon="💰")

st.title("💰 Kalkulator Pemasukan & Pengeluaran Nepi")

# Baca credentials dari secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Ganti ini dengan ID Google Sheets kamu
SHEET_ID = "1CRHQlKgtYIzut1BahDqakVjBfRaYCRSCowCuV1u1jAE"
sheet = client.open_by_key(SHEET_ID).worksheet("Data")

# Form input
with st.form("form_input"):
    st.subheader("📝 Masukkan Data Baru")
    jenis = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
    keterangan = st.text_input("Keterangan")
    jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
    submit = st.form_submit_button("Simpan")

    if submit and keterangan and jumlah > 0:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([waktu, jenis, keterangan, jumlah])
        st.success("✅ Data berhasil disimpan ke Google Sheets!")

# Tampilkan riwayat
st.subheader("📄 Riwayat Transaksi (10 Terakhir)")
data = sheet.get_all_records()

if data:
    df = pd.DataFrame(data)
    df['jumlah'] = pd.to_numeric(df['jumlah'])
    df['waktu'] = pd.to_datetime(df['waktu'])

    st.dataframe(df.tail(10)[['waktu', 'jenis', 'keterangan', 'jumlah']], use_container_width=True)

    # Ringkasan
    pemasukan = df[df['jenis'] == 'Pemasukan']['jumlah'].sum()
    pengeluaran = df[df['jenis'] == 'Pengeluaran']['jumlah'].sum()
    sisa = pemasukan - pengeluaran

    st.subheader("📊 Ringkasan:")
    st.write(f"💵 Total Pemasukan: Rp{pemasukan:,.0f}")
    st.write(f"🧾 Total Pengeluaran: Rp{pengeluaran:,.0f}")
    st.success(f"💰 Sisa Uang: Rp{sisa:,.0f}")
else:
    st.info("Belum ada data.")
