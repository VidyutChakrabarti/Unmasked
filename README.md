## Unmasked

Unmasked is a comprehensive application for detecting deepfake videos, validating news authenticity, and tracking suspicious user activity. It leverages advanced AI models and agentic solutions to provide robust tools for digital forensics, media verification, and cyber investigation.

### Features

- **Deepfake Detection:**  
  Upload a video to determine if it is real or fake using a trained deep learning model.

- **Fake News Validation:**  
  Enter a news article URL to check its authenticity using AI-powered fact-checking and cross-referencing with trusted sources.

- **User Tracking:**  
  Generate a tracking link to monitor user location and activity via a Flask server and Ngrok tunnel.

- **Interactive Dashboard:**  
  Modern, responsive interface with carousels, video previews, and real-time logs.

  ### Gallery:

![Demo](gallery.gif)

### Requirements

- Python 3.8 or higher
- [Streamlit](https://streamlit.io/)
- [Flask](https://flask.palletsprojects.com/)
- [Ngrok](https://ngrok.com/) (Python package: `pyngrok`)
- TensorFlow
- OpenAI Python SDK
- dlib, OpenCV, numpy, pandas, requests, beautifulsoup4, lxml, regex, streamlit-extras

Install all dependencies using:

```sh
pip install -r requirements.txt
```

> **Note:**  
> You may need to install system dependencies for `dlib` and `opencv-python` depending on your OS.

## Project Structure

```
.
├── app.py
├── unmasked.py
├── pages/
│   ├── deepfake.py
│   ├── fakenews.py
│   └── track.py
├── Model/
│   └── deepfake_detection_model.h5
├── style.css
├── style2.css
├── news_slider.html
├── placeholder_image.png
├── aibot.png
├── logo.jpg
├── gallery.gif
├── .streamlit/
│   └── config.toml
├── .gitignore
├── .gitattributes
└── README.md
```

### How to Run

1. **Clone the repository and navigate to the project directory:**

    ```sh
    git clone <repository-url>
    cd Unmasked
    ```

2. **Install all required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Ensure the deepfake detection model file is present:**

    - Place `deepfake_detection_model.h5` in the `Model` directory.

4. **Start the application:**

    - On Windows, you can use the provided batch script:

        ```sh
        startapp.bat
        ```

    - Or manually run Streamlit:

        ```sh
        streamlit run unmasked.py
        ```

5. **Access the application:**

    - Open your browser and go to the local Streamlit URL (typically `http://localhost:8501`).

6. **Using the Features:**

    - **Deepfake Detection:**  
      Navigate to the Deepfake page and upload a video file (MP4 format, max 10MB).

    - **Fake News Validation:**  
      Go to the News Validator page and enter a news article URL.

    - **User Tracking:**  
      Use the Track page to start the Flask server and generate a tracking link. Share the link to monitor user activity.

### Configuration
- The application uses `.streamlit/config.toml` for Streamlit settings.
- API keys (such as for OpenAI or DeepSeek) should be set in the relevant Python files or via environment variables.

### Notes
- For the tracking feature, Ngrok is used to expose the local Flask server to the internet.
- The news carousel uses NewsAPI; you may need to provide your own API key in `news_slider.html`.
- The application is intended for research and educational purposes. Use tracking features responsibly and in compliance with applicable laws.