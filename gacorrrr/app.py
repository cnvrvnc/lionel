import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Virtual Lab Grafik Fungsi Kuadrat")

st.title("🔬 Virtual Lab Grafik Fungsi Kuadrat")
st.markdown("Aplikasi interaktif untuk memahami pengaruh koefisien **$a$**, **$b$**, dan **$c$** pada grafik fungsi kuadrat.")

st.divider()

# --- Kontrol Interaktif (Sidebar) ---
st.sidebar.header("Kontrol Koefisien F(x) = ax² + bx + c")

# Koefisien a (Rentang DIBUAT LEBIH BESAR: -10.0 sampai 10.0)
a = st.sidebar.slider(
    '1. Nilai Koefisien a (Kecekungan/Kelancipan)',
    min_value=-10.0,
    max_value=10.0,
    value=1.0,
    step=0.1,
    help="a > 0: terbuka ke atas. a < 0: terbuka ke bawah. Semakin besar |a|, grafik semakin sempit/lancip."
)

# Koefisien b (Rentang DIBUAT LEBIH BESAR: -15.0 sampai 15.0)
b = st.sidebar.slider(
    '2. Nilai Koefisien b (Sumbu Simetri)',
    min_value=-15.0,
    max_value=15.0,
    value=0.0,
    step=0.1,
    help="Menggeser sumbu simetri secara horizontal."
)

# Koefisien c (Rentang DIBUAT LEBIH BESAR: -20.0 sampai 20.0)
c = st.sidebar.slider(
    '3. Nilai Koefisien c (Titik Potong Y)',
    min_value=-20.0,
    max_value=20.0,
    value=0.0,
    step=0.1,
    help="Menggeser grafik secara vertikal."
)

# --- Tampilkan Formula ---
formula_a = f"{a:g}x^2" if a != 0 else ""
formula_b = f"{b:g}x" if b != 0 else ""
formula_c = f"{c:g}" if c != 0 or (a == 0 and b == 0) else ""

if formula_b and formula_a:
    formula_b = f"+ {formula_b}" if b > 0 else f"- {-b:g}x"
if formula_c and (formula_a or formula_b):
    formula_c = f"+ {formula_c}" if c > 0 else f"- {-c:g}"
    
formula_display = f"$f(x) = {formula_a} {formula_b} {formula_c}$".replace("1x", "x").replace("-1x", "-x").replace(" ", "").replace("+-", "-")
st.header("Persamaan Fungsi Kuadrat Saat Ini:")
st.latex(formula_display.replace("f(x)=", ""))

# --- Visualisasi Grafik ---
x = np.linspace(-10, 10, 400)
y = a * x**2 + b * x + c

# Hitung Titik Puncak
if a != 0:
    x_puncak = -b / (2 * a)
    y_puncak = a * x_puncak**2 + b * x_puncak + c
else:
    # Handle fungsi linear/konstan
    x_puncak = 0
    y_puncak = c

# Buat Plot Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, label=f"a={a}, b={b}, c={c}", color='orange', linewidth=3)
ax.scatter(x_puncak, y_puncak, color='red', zorder=5, label='Titik Puncak') 
ax.scatter(0, c, color='blue', zorder=5, label='Titik Potong Y')

# Pengaturan Sumbu dan Garis Bantu
ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax.axvline(0, color='gray', linewidth=0.8, linestyle='--')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlabel('Sumbu X', fontsize=12)
ax.set_ylabel('Sumbu Y / f(x)', fontsize=12)
ax.set_title('Grafik Parabola', fontsize=14)

# Batasan Sumbu Y (agar grafik selalu terlihat)
# Menggunakan batas y yang adaptif
if a != 0:
    y_range = max(abs(y_puncak) * 2, abs(c) * 2, 20) 
    ax.set_ylim(y_puncak - y_range/2, y_puncak + y_range/2) 
    # Atur x_lim agar tetap fokus di sekitar puncak
    x_range = max(abs(x_puncak) * 2 + 2, 10)
    ax.set_xlim(x_puncak - x_range/2, x_puncak + x_range/2) 
else:
    # Kasus linear/konstan
    ax.set_ylim(c - 10, c + 10)
    ax.set_xlim(-10, 10) 

ax.legend()

# Tampilkan plot ke Streamlit
st.pyplot(fig) 

[Image of a parabola graph showing the vertex and intercepts]


st.divider()

# --- Display Informasi Titik Penting & Analisis ---
st.subheader("Titik Penting dan Analisis")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Titik Potong Sumbu Y (c)",
        value=f"(0, {c:.1f})",
        delta="Geseran Vertikal"
    )

with col2:
    if a != 0:
        st.metric(
            label="Sumbu Simetri (x = -b/2a)",
            value=f"x = {x_puncak:.2f}"
        )
    else:
        st.info("Koefisien 'a' = 0. Ini adalah fungsi linear.")

with col3:
    if a != 0:
        st.metric(
            label=f"Titik Puncak/Balik ({'Minimum' if a > 0 else 'Maksimum'})",
            value=f"({x_puncak:.2f}, {y_puncak:.2f})"
        )

st.subheader("💡 Kesimpulan Interaktif")
st.info(f"""
1.  **Pengaruh 'a' ({a:.1f}):**
    * Jika Anda menggeser $a$ menjadi **positif** ($a>0$), parabola terbuka **ke atas** dan memiliki titik **minimum**.
    * Jika Anda menggeser $a$ menjadi **negatif** ($a<0$), parabola terbuka **ke bawah** dan memiliki titik **maksimum**.
    * Karena rentang $a$ sekarang besar (hingga $\pm 10$), perubahan kecil pada $a$ akan membuat grafik menjadi **sangat sempit atau lebar**.
2.  **Pengaruh 'b' ({b:.1f}):**
    * Mengontrol pergeseran horizontal grafik dengan mengubah posisi sumbu simetri $x = -b/(2a)$.
3.  **Pengaruh 'c' ({c:.1f}):**
    * Mengontrol pergeseran vertikal, yaitu tempat grafik **memotong sumbu Y** di titik **(0, c)**.
""")
