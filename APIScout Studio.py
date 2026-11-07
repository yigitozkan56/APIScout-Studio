"""
APIScout Studio v2.0.0 - Modern Tkinter/TTK Edition
A standalone, multi-language desktop studio for discovering, validating,
and testing AI models across major LLM providers in real time.
"""

import json
import os
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext, ttk
import requests


def resource_path(relative_path: str) -> str:
    """Resolve resource path for both development and PyInstaller standalone builds."""
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ==================== MULTI-LANGUAGE DICTIONARY ====================
TRANSLATIONS = {
    "en": {
        "title": "APIScout Studio v2.0",
        "subtitle": "AI Model Explorer & Multi-Provider Playground",
        "api_params": " API Configuration ",
        "provider": "Provider:",
        "base_url": "Base URL:",
        "api_key": "API Key:",
        "show_key": "Show",
        "hide_key": "Hide",
        "clear_key": "Clear",
        "scan_btn": "Scan Models",
        "scanning_btn": "Scanning...",
        "models_pg": " Model Explorer ",
        "initial_status": "Enter your API key and click Scan Models.",
        "search_placeholder": "Filter models (e.g. gpt-4, claude, flash)...",
        "search_lbl": "Filter:",
        "select_model_lbl": "Selected Model:",
        "double_click_hint": "Tip: Double-click any model to open a Playground tab",
        "open_pg_btn": "+ Open Playground",
        "copy_model_btn": "Copy ID",
        "export_models_btn": "Export List",
        "close_tab": "Close Tab",
        "warning_title": "Warning",
        "warning_key_msg": "Please enter a valid API Key first.",
        "warning_model_msg": "Please select a model from the list.",
        "scanning": "Scanning {provider} endpoints...",
        "success": "Found {count} models ({ms} ms)",
        "filtered_count": "Showing {shown} of {total} models",
        "error": "Scan failed!",
        "err_prefix": "ERROR: ",
        "invalid_key": "Invalid API Key (401 Unauthorized)",
        "err_code": "HTTP Error",
        "conn_err": "Connection Error",
        "unauthorized_or_invalid": "Invalid API Key or Unauthorized Access",
        "send_btn": "Send ↵",
        "sending_btn": "Thinking...",
        "you": "You",
        "system_error": "System Error",
        "info_lbl": "{provider}  •  {model}",
        "language": "Language:",
        "theme_dark": "🌙 Dark",
        "theme_light": "☀️ Light",
        "sys_prompt": "System Prompt:",
        "sys_prompt_default": "You are a helpful, accurate AI assistant.",
        "temp_lbl": "Temp:",
        "max_tokens_lbl": "Max Tokens:",
        "clear_chat": "Clear",
        "copy_last": "Copy Reply",
        "export_chat": "Export .MD",
        "copied_msg": "Copied to clipboard!",
        "exported_msg": "Saved successfully to:\n{path}",
        "welcome_title": "Welcome to APIScout Studio v2.0",
        "welcome_body": (
            "1. Choose an AI Provider on the left panel (OpenAI, Gemini, Anthropic, Groq, OpenRouter, DeepSeek, Mistral, xAI, or Custom).\n"
            "2. Enter your API Key and click 'Scan Models' to fetch accessible endpoints asynchronously.\n"
            "3. Search & filter models in real time, then double-click any model (or click '+ Open Playground') to start chatting.\n"
            "4. Compare multiple models side-by-side in separate tabs with custom System Prompts and Temperature controls."
        ),
        "input_hint": "Press Enter to send, Shift+Enter for new line",
        "latency_ info": "Response in {ms} ms  |  {chars} chars"
    },
    "tr": {
        "title": "APIScout Studio v2.0",
        "subtitle": "Yapay Zeka Model Tarayıcı & Çoklu Playground",
        "api_params": " API Yapılandırması ",
        "provider": "Sağlayıcı:",
        "base_url": "Base URL:",
        "api_key": "API Anahtarı:",
        "show_key": "Göster",
        "hide_key": "Gizle",
        "clear_key": "Temizle",
        "scan_btn": "Modelleri Tara",
        "scanning_btn": "Taranıyor...",
        "models_pg": " Model Gezgini ",
        "initial_status": "Lütfen API anahtarınızı girip 'Modelleri Tara'ya tıklayın.",
        "search_placeholder": "Model ara (örn. gpt-4, claude, flash)...",
        "search_lbl": "Filtrele:",
        "select_model_lbl": "Seçili Model:",
        "double_click_hint": "İpucu: Sohbet açmak için herhangi bir modele çift tıklayın",
        "open_pg_btn": "+ Playground Aç",
        "copy_model_btn": "ID Kopyala",
        "export_models_btn": "Listeyi Kaydet",
        "close_tab": "Sekmeyi Kapat",
        "warning_title": "Uyarı",
        "warning_key_msg": "Lütfen önce bir API Anahtarı girin.",
        "warning_model_msg": "Lütfen listeden bir model seçin.",
        "scanning": "{provider} uç noktaları taranıyor...",
        "success": "{count} model bulundu ({ms} ms)",
        "filtered_count": "{total} modelden {shown} tanesi gösteriliyor",
        "error": "Tarama başarısız!",
        "err_prefix": "HATA: ",
        "invalid_key": "Geçersiz API Anahtarı (401 Yetkisiz)",
        "err_code": "HTTP Hatası",
        "conn_err": "Bağlantı Hatası",
        "unauthorized_or_invalid": "Geçersiz API Anahtarı veya Yetkisiz Erişim",
        "send_btn": "Gönder ↵",
        "sending_btn": "Yanıtlanıyor...",
        "you": "Siz",
        "system_error": "Sistem Hatası",
        "info_lbl": "{provider}  •  {model}",
        "language": "Dil:",
        "theme_dark": "🌙 Koyu",
        "theme_light": "☀️ Açık",
        "sys_prompt": "Sistem Komutu:",
        "sys_prompt_default": "Yardımsever ve doğru bilgi veren bir yapay zeka asistanısın.",
        "temp_lbl": "Sıcaklık:",
        "max_tokens_lbl": "Maks Token:",
        "clear_chat": "Temizle",
        "copy_last": "Yanıtı Kopyala",
        "export_chat": ".MD Kaydet",
        "copied_msg": "Panoya kopyalandı!",
        "exported_msg": "Başarıyla kaydedildi:\n{path}",
        "welcome_title": "APIScout Studio v2.0'a Hoş Geldiniz",
        "welcome_body": (
            "1. Sol panelden bir Yapay Zeka Sağlayıcısı seçin (OpenAI, Gemini, Anthropic, Groq, OpenRouter, DeepSeek, Mistral, xAI veya Özel).\n"
            "2. API Anahtarınızı girin ve erişilebilir modelleri asenkron olarak taramak için 'Modelleri Tara'ya tıklayın.\n"
            "3. Modelleri anlık olarak filtreleyin; sohbet başlatmak için bir modele çift tıklayın veya '+ Playground Aç' butonunu kullanın.\n"
            "4. Farklı sekmelerde birden fazla modeli özel Sistem Komutu ve Sıcaklık (Temperature) ayarlarıyla test edin."
        ),
        "input_hint": "Göndermek için Enter, yeni satır için Shift+Enter",
        "latency_ info": "{ms} ms içinde yanıtlandı  |  {chars} karakter"
    },
    "es": {
        "title": "APIScout Studio v2.0",
        "subtitle": "Explorador de Modelos IA y Playground Multi-Proveedor",
        "api_params": " Configuración de API ",
        "provider": "Proveedor:",
        "base_url": "URL Base:",
        "api_key": "Clave API:",
        "show_key": "Mostrar",
        "hide_key": "Ocultar",
        "clear_key": "Limpiar",
        "scan_btn": "Escanear Modelos",
        "scanning_btn": "Escaneando...",
        "models_pg": " Explorador de Modelos ",
        "initial_status": "Ingrese su clave API y haga clic en Escanear Modelos.",
        "search_placeholder": "Filtrar modelos...",
        "search_lbl": "Filtrar:",
        "select_model_lbl": "Modelo Seleccionado:",
        "double_click_hint": "Consejo: Doble clic en un modelo para abrir Playground",
        "open_pg_btn": "+ Abrir Playground",
        "copy_model_btn": "Copiar ID",
        "export_models_btn": "Exportar Lista",
        "close_tab": "Cerrar Pestaña",
        "warning_title": "Advertencia",
        "warning_key_msg": "Por favor, ingrese una clave API válida.",
        "warning_model_msg": "Por favor, seleccione un modelo de la lista.",
        "scanning": "Escaneando endpoints de {provider}...",
        "success": "¡{count} modelos encontrados ({ms} ms)!",
        "filtered_count": "Mostrando {shown} de {total} modelos",
        "error": "¡Error al escanear!",
        "err_prefix": "ERROR: ",
        "invalid_key": "Clave API no válida (401 No autorizado)",
        "err_code": "Código de Error",
        "conn_err": "Error de conexión",
        "unauthorized_or_invalid": "Clave API no válida o acceso no autorizado",
        "send_btn": "Enviar ↵",
        "sending_btn": "Pensando...",
        "you": "Tú",
        "system_error": "Error del Sistema",
        "info_lbl": "{provider}  •  {model}",
        "language": "Idioma:",
        "theme_dark": "🌙 Oscuro",
        "theme_light": "☀️ Claro",
        "sys_prompt": "Prompt del Sistema:",
        "sys_prompt_default": "Eres un asistente de IA útil y preciso.",
        "temp_lbl": "Temp:",
        "max_tokens_lbl": "Máx Tokens:",
        "clear_chat": "Limpiar",
        "copy_last": "Copiar Respuesta",
        "export_chat": "Exportar .MD",
        "copied_msg": "¡Copiado al portapapeles!",
        "exported_msg": "Guardado exitosamente en:\n{path}",
        "welcome_title": "Bienvenido a APIScout Studio v2.0",
        "welcome_body": (
            "1. Seleccione un proveedor de IA en el panel izquierdo.\n"
            "2. Ingrese su Clave API y presione 'Escanear Modelos'.\n"
            "3. Filtre modelos en tiempo real y haga doble clic en cualquiera para abrir un Playground.\n"
            "4. Pruebe múltiples modelos en pestañas separadas con configuración personalizada."
        ),
        "input_hint": "Presione Enter para enviar, Shift+Enter para nueva línea",
        "latency_ info": "Respuesta en {ms} ms  |  {chars} caracteres"
    },
    "fr": {
        "title": "APIScout Studio v2.0",
        "subtitle": "Explorateur de Modèles IA & Playground Multi-Fournisseurs",
        "api_params": " Paramètres API ",
        "provider": "Fournisseur:",
        "base_url": "URL de Base:",
        "api_key": "Clé API:",
        "show_key": "Afficher",
        "hide_key": "Masquer",
        "clear_key": "Effacer",
        "scan_btn": "Analyser les Modèles",
        "scanning_btn": "Analyse...",
        "models_pg": " Explorateur de Modèles ",
        "initial_status": "Entrez votre clé API et cliquez sur Analyser.",
        "search_placeholder": "Filtrer les modèles...",
        "search_lbl": "Filtrer:",
        "select_model_lbl": "Modèle Sélectionné:",
        "double_click_hint": "Astuce: Double-cliquez sur un modèle pour ouvrir un Playground",
        "open_pg_btn": "+ Ouvrir Playground",
        "copy_model_btn": "Copier ID",
        "export_models_btn": "Exporter Liste",
        "close_tab": "Fermer l'Onglet",
        "warning_title": "Avertissement",
        "warning_key_msg": "Veuillez entrer une clé API valide.",
        "warning_model_msg": "Veuillez sélectionner un modèle.",
        "scanning": "Analyse des endpoints {provider}...",
        "success": "{count} modèles trouvés ({ms} ms)",
        "filtered_count": "Affichage de {shown} sur {total} modèles",
        "error": "Échec de l'analyse !",
        "err_prefix": "ERREUR: ",
        "invalid_key": "Clé API invalide (401 Non autorisé)",
        "err_code": "Erreur HTTP",
        "conn_err": "Erreur de connexion",
        "unauthorized_or_invalid": "Clé API invalide ou accès non autorisé",
        "send_btn": "Envoyer ↵",
        "sending_btn": "Réflexion...",
        "you": "Vous",
        "system_error": "Erreur Système",
        "info_lbl": "{provider}  •  {model}",
        "language": "Langue:",
        "theme_dark": "🌙 Sombre",
        "theme_light": "☀️ Clair",
        "sys_prompt": "Prompt Système:",
        "sys_prompt_default": "Vous êtes un assistant IA utile et précis.",
        "temp_lbl": "Temp:",
        "max_tokens_lbl": "Tokens Max:",
        "clear_chat": "Effacer",
        "copy_last": "Copier Réponse",
        "export_chat": "Exporter .MD",
        "copied_msg": "Copié dans le presse-papiers !",
        "exported_msg": "Enregistré avec succès :\n{path}",
        "welcome_title": "Bienvenue sur APIScout Studio v2.0",
        "welcome_body": (
            "1. Choisissez un fournisseur d'IA dans le panneau de gauche.\n"
            "2. Entrez votre clé API et cliquez sur 'Analyser les Modèles'.\n"
            "3. Filtrez les modèles en temps réel et double-cliquez sur un modèle pour discuter.\n"
            "4. Comparez plusieurs modèles dans des onglets séparés."
        ),
        "input_hint": "Entrée pour envoyer, Maj+Entrée pour nouvelle ligne",
        "latency_ info": "Réponse en {ms} ms  |  {chars} caractères"
    }
}


