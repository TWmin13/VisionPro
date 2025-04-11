# Vision Pro

**Vision Pro** is an intuitive computer vision application built for real-time image processing. It offers a rich suite of tools including webcam capture, OCR (Optical Character Recognition), color pop effects, live FFT visualization, pixel inspection, and advanced image filtering — all integrated into a sleek, black-themed Streamlit web app.

Link to the Website: https://visionpro13.streamlit.app

## Features

- 📸 **Webcam Support** — Capture and process live feed from your webcam.
- 🖼️ **Image Upload & Preview** — Drag-and-drop images or select from your files.
- 🧠 **OCR Integration** — Extract and display text from images.
- 🌈 **Color Pop Effect** — Highlight a specific color while desaturating the rest.
- 📊 **Live FFT Viewer** — Real-time frequency domain visualization.
- 🔍 **Pixel Inspector** — Click on a pixel to see its exact RGB and location.
- 🧪 **Advanced Filters** — Gaussian blur, edge detection, denoising, and more.
- 🖤 **Dark-Themed UI** — Modern and minimal interface designed with user experience in mind.
- 📥 **Download Results** — Export processed images in high quality.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- OpenCV
- NumPy
- Pillow
- pytesseract
- matplotlib

### Installation

git clone https://github.com/your-username/vision-pro.git
cd vision-pro

## 🛠️ Set Up the Environment

Ensure you have **Python 3.8+** installed. Then, install the required dependencies:

pip install -r requirements.txt

If you're using a virtual environment (recommended):

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt


## Run the App

streamlit run app.py

## 📁 Folder Structure

vision-pro/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # All Python dependencies
├── README.md             # Project documentation
├── packages.txt          # System packages to install (e.g., tesseract-ocr)    








