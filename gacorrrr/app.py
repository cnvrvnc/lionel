import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Virtual Lab Grafik Fungsi Kuadrat")

st.title("🔬 Virtual Lab Grafik Fungsi Kuadrat")
st.markdown("Aplikasi interaktif untuk memahami pengaruh koefisien **$a$**, **$b$**, dan **$c$** pada grafik fungsi kuadrat $f(x) = ax^2 + bx + c$.")

st.divider()

# --- Kontrol Interaktif (Sidebar) ---
st.sidebar.header("Kontrol Koefisien F(x) = ax² + bx + c")

MAX_VAL_SMALL = 10.0
MIN_VAL_SMALL = -10.0

# Koefisien a (Kecekungan/Kelancipan)
a = st.sidebar.slider(
    '1. Nilai Koefisien a',
    min_value=-5.0, # Batas a sedikit diperkecil agar grafik tidak terlalu lancip
    max_value=5.0,
    value=1.0,
    step=0.1,
    help="a > 0: terbuka ke atas. a < 0: terbuka ke bawah. Semakin besar |a|, grafik semakin sempit."
)

# Koefisien b (Sumbu Simetri)
b = st.sidebar.slider(
    '2. Nilai Koefisien b',
    min_value=MIN_VAL_SMALL,
    max_value=MAX_VAL_SMALL,
    value=0.0,
    step=0.5,
    help="Menggeser sumbu simetri secara horizontal."
)

# Koefisien c (Titik Potong Y)
c = st.sidebar.slider(
    '3. Nilai Koefisien c',
    min_value=MIN_VAL_SMALL,
    max_value=MAX_VAL_SMALL,
    value=0.0,
    step=0.5,
    help="Menggeser grafik secara vertikal."
)

# --- Tampilkan Formula ---
def format_value(val):
    """Format angka."""
    return f"{val:g}"

formula_a = f"{format_value(a)}x^2" if a != 0 else ""
formula_b = f"{format_value(b)}x" if b != 0 else ""
formula_c = f"{format_value(c)}" if c != 0 or (a == 0 and b == 0) else ""

# Atur tanda operator
if formula_b and formula_a:
    formula_b = f"+ {formula_b}" if b > 0 else f"- {-b:g}x"
if formula_c and (formula_a or formula_b):
    formula_c = f"+ {formula_c}" if c > 0 else f"- {-c:g}"
    
formula_display = f"$f(x) = {formula_a} {formula_b} {formula_c}$".replace("1x", "x").replace("1x", "x").replace("-1x", "-x").replace(" ", "").replace("+-", "-")
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

# Rentang X untuk Plot
x_plot = np.linspace(-10, 10, 400)
y_plot = a * x_plot**2 + b * x_plot + c

# Tentukan rentang Y plot agar adaptif tetapi fokus di sekitar rentang X [-10, 10]
min_y_plot = np.min(y_plot)
max_y_plot = np.max(y_plot)
y_buffer = max(1.0, (max_y_plot - min_y_plot) * 0.1) # Buffer minimal 1.0

ax_min_y = min_y_plot - y_buffer
ax_max_y = max_y_plot + y_buffer

# Buat Plot Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_plot, y_plot, label=f"a={format_value(a)}, b={format_value(b)}, c={format_value(c)}", color='orange', linewidth=3)

# Scatter titik puncak dan titik potong Y (jika dalam batas sumbu)
ax.scatter(x_puncak, y_puncak, color='red', zorder=5, label='Titik Puncak') 
ax.scatter(0, c, color='blue', zorder=5, label='Titik Potong Y')

# Pengaturan Sumbu dan Garis Bantu
ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax.axvline(0, color='gray', linewidth=0.8, linestyle='--')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlabel('Sumbu X', fontsize=12)
ax.set_ylabel('Sumbu Y / f(x)', fontsize=12)
ax.set_title('Grafik Parabola')

# Terapkan batas sumbu tetap X (-10 s.d. 10) dan Y adaptif
ax.set_xlim(-10, 10) 
ax.set_ylim(ax_min_y, ax_max_y)

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
        value=f"(0, {format_value(c)})",
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
1.  **Pengaruh 'a' ({format_value(a)}):**
    * **Kecekungan:** Jika $a>0$, terbuka ke atas. Jika $a<0$, terbuka ke bawah.
    * **Lebar Grafik:** Semakin besar nilai mutlak $a$, semakin sempit grafik (lebih lancip).
2.  **Pengaruh 'b' ({format_value(b)}):**
    * Mengontrol pergeseran horizontal sumbu simetri $x = -b/(2a)$.
3.  **Pengaruh 'c' ({format_value(c)}):**
    * Mengontrol pergeseran vertikal, yaitu tempat grafik **memotong sumbu Y** di $(0, c)$.
""")
