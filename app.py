import streamlit as st

st.title("💰 Kalkulator Pemasukan & Pengeluaran Nepi")

st.markdown("Masukkan daftar pemasukan dan pengeluaran Nepi, lalu lihat total sisa uangnya.")

st.header("📥 Input Pemasukan")
pemasukan_data = []
jumlah_pemasukan = st.number_input("Berapa banyak item pemasukan?", min_value=1, max_value=20, step=1)

for i in range(jumlah_pemasukan):
    with st.expander(f"Pemasukan #{i+1}"):
        keterangan = st.text_input(f"Keterangan Pemasukan #{i+1}", key=f"pemasukan_ket_{i}")
        jumlah = st.number_input(f"Jumlah (Rp)", key=f"pemasukan_jml_{i}", min_value=0)
        pemasukan_data.append({"keterangan": keterangan, "jumlah": jumlah})

st.header("📤 Input Pengeluaran")
pengeluaran_data = []
jumlah_pengeluaran = st.number_input("Berapa banyak item pengeluaran?", min_value=1, max_value=20, step=1)

for i in range(jumlah_pengeluaran):
    with st.expander(f"Pengeluaran #{i+1}"):
        keterangan = st.text_input(f"Keterangan Pengeluaran #{i+1}", key=f"pengeluaran_ket_{i}")
        jumlah = st.number_input(f"Jumlah (Rp)", key=f"pengeluaran_jml_{i}", min_value=0)
        pengeluaran_data.append({"keterangan": keterangan, "jumlah": jumlah})

# Tombol Hitung
if st.button("🔍 Hitung Total"):
    total_pemasukan = sum(item["jumlah"] for item in pemasukan_data)
    total_pengeluaran = sum(item["jumlah"] for item in pengeluaran_data)
    sisa_uang = total_pemasukan - total_pengeluaran

    st.subheader("📊 Rangkuman Pemasukan")
    for item in pemasukan_data:
        st.write(f"- {item['keterangan']}: Rp{item['jumlah']:,}")
    st.write(f"**Total Pemasukan: Rp{total_pemasukan:,}**")

    st.subheader("📉 Rangkuman Pengeluaran")
    for item in pengeluaran_data:
        st.write(f"- {item['keterangan']}: Rp{item['jumlah']:,}")
    st.write(f"**Total Pengeluaran: Rp{total_pengeluaran:,}**")

    st.subheader("💵 Sisa Uang")
    st.success(f"Rp{sisa_uang:,}")
