# Gemini Bookmark Extension

## Overview

This Chrome extension allows you to select text or capture a portion of your screen on any webpage and get an analysis from Google's Gemini model. The analysis is displayed in a convenient sidebar, providing insights, summaries, or further information related to your selection.

## Features

- **Text Analysis:** Select any text on a webpage to send it for analysis.
- **Screen Capture Analysis:** Capture a specific area of the screen for image-based analysis.
- **Sidebar Interface:** All interactions and results are handled in a clean, accessible sidebar.
- **Model Selection:** Choose from different Gemini models for tailored results.

## Getting Started

Follow these instructions to set up and use the Gemini Bookmark Extension.

### Prerequisites

- Python 3.7+
- Google Chrome
- A Google Gemini API Key

### Backend Setup

1.  **Navigate to the Backend Directory:**
    ```bash
    cd backend
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Your API Key:**
    Place your Google Gemini API key into the `gemini.md` file in the root directory. The file should contain only your API key.



4.  **Run the Backend Server:**
    ```bash
    python main.py
    ```
    The server will start on `localhost:8000`.

### Frontend Setup (Chrome Extension)

1.  **Open Chrome Extensions:**
    Navigate to `chrome://extensions/` in your Chrome browser.

2.  **Enable Developer Mode:**
    Turn on the "Developer mode" toggle in the top right corner.

3.  **Load the Extension:**
    - Click on "Load unpacked".
    - Select the `extension` folder from the project directory.

4.  **Pin the Extension:**
    Click the puzzle piece icon in the Chrome toolbar and pin the Gemini Bookmark Extension for easy access.

## How to Use

1.  **Open the Sidebar:**
    Click the extension icon in your toolbar to open the sidebar on any webpage.

2.  **For Text Analysis:**
    - Select a piece of text on the page.
    - The selected text will automatically appear in the sidebar, and the analysis will begin.

3.  **For Image Analysis:**
    - Click the "Capture Screen" button in the sidebar.
    - Your cursor will turn into a crosshair. Click and drag to select a region of the screen.
    - The analysis of the captured image will appear in the sidebar.
