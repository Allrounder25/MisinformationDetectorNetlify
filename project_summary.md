# Project Summary: Gemini Bookmark Extension

## Introduction

The Gemini Bookmark Extension is a productivity tool designed to integrate the power of Google's Gemini models directly into the user's browsing experience. It provides on-demand text and image analysis for content on any webpage, presenting the results in an intuitive sidebar interface. This tool is built for students, researchers, and anyone looking to gain deeper insights into web content without disrupting their workflow.

## Core Functionality

The extension's primary function is to act as a seamless bridge between the user's web browsing and the analytical capabilities of the Gemini API. It allows for two main types of analysis:

1.  **Text Analysis:** Users can highlight any text on a webpage. The extension automatically captures this text and sends it to the backend for processing by a selected Gemini model. The model's response is then streamed back to the user in the sidebar.

2.  **Image Analysis:** Users can initiate a screen capture mode, allowing them to select a specific rectangular area of the webpage. This captured image is sent to the backend for analysis by a multimodal Gemini model, which can understand and interpret the visual content.

## Features

- **Context-Aware Analysis:** The extension sends the URL of the source page along with the selected text or image, providing the model with context for more accurate and relevant results.
- **Real-time Streaming:** For text analysis, the response from the Gemini model is streamed back to the sidebar, allowing users to see the results as they are being generated.
- **Dynamic Model Selection:** Users can switch between different Gemini models via a dropdown menu in the sidebar, enabling them to choose the best model for their specific task (e.g., choosing between `gemini-2.5-pro` for deep analysis or `gemini-2.5-flash-lite` for quick text analysis, while `gemini-1.5-flash` is used for image analysis).
- **Intuitive UI:** The extension features a clean and user-friendly sidebar that displays the analysis results, loading states, and error messages in a clear and organized manner.
- **Screen Capture Tool:** A built-in screen capture utility allows for precise selection of on-page elements for visual analysis.
- **Asynchronous Backend:** The Python backend, built with FastAPI, handles requests asynchronously, ensuring that the application remains responsive even under load.

## Use Cases

- **Research and Learning:** Students and researchers can quickly summarize articles, define complex terms, or get explanations of diagrams and charts without leaving the page.
- **Content Creation:** Writers and content creators can use the extension to generate ideas, rephrase sentences, or gather information on a topic.
- **Web Development and Design:** Developers can capture UI elements to get feedback on design, accessibility, or even generate code snippets based on visual mockups.
- **Everyday Browsing:** General users can look up unfamiliar terms, get more information about images, or translate text on the fly.

## Technical Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **API:** Google Gemini API
- **Platform:** Chrome Extension framework
