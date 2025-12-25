import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import colorsys
import warnings
warnings.filterwarnings('ignore')

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Analisis Koneksi Warna",
    page_icon="🎨",
    layout="wide"
)

# ================= SUPER CSS =================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eef2ff, #fdf2f8);
}
.glass {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    margin-bottom: 24px;
}
.hero-title {
    font-size: 42px;
    font-weight: 900;
    background: linear-gradient(90deg,#4f46e5,#ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #6b7280;
    font-size: 18px;
}
.badge {
    display:inline-block;
    background:#eef2ff;
    color:#4338ca;
    padding:6px 16px;
    border-radius:999px;
    font-size:14px;
    margin-bottom:10px;
}
.color-chip {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:10px 16px;
    border-radius:14px;
    background:white;
    box-shadow:0 4px 12px rgba(0,0,0,.05);
    margin-bottom:10px;
}
.color-box {
    width:36px;
    height:36px;
    border-radius:8px;
}
footer {
    text-align:center;
    color:#6b7280;
}
</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================
def extract_dominant_colors(image, num=5):
    image = image.resize((100,100))
    img = np.array(image)
    if img.shape[2] == 4:
        img = img[:,:,:3]
    q = (img // 32) * 32
    pixels = q.reshape(-1,3)
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    idx = np.argsort(counts)[-num:]
    colors = colors[idx]
    perc = (counts[idx] / counts.sum()) * 100
    s = np.argsort(perc)[::-1]
    return colors[s], perc[s]

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def complementary(rgb):
    h,s,v = colorsys.rgb_to_hsv(rgb[0]/255,rgb[1]/255,rgb[2]/255)
    h = (h+0.5)%1
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    return int(r*255),int(g*255),int(b*255)

def generate(rgb, mode):
    h,s,v = colorsys.rgb_to_hsv(rgb[0]/255,rgb[1]/255,rgb[2]/255)
    out=[]
    if mode=="Analog":
        for d in [-0.08,0,0.08]:
            out.append(colorsys.hsv_to_rgb((h+d)%1,s,v))
    elif mode=="Triadik":
        for i in range(3):
            out.append(colorsys.hsv_to_rgb((h+i/3)%1,s,v))
    elif mode=="Monokromatik":
        for val in np.linspace(0.35,1,5):
            out.append(colorsys.hsv_to_rgb(h,s,val))
    return [(int(r*255),int(g*255),int(b*255)) for r,g,b in out]

def show_palette(colors,title):
    fig,ax = plt.subplots(1,len(colors),figsize=(10,2))
    if len(colors)==1: ax=[ax]
    for i,c in enumerate(colors):
        ax[i].add_patch(patches.Rectangle((0,0),1,1,color=np.array(c)/255))
        ax[i].text(0.5,-0.25,rgb_to_hex(c),
                   ha="center",transform=ax[i].transAxes,fontsize=9)
        ax[i].axis("off")
    plt.suptitle(title)
    st.pyplot(fig)

# ================= SIDEBAR =================
st.sidebar.title("🎛 Kontrol Analisis")
st.sidebar.caption("Atur visualisasi warna")
num_colors = st.sidebar.slider("Jumlah Warna Dominan",3,8,5)
scheme = st.sidebar.selectbox(
    "Skema Warna",
    ["Komplementer","Analog","Triadik","Monokromatik"]
)

# ================= HERO =================
st.markdown("""
<div class="glass">
<span class="badge">🎨 Smart Color Analyzer</span>
<div class="hero-title">Analisis Koneksi Warna</div>
<p class="hero-sub">
Tool cerdas untuk menganalisis warna dominan foto produk dan menghasilkan
rekomendasi skema warna profesional untuk branding & desain visual.
</p>
</div>
""", unsafe_allow_html=True)

# ================= UPLOAD =================
uploaded = st.file_uploader("📤 Upload Foto Produk", type=["jpg","jpeg","png"])

if uploaded:
    image = Image.open(uploaded)
    col1,col2 = st.columns([2,1])

    with col1:
        st.markdown("<div class='glass'>",unsafe_allow_html=True)
        st.subheader("📸 Preview Produk")
        st.image(image,use_column_width=True)

        colors,perc = extract_dominant_colors(image,num_colors)
        st.subheader("🎨 Warna Dominan")

        for c,p in zip(colors,perc):
            st.markdown(f"""
            <div class="color-chip">
                <div style="display:flex;align-items:center;gap:12px">
                    <div class="color-box" style="background:{rgb_to_hex(c)}"></div>
                    <b>{rgb_to_hex(c)}</b>
                </div>
                <span>{p:.1f}%</span>
            </div>
            """,unsafe_allow_html=True)
            st.progress(int(p))

        st.markdown("</div>",unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass'>",unsafe_allow_html=True)
        st.subheader("💡 Skema Warna Rekomendasi")

        main = colors[0]
        if scheme=="Komplementer":
            show_palette([main,complementary(main)],"Komplementer")
        else:
            show_palette(generate(main,scheme),scheme)

        st.success("Skema ini direkomendasikan untuk meningkatkan daya tarik visual.")
        st.markdown("</div>",unsafe_allow_html=True)

else:
    st.markdown("<div class='glass'>",unsafe_allow_html=True)
    st.subheader("✨ Contoh Visual Skema Warna")
    show_palette([(255,80,80),(80,255,80)],"Komplementer")
    st.markdown("</div>",unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<footer>
<hr>
<b>Analisis Koneksi Warna</b><br>
Kelompok: Emiliano Jovian, Epri Wibowo, Khoirrudin, Novita Rahma Wati, Heni
</footer>
""", unsafe_allow_html=True)