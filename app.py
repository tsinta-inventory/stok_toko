import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Kasir Toko", layout="wide")
st.title("🛒 Kasir Toko Sederhana")

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/10ZsM17t1Yc9wzrbngX1ufIXKcW3fbIaxzlEkUuL4EZo/edit?usp=sharing"

# Membaca Data
try:
    # Membaca semua kolom agar tidak bingung
    df = conn.read(spreadsheet=url)
except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets: {e}")
    st.stop()

tab1, tab2 = st.tabs(["📦 Cek Stok", "💳 Input Penjualan"])

with tab1:
    st.subheader("Daftar Barang Tersedia")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Data kosong.")

with tab2:
    st.subheader("Catat Transaksi Baru")
    if not df.empty:
        with st.form("transaksi"):
            # Pilih produk berdasarkan 'Nama Barang' (Kolom B)
            list_produk = df['Nama Barang'].tolist()
            produk = st.selectbox("Pilih Produk", list_produk)
            
            jumlah = st.number_input("Jumlah Beli", min_value=1, step=1)
            submit = st.form_submit_button("Simpan & Potong Stok")

            if submit:
                # Cari baris produk
                idx = df[df['Nama Barang'] == produk].index[0]
                
                try:
                    # Ambil nilai dari kolom 'Stok' (Kolom D)
                    stok_sekarang = pd.to_numeric(df.at[idx, 'Stok'], errors='coerce')
                    
                    if pd.isna(stok_sekarang):
                        st.error(f"Data stok untuk {produk} di kolom D bukan angka!")
                    elif stok_sekarang >= jumlah:
                        # Potong stok di kolom 'Stok'
                        df.at[idx, 'Stok'] = int(stok_sekarang - jumlah)
                        
                        # Update ke Google Sheets
                        conn.update(spreadsheet=url, data=df)
                        
                        st.success(f"Berhasil! Stok {produk} berkurang. Sisa: {df.at[idx, 'Stok']}")
                        st.balloons()
                    else:
                        st.error(f"Stok tidak cukup! Sisa: {int(stok_sekarang)}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Tidak ada produk.")
