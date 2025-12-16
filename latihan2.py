import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import colorsys
import warnings
import cv2
import tempfile
import os
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Koneksi Warna",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CSS CUSTOM UNTUK BACKGROUND BIRU
# =============================================
st.markdown(
    """
    <style>
    /* Background utama aplikasi */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2a5298 0%, #1e3c72 100%);
        border-right: 2px solid #4a7dff;
    }
    
    /* Header dan judul */
    .stTitle, h1, h2, h3, h4, h5, h6 {
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 5px;
        margin: 2px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #4a7dff, #2a5bd7) !important;
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #4a7dff, #2a5bd7);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #2a5bd7, #1e3c72);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        border: 2px dashed rgba(255, 255, 255, 0.3);
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
    }
    
    /* Metric cards */
    .stMetric {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4a7dff, #2a5bd7);
    }
    
    /* Selectbox and slider */
    .stSelectbox, .stSlider {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Markdown text color */
    .stMarkdown {
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Card containers */
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
    }
    
    /* Footer styling */
    .footer {
        background: rgba(0, 0, 0, 0.2);
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
        text-align: center;
        border-top: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4a7dff, #2a5bd7);
        border-radius: 5px;
    }
    
    /* Matplotlib figure background */
    .stPlotlyChart, .stPyplot {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
    }
    
    /* Color picker styling */
    .stColorPicker {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 5px;
    }
    
    /* Success message */
    .stSuccess {
        background: rgba(46, 204, 113, 0.2);
        border: 1px solid rgba(46, 204, 113, 0.5);
        color: white;
    }
    
    /* Error message */
    .stError {
        background: rgba(231, 76, 60, 0.2);
        border: 1px solid rgba(231, 76, 60, 0.5);
        color: white;
    }
    
    /* Warning message */
    .stWarning {
        background: rgba(241, 196, 15, 0.2);
        border: 1px solid rgba(241, 196, 15, 0.5);
        color: white;
    }
    
    /* Info message */
    .stInfo {
        background: rgba(52, 152, 219, 0.2);
        border: 1px solid rgba(52, 152, 219, 0.5);
        color: white;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# =============================================
# FUNGSI UTAMA
# =============================================

def extract_dominant_colors(image, num_colors=5):
    """Mengekstrak warna dominan menggunakan metode sederhana"""
    # Resize gambar untuk mempercepat processing
    image = image.resize((100, 100))
    img_array = np.array(image)
    
    # Handle gambar dengan alpha channel
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    
    # Quantize colors manually - sederhanakan warna
    quantized = (img_array // 32) * 32
    pixels = quantized.reshape(-1, 3)
    
    # Get unique colors and counts
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    # Get top N colors
    if len(unique_colors) > num_colors:
        top_indices = np.argsort(counts)[-num_colors:]
        dominant_colors = unique_colors[top_indices]
        percentages = (counts[top_indices] / counts.sum()) * 100
    else:
        dominant_colors = unique_colors
        percentages = (counts / counts.sum()) * 100
    
    # Sort by percentage (descending)
    sorted_indices = np.argsort(percentages)[::-1]
    return dominant_colors[sorted_indices], percentages[sorted_indices]

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def get_complementary_color(rgb_color):
    """Mendapatkan warna komplementer"""
    hsv = colorsys.rgb_to_hsv(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
    comp_hue = (hsv[0] + 0.5) % 1.0
    comp_rgb = colorsys.hsv_to_rgb(comp_hue, hsv[1], hsv[2])
    return tuple(int(c * 255) for c in comp_rgb)

def generate_analogous_colors(rgb_color, num_colors=3):
    """Generate warna analog"""
    hsv = colorsys.rgb_to_hsv(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
    analogous = []
    for i in range(num_colors):
        hue = (hsv[0] + (i-1)*0.083) % 1.0  # 30 derajat difference
        analogous.append(colorsys.hsv_to_rgb(hue, hsv[1], hsv[2]))
    return [tuple(int(c * 255) for c in rgb) for rgb in analogous]

def generate_triadic_colors(rgb_color):
    """Generate warna triadic"""
    hsv = colorsys.rgb_to_hsv(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
    triadic = []
    for i in range(3):
        hue = (hsv[0] + i/3) % 1.0
        triadic.append(colorsys.hsv_to_rgb(hue, hsv[1], hsv[2]))
    return [tuple(int(c * 255) for c in rgb) for rgb in triadic]

def generate_monochromatic_colors(rgb_color, num_colors=5):
    """Generate warna monokromatik"""
    hsv = colorsys.rgb_to_hsv(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
    monochromatic = []
    for i in range(num_colors):
        value = 0.3 + (i * 0.7/(num_colors-1))  # Vary brightness
        monochromatic.append(colorsys.hsv_to_rgb(hsv[0], hsv[1], min(value, 1.0)))
    return [tuple(int(c * 255) for c in rgb) for rgb in monochromatic]

def display_color_palette(colors, percentages, title="Warna Dominan"):
    """Menampilkan palette warna dengan persentase"""
    fig, axes = plt.subplots(1, len(colors), figsize=(15, 3))
    fig.patch.set_facecolor('#1e3c72')
    
    if len(colors) == 1:
        axes = [axes]
    
    for i, (color, percentage) in enumerate(zip(colors, percentages)):
        axes[i].add_patch(patches.Rectangle((0, 0), 1, 1, color=np.array(color)/255))
        axes[i].set_title(f'{percentage:.1f}%', fontsize=10, pad=10, color='white')
        axes[i].text(0.5, -0.2, f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}', 
                    ha='center', va='top', transform=axes[i].transAxes, fontsize=8, color='white')
        axes[i].set_facecolor('#1e3c72')
        axes[i].axis('off')
    
    plt.suptitle(title, y=1.1, color='white', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

def display_color_scheme(colors, scheme_name):
    """Menampilkan skema warna yang direkomendasikan"""
    fig, axes = plt.subplots(1, len(colors), figsize=(12, 2))
    fig.patch.set_facecolor('#1e3c72')
    
    if len(colors) == 1:
        axes = [axes]
    
    for i, color in enumerate(colors):
        axes[i].add_patch(patches.Rectangle((0, 0), 1, 1, color=np.array(color)/255))
        axes[i].set_title(f'Warna {i+1}', fontsize=9, pad=8, color='white')
        axes[i].text(0.5, -0.2, f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}', 
                    ha='center', va='top', transform=axes[i].transAxes, fontsize=7, color='white')
        axes[i].set_facecolor('#1e3c72')
        axes[i].axis('off')
    
    plt.suptitle(f'Skema Warna {scheme_name}', y=1.2, color='white', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

def analyze_color_harmony(colors):
    """Menganalisis harmoni warna secara sederhana"""
    if len(colors) < 2:
        return "Tidak cukup warna untuk analisis"
    
    brightness_diffs = []
    for i in range(len(colors)):
        for j in range(i+1, len(colors)):
            bright1 = sum(colors[i]) / 3
            bright2 = sum(colors[j]) / 3
            brightness_diffs.append(abs(bright1 - bright2))
    
    avg_bright_diff = np.mean(brightness_diffs)
    
    if avg_bright_diff > 100:
        return "Kontras Tinggi"
    elif avg_bright_diff > 50:
        return "Kontras Baik"
    else:
        return "Harmoni Lembut"

# =============================================
# SIDEBAR
# =============================================

st.sidebar.title("🎨 Pengaturan Analisis Warna")
st.sidebar.markdown("---")

num_colors = st.sidebar.slider("Jumlah Warna Dominan", 3, 8, 5, 
                               help="Pilih jumlah warna dominan yang ingin diekstrak dari gambar")
color_scheme_type = st.sidebar.selectbox(
    "Skema Warna yang Disukai",
    ["Komplementer", "Analog", "Triadik", "Monokromatik", "Semua Skema"],
    help="Pilih jenis skema warna untuk rekomendasi"
)

st.sidebar.markdown("---")
st.sidebar.info("""
**🎯 Tips Penggunaan:** 
- 📸 Upload foto dengan pencahayaan yang baik
- 🎨 Pilih jumlah warna sesuai kompleksitas gambar
- 💡 Gunakan skema warna yang sesuai dengan identitas brand
- 🌟 Gunakan background yang kontras untuk hasil terbaik
""")

# =============================================
# MAIN CONTENT
# =============================================

st.title("🎨 Analisis Koneksi Warna Foto Produk")
st.markdown("### Analisis koneksi warna dari foto produk dan dapatkan rekomendasi palette yang harmonis")

# Inisialisasi session state untuk menyimpan gambar
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'image_source' not in st.session_state:
    st.session_state.image_source = None

# Tab untuk pilihan input gambar
tab1, tab2 = st.tabs(["📁 **Upload Gambar**", "📷 **Ambil dari Kamera**"])

with tab1:
    st.subheader("📤 Upload Gambar dari File")
    st.markdown("Unggah foto produk Anda dalam format JPG, PNG, atau JPEG")
    
    uploaded_file = st.file_uploader(
        "Pilih file gambar...", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload gambar produk dengan background yang bersih untuk hasil terbaik",
        key="file_uploader_tab1"
    )
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.session_state.current_image = image
            st.session_state.image_source = "upload"
            st.success("✅ Gambar berhasil diupload!")
            st.image(image, use_container_width=True, caption="Preview Gambar")
            
            # Tombol untuk melanjutkan analisis
            if st.button("🔍 Analisis Gambar Ini", type="primary", use_container_width=True):
                st.rerun()
        except Exception as e:
            st.error(f"❌ Error loading image: {str(e)}")

with tab2:
    st.subheader("📷 Ambil Foto dengan Kamera")
    st.markdown("Gunakan kamera perangkat Anda untuk mengambil foto produk secara langsung")
    
    # Gunakan st.camera_input yang lebih sederhana
    camera_photo = st.camera_input(
        "Ambil foto produk Anda",
        help="Pastikan kamera sudah diizinkan di browser",
        key="camera_input_tab2"
    )
    
    if camera_photo is not None:
        try:
            image = Image.open(camera_photo)
            st.session_state.current_image = image
            st.session_state.image_source = "camera"
            st.success("✅ Foto berhasil diambil!")
            st.image(image, use_container_width=True, caption="Foto dari Kamera")
            
            # Tombol untuk melanjutkan analisis
            if st.button("🔍 Analisis Foto Ini", type="primary", use_container_width=True):
                st.rerun()
        except Exception as e:
            st.error(f"❌ Error processing camera image: {str(e)}")

# =============================================
# ANALISIS GAMBAR
# =============================================

if st.session_state.current_image is not None:
    image = st.session_state.current_image
    image_source = st.session_state.image_source
    
    try:
        # Container untuk analisis utama
        with st.container():
            # Layout utama
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Card untuk foto produk
                with st.container():
                    st.subheader("📸 Foto Produk")
                    caption = "Foto Produk yang Diupload" if image_source == "upload" else "Foto dari Kamera"
                    st.image(image, use_container_width=True, caption=caption)
                    
                    # Ekstrak warna dominan
                    with st.spinner("🔍 Menganalisis warna dominan..."):
                        dominant_colors, percentages = extract_dominant_colors(image, num_colors)
                    
                    # Card untuk analisis warna dominan
                    with st.container():
                        st.subheader("🎨 Analisis Warna Dominan")
                        display_color_palette(dominant_colors, percentages)
                        
                        # Analisis harmoni warna dalam metric card
                        col_metric1, col_metric2 = st.columns(2)
                        with col_metric1:
                            harmony_score = analyze_color_harmony(dominant_colors)
                            st.metric("🎯 Skor Harmoni Warna", harmony_score)
                        with col_metric2:
                            st.metric("🌈 Jumlah Warna", len(dominant_colors))
                        
                        # Tampilkan informasi warna dalam tabel
                        st.subheader("📊 Informasi Detail Warna")
                        for i, (color, percentage) in enumerate(zip(dominant_colors, percentages)):
                            hex_code = rgb_to_hex(color)
                            col_a, col_b, col_c = st.columns([1, 2, 2])
                            with col_a:
                                st.color_picker(f"Warna {i+1}", hex_code, key=f"picker_{i}")
                            with col_b:
                                st.markdown(f"**Warna {i+1}**")
                                st.code(f"RGB: {tuple(color)}", language='python')
                                st.code(f"HEX: {hex_code}", language='python')
                            with col_c:
                                st.markdown(f"**Persentase:**")
                                st.markdown(f"### {percentage:.1f}%")
                                st.progress(int(percentage) / 100)
            
            with col2:
                # Card untuk skema warna yang direkomendasikan
                with st.container():
                    st.subheader("💡 Skema Warna yang Direkomendasikan")
                    
                    # Generate recommended color schemes
                    primary_color = dominant_colors[0]
                    
                    if color_scheme_type in ["Komplementer", "Semua Skema"]:
                        comp_color = get_complementary_color(primary_color)
                        display_color_scheme([primary_color, comp_color], "Komplementer")
                        st.caption("🎭 Warna komplementer memberikan kontras tinggi")
                    
                    if color_scheme_type in ["Analog", "Semua Skema"]:
                        analog_colors = generate_analogous_colors(primary_color)
                        display_color_scheme(analog_colors, "Analog")
                        st.caption("🌿 Warna analog menciptakan harmoni yang natural")
                    
                    if color_scheme_type in ["Triadik", "Semua Skema"]:
                        triadic_colors = generate_triadic_colors(primary_color)
                        display_color_scheme(triadic_colors, "Triadik")
                        st.caption("⚡ Warna triadik memberikan keseimbangan yang dinamis")
                    
                    if color_scheme_type in ["Monokromatik", "Semua Skema"]:
                        mono_colors = generate_monochromatic_colors(primary_color)
                        display_color_scheme(mono_colors, "Monokromatik")
                        st.caption("🎩 Warna monokromatik menciptakan kesan elegan dan konsisten")
                    
                    # Card untuk tips aplikasi
                    with st.container():
                        st.subheader("🎯 Tips Aplikasi")
                        
                        product_type = st.selectbox(
                            "Pilih Tipe Produk",
                            ["Fashion/Pakaian", "Makanan/Minuman", "Elektronik", "Kecantikan/Kosmetik", "Dekorasi Rumah", "Lainnya"],
                            key="product_type_select"
                        )
                        
                        tips = {
                            "Fashion/Pakaian": """
                            ✅ **Gunakan warna netral** sebagai base warna  
                            ✅ **Tambahkan warna cerah** sebagai aksen menarik  
                            ✅ **Perhatikan tren warna** musiman untuk relevansi  
                            ✅ **Konsistensi** dengan identitas brand yang ada
                            """,
                            "Makanan/Minuman": """
                            ✅ **Warna hangat** untuk makanan panas dan comfort food  
                            ✅ **Warna segar** untuk makanan dingin dan minuman  
                            ✅ **Highlight warna natural** untuk kesan sehat  
                            ✅ **Gunakan kontras** untuk menonjalkan tekstur makanan
                            """,
                            "Elektronik": """
                            ✅ **Skema warna modern** dan minimalis untuk produk tech  
                            ✅ **Gunakan aksen warna techy** seperti biru, silver, hitam  
                            ✅ **Warna metalik** untuk kesan premium dan futuristik  
                            ✅ **Konsistensi** dengan desain UI/UX produk
                            """,
                            "Kecantikan/Kosmetik": """
                            ✅ **Soft pastel** untuk skincare dan produk natural  
                            ✅ **Bold colors** untuk makeup dan produk fashion  
                            ✅ **Luxury feel** dengan warna emas/perak untuk premium  
                            ✅ **Clean appearance** untuk kesan higienis
                            """,
                            "Dekorasi Rumah": """
                            ✅ **Earth tones** untuk natural look dan rustic style  
                            ✅ **Bright colors** untuk statement pieces dan aksen  
                            ✅ **Konsistensi** dengan estetik ruangan dan tema  
                            ✅ **Pertimbangkan** kondisi pencahayaan ruangan
                            """,
                            "Lainnya": """
                            ✅ **Pertimbangkan** target audience dan demografi  
                            ✅ **Test** berbagai skema warna untuk optimalisasi  
                            ✅ **Konsistensi** dengan identitas brand yang kuat  
                            ✅ **Perhatikan** asosiasi kultural dan psikologis warna
                            """
                        }
                        
                        st.info(tips[product_type])
                    
                    # Card untuk kontrol
                    with st.container():
                        st.subheader("🔄 Kontrol")
                        col_d1, col_d2 = st.columns(2)
                        
                        with col_d1:
                            if st.button("💾 Simpan Laporan", use_container_width=True):
                                st.success("✅ Laporan berhasil dibuat! (Simpan screenshot untuk menyimpan hasil)")
                                st.balloons()
                        
                        with col_d2:
                            if st.button("🔄 Gambar Baru", use_container_width=True):
                                # Reset session state
                                st.session_state.current_image = None
                                st.session_state.image_source = None
                                st.rerun()
                        
                        st.markdown("---")
                        st.caption("📌 **Tips:** Gunakan screenshot untuk menyimpan hasil analisis")
    
    except Exception as e:
        st.error(f"❌ Error saat memproses gambar: {str(e)}")
        st.info("ℹ️ Silakan coba upload file gambar yang berbeda atau ambil foto ulang.")

else:
    # Show instructions when no file is uploaded
    st.markdown("""
    <div style='background: rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 15px; border: 2px solid rgba(255, 255, 255, 0.2);'>
    <h2 style='color: white; text-align: center;'>📋 Cara Menggunakan Tool Ini</h2>
    
    <h3 style='color: #4a7dff;'>Pilih salah satu metode input:</h3>
    
    <div style='display: flex; justify-content: space-between; margin: 20px 0;'>
        <div style='flex: 1; background: rgba(74, 125, 255, 0.2); padding: 20px; border-radius: 10px; margin: 0 10px; text-align: center;'>
            <h4>📁 Upload File</h4>
            <p>Upload foto produk dari perangkat Anda</p>
        </div>
        <div style='flex: 1; background: rgba(74, 125, 255, 0.2); padding: 20px; border-radius: 10px; margin: 0 10px; text-align: center;'>
            <h4>📷 Ambil Foto</h4>
            <p>Gunakan kamera untuk mengambil foto langsung</p>
        </div>
    </div>
    
    <h3 style='color: #4a7dff;'>Langkah Analisis:</h3>
    <ol style='color: white;'>
        <li><strong>Pilih</strong> metode input gambar yang diinginkan</li>
        <li><strong>Unggah atau ambil</strong> foto produk Anda</li>
        <li><strong>Klik "Analisis Gambar Ini"</strong> untuk memulai analisis</li>
        <li><strong>Atur pengaturan</strong> analisis warna di sidebar</li>
        <li><strong>Jelajahi</strong> rekomendasi skema warna yang cocok</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Manfaat dengan icon
    col_ben1, col_ben2, col_ben3, col_ben4 = st.columns(4)
    
    with col_ben1:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center; height: 150px;'>
        <h3 style='color: #4a7dff;'>✅</h3>
        <h4>Konsistensi Warna</h4>
        <p>Pertahankan konsistensi warna brand</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ben2:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center; height: 150px;'>
        <h3 style='color: #4a7dff;'>🎨</h3>
        <h4>Estetika Lebih Baik</h4>
        <p>Ciptakan tampilan produk yang menarik</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ben3:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center; height: 150px;'>
        <h3 style='color: #4a7dff;'>💰</h3>
        <h4>Meningkatkan Penjualan</h4>
        <p>Warna yang menarik perhatian customer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ben4:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center; height: 150px;'>
        <h3 style='color: #4a7dff;'>🏆</h3>
        <h4>Pengenalan Brand</h4>
        <p>Asosiasi warna yang kuat dengan brand Anda</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Contoh skema warna
    st.subheader("🎨 Contoh Skema Warna")
    
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    
    with col_ex1:
        with st.container():
            st.markdown("### **Skema Komplementer**")
            st.markdown("Warna yang berseberangan di color wheel")
            example_colors = [(255, 100, 100), (100, 255, 100)]
            fig, axes = plt.subplots(1, 2, figsize=(6, 2))
            fig.patch.set_facecolor('#1e3c72')
            for i, color in enumerate(example_colors):
                axes[i].add_patch(patches.Rectangle((0, 0), 1, 1, color=np.array(color)/255))
                axes[i].set_facecolor('#1e3c72')
                axes[i].axis('off')
            st.pyplot(fig)
            st.caption("Ideal untuk call-to-action")
    
    with col_ex2:
        with st.container():
            st.markdown("### **Skema Analog**")
            st.markdown("Warna yang berdekatan di color wheel")
            example_colors = [(255, 100, 100), (255, 150, 100), (255, 200, 100)]
            fig, axes = plt.subplots(1, 3, figsize=(6, 2))
            fig.patch.set_facecolor('#1e3c72')
            for i, color in enumerate(example_colors):
                axes[i].add_patch(patches.Rectangle((0, 0), 1, 1, color=np.array(color)/255))
                axes[i].set_facecolor('#1e3c72')
                axes[i].axis('off')
            st.pyplot(fig)
            st.caption("Menciptakan harmoni yang lembut")
    
    with col_ex3:
        with st.container():
            st.markdown("### **Skema Monokromatik**")
            st.markdown("Variasi gelap-terang dari satu warna")
            example_colors = [(100, 150, 255), (150, 180, 255), (200, 210, 255)]
            fig, axes = plt.subplots(1, 3, figsize=(6, 2))
            fig.patch.set_facecolor('#1e3c72')
            for i, color in enumerate(example_colors):
                axes[i].add_patch(patches.Rectangle((0, 0), 1, 1, color=np.array(color)/255))
                axes[i].set_facecolor('#1e3c72')
                axes[i].axis('off')
            st.pyplot(fig)
            st.caption("Elegan dan konsisten")

# Footer
st.markdown("---")
st.markdown(
    """
    <div class='footer'>
    <h3 style='color: #4a7dff;'>🎨 Analisis Koneksi Warna</h3>
    <p>Gunakan tool ini untuk meningkatkan visual branding produk Anda • Dibuat dengan ❤️ menggunakan Streamlit</p>
    <p><strong>👥 Kelompok:</strong> Emiliano Jovian, Epri Wibowo, Khoirrudin, Novita Rahma Wati, Heni</p>
    </div>
    """,
    unsafe_allow_html=True
)