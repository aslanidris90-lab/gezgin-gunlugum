import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os
from datetime import datetime

# 1. Sayfa Ayarları (Mobil İçin Kritik: 'centered' düzeni telefon ekranına tam oturur)
st.set_page_config(
    page_title="Gezgin Günlüğü", 
    page_icon="🌍", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Modern & Oval Tasarım (CSS ile iPhone stili)
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #0e1117; }
    
    /* Oval Butonlar */
    .stButton>button {
        border-radius: 25px;
        background-color: #ff4d4d;
        color: white;
        font-weight: bold;
        border: none;
        height: 3em;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff3333; border: none; }
    
    /* Oval Giriş Alanları */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 15px;
        background-color: #1a1c24;
        color: white;
        border: 1px solid #333;
    }
    
    /* Başlık Stili */
    h1 { color: #ff4d4d; font-family: 'Segoe UI', sans-serif; text-align: center; }
    
    /* Harita Çerçevesi */
    iframe { border-radius: 20px; border: 2px solid #222; }
    </style>
    """, unsafe_allow_html=True)

# 3. Veri Yönetimi (Basit JSON Kaydı)
def verileri_yukle():
    if os.path.exists("mobil_veriler.json"):
        with open("mobil_veriler.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def veri_kaydet(yeni_not):
    veriler = verileri_yukle()
    veriler.append(yeni_not)
    with open("mobil_veriler.json", "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=4)

# --- UYGULAMA BAŞLANGICI ---
st.title("🌍 Dünya Günlüğüm")

# Harita Ayarları
m = folium.Map(
    location=[25, 10], 
    zoom_start=2, 
    tiles="CartoDB dark_matter",
    zoom_control=False # Mobil ekranında kalabalık yapmasın
)

# Kayıtlı anıları haritaya işaretle (Marker ekle)
anilar = verileri_yukle()
for ani in anilar:
    folium.Marker(
        location=ani["konum"],
        popup=f"<b>{ani['ulke']}</b><br>{ani['not']}",
        tooltip=ani['ulke'],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Haritayı Görüntüle (Dokunmatik uyumlu)
st_data = st_folium(m, width="100%", height=400)

# Alt Panel: Yeni Keşif Ekle
st.write("---")
with st.container():
    st.subheader("📝 Yeni Bir Yer Keşfet")
    
    col1, col2 = st.columns(2)
    with col1:
        ulke_adi = st.text_input("Ülke/Şehir Adı", placeholder="Örn: İtalya")
    with col2:
        tarih = st.date_input("Ziyaret Tarihi", datetime.now())
        
    gezi_notu = st.text_area("Neler Gördün?", placeholder="Anılarını buraya yaz...")

    if st.button("Anıyı Buluta Kaydet 🚀"):
        if ulke_adi and gezi_notu:
            # Haritaya rastgele veya seçilen bir koordinat atayalım (Şimdilik örnek koordinat)
            yeni_ani = {
                "ulke": ulke_adi,
                "not": gezi_notu,
                "tarih": str(tarih),
                "konum": [20, 0] # Gerçekte harita tıklamasından alınabilir
            }
            veri_kaydet(yeni_ani)
            st.success(f"Harika! {ulke_adi} anıların başarıyla saklandı.")
            st.rerun()
        else:
            st.warning("Lütfen ülke adını ve notunu boş bırakma!")

# İstatistikler
st.sidebar.header("📊 Keşif Durumu")
st.sidebar.write(f"Toplam Gezilen Yer: {len(anilar)}")
if len(anilar) > 0:
    st.sidebar.progress(min(len(anilar) * 5, 100)) # Her yer %5 ilerleme gibi
