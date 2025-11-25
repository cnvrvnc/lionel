import streamlit as st

# --- Fungsi untuk Luas Persegi ---
def luas_persegi(sisi):
  """Menghitung luas persegi: sisi * sisi"""
  luas = sisi * sisi
  return luas

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Kalkulator Luas Persegi",
    page_icon="📐",
    layout="centered"
)

st.title('📐 Kalkulator Luas Persegi Sederhana')
st.caption('Aplikasi ini menghitung luas persegi menggunakan Streamlit.')

# --- Input dari Pengguna ---
# Gunakan st.number_input untuk input numerik
s = st.number_input(
    'Masukkan panjang sisi persegi (satuan)',
    min_value=0.0,  # Memastikan sisi tidak negatif
    value=10.0,     # Nilai default
    step=0.5
)

# --- Perhitungan dan Output ---
# Tombol untuk memicu perhitungan
if st.button('Hitung Luas'):
    # Panggil fungsi
    hasil_luas = luas_persegi(s)

    # Tampilkan hasil
    st.success(f"**Luas persegi** dengan sisi **{s}** adalah:")
    st.markdown(f"## {hasil_luas:.2f} satuan persegi")

    # Opsional: Tampilkan rumus
    st.info(f"Rumus: Luas = sisi * sisi = {s} * {s} = {hasil_luas:.2f}")