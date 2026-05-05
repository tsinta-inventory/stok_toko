import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Kasir Toko", layout="wide")
st.title("🛒 Kasir Toko Sederhana")

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# URL Google Sheets Anda
url = "https://docs.google.com/spreadsheets/d/10ZsM17t1Yc9wzrbngX1ufIXKcW3fbIaxzlEkUuL4EZo/edit?usp=sharing"

# Membaca Data
df = conn.read(spreadsheet=url)

# --- PERBAIKAN ERROR DI SINI ---
# Kita bersihkan data stok agar pasti jadi angka, jika gagal akan jadi 0
if len(df.columns) > 1:
    df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce').fillna(0)
# -------------------------------

tab1, tab2 = st.tabs(["📦 Cek Stok", "💳 Input Penjualan"])

with tab1:
    st.subheader("Daftar Barang Tersedia")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Catat Transaksi Baru")
    with st.form("transaksi"):
        list_produk = df.iloc[:, 0].tolist()
        produk = st.selectbox("Pilih Produk", list_produk)
        
        jumlah = st.number_input("Jumlah Beli", min_value=1, step=1)
        submit = st.form_submit_button("Simpan & Potong Stok")

        if submit:
            idx = df[df.iloc[:, 0] == produk].index[0]
            # Pastikan stok_lama dikonversi ke angka saat pengecekan
            stok_lama = float(df.iloc[idx, 1])
            
            if stok_lama >= jumlah:
                df.iloc[idx, 1] = stok_lama - jumlah
                
                # Update kembali ke Google Sheets
                conn.update(spreadsheet=url, data=df)
                
                st.success(f"Berhasil! Stok {produk} berkurang. Sisa: {df.iloc[idx, 1]}")
                st.balloons()
            else:
                st.error(f"Stok tidak cukup! Sisa stok: {stok_lama}")
