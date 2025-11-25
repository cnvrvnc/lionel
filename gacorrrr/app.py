import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Virtual Lab Grafik Fungsi Kuadrat (Skala Besar)")

st.title("🔬 Virtual Lab Grafik Fungsi Kuadrat")
st.markdown("Aplikasi interaktif untuk memahami pengaruh koefisien **$a$**, **$b$**, dan **$c$** pada grafik fungsi kuadrat.")
st.warning("Perhatian: Rentang nilai koefisien sangat besar (hingga ±100.000). Batas sumbu X dan Y akan disesuaikan secara dinamis agar grafik tetap terlihat.")

st.divider()

# --- Kontrol Interaktif (Sidebar) ---
st.sidebar.header("Kontrol Koefisien F(x) = ax² + bx + c")

MAX_VAL = 100000.0

# Koefisien a (Kecekungan/Kelancipan)
a = st.sidebar.slider(
    '1. Nilai Koefisien a',
    min_value=-MAX_VAL,
    max_value=MAX_VAL,
    value=100.0,
    step=100.0, # Langkah 100
    help=f"Rentang: -{MAX_VAL:g} s.d. {MAX_VAL:g}. Nilai a yang besar membuat parabola sangat sempit."
)

# Koefisien b (Sumbu Simetri)
b = st.sidebar.slider(
    '2. Nilai Koefisien b',
    min_value=-MAX_VAL,
    max_value=MAX_VAL,
    value=100.0,
    step=100.0, # Langkah 100
    help="Menggeser sumbu simetri secara horizontal."
)

# Koefisien c (Titik Potong Y)
c = st.sidebar.slider(
    '3. Nilai Koefisien c',
    min_value=-MAX_VAL,
    max_value=MAX_VAL,
    value=100.0,
    step=1000.0, # Langkah 1000
    help="Menggeser grafik secara vertikal."
)

# --- Tampilkan Formula ---
def format_value(val):
    """Format angka besar ke notasi ilmiah jika diperlukan."""
    if abs(val) >= 1000:
        return f"{val:.2e}"
    return f"{val:g}"

formula_a = f"{format_value(a)}x^2" if a != 0 else ""
formula_b = f"{format_value(b)}x" if b != 0 else ""
formula_c = f"{format_value(c)}" if c != 0 or (a == 0 and b == 0) else ""

# Atur tanda operator
if formula_b and formula_a:
    formula_b = f"+ {formula_b}" if b > 0 else f"- {-b:g}x"
if formula_c and (formula_a or formula_b):
    formula_c = f"+ {formula_c}" if c > 0 else f"- {-c:g}"
    
formula_display = f"$f(x) = {formula_a} {formula_b} {formula_c}$".replace("1x", "x").replace("-1x", "-x").replace(" ", "").replace("+-", "-")
st.header("Persamaan Fungsi Kuadrat Saat Ini:")
st.latex(formula_display.replace("f(x)=", ""))

# --- Visualisasi Grafik ---

# Hitung Titik Puncak
if a != 0:
    x_puncak = -b / (2 * a)
    y_puncak = a * x_puncak**2 + b * x_puncak + c
else:
    x_puncak = 0
    y_puncak = c

# --- LOGIKA BATAS SUMBU (SANGAT ADAPTIF) ---

# Tentukan rentang X yang akan diplot, berpusat pada x_puncak
if abs(a) > 1000:
    # Jika a sangat besar, gunakan rentang x yang sangat kecil (parabola sangat lancip)
    x_range_display = 2 / abs(a)**0.5 if abs(a) > 0 else 10 # agar range x lebih masuk akal
    x = np.linspace(x_puncak - x_range_display, x_puncak + x_range_display, 400)
elif a == 0:
    # Kasus linear/konstan
    x = np.linspace(-10, 10, 400)
else:
    # a tidak terlalu besar, gunakan rentang x sedang
    x_range_display = 10 
    x = np.linspace(x_puncak - x_range_display/2, x_puncak + x_range_display/2, 400)

y = a * x**2 + b * x + c

# Tentukan rentang Y
min_y_plot = np.min(y)
max_y_plot = np.max(y)
y_buffer = max(100.0, (max_y_plot - min_y_plot) * 0.1) # Buffer minimal 100 atau 10% dari rentang plot

ax_min_y = min_y_plot - y_buffer
ax_max_y = max_y_plot + y_buffer

# Buat Plot Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, label=f"a={format_value(a)}, b={format_value(b)}, c={format_value(c)}", color='orange', linewidth=3)

# Scatter hanya jika nilai titik puncak dan c berada dalam rentang plot
if ax_min_y <= y_puncak <= ax_max_y and ax_min_y <= c <= ax_max_y:
    ax.scatter(x_puncak, y_puncak, color='red', zorder=5, label='Titik Puncak') 
    ax.scatter(0, c, color='blue', zorder=5, label='Titik Potong Y')

# Pengaturan Sumbu dan Garis Bantu
ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax.axvline(0, color='gray', linewidth=0.8, linestyle='--')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlabel('Sumbu X', fontsize=12)
ax.set_ylabel('Sumbu Y / f(x)', fontsize=12)
ax.set_title('Grafik Parabola', fontsize=14)

# Terapkan batas sumbu yang adaptif
ax.set_xlim(x.min(), x.max()) 
ax.set_ylim(ax_min_y, ax_max_y)

ax.legend()

# Tampilkan plot ke Streamlit
st.pyplot(fig) 

[Image of a parabola graph showing the vertex and intercepts]


st.divider()

# --- Display Informasi Titik Penting & Analisis ---
st.subheader("Titik Penting dan Analisis (dalam Notasi Ilmiah jika besar)")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Titik Potong Sumbu Y (c)",
        value=f"(0, {format_value(c)})",
        delta="Geseran Vertikal"
    )

with col2:
    if a != 0:
        st.metric(
            label="Sumbu Simetri (x = -b/2a)",
            value=f"x = {format_value(x_puncak)}"
        )
    else:
        st.info("Koefisien 'a' = 0. Ini adalah fungsi linear.")

with col3:
    if a != 0:
        st.metric(
            label=f"Titik Puncak/Balik ({'Minimum' if a > 0 else 'Maksimum'})",
            value=f"({format_value(x_puncak)}, {format_value(y_puncak)})"
        )

st.subheader("💡 Kesimpulan Interaktif")
st.info(f"""
1.  **Pengaruh 'a' ({format_value(a)}):**
    * **Kecekungan:** Jika $a>0$, terbuka ke atas. Jika $a<0$, terbuka ke bawah.
    * **Lebar Grafik:** Karena $|a|$ bisa mencapai $100.000$, perubahan kecil pada $x$ akan menghasilkan perubahan besar pada $y$, membuat parabola sangat sempit.
2.  **Pengaruh 'b' ({format_value(b)}):**
    * Mengontrol pergeseran horizontal sumbu simetri $x = -b/(2a)$.
3.  **Pengaruh 'c' ({format_value(c)}):**
    * Mengontrol pergeseran vertikal, yaitu tempat grafik **memotong sumbu Y** di $(0, c)$.
""")
