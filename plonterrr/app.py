import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Fungsi Transformasi Geometri ---

def translate(point, tx, ty):
    """Menerapkan Translasi pada titik (x, y)."""
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]])
    P = np.array([[point[0]], [point[1]], [1]])
    P_prime = T @ P
    return P_prime[0, 0], P_prime[1, 0]

def rotate(point, angle_deg, cx=0, cy=0):
    """Menerapkan Rotasi terhadap pusat (cx, cy)."""
    angle_rad = np.radians(angle_deg)
    
    # 1. Translasi titik ke pusat (cx, cy)
    x_translated = point[0] - cx
    y_translated = point[1] - cy
    
    # 2. Rotasi
    x_rotated = x_translated * np.cos(angle_rad) - y_translated * np.sin(angle_rad)
    y_rotated = x_translated * np.sin(angle_rad) + y_translated * np.cos(angle_rad)
    
    # 3. Translasi kembali
    x_final = x_rotated + cx
    y_final = y_rotated + cy
    
    return x_final, y_final

def reflect(point, axis_choice):
    """Menerapkan Refleksi terhadap sumbu X, Y, atau garis y=x."""
    x, y = point
    if axis_choice == "Sumbu X":
        return x, -y
    elif axis_choice == "Sumbu Y":
        return -x, y
    elif axis_choice == "Garis y=x":
        return y, x
    return x, y

def dilate(point, scale_factor, cx=0, cy=0):
    """Menerapkan Dilatasi terhadap pusat (cx, cy)."""
    # Menggeser titik ke pusat
    x_translated = point[0] - cx
    y_translated = point[1] - cy
    
    # Skala
    x_scaled = x_translated * scale_factor
    y_scaled = y_translated * scale_factor
    
    # Menggeser kembali
    x_final = x_scaled + cx
    y_final = y_scaled + cy
    
    return x_final, y_final

def apply_transformation(shape_points, transformation_type, params):
    """Menerapkan transformasi ke semua titik pada bangun."""
    transformed_points = []
    
    if transformation_type == "Translasi":
        tx, ty = params
        for p in shape_points:
            transformed_points.append(translate(p, tx, ty))
            
    elif transformation_type == "Rotasi":
        angle, cx, cy = params
        for p in shape_points:
            transformed_points.append(rotate(p, angle, cx, cy))
            
    elif transformation_type == "Refleksi":
        axis = params[0]
        for p in shape_points:
            transformed_points.append(reflect(p, axis))

    elif transformation_type == "Dilatasi":
        scale, cx, cy = params
        for p in shape_points:
            transformed_points.append(dilate(p, scale, cx, cy))
            
    return np.array(transformed_points)

# --- Visualisasi Grafik ---

