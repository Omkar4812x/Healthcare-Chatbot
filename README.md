# 🩺 Healthcare AI Hub & Clinical Assistant

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![AI Model](https://img.shields.io/badge/AI_Model-Gemini_2.0_Flash-4285F4.svg)](https://aistudio.google.com/)
[![CI Status](https://img.shields.io/badge/CI-GitHub_Actions-success.svg)](.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An intelligent, multi-persona, and safe **Healthcare Assistant & Portal** powered by **Google Gemini 2.0 Flash** and **Streamlit**. Provides real-time health consultations, symptom triage guidance, interactive health metrics calculators (BMI, BMR/TDEE, Hydration, Heart Rate Zones), global emergency hotline directory, consultation transcript exports, medication tracker, and a rich CLI terminal interface.

---

## ✨ Features Breakdown

| Feature | Description |
| :--- | :--- |
| 💬 **AI Consultation Assistant** | Multi-persona (General, Triage, Nutrition, Caregiver/Seniors) chat with streaming responses and pill prompt shortcuts. |
| 📄 **Consultation Notes Exporter** | Export chat sessions to downloadable Markdown/TXT notes for medical records or doctor visit prep. |
| 📊 **Interactive Health Calculators** | **BMI**, **BMR & Daily Calories (TDEE)**, **Hydration Target**, and **Heart Rate Target Zones** (Karvonen method). |
| 🚨 **Global Emergency Directory** | Quick access to emergency contacts, poison control, and crisis lifelines for US, UK, EU, India, Canada, Australia. |
| 💊 **Medication Schedule Log** | Session-based personal medication logger with dosage, frequency, and administration notes. |
| 🖥️ **Rich Terminal CLI** | Interactive command-line chatbot formatted with `rich` panels, tables, Markdown rendering, `/sos`, `/export`, and `/clear`. |
| 🛡️ **Medical Safety System** | Custom system prompts enforcing medical disclaimers and emergency redirects. |
| ⚙️ **CI/CD & Automated Testing** | Unit test suite powered by `pytest` with automated GitHub Actions CI workflow. |

---

## 📁 Repository Structure

```text
Healthcare-Chatbot/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI workflow
├── .streamlit/
│   └── config.toml              # Dark emerald/cyan glassmorphism theme config
├── tests/
│   └── test_chatbot.py          # Pytest unit test suite
├── Healthcarechatbot.py         # Rich interactive CLI script & AI logic
├── app.py                       # Multi-tab Streamlit Web Application
├── requirements.txt             # Project Python dependencies
├── .env.example                 # Environment configuration template
├── .gitignore                   # Git ignore file (securing .env and caches)
├── LICENSE                      # MIT Open-Source License
└── README.md                    # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites

- **Python 3.10, 3.11, or 3.12** installed on your system.
- A **Google Gemini API Key** (Get a free API key at [Google AI Studio](https://aistudio.google.com/)).

### 2. Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Omkar4812x/Healthcare-Chatbot.git
   cd Healthcare-Chatbot
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # On Windows:
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variable:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and set your key:
     ```env
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     ```

---

## 💻 Usage Instructions

### Launch the Streamlit Web Application

To start the full-featured Web Portal:
```bash
streamlit run app.py
```
Open your web browser at `http://localhost:8501`.

### Launch the Terminal CLI Assistant

To run the interactive CLI in your terminal:
```bash
python Healthcarechatbot.py
```
Available CLI Shortcuts:
- `/help` : View available commands table
- `/sos` : View global emergency hotlines
- `/clear` : Reset active chat history
- `/export` : Export chat transcript to Markdown file
- `exit` or `quit` : Exit the chatbot

---

## 🧪 Running Unit Tests

Run the automated test suite with `pytest`:
```bash
pytest tests/ -v
```

---

## ☁️ Deployment

### Streamlit Community Cloud
1. Fork or push this repository to your GitHub account.
2. Visit [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repository, set the main file path to `app.py`.
4. Under **Advanced settings**, add `GEMINI_API_KEY = "your_key"` to **Secrets**.
5. Deploy!

---

## ⚠️ Important Safety Disclaimer

> **DISCLAIMER**: Healthcare AI Hub is an artificial intelligence assistant created for general educational and informational purposes only. It is **NOT** a medical doctor and does not provide professional medical diagnosis, treatment, or clinical advice.
> If you or someone you know is experiencing a life-threatening medical emergency (such as severe chest pain, stroke symptoms, or severe bleeding), call your local emergency services (e.g. 911, 112, 108) immediately.

---

## 📄 License & Attribution

Developed and maintained by [Omkar Bhandalkar](https://github.com/Omkar4812x). Open source under the [MIT License](LICENSE).
