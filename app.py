import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Kasir Toko API", layout="wide")
st.title("🛒 Kasir Toko (Via SheetDB)")

# API URL yang baru Anda buat
API_URL = "https://sheetdb.io/api/v1/ar1o4wvhtcr6b"

# Fungsi untuk mengambil data terbaru dari Google Sheets
def get_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        return pd.DataFrame()

df = get_data()

tab1, tab2 = st.tabs(["📦 Cek Stok", "💳 Input Penjualan"])

with tab1:
    st.subheader("Daftar Barang")
    if not df.empty:
        # Menampilkan tabel stok
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Gagal mengambil data dari API.")

with tab2:
    st.subheader("Catat Penjualan")
    if not df.empty:
        with st.form("transaksi"):
            # Kolom 'Nama Barang' harus sama persis dengan di Google Sheets
            produk = st.selectbox("Pilih Produk", df['Nama Barang'].tolist())
            jumlah = st.number_input("Jumlah Beli", min_value=1, step=1)
            submit = st.form_submit_button("Simpan & Potong Stok")

            if submit:
                # Ambil baris produk yang dipilih
                row = df[df['Nama Barang'] == produk].iloc[0]
                stok_lama = int(row['Stok'])
                
                if stok_lama >= jumlah:
                    stok_baru = stok_lama - jumlah
                    
                    # Proses Update ke Google Sheets via SheetDB
                    # Update dilakukan berdasarkan kolom 'Nama Barang'
                    update_url = f"{API_URL}/Nama%20Barang/{produk}"
                    data_update = {"data": {"Stok": stok_baru}}
                    
                    res = requests.put(update_url, json=data_update)
                    
                    if res.status_code == 200:
                        st.success(f"Berhasil! Stok {produk} sekarang: {stok_baru}")
                        st.balloons()
                        # Refresh data setelah berhasil
                        st.rerun()
                    else:
                        st.error("Gagal memperbarui stok di server.")
                else:
                    st.error(f"Stok tidak cukup! Sisa stok: {stok_lama}")
    else:
        st.warning("Data produk tidak tersedia.")
