# 🩺 Healthcare AI Chatbot

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Model](https://img.shields.io/badge/AI_Model-Gemini_2.0_Flash-4285F4.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An intelligent, empathetic, and safe AI-powered **Healthcare Assistant** built using **Google Gemini 2.0 Flash** and **Streamlit**. Provides general medical guidance, health & wellness tips, symptom information, and emergency guidelines with interactive Web UI and CLI support.

---

## ✨ Features

- 💬 **Interactive Dual Interface**:
  - **Streamlit Web Application**: Modern dark glassmorphism dashboard with medical theme, pill shortcuts, and real-time streaming chat.
  - **Terminal CLI**: Lightweight interactive command-line interface with formatted markdown output.
- 🛡️ **Built-in Medical Safety System**: System prompt tailored to mandate clear medical disclaimers and emergency alert redirects (911/112/108).
- 🔑 **Secure Environment Configuration**: Flexible API key loading via `.env` environment variables using `python-dotenv`.
- 🧠 **Context-Aware Chat History**: Retains conversational context across back-and-forth medical questions with one-click chat history clearing.
- 💡 **Quick Prompt Pills**: One-click quick actions for diet tips, sleep hygiene, symptom comparison (cold vs flu), and safe medication storage.

---

## 📁 Repository Structure

```text
Healthcare-Chatbot/
├── Healthcarechatbot.py  # Interactive CLI script & core AI logic
├── app.py                # Streamlit Web Application interface
├── requirements.txt      # Project Python dependencies
├── .env.example          # Template for environment configuration
├── .gitignore            # Ignored files (securing .env and caches)
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.10 or higher** installed on your system.
- A **Google Gemini API Key** (Get one for free at [Google AI Studio](https://aistudio.google.com/)).

### 2. Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Omkar4812x/Healthcare-Chatbot.git
   cd Healthcare-Chatbot
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your API key:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and set your key:
     ```env
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     ```

---

## 💻 Usage

### Launch the Streamlit Web Application

To start the interactive web interface:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### Launch the Terminal CLI

To run the chatbot in your terminal:
```bash
python Healthcarechatbot.py
```
- Type `/clear` to reset chat history.
- Type `exit` or `quit` to exit.

---

## ⚠️ Important Safety Disclaimer

> **DISCLAIMER**: Healthcare AI Chatbot is an artificial intelligence assistant created for general educational and informational purposes only. It is **NOT** a medical doctor and does not provide professional medical diagnosis, treatment, or clinical advice.
> If you or someone you know is experiencing a life-threatening medical emergency (such as severe chest pain, stroke symptoms, or severe bleeding), call your local emergency services (e.g. 911, 112, 108) immediately.

---

## 📄 License & Attribution

Developed and maintained by [Omkar Bhandalkar](https://github.com/Omkar4812x). Open source under the MIT License.
