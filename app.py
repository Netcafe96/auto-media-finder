import streamlit as st import urllib.parse import requests from PIL import Image from io import BytesIO from bs4 import BeautifulSoup import re

st.set_page_config(page_title="Auto Media Finder", layout="wide") st.title("🎬 Auto Media Finder - No API Version") st.markdown("Tự động hiển thị link video và hình ảnh từ các nền tảng phổ biến mà không cần API.")

query = st.text_input("🔍 Nhập từ khóa tìm kiếm (ví dụ: 'Hố đen lớn nhất vũ trụ'):")

def get_youtube_video_data(q, max_results=5): try: q_enc = urllib.parse.quote_plus(q + " short") url = f"https://www.youtube.com/results?search_query={q_enc}" headers = {"User-Agent": "Mozilla/5.0"} r = requests.get(url, headers=headers) video_ids = list(set(re.findall(r"watch?v=(.{11})", r.text))) results = [] for vid in video_ids: video_url = f"https://www.youtube.com/watch?v={vid}" thumbnail_url = f"https://img.youtube.com/vi/{vid}/0.jpg" results.append((video_url, thumbnail_url)) if len(results) >= max_results: break return results except: return []

def get_google_image_previews(q, max_images=15): try: q_enc = urllib.parse.quote_plus(q) url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1&tsc=ImageHoverTitle" headers = {"User-Agent": "Mozilla/5.0"} r = requests.get(url, headers=headers, timeout=5) img_urls = list(set([ line.split('src="')[1].split('"')[0] for line in r.text.split('\n') if 'src="' in line and any(ext in line.lower() for ext in ['.jpg', '.jpeg', '.png']) and not any(x in line for x in ['data:', 'logo', 'icon']) ])) return img_urls[:max_images] if img_urls else None except: return None

if query: st.markdown("---") st.subheader("🎥 YouTube Videos (with thumbnails)") videos = get_youtube_video_data(query) if videos: for url, thumb in videos: st.image(thumb, width=320) st.markdown(f"🔗 Xem video") else: st.warning("Không tìm thấy video YouTube phù hợp.")

st.markdown("---")
st.subheader("🖼️ Image Sources")
q_enc = urllib.parse.quote_plus(query)
st.markdown(f"- 🖼️ [Freepik Images](https://www.freepik.com/search?format=search&query={q_enc})")
st.markdown(f"- 📹 [Freepik Videos](https://www.freepik.com/search/videos?query={q_enc})")

st.markdown("### 🖼️ Google Image Preview (Top 15)")
google_images = get_google_image_previews(query)
if google_images:
    for img_url in google_images:
        try:
            img_data = requests.get(img_url).content
            image = Image.open(BytesIO(img_data))
            if image.width >= 300:
                st.image(image, caption=img_url, use_column_width=True)
        except:
            continue
else:
    st.warning("Không tìm thấy ảnh phù hợp từ Google Images.")

