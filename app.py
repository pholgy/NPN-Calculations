import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="NPN Analyzer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'language' not in st.session_state:
    st.session_state.language = 'th'
if 'page' not in st.session_state:
    st.session_state.page = 'upload'

translations = {
    'th': {
        'upload': 'อัปโหลด', 'results': 'ผลลัพธ์', 'guide': 'คู่มือ', 'about': 'เกี่ยวกับ',
        'title': 'NPN ANALYZER', 'subtitle': 'ระบบวิเคราะห์ไนโตรเจนไม่ใช่โปรตีน',
        'upload_title': 'อัปโหลดภาพสารละลาย', 'analyze': 'วิเคราะห์', 'npn': 'ปริมาณ NPN',
        'quality': 'คุณภาพ', 'recommendation': 'คำแนะนำ', 'rgb': 'ค่าสี RGB',
        'excellent': 'ดีเยี่ยม', 'good': 'ดี', 'medium': 'ปานกลาง', 'low': 'ต่ำ', 'very_low': 'ต่ำมาก',
        'rec_excellent': 'คุณภาพดีเยี่ยม เหมาะสำหรับใช้เป็นวัตถุดิบอาหารสัตว์',
        'rec_medium': 'คุณภาพปานกลาง ควรตรวจสอบเพิ่มเติม',
        'rec_low': 'คุณภาพต่ำ ควรปรับปรุงกระบวนการผลิต',
        'rec_very_low': 'คุณภาพต่ำมาก ไม่แนะนำให้ใช้งาน',
        'no_result': 'ยังไม่มีผลการวิเคราะห์', 'upload_first': 'กรุณาอัปโหลดภาพและกดวิเคราะห์',
    },
    'en': {
        'upload': 'Upload', 'results': 'Results', 'guide': 'Guide', 'about': 'About',
        'title': 'NPN ANALYZER', 'subtitle': 'Non-Protein Nitrogen Analysis System',
        'upload_title': 'Upload Solution Image', 'analyze': 'Analyze', 'npn': 'NPN Content',
        'quality': 'Quality', 'recommendation': 'Recommendation', 'rgb': 'RGB Values',
        'excellent': 'Excellent', 'good': 'Good', 'medium': 'Medium', 'low': 'Low', 'very_low': 'Very Low',
        'rec_excellent': 'Excellent quality, suitable for animal feed',
        'rec_medium': 'Medium quality, further inspection recommended',
        'rec_low': 'Low quality, production improvement needed',
        'rec_very_low': 'Very low quality, not recommended',
        'no_result': 'No Results Yet', 'upload_first': 'Please upload an image and analyze',
    }
}

def t(key):
    return translations[st.session_state.language][key]

def extract_rgb_from_image(image):
    img_array = np.array(image)
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    return np.mean(img_array[:, :, 0]), np.mean(img_array[:, :, 1]), np.mean(img_array[:, :, 2])

def calculate_npn(green_value):
    return max(0, -0.0261 * green_value + 3.8385)

def assess_quality(npn_value):
    if npn_value <= 0.5:
        return t('excellent'), t('rec_excellent'), '#10b981', '🟢'
    elif npn_value <= 1.0:
        return t('good'), t('rec_excellent'), '#10b981', '🟢'
    elif npn_value <= 2.0:
        return t('medium'), t('rec_medium'), '#f59e0b', '🟡'
    elif npn_value <= 3.0:
        return t('low'), t('rec_low'), '#ef4444', '🔴'
    else:
        return t('very_low'), t('rec_very_low'), '#dc2626', '🔴'

