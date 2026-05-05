import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Kasir Toko", layout="wide")
st.title("🛒 Kasir Toko Sederhana")

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Ambil Data
url = "https://docs.google.com/spreadsheets/d/10ZsM17t1Yc9wzrbngX1ufIXKcW3fbIaxzlEkUuL4EZo/edit?usp=sharing"
df = conn.read(spreadsheet=url, usecols=[0, 1, 2]) # Sesuaikan kolom Nama, Stok, Harga

tab1, tab2 = st.tabs(["📦 Cek Stok", "💳 Input Penjualan"])

with tab1:
    st.subheader("Daftar Barang Tersedia")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Catat Transaksi Baru")
    with st.form("transaksi"):
        produk = st.selectbox("Pilih Produk", df.iloc[:, 0].tolist())
        jumlah = st.number_input("Jumlah Beli", min_value=1, step=1)
        submit = st.form_submit_button("Simpan & Potong Stok")

        if submit:
            # Proses potong stok
            idx = df[df.iloc[:, 0] == produk].index[0]
            stok_lama = df.iloc[idx, 1]
            
            if stok_lama >= jumlah:
                df.iloc[idx, 1] = stok_lama - jumlah
                # Update ke Google Sheets
                conn.update(spreadsheet=url, data=df)
                st.success(f"Berhasil! Stok {produk} berkurang.")
                st.balloons()
            else:
                st.error("Stok tidak cukup!")
