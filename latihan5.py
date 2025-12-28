import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageEnhance
import numpy as np
import colorsys
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from io import BytesIO

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Analisis Koneksi Warna - Smart Color Analyzer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SUPER CSS =================
st.markdown("""
<style>
/* Global Styles */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* DARK THEME - Background hitam */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f1f5f9;
}

/* Glassmorphism - Dark Version */
.glass-card {
    background: rgba(30, 41, 59, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 28px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3), 0 5px 15px rgba(0, 0, 0, 0.2);
    margin-bottom: 28px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    color: #f1f5f9;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 10px 20px rgba(0, 0, 0, 0.3);
}

/* Hero Section - Dark Theme */
.hero-title {
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin-bottom: 16px;
}

.hero-subtitle {
    font-size: 20px;
    color: #cbd5e1;
    font-weight: 500;
    margin-bottom: 24px;
}

/* Badges - Dark Theme */
.badge {
    display: inline-block;
    background: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%);
    color: white;
    padding: 8px 20px;
    border-radius: 50px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(96, 165, 250, 0.3);
}

/* Color Chips - Dark Theme */
.color-chip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
    border-radius: 16px;
    background: rgba(30, 41, 59, 0.9);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    margin-bottom: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    color: #f1f5f9;
}

.color-chip:hover {
    transform: translateX(5px);
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
    background: rgba(41, 56, 80, 0.9);
}

.color-box {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    border: 3px solid rgba(255, 255, 255, 0.1);
}

/* Progress Bar Customization - Dark Theme */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%);
}

/* Sidebar Styling - Dark Theme */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

[data-testid="stSidebar"] .st-bq {
    color: #cbd5e1 !important;
}

[data-testid="stSidebar"] .st-c0 {
    color: #cbd5e1 !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: #cbd5e1 !important;
}

/* Button Styling - Dark Theme */
.stButton > button {
    background: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(96, 165, 250, 0.4);
}

/* Metric Cards - Dark Theme */
.metric-card {
    background: rgba(30, 41, 59, 0.9);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    margin: 10px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 10px 0;
}

.metric-label {
    font-size: 14px;
    color: #94a3b8;
    font-weight: 500;
}

/* Tabs Styling - Dark Theme */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: rgba(30, 41, 59, 0.8);
    border-radius: 12px 12px 0 0;
    padding: 5px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 10px 10px 0 0;
    gap: 1px;
    padding: 10px 24px;
    font-weight: 600;
    color: #94a3b8;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%) !important;
    color: white !important;
}

/* Text colors for dark theme */
h1, h2, h3, h4, h5, h6 {
    color: #f1f5f9 !important;
}

p, span, div {
    color: #cbd5e1 !important;
}

.stMarkdown h1, 
.stMarkdown h2, 
.stMarkdown h3, 
.stMarkdown h4 {
    color: #f1f5f9 !important;
}

/* File Uploader - Dark Theme */
.stFileUploader > div > div {
    border: 2px dashed #475569;
    border-radius: 20px;
    background: rgba(30, 41, 59, 0.7);
}

.stFileUploader > div > div:hover {
    border-color: #60a5fa;
    background: rgba(30, 41, 59, 0.9);
}

/* Success, Info, Warning boxes */
.stSuccess {
    background-color: rgba(21, 128, 61, 0.2) !important;
    border-color: #16a34a !important;
    color: #bbf7d0 !important;
}

.stInfo {
    background-color: rgba(29, 78, 216, 0.2) !important;
    border-color: #3b82f6 !important;
    color: #93c5fd !important;
}

.stWarning {
    background-color: rgba(180, 83, 9, 0.2) !important;
    border-color: #f59e0b !important;
    color: #fde68a !important;
}

/* Code blocks */
.stCode {
    background-color: #1e293b !important;
    border: 1px solid #475569 !important;
}

/* Footer */
footer {
    text-align: center;
    padding: 30px 0;
    color: #94a3b8;
    font-size: 14px;
    background: rgba(15, 23, 42, 0.9);
    border-radius: 20px;
    margin-top: 40px;
}

/* Team Member Cards */
.team-member-card {
    display: inline-block;
    background: linear-gradient(135deg, #334155 0%, #475569 100%);
    color: #f1f5f9;
    padding: 12px 24px;
    border-radius: 25px;
    margin: 6px;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    cursor: pointer;
}

.team-member-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    background: linear-gradient(135deg, #475569 0%, #64748b 100%);
}

/* Table styling for dark theme */
table {
    background-color: rgba(30, 41, 59, 0.9) !important;
    color: #f1f5f9 !important;
}

th {
    background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%) !important;
    color: white !important;
}

td {
    background-color: rgba(30, 41, 59, 0.7) !important;
    color: #cbd5e1 !important;
    border-color: #475569 !important;
}

/* Horizontal rule */
hr {
    border-color: #475569 !important;
    margin: 30px 0 !important;
}

/* Plot background */
.js-plotly-plot, .plotly, .modebar {
    background-color: transparent !important;
}

/* Matplotlib figure background */
figure {
    background-color: transparent !important;
}

.embed-container {
    background-color: transparent !important;
}

/* Badge tags */
span[style*="background"] {
    color: #f1f5f9 !important;
}

/* Streamlit widget text colors */
[data-testid="stMetricLabel"], 
[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
}

.stSelectbox label,
.stSlider label,
.stNumberInput label {
    color: #cbd5e1 !important;
}

/* Fix for all text visibility */
div, p, span, label, h1, h2, h3, h4, h5, h6, li, td, th {
    color: #f1f5f9 !important;
}

/* Make sure code blocks are visible */
code, pre {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
}

</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================
def extract_dominant_colors(image, num=5):
    """Extract dominant colors with improved algorithm"""
    image = image.resize((200, 200))
    img = np.array(image)
    if img.shape[2] == 4:
        img = img[:,:,:3]
    
    # Use K-means approximation for better color extraction
    pixels = img.reshape(-1, 3)
    # Simple color quantization
    q = (pixels // 32) * 32
    colors, counts = np.unique(q, axis=0, return_counts=True)
    
    # Filter out very dark and very light colors
    brightness = colors.mean(axis=1)
    mask = (brightness > 30) & (brightness < 220)
    colors = colors[mask]
    counts = counts[mask]
    
    idx = np.argsort(counts)[-num*2:]
    colors = colors[idx]
    counts = counts[idx]
    
    # Group similar colors
    unique_colors = []
    unique_counts = []
    for color, count in zip(colors, counts):
        if not unique_colors:
            unique_colors.append(color)
            unique_counts.append(count)
        else:
            distances = [np.linalg.norm(color - uc) for uc in unique_colors]
            if min(distances) > 30:
                unique_colors.append(color)
                unique_counts.append(count)
            else:
                idx = np.argmin(distances)
                unique_counts[idx] += count
    
    unique_colors = np.array(unique_colors)
    unique_counts = np.array(unique_counts)
    
    idx = np.argsort(unique_counts)[-num:]
    colors = unique_colors[idx]
    perc = (unique_counts[idx] / unique_counts.sum()) * 100
    s = np.argsort(perc)[::-1]
    
    return colors[s], perc[s]

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def complementary(rgb):
    h,s,v = colorsys.rgb_to_hsv(rgb[0]/255,rgb[1]/255,rgb[2]/255)
    h = (h+0.5)%1
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    return int(r*255),int(g*255),int(b*255)

def generate(rgb, mode):
    h,s,v = colorsys.rgb_to_hsv(rgb[0]/255,rgb[1]/255,rgb[2]/255)
    out=[]
    if mode=="Analog":
        for d in [-0.0833, 0, 0.0833]:
            out.append(colorsys.hsv_to_rgb((h+d)%1,s,v))
    elif mode=="Triadik":
        for i in range(3):
            out.append(colorsys.hsv_to_rgb((h+i/3)%1,s,v))
    elif mode=="Monokromatik":
        for val in np.linspace(0.3, 0.9, 5):
            out.append(colorsys.hsv_to_rgb(h,s,val))
    elif mode=="Split Komplementer":
        base_h = h
        out.append(colorsys.hsv_to_rgb(base_h,s,v))
        out.append(colorsys.hsv_to_rgb((base_h+0.417)%1,s,v))
        out.append(colorsys.hsv_to_rgb((base_h+0.583)%1,s,v))
    elif mode=="Tetradik":
        for i in range(4):
            out.append(colorsys.hsv_to_rgb((h+i*0.25)%1,s,v))
    return [(int(r*255),int(g*255),int(b*255)) for r,g,b in out]

def get_color_name(rgb):
    """Get approximate color name"""
    r, g, b = rgb
    colors = {
        (255,0,0): "Merah",
        (0,255,0): "Hijau",
        (0,0,255): "Biru",
        (255,255,0): "Kuning",
        (255,0,255): "Magenta",
        (0,255,255): "Cyan",
        (255,255,255): "Putih",
        (0,0,0): "Hitam",
        (128,128,128): "Abu-abu"
    }
    
    # Find closest color
    min_dist = float('inf')
    closest_name = "Custom"
    for color_rgb, name in colors.items():
        dist = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, color_rgb))
        if dist < min_dist:
            min_dist = dist
            closest_name = name
    
    return closest_name

def create_color_palette_image(colors, title):
    """Create a beautiful palette image"""
    fig, ax = plt.subplots(figsize=(12, 3), facecolor='#0f172a')
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    for i, color in enumerate(colors):
        rect = patches.Rectangle((i, 0), 1, 1, 
                                color=np.array(color)/255,
                                edgecolor='white',
                                linewidth=3)
        ax.add_patch(rect)
        
        hex_code = rgb_to_hex(color)
        ax.text(i + 0.5, -0.15, hex_code,
                ha='center', va='top',
                fontsize=11, fontweight='bold',
                color='#f1f5f9')
        
        # Add color name
        color_name = get_color_name(color)
        ax.text(i + 0.5, 1.15, color_name,
                ha='center', va='bottom',
                fontsize=10, fontweight='medium',
                color='#94a3b8')
    
    ax.set_xlim(0, len(colors))
    ax.set_ylim(-0.3, 1.3)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color='#f1f5f9')
    ax.axis('off')
    plt.tight_layout()
    
    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, transparent=False, facecolor='#0f172a')
    buf.seek(0)
    plt.close(fig)
    return buf

def calculate_color_harmony_score(colors):
    """Calculate a harmony score for the color palette"""
    if len(colors) < 2:
        return 0
    
    # Convert to HSV for better harmony analysis
    hsv_colors = []
    for rgb in colors:
        h,s,v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        hsv_colors.append([h,s,v])
    
    hsv_colors = np.array(hsv_colors)
    
    # Calculate hue diversity (good for harmony)
    hue_std = np.std(hsv_colors[:,0])
    saturation_mean = np.mean(hsv_colors[:,1])
    value_mean = np.mean(hsv_colors[:,2])
    
    # Score based on principles of color harmony
    score = 0
    score += (1 - hue_std) * 40  # Lower hue variance is often more harmonious
    score += saturation_mean * 30  # Higher saturation is more vibrant
    score += (1 - abs(value_mean - 0.5)) * 30  # Mid brightness is often best
    
    return min(100, max(0, int(score)))

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #f1f5f9; font-size: 28px; margin-bottom: 5px;'>🎨</h1>
        <h2 style='color: #f1f5f9; font-size: 22px; font-weight: 600;'>Smart Color Analyzer</h2>
        <p style='color: #94a3b8; font-size: 14px;'>Analisis Warna Profesional</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Pengaturan Analisis")
    
    num_colors = st.slider(
        "**Jumlah Warna Dominan**",
        min_value=3,
        max_value=8,
        value=5,
        help="Tentukan berapa banyak warna dominan yang ingin diekstrak"
    )
    
    scheme = st.selectbox(
        "**Skema Warna**",
        ["Komplementer", "Analog", "Triadik", "Monokromatik", "Split Komplementer", "Tetradik"],
        help="Pilih jenis skema warna yang ingin dihasilkan"
    )
    
    st.markdown("---")
    
    st.markdown("### 🎯 Tips Penggunaan")
    with st.expander("Klik untuk melihat tips"):
        st.info("""
        1. **Gunakan foto dengan pencahayaan baik**
        2. **Foto produk dengan background sederhana**
        3. **Minimal resolusi 800x600px**
        4. **Format JPG/PNG direkomendasikan**
        5. **Hasil terbaik dengan kontras warna jelas**
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);'>
        <p style='color: #94a3b8; font-size: 12px; text-align: center;'>
        Dibuat dengan ❤️ oleh Tim Analisis Warna ~Emilliano Jovian ~Epri Wibowo ~ Khoirudin ~Novita Rahma Wati ~Heni<br>
        v2.0 | Powered by Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

