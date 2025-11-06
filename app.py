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
if 'calibration_factor' not in st.session_state:
    st.session_state.calibration_factor = 1.0

translations = {
    'th': {
        'upload': 'อัปโหลด', 'results': 'ผลลัพธ์', 'guide': 'คู่มือ', 'about': 'เกี่ยวกับ',
        'npn_info': 'เกี่ยวกับ NPN', 'calibration': 'คาลิเบรตสี', 'privacy': 'ความเป็นส่วนตัว',
        'title': 'NPN ANALYZER', 'subtitle': 'ระบบวิเคราะห์ไนโตรเจนไม่ใช่โปรตีน',
        'upload_title': 'อัปโหลดภาพสารละลาย', 'analyze': 'วิเคราะห์', 'npn': 'ปริมาณ NPN',
        'quality': 'คุณภาพ', 'recommendation': 'คำแนะนำ', 'rgb': 'ค่าสี RGB',
        'excellent': 'ดีเยี่ยม', 'good': 'ดี', 'medium': 'ปานกลาง', 'low': 'ต่ำ', 'very_low': 'ต่ำมาก',
        'rec_excellent': 'คุณภาพดีเยี่ยม เหมาะสำหรับใช้เป็นวัตถุดิบอาหารสัตว์',
        'rec_medium': 'คุณภาพปานกลาง ควรตรวจสอบเพิ่มเติม',
        'rec_low': 'คุณภาพต่ำ ควรปรับปรุงกระบวนการผลิต',
        'rec_very_low': 'คุณภาพต่ำมาก ไม่แนะนำให้ใช้งาน',
        'no_result': 'ยังไม่มีผลการวิเคราะห์', 'upload_first': 'กรุณาอัปโหลดภาพและกดวิเคราะห์',
        'upload_image': '📤 อัปโหลดภาพ', 'take_photo': '📷 ถ่ายภาพ', 'use_sample': '🧪 ใช้ภาพตัวอย่าง',
        'calibrate_color': 'คาลิเบรตสี', 'upload_reference': 'อัปโหลดภาพอ้างอิง',
        'ref_npn_value': 'ค่า NPN ที่ทราบ (%)', 'apply_calibration': 'ใช้การคาลิเบรต',
        'calibration_applied': 'ใช้การคาลิเบรตแล้ว'
    },
    'en': {
        'upload': 'Upload', 'results': 'Results', 'guide': 'Guide', 'about': 'About',
        'npn_info': 'About NPN', 'calibration': 'Color Calibration', 'privacy': 'Privacy',
        'title': 'NPN ANALYZER', 'subtitle': 'Non-Protein Nitrogen Analysis System',
        'upload_title': 'Upload Solution Image', 'analyze': 'Analyze', 'npn': 'NPN Content',
        'quality': 'Quality', 'recommendation': 'Recommendation', 'rgb': 'RGB Values',
        'excellent': 'Excellent', 'good': 'Good', 'medium': 'Medium', 'low': 'Low', 'very_low': 'Very Low',
        'rec_excellent': 'Excellent quality, suitable for animal feed',
        'rec_medium': 'Medium quality, further inspection recommended',
        'rec_low': 'Low quality, production improvement needed',
        'rec_very_low': 'Very low quality, not recommended',
        'no_result': 'No Results Yet', 'upload_first': 'Please upload an image and analyze',
        'upload_image': '📤 Upload Image', 'take_photo': '📷 Take Photo', 'use_sample': '🧪 Use Sample',
        'calibrate_color': 'Calibrate Color', 'upload_reference': 'Upload Reference Image',
        'ref_npn_value': 'Known NPN Value (%)', 'apply_calibration': 'Apply Calibration',
        'calibration_applied': 'Calibration Applied'
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

def calculate_npn(green_value, calibration_factor=1.0):
    adjusted_green = green_value * calibration_factor
    return max(0, -0.0261 * adjusted_green + 3.8385)

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

    /* Action buttons */
    .action-button {
        background: #ffffff;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 32px 24px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 16px;
    }

    .action-button:hover {
        border-color: #000000;
        background: #fafafa;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .action-button-icon {
        font-size: 48px;
        margin-bottom: 16px;
    }

    .action-button-title {
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin: 0;
    }

    .action-button-desc {
        font-size: 14px;
        color: #6b7280;
        margin: 8px 0 0 0;
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

    if st.button(f"🎨  {t('calibration')}", key="btn_calibration"):
        st.session_state.page = 'calibration'
        st.rerun()

    if st.button(f"🧬  {t('npn_info')}", key="btn_npn_info"):
        st.session_state.page = 'npn_info'
        st.rerun()

    if st.button(f"📖  {t('guide')}", key="btn_guide"):
        st.session_state.page = 'guide'
        st.rerun()

    if st.button(f"🔒  {t('privacy')}", key="btn_privacy"):
        st.session_state.page = 'privacy'
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
    # Action buttons
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            t('upload_image'), type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", key="main_uploader")
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.markdown('<div class="image-preview">', unsafe_allow_html=True)
            st.image(image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="analyze-button">', unsafe_allow_html=True)
            if st.button(t('analyze'), use_container_width=True, key="analyze_btn"):
                r, g, b = extract_rgb_from_image(image)
                npn_value = calculate_npn(g, st.session_state.calibration_factor)
                quality, rec, color, emoji = assess_quality(npn_value)

                st.session_state.update({
                    'analyzed': True, 'r': r, 'g': g, 'b': b,
                    'npn_value': npn_value, 'quality': quality,
                    'recommendation': rec, 'color': color, 'emoji': emoji, 'image': image
                })

                st.session_state.page = 'results'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card" style="height: 100%">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 64px; margin-bottom: 20px;">📷</div>
            <h3 style="margin: 0 0 12px 0;">""" + t('take_photo') + """</h3>
            <p style="color: #6b7280; margin: 0;">ถ่ายภาพสารละลายโดยตรงจากกล้อง</p>
        </div>
        """, unsafe_allow_html=True)
        camera_file = st.camera_input("", label_visibility="collapsed", key="camera")
        if camera_file:
            image = Image.open(camera_file)
            st.markdown('<div class="analyze-button">', unsafe_allow_html=True)
            if st.button(t('analyze'), use_container_width=True, key="analyze_camera"):
                r, g, b = extract_rgb_from_image(image)
                npn_value = calculate_npn(g, st.session_state.calibration_factor)
                quality, rec, color, emoji = assess_quality(npn_value)

                st.session_state.update({
                    'analyzed': True, 'r': r, 'g': g, 'b': b,
                    'npn_value': npn_value, 'quality': quality,
                    'recommendation': rec, 'color': color, 'emoji': emoji, 'image': image
                })

                st.session_state.page = 'results'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card" style="height: 100%">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 64px; margin-bottom: 20px;">🧪</div>
            <h3 style="margin: 0 0 12px 0;">""" + t('use_sample') + """</h3>
            <p style="color: #6b7280; margin: 0;">ทดลองใช้งานด้วยภาพตัวอย่าง</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ใช้ภาพตัวอย่าง", use_container_width=True, key="use_sample"):
            st.info("ฟีเจอร์นี้จะเพิ่มในเวอร์ชันถัดไป")
        st.markdown('</div>', unsafe_allow_html=True)

    # Calibration status
    if st.session_state.calibration_factor != 1.0:
        st.success(f"✓ {t('calibration_applied')} (Factor: {st.session_state.calibration_factor:.3f})")

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

elif page == 'calibration':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {t('calibrate_color')}")
    st.markdown("""
    การคาลิเบรตสีช่วยให้ผลการวิเคราะห์แม่นยำยิ่งขึ้นโดยการปรับค่าสีให้เหมาะสมกับสภาพแสงและกล้องของคุณ

    **วิธีการ:** อัปโหลดภาพตัวอย่างที่ทราบค่า NPN แล้ว ระบบจะคำนวณค่าปรับแก้อัตโนมัติ
    """)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"#### {t('upload_reference')}")
        ref_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key="calibration_uploader")

        if ref_file:
            ref_image = Image.open(ref_file)
            st.image(ref_image, use_container_width=True)

    with col2:
        if ref_file:
            st.markdown(f"#### {t('ref_npn_value')}")
            known_npn = st.number_input("", min_value=0.0, max_value=10.0, value=1.0, step=0.1, key="known_npn")

            if st.button(t('apply_calibration'), use_container_width=True):
                r, g, b = extract_rgb_from_image(ref_image)
                # Calculate what the green value should be for the known NPN
                # y = -0.0261x + 3.8385
                # x = (3.8385 - y) / 0.0261
                expected_green = (3.8385 - known_npn) / 0.0261
                st.session_state.calibration_factor = expected_green / g
                st.success(f"✓ คาลิเบรตสำเร็จ! Factor: {st.session_state.calibration_factor:.3f}")
                st.info(f"ค่า Green ที่วัดได้: {g:.1f} → ค่า Green ที่คาดหวัง: {expected_green:.1f}")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.calibration_factor != 1.0:
        if st.button("รีเซ็ตการคาลิเบรต"):
            st.session_state.calibration_factor = 1.0
            st.rerun()

elif page == 'npn_info':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🧬 NPN (Non-Protein Nitrogen) คืออะไร?

    **NPN หรือ ไนโตรเจนไม่ใช่โปรตีน** คือสารประกอบไนโตรเจนที่ไม่ได้อยู่ในรูปโปรตีน เช่น ยูเรีย แอมโมเนีย กรดอะมิโนอิสระ และนิวคลีโอไทด์

    ---

    ### ทำไมต้องตรวจ NPN?

    **1. ประเมินคุณภาพวัตถุดิบ**
    - กากถั่วเหลืองคุณภาพดีควรมี NPN ต่ำ (< 1%)
    - NPN สูงอาจบ่งชี้ถึงการเสื่อมสภาพหรือการปลอมปน

    **2. ป้องกันการทุจริต**
    - ผู้ไม่ประสงค์ดีอาจเติมยูเรียเพื่อเพิ่มปริมาณโปรตีนปลอม
    - การวัด NPN ช่วยตรวจจับการปลอมปนนี้ได้

    **3. ความปลอดภัยของสัตว์**
    - NPN สูงเกินไปอาจเป็นอันตรายต่อสัตว์
    - โดยเฉพาะในสัตว์เคี้ยวเอื้อง NPN ควรอยู่ในระดับที่เหมาะสม

    ---

    ### ระดับ NPN ที่ดี

    | ระดับ NPN | คุณภาพ | คำอธิบาย |
    |-----------|--------|----------|
    | ≤ 0.5% | ดีเยี่ยม | คุณภาพสูงสุด เหมาะสำหรับอาหารสัตว์คุณภาพ |
    | 0.5-1.0% | ดี | คุณภาพดี ใช้งานได้ตามมาตรฐาน |
    | 1.0-2.0% | ปานกลาง | ควรตรวจสอบเพิ่มเติม อาจมีการเสื่อมสภาพเล็กน้อย |
    | 2.0-3.0% | ต่ำ | คุณภาพต่ำ ควรปรับปรุงกระบวนการผลิต |
    | > 3.0% | ต่ำมาก | ไม่แนะนำให้ใช้ อาจมีการปลอมปนหรือเสื่อมสภาพ |

    ---

    ### วิธีการตรวจวัด

    **วิธีดั้งเดิม:** ใช้เครื่อง Spectrophotometer ในห้องแล็บ
    - ใช้เวลานาน
    - ต้องการอุปกรณ์ราคาแพง
    - ต้องมีผู้เชี่ยวชาญ

    **วิธีใหม่ (ระบบนี้):** วิเคราะห์จากภาพถ่าย
    - รวดเร็ว ได้ผลในไม่กี่วินาที
    - ไม่ต้องใช้อุปกรณ์แพง
    - ใช้งานง่าย เพียงมีสมาร์ทโฟน

    ---

    ### หลักการทำงาน

    1. **ปฏิกิริยาสี:** NPN ทำปฏิกิริยากับ Nessler reagent เกิดสีเหลือง-ส้ม
    2. **วิเคราะห์สี:** ค่าสีเขียว (G) ในระบบ RGB มีความสัมพันธ์กับปริมาณ NPN
    3. **คำนวณ:** ใช้สมการถดถอย `NPN = -0.0261 × G + 3.8385`

    ยิ่ง NPN สูง → สีเข้มขึ้น → ค่า G น้อยลง → NPN% สูงขึ้น
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == 'privacy':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🔒 นโยบายความเป็นส่วนตัวและการรักษาข้อมูล

    ---

    ### การเก็บรักษาข้อมูล

    **ระบบนี้ให้ความสำคัญกับความเป็นส่วนตัวของคุณ:**

    ✓ **ไม่เก็บภาพถ่าย** - ทุกภาพที่อัปโหลดจะถูกประมวลผลใน Session ปัจจุบันเท่านั้น
    ✓ **ไม่บันทึกผลลัพธ์** - ข้อมูลทั้งหมดจะหายไปเมื่อปิดหน้าเว็บ
    ✓ **ไม่มีฐานข้อมูล** - ระบบไม่มีการเชื่อมต่อกับฐานข้อมูลใดๆ
    ✓ **ไม่แชร์ข้อมูล** - ข้อมูลของคุณจะไม่ถูกส่งไปยังบุคคลที่สาม

    ---

    ### การประมวลผลข้อมูล

    **ข้อมูลที่ระบบใช้:**
    - ภาพถ่ายสารละลายที่คุณอัปโหลด
    - ค่าสี RGB ที่คำนวณจากภาพ
    - ผลการวิเคราะห์ NPN

    **ระยะเวลาเก็บข้อมูล:**
    - ข้อมูลจะถูกเก็บใน Session Storage ของเบราว์เซอร์เท่านั้น
    - เมื่อปิดหรือรีเฟรชหน้าเว็บ ข้อมูลทั้งหมดจะถูกลบทันที
    - ระบบไม่มีการบันทึกข้อมูลลงเซิร์ฟเวอร์

    ---

    ### เทคโนโลยีที่ใช้

    **Streamlit Community Cloud:**
    - แอปพลิเคชันถูกโฮสต์บน Streamlit Community Cloud
    - เป็น Platform ที่ปลอดภัยและเชื่อถือได้
    - มีการเข้ารหัส HTTPS สำหรับการสื่อสารทั้งหมด

    **การประมวลผลข้อมูล:**
    - การวิเคราะห์ภาพทำบนเซิร์ฟเวอร์ชั่วคราว
    - ไม่มีการบันทึกภาพหรือผลลัพธ์หลังจากประมวลผลเสร็จ
    - ใช้ Python libraries: Streamlit, PIL, NumPy

    ---

    ### สิทธิของผู้ใช้งาน

    คุณมีสิทธิ์:
    - ใช้งานระบบโดยไม่ต้องลงทะเบียน
    - ไม่ต้องให้ข้อมูลส่วนตัว
    - หยุดการใช้งานได้ทุกเมื่อ

    ---

    ### ข้อจำกัดความรับผิดชอบ

    ⚠️ **คำเตือน:**
    - ระบบนี้เป็นเครื่องมือช่วยประเมินเบื้องต้น
    - ผลการวิเคราะห์ควรใช้ประกอบการตัดสินใจเท่านั้น
    - สำหรับการตรวจสอบอย่างเป็นทางการ ควรใช้ห้องปฏิบัติการที่ได้มาตรฐาน
    - ผู้พัฒนาไม่รับผิดชอบต่อความเสียหายที่เกิดจากการใช้งาน

    ---

    ### การติดต่อ

    หากมีคำถามเกี่ยวกับนโยบายความเป็นส่วนตัว กรุณาติดต่อผู้พัฒนาระบบ

    **อัปเดตล่าสุด:** 6 มกราคม 2568
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