# ==================== PROVIDER ENDPOINT CONFIGURATIONS ====================
PROVIDER_CONFIGS = {
    "OpenAI": {
        "type": "openai",
        "models_url": "https://api.openai.com/v1/models",
        "chat_url": "https://api.openai.com/v1/chat/completions"
    },
    "Google Gemini": {
        "type": "gemini",
        "models_url": "https://generativelanguage.googleapis.com/v1beta/models",
        "chat_url": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    },
    "Anthropic Claude": {
        "type": "anthropic",
        "models_url": "https://api.anthropic.com/v1/models",
        "chat_url": "https://api.anthropic.com/v1/messages"
    },
    "OpenRouter": {
        "type": "openai",
        "models_url": "https://openrouter.ai/api/v1/models",
        "chat_url": "https://openrouter.ai/api/v1/chat/completions"
    },
    "Groq": {
        "type": "openai",
        "models_url": "https://api.groq.com/openai/v1/models",
        "chat_url": "https://api.groq.com/openai/v1/chat/completions"
    },
    "DeepSeek": {
        "type": "openai",
        "models_url": "https://api.deepseek.com/models",
        "chat_url": "https://api.deepseek.com/chat/completions"
    },
    "Mistral AI": {
        "type": "openai",
        "models_url": "https://api.mistral.ai/v1/models",
        "chat_url": "https://api.mistral.ai/v1/chat/completions"
    },
    "xAI (Grok)": {
        "type": "openai",
        "models_url": "https://api.x.ai/v1/models",
        "chat_url": "https://api.x.ai/v1/chat/completions"
    },
    "Custom (OpenAI-Compatible)": {
        "type": "openai_custom",
        "models_url": "{base_url}/models",
        "chat_url": "{base_url}/chat/completions"
    }
}


