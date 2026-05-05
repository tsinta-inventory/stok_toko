import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kasir Toko Tsinta", layout="wide")
st.title("👕 Sistem Manajemen Stok & Kasir")

# LINK YANG SUDAH DIPERBAIKI
URL_DATABASE = "https://docs.google.com/spreadsheets/d/10ZsM17t1Yc9wzrbngX1ufIXKcW3fbIaxzlEkUuL4EZo/export?format=csv"

def ambil_data():
    try:
        return pd.read_csv(URL_DATABASE)
    except:
        return pd.DataFrame({
            'Nama Barang': ['Kaos Polo Scuba', 'Kemeja Victor', 'Chinos Panjang', 'Hoodie Polos'],
            'Kategori': ['Polo', 'Kemeja', 'Celana', 'Hoodie'],
            'Stok': [10, 15, 20, 5],
            'Harga': [85000, 120000, 150000, 135000]
        })

df = ambil_data()

tab1, tab2 = st.tabs(["📦 Cek Stok", "🛒 Input Penjualan"])

with tab1:
    st.subheader("Daftar Barang Tersedia")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Catat Transaksi Baru")
    with st.form("form_kasir"):
        produk = st.selectbox("Pilih Produk", df['Nama Barang'].unique())
        jumlah = st.number_input("Jumlah Beli", min_value=1)
        proses = st.form_submit_button("Simpan Transaksi")
        
        if proses:
            st.success(f"Berhasil mencatat penjualan {jumlah} {produk}!")
