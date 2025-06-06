import streamlit as st
import urllib.parse
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

st.set_page_config(page_title="Auto Media Finder", layout="wide")
st.title("🎬 Auto Media Finder - No API Version")
st.markdown("Tự động hiển thị link video và hình ảnh từ các nền tảng phổ biến mà không cần API.")

query = st.text_input("🔍 Nhập từ khóa tìm kiếm (ví dụ: 'Hố đen lớn nhất vũ trụ'):")

def get_youtube_video_data(q, max_results=5):
    try:
        q_enc = urllib.parse.quote_plus(q + " short")
        url = f"https://www.youtube.com/results?search_query={q_enc}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        results = []
        seen = set()
        for line in r.text.split('\n'):
            if 'watch?v=' in line:
                try:
                    vid = line.split('watch?v=')[1].split('\\')[0].split('"')[0]
                    if vid not in seen and len(vid) == 11:
                        video_url = f"https://www.youtube.com/watch?v={vid}"
                        thumbnail_url = f"https://img.youtube.com/vi/{vid}/0.jpg"
                        results.append((video_url, thumbnail_url))
                        seen.add(vid)
                    if len(results) >= max_results:
                        break
                except:
                    continue
        return results
    except:
        return []

def get_google_image_previews(q, max_images=15):
    try:
        q_enc = urllib.parse.quote_plus(q)
        url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1&tsc=ImageBasicHover"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        img_urls = list(set([
            line.split('src="')[1].split('"')[0]
            for line in r.text.split('\n')
            if 'mimg' in line and 'src="' in line and ('.jpg' in line or '.png' in line)
        ]))
        return img_urls[:max_images] if img_urls else None
    except:
        return None

if query:
    st.markdown("---")
    st.subheader("🎥 YouTube Videos (with thumbnails)")
    videos = get_youtube_video_data(query)
    if videos:
        for url, thumb in videos:
            st.image(thumb, width=320)
            st.markdown(f"[🔗 Xem video]({url})")
    else:
        st.warning("Không tìm thấy video YouTube phù hợp.")

    st.markdown("---")
    st.subheader("🖼️ Image Sources")
    q_enc = urllib.parse.quote_plus(query)
    st.markdown(f"- 🖼️ [Freepik Images](https://www.freepik.com/search?format=search&query={q_enc})")
    st.markdown(f"- 📹 [Freepik Videos](https://www.freepik.com/videos/search/{q_enc})")

    st.markdown("### 🖼️ Google Image Preview (Top 15)")
    google_images = get_google_image_previews(query)
    if google_images:
        for img_url in google_images:
            try:
                img_data = requests.get(img_url).content
                image = Image.open(BytesIO(img_data))
                st.image(image, caption=img_url, use_column_width=True)
            except:
                continue
    else:
        st.warning("Không tìm thấy ảnh phù hợp từ Google Images.")
