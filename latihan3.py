import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import colorsys
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Warna Produk",
    page_icon="🎨",
    layout="wide"
)

# CSS yang lebih sederhana
st.markdown(
    """
    <style>
    .stApp {
        background: #1e3c72;
        color: white;
    }
    
    .stButton > button {
        background: #4a7dff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: #2a5bd7;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4a7dff !important;
        color: white !important;
    }
    
    .stAlert {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================================
# FUNGSI UTAMA YANG SIMPLE
# =============================================

def extract_dominant_colors(image, num_colors=5):
    """Ekstrak warna dominan dari gambar"""
    # Perkecil gambar untuk proses cepat
    image = image.resize((100, 100))
    img_array = np.array(image)
    
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    
    # Sederhanakan warna
    quantized = (img_array // 32) * 32
    pixels = quantized.reshape(-1, 3)
    
    # Hitung warna unik
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    if len(unique_colors) > num_colors:
        top_indices = np.argsort(counts)[-num_colors:]
        dominant_colors = unique_colors[top_indices]
        percentages = (counts[top_indices] / counts.sum()) * 100
    else:
        dominant_colors = unique_colors
        percentages = (counts / counts.sum()) * 100
    
    # Urutkan dari yang terbanyak
    sorted_indices = np.argsort(percentages)[::-1]
    return dominant_colors[sorted_indices], percentages[sorted_indices]

def rgb_to_hex(rgb):
    """Ubah RGB ke format HEX"""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def get_complementary_color(rgb_color):
    """Cari warna pelengkap"""
    hsv = colorsys.rgb_to_hsv(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
    comp_hue = (hsv[0] + 0.5) % 1.0
    comp_rgb = colorsys.hsv_to_rgb(comp_hue, hsv[1], hsv[2])
    return tuple(int(c * 255) for c in comp_rgb)

def display_color_palette(colors, percentages, title="Warna Dominan"):
    """Tampilkan palette warna"""
    fig, axes = plt.subplots(1, len(colors), figsize=(12, 2))
    fig.patch.set_facecolor('#1e3c72')
    
    if len(colors) == 1:
        axes = [axes]
    
    for i, (color, percentage) in enumerate(zip(colors, percentages)):
        axes[i].add_patch(patches.Rectangle((0, 0), 1, 1, color=np.array(color)/255))
        axes[i].set_title(f'{percentage:.1f}%', fontsize=10, pad=10, color='white')
        axes[i].text(0.5, -0.15, f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}', 
                    ha='center', va='top', transform=axes[i].transAxes, fontsize=8, color='white')
        axes[i].set_facecolor('#1e3c72')
        axes[i].axis('off')
    
    plt.suptitle(title, y=1.1, color='white', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

# =============================================
# SIDEBAR SIMPLE
# =============================================

st.sidebar.title("⚙️ Pengaturan")
st.sidebar.markdown("---")

num_colors = st.sidebar.slider("Jumlah warna yang ditampilkan", 3, 6, 4)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**💡 Tips singkat:** 
- Upload foto produk dengan background bersih
- Hasil terbaik didapat dari foto dengan pencahayaan baik
- Gunakan hasil untuk memilih warna brand Anda
""")

# =============================================
# TAMPILAN UTAMA
# =============================================

st.title("🎨 Analisis Warna Produk")
st.markdown("### Unggah foto produk untuk melihat warna-warna dominannya")

# Pilih gambar
option = st.radio(
    "Pilih cara memasukkan foto:",
    ["📁 Upload dari file", "📷 Ambil foto dengan kamera"],
    horizontal=True
)

