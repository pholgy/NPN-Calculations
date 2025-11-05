import streamlit as st
from PIL import Image
import numpy as np

# Page configuration
st.set_page_config(
    page_title="NPN Analyzer | วิเคราะห์ NPN",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Language selection
if 'language' not in st.session_state:
    st.session_state.language = 'th'

# Translation dictionary
translations = {
    'th': {
        'title': 'ระบบวิเคราะห์ NPN',
        'subtitle': 'วิเคราะห์ปริมาณไนโตรเจนไม่ใช่โปรตีนในกากถั่วเหลือง',
        'upload_title': 'อัปโหลดภาพสารละลาย',
        'upload_help': 'ถ่ายหรืออัปโหลดภาพสารละลายหลังทำปฏิกิริยากับ Nessler reagent',
        'analyze_btn': '🔍 วิเคราะห์ทันที',
        'results_title': 'ผลการวิเคราะห์',
        'npn_value': 'ปริมาณ NPN',
        'quality_level': 'คุณภาพ',
        'recommendation': 'คำแนะนำ',
        'rgb_values': 'ค่าสี RGB',
        'method': 'รายละเอียดการคำนวณ',
        'how_it_works': 'วิธีใช้งาน',
        'step1': '📸 ถ่ายหรืออัปโหลดภาพ',
        'step1_detail': 'ถ่ายภาพสารละลายหลังทำปฏิกิริยากับ Nessler reagent',
        'step2': '🔬 วิเคราะห์อัตโนมัติ',
        'step2_detail': 'ระบบดึงค่าสี RGB และคำนวณปริมาณ NPN',
        'step3': '📊 รับผลลัพธ์',
        'step3_detail': 'ดูค่า NPN พร้อมระดับคุณภาพและคำแนะนำ',
        'about_system': 'เกี่ยวกับระบบ',
        'reference': 'อ้างอิง',
        'ref_text': 'Nopparatmaitree et al. (2023) - Khon Kaen Agriculture Journal',
        'equation': 'สมการ',
        'quality_good': 'ดีเยี่ยม',
        'quality_medium': 'ปานกลาง',
        'quality_low': 'ต่ำ',
        'quality_very_low': 'ต่ำมาก',
        'rec_good': 'คุณภาพดี เหมาะสำหรับใช้เป็นวัตถุดิบอาหารสัตว์',
        'rec_medium': 'คุณภาพปานกลาง แนะนำให้ตรวจสอบเพิ่มเติม',
        'rec_low': 'คุณภาพต่ำ ควรปรับปรุงกระบวนการผลิต',
        'rec_very_low': 'คุณภาพต่ำมาก ไม่แนะนำให้ใช้ ควรตรวจสอบการปลอมปน',
        'note': 'หมายเหตุ',
        'note_text': 'ควรถ่ายภาพภายใต้แสงสม่ำเสมอและใช้พื้นหลังสีขาวเพื่อความแม่นยำ',
    },
    'en': {
        'title': 'NPN Analysis System',
        'subtitle': 'Analyze Non-Protein Nitrogen in Soybean Meal',
        'upload_title': 'Upload Solution Image',
        'upload_help': 'Take or upload photo of solution after Nessler reagent reaction',
        'analyze_btn': '🔍 Analyze Now',
        'results_title': 'Analysis Results',
        'npn_value': 'NPN Content',
        'quality_level': 'Quality',
        'recommendation': 'Recommendation',
        'rgb_values': 'RGB Values',
        'method': 'Calculation Details',
        'how_it_works': 'How It Works',
        'step1': '📸 Capture or Upload',
        'step1_detail': 'Take photo of solution after Nessler reagent reaction',
        'step2': '🔬 Auto Analysis',
        'step2_detail': 'System extracts RGB values and calculates NPN',
        'step3': '📊 Get Results',
        'step3_detail': 'View NPN value with quality level and recommendations',
        'about_system': 'About System',
        'reference': 'Reference',
        'ref_text': 'Nopparatmaitree et al. (2023) - Khon Kaen Agriculture Journal',
        'equation': 'Equation',
        'quality_good': 'Excellent',
        'quality_medium': 'Medium',
        'quality_low': 'Low',
        'quality_very_low': 'Very Low',
        'rec_good': 'Good quality, suitable for animal feed',
        'rec_medium': 'Medium quality, further inspection recommended',
        'rec_low': 'Low quality, production process improvement needed',
        'rec_very_low': 'Very low quality, not recommended, check for adulteration',
        'note': 'Note',
        'note_text': 'Take photos under consistent lighting with white background for accuracy',
    }
}

def get_text(key):
    return translations[st.session_state.language][key]

def extract_rgb_from_image(image):
    """Extract average RGB values from the uploaded image"""
    img_array = np.array(image)

    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    avg_r = np.mean(img_array[:, :, 0])
    avg_g = np.mean(img_array[:, :, 1])
    avg_b = np.mean(img_array[:, :, 2])

    return avg_r, avg_g, avg_b

def calculate_npn(green_value):
    """
    Calculate NPN using regression equation from research
    y = -0.0261x + 3.8385
    where y = NPN (%), x = Green (G) value
    R² = 0.5902, r = -0.76823
    """
    npn_percentage = -0.0261 * green_value + 3.8385
    return max(0, npn_percentage)

def assess_quality(npn_value):
    """Assess quality based on NPN content"""
    if npn_value <= 0.5:
        quality = get_text('quality_good')
        recommendation = get_text('rec_good')
        color = '#10b981'
        emoji = '✅'
    elif npn_value <= 1.0:
        quality = get_text('quality_medium')
        recommendation = get_text('rec_medium')
        color = '#f59e0b'
        emoji = '⚠️'
    elif npn_value <= 2.0:
        quality = get_text('quality_low')
        recommendation = get_text('rec_low')
        color = '#ef4444'
        emoji = '⚠️'
    else:
        quality = get_text('quality_very_low')
        recommendation = get_text('rec_very_low')
        color = '#dc2626'
        emoji = '❌'

    return quality, recommendation, color, emoji

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
    }

    /* Card style */
    .card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
    }

    /* Header */
    .header {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }

    .header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }

    /* Result card */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }

    .npn-value {
        font-size: 4rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .quality-badge {
        display: inline-block;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Info boxes */
    .info-box {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }

    /* RGB display */
    .rgb-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        gap: 1rem;
    }

    .rgb-box {
        flex: 1;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        background: #f1f5f9;
    }

    .rgb-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
    }

    .rgb-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 0.5rem;
    }

    /* Steps */
    .step-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        gap: 1rem;
    }

    .step {
        flex: 1;
        text-align: center;
        padding: 1.5rem;
        background: #f8fafc;
        border-radius: 12px;
    }

    .step-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .step-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0.5rem 0;
    }

    .step-detail {
        font-size: 0.9rem;
        color: #64748b;
    }

    /* Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        padding: 1rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Language toggle in sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    lang = st.radio(
        "Language / ภาษา",
        ["🇹🇭 ไทย", "🇬🇧 English"],
        index=0 if st.session_state.language == 'th' else 1
    )
    st.session_state.language = 'th' if '🇹🇭' in lang else 'en'

    st.markdown("---")
    st.markdown(f"### {get_text('about_system')}")
    st.markdown(f"""
    **{get_text('equation')}:**
    `y = -0.0261x + 3.8385`

    - y = NPN (%)
    - x = Green (G) value
    - R² = 0.5902

    **{get_text('reference')}:**
    {get_text('ref_text')}
    """)

# Header
st.markdown(f"""
<div class="header">
    <h1>🔬 {get_text('title')}</h1>
    <p>{get_text('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# Main container
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # How it works
    st.markdown(f"### {get_text('how_it_works')}")

    st.markdown(f"""
    <div class="step-container">
        <div class="step">
            <div class="step-icon">📸</div>
            <div class="step-title">{get_text('step1')}</div>
            <div class="step-detail">{get_text('step1_detail')}</div>
        </div>
        <div class="step">
            <div class="step-icon">🔬</div>
            <div class="step-title">{get_text('step2')}</div>
            <div class="step-detail">{get_text('step2_detail')}</div>
        </div>
        <div class="step">
            <div class="step-icon">📊</div>
            <div class="step-title">{get_text('step3')}</div>
            <div class="step-detail">{get_text('step3_detail')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload section
    st.markdown(f"### {get_text('upload_title')}")
    uploaded_file = st.file_uploader(
        get_text('upload_help'),
        type=['png', 'jpg', 'jpeg'],
        label_visibility="collapsed"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="Uploaded Image")

        if st.button(get_text('analyze_btn'), use_container_width=True):
            st.session_state.analyzed = True
            st.session_state.image = image

    st.markdown('</div>', unsafe_allow_html=True)

    # Note
    st.info(f"**{get_text('note')}:** {get_text('note_text')}")

with col2:
    if 'analyzed' in st.session_state and st.session_state.analyzed:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        # Extract RGB and calculate
        r, g, b = extract_rgb_from_image(st.session_state.image)
        npn_value = calculate_npn(g)
        quality, recommendation, color, emoji = assess_quality(npn_value)

        # Results
        st.markdown(f"### {get_text('results_title')}")

        st.markdown(f"""
        <div class="result-card">
            <div style="font-size: 1.2rem; font-weight: 600;">
                {get_text('npn_value')}
            </div>
            <div class="npn-value">{npn_value:.2f}%</div>
            <div class="quality-badge" style="color: {color};">
                {emoji} {quality}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Recommendation
        st.markdown(f"""
        <div class="info-box">
            <h4 style="margin: 0 0 0.5rem 0; color: {color};">{emoji} {get_text('recommendation')}</h4>
            <p style="margin: 0; font-size: 1.1rem;">{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)

        # RGB Values
        st.markdown(f"### {get_text('rgb_values')}")
        st.markdown(f"""
        <div class="rgb-container">
            <div class="rgb-box" style="background: linear-gradient(135deg, #fee2e2, #fca5a5);">
                <div class="rgb-label">Red (R)</div>
                <div class="rgb-value">{r:.1f}</div>
            </div>
            <div class="rgb-box" style="background: linear-gradient(135deg, #dcfce7, #86efac);">
                <div class="rgb-label">Green (G)</div>
                <div class="rgb-value">{g:.1f}</div>
            </div>
            <div class="rgb-box" style="background: linear-gradient(135deg, #dbeafe, #93c5fd);">
                <div class="rgb-label">Blue (B)</div>
                <div class="rgb-value">{b:.1f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Calculation details
        with st.expander(f"🔍 {get_text('method')}"):
            st.markdown(f"""
            **{get_text('equation')}:**
            `y = -0.0261x + 3.8385`

            **Calculation:**
            - Green (G) value: {g:.2f}
            - NPN = -0.0261 × {g:.2f} + 3.8385
            - NPN = {npn_value:.2f}%

            **Correlation:**
            - R² = 0.5902
            - r = -0.76823 (P < 0.01)

            **{get_text('reference')}:**
            {get_text('ref_text')}
            """)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 4rem 2rem;">
            <div style="font-size: 5rem; margin-bottom: 1rem;">📊</div>
            <h3>{get_text('results_title')}</h3>
            <p style="color: #64748b;">
                {get_text('upload_help')}<br>
                {get_text('analyze_btn').replace('🔍', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: white; padding: 2rem; font-size: 0.9rem;">
    Powered by Streamlit | Based on research by Nopparatmaitree et al. (2023)
</div>
""", unsafe_allow_html=True)
