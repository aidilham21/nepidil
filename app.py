import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import json

# ------------------ CONFIGURASI HALAMAN ------------------ #
st.set_page_config(page_title="Kalkulator Nepi", page_icon="💰", layout="centered")

# ------------------ CUSTOM CSS ------------------ #
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #FFFDE7; /* kuning pastel */
        color: #212121;
    }

    h1 {
        text-align: center;
        color: #1565C0; /* biru */
    }

    p {
        text-align: center;
        font-size: 16px;
        color: #424242;
        margin-top: -10px;
    }

    .stButton > button {
        background-color: #FFCA28 !important; /* kuning */
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 0.5em 1.2em;
    }

    .stButton > button:hover {
        background-color: #FBC02D !important;
        color: black;
    }

    .st-emotion-cache-1c7y2kd, .st-emotion-cache-1avcm0n {
        border: 1px solid #1565C0;
        border-radius: 10px;
        padding: 1.5rem;
        background-color: #FFFFFF;
    }

    .st-expander {
        background-color: #FFF9C4;
        border: 1px solid #1565C0;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------ #
st.markdown("<h1>💰 Kalkulator Nepi</h1>", unsafe_allow_html=True)
st.markdown("<p>Pantau pemasukan dan pengeluaran dengan warna khas Nepi 💙💛</p>", unsafe_allow_html=True)

# ------------------ GOOGLE SHEETS ------------------ #
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

SHEET_ID = "1CRHQlKgtYIzut1BahDqakVjBfRaYCRSCowCuV1u1jAE"
try:
    sheet = client.open_by_key(SHEET_ID).worksheet("Data")
except gspread.exceptions.WorksheetNotFound:
    sheet = client.open_by_key(SHEET_ID).add_worksheet(title="Data", rows="1000", cols="4")
    sheet.append_row(["waktu", "jenis", "keterangan", "jumlah"])

# ------------------ FORM INPUT ------------------ #
with st.form("form_input", clear_on_submit=True):
    st.subheader("📝 Tambah Transaksi")
    jenis = st.selectbox("Jenis Transaksi", ["Pemasukan", "Pengeluaran"])
    keterangan = st.text_input("Keterangan")
    jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
    submit = st.form_submit_button("💾 Simpan")

    if submit and keterangan and jumlah > 0:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([waktu, jenis, keterangan, jumlah])
        st.success("✅ Data berhasil disimpan!")

# ------------------ AMBIL & TAMPILKAN DATA ------------------ #
try:
    data = sheet.get_all_records()
    if not data:
        headers = sheet.row_values(1)
        if headers != ["waktu", "jenis", "keterangan", "jumlah"]:
            sheet.insert_row(["waktu", "jenis", "keterangan", "jumlah"], 1)
except Exception as e:
    st.error(f"Gagal ambil data: {e}")
    data = []

if data:
    df = pd.DataFrame(data)
    df['jumlah'] = pd.to_numeric(df['jumlah'], errors='coerce').fillna(0)
    df['waktu'] = pd.to_datetime(df['waktu'], errors='coerce')

    pemasukan = df[df['jenis'] == 'Pemasukan']['jumlah'].sum()
    pengeluaran = df[df['jenis'] == 'Pengeluaran']['jumlah'].sum()
    sisa = pemasukan - pengeluaran

    st.markdown("---")
    st.subheader("📊 Ringkasan Keuangan")

    col1, col2, col3 = st.columns(3)
    col1.metric("Pemasukan", f"Rp{pemasukan:,.0f}")
    col2.metric("Pengeluaran", f"Rp{pengeluaran:,.0f}")
    col3.metric("Sisa Uang", f"Rp{sisa:,.0f}")

    with st.expander("📄 Lihat Riwayat Transaksi"):
        st.dataframe(df[['waktu', 'jenis', 'keterangan', 'jumlah']].sort_values(by="waktu", ascending=False),
                     use_container_width=True)
else:
    st.info("Belum ada data transaksi.")

# ------------------ FOOTER ------------------ #
st.markdown("<hr style='margin-top: 30px;'>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; font-size: 13px; color: gray;'>
💙💛 Dibuat oleh Aidil untuk Nepi System • Streamlit + Google Sheets • © 2025
</p>
""", unsafe_allow_html=True)
