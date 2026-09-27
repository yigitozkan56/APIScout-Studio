# 🔍 APIScout

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
  <img src="https://img.shields.io/badge/Standalone-.EXE-green?style=for-the-badge" alt="Executable" />
  <img src="https://img.shields.io/badge/MultiThreaded-Async-brightgreen?style=for-the-badge" alt="Async" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <b>APIScout</b> is a standalone, lightweight, and multi-language desktop application for AI developers and researchers. It instantly validates API keys and scans available model endpoints across major AI providers without requiring Python or any external dependencies.
</p>

---

## 🎬 Live Demo

<img width="500" height="430" alt="Ekran görüntüsü 2026-09-27 121218" src="https://github.com/user-attachments/assets/0ef48ab2-b69b-4b94-a2b7-ea5c88c07f5d" />

<img width="500" height="430" alt="Ekran görüntüsü 2026-09-27 121411" src="https://github.com/user-attachments/assets/bcf19e36-6166-400e-ad3b-03e3f91ff7a3" />

<img width="1000" height="860" alt="Ekran Kaydı 2026-09-27 123305" src="https://github.com/user-attachments/assets/183278f9-2f98-480d-a942-e9b92fd74253" />

---

## 💡 Why APIScout?

Managing multiple AI service providers often requires testing API key validity, scope permissions, and checking accessible model versions. **APIScout** combines this process into a single executable application, eliminating the need for terminal commands, Python environments, or manual API calls.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🌐 **Multi-Language UI** | Switch dynamically between **English**, **Turkish**, **Spanish**, and **French** without restarting. |
| 🚀 **Zero Dependencies** | Pre-compiled standalone executable (.exe). No Python installation required. |
| ⚡ **Asynchronous Threading** | Non-blocking background workers keep the interface smooth and responsive during API calls. |
| 🛡️ **Privacy & Security First** | API keys are held strictly in local memory, never logged or saved, and auto-cleared upon provider switch or exit. |

---

## 🔌 Supported Providers & Endpoints

| Provider | Status | Base Endpoint |
| :--- | :---: | :--- |
| **OpenAI** | ✅ Active | api.openai.com/v1/models |
| **Google Gemini** | ✅ Active | generativelanguage.googleapis.com |
| **OpenRouter** | ✅ Active | openrouter.ai/api/v1/models |
| **Groq** | ✅ Active | api.groq.com/openai/v1/models |

---

## 🏗️ Architecture & Workflow

```text
  +-------------------+
  |   User Dashboard  |  (Desktop GUI)
  +---------+---------+
            |
            v
  +-------------------+
  |  Async Dispatcher |  (Background Worker)
  +---------+---------+
            |
            v
  +-------------------+      GET Request
  |   REST Provider   | ------------------->  OpenAI / Gemini /
  |      Engines      | <-------------------  OpenRouter / Groq
  +-------------------+     JSON Response
```

---

## 🚀 Quick Start Guide

### Download & Run (.exe)

1. Go to the Releases section on GitHub.
2. Download the latest version of `APIScout.exe`.
3. Double-click `APIScout.exe` to launch the application immediately.

---

## 📖 Usage Instructions

1. Select your preferred **Language** and **AI Provider** from the header dropdowns.
2. Input your **API Key** into the entry field.
3. Click **Scan Models** to initialize the scan.
4. Browse the numbered list of active models available for your account.

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