def plot_shape(original_points, transformed_points, title):
    """Membuat plot untuk bangun asli dan hasil transformasi."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Menggabungkan titik awal dan akhir untuk visualisasi bentuk tertutup
    original_closed = np.vstack([original_points, original_points[0]])
    transformed_closed = np.vstack([transformed_points, transformed_points[0]])
    
    # Plot bangun asli
    ax.plot(original_closed[:, 0], original_closed[:, 1], 'bo-', label='Asli (Original)', alpha=0.6)
    
    # Plot hasil transformasi
    ax.plot(transformed_closed[:, 0], transformed_closed[:, 1], 'r*-', label='Hasil Transformasi', alpha=0.9)
    
    # Pengaturan plot
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    
    # Menampilkan koordinat titik
    for i, (x, y) in enumerate(original_points):
        ax.text(x, y, f'P{i+1}({x:.1f}, {y:.1f})', color='blue', fontsize=9)
    for i, (x, y) in enumerate(transformed_points):
        ax.text(x, y, f"P'{i+1}({x:.1f}, {y:.1f})", color='red', fontsize=9, ha='right')
        
    # Memastikan sumbu memiliki rasio 1:1
    ax.set_aspect('equal', adjustable='box')
    
    # Batas sumbu
    all_coords = np.vstack([original_points, transformed_points])
    max_val = np.ceil(np.max(np.abs(all_coords))) + 1
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    
    ax.set_title(title)
    ax.set_xlabel('Sumbu X')
    ax.set_ylabel('Sumbu Y')
    ax.legend()
    ax.grid(True, linestyle='dotted')
    
    return fig

# --- Antarmuka Streamlit ---

st.set_page_config(layout="wide", page_title="Lab Virtual Transformasi Geometri")

st.title("🔬 Lab Virtual Transformasi Geometri")
st.markdown("""
Aplikasi interaktif ini memungkinkan Anda untuk memvisualisasikan **Translasi, Rotasi, Refleksi, dan Dilatasi**
pada bangun datar di koordinat kartesius.
""")

# --- Sidebar untuk Input ---
st.sidebar.header("⚙️ Pengaturan Bangun dan Transformasi")

# 1. Input Bangun Datar
st.sidebar.subheader("1. Tentukan Bangun Datar Awal")
default_points = "1,1; 3,1; 3,3; 1,3"
point_input = st.sidebar.text_area(
    "Masukkan Koordinat Titik (Contoh: x1,y1; x2,y2; ...)",
    value=default_points
)

# Parsing input
try:
    points_list = [tuple(map(float, p.split(','))) for p in point_input.split(';') if p.strip()]
    if len(points_list) < 2:
         st.sidebar.error("Masukkan minimal 2 titik (x,y) yang dipisahkan oleh tanda semi-kolon (;).")
         original_points = np.array([[0, 0], [1, 1]]) # Titik default aman
    else:
        original_points = np.array(points_list)
except Exception:
    st.sidebar.error("Format input koordinat salah. Gunakan format 'x1,y1; x2,y2'.")
    original_points = np.array([[0, 0], [1, 1]])

# 2. Pilih Transformasi
st.sidebar.subheader("2. Pilih Jenis Transformasi")
transform_type = st.sidebar.selectbox(
    "Pilih Transformasi:",
    ("Translasi", "Rotasi", "Refleksi", "Dilatasi")
)

# --- Kontrol Transformasi ---
params = []

if transform_type == "Translasi":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Translasi (Pergeseran)")
    tx = st.sidebar.slider("Pergeseran pada Sumbu X ($T_x$)", -10.0, 10.0, 2.0, 0.5)
    ty = st.sidebar.slider("Pergeseran pada Sumbu Y ($T_y$)", -10.0, 10.0, 1.0, 0.5)
    params = [tx, ty]
    st.markdown(f"**Translasi** $T=({tx}, {ty})$")
    
elif transform_type == "Rotasi":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Rotasi (Perputaran)")
    angle = st.sidebar.slider("Sudut Rotasi (Derajat)", -360, 360, 90, 5)
    cx = st.sidebar.number_input("Pusat Rotasi X ($C_x$)", value=0.0)
    cy = st.sidebar.number_input("Pusat Rotasi Y ($C_y$)", value=0.0)
    params = [angle, cx, cy]
    st.markdown(f"**Rotasi** sebesar ${angle}^\circ$ terhadap pusat $C({cx}, {cy})$")
    
elif transform_type == "Refleksi":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Refleksi (Pencerminan)")
    axis = st.sidebar.selectbox(
        "Pilih Sumbu Pencerminan:",
        ("Sumbu X", "Sumbu Y", "Garis y=x")
    )
    params = [axis]
    st.markdown(f"**Refleksi** terhadap **{axis}**")
    
elif transform_type == "Dilatasi":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Dilatasi (Perkalian/Pengecilan)")
    scale = st.sidebar.slider("Faktor Skala ($k$)", 0.1, 5.0, 2.0, 0.1)
    cx = st.sidebar.number_input("Pusat Dilatasi X ($C_x$)", value=0.0)
    cy = st.sidebar.number_input("Pusat Dilatasi Y ($C_y$)", value=0.0)
    params = [scale, cx, cy]
    st.markdown(f"**Dilatasi** dengan faktor skala $k={scale}$ terhadap pusat $C({cx}, {cy})$")

# --- Eksekusi dan Visualisasi ---
if len(original_points) >= 2:
    transformed_points = apply_transformation(original_points, transform_type, params)
    
    # Judul Plot
    plot_title = f"Visualisasi Transformasi: {transform_type}"
    
    # Tampilkan Plot
    fig = plot_shape(original_points, transformed_points, plot_title)
    st.pyplot(fig)
    
    st.subheader("📋 Data Titik Hasil Transformasi")
    
    # Persiapan data untuk tabel
    data_table = []
    for i, (orig, trans) in enumerate(zip(original_points, transformed_points)):
        data_table.append({
            "Titik Asli": f"P{i+1}({orig[0]:.2f}, {orig[1]:.2f})",
            "Titik Transformasi": f"P'{i+1}({trans[0]:.2f}, {trans[1]:.2f})"
        })
        
    st.dataframe(data_table, use_container_width=True)
