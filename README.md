## Unmasked

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-v1.0-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

Unmasked is a next-generation digital forensics toolkit for detecting deepfake videos, validating news authenticity, and monitoring suspicious user activity. Powered by state-of-the-art AI models and seamless integrations, Unmasked empowers journalists, researchers, and cybersecurity professionals to verify digital content with confidence.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Demo Gallery](#demo-gallery)
3. [Installation](#installation)
4. [Usage](#usage)

   * [Deepfake Detection](#deepfake-detection)
   * [Fake News Validation](#fake-news-validation)
   * [User Activity Tracking](#user-activity-tracking)
5. [Project Structure](#project-structure)
6. [Configuration](#configuration)
7. [Contributing](#contributing)
8. [License](#license)

---

## Key Features

* **Deepfake Detection**
  Upload videos (MP4, ≤10MB) to analyze authenticity using a custom TensorFlow deep learning model.

* **Fake News Validation**
  Validate news articles via AI-driven fact-checking, cross-referencing with trusted outlets.

* **User Activity Tracking**
  Generate secure tracking links (via Flask + Ngrok) to monitor location and interaction logs in real-time.

* **Interactive Dashboard**
  Responsive Streamlit interface with carousels, video previews, and live logs.

* **Modular & Extensible**
  Add custom modules or integrate external APIs with minimal effort.

---

## Demo Gallery

![Demo](gallery.gif)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/VidyutChakrabarti/Unmasked.git
   cd Unmasked
   ```
2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```
3. **Install system prerequisites**

   * For **dlib** and **opencv-python**, follow your OS-specific install guides.
   * Ensure `ffmpeg` is available in your `PATH` for video processing.

---

## Usage

### Deepfake Detection

1. Place the model file in `Model/deepfake_detection_model.h5`.
2. Run the app:

   ```bash
   streamlit run unmasked.py
   ```
3. Navigate to **Deepfake** page, upload your video, and view results.

### Fake News Validation

1. Go to **News Validator** page.
2. Enter the article URL and submit.
3. Review AI-powered authenticity score and source comparisons.

### User Activity Tracking

1. Open **Track** page.
2. Start the Flask server and generate an Ngrok link:

   ```bash
   python app.py  # launches Flask & Ngrok
   ```
3. Share the link to collect activity logs securely.

---

## Project Structure

```plaintext
.
├── app.py                        # Entry point for tracking service
├── unmasked.py                   # Main Streamlit application
├── pages/                        # Streamlit multipage modules
│   ├── deepfake.py
│   ├── fakenews.py
│   └── track.py
├── Model/                        # Pretrained models
│   └── deepfake_detection_model.h5
├── assets/                       # Static assets (CSS, images)
│   ├── style.css
│   ├── style2.css
│   ├── placeholder_image.png
│   ├── aibot.png
│   └── logo.jpg
├── news_slider.html              # News carousel template
├── gallery.gif                   # Demo animation
├── requirements.txt              # Python dependencies
├── .streamlit/config.toml        # Streamlit settings
├── .gitignore
└── README.md
```

---

## Configuration

* **API Keys**: Store sensitive keys (OpenAI, NewsAPI) as environment variables:

  ```bash
  export OPENAI_API_KEY="your_key"
  export NEWSAPI_KEY="your_key"
  ```
* **Streamlit settings**: Customize in `.streamlit/config.toml`.

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
