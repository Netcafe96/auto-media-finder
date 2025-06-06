import streamlit as st
import urllib.parse

st.set_page_config(page_title="Auto Media Finder", layout="wide")
st.title("🎬 Auto Media Finder for Science Scripts")
st.markdown("Tự động tạo liên kết tìm kiếm video và hình ảnh từ kịch bản khoa học.")

# Input script
script = st.text_area("📜 Nhập kịch bản khoa học:", height=300)

# Process script into segments
def split_script(text):
    import re
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return [s for s in sentences if len(s) > 10]

# Generate search links
def generate_links(keyword):
    q = urllib.parse.quote_plus(keyword)
    return {
        "YouTube": f"https://www.youtube.com/results?search_query={q}",
        "TikTok": f"https://www.tiktok.com/search?q={q}",
        "Freepik Video": f"https://www.freepik.com/videos/search/{q}",
        "Archive.org": f"https://archive.org/search.php?query={q}",
        "Google Images": f"https://www.google.com/search?q={q}&tbm=isch",
        "Wikimedia": f"https://commons.wikimedia.org/w/index.php?search={q}",
        "Freepik Image": f"https://www.freepik.com/search?format=search&query={q}"
    }

if script:
    st.markdown("---")
    st.subheader("🔎 Kết quả tìm kiếm:")
    segments = split_script(script)

    for i, segment in enumerate(segments, 1):
        st.markdown(f"### 📌 Đoạn {i}: {segment}")
        links = generate_links(segment)

        with st.expander("🎥 VIDEO ƯU TIÊN"):
            st.markdown(f"- [▶️ YouTube]({links['YouTube']})")
            st.markdown(f"- [🎵 TikTok]({links['TikTok']})")
            st.markdown(f"- [📹 Freepik Video]({links['Freepik Video']})")
            st.markdown(f"- [📼 Archive.org]({links['Archive.org']})")

        with st.expander("🖼️ HÌNH ẢNH"):
            st.markdown(f"- [🖼️ Google Images]({links['Google Images']})")
            st.markdown(f"- [🌐 Wikimedia Commons]({links['Wikimedia']})")
            st.markdown(f"- [🎨 Freepik Image]({links['Freepik Image']})")

        st.markdown("---")