# ================= HERO SECTION =================
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("""
    <div class='glass-card' style='border-top: 5px solid #60a5fa;'>
        <div class="badge">🚀 AI-Powered Color Analysis</div>
        <div class="hero-title">Smart Color Analyzer</div>
        <div class="hero-subtitle">
        Ekstrak palet warna dari produk Anda dan dapatkan rekomendasi skema warna 
        profesional untuk branding, desain, dan pemasaran visual.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card'>
        <div style='font-size: 40px; color: #60a5fa;'>🎨</div>
        <div class="metric-value">5+</div>
        <div class="metric-label">Skema Warna</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-card'>
        <div style='font-size: 40px; color: #a855f7;'>⚡</div>
        <div class="metric-value">AI</div>
        <div class="metric-label">Analisis Cerdas</div>
    </div>
    """, unsafe_allow_html=True)

# ================= MAIN CONTENT =================
st.markdown("## 📤 Upload Foto Produk")

uploaded_file = st.file_uploader(
    "Seret dan lepas file atau klik untuk memilih",
    type=["jpg", "jpeg", "png", "webp"],
    help="Upload foto produk Anda untuk analisis warna",
    label_visibility="collapsed"
)

if uploaded_file:
    # Process uploaded image
    image = Image.open(uploaded_file)
    
    # Enhance image for better analysis
    enhancer = ImageEnhance.Contrast(image)
    image_enhanced = enhancer.enhance(1.2)
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["🎨 Analisis Warna", "📊 Detail Palet", "💡 Rekomendasi"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class='glass-card'>
                <h3 style='color: #f1f5f9; margin-bottom: 20px;'>📸 Preview Produk</h3>
            """, unsafe_allow_html=True)
            
            # Show image with caption
            st.image(image_enhanced, use_container_width=True, caption="Foto Produk - Enhanced")
            
            # Image info
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Format", uploaded_file.type.split('/')[-1].upper())
            with col_info2:
                st.metric("Dimensi", f"{image.width} × {image.height}")
            with col_info3:
                st.metric("Mode Warna", image.mode)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='glass-card'>
                <h3 style='color: #f1f5f9; margin-bottom: 20px;'>⚡ Analisis Cepat</h3>
            """, unsafe_allow_html=True)
            
            # Extract dominant colors
            colors, percentages = extract_dominant_colors(image_enhanced, num_colors)
            
            # Display color metrics
            st.markdown("### 🎯 Warna Dominan")
            
            for i, (color, perc) in enumerate(zip(colors, percentages)):
                hex_code = rgb_to_hex(color)
                color_name = get_color_name(color)
                
                st.markdown(f"""
                <div class="color-chip">
                    <div style="display:flex; align-items:center; gap:15px;">
                        <div class="color-box" style="background:{hex_code}; 
                             box-shadow: 0 4px 15px {hex_code}80;"></div>
                        <div>
                            <div style="font-weight: 700; font-size: 16px; color: #f1f5f9;">{hex_code}</div>
                            <div style="font-size: 12px; color: #94a3b8;">{color_name}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 700; font-size: 18px; color: #60a5fa;">{perc:.1f}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar with custom styling
                st.markdown(f"""
                <div style="height: 8px; background: #334155; border-radius: 4px; margin: 5px 0 20px 0;">
                    <div style="width: {perc}%; height: 100%; background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%); border-radius: 4px;"></div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='color: #f1f5f9; margin-bottom: 20px;'>📊 Detail Palet Warna</h3>
        """, unsafe_allow_html=True)
        
        # Create comprehensive color palette display
        main_color = colors[0]
        
        # Generate all schemes for comparison
        schemes_data = {}
        scheme_names = ["Komplementer", "Analog", "Triadik", "Monokromatik", "Split Komplementer", "Tetradik"]
        
        for scheme_name in scheme_names:
            if scheme_name == "Komplementer":
                schemes_data[scheme_name] = [main_color, complementary(main_color)]
            else:
                schemes_data[scheme_name] = generate(main_color, scheme_name)
        
        # Display selected scheme prominently
        st.markdown(f"### 🎨 Skema {scheme}")
        
        if scheme == "Komplementer":
            selected_scheme = [main_color, complementary(main_color)]
        else:
            selected_scheme = generate(main_color, scheme)
        
        # Create and display palette image
        palette_img = create_color_palette_image(selected_scheme, f"Skema {scheme}")
        st.image(palette_img, use_container_width=True)
        
        # Calculate harmony score
        harmony_score = calculate_color_harmony_score(selected_scheme)
        
        col_score1, col_score2, col_score3 = st.columns(3)
        with col_score1:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 24px; color: #60a5fa;'>🎯</div>
                <div class="metric-value">{harmony_score}</div>
                <div class="metric-label">Skor Harmoni</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_score2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 24px; color: #a855f7;'>🌈</div>
                <div class="metric-value">{len(selected_scheme)}</div>
                <div class="metric-label">Jumlah Warna</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_score3:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 24px; color: #10b981;'>💫</div>
                <div style='font-size: 18px; font-weight: 700; color: #60a5fa; margin: 10px 0;'>
                    {scheme}
                </div>
                <div class="metric-label">Tipe Skema</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Color codes table
        st.markdown("### 📋 Kode Warna")
        
        color_data = []
        for i, color in enumerate(selected_scheme):
            hex_code = rgb_to_hex(color)
            rgb_code = f"RGB({color[0]}, {color[1]}, {color[2]})"
            color_name = get_color_name(color)
            color_data.append({
                "No": i+1,
                "Warna": f"<div style='background-color:{hex_code}; width:24px; height:24px; border-radius:6px;'></div>",
                "HEX": hex_code,
                "RGB": rgb_code,
                "Nama": color_name
            })
        
        # Convert to HTML table
        html_table = """
        <table style='width:100%; border-collapse: separate; border-spacing: 0 10px;'>
            <thead>
                <tr style='background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%); color: white;'>
                    <th style='padding: 15px; border-radius: 12px 0 0 12px;'>No</th>
                    <th style='padding: 15px;'>Warna</th>
                    <th style='padding: 15px;'>HEX</th>
                    <th style='padding: 15px;'>RGB</th>
                    <th style='padding: 15px; border-radius: 0 12px 12px 0;'>Nama</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for row in color_data:
            html_table += f"""
            <tr style='background: rgba(30, 41, 59, 0.8); box-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
                <td style='padding: 15px; text-align: center; font-weight: 600; color: #f1f5f9;'>{row['No']}</td>
                <td style='padding: 15px; text-align: center;'>{row['Warna']}</td>
                <td style='padding: 15px; font-family: monospace; font-weight: 600; color: #60a5fa;'>{row['HEX']}</td>
                <td style='padding: 15px; font-family: monospace; color: #cbd5e1;'>{row['RGB']}</td>
                <td style='padding: 15px; color: #94a3b8;'>{row['Nama']}</td>
            </tr>
            """
        
        html_table += "</tbody></table>"
        st.markdown(html_table, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='color: #f1f5f9; margin-bottom: 20px;'>💡 Rekomendasi Aplikasi</h3>
        """, unsafe_allow_html=True)
        
        # Recommendations based on color scheme
        recommendations = {
            "Komplementer": [
                "Ideal untuk tombol Call-to-Action",
                "Bagus untuk menciptakan kontras tinggi",
                "Cocok untuk desain yang bold dan eye-catching"
            ],
            "Analog": [
                "Sempurna untuk gradasi warna",
                "Cocok untuk tema yang harmonis",
                "Bagus untuk background dan layout utama"
            ],
            "Triadik": [
                "Ideal untuk dashboard dan data visualization",
                "Cocok untuk desain yang dinamis",
                "Bagus untuk membedakan kategori berbeda"
            ],
            "Monokromatik": [
                "Sempurna untuk brand yang elegant",
                "Cocok untuk tipografi dan hierarki",
                "Bagus untuk desain minimalis"
            ],
            "Split Komplementer": [
                "Ideal untuk desain yang seimbang",
                "Cocok untuk website dan aplikasi",
                "Bagus untuk highlight elemen penting"
            ],
            "Tetradik": [
                "Sempurna untuk desain yang colorful",
                "Cocok untuk media sosial dan konten visual",
                "Bagus untuk infografis dan presentasi"
            ]
        }
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.markdown("### 🎯 Untuk Branding")
            st.success("""
            **Palet ini cocok untuk:**
            - Logo dan identitas visual
            - Material marketing
            - Website dan sosial media
            - Kemasan produk
            """)
            
            st.markdown("### 📱 Untuk UI/UX")
            st.info("""
            **Gunakan warna-warna ini untuk:**
            - Primary Button: Warna utama
            - Secondary Button: Warna kedua
            - Background: Warna paling terang
            - Accent: Warna kontras
            """)
        
        with col_rec2:
            st.markdown("### 💫 Tips Implementasi")
            
            for rec in recommendations.get(scheme, []):
                st.markdown(f"""
                <div style='background: rgba(96, 165, 250, 0.1); padding: 12px 16px; border-radius: 12px; 
                          border-left: 4px solid #60a5fa; margin-bottom: 10px; color: #cbd5e1;'>
                    ✅ {rec}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 📈 Best Practices")
            st.warning("""
            1. **Gunakan 60-30-10 rule** untuk distribusi warna
            2. **Test kontras** untuk aksesibilitas
            3. **Consistency** adalah kunci
            4. **Consider color psychology** untuk target audience
            """)
        
        # Download section
        st.markdown("---")
        st.markdown("### 📥 Download Resources")
        
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            if st.button("💾 Download Palet (PNG)", use_container_width=True):
                # Create downloadable palette image
                palette_img.seek(0)
                st.download_button(
                    label="Klik untuk Download",
                    data=palette_img,
                    file_name=f"palette_{scheme.lower()}.png",
                    mime="image/png",
                    use_container_width=True
                )
        
        with col_dl2:
            if st.button("📋 Copy HEX Codes", use_container_width=True):
                hex_codes = "\n".join([rgb_to_hex(c) for c in selected_scheme])
                st.code(hex_codes, language="text")
        
        with col_dl3:
            if st.button("🎨 CSS Variables", use_container_width=True):
                css_vars = ":root {\n"
                for i, color in enumerate(selected_scheme):
                    hex_code = rgb_to_hex(color)
                    css_vars += f"  --color-{i+1}: {hex_code};\n"
                css_vars += "}"
                st.code(css_vars, language="css")
        
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Show sample/demo when no image uploaded
    st.markdown("""
    <div class='glass-card' style='text-align: center; padding: 60px 40px;'>
        <div style='font-size: 80px; margin-bottom: 20px; color: #60a5fa;'>🎨</div>
        <h2 style='color: #f1f5f9; margin-bottom: 20px;'>Mulai Analisis Warna Anda</h2>
        <p style='color: #94a3b8; font-size: 16px; margin-bottom: 30px;'>
        Upload foto produk Anda untuk mengekstrak palet warna dan mendapatkan<br>
        rekomendasi skema warna profesional secara instan.
        </p>
        
        <div style='display: inline-block; background: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%); 
             color: white; padding: 15px 30px; border-radius: 50px; font-weight: 600; margin-top: 20px;'>
            📤 Upload Foto Pertama Anda
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show sample color schemes
    st.markdown("### ✨ Contoh Skema Warna")
    
    sample_col1, sample_col2, sample_col3 = st.columns(3)
    
    with sample_col1:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #f1f5f9;'>🎯 Komplementer</h4>
            <div style='display: flex; gap: 5px; margin: 15px 0;'>
                <div style='flex: 1; height: 80px; background: #60a5fa; border-radius: 12px;'></div>
                <div style='flex: 1; height: 80px; background: #f59e0b; border-radius: 12px;'></div>
            </div>
            <p style='font-size: 12px; color: #94a3b8;'>Kontras tinggi, eye-catching</p>
        </div>
        """, unsafe_allow_html=True)
    
    with sample_col2:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #f1f5f9;'>🌈 Analog</h4>
            <div style='display: flex; gap: 5px; margin: 15px 0;'>
                <div style='flex: 1; height: 80px; background: #60a5fa; border-radius: 12px;'></div>
                <div style='flex: 1; height: 80px; background: #8b5cf6; border-radius: 12px;'></div>
                <div style='flex: 1; height: 80px; background: #a855f7; border-radius: 12px;'></div>
            </div>
            <p style='font-size: 12px; color: #94a3b8;'>Harmonis, natural flow</p>
        </div>
        """, unsafe_allow_html=True)
    
    with sample_col3:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #f1f5f9;'>⚡ Triadik</h4>
            <div style='display: flex; gap: 5px; margin: 15px 0;'>
                <div style='flex: 1; height: 80px; background: #60a5fa; border-radius: 12px;'></div>
                <div style='flex: 1; height: 80px; background: #f59e0b; border-radius: 12px;'></div>
                <div style='flex: 1; height: 80px; background: #10b981; border-radius: 12px;'></div>
            </div>
            <p style='font-size: 12px; color: #94a3b8;'>Dinamis, energik</p>
        </div>
        """, unsafe_allow_html=True)

# ================= FOOTER (Dihapus) =================
# Bagian footer/team developer telah dihapus sesuai permintaan