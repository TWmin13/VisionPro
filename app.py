import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
from streamlit_drawable_canvas import st_canvas
from streamlit_image_comparison import image_comparison
from streamlit_image_coordinates import streamlit_image_coordinates
import io
from datetime import datetime
import base64



def pil_image_to_data_url(img: Image.Image) -> str:
    """Converts a PIL image to a data URL (base64) for Streamlit canvas."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Initialize session state for theme if it doesn't exist
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Default to dark mode

st.set_page_config(page_title="VisionPro", layout="wide")

# Function to toggle theme
''''def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    #st.experimental_rerun()'''

# Apply theme based on session state
if st.session_state.theme == 'dark':
    # Dark mode styling - sleeker Apple-inspired UI
    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            background-color: #000000;
            color: #f5f5f7;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'San Francisco', 'Segoe UI', 'Helvetica Neue', sans-serif;
        }
        h1, h2, h3 {
            font-weight: 600 !important;
        }
        .stButton > button {
            background-color: #1c1c1e;
            color: #f5f5f7;
            border-radius: 20px;
            padding: 0.6em 1.2em;
            border: none;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #2c2c2e;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        .stButton > button:active {
            transform: translateY(0px);
        }
        .stSlider > div[data-baseweb="slider"] {
            padding: 0.5em;
        }
        .stSlider [data-testid="stThumbValue"] {
            color: #f5f5f7 !important;
        }
        .stTextInput > div > div > input {
            background-color: #1c1c1e;
            color: #f5f5f7;
            border-radius: 12px;
            border: none;
            padding: 12px 16px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stTextInput > div > div > input:focus {
            background-color: #2c2c2e;
            box-shadow: 0 0 0 3px rgba(0,125,250,0.4);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        [data-testid="stSidebar"] {
            background-color: #1c1c1e;
            border-right: none !important;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
        }
        .st-cb, .st-ce, .st-af, .st-ag {
            background-color: #1c1c1e !important;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .st-cy {
            color: #f5f5f7 !important;
        }
        .stTextArea > div > div > textarea {
            background-color: #1c1c1e !important;
            color: #f5f5f7 !important;
            border-radius: 12px;
            border: none;
            padding: 12px 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stSelectbox > div > div {
            background-color: #1c1c1e !important;
            color: #f5f5f7 !important;
            border-radius: 12px;
            border: none;
        }
        .stSelectbox [data-baseweb="select"] > div {
            background-color: #1c1c1e !important;
            border: none !important;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        .stSelectbox [data-baseweb="select"]:hover > div {
            background-color: #2c2c2e !important;
        }
        .stRadio > div {
            background-color: #1c1c1e !important;
            border-radius: 12px;
            padding: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            color: #f5f5f7 !important;
        }
        .stRadio [data-testid="stMarkdownContainer"] p {
            color: #f5f5f7 !important;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.6s ease forwards;
        }
        .stSlider [data-baseweb="slider"] [data-testid="stThumb"] {
            background-color: #0071e3;
            border: none;
            box-shadow: 0 0 5px rgba(0,113,227,0.5);
        }
        [data-testid="stFileUploader"] > div > label {
            background-color: #1c1c1e !important;
            color: #f5f5f7 !important;
            border-radius: 20px !important;
            padding: 0.6em 1.2em !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        }
        [data-testid="stFileUploader"] > div > label:hover {
            background-color: #2c2c2e !important;
            box-shadow: 0 6px 8px rgba(0,0,0,0.15) !important;
        }
        [data-testid="stFileUploader"] > div > small {
            color: #86868b !important;
        }
        [data-testid="stImage"] {
            border-radius: 12px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        }
        [data-testid="stImage"]:hover {
            transform: scale(1.01);
            box-shadow: 0 16px 30px rgba(0,0,0,0.3);
        }
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        [data-testid="StyledLinkIconContainer"] svg {
            fill: #f5f5f7 !important;
        }
        .stApp a {
            color: #0071e3 !important;
        }
        [data-testid="stDownloadButton"] {
            border-radius: 20px !important;
        }
        .streamlit-expanderHeader {
            background-color: #1c1c1e !important;
            color: #f5f5f7 !important;
            border-radius: 8px !important;
        }
        [data-testid="caption"] {
            color: #a1a1a6 !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    # Light mode styling - sleeker Apple-inspired UI
    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            background-color: #f5f5f7;
            color: #1d1d1f;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'San Francisco', 'Segoe UI', 'Helvetica Neue', sans-serif;
        }
        h1, h2, h3 {
            font-weight: 600 !important;
            color: #1d1d1f !important;
        }
        p, li, div {
            color: #1d1d1f !important;
        }
        .stButton > button {
            background-color: #ffffff;
            color: #1d1d1f;
            border-radius: 20px;
            padding: 0.6em 1.2em;
            border: none;
            transition: all 0.2s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #f7f7f7;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        }
        .stButton > button:active {
            transform: translateY(0px);
        }
        .stSlider > div[data-baseweb="slider"] {
            padding: 0.5em;
        }
        .stSlider [data-testid="stThumbValue"] {
            color: #1d1d1f !important;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            color: #1d1d1f;
            border-radius: 12px;
            border: none;
            padding: 12px 16px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .stTextInput > div > div > input:focus {
            background-color: #f7f7f7;
            box-shadow: 0 0 0 3px rgba(0,125,250,0.2);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: none !important;
            box-shadow: 0 0 20px rgba(0,0,0,0.06);
        }
        .st-cb, .st-ce, .st-af, .st-ag {
            background-color: #ffffff !important;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        }
        .st-cy {
            color: #1d1d1f !important;
        }
        .stTextArea > div > div > textarea {
            background-color: #ffffff !important;
            color: #1d1d1f !important;
            border-radius: 12px;
            border: none;
            padding: 12px 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .stSelectbox > div > div {
            background-color: #ffffff !important;
            color: #1d1d1f !important;
            border-radius: 12px;
            border: none;
        }
        .stSelectbox [data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: none !important;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .stSelectbox [data-baseweb="select"]:hover > div {
            background-color: #f7f7f7 !important;
        }
        .stRadio > div {
            background-color: #ffffff !important;
            border-radius: 12px;
            padding: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        }
        .stRadio [data-testid="stMarkdownContainer"] p {
            color: #1d1d1f !important;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.6s ease forwards;
        }
        .stSlider [data-baseweb="slider"] [data-testid="stThumb"] {
            background-color: #0071e3;
            border: none;
            box-shadow: 0 0 5px rgba(0,113,227,0.3);
        }
        [data-testid="stFileUploader"] > div > label {
            background-color: #ffffff !important;
            color: #1d1d1f !important;
            border-radius: 20px !important;
            padding: 0.6em 1.2em !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        }
        [data-testid="stFileUploader"] > div > label:hover {
            background-color: #f7f7f7 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08) !important;
        }
        [data-testid="stFileUploader"] > div > small {
            color: #6e6e73 !important;
        }
        [data-testid="stImage"] {
            border-radius: 12px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        }
        [data-testid="stImage"]:hover {
            transform: scale(1.01);
            box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        }
        [data-testid="stHeader"] {
            background-color: rgba(245,245,247,0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        [data-testid="StyledLinkIconContainer"] svg {
            fill: #1d1d1f !important;
        }
        .stApp a {
            color: #0071e3 !important;
        }
        [data-testid="stDownloadButton"] {
            border-radius: 20px !important;
        }
        .streamlit-expanderHeader {
            background-color: #ffffff !important;
            color: #1d1d1f !important;
            border-radius: 8px !important;
        }
        [data-testid="caption"] {
            color: #6e6e73 !important;
        }
        [data-testid="stMarkdownContainer"] {
            color: #1d1d1f !important;
        }
        .stCheckbox label p {
            color: #1d1d1f !important;
        }
        label, .stRadio label p {
            color: #1d1d1f !important;
        }
        </style>
    """, unsafe_allow_html=True)

