import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Space Media Finder", layout="wide")
st.title("🚀 Tìm Ảnh & Video Khoa Học Vũ Trụ từ Kịch Bản")

# --- Thiết lập Gemini API ---
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("❌ Chưa có API Key của Gemini. Vui lòng thêm vào .streamlit/secrets.toml hoặc biến môi trường.")

# --- Nhập nội dung kịch bản ---
script = st.text_area("✍️ Nhập kịch bản về vũ trụ hoặc khoa học:", height=250)

if script:
    st.subheader("📘 Phân tích từng câu:")
    sentences = re.split(r'(?<=[.!?])\s+', script.strip())

    for i, sentence in enumerate(sentences):
        st.markdown(f"### 🔹 Câu {i+1}: {sentence}")
        prompt = quote(sentence)
        col1, col2 = st.columns(2)

        # --- Ảnh từ Freepik (chỉ hiển thị link) ---
        with col1:
            st.markdown("**🖼 Ảnh minh họa (Freepik):**")
            freepik_url = f"https://www.freepik.com/search?format=search&query={prompt}&type=photo"
            st.markdown(f"[🔗 Tìm ảnh trên Freepik]({freepik_url})")

        # --- Video từ NASA/ESA hoặc tạo ảnh AI ---
        with col2:
            st.markdown("**🎞 Video hoặc Ảnh minh họa:**")
            nasa_url = f"https://images.nasa.gov/search-results?q={prompt}&media=video"
            esa_url = f"https://www.esa.int/ESA_Multimedia/Search?SearchText={prompt}&SearchButton=GO"

            # Thử kiểm tra xem NASA có kết quả không (chỉ kiểm tra thô)
            found_video = False
            try:
                html = requests.get(nasa_url, headers={"User-Agent": "Mozilla/5.0"}).text
                if "No results found" not in html:
                    found_video = True
            except:
                pass

            if found_video:
                st.markdown(f"🔗 [Xem video trên NASA]({nasa_url})")
                st.markdown(f"🔗 [Xem video trên ESA]({esa_url})")
            else:
                st.info("🎨 Không có video phù hợp → tạo ảnh minh họa AI với Gemini")
                try:
                    model = genai.GenerativeModel("models/gemini-pro-vision")
                    response = model.generate_content(
                        f"Cinematic illustration of: {sentence}",
                        generation_config={"response_mime_type": "image/jpeg"}
                    )
                    image_bytes = response.parts[0].raw
                    image = Image.open(BytesIO(image_bytes))
                    st.image(image, caption="Ảnh AI từ Gemini", use_column_width=True)
                except Exception as e:
                    st.error(f"❌ Lỗi tạo ảnh AI từ Gemini: {e}")