# Modern CSS with proper spacing
st.markdown("""
<style>
    @import url('https://rsms.me/inter/inter.css');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Remove default padding */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
        padding: 0;
    }

    [data-testid="stSidebar"] > div {
        padding: 40px 24px;
    }

    /* Sidebar title */
    .sidebar-header {
        margin-bottom: 48px;
    }

    .sidebar-header h1 {
        font-size: 18px;
        font-weight: 700;
        color: #111827;
        margin: 0 0 4px 0;
        letter-spacing: -0.02em;
    }

    .sidebar-header p {
        font-size: 13px;
        color: #6b7280;
        margin: 0;
    }

    /* Menu buttons */
    .menu-item {
        display: block;
        width: 100%;
        padding: 12px 16px;
        margin: 4px 0;
        background: transparent;
        border: none;
        border-radius: 8px;
        text-align: left;
        font-size: 14px;
        font-weight: 500;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.15s ease;
    }

    .menu-item:hover {
        background: #f3f4f6;
        color: #111827;
    }

    .menu-item.active {
        background: #000000;
        color: #ffffff;
    }

    .stButton > button {
        width: 100%;
        padding: 12px 16px;
        background: transparent;
        border: none;
        border-radius: 8px;
        text-align: left;
        font-size: 14px;
        font-weight: 500;
        color: #6b7280;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background: #f3f4f6;
        color: #111827;
    }

    /* Language selector */
    [data-testid="stRadio"] {
        margin: 32px 0;
    }

    [data-testid="stRadio"] > div {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 4px;
    }

    /* Main content */
    .main {
        background: #fafafa;
    }

    /* Top bar */
    .top-bar {
        background: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        padding: 24px 48px;
        margin-bottom: 48px;
    }

    .top-bar h1 {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin: 0 0 4px 0;
        letter-spacing: -0.03em;
    }

    .top-bar p {
        font-size: 15px;
        color: #6b7280;
        margin: 0;
    }

    /* Content area */
    .content-wrapper {
        padding: 0 48px 48px 48px;
        max-width: 1400px;
        margin: 0 auto;
    }

    /* Card */
    .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }

    .card h2 {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 20px 0;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 48px 32px;
        text-align: center;
        background: #fafafa;
        transition: all 0.2s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #9ca3af;
        background: #f9fafb;
    }

    /* Results card */
    .result-card {
        background: linear-gradient(135deg, #000000 0%, #1f2937 100%);
        border-radius: 16px;
        padding: 48px 32px;
        text-align: center;
        margin: 24px 0;
    }

    .result-value {
        font-size: 72px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1;
        margin: 16px 0;
        letter-spacing: -0.04em;
    }

    .result-label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9ca3af;
        font-weight: 600;
    }

    .quality-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 24px;
        border-radius: 100px;
        font-weight: 600;
        font-size: 14px;
        margin: 20px 0;
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        backdrop-filter: blur(10px);
    }

    /* RGB Grid */
    .rgb-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin: 24px 0;
    }

    .rgb-item {
        background: #fafafa;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }

    .rgb-item-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9ca3af;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .rgb-item-value {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
    }

    /* Info box */
    .info-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-left: 3px solid #111827;
        border-radius: 8px;
        padding: 20px 24px;
        margin: 24px 0;
    }

    .info-box-title {
        font-size: 14px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 8px 0;
    }

    .info-box-text {
        font-size: 14px;
        color: #4b5563;
        line-height: 1.6;
        margin: 0;
    }

    /* Analyze button */
    .analyze-button button {
        background: #000000 !important;
        color: #ffffff !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 16px 32px !important;
        border: none !important;
        border-radius: 12px !important;
        transition: all 0.2s ease !important;
    }

    .analyze-button button:hover {
        background: #1f2937 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }

    /* Image preview */
    .image-preview {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, .stDeployButton {
        display: none;
    }

    /* Section spacing */
    h2 {
        font-size: 20px;
        font-weight: 600;
        color: #111827;
        margin: 40px 0 20px 0;
        letter-spacing: -0.02em;
    }

    h3 {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin: 24px 0 12px 0;
    }

    /* Sidebar sections */
    .sidebar-section {
        margin: 32px 0;
        padding: 20px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
    }

    .sidebar-section h3 {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6b7280;
        font-weight: 600;
        margin: 0 0 12px 0;
    }

    .sidebar-section code {
        display: block;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 12px;
        border-radius: 8px;
        font-size: 13px;
        color: #111827;
        font-family: 'SF Mono', Monaco, Consolas, monospace;
    }

    .sidebar-section p {
        font-size: 13px;
        color: #6b7280;
        line-height: 1.6;
        margin: 8px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <h1>🔬 {t('title')}</h1>
        <p>{t('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Language
    lang = st.radio("", ["🇹🇭 ไทย", "🇬🇧 English"],
                    index=0 if st.session_state.language == 'th' else 1,
                    label_visibility="collapsed")
    st.session_state.language = 'th' if '🇹🇭' in lang else 'en'

    # Menu
    if st.button(f"📸  {t('upload')}", key="btn_upload"):
        st.session_state.page = 'upload'
        st.rerun()

    if st.button(f"📊  {t('results')}", key="btn_results"):
        st.session_state.page = 'results'
        st.rerun()

    if st.button(f"📖  {t('guide')}", key="btn_guide"):
        st.session_state.page = 'guide'
        st.rerun()

    if st.button(f"ℹ️  {t('about')}", key="btn_about"):
        st.session_state.page = 'about'
        st.rerun()

    # Equation
    st.markdown("""
    <div class="sidebar-section">
        <h3>สมการ / Equation</h3>
        <code>y = -0.0261x + 3.8385</code>
        <p>
        <strong>y</strong> = NPN (%)<br>
        <strong>x</strong> = Green (G)<br>
        <strong>R²</strong> = 0.5902
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Reference
    st.markdown("""
    <div class="sidebar-section">
        <h3>อ้างอิง / Reference</h3>
        <p>
        Nopparatmaitree et al.<br>
        Khon Kaen Agriculture Journal<br>
        SUPPL. 1 (2023)
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main content
page = st.session_state.page

# Top bar
st.markdown(f"""
<div class="top-bar">
    <h1>{t(page).title() if page in ['upload', 'results', 'guide', 'about'] else t('upload').title()}</h1>
    <p>{t('upload_title') if page == 'upload' else ''}</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

if page == 'upload':
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.markdown('<div class="image-preview">', unsafe_allow_html=True)
            st.image(image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if uploaded_file:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**Filename:** {uploaded_file.name}")
            st.markdown(f"**Size:** {uploaded_file.size / 1024:.1f} KB")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('<div class="analyze-button">', unsafe_allow_html=True)
            if st.button(t('analyze'), use_container_width=True):
                r, g, b = extract_rgb_from_image(image)
                npn_value = calculate_npn(g)
                quality, rec, color, emoji = assess_quality(npn_value)

                st.session_state.update({
                    'analyzed': True, 'r': r, 'g': g, 'b': b,
                    'npn_value': npn_value, 'quality': quality,
                    'recommendation': rec, 'color': color, 'emoji': emoji, 'image': image
                })

                st.session_state.page = 'results'
                st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

elif page == 'results':
    if 'analyzed' in st.session_state and st.session_state.analyzed:
        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            st.markdown('<div class="card image-preview">', unsafe_allow_html=True)
            st.image(st.session_state.image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">{t('npn')}</div>
                <div class="result-value">{st.session_state.npn_value:.2f}%</div>
                <div class="quality-badge">
                    <span>{st.session_state.emoji}</span>
                    <span>{st.session_state.quality}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="info-box">
                <div class="info-box-title">{t('recommendation')}</div>
                <div class="info-box-text">{st.session_state.recommendation}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"## {t('rgb')}")
        st.markdown(f"""
        <div class="rgb-grid">
            <div class="rgb-item">
                <div class="rgb-item-label">Red (R)</div>
                <div class="rgb-item-value">{st.session_state.r:.0f}</div>
            </div>
            <div class="rgb-item">
                <div class="rgb-item-label">Green (G)</div>
                <div class="rgb-item-value">{st.session_state.g:.0f}</div>
            </div>
            <div class="rgb-item">
                <div class="rgb-item-label">Blue (B)</div>
                <div class="rgb-item-value">{st.session_state.b:.0f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"{t('no_result')}\n\n{t('upload_first')}")

elif page == 'guide':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### วิธีใช้งาน / User Guide

    **ขั้นตอนที่ 1: เตรียมตัวอย่าง**
    - เตรียมสารละลายกากถั่วเหลือง
    - ทำปฏิกิริยากับ Nessler reagent
    - รอให้เกิดสีตามมาตรฐาน

    **ขั้นตอนที่ 2: ถ่ายภาพ**
    - ใช้แสงสม่ำเสมอ (LED แนะนำ)
    - พื้นหลังสีขาว
    - ระยะห่าง 15-20 cm
    - หลีกเลี่ยงเงาและแสงสะท้อน

    **ขั้นตอนที่ 3: อัปโหลดและวิเคราะห์**
    - ไปที่หน้า "อัปโหลด"
    - เลือกหรือลากไฟล์ภาพ
    - กดปุ่ม "วิเคราะห์"
    - ดูผลลัพธ์ที่หน้า "ผลลัพธ์"
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == 'about':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### เกี่ยวกับระบบ / About System

    ระบบนี้พัฒนาจากงานวิจัย:

    **"การพัฒนาเทคนิคการตรวจวัดนันโปรตีนไนโตรเจนในกากถั่วเหลืองด้วยวิธีการวัดสีของถ่ายภาพและเครื่องสเปกโตโฟโตมิเตอร์"**

    **ผู้วิจัย:** มนัสนันท์ นพรัตน์ไมตรี และคณะ

    **หน่วยงาน:** คณะสัตวศาสตร์และเทคโนโลยีการเกษตร มหาวิทยาลัยศิลปากร

    **วารสาร:** Khon Kaen Agriculture Journal SUPPL. 1 (2023)

    **วิธีการ:** ใช้สมการถดถอยเชิงเส้นในการคำนวณปริมาณ NPN จากค่าสีเขียว (G) ของภาพถ่าย

    **ความแม่นยำ:**
    - R² = 0.5902
    - r = -0.76823 (P < 0.01)
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
