import streamlit as st import urllib.parse import requests from PIL import Image from io import BytesIO from bs4 import BeautifulSoup

st.set_page_config(page_title="Auto Media Finder", layout="wide") st.title("🎬 Auto Media Finder - No API Version") st.markdown("Tự động hiển thị link video và hình ảnh từ các nền tảng phổ biến mà không cần API.")

Input script

query = st.text_input("🔍 Nhập từ khóa tìm kiếm (ví dụ: 'Hố đen lớn nhất vũ trụ'):")

Helper functions

def get_youtube_links(q, max_results=5): try: q_enc = urllib.parse.quote_plus(q + " short") url = f"https://www.youtube.com/results?search_query={q_enc}" headers = {"User-Agent": "Mozilla/5.0"} r = requests.get(url, headers=headers) results = [] seen = set() for line in r.text.split('\n'): if 'watch?v=' in line: try: vid = line.split('watch?v=')[1].split('\')[0].split('"')[0] link = f"https://www.youtube.com/watch?v={vid}" if link not in seen: results.append(link) seen.add(link) if len(results) >= max_results: break except: continue return results except: return []

def get_tiktok_links(q, max_results=5): try: q_enc = urllib.parse.quote_plus(q) url = f"https://www.tiktok.com/search?q={q_enc}" headers = {"User-Agent": "Mozilla/5.0"} r = requests.get(url, headers=headers) soup = BeautifulSoup(r.text, 'html.parser') links = [] for a in soup.find_all('a', href=True): href = a['href'] if '/video/' in href and href.startswith("https://www.tiktok.com/"): if href not in links: links.append(href) if len(links) >= max_results: break return links except: return []

def get_google_image_previews(q, max_images=5): try: q_enc = urllib.parse.quote_plus(q) url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1&tsc=ImageBasicHover" headers = {"User-Agent": "Mozilla/5.0"} r = requests.get(url, headers=headers, timeout=5) img_urls = list(set([ line.split('src="')[1].split('"')[0] for line in r.text.split('\n') if 'mimg' in line and 'src="' in line ])) return img_urls[:max_images] if img_urls else None except: return None

if query: st.markdown("---") st.subheader("🎥 Video Links")

with st.spinner("🔎 Đang tìm video YouTube..."):
    yt_links = get_youtube_links(query)
    if yt_links:
        for i, link in enumerate(yt_links, 1):
            st.markdown(f"{i}. [YouTube Video]({link})")
    else:
        st.warning("Không tìm thấy video YouTube phù hợp.")

with st.spinner("🔎 Đang tìm video TikTok..."):
    tk_links = get_tiktok_links(query)
    if tk_links:
        for i, link in enumerate(tk_links, 1):
            st.markdown(f"{i}. [TikTok Video]({link})")
    else:
        st.warning("Không tìm thấy video TikTok phù hợp.")

st.markdown("---")
st.subheader("🖼️ Image Sources")
q_enc = urllib.parse.quote_plus(query)
st.markdown(f"- 🖼️ [Freepik Images](https://www.freepik.com/search?format=search&query={q_enc})")
st.markdown(f"- 📹 [Freepik Videos](https://www.freepik.com/videos/search/{q_enc})")

st.markdown("### 🖼️ Google Image Preview")
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

