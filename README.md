<p align="center">
  <img src="assets/logo.png" width="140" height="140" alt="APIScout Studio Logo" />
</p>

<h1 align="center">🔍 APIScout Studio</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Version-v2.0.0-0284c7?style=for-the-badge" alt="Version" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
  <img src="https://img.shields.io/badge/Standalone-.EXE-22c55e?style=for-the-badge" alt="Executable" />
  <img src="https://img.shields.io/badge/MultiThreaded-Async-10b981?style=for-the-badge" alt="Async" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <b>APIScout Studio</b> is a standalone, lightweight, multi-language desktop application for AI developers and researchers. Instantly validate API keys, scan accessible model endpoints across <b>9 major AI providers</b>, and test models side-by-side in an interactive multi-tab <b>AI Playground</b>—without requiring Python or external dependencies.
</p>

---

## 🚀 What's New in v2.0 (Studio Edition)

- 💬 **Multi-Tab AI Playground:** Open unlimited side-by-side chat tabs across different providers and models to compare responses in real time.
- 🎛️ **Granular Inference Controls:** Customize the **System Prompt**, **Temperature** (`0.0 – 2.0`), and **Max Tokens** independently for every Playground tab.
- 🔎 **Interactive Model Explorer:** Live search and instant substring filtering across hundreds of models. Double-click any model to immediately launch a Playground tab.
- 🌐 **Expanded Provider Support (9 Providers):** Added native support for **Anthropic Claude**, **DeepSeek**, **Mistral AI**, **xAI (Grok)**, and **Custom OpenAI-Compatible Endpoints** (Ollama, LM Studio, vLLM, Together AI) alongside **OpenAI**, **Google Gemini**, **OpenRouter**, and **Groq**.
- 🌓 **Modern Dark & Light Themes:** Built-in one-click theme switcher with a sleek slate/cyan dark studio palette and high-contrast light mode.
- 📥 **Export & Clipboard Tools:** Export scanned model lists (`.txt` / `.json`) and full chat transcripts (`.md` / `.json`), or copy model IDs and AI replies with a single click.
- ⚡ **Latency Telemetry:** Real-time response latency (`ms`) and character count tracking for both endpoint discovery and chat completions.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🌍 **Multi-Language UI** | Dynamically switch between **English**, **Turkish**, **Spanish**, and **French** without restarting. |
| 📦 **Zero Dependencies** | Pre-compiled standalone Windows executables (`.exe`). No Python installation required. |
| ⚡ **Asynchronous Workers** | Non-blocking background threads keep the UI smooth and responsive during model scans and LLM generation. |
| 🛡️ **Privacy & Security First** | API keys are stored strictly in volatile session memory—never written to disk or logged—with instant show/hide and clear controls. |
| 🖥️ **Dual Release Builds** | Choose between the **Lightweight Tkinter/TTK Edition** (fast startup, minimal size) or the **PyQt5 Desktop Edition** in GitHub Releases. |

---

## 🔌 Supported Providers & Endpoints

| Provider | Status | Discovery Endpoint | Playground Chat Endpoint |
| :--- | :---: | :--- | :--- |
| **OpenAI** | ✅ Active | `api.openai.com/v1/models` | `api.openai.com/v1/chat/completions` |
| **Google Gemini** | ✅ Active | `generativelanguage.googleapis.com/v1beta/models` | `.../v1beta/models/{model}:generateContent` |
| **Anthropic Claude** | ✅ Active | `api.anthropic.com/v1/models` | `api.anthropic.com/v1/messages` |
| **OpenRouter** | ✅ Active | `openrouter.ai/api/v1/models` | `openrouter.ai/api/v1/chat/completions` |
| **Groq** | ✅ Active | `api.groq.com/openai/v1/models` | `api.groq.com/openai/v1/chat/completions` |
| **DeepSeek** | ✅ Active | `api.deepseek.com/models` | `api.deepseek.com/chat/completions` |
| **Mistral AI** | ✅ Active | `api.mistral.ai/v1/models` | `api.mistral.ai/v1/chat/completions` |
| **xAI (Grok)** | ✅ Active | `api.x.ai/v1/models` | `api.x.ai/v1/chat/completions` |
| **Custom (OpenAI-Compatible)** | ✅ Active | `{base_url}/models` (e.g. Ollama / LM Studio) | `{base_url}/chat/completions` |

