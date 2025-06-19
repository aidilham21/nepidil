import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import json

st.set_page_config(page_title="Kalkulator Nepi", page_icon="💰")
st.title("💰 Kalkulator Pemasukan & Pengeluaran Nepi")

# Autentikasi Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# ID dan worksheet Google Sheets
SHEET_ID = "1CRHQlKgtYIzut1BahDqakVjBfRaYCRSCowCuV1u1jAE"
try:
    sheet = client.open_by_key(SHEET_ID).worksheet("Data")
except gspread.exceptions.WorksheetNotFound:
    # Buat worksheet jika belum ada
    spreadsheet = client.open_by_key(SHEET_ID)
    sheet = spreadsheet.add_worksheet(title="Data", rows="1000", cols="4")
    sheet.append_row(["waktu", "jenis", "keterangan", "jumlah"])

# Form Input
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

# Ambil data dari Google Sheets
try:
    data = sheet.get_all_records()
if not data:
    # Cek apakah header sudah ada, kalau belum, tambahkan
    headers = sheet.row_values(1)
    expected_headers = ["waktu", "jenis", "keterangan", "jumlah"]
    if headers != expected_headers:
        sheet.insert_row(expected_headers, 1)
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
    data = []

# Tampilkan riwayat
st.subheader("📄 Riwayat Transaksi (10 Terakhir)")

if data:
    df = pd.DataFrame(data)
    df['jumlah'] = pd.to_numeric(df['jumlah'], errors='coerce').fillna(0)
    df['waktu'] = pd.to_datetime(df['waktu'], errors='coerce')

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
    st.info("Belum ada data transaksi. Silakan masukkan data pertama kamu.")
