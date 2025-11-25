import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import ConvexHull # Untuk menggambar garis pada proyeksi

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Virtual Lab Dimensi 5: Memahami Hyper-Ruang")

st.title("🌌 Virtual Lab: Memahami Dimensi Kelima")
st.markdown("""
Selamat datang di lab virtual ini\! Kita akan menjelajahi konsep dimensi yang lebih tinggi, 
khususnya dimensi kelima, melalui **analogi, proyeksi, dan visualisasi abstrak**.

**Apa itu dimensi?** Kita hidup di ruang 3D (panjang, lebar, tinggi) dan bergerak maju dalam waktu (dimensi ke-4). 
Dimensi ke-5 (dan seterusnya) adalah konsep matematis yang melampaui intuisi kita sehari-hari, 
tetapi dapat dibantu dengan visualisasi dan analogi.
""")

st.divider()

# --- BAGIAN 1: Analogi Dimensi (0D ke 3D) ---
st.header("1. Analog Dimensi: Dari Titik ke Kubus")
st.markdown("""
Mari kita pahami dimensi dengan membangun dari yang paling sederhana:
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Titik (0D)")
    st.write("Tidak punya panjang, lebar, atau tinggi. Hanya posisi.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Point.svg/100px-Point.svg.png", caption="Titik (0D)")

with col2:
    st.subheader("Garis (1D)")
    st.write("Dibuat dengan menggerakkan titik. Hanya punya panjang.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Line_segment.svg/150px-Line_segment.svg.png", caption="Garis (1D)")

with col3:
    st.subheader("Kotak (2D)")
    st.write("Dibuat dengan menggerakkan garis. Punya panjang dan lebar.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Square_flat.svg/150px-Square_flat.svg.png", caption="Kotak (2D)")

with col4:
    st.subheader("Kubus (3D)")
    st.write("Dibuat dengan menggerakkan kotak. Punya panjang, lebar, dan tinggi.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Cube.svg/150px-Cube.svg.png", caption="Kubus (3D)")

st.markdown("""
**Konsep Kunci:** Setiap dimensi baru "dibuat" dengan menggerakkan objek dari dimensi sebelumnya dalam arah yang tegak lurus dengan semua dimensi yang sudah ada.
""")

st.divider()

# --- BAGIAN 2: Proyeksi Objek Dimensi Tinggi (Tesseract/Hypercube 4D) ---
st.header("2. Proyeksi dari Dimensi Ke-4: Tesseract (Hypercube)")
st.markdown("""
Bayangkan sebuah kubus 4 dimensi (disebut **Tesseract** atau Hypercube). Kita tidak bisa melihatnya secara langsung,
tapi kita bisa melihat **proyeksinya** ke ruang 3D kita. Mirip dengan bagaimana bayangan kubus 3D
terlihat seperti kotak 2D yang aneh.
""")

st.sidebar.header("Kontrol Proyeksi Tesseract")
rotation_angle_xy = st.sidebar.slider("Rotasi (XY)", 0, 360, 45, help="Rotasi di bidang XY")
rotation_angle_xz = st.sidebar.slider("Rotasi (XZ)", 0, 360, 45, help="Rotasi di bidang XZ")
rotation_angle_yz = st.sidebar.slider("Rotasi (YZ)", 0, 360, 45, help="Rotasi di bidang YZ")
perspective_w = st.sidebar.slider("Perspektif Dimensi ke-4 (W)", -1.0, 1.0, 0.5, 0.01, help="Menyesuaikan perspektif dari dimensi W")


def rotate_4d(points, angle_xy, angle_xz, angle_yz):
    """Rotasi 4D (hanya 3 bidang rotasi 2D untuk kesederhanaan)."""
    R_xy = np.array([
        [np.cos(np.radians(angle_xy)), -np.sin(np.radians(angle_xy)), 0, 0],
        [np.sin(np.radians(angle_xy)),  np.cos(np.radians(angle_xy)), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    R_xz = np.array([
        [np.cos(np.radians(angle_xz)), 0, -np.sin(np.radians(angle_xz)), 0],
        [0, 1, 0, 0],
        [np.sin(np.radians(angle_xz)), 0,  np.cos(np.radians(angle_xz)), 0],
        [0, 0, 0, 1]
    ])
    R_yz = np.array([
        [1, 0, 0, 0],
        [0, np.cos(np.radians(angle_yz)), -np.sin(np.radians(angle_yz)), 0],
        [0, np.sin(np.radians(angle_yz)),  np.cos(np.radians(angle_yz)), 0],
        [0, 0, 0, 1]
    ])
    return (R_xy @ R_xz @ R_yz @ points.T).T

def project_4d_to_3d(points_4d, w_factor=0.5):
    """Proyeksi perspektif dari 4D ke 3D."""
    projected = []
    for p in points_4d:
        x, y, z, w = p
        # Faktor skala berbasis perspektif dari dimensi w
        # Semakin jauh di dimensi w, semakin kecil proyeksi
        # w_factor mengontrol "kedalaman" w
        divisor = (w_factor - w)
        if divisor == 0: # Hindari pembagian nol
            projected.append([x,y,z]) # atau tangani sesuai kebutuhan
            continue
        projected_x = x / divisor
        projected_y = y / divisor
        projected_z = z / divisor
        projected.append([projected_x, projected_y, projected_z])
    return np.array(projected)

# Titik-titik Hypercube (Tesseract) 4D
# Ada 16 titik (2^4)
tesseract_points_4d = np.array([
    [-1, -1, -1, -1], [ 1, -1, -1, -1], [-1,  1, -1, -1], [ 1,  1, -1, -1],
    [-1, -1,  1, -1], [ 1, -1,  1, -1], [-1,  1,  1, -1], [ 1,  1,  1, -1],
    [-1, -1, -1,  1], [ 1, -1, -1,  1], [-1,  1, -1,  1], [ 1,  1, -1,  1],
    [-1, -1,  1,  1], [ 1, -1,  1,  1], [-1,  1,  1,  1], [ 1,  1,  1,  1]
])

# Rotasi Tesseract 4D
rotated_tesseract = rotate_4d(tesseract_points_4d, rotation_angle_xy, rotation_angle_xz, rotation_angle_yz)
# Proyeksi ke 3D
projected_tesseract_3d = project_4d_to_3d(rotated_tesseract, perspective_w)

# Menghubungkan titik-titik (edges) untuk tesseract (ini sedikit kompleks, tapi esensinya mirip kubus ganda)
# Ada 32 garis untuk tesseract (2 * 12 (kubus) + 8 (menghubungkan kubus))
edges = []
for i in range(16):
    for j in range(i + 1, 16):
        if np.sum(np.abs(tesseract_points_4d[i] - tesseract_points_4d[j])) == 2: # Hanya menghubungkan titik yang berbeda 1 dimensi
            edges.append((i, j))

fig_tesseract = go.Figure()

for edge in edges:
    p1 = projected_tesseract_3d[edge[0]]
    p2 = projected_tesseract_3d[edge[1]]
    fig_tesseract.add_trace(go.Scatter3d(
        x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
        mode='lines',
        line=dict(color='blue', width=2),
        showlegend=False
    ))

# Menambahkan titik
fig_tesseract.add_trace(go.Scatter3d(
    x=projected_tesseract_3d[:,0], y=projected_tesseract_3d[:,1], z=projected_tesseract_3d[:,2],
    mode='markers',
    marker=dict(size=4, color='red'),
    name='Vertices'
))

fig_tesseract.update_layout(
    title='Proyeksi Tesseract (Hypercube 4D) ke Ruang 3D',
    scene=dict(
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        zaxis=dict(title='Z'),
        aspectmode='cube' # Menjaga rasio aspek tetap
    ),
    width=700, height=700
)

st.plotly_chart(fig_tesseract, use_container_width=True)
st.markdown("""
**Perhatikan:**
* Saat Anda menggeser sudut rotasi, bentuk proyeksi Tesseract ini berubah. Ini adalah "bayangan" dari objek 4D yang berputar di ruang 4D.
* *Slider* **Perspektif Dimensi ke-4 (W)** mencoba mensimulasikan bagaimana objek terlihat berbeda jika kita melihatnya dari "jarak" yang berbeda di dimensi keempat.
""")

st.divider()

# --- BAGIAN 3: Membayangkan Dimensi ke-5 (Hyper-Kubus 5D) ---
st.header("3. Membayangkan Hypercube 5D")
st.markdown("""
Jika sebuah kubus 3D dibuat dengan menggerakkan persegi 2D, dan Tesseract 4D dibuat dengan menggerakkan kubus 3D,
maka **Hypercube 5D** (disebut juga **Penteract**) dibuat dengan menggerakkan Tesseract 4D
dalam arah yang tegak lurus terhadap keempat dimensi yang sudah ada\!

Tentu saja, kita tidak bisa memvisualisasikan Hypercube 5D secara langsung.
Namun, kita bisa memahaminya secara konseptual:
""")

col_5d_1, col_5d_2 = st.columns(2)

with col_5d_1:
    st.subheader("Konsep Proyeksi ke 3D")
    st.markdown("""
    Seperti Tesseract yang diproyeksikan ke 3D, Hypercube 5D akan terlihat seperti objek 3D yang jauh
    lebih kompleks dan aneh saat diproyeksikan.
    Bayangkan dua Tesseract yang terhubung satu sama lain oleh banyak garis, 
    dan mereka bisa bergeser "masuk" dan "keluar" satu sama lain seperti dalam sebuah dimensi tambahan.
    """)
    st.info("""
    **Jumlah Titik (Vertices):** $2^N$
    * Kubus (3D): $2^3 = 8$ titik
    * Tesseract (4D): $2^4 = 16$ titik
    * **Penteract (5D):** $2^5 = 32$ titik
    """)

with col_5d_2:
    st.subheader("Konsep Irisan (Cross-Section)")
    st.markdown("""
    Bayangkan jika Anda mengiris sebuah apel 3D dengan pisau 2D (permukaan). Anda akan melihat irisan 2D.
    Jika Anda mengiris kubus 4D (Tesseract) dengan "hyper-pisau" 3D, Anda akan melihat irisan 3D yang mungkin
    berubah bentuk saat pisau bergerak sepanjang dimensi ke-4.

    **Untuk Hypercube 5D:** Jika kita "mengiris" Hypercube 5D dengan sebuah "hyper-pisau" 4D, kita akan
    mendapatkan irisan 4D (Tesseract). Dan saat "pisau" itu bergerak di dimensi ke-5, Tesseract yang kita lihat
    akan berubah bentuk, muncul, dan menghilang.
    """)
    st.info("""
    **Jumlah Rusuk (Edges):** $N \times 2^{N-1}$
    * Kubus (3D): $3 \times 2^2 = 12$ rusuk
    * Tesseract (4D): $4 \times 2^3 = 32$ rusuk
    * **Penteract (5D):** $5 \times 2^4 = 80$ rusuk
    """)

st.markdown("""
**Kesimpulan:**
Memahami dimensi ke-5 bukanlah tentang melihatnya, tetapi tentang **memahami strukturnya secara matematis**
dan bagaimana ia berhubungan dengan dimensi yang lebih rendah melalui proyeksi dan irisan. 
Ini adalah latihan dalam abstraksi dan penalaran spasial yang melampaui pengalaman kita sehari-hari.
""")

st.divider()
st.info("Anda bisa menemukan lebih banyak tentang topik ini dengan mencari 'Hypercube', 'Tesseract', atau 'Penteract'.")
