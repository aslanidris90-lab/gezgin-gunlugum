import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Gezgin v4.0", layout="centered")

st.title("📸 Gezgin Günlüğüm Pro")

# Kamera Girişi (iPhone'da kamera açar)
resim = st.camera_input("Gittiğin Yerden Bir Kare Çek")

# Harita ve Tıklama Özelliği
m = folium.Map(location=[39, 35], zoom_start=5, tiles="CartoDB dark_matter")

# Haritaya tıklandığında ne olacağını yakalayalım
harita_verisi = st_folium(m, width="100%", height=400)

if harita_verisi["last_clicked"]:
    lat = harita_verisi["last_clicked"]["lat"]
    lng = harita_verisi["last_clicked"]["lng"]
    st.success(f"Seçilen Konum: {lat:.2f}, {lng:.2f}")
    
    with st.expander("📝 Bu Konuma Not Yaz"):
        baslik = st.text_input("Yer Adı")
        not_alani = st.text_area("Anıların...")
        if st.button("Anıyı Ölümsüzleştir"):
            st.balloons() # Kutlama!
            st.info(f"{baslik} kaydedildi!")