# App title and description
title_color = "#f5f5f7" if st.session_state.theme == 'dark' else "#1d1d1f"
subtitle_color = "#a1a1a6" if st.session_state.theme == 'dark' else "#6e6e73"

st.markdown(f"""
    <h1 style='text-align: center; color: {title_color}; text-shadow: 0 2px 8px rgba(0,0,0,0.08);' class='fade-in'>VisionPro</h1>
    <p style='text-align: center; font-size: 1.2rem; color: {subtitle_color}; margin-bottom: 30px;' class='fade-in'>Made for Creators. Built for Intelligence.</p>
""", unsafe_allow_html=True)

# Create a cleaner sidebar
st.sidebar.markdown(f"<h3 style='color: {title_color}; margin-bottom: 20px;'>⚙️ Controls</h3>", unsafe_allow_html=True)

# --- In the sidebar or header section ---
theme_toggle = st.toggle("Dark Mode", value=(st.session_state.theme == 'dark'))

# --- Update theme without rerun ---
st.session_state.theme = 'dark' if theme_toggle else 'light'

# You can now use the theme like:
bg_color = "#1c1c1e" if st.session_state.theme == 'dark' else "#ffffff"
text_color = "#f5f5f7" if st.session_state.theme == 'dark' else "#1d1d1f"

# Theme toggle in sidebar with Apple-like button
'''theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
theme_text = "Light Mode" if st.session_state.theme == 'dark' else "Dark Mode"
st.sidebar.button(f"{theme_icon} {theme_text}", on_click=toggle_theme)'''

st.sidebar.markdown(f"<p style='color: {subtitle_color}; margin-top: 25px; margin-bottom: 10px;'>Image Source</p>", unsafe_allow_html=True)
source_type = st.sidebar.radio("", ["Upload", "Webcam"], index=0, label_visibility="collapsed")

if source_type == "Webcam":
    uploaded_file = st.camera_input("📷 Capture Image")
else:
    uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png", "webp", "bmp"], label_visibility="collapsed")
    st.sidebar.markdown(f"<p style='color: {subtitle_color}; font-size: 0.8rem;'>Supported: JPG, PNG, WebP, BMP</p>", unsafe_allow_html=True)

