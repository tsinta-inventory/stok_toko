import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Kasir Toko", layout="wide")
st.title("🛒 Kasir Toko Sederhana")

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Link baru yang Anda berikan
url = "https://docs.google.com/spreadsheets/d/10ZsM17t1Yc9wzrbngX1ufIXKcW3fbIaxzlEkUuL4EZo/edit?usp=sharing"

# Membaca Data
try:
    df = conn.read(spreadsheet=url)
except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets. Pastikan link benar dan sudah di-share sebagai Editor. Error: {e}")
    st.stop()

tab1, tab2 = st.tabs(["📦 Cek Stok", "💳 Input Penjualan"])

with tab1:
    st.subheader("Daftar Barang Tersedia")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Data di Google Sheets kosong.")

with tab2:
    st.subheader("Catat Transaksi Baru")
    if not df.empty:
        with st.form("transaksi"):
            # Mengambil daftar produk dari kolom pertama
            list_produk = df.iloc[:, 0].tolist()
            produk = st.selectbox("Pilih Produk", list_produk)
            
            jumlah = st.number_input("Jumlah Beli", min_value=1, step=1)
            submit = st.form_submit_button("Simpan & Potong Stok")

            if submit:
                # Cari baris produk yang dipilih
                idx = df[df.iloc[:, 0] == produk].index[0]
                
                try:
                    # Konversi stok ke angka secara lokal untuk perhitungan
                    stok_sekarang = pd.to_numeric(df.iloc[idx, 1], errors='coerce')
                    
                    if pd.isna(stok_sekarang):
                        st.error("Data stok di Google Sheets bukan angka!")
                    elif stok_sekarang >= jumlah:
                        # Kurangi stok
                        df.iloc[idx, 1] = int(stok_sekarang - jumlah)
                        
                        # Kirim update ke Google Sheets
                        conn.update(spreadsheet=url, data=df)
                        
                        st.success(f"Berhasil! Stok {produk} berkurang. Sisa: {df.iloc[idx, 1]}")
                        st.balloons()
                    else:
                        st.error(f"Stok tidak cukup! Sisa stok: {int(stok_sekarang)}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses data: {e}")
    else:
        st.warning("Tidak ada produk yang bisa dipilih.")
