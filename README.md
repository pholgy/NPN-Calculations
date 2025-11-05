# 🔬 NPN Analysis System for Soybean Meal

ระบบวิเคราะห์ปริมาณไนโตรเจนไม่ใช่โปรตีน (NPN) ในสารสกัดจากกากถั่วเหลือง

## Overview

This web application analyzes Non-Protein Nitrogen (NPN) content in soybean meal extracts using photocolorimetric methodology. The system is based on research by Nopparatmaitree et al. (2023) published in Khon Kaen Agriculture Journal.

## Features

✅ **Bilingual Support** - Thai and English interface
✅ **Image Upload** - Upload solution photos from mobile or desktop
✅ **Automatic RGB Extraction** - Analyzes color values automatically
✅ **NPN Calculation** - Uses validated regression equation (R² = 0.5902)
✅ **Quality Assessment** - Provides quality level and recommendations
✅ **Clean UI** - Simple, infographic-style interface
✅ **Mobile Friendly** - Responsive design for all devices

## How It Works

1. **Upload Image**: Take or upload a photo of the solution after reaction with Nessler reagent
2. **RGB Extraction**: System automatically extracts RGB color values from the image
3. **NPN Calculation**: Calculates NPN using the equation: `y = -0.0261x + 3.8385`
   - y = NPN content (%)
   - x = Green color intensity (G)
4. **Results Display**: Shows NPN value, quality level, and recommendations

## Installation & Local Testing

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

```bash
# Clone or download this repository
cd WebApp-Wansaiyidahkaosar

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Set main file path: `app.py`
7. Click "Deploy"

**Deployment URL**: Will be `https://[your-app-name].streamlit.app`

### Option 2: Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com)
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Click "Create Web Service"

### Option 3: Hugging Face Spaces

1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Space
3. Select "Streamlit" as SDK
4. Upload your files or connect to GitHub
5. App will deploy automatically

## Project Structure

```
WebApp-Wansaiyidahkaosar/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── README.md                # This file
└── เปเปอร์+สมการ.pdf         # Research paper reference
```

## Technical Details

### Regression Equation
Based on the research paper (Experiment 1):
- **Equation**: y = -0.0261x + 3.8385
- **Correlation coefficient (r)**: -0.76823 (P < 0.01)
- **R²**: 0.5902 (P < 0.01)
- **Method**: Simple linear regression between NPN content and Green (G) color value

### Quality Assessment Criteria

| NPN Content (%) | Quality Level | Status |
|----------------|---------------|--------|
| ≤ 0.5 | Good | ✅ Suitable for use |
| 0.5 - 1.0 | Medium | ⚠️ Further inspection |
| 1.0 - 2.0 | Low | ⚠️ Needs improvement |
| > 2.0 | Very Low | ❌ Not recommended |

## Research Reference

**Title**: Development of technique for measuring non protein nitrogen in soybean meal by spectrophotometer and photocolorimetric methodology

**Authors**: Manatsanun Nopparatmaitree et al.

**Publication**: Khon Kaen Agriculture Journal SUPPL. 1: (2023)

**Institution**: Silpakorn University, Faculty of Animal Sciences and Agricultural Technology

## Usage Notes

- Take photos under consistent lighting conditions
- Use white background for best results
- Ensure solution has completed reaction with Nessler reagent
- Photos should clearly show the solution color
- Avoid shadows or glare in photos

## Support

For issues or questions:
- Check the "How to Use" section in the app
- Review the research paper for methodology details
- Ensure proper sample preparation with Nessler reagent

## License

This application is developed for educational and research purposes based on published scientific research.

---

**Developed based on research by Nopparatmaitree et al. (2023)**
Khon Kaen Agriculture Journal SUPPL. 1: (2023)