if uploaded_file:
    # Process the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Display original image
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.image(image, caption="Original Image", use_column_width=True)
    
    with col2:
        # Metadata display in a clean card
        bg_color = "#1c1c1e" if st.session_state.theme == 'dark' else "#ffffff"
        text_color = "#f5f5f7" if st.session_state.theme == 'dark' else "#1d1d1f"
        accent_color = "#a1a1a6" if st.session_state.theme == 'dark' else "#6e6e73"
        
        st.markdown(f"""
            <div style="background-color: {bg_color}; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <h4 style="color: {text_color}; margin-bottom: 15px;">Image Info</h4>
                <p style="color: {text_color}; margin-bottom: 8px;"><span style="color: {accent_color};">Dimensions:</span> {image.width} × {image.height}</p>
                <p style="color: {text_color}; margin-bottom: 8px;"><span style="color: {accent_color};">Format:</span> {image.format if image.format else 'Unknown'}</p>
                <p style="color: {text_color};"><span style="color: {accent_color};">Mode:</span> {image.mode}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Fix the download button issue by ensuring the buffer is populated correctly
        download_buf = io.BytesIO()
        image.save(download_buf, format="JPEG")
        download_buf.seek(0)  # Reset buffer position to beginning
        st.download_button(
            label="Download Original",
            data=download_buf.getvalue(),
            file_name=f"original_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    # Feature selection with sleeker UI
    st.sidebar.markdown(f"<p style='color: {subtitle_color}; margin-top: 25px; margin-bottom: 10px;'>Processing</p>", unsafe_allow_html=True)
    feature = st.sidebar.selectbox("", [
        "Resize", "Histogram", "Histogram Equalization", "Contrast Stretching", "Thresholding",
        "Color Pop", "Gray Level Slicing", "Bit Plane Slicing", "Filters", "Draw on Image",
        "Canny Edge Detection", "Cartoon Effect", "OCR (Text Extraction)", "Live FFT", "Pixel Inspector"], 
        label_visibility="collapsed")

    # Display the selected feature name
    feature_title_color = "#f5f5f7" if st.session_state.theme == 'dark' else "#1d1d1f"
    st.markdown(f"<h2 style='color: {feature_title_color}; margin-top: 20px; margin-bottom: 20px;'>{feature}</h2>", unsafe_allow_html=True)
    
    if feature == "Resize":
        col1, col2 = st.columns(2)
        with col1:
            width = st.slider("Width", 50, 1000, image_cv.shape[1])
        with col2:
            height = st.slider("Height", 50, 1000, image_cv.shape[0])
        
        resized = cv2.resize(image_cv, (width, height))
        st.image(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB), caption=f"Resized to {width}×{height}", use_column_width=True)
        
        # Fix download button for resized image
        buf = io.BytesIO()
        resized_img = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
        resized_img.save(buf, format="JPEG")
        buf.seek(0)  # Reset buffer position
        st.download_button(
            label="Download Resized Image",
            data=buf.getvalue(),
            file_name=f"resized_{width}x{height}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "Histogram":
        rgb_hist = st.checkbox("Show RGB Histogram", value=False)

        # Theme-based color setup
        if st.session_state.theme == 'dark':
            text_color = '#f5f5f7'
            background_color = (28/255, 28/255, 30/255, 0.7)
        else:
            text_color = '#1d1d1f'
            background_color = (28/255, 28/255, 30/255, 0.7)

        fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')

        if rgb_hist:
            for i, col in enumerate(('r', 'g', 'b')):
                hist = cv2.calcHist([image_cv], [i], None, [256], [0, 256])
                ax.plot(hist, color=col, label=f"{col.upper()} Channel", linewidth=2)
                ax.fill_between(range(256), hist.flatten(), alpha=0.2, color=col)
        else:
            hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
            ax.plot(hist, color=text_color, label="Grayscale", linewidth=2)
            ax.fill_between(range(256), hist.flatten(), alpha=0.2, color=text_color)

        ax.set_title("Pixel Intensity Distribution", color=text_color, fontsize=14, fontweight='bold')
        ax.set_xlabel("Pixel Intensity", color=text_color)
        ax.set_ylabel("Frequency", color=text_color)
        ax.tick_params(colors=text_color)

        for spine in ax.spines.values():
            spine.set_color(text_color)

        # Legend styling
        legend = ax.legend(facecolor=background_color, edgecolor='none', framealpha=0.8, fontsize=10)
        plt.setp(legend.get_texts(), color=text_color)

        ax.grid(True, linestyle='--', alpha=0.3, color=text_color)
        ax.set_facecolor('none')
        fig.patch.set_alpha(0.0)

        st.pyplot(fig)

        # Download button for histogram
        buf = io.BytesIO()
        fig.savefig(buf, format='png', transparent=True, dpi=300)
        buf.seek(0)

        st.download_button(
            label="Download Histogram",
            data=buf.getvalue(),
            file_name=f"histogram_{'rgb' if rgb_hist else 'gray'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png"
        )

    elif feature == "Histogram Equalization":
        equalized = cv2.equalizeHist(gray_image)
        image_comparison(
            img1=Image.fromarray(gray_image),
            img2=Image.fromarray(equalized),
            label1="Original",
            label2="Equalized"
        )

        # Use theme-aware text color
        hist_color = '#1d1d1f' if st.session_state.theme == 'light' else '#f5f5f7'

        col1, col2 = st.columns(2)

        with col1:
            fig1, ax1 = plt.subplots(figsize=(5, 3), facecolor='none')
            hist_original = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
            ax1.plot(hist_original, color=hist_color, linewidth=2)
            ax1.set_title("Original Histogram", color=hist_color)
            ax1.tick_params(colors=hist_color)
            for spine in ax1.spines.values():
                spine.set_color(hist_color)
            ax1.set_facecolor('none')
            fig1.patch.set_alpha(0.0)
            st.pyplot(fig1)

        with col2:
            fig2, ax2 = plt.subplots(figsize=(5, 3), facecolor='none')
            hist_equalized = cv2.calcHist([equalized], [0], None, [256], [0, 256])
            ax2.plot(hist_equalized, color=hist_color, linewidth=2)
            ax2.set_title("Equalized Histogram", color=hist_color)
            ax2.tick_params(colors=hist_color)
            for spine in ax2.spines.values():
                spine.set_color(hist_color)
            ax2.set_facecolor('none')
            fig2.patch.set_alpha(0.0)
            st.pyplot(fig2)

        # Download button for equalized image
        buf = io.BytesIO()
        Image.fromarray(equalized).save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="Download Equalized Image",
            data=buf.getvalue(),
            file_name=f"equalized_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "Contrast Stretching":
        r_min, r_max = np.min(gray_image), np.max(gray_image)
        stretched = cv2.normalize(gray_image, None, 0, 255, cv2.NORM_MINMAX)
        stretched = stretched.astype(np.uint8)
        
        image_comparison(
            img1=Image.fromarray(gray_image), 
            img2=Image.fromarray(stretched), 
            label1="Original", 
            label2="Stretched"
        )
        
        # Display min/max values
        col1, col2 = st.columns(2)
        
        with col1:
            text_color = "#f5f5f7" if st.session_state.theme == 'dark' else "#1d1d1f"
            bg_color = "#1c1c1e" if st.session_state.theme == 'dark' else "#ffffff"
            st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <h4 style="color: {text_color}; margin-bottom: 10px;">Original Range</h4>
                    <p style="color: {text_color};">Min: {r_min}</p>
                    <p style="color: {text_color};">Max: {r_max}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <h4 style="color: {text_color}; margin-bottom: 10px;">Stretched Range</h4>
                    <p style="color: {text_color};">Min: 0</p>
                    <p style="color: {text_color};">Max: 255</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Add download button for stretched image
        buf = io.BytesIO()
        Image.fromarray(stretched).save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="Download Stretched Image",
            data=buf.getvalue(),
            file_name=f"stretched_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "Thresholding":
        col1, col2 = st.columns(2)
        with col1:
            thresh_value = st.slider("Threshold Value", 0, 255, 127)
        with col2:
            thresh_type = st.selectbox("Threshold Method", ["Binary", "Adaptive", "Otsu"], index=0)
        
        if thresh_type == "Binary":
            _, threshold = cv2.threshold(gray_image, thresh_value, 255, cv2.THRESH_BINARY)
            caption = f"Binary Threshold (value={thresh_value})"
        elif thresh_type == "Adaptive":
            block_size = st.slider("Block Size (must be odd)", 3, 51, 11, step=2)
            constant = st.slider("Constant", 0, 50, 2)
            threshold = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, block_size, constant)
            caption = f"Adaptive Threshold (block={block_size}, C={constant})"
        else:  # Otsu
            _, threshold = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            caption = "Otsu Threshold"
        
        image_comparison(
            img1=Image.fromarray(gray_image), 
            img2=Image.fromarray(threshold), 
            label1="Original", 
            label2=thresh_type
        )
        
        # Add download button for thresholded image
        buf = io.BytesIO()
        Image.fromarray(threshold).save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="Download Thresholded Image",
            data=buf.getvalue(),
            file_name=f"{thresh_type.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "Color Pop":
        col1, col2 = st.columns(2)
        with col1:
            color_name = st.selectbox("Select color to pop", ["Red", "Green", "Blue", "Yellow", "Orange", "Purple"])
            sensitivity = st.slider("Color Sensitivity", 10, 100, 40)
        with col2:
            grayscale_bg = st.checkbox("Grayscale Background", value=True)
            preview = st.checkbox("Show Color Range Preview", value=False)
        
        # Define HSV ranges for common colors
        color_ranges = {
            "Red": ([0, 100-sensitivity, 50], [10, 255, 255]),
            "Green": ([45, 100-sensitivity, 50], [85, 255, 255]),
            "Blue": ([100, 100-sensitivity, 50], [140, 255, 255]),
            "Yellow": ([25, 100-sensitivity, 50], [35, 255, 255]),
            "Orange": ([10, 100-sensitivity, 50], [25, 255, 255]),
            "Purple": ([140, 100-sensitivity, 50], [170, 255, 255])
        }
        
        lower_bound, upper_bound = color_ranges[color_name]
        
        # Convert to HSV and create mask
        hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(lower_bound), np.array(upper_bound))
        
        # Optional: show mask preview
        if preview:
            st.image(mask, caption="Color Range Mask", use_column_width=True)
        
        # Apply color pop effect
        color_part = cv2.bitwise_and(image_cv, image_cv, mask=mask)
        
        if grayscale_bg:
            gray_bg = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            gray_bg = cv2.cvtColor(gray_bg, cv2.COLOR_GRAY2BGR)
        else:
            gray_bg = image_cv.copy()
            gray_bg[mask > 0] = [0, 0, 0]
        
        final = np.where(mask[:, :, None] == 0, gray_bg, color_part)
        st.image(cv2.cvtColor(final, cv2.COLOR_BGR2RGB), caption=f"{color_name} Pop Effect", use_column_width=True)
        
        # Fix download button for color pop
        buf = io.BytesIO()
        Image.fromarray(cv2.cvtColor(final, cv2.COLOR_BGR2RGB)).save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="Download Color Pop Image",
            data=buf.getvalue(),
            file_name=f"colorpop_{color_name.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "Gray Level Slicing":
        col1, col2 = st.columns(2)
        with col1:
            min_val = st.slider("Min Gray Value", 0, 255, 100)
        with col2:
            max_val = st.slider("Max Gray Value", 0, 255, 200)
        
        highlight_option = st.radio("Slicing Method", 
            ["Highlight range, set rest to 0", 
             "Highlight range to white, preserve rest", 
             "Highlight range, make rest grayscale"])
        
        if highlight_option == "Highlight range, set rest to 0":
            sliced = np.where((gray_image >= min_val) & (gray_image <= max_val), gray_image, 0).astype(np.uint8)
        elif highlight_option == "Highlight range to white, preserve rest":
            sliced = np.where((gray_image >= min_val) & (gray_image <= max_val), 255, gray_image).astype(np.uint8)
        else:
            # Create a color version for highlighting
            color_highlight = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
            
            # Create a mask for the range
            mask = np.zeros_like(gray_image)
            mask[(gray_image >= min_val) & (gray_image <= max_val)] = 255
            
            # Apply a color tint to the range (bluish)
            color_highlight[(gray_image >= min_val) & (gray_image <= max_val), 0] = 255  # Blue channel
            
            sliced = color_highlight
        
        image_comparison(
            img1=Image.fromarray(gray_image), 
            img2=Image.fromarray(sliced), 
            label1="Original", 
            label2="Gray Level Sliced"
        )
        
        # Add download button for gray level slicing
        buf = io.BytesIO()
        Image.fromarray(sliced).save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="Download Sliced Image",
            data=buf.getvalue(),
            file_name=f"sliced_{min_val}_{max_val}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "Bit Plane Slicing":
        st.markdown("""
            <div style="background-color: #1c1c1e; padding: 15px; border-radius: 12px; margin-bottom: 20px;">
                <p style="color: #f5f5f7; margin: 0;">Bit plane slicing separates an image into individual bit planes, showing the contribution of each bit to the overall image.</p>
            </div>
        """, unsafe_allow_html=True)
        
        selected_plane = st.slider("Select Bit Plane to View", 0, 7, 7)
        show_all = st.checkbox("Show All Planes", value=False)
        
        plane = ((gray_image & (1 << selected_plane)) >> selected_plane) * 255
        
        if show_all:
            bit_planes = []
            col_titles = []
            for i in range(8):
                current_plane = ((gray_image & (1 << i)) >> i) * 255
                bit_planes.append(current_plane)
                col_titles.append(f"Bit {i}")
            
            # Display bit planes in grid
            st.image(bit_planes, caption=col_titles, width=150)
            
            # Reconstruct image using selected bits
            selected_bits = st.multiselect("Select Bits for Reconstruction", list(range(8)), default=[7, 6, 5, 4])
            if selected_bits:
                reconstructed = np.zeros_like(gray_image)
                for bit in selected_bits:
                    reconstructed += ((gray_image & (1 << bit)) >> bit) << bit
                
                image_comparison(
                    img1=Image.fromarray(gray_image), 
                    img2=Image.fromarray(reconstructed), 
                    label1="Original", 
                    label2=f"Bits {', '.join(map(str, selected_bits))}"
                )
                
                # Add download button for reconstructed image
                buf = io.BytesIO()
                Image.fromarray(reconstructed).save(buf, format="JPEG")
                buf.seek(0)
                st.download_button(
                    label="Download Reconstructed Image",
                    data=buf.getvalue(),
                    file_name=f"reconstructed_bits{''.join(map(str, selected_bits))}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                    mime="image/jpeg"
                )
        else:
            image_comparison(
                img1=Image.fromarray(gray_image), 
                img2=Image.fromarray(plane), 
                label1="Original", 
                label2=f"Bit Plane {selected_plane}"
            )
            
            # Add download button for bit plane
            buf = io.BytesIO()
            Image.fromarray(plane).save(buf, format="JPEG")
            buf.seek(0)
            st.download_button(
                label=f"Download Bit Plane {selected_plane}",
                data=buf.getvalue(),
                file_name=f"bit_plane_{selected_plane}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                mime="image/jpeg"
            )

    elif feature == "Filters":
        col1, col2 = st.columns(2)
        with col1:
            filter_type = st.selectbox("Filter Type", [
                "Gaussian Blur", "Median Blur", "Bilateral Filter", 
                "Sharpen", "Edge Enhance", "Emboss", "Sepia", "Negative"
            ])
        with col2:
            intensity = st.slider("Intensity/Kernel Size", 1, 31, 5, step=2)
        
        if filter_type == "Gaussian Blur":
            filtered = cv2.GaussianBlur(image_cv, (intensity, intensity), 0)
        elif filter_type == "Median Blur":
            filtered = cv2.medianBlur(image_cv, intensity)
        elif filter_type == "Bilateral Filter":
            sigma = intensity * 5
            filtered = cv2.bilateralFilter(image_cv, intensity, sigma, sigma)
        elif filter_type == "Sharpen":
            kernel = np.array([
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ]) * (intensity / 5)
            kernel[1, 1] = 1 + 4 * (intensity / 5)  # Adjust center based on intensity
            filtered = cv2.filter2D(image_cv, -1, kernel)
        elif filter_type == "Edge Enhance":
            kernel = np.array([
                [-1, -1, -1],
                [-1, 9, -1],
                [-1, -1, -1]
            ]) * (intensity / 10)
            kernel[1, 1] = 1 + 8 * (intensity / 10)  # Adjust center based on intensity
            filtered = cv2.filter2D(image_cv, -1, kernel)
        elif filter_type == "Emboss":
            kernel = np.array([
                [-2, -1, 0],
                [-1, 1, 1],
                [0, 1, 2]
            ]) * (intensity / 10)
            filtered = cv2.filter2D(image_cv, -1, kernel) + 128
        elif filter_type == "Sepia":
            filtered = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
            filtered = filtered.astype(np.float32) / 255.0
            sepia_filter = np.array([
                [0.393 + (intensity / 100), 0.769 - (intensity / 100), 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131 + (intensity / 100)]
            ])
            filtered = cv2.transform(filtered, sepia_filter)
            filtered = np.clip(filtered * 255, 0, 255).astype(np.uint8)
        elif filter_type == "Negative":
            filtered = 255 - image_cv
        
        image_comparison(
            img1=Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)), 
            img2=Image.fromarray(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)), 
            label1="Original", 
            label2=filter_type
        )
        
        # Add download button for filtered image
        buf = io.BytesIO()
        Image.fromarray(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)).save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="Download Filtered Image",
            data=buf.getvalue(),
            file_name=f"{filter_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "Draw on Image":
        stroke_width = st.slider("Brush Width", 1, 25, 5)
        stroke_color = st.color_picker("Brush Color", "#FF0000")
    
        # Convert original image to RGBA (needed for overlay)
        rgba_image = image.convert("RGBA")
    
        # Convert to base64 URL so Streamlit Cloud can use it
        import base64
        def image_to_url(pil_img):
            buffered = io.BytesIO()
            pil_img.save(buffered, format="PNG")
            encoded = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/png;base64,{encoded}"
    
        bg_image_url = image_to_url(rgba_image)
    
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.0)",  # Transparent fill
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_image_url=bg_image_url,  # ✅ Only use the URL version
            update_streamlit=True,
            height=rgba_image.height,
            width=rgba_image.width,
            drawing_mode="freedraw",
            key="canvas",
        )
    
        if canvas_result.image_data is not None:
            # Convert drawn canvas back to image
            drawn_rgba = Image.fromarray(canvas_result.image_data.astype(np.uint8))
    
            # --- Download annotation only ---
            buf_annot = io.BytesIO()
            drawn_rgba.convert("RGB").save(buf_annot, format="JPEG")
            buf_annot.seek(0)
    
            st.download_button(
                label="Download Drawing Only",
                data=buf_annot.getvalue(),
                file_name=f"annotation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                mime="image/jpeg"
            )
    
            # --- Merge drawing and original ---
            combined = Image.alpha_composite(rgba_image, drawn_rgba)
    
            st.image(combined, caption="Combined Image (Original + Drawing)", use_column_width=True)
    
            # --- Download combined image ---
            buf_combined = io.BytesIO()
            combined.convert("RGB").save(buf_combined, format="JPEG")
            buf_combined.seek(0)
    
            st.download_button(
                label="Download Combined Image",
                data=buf_combined.getvalue(),
                file_name=f"combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                mime="image/jpeg"
            )


    elif feature == "Canny Edge Detection":
        col1, col2 = st.columns(2)
        with col1:
            low_threshold = st.slider("Low Threshold", 0, 255, 50)
        with col2:
            high_threshold = st.slider("High Threshold", 0, 255, 150)
        
        blur_kernel = st.slider("Blur Kernel Size", 1, 15, 5, step=2)
        edges = cv2.GaussianBlur(gray_image, (blur_kernel, blur_kernel), 0)
        edges = cv2.Canny(edges, low_threshold, high_threshold)
        
        image_comparison(
            img1=Image.fromarray(gray_image), 
            img2=Image.fromarray(edges), 
            label1="Original", 
            label2="Edges"
        )
        
        # Create colored edges option
        colored_edges = st.checkbox("Colored Edges", value=False)
        if colored_edges:
            # Create a color image from edges
            edge_color = st.color_picker("Edge Color", "#00FF00")
            r, g, b = int(edge_color[1:3], 16), int(edge_color[3:5], 16), int(edge_color[5:7], 16)
            
            color_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            color_edges[edges > 0] = [b, g, r]  # BGR format
            
            st.image(cv2.cvtColor(color_edges, cv2.COLOR_BGR2RGB), caption="Colored Edges", use_column_width=True)
            
            # Add download button for colored edges
            buf = io.BytesIO()
            Image.fromarray(cv2.cvtColor(color_edges, cv2.COLOR_BGR2RGB)).save(buf, format="JPEG")
            buf.seek(0)
            st.download_button(
                label="Download Colored Edges",
                data=buf.getvalue(),
                file_name=f"colored_edges_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                mime="image/jpeg"
            )
        
        # Add download button for edge detection
        buf = io.BytesIO()
        Image.fromarray(edges).save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="Download Edge Image",
            data=buf.getvalue(),
            file_name=f"edges_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "Cartoon Effect":
        col1, col2 = st.columns(2)
        with col1:
            edge_thresh = st.slider("Edge Threshold", 1, 21, 9, step=2)
        with col2:
            bilateral_iterations = st.slider("Detail Smoothing", 1, 15, 7)
        
        # Create cartoon effect
        gray_blur = cv2.medianBlur(gray_image, 5)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                     cv2.THRESH_BINARY, edge_thresh, edge_thresh)
        
        # Apply bilateral filter multiple times for smoother colors
        color = image_cv.copy()
        for _ in range(bilateral_iterations):
            color = cv2.bilateralFilter(color, 9, 150, 150)
        
        # Merge color image with edges
        cartoon = cv2.bitwise_and(cv2.cvtColor(color, cv2.COLOR_BGR2RGB), 
                                  cv2.cvtColor(color, cv2.COLOR_BGR2RGB), 
                                  mask=edges)
        
        # Additional style options
        style = st.selectbox("Cartoon Style", ["Classic", "Detailed", "Artistic"])
        
        if style == "Detailed":
            # Less edge detection, more detail
            edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, edge_thresh*2+1, edge_thresh)
            cartoon = cv2.bitwise_and(cv2.cvtColor(color, cv2.COLOR_BGR2RGB), 
                                      cv2.cvtColor(color, cv2.COLOR_BGR2RGB), 
                                      mask=edges)
        elif style == "Artistic":
            # More color quantization
            k = 8  # Number of clusters for color quantization
            data = np.float32(image_cv).reshape((-1, 3))
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            center = np.uint8(center)
            result = center[label.flatten()]
            quantized = result.reshape(image_cv.shape)
            
            # Combine with edges
            cartoon = cv2.bitwise_and(cv2.cvtColor(quantized, cv2.COLOR_BGR2RGB), 
                                      cv2.cvtColor(quantized, cv2.COLOR_BGR2RGB), 
                                      mask=edges)
        
        image_comparison(
            img1=Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)), 
            img2=Image.fromarray(cartoon), 
            label1="Original", 
            label2=f"{style} Cartoon"
        )
        
        # Add download button for cartoon effect
        buf = io.BytesIO()
        Image.fromarray(cartoon).save(buf, format="JPEG")
        buf.seek(0)
        st.download_button(
            label="Download Cartoon Image",
            data=buf.getvalue(),
            file_name=f"cartoon_{style.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg"
        )

    elif feature == "OCR (Text Extraction)":
        # Language selection
        lang = st.selectbox("Select Language", ["eng", "fra", "deu", "spa", "ita", "jpn", "kor", "chi_sim"])
        
        # Preprocessing options
        col1, col2 = st.columns(2)
        with col1:
            preprocess = st.checkbox("Preprocess for Better Results", value=True)
        with col2:
            show_boxes = st.checkbox("Show Detected Text Regions", value=False)
        
        if preprocess:
            ocr_img = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            ocr_img = cv2.GaussianBlur(ocr_img, (5, 5), 0)
            ocr_img = cv2.adaptiveThreshold(ocr_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 11, 2)
            
            st.image(ocr_img, caption="Preprocessed Image", use_column_width=True)
        else:
            ocr_img = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        
        # Perform OCR
        text = pytesseract.image_to_string(ocr_img, lang=lang)
        
        # Show text in stylized text area
        st.markdown("""
            <p style="color: #f5f5f7; margin-bottom: 10px;">Extracted Text:</p>
        """, unsafe_allow_html=True)
        
        st.text_area("", text, height=200)
        
        # Show text regions if requested
        if show_boxes:
            boxes_img = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB).copy()
            d = pytesseract.image_to_data(ocr_img, lang=lang, output_type=pytesseract.Output.DICT)
            
            for i in range(len(d['text'])):
                if int(d['conf'][i]) > 60:  # Only show confident detections
                    x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
                    boxes_img = cv2.rectangle(boxes_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    boxes_img = cv2.putText(boxes_img, d['text'][i], (x, y - 10), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            st.image(boxes_img, caption="Detected Text Regions", use_column_width=True)
            
            # Add download button for text regions image
            buf = io.BytesIO()
            Image.fromarray(boxes_img).save(buf, format="JPEG")
            buf.seek(0)
            st.download_button(
                label="Download Text Regions Image",
                data=buf.getvalue(),
                file_name=f"text_regions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                mime="image/jpeg",
                key="download_text_regions"
            )
        
        # Add download button for extracted text
        text_buf = io.StringIO()
        text_buf.write(text)
        text_buf.seek(0)
        st.download_button(
            label="Download Extracted Text",
            data=text_buf.getvalue(),
            file_name=f"extracted_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

    elif feature == "Live FFT":
        # Display original image
        st.image(gray_image, caption="Grayscale Image", use_column_width=True)
        
        # Compute FFT
        f = np.fft.fft2(gray_image)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
        magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Display FFT
        text_color = "#f5f5f7" if st.session_state.theme == 'dark' else "#1d1d1f"
        fig, ax = plt.subplots(figsize=(10, 8), facecolor='none')
        ax.imshow(magnitude_spectrum, cmap='viridis')
        ax.set_title("Magnitude Spectrum (FFT)", color=text_color, fontsize=14)
        ax.axis('off')
        fig.patch.set_alpha(0.0)
        st.pyplot(fig)
        
        # Interactive frequency filtering
        st.subheader("Frequency Domain Filtering")
        filter_type = st.selectbox("Filter Type", ["None", "Low Pass", "High Pass", "Band Pass"])
        
        if filter_type != "None":
            # Create filter mask
            rows, cols = gray_image.shape
            crow, ccol = rows // 2, cols // 2
            mask = np.ones((rows, cols), np.uint8)
            
            if filter_type == "Low Pass":
                radius = st.slider("Cutoff Radius", 5, min(crow, ccol), 30)
                # Create circular mask
                center = [crow, ccol]
                x, y = np.ogrid[:rows, :cols]
                mask_area = (x - center[0])**2 + (y - center[1])**2 > radius**2
                mask[mask_area] = 0
                
            elif filter_type == "High Pass":
                radius = st.slider("Cutoff Radius", 5, min(crow, ccol), 50)
                # Create circular mask (inverted from low pass)
                center = [crow, ccol]
                x, y = np.ogrid[:rows, :cols]
                mask_area = (x - center[0])**2 + (y - center[1])**2 <= radius**2
                mask[mask_area] = 0
                
            elif filter_type == "Band Pass":
                inner_radius = st.slider("Inner Radius", 5, min(crow, ccol) - 10, 20)
                outer_radius = st.slider("Outer Radius", inner_radius + 5, min(crow, ccol), 50)
                # Create band mask
                center = [crow, ccol]
                x, y = np.ogrid[:rows, :cols]
                mask_area1 = (x - center[0])**2 + (y - center[1])**2 <= inner_radius**2
                mask_area2 = (x - center[0])**2 + (y - center[1])**2 > outer_radius**2
                mask[mask_area1] = 0
                mask[mask_area2] = 0
            
            # Apply mask to frequency domain
            fshift_filtered = fshift * mask
            
            # Compute inverse FFT
            f_ishift = np.fft.ifftshift(fshift_filtered)
            img_back = np.fft.ifft2(f_ishift)
            img_back = np.abs(img_back)
            img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Show filtered image
            image_comparison(
                img1=Image.fromarray(gray_image), 
                img2=Image.fromarray(img_back), 
                label1="Original", 
                label2=f"{filter_type} Filtered"
            )
            
            # Show filter mask
            mask_display = mask * 255
            
            # Add download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                buf = io.BytesIO()
                Image.fromarray(img_back).save(buf, format="JPEG")
                buf.seek(0)
                st.download_button(
                    label=f"Download {filter_type} Filtered",
                    data=buf.getvalue(),
                    file_name=f"{filter_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                    mime="image/jpeg"
                )
            
            with col2:
                buf = io.BytesIO()
                plt.imsave(buf, magnitude_spectrum, cmap='viridis', format='png')
                buf.seek(0)
                st.download_button(
                    label="Download FFT Spectrum",
                    data=buf.getvalue(),
                    file_name=f"fft_spectrum_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )

    elif feature == "Pixel Inspector":

        image_rgb = image.convert("RGB")
        image_np = np.array(image_rgb)

        coords = streamlit_image_coordinates(image_rgb, key="pixel-inspect")

        if coords is not None:
            x, y = coords["x"], coords["y"]
            if 0 <= y < image_np.shape[0] and 0 <= x < image_np.shape[1]:
                r, g, b = image_np[y, x]
                st.success(f"Coordinates: ({x}, {y}) — RGB: ({r}, {g}, {b})")
                st.color_picker("Pixel Color", value=f'#{r:02x}{g:02x}{b:02x}'.upper(), label_visibility="collapsed")
            else:
                st.warning("Clicked outside the image.")
        else:
            st.info("Click on the image to inspect a pixel.")