# ==================== API SCANNING ENGINE ====================
def scan_provider_models(provider: str, api_key: str, lang: str = "en", custom_base_url: str = ""):
    """Fetch available models for the selected provider and return (success, models_or_error, elapsed_ms)."""
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    cfg = PROVIDER_CONFIGS.get(provider, PROVIDER_CONFIGS["OpenAI"])
    ptype = cfg["type"]
    start_ts = time.perf_counter()

    try:
        if ptype in ("openai", "openai_custom"):
            if ptype == "openai_custom":
                base = custom_base_url.strip().rstrip("/") or "http://localhost:11434/v1"
                url = f"{base}/models"
            else:
                url = cfg["models_url"]
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            response = requests.get(url, headers=headers, timeout=12)
            elapsed_ms = int((time.perf_counter() - start_ts) * 1000)

            if response.status_code == 200:
                data = response.json()
                raw_list = data.get("data", data if isinstance(data, list) else [])
                models = sorted({str(item.get("id", item)) for item in raw_list if item})
                return True, models, elapsed_ms
            elif response.status_code in (401, 403):
                return False, t["invalid_key"], elapsed_ms
            else:
                return False, f"{t['err_code']} {response.status_code}: {response.text[:300]}", elapsed_ms

        elif ptype == "gemini":
            url = f"{cfg['models_url']}?key={api_key}"
            response = requests.get(url, timeout=12)
            elapsed_ms = int((time.perf_counter() - start_ts) * 1000)

            if response.status_code == 200:
                data = response.json()
                raw_models = data.get("models", [])
                models = sorted([
                    m["name"].replace("models/", "")
                    for m in raw_models
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                ])
                if not models:
                    models = sorted([m["name"].replace("models/", "") for m in raw_models])
                return True, models, elapsed_ms
            elif response.status_code in (400, 401, 403):
                return False, t["unauthorized_or_invalid"], elapsed_ms
            else:
                return False, f"{t['err_code']} {response.status_code}: {response.text[:300]}", elapsed_ms

        elif ptype == "anthropic":
            url = cfg["models_url"]
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }
            response = requests.get(url, headers=headers, timeout=12)
            elapsed_ms = int((time.perf_counter() - start_ts) * 1000)

            if response.status_code == 200:
                data = response.json()
                models = sorted([item["id"] for item in data.get("data", []) if "id" in item])
                return True, models, elapsed_ms
            elif response.status_code in (401, 403):
                return False, t["invalid_key"], elapsed_ms
            else:
                return False, f"{t['err_code']} {response.status_code}: {response.text[:300]}", elapsed_ms

    except Exception as exc:
        elapsed_ms = int((time.perf_counter() - start_ts) * 1000)
        return False, f"{t['conn_err']}: {str(exc)}", elapsed_ms

    return False, "Unsupported provider", 0


# ==================== CHAT COMPLETION ENGINE ====================
def send_chat_message(
    provider: str,
    api_key: str,
    model: str,
    history: list,
    user_message: str,
    system_prompt: str = "",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    lang: str = "en",
    custom_base_url: str = ""
):
    """Send a chat completion request to the specified provider and return (success, reply_or_error, elapsed_ms)."""
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    cfg = PROVIDER_CONFIGS.get(provider, PROVIDER_CONFIGS["OpenAI"])
    ptype = cfg["type"]
    start_ts = time.perf_counter()

    try:
        if ptype in ("openai", "openai_custom"):
            if ptype == "openai_custom":
                base = custom_base_url.strip().rstrip("/") or "http://localhost:11434/v1"
                url = f"{base}/chat/completions"
            else:
                url = cfg["chat_url"]

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            messages = []
            if system_prompt.strip():
                messages.append({"role": "system", "content": system_prompt.strip()})
            for item in history:
                messages.append({"role": item["role"], "content": item["content"]})
            messages.append({"role": "user", "content": user_message})

            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            elapsed_ms = int((time.perf_counter() - start_ts) * 1000)

            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                return True, reply, elapsed_ms
            else:
                return False, f"{t['err_code']} ({response.status_code}): {response.text[:400]}", elapsed_ms

        elif ptype == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            contents = []
            for item in history:
                role = "user" if item["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": item["content"]}]})
            contents.append({"role": "user", "parts": [{"text": user_message}]})

            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens
                }
            }
            if system_prompt.strip():
                payload["systemInstruction"] = {"parts": [{"text": system_prompt.strip()}]}

            response = requests.post(url, headers=headers, json=payload, timeout=45)
            elapsed_ms = int((time.perf_counter() - start_ts) * 1000)

            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    reply = "".join(p.get("text", "") for p in parts)
                    return True, reply, elapsed_ms
                return False, f"Empty response: {json.dumps(data)[:300]}", elapsed_ms
            else:
                return False, f"{t['err_code']} ({response.status_code}): {response.text[:400]}", elapsed_ms

        elif ptype == "anthropic":
            url = cfg["chat_url"]
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            messages = []
            for item in history:
                messages.append({"role": item["role"], "content": item["content"]})
            messages.append({"role": "user", "content": user_message})

            payload = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }
            if system_prompt.strip():
                payload["system"] = system_prompt.strip()

            response = requests.post(url, headers=headers, json=payload, timeout=45)
            elapsed_ms = int((time.perf_counter() - start_ts) * 1000)

            if response.status_code == 200:
                data = response.json()
                blocks = data.get("content", [])
                reply = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
                return True, reply, elapsed_ms
            else:
                return False, f"{t['err_code']} ({response.status_code}): {response.text[:400]}", elapsed_ms

    except Exception as exc:
        elapsed_ms = int((time.perf_counter() - start_ts) * 1000)
        return False, f"{t['conn_err']}: {str(exc)}", elapsed_ms

    return False, "Unsupported provider", 0


