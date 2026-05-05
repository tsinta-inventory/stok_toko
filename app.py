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

# Pastikan kolom stok (kolom kedua/index 1) dibaca sebagai angka
df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce').fillna(0).astype(int)

tab1, tab2 = st.tabs(["📦 Cek Stok", "💳 Input Penjualan"])

with tab1:
    st.subheader("Daftar Barang Tersedia")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Catat Transaksi Baru")
    with st.form("transaksi"):
        # Pilih produk berdasarkan kolom pertama (Nama Barang)
        list_produk = df.iloc[:, 0].tolist()
        produk = st.selectbox("Pilih Produk", list_produk)
        
        jumlah = st.number_input("Jumlah Beli", min_value=1, step=1)
        submit = st.form_submit_button("Simpan & Potong Stok")

        if submit:
            # Mencari baris barang yang dipilih
            idx = df[df.iloc[:, 0] == produk].index[0]
            stok_lama = int(df.iloc[idx, 1])
            
            if stok_lama >= jumlah:
                # Proses pengurangan stok
                df.iloc[idx, 1] = stok_lama - jumlah
                
                # Update kembali ke Google Sheets
                conn.update(spreadsheet=url, data=df)
                
                st.success(f"Berhasil! Stok {produk} berkurang. Sisa stok sekarang: {df.iloc[idx, 1]}")
                st.balloons()
            else:
                st.error(f"Stok tidak cukup! Stok saat ini hanya ada {stok_lama}")
