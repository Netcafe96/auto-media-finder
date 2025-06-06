import streamlit as st import requests from bs4 import BeautifulSoup from urllib.parse import quote import re import os import google.generativeai as genai from PIL import Image from io import BytesIO

st.set_page_config(page_title="Space Media Finder", layout="wide") st.title("🚀 Tìm Ảnh & Video Khoa Học Vũ Trụ từ Kịch Bản")

--- Thiết lập Gemini API ---

API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") if API_KEY: genai.configure(api_key=API_KEY) else: st.error("❌ Chưa có API Key của Gemini. Vui lòng thêm vào .streamlit/secrets.toml hoặc biến môi trường.")

--- Nhập nội dung kịch bản ---

script = st.text_area("✍️ Nhập kịch bản về vũ trụ hoặc khoa học:", height=200)

if script: st.subheader("📘 Kết quả theo từng câu:") sentences = re.split(r'(?<=[.!?])\s+', script.strip())

for i, sentence in enumerate(sentences):
    st.markdown(f"### 🔹 Câu {i+1}: {sentence}")
    prompt = quote(sentence)
    col1, col2 = st.columns(2)

    # Ảnh từ Freepik
    with col1:
        st.markdown("**📷 Ảnh minh họa (Freepik):**")
        freepik_url = f"https://www.freepik.com/search?format=search&query={prompt}&type=photo"
        try:
            html = requests.get(freepik_url, headers={"User-Agent": "Mozilla/5.0"}).text
            soup = BeautifulSoup(html, "html.parser")
            thumbs = soup.select("figure img")[:5]
            if thumbs:
                for img in thumbs:
                    img_url = img.get("src") or img.get("data-src")
                    link = img.find_parent("a")
                    if img_url and link:
                        full_link = "https://www.freepik.com" + link.get("href")
                        st.image(img_url, width=200)
                        st.markdown(f"[🔗 Xem ảnh trên Freepik]({full_link})")
            else:
                raise ValueError("Không tìm thấy ảnh Freepik")
        except:
            st.warning("❌ Không tìm thấy ảnh từ Freepik.")

    # Video từ NASA, ESA hoặc ảnh AI
    with col2:
        st.markdown("**🎞 Video Khoa học (NASA & ESA):**")
        nasa_url = f"https://images.nasa.gov/search-results?q={prompt}&media=video"
        esa_url = f"https://www.esa.int/ESA_Multimedia/Search?SearchText={prompt}&SearchButton=GO"

        show_video_links = False
        try:
            nasa_html = requests.get(nasa_url, headers={"User-Agent": "Mozilla/5.0"}).text
            if "search-results" in nasa_html and "No results found" not in nasa_html:
                show_video_links = True
        except:
            pass

        if show_video_links:
            st.markdown(f"🔗 [Xem video liên quan trên NASA]({nasa_url})")
            st.markdown(f"🔗 [Xem video liên quan trên ESA]({esa_url})")
        else:
            st.info("❗ Không tìm thấy video phù hợp – tạo ảnh minh họa AI bằng Gemini:")
            if API_KEY:
                try:
                    model = genai.GenerativeModel("models/gemini-pro-vision")
                    response = model.generate_content(
                        f"Cinematic illustration of: {sentence}",
                        generation_config={"response_mime_type": "image/jpeg"}
                    )
                    img_bytes = response.parts[0].raw
                    img = Image.open(BytesIO(img_bytes))
                    st.image(img, caption="Ảnh AI minh họa từ Gemini", width=300)
                except Exception as e:
                    st.error(f"Lỗi khi tạo ảnh từ Gemini: {e}")
            else:
                st.error("Không có API key Gemini.")