# ==================== THEME PALETTES ====================
THEMES = {
    "dark": {
        "bg": "#0f172a",
        "panel": "#1e293b",
        "surface": "#0b1120",
        "input_bg": "#0f172a",
        "fg": "#f8fafc",
        "fg_muted": "#94a3b8",
        "accent": "#38bdf8",
        "accent_hover": "#0284c7",
        "border": "#334155",
        "user_tag": "#38bdf8",
        "ai_tag": "#4ade80",
        "err_tag": "#f87171",
        "success_fg": "#4ade80",
        "warn_fg": "#facc15",
        "select_bg": "#0284c7",
        "select_fg": "#ffffff"
    },
    "light": {
        "bg": "#f1f5f9",
        "panel": "#ffffff",
        "surface": "#f8fafc",
        "input_bg": "#ffffff",
        "fg": "#0f172a",
        "fg_muted": "#64748b",
        "accent": "#0284c7",
        "accent_hover": "#0369a1",
        "border": "#cbd5e1",
        "user_tag": "#0284c7",
        "ai_tag": "#16a34a",
        "err_tag": "#dc2626",
        "success_fg": "#16a34a",
        "warn_fg": "#ca8a04",
        "select_bg": "#0284c7",
        "select_fg": "#ffffff"
    }
}