---

## 🆚 Release Editions Comparison

Starting with **v2.0.0**, each GitHub Release provides two standalone `.exe` builds so you can pick the edition that best fits your workflow:

| Aspect | `APIScout-Studio-Tkinter.exe` (Recommended / Repo Default) | `APIScout-Studio-PyQt5.exe` (Qt5 Desktop Edition) |
| :--- | :--- | :--- |
| **UI Framework** | Enhanced Python `tkinter` / `ttk` (`clam` engine) | `PyQt5` (`QtWidgets` + custom QSS stylesheets) |
| **Executable Size** | **~16.4 MB** (Ultra-lightweight) | **~42.0 MB** (Includes Qt5 C++ runtime & DLLs) |
| **Cold Startup Speed** | **Instant (< 0.8s)** | Fast (~1.5s – 2.0s single-file extraction) |
| **RAM Footprint** | **~28 MB** | ~55 MB |
| **Visual Styling** | Flat modern slate/cyan studio theme (Dark & Light) | Rounded QSS cards, rich HTML chat viewer, native close buttons on tabs |
| **Core Features** | All 9 providers, async scan, live filter, multi-tab Playground, exports | Identical core engine, providers, translations, and Playground features |

---

## 🏗️ Architecture & Workflow

```text
  +-------------------------------------------------------------------+
  |                     APIScout Studio GUI                           |
  |  [API Config & Key Vault]  |  [Model Explorer]  |  [Playgrounds]  |
  +-------------+--------------+---------+----------+--------+--------+
                |                        |                   |
                v                        v                   v
  +-------------------------------------------------------------------+
  |                 Asynchronous Threading Dispatcher                 |
  +--------------------------------------+----------------------------+
                                         |
                                         v
  +-------------------------------------------------------------------+
  |                   Multi-Provider REST Engine                      |
  |   OpenAI / Gemini / Anthropic / OpenRouter / Groq / DeepSeek /    |
  |               Mistral / xAI / Custom Base URL                     |
  +-------------------------------------------------------------------+
```

---

## 🚀 Quick Start Guide

### Option 1: Download Standalone Executable (`.exe`)

1. Visit the [**Releases**](https://github.com/yigitozkan56/APIScout-Studio/releases) page on GitHub.
2. Download either:
   - `APIScout-Studio-Tkinter.exe` *(Lightweight & fast startup — Recommended)*
   - `APIScout-Studio-PyQt5.exe` *(Rich Qt5 widget styling)*
3. Double-click the downloaded `.exe` file to launch **APIScout Studio** immediately.

### Option 2: Run from Source

```bash
git clone https://github.com/yigitozkan56/APIScout-Studio.git
cd APIScout-Studio
pip install -r requirements.txt
python "APIScout Studio.py"
```

---

## 📖 Usage Instructions

1. **Select Language & Theme:** Choose your preferred language (**English**, **Türkçe**, **Español**, **Français**) and toggle between **Dark** or **Light** mode in the top header bar.
2. **Configure Provider:** Select an AI Provider from the dropdown. *(If using a local server like Ollama or LM Studio, select `Custom (OpenAI-Compatible)` and set your Base URL).*
3. **Scan Models:** Enter your API Key and click **Scan Models** (or press `Enter`). Available models and response latency will appear in the Model Explorer.
4. **Filter & Launch Playground:** Use the **Filter** input to narrow down models, then **double-click** any model (or click **+ Open Playground**) to start a chat session in a new tab.
5. **Experiment & Export:** Adjust the System Prompt, Temperature, and Max Tokens at the top of any Playground tab, and export your conversation to Markdown (`.md`) or JSON (`.json`) anytime.

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.
