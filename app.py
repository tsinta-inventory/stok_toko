import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Kasir Toko Tsinta", layout="wide")
st.title("👕 Sistem Manajemen Stok & Kasir")

# Membuat koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Membaca data dari Google Sheets
def ambil_data():
    return conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/10ZsM17t1Yc9wzrbngX1ufIXKcW3fbIaxzlEkUuL4EZo/edit?usp=sharing", ttl=0)

df = ambil_data()

tab1, tab2 = st.tabs(["📦 Cek Stok", "🛒 Input Penjualan"])

with tab1:
    st.subheader("Daftar Barang Tersedia")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Catat Transaksi Baru")
    with st.form("form_kasir"):
        produk = st.selectbox("Pilih Produk", df['Nama Barang'].unique())
        jumlah = st.number_input("Jumlah Beli", min_value=1, step=1)
        proses = st.form_submit_button("Simpan & Potong Stok")
        
        if proses:
            # Logika memotong stok
            idx = df[df['Nama Barang'] == produk].index[0]
            stok_sekarang = df.at[idx, 'Stok']
            
            if stok_sekarang >= jumlah:
                df.at[idx, 'Stok'] = stok_sekarang - jumlah
                # Update ke Google Sheets
                conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/10ZsM17t1Yc9wzrbngX1ufIXKcW3fbIaxzlEkUuL4EZo/edit?usp=sharing", data=df)
                st.success(f"Berhasil! Stok {produk} berkurang menjadi {stok_sekarang - jumlah}")
                st.balloons()
            else:
                st.error(f"Stok tidak cukup! Sisa stok {produk} hanya {stok_sekarang}")