# ==================== PLAYGROUND TAB COMPONENT ====================
class PlaygroundTab(ttk.Frame):
    def __init__(self, parent, provider: str, api_key: str, model: str, custom_base_url: str, app_instance):
        super().__init__(parent, style="Card.TFrame")
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.custom_base_url = custom_base_url
        self.app_instance = app_instance
        self.history = []
        self.last_reply = ""

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        t = TRANSLATIONS[self.app_instance.current_lang]

        # Top Header Bar
        self.header_frame = ttk.Frame(self, style="Card.TFrame", padding=(10, 8))
        self.header_frame.pack(fill="x")

        info_str = t["info_lbl"].format(provider=self.provider, model=self.model)
        self.lbl_info = ttk.Label(self.header_frame, text=info_str, style="AccentTitle.TLabel")
        self.lbl_info.pack(side="left")

        self.btn_close = ttk.Button(
            self.header_frame, text="✕", width=3,
            command=lambda: self.app_instance.close_specific_tab(self)
        )
        self.btn_close.pack(side="right", padx=(4, 0))

        self.btn_export = ttk.Button(self.header_frame, text=t["export_chat"], command=self.export_chat)
        self.btn_export.pack(side="right", padx=3)

        self.btn_copy = ttk.Button(self.header_frame, text=t["copy_last"], command=self.copy_last_reply)
        self.btn_copy.pack(side="right", padx=3)

        self.btn_clear = ttk.Button(self.header_frame, text=t["clear_chat"], command=self.clear_chat)
        self.btn_clear.pack(side="right", padx=3)

        # Parameters Bar (System Prompt + Temp + Max Tokens)
        self.params_bar = ttk.Frame(self, style="Card.TFrame", padding=(10, 2, 10, 6))
        self.params_bar.pack(fill="x")

        self.lbl_sys = ttk.Label(self.params_bar, text=t["sys_prompt"], style="Muted.TLabel")
        self.lbl_sys.pack(side="left", padx=(0, 5))

        self.sys_prompt_var = tk.StringVar(value=t["sys_prompt_default"])
        self.entry_sys = ttk.Entry(self.params_bar, textvariable=self.sys_prompt_var)
        self.entry_sys.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.lbl_temp = ttk.Label(self.params_bar, text=t["temp_lbl"], style="Muted.TLabel")
        self.lbl_temp.pack(side="left", padx=(0, 4))

        self.temp_var = tk.DoubleVar(value=0.7)
        self.spin_temp = ttk.Spinbox(self.params_bar, from_=0.0, to=2.0, increment=0.1, textvariable=self.temp_var, width=5)
        self.spin_temp.pack(side="left", padx=(0, 10))

        self.lbl_tokens = ttk.Label(self.params_bar, text=t["max_tokens_lbl"], style="Muted.TLabel")
        self.lbl_tokens.pack(side="left", padx=(0, 4))

        self.tokens_var = tk.IntVar(value=2048)
        self.spin_tokens = ttk.Spinbox(self.params_bar, from_=128, to=16384, increment=256, textvariable=self.tokens_var, width=6)
        self.spin_tokens.pack(side="left")

        # Chat Display Area
        self.chat_display = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, state="disabled",
            font=("Segoe UI", 10), relief="flat", bd=0, padx=12, pady=10
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=(2, 6))

        # Input Area (Multi-line + Send Button)
        self.bottom_frame = ttk.Frame(self, style="Card.TFrame", padding=(10, 4, 10, 8))
        self.bottom_frame.pack(fill="x")

        input_row = ttk.Frame(self.bottom_frame, style="Card.TFrame")
        input_row.pack(fill="x")

        self.entry_msg = tk.Text(
            input_row, height=3, wrap=tk.WORD,
            font=("Segoe UI", 10), relief="solid", bd=1, padx=8, pady=6
        )
        self.entry_msg.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry_msg.bind("<Return>", self.on_enter_key)

        self.btn_send = ttk.Button(input_row, text=t["send_btn"], style="Accent.TButton", command=self.send)
        self.btn_send.pack(side="right", fill="y")

        meta_row = ttk.Frame(self.bottom_frame, style="Card.TFrame")
        meta_row.pack(fill="x", pady=(4, 0))

        self.lbl_hint = ttk.Label(meta_row, text=t["input_hint"], style="Muted.TLabel")
        self.lbl_hint.pack(side="left")

        self.lbl_metrics = ttk.Label(meta_row, text="", style="Muted.TLabel")
        self.lbl_metrics.pack(side="right")

    def on_enter_key(self, event):
        if event.state & 0x0001:  # Shift key pressed -> allow newline
            return None
        self.send()
        return "break"

    def apply_theme(self):
        pal = THEMES[self.app_instance.current_theme]
        self.chat_display.config(
            bg=pal["surface"], fg=pal["fg"],
            insertbackground=pal["fg"], selectbackground=pal["select_bg"]
        )
        self.chat_display.tag_config("user", foreground=pal["user_tag"], font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("ai", foreground=pal["ai_tag"], font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("error", foreground=pal["err_tag"], font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("body", foreground=pal["fg"], font=("Segoe UI", 10))

        self.entry_msg.config(
            bg=pal["input_bg"], fg=pal["fg"],
            insertbackground=pal["fg"], highlightbackground=pal["border"],
            highlightcolor=pal["accent"], highlightthickness=1, bd=0
        )

    def update_language(self):
        t = TRANSLATIONS[self.app_instance.current_lang]
        self.lbl_info.config(text=t["info_lbl"].format(provider=self.provider, model=self.model))
        self.btn_export.config(text=t["export_chat"])
        self.btn_copy.config(text=t["copy_last"])
        self.btn_clear.config(text=t["clear_chat"])
        self.lbl_sys.config(text=t["sys_prompt"])
        self.lbl_temp.config(text=t["temp_lbl"])
        self.lbl_tokens.config(text=t["max_tokens_lbl"])
        self.btn_send.config(text=t["send_btn"])
        self.lbl_hint.config(text=t["input_hint"])

    def append_text(self, sender: str, text: str, tag: str = "user"):
        self.chat_display.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        if sender:
            self.chat_display.insert(tk.END, f"[{timestamp}] {sender}:\n", tag)
        self.chat_display.insert(tk.END, f"{text}\n\n", "body" if tag != "error" else "error")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def clear_chat(self):
        self.history.clear()
        self.last_reply = ""
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state="disabled")
        self.lbl_metrics.config(text="")

    def copy_last_reply(self):
        if not self.last_reply:
            return
        self.clipboard_clear()
        self.clipboard_append(self.last_reply)
        t = TRANSLATIONS[self.app_instance.current_lang]
        self.lbl_metrics.config(text=t["copied_msg"])

    def export_chat(self):
        if not self.history:
            return
        t = TRANSLATIONS[self.app_instance.current_lang]
        safe_model = "".join(c if c.isalnum() or c in "-_." else "_" for c in self.model)
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            initialfile=f"chat_{safe_model}.md",
            filetypes=[("Markdown File", "*.md"), ("JSON File", "*.json"), ("Text File", "*.txt")]
        )
        if not path:
            return
        if path.endswith(".json"):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({
                    "provider": self.provider,
                    "model": self.model,
                    "system_prompt": self.sys_prompt_var.get(),
                    "messages": self.history
                }, f, indent=2, ensure_ascii=False)
        else:
            lines = [
                f"# APIScout Studio Chat — {self.provider} ({self.model})",
                f"**System Prompt:** `{self.sys_prompt_var.get()}`\n",
                "---\n"
            ]
            for msg in self.history:
                role_title = "User" if msg["role"] == "user" else f"AI ({self.model})"
                lines.append(f"### {role_title}\n\n{msg['content']}\n")
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        messagebox.showinfo("APIScout Studio", t["exported_msg"].format(path=path))

    def send(self):
        t = TRANSLATIONS[self.app_instance.current_lang]
        user_text = self.entry_msg.get("1.0", tk.END).strip()
        if not user_text:
            return

        self.entry_msg.delete("1.0", tk.END)
        self.append_text(t["you"], user_text, "user")

        self.btn_send.config(state="disabled", text=t["sending_btn"])
        self.entry_msg.config(state="disabled")

        try:
            temp = float(self.temp_var.get())
        except Exception:
            temp = 0.7
        try:
            max_tok = int(self.tokens_var.get())
        except Exception:
            max_tok = 2048

        sys_prompt = self.sys_prompt_var.get()

        threading.Thread(
            target=self._async_send,
            args=(user_text, sys_prompt, temp, max_tok),
            daemon=True
        ).start()

    def _async_send(self, user_text: str, sys_prompt: str, temp: float, max_tok: int):
        lang = self.app_instance.current_lang
        success, response, elapsed_ms = send_chat_message(
            provider=self.provider,
            api_key=self.api_key,
            model=self.model,
            history=self.history,
            user_message=user_text,
            system_prompt=sys_prompt,
            temperature=temp,
            max_tokens=max_tok,
            lang=lang,
            custom_base_url=self.custom_base_url
        )
        self.after(0, lambda: self._update_chat(success, user_text, response, elapsed_ms))

    def _update_chat(self, success: bool, user_text: str, response: str, elapsed_ms: int):
        t = TRANSLATIONS[self.app_instance.current_lang]
        if success:
            self.last_reply = response
            self.append_text(f"AI ({self.model})", response, "ai")
            self.history.append({"role": "user", "content": user_text})
            self.history.append({"role": "assistant", "content": response})
            self.lbl_metrics.config(text=t["latency_ info"].format(ms=elapsed_ms, chars=len(response)))
        else:
            self.append_text(t["system_error"], response, "error")

        self.btn_send.config(state="normal", text=t["send_btn"])
        self.entry_msg.config(state="normal")
        self.entry_msg.focus()


# ==================== MAIN APPLICATION ====================
class AIModelScannerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.current_lang = "en"
        self.current_theme = "dark"
        self.key_visible = False

        self.root.geometry("1220x760")
        self.root.minsize(920, 580)

        icon_file = resource_path("app_icon.ico")
        if os.path.exists(icon_file):
            try:
                self.root.iconbitmap(icon_file)
            except Exception:
                pass

        self.scanned_models = []
        self.filtered_models = []
        self.session_keys = {}  # In-memory only per-provider key cache

        self.style = ttk.Style(self.root)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.create_widgets()
        self.apply_theme()
        self.update_ui_language()

    def create_widgets(self):
        # Top App Header Bar
        self.top_bar = ttk.Frame(self.root, style="TopBar.TFrame", padding=(16, 10))
        self.top_bar.pack(fill="x")

        title_box = ttk.Frame(self.top_bar, style="TopBar.TFrame")
        title_box.pack(side="left")

        self.lbl_app_title = ttk.Label(title_box, text="🔍 APIScout Studio", style="HeroTitle.TLabel")
        self.lbl_app_title.pack(side="left")

        self.lbl_app_sub = ttk.Label(title_box, text="", style="MutedTop.TLabel")
        self.lbl_app_sub.pack(side="left", padx=(12, 0))

        # Controls on right of Top Bar (Theme + Language)
        controls_box = ttk.Frame(self.top_bar, style="TopBar.TFrame")
        controls_box.pack(side="right")

        self.btn_theme = ttk.Button(controls_box, text="☀️ Light", width=10, command=self.toggle_theme)
        self.btn_theme.pack(side="right", padx=(10, 0))

        self.lang_var = tk.StringVar(value="English")
        self.lang_map = {"English": "en", "Türkçe": "tr", "Español": "es", "Français": "fr"}

        self.lang_dropdown = ttk.Combobox(
            controls_box,
            textvariable=self.lang_var,
            values=list(self.lang_map.keys()),
            state="readonly",
            width=11
        )
        self.lang_dropdown.pack(side="right")
        self.lang_dropdown.bind("<<ComboboxSelected>>", self.on_language_change)

        self.lbl_lang = ttk.Label(controls_box, text="Language:", style="MutedTop.TLabel")
        self.lbl_lang.pack(side="right", padx=(0, 6))

        # Main Split Workspace
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        # --- LEFT SIDEBAR ---
        self.left_frame = ttk.Frame(self.main_paned, style="Main.TFrame", width=410, padding=(4, 4, 8, 4))
        self.main_paned.add(self.left_frame, weight=1)

        # 1. API Configuration Frame
        self.form_frame = ttk.LabelFrame(self.left_frame, style="Card.TLabelframe", padding=12)
        self.form_frame.pack(fill="x", pady=(0, 10))

        self.lbl_provider = ttk.Label(self.form_frame, style="Card.TLabel")
        self.lbl_provider.grid(row=0, column=0, sticky="w", pady=5)

        self.provider_var = tk.StringVar(value="OpenAI")
        self.provider_dropdown = ttk.Combobox(
            self.form_frame,
            textvariable=self.provider_var,
            values=list(PROVIDER_CONFIGS.keys()),
            state="readonly"
        )
        self.provider_dropdown.grid(row=0, column=1, columnspan=3, sticky="ew", padx=(6, 0), pady=5)
        self.provider_dropdown.bind("<<ComboboxSelected>>", self.on_provider_change)

        # Optional Base URL row for Custom OpenAI-Compatible Provider
        self.lbl_base_url = ttk.Label(self.form_frame, text="Base URL:", style="Card.TLabel")
        self.base_url_var = tk.StringVar(value="http://localhost:11434/v1")
        self.entry_base_url = ttk.Entry(self.form_frame, textvariable=self.base_url_var)

        # API Key Row with Show/Hide & Clear buttons
        self.lbl_api_key = ttk.Label(self.form_frame, style="Card.TLabel")
        self.lbl_api_key.grid(row=2, column=0, sticky="w", pady=5)

        self.api_key_entry = ttk.Entry(self.form_frame, show="•")
        self.api_key_entry.grid(row=2, column=1, sticky="ew", padx=(6, 4), pady=5)
        self.api_key_entry.bind("<Return>", lambda e: self.start_scan())

        self.btn_toggle_key = ttk.Button(self.form_frame, text="Show", width=6, command=self.toggle_key_visibility)
        self.btn_toggle_key.grid(row=2, column=2, padx=(0, 4), pady=5)

        self.btn_clear_key = ttk.Button(self.form_frame, text="✕", width=3, command=self.clear_api_key)
        self.btn_clear_key.grid(row=2, column=3, pady=5)

        # Scan Button & Progress Bar
        self.scan_btn = ttk.Button(self.form_frame, style="Accent.TButton", command=self.start_scan)
        self.scan_btn.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(8, 2))

        self.progress_bar = ttk.Progressbar(self.form_frame, mode="indeterminate")

        self.form_frame.columnconfigure(1, weight=1)

        # 2. Models Explorer Frame
        self.models_frame = ttk.LabelFrame(self.left_frame, style="Card.TLabelframe", padding=12)
        self.models_frame.pack(fill="both", expand=True)

        self.status_label = ttk.Label(self.models_frame, style="Status.TLabel", wraplength=360)
        self.status_label.pack(anchor="w", pady=(0, 6))

        # Live Search / Filter Row
        search_row = ttk.Frame(self.models_frame, style="Card.TFrame")
        search_row.pack(fill="x", pady=(0, 6))

        self.lbl_search = ttk.Label(search_row, text="Filter:", style="Card.TLabel")
        self.lbl_search.pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.filter_models())
        self.entry_search = ttk.Entry(search_row, textvariable=self.search_var)
        self.entry_search.pack(side="left", fill="x", expand=True)

        # Interactive Model Listbox + Scrollbar
        list_container = ttk.Frame(self.models_frame, style="Card.TFrame")
        list_container.pack(fill="both", expand=True, pady=(0, 6))

        self.model_listbox = tk.Listbox(
            list_container,
            font=("Consolas", 10),
            activestyle="none",
            selectmode=tk.SINGLE,
            exportselection=False,
            relief="flat",
            bd=0
        )
        self.model_listbox.pack(side="left", fill="both", expand=True)
        self.model_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.model_listbox.bind("<Double-Button-1>", lambda e: self.open_playground())

        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.model_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.model_listbox.config(yscrollcommand=scrollbar.set)

        self.lbl_count = ttk.Label(self.models_frame, text="", style="Muted.TLabel")
        self.lbl_count.pack(anchor="w", pady=(0, 6))

        # Action Buttons for Selected Model
        btn_row = ttk.Frame(self.models_frame, style="Card.TFrame")
        btn_row.pack(fill="x", pady=(2, 0))

        self.open_pg_btn = ttk.Button(
            btn_row, style="Accent.TButton",
            command=self.open_playground, state="disabled"
        )
        self.open_pg_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_copy_model = ttk.Button(
            btn_row, command=self.copy_selected_model, state="disabled", width=10
        )
        self.btn_copy_model.pack(side="left", padx=(0, 4))

        self.btn_export_models = ttk.Button(
            btn_row, command=self.export_models_list, state="disabled", width=11
        )
        self.btn_export_models.pack(side="left")

        # --- RIGHT PLAYGROUND WORKSPACE ---
        self.right_frame = ttk.Frame(self.main_paned, style="Main.TFrame", padding=(4, 4, 4, 4))
        self.main_paned.add(self.right_frame, weight=3)

        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<Button-3>", self.show_tab_menu)
        self.notebook.bind("<Button-2>", self.on_middle_click_tab)

        # Create Welcome Overview Tab
        self.create_welcome_tab()

    def create_welcome_tab(self):
        t = TRANSLATIONS[self.current_lang]
        self.welcome_tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=30)
        self.lbl_welcome_title = ttk.Label(self.welcome_tab, text=t["welcome_title"], style="HeroTitle.TLabel")
        self.lbl_welcome_title.pack(anchor="w", pady=(10, 16))

        self.lbl_welcome_body = ttk.Label(
            self.welcome_tab, text=t["welcome_body"],
            style="Card.TLabel", justify="left", wraplength=680
        )
        self.lbl_welcome_body.pack(anchor="w", pady=(0, 20))

        self.lbl_double_hint = ttk.Label(
            self.welcome_tab, text=t["double_click_hint"],
            style="AccentTitle.TLabel"
        )
        self.lbl_double_hint.pack(anchor="w")

        self.notebook.add(self.welcome_tab, text=" 🏠 Welcome ")

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme()
        self.update_ui_language()

    def apply_theme(self):
        pal = THEMES[self.current_theme]
        self.root.configure(bg=pal["bg"])

        self.style.configure(".", background=pal["bg"], foreground=pal["fg"], font=("Segoe UI", 9))
        self.style.configure("Main.TFrame", background=pal["bg"])
        self.style.configure("TopBar.TFrame", background=pal["panel"])
        self.style.configure("Card.TFrame", background=pal["panel"])
        self.style.configure("Card.TLabelframe", background=pal["panel"], foreground=pal["accent"], bordercolor=pal["border"])
        self.style.configure("Card.TLabelframe.Label", background=pal["panel"], foreground=pal["accent"], font=("Segoe UI", 10, "bold"))

        self.style.configure("Card.TLabel", background=pal["panel"], foreground=pal["fg"], font=("Segoe UI", 9))
        self.style.configure("Muted.TLabel", background=pal["panel"], foreground=pal["fg_muted"], font=("Segoe UI", 8))
        self.style.configure("MutedTop.TLabel", background=pal["panel"], foreground=pal["fg_muted"], font=("Segoe UI", 9))
        self.style.configure("HeroTitle.TLabel", background=pal["panel"], foreground=pal["fg"], font=("Segoe UI", 13, "bold"))
        self.style.configure("AccentTitle.TLabel", background=pal["panel"], foreground=pal["accent"], font=("Segoe UI", 10, "bold"))
        self.style.configure("Status.TLabel", background=pal["panel"], foreground=pal["fg_muted"], font=("Segoe UI", 9, "italic"))

        self.style.configure("TButton", background=pal["surface"], foreground=pal["fg"], bordercolor=pal["border"], padding=(8, 5))
        self.style.map("TButton", background=[("active", pal["border"]), ("disabled", pal["panel"])], foreground=[("disabled", pal["fg_muted"])])

        self.style.configure("Accent.TButton", background=pal["accent"], foreground="#ffffff", font=("Segoe UI", 9, "bold"), padding=(10, 6))
        self.style.map("Accent.TButton", background=[("active", pal["accent_hover"]), ("disabled", pal["border"])], foreground=[("disabled", pal["fg_muted"])])

        self.style.configure("TEntry", fieldbackground=pal["input_bg"], foreground=pal["fg"], insertcolor=pal["fg"], bordercolor=pal["border"], padding=4)
        self.style.configure("TCombobox", fieldbackground=pal["input_bg"], background=pal["surface"], foreground=pal["fg"], arrowcolor=pal["fg"], padding=4)
        self.style.map("TCombobox", fieldbackground=[("readonly", pal["input_bg"])], foreground=[("readonly", pal["fg"])])
        self.style.configure("TSpinbox", fieldbackground=pal["input_bg"], foreground=pal["fg"], arrowcolor=pal["fg"], padding=3)

        self.style.configure("TNotebook", background=pal["bg"], bordercolor=pal["border"])
        self.style.configure("TNotebook.Tab", background=pal["surface"], foreground=pal["fg_muted"], padding=(12, 6), font=("Segoe UI", 9, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", pal["panel"])], foreground=[("selected", pal["accent"])])

        self.model_listbox.config(
            bg=pal["surface"], fg=pal["fg"],
            selectbackground=pal["select_bg"], selectforeground=pal["select_fg"],
            highlightbackground=pal["border"], highlightcolor=pal["accent"], highlightthickness=1
        )

        # Update all existing Playground tabs
        for tab_id in self.notebook.tabs():
            widget = self.root.nametowidget(tab_id)
            if isinstance(widget, PlaygroundTab):
                widget.apply_theme()

    def toggle_key_visibility(self):
        self.key_visible = not self.key_visible
        self.api_key_entry.config(show="" if self.key_visible else "•")
        t = TRANSLATIONS[self.current_lang]
        self.btn_toggle_key.config(text=t["hide_key"] if self.key_visible else t["show_key"])

    def clear_api_key(self):
        self.api_key_entry.delete(0, tk.END)
        prov = self.provider_var.get()
        self.session_keys.pop(prov, None)

    def on_provider_change(self, event=None):
        prov = self.provider_var.get()
        if prov == "Custom (OpenAI-Compatible)":
            self.lbl_base_url.grid(row=1, column=0, sticky="w", pady=5)
            self.entry_base_url.grid(row=1, column=1, columnspan=3, sticky="ew", padx=(6, 0), pady=5)
        else:
            self.lbl_base_url.grid_forget()
            self.entry_base_url.grid_forget()

        # Restore session key if available, otherwise clear for security
        self.api_key_entry.delete(0, tk.END)
        if prov in self.session_keys:
            self.api_key_entry.insert(0, self.session_keys[prov])

    def on_language_change(self, event=None):
        self.current_lang = self.lang_map.get(self.lang_var.get(), "en")
        self.update_ui_language()

    def update_ui_language(self):
        t = TRANSLATIONS[self.current_lang]
        self.root.title(t["title"])
        self.lbl_app_sub.config(text=t["subtitle"])
        self.lbl_lang.config(text=t["language"])
        self.btn_theme.config(text=t["theme_light"] if self.current_theme == "dark" else t["theme_dark"])

        self.form_frame.config(text=t["api_params"])
        self.lbl_provider.config(text=t["provider"])
        self.lbl_base_url.config(text=t["base_url"])
        self.lbl_api_key.config(text=t["api_key"])
        self.btn_toggle_key.config(text=t["hide_key"] if self.key_visible else t["show_key"])
        self.scan_btn.config(text=t["scan_btn"])

        self.models_frame.config(text=t["models_pg"])
        if not self.scanned_models:
            self.status_label.config(text=t["initial_status"])
        self.lbl_search.config(text=t["search_lbl"])
        self.open_pg_btn.config(text=t["open_pg_btn"])
        self.btn_copy_model.config(text=t["copy_model_btn"])
        self.btn_export_models.config(text=t["export_models_btn"])

        if hasattr(self, "lbl_welcome_title"):
            self.lbl_welcome_title.config(text=t["welcome_title"])
            self.lbl_welcome_body.config(text=t["welcome_body"])
            self.lbl_double_hint.config(text=t["double_click_hint"])

        for tab_id in self.notebook.tabs():
            widget = self.root.nametowidget(tab_id)
            if isinstance(widget, PlaygroundTab):
                widget.update_language()

    def start_scan(self):
        t = TRANSLATIONS[self.current_lang]
        provider = self.provider_var.get()
        api_key = self.api_key_entry.get().strip()
        custom_url = self.base_url_var.get().strip()

        if not api_key and provider != "Custom (OpenAI-Compatible)":
            messagebox.showwarning(t["warning_title"], t["warning_key_msg"])
            return

        self.session_keys[provider] = api_key
        pal = THEMES[self.current_theme]
        self.status_label.config(text=t["scanning"].format(provider=provider), foreground=pal["accent"])
        self.scan_btn.config(state="disabled", text=t["scanning_btn"])

        self.progress_bar.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(4, 0))
        self.progress_bar.start(12)

        self.model_listbox.delete(0, tk.END)
        self.lbl_count.config(text="")

        threading.Thread(
            target=self._async_scan,
            args=(provider, api_key, custom_url),
            daemon=True
        ).start()

    def _async_scan(self, provider: str, api_key: str, custom_url: str):
        success, result, elapsed_ms = scan_provider_models(
            provider=provider,
            api_key=api_key,
            lang=self.current_lang,
            custom_base_url=custom_url
        )
        self.root.after(0, lambda: self._finish_scan(success, result, elapsed_ms))

    def _finish_scan(self, success: bool, result, elapsed_ms: int):
        t = TRANSLATIONS[self.current_lang]
        pal = THEMES[self.current_theme]

        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.scan_btn.config(state="normal", text=t["scan_btn"])

        if success and isinstance(result, list):
            self.scanned_models = result
            self.status_label.config(
                text=t["success"].format(count=len(result), ms=elapsed_ms),
                foreground=pal["success_fg"]
            )
            self.filter_models()
            self.btn_export_models.config(state="normal" if result else "disabled")
        else:
            self.scanned_models = []
            self.filtered_models = []
            self.status_label.config(text=f"{t['error']} {result}", foreground=pal["err_tag"])
            self.open_pg_btn.config(state="disabled")
            self.btn_copy_model.config(state="disabled")
            self.btn_export_models.config(state="disabled")

    def filter_models(self):
        t = TRANSLATIONS[self.current_lang]
        query = self.search_var.get().strip().lower()
        self.model_listbox.delete(0, tk.END)

        if not self.scanned_models:
            self.filtered_models = []
            self.lbl_count.config(text="")
            return

        self.filtered_models = [
            m for m in self.scanned_models
            if not query or query in m.lower()
        ]
        for model in self.filtered_models:
            self.model_listbox.insert(tk.END, model)

        self.lbl_count.config(
            text=t["filtered_count"].format(shown=len(self.filtered_models), total=len(self.scanned_models))
        )

        if self.filtered_models:
            self.model_listbox.selection_set(0)
            self.open_pg_btn.config(state="normal")
            self.btn_copy_model.config(state="normal")
        else:
            self.open_pg_btn.config(state="disabled")
            self.btn_copy_model.config(state="disabled")

    def get_selected_model(self) -> str:
        sel = self.model_listbox.curselection()
        if not sel:
            return ""
        idx = sel[0]
        if 0 <= idx < len(self.filtered_models):
            return self.filtered_models[idx]
        return ""

    def on_listbox_select(self, event=None):
        has_sel = bool(self.get_selected_model())
        self.open_pg_btn.config(state="normal" if has_sel else "disabled")
        self.btn_copy_model.config(state="normal" if has_sel else "disabled")

    def copy_selected_model(self):
        model = self.get_selected_model()
        if not model:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(model)
        t = TRANSLATIONS[self.current_lang]
        self.lbl_count.config(text=f"{t['copied_msg']} ({model})")

    def export_models_list(self):
        if not self.scanned_models:
            return
        t = TRANSLATIONS[self.current_lang]
        provider = self.provider_var.get()
        safe_prov = "".join(c if c.isalnum() else "_" for c in provider)
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"{safe_prov}_models.txt",
            filetypes=[("Text File", "*.txt"), ("JSON File", "*.json")]
        )
        if not path:
            return
        if path.endswith(".json"):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({
                    "provider": provider,
                    "count": len(self.scanned_models),
                    "models": self.scanned_models
                }, f, indent=2, ensure_ascii=False)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.scanned_models))
        messagebox.showinfo("APIScout Studio", t["exported_msg"].format(path=path))

    def open_playground(self):
        t = TRANSLATIONS[self.current_lang]
        provider = self.provider_var.get()
        api_key = self.api_key_entry.get().strip()
        custom_url = self.base_url_var.get().strip()
        model = self.get_selected_model()

        if not model:
            messagebox.showwarning(t["warning_title"], t["warning_model_msg"])
            return

        short_model = f"{model[:18]}…" if len(model) > 19 else model
        tab_title = f" 💬 {provider.split()[0]}: {short_model} "
        pg_tab = PlaygroundTab(self.notebook, provider, api_key, model, custom_url, self)

        self.notebook.add(pg_tab, text=tab_title)
        self.notebook.select(pg_tab)

    def close_specific_tab(self, tab_widget):
        try:
            self.notebook.forget(tab_widget)
            tab_widget.destroy()
        except Exception:
            pass

    def on_middle_click_tab(self, event):
        try:
            tab_index = self.notebook.index(f"@{event.x},{event.y}")
            tab_id = self.notebook.tabs()[tab_index]
            widget = self.root.nametowidget(tab_id)
            if isinstance(widget, PlaygroundTab):
                self.close_specific_tab(widget)
        except Exception:
            pass

    def show_tab_menu(self, event):
        t = TRANSLATIONS[self.current_lang]
        try:
            tab_index = self.notebook.index(f"@{event.x},{event.y}")
            tab_id = self.notebook.tabs()[tab_index]
            widget = self.root.nametowidget(tab_id)
            if not isinstance(widget, PlaygroundTab):
                return
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label=t["close_tab"], command=lambda: self.close_specific_tab(widget))
            menu.post(event.x_root, event.y_root)
        except Exception:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = AIModelScannerApp(root)
    if "--self-test" in sys.argv:
        import http.server
        import socketserver

        class _MockHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"data": [{"id": "gpt-4o-test"}, {"id": "claude-3-7-sonnet-test"}]}).encode("utf-8"))
            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                if length:
                    self.rfile.read(length)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"choices": [{"message": {"content": "Hello from APIScout Studio Tkinter E2E test!"}}]}).encode("utf-8"))

        httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _MockHandler)
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()

        def _step1():
            try:
                app.toggle_theme()
                app.toggle_theme()
                for lang_label in ["Türkçe", "Español", "Français", "English"]:
                    app.lang_var.set(lang_label)
                    app.on_language_change()
                app.provider_var.set("Custom (OpenAI-Compatible)")
                app.on_provider_change()
                app.base_url_var.set(f"http://127.0.0.1:{port}/v1")
                app.api_key_entry.delete(0, tk.END)
                app.api_key_entry.insert(0, "sk-test-key-12345")
                app.start_scan()
                root.after(700, _step2)
            except Exception as exc:
                _fail(exc)

        def _step2():
            try:
                assert "gpt-4o-test" in app.scanned_models, f"Expected model not found: {app.scanned_models}"
                app.search_var.set("gpt-4o")
                app.open_playground()
                tab_id = app.notebook.select()
                current_tab = root.nametowidget(tab_id)
                assert isinstance(current_tab, PlaygroundTab), "Playground tab did not open"
                current_tab.entry_msg.insert("1.0", "Ping test")
                current_tab.send()
                root.after(700, lambda: _step3(current_tab))
            except Exception as exc:
                _fail(exc)

        def _step3(current_tab):
            try:
                assert "Hello from APIScout Studio Tkinter E2E test!" in current_tab.last_reply, f"Unexpected reply: {current_tab.last_reply}"
                if len(sys.argv) > 2 and sys.argv[1] == "--self-test":
                    with open(sys.argv[2], "w", encoding="utf-8") as f:
                        f.write("SELF_TEST_E2E_OK")
                httpd.shutdown()
                root.destroy()
            except Exception as exc:
                _fail(exc)

        def _fail(exc):
            if len(sys.argv) > 2 and sys.argv[1] == "--self-test":
                with open(sys.argv[2], "w", encoding="utf-8") as f:
                    f.write(f"SELF_TEST_ERR: {exc}")
            sys.exit(1)

        root.after(250, _step1)
    root.mainloop()
