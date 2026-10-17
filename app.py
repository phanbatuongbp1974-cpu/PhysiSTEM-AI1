import json
import os
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PhysiSTEM AI • Học Vật lí KNTT 6–9",
    page_icon="⚛️",
    layout="wide",
)

# Ẩn giao diện mặc định của Streamlit, bỏ thanh cuộn ngoài,
# và cho khung trang cao đúng bằng cửa sổ trình duyệt.
st.markdown("""
<style>
    #MainMenu, footer, header,
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
    }
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main {
        overflow: hidden !important;
        height: 100vh !important;
    }
    .block-container, .stMainBlockContainer {
        padding: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }
    [data-testid="stElementContainer"]:has(style) { display: none !important; }
    iframe { height: 100vh !important; display: block; border: 0; }
</style>
""", unsafe_allow_html=True)


def get_keys():
    """Đọc key từ .streamlit/secrets.toml (hoặc biến môi trường):
    GEMINI_API_KEY_1, GEMINI_API_KEY_2, ... / GEMINI_API_KEYS / GEMINI_API_KEY"""
    found = {}
    try:
        for name in st.secrets:
            found[str(name)] = st.secrets[name]
    except Exception:
        pass
    for name, val in os.environ.items():
        if name.startswith("GEMINI_API_KEY") and name not in found:
            found[name] = val

    keys = []

    def add(v):
        if isinstance(v, str):
            v = re.split(r"[,\s]+", v)
        try:
            for k in list(v):
                if isinstance(k, str) and k.strip():
                    keys.append(k.strip())
        except TypeError:
            pass

    numbered = []
    for name, val in found.items():
        m = re.fullmatch(r"GEMINI_API_KEY_?(\d+)", name)
        if m:
            numbered.append((int(m.group(1)), val))
    for _, val in sorted(numbered, key=lambda x: x[0]):
        add(val)
    for name in ("GEMINI_API_KEYS", "GEMINI_API_KEY"):
        if name in found:
            add(found[name])
    return list(dict.fromkeys(keys))


html_path = Path(__file__).parent / "index.html"

if html_path.exists():
    html = html_path.read_text(encoding="utf-8")
    # Đưa key từ secrets.toml vào trang để chatbot dùng luôn, không cần nhập tay
    keys_js = ",".join(json.dumps(k) for k in get_keys())
    html = html.replace("[/*KEYS*/]", "[" + keys_js + "]", 1)
    components.html(html, height=1000, scrolling=True)
else:
    st.error(f"⚠️ Không tìm thấy tệp `index.html` tại: {html_path}")