if option == "📁 Upload dari file":
    uploaded_file = st.file_uploader(
        "Pilih file gambar (JPG/PNG)", 
        type=['png', 'jpg', 'jpeg']
    )
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True, caption="Foto Produk Anda")
            
            if st.button("🔍 Analisis Warna", type="primary", use_container_width=True):
                with st.spinner("Menganalisis warna..."):
                    dominant_colors, percentages = extract_dominant_colors(image, num_colors)
                
                st.success("✅ Analisis selesai!")
                
                # Tampilkan hasil
                st.subheader("🎨 Warna Dominan")
                display_color_palette(dominant_colors, percentages)
                
                # Tampilkan info warna
                st.subheader("📋 Detail Warna")
                for i, (color, percentage) in enumerate(zip(dominant_colors, percentages)):
                    hex_code = rgb_to_hex(color)
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.color_picker(f"Color {i+1}", hex_code, key=f"color_{i}")
                    with col2:
                        st.markdown(f"**Warna {i+1}**")
                        st.write(f"RGB: {tuple(color)}")
                        st.write(f"HEX: {hex_code}")
                    with col3:
                        st.markdown(f"**{percentage:.1f}%**")
                
                # Warna pelengkap
                st.subheader("💡 Warna Pelengkap")
                primary_color = dominant_colors[0]
                comp_color = get_complementary_color(primary_color)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Warna Utama**")
                    fig1, ax1 = plt.subplots(figsize=(4, 1))
                    ax1.add_patch(patches.Rectangle((0, 0), 1, 1, color=np.array(primary_color)/255))
                    ax1.set_facecolor('#1e3c72')
                    ax1.axis('off')
                    st.pyplot(fig1)
                    st.write(f"HEX: {rgb_to_hex(primary_color)}")
                
                with col_b:
                    st.markdown("**Warna Pelengkap**")
                    fig2, ax2 = plt.subplots(figsize=(4, 1))
                    ax2.add_patch(patches.Rectangle((0, 0), 1, 1, color=np.array(comp_color)/255))
                    ax2.set_facecolor('#1e3c72')
                    ax2.axis('off')
                    st.pyplot(fig2)
                    st.write(f"HEX: {rgb_to_hex(comp_color)}")
                
                st.info("💡 **Tips:** Gunakan warna pelengkap untuk aksen atau teks agar kontras")
                
                # Tombol reset
                if st.button("🔄 Analisis Gambar Baru", use_container_width=True):
                    st.rerun()
                    
        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")

else:  # Ambil dari kamera
    camera_photo = st.camera_input("Ambil foto produk")
    
    if camera_photo is not None:
        try:
            image = Image.open(camera_photo)
            st.image(image, use_container_width=True, caption="Foto dari Kamera")
            
            if st.button("🔍 Analisis Warna", type="primary", use_container_width=True):
                with st.spinner("Menganalisis warna..."):
                    dominant_colors, percentages = extract_dominant_colors(image, num_colors)
                
                st.success("✅ Analisis selesai!")
                
                # Tampilkan hasil
                st.subheader("🎨 Warna Dominan")
                display_color_palette(dominant_colors, percentages)
                
                # Tampilkan info warna
                st.subheader("📋 Detail Warna")
                for i, (color, percentage) in enumerate(zip(dominant_colors, percentages)):
                    hex_code = rgb_to_hex(color)
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.color_picker(f"", hex_code, key=f"cam_color_{i}")
                    with col2:
                        st.markdown(f"**Warna {i+1}** - {percentage:.1f}%")
                        st.write(f"HEX: {hex_code} | RGB: {tuple(color)}")
                
                # Tombol reset
                if st.button("📸 Ambil Foto Baru", use_container_width=True):
                    st.rerun()
                    
        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")

# =============================================
# PETUNJUK JIKA BELUM ADA GAMBAR
# =============================================

if not uploaded_file and not camera_photo:
    st.markdown("""
    <div style='background: rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 15px;'>
    <h2 style='color: white; text-align: center;'>🏆 Cara Menggunakan</h2>
    
    <h3 style='color: #4a7dff;'>Langkah 1:</h3>
    <p style='font-size: 18px;'>Pilih "Upload dari file" atau "Ambil foto dengan kamera"</p>
    
    <h3 style='color: #4a7dff;'>Langkah 2:</h3>
    <p style='font-size: 18px;'>Upload foto produk Anda atau ambil foto langsung</p>
    
    <h3 style='color: #4a7dff;'>Langkah 3:</h3>
    <p style='font-size: 18px;'>Klik "Analisis Warna" untuk melihat hasil</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Manfaat singkat
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center;'>
        <h3>✅</h3>
        <h4>Mudah Digunakan</h4>
        <p>Cukup upload foto untuk mulai</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center;'>
        <h3>🎨</h3>
        <h4>Hasil Cepat</h4>
        <p>Analisis warna dalam hitungan detik</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center;'>
        <h3>💰</h3>
        <h4>Gratis</h4>
        <p>Tidak perlu biaya apapun</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# FOOTER SIMPLE
# =============================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
    <p>🎨 <strong>Analisis Warna Produk</strong> - Dibuat dengan Streamlit</p>
    <p>Untuk membantu bisnis kecil memilih warna brand yang tepat</p>
    </div>
    """,
    unsafe_allow_html=True
)