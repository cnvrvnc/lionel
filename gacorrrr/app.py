import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Virtual Lab Grafik Fungsi Kuadrat")

st.title("🔬 Virtual Lab Grafik Fungsi Kuadrat")
st.markdown("Aplikasi interaktif untuk memahami pengaruh koefisien **$a$**, **$b$**, dan **$c$** pada grafik fungsi kuadrat.")

st.divider()

# 

[Image of a parabola graph showing the vertex and intercepts]


# --- Kontrol Interaktif (Sidebar) ---
st.sidebar.header("Kontrol Koefisien F(x) = ax² + bx + c")

# Koefisien a (Arah bukaan parabola)
a = st.sidebar.slider(
    '1. Nilai Koefisien a',
    min_value=-2.0,
    max_value=2.0,
    value=1.0,
    step=0.1,
    help="Mengontrol arah bukaan parabola (a>0 ke atas, a<0 ke bawah) dan kelancipan grafik."
)

# Koefisien b (Menggeser sumbu simetri)
b = st.sidebar.slider(
    '2. Nilai Koefisien b',
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    help="Mengontrol posisi sumbu simetri/pergeseran horizontal."
)

# Koefisien c (Titik potong sumbu Y)
c = st.sidebar.slider(
    '3. Nilai Koefisien c',
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    help="Mengontrol titik potong terhadap sumbu Y (pergeseran vertikal)."
)

# --- Tampilkan Formula ---
# Membersihkan tampilan formula dari tanda + atau 0 yang tidak perlu
formula_a = f"{a:g}x^2" if a != 0 else ""
formula_b = f"{b:g}x" if b != 0 else ""
formula_c = f"{c:g}" if c != 0 or (a == 0 and b == 0) else ""

# Atur tanda operator
if formula_b and formula_a:
    formula_b = f"+ {formula_b}" if b > 0 else f"- {-b:g}x"
if formula_c and (formula_a or formula_b):
    formula_c = f"+ {formula_c}" if c > 0 else f"- {-c:g}"
    
# Gabungkan formula
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
min_y = min(y) if len(y) > 0 else 0
max_y = max(y) if len(y) > 0 else 0
y_limit = max(abs(min_y), abs(max_y)) + 2

# Batas y minimum yang baik
if a != 0:
    min_y_display = y_puncak - 5 if a > 0 else min_y - 2
    max_y_display = y_puncak + 5 if a < 0 else max_y + 2
else:
    min_y_display = -5
    max_y_display = 5

ax.set_ylim(min_y_display, max_y_display)
ax.set_xlim(-5, 5) # Fokuskan di range -5 sampai 5 untuk x
ax.legend()

# Tampilkan plot ke Streamlit
st.pyplot(fig)

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
2.  **Pengaruh 'b' ({b:.1f}):**
    * Mengontrol pergeseran horizontal grafik dengan mengubah posisi sumbu simetri $x = -b/(2a)$.
3.  **Pengaruh 'c' ({c:.1f}):**
    * Mengontrol pergeseran vertikal, yaitu tempat grafik **memotong sumbu Y** di titik **(0, c)**.
""")
