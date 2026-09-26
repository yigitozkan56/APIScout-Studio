import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import os

# ==================== DİL ÇEVİRİ SÖZLÜĞÜ ====================
TRANSLATIONS = {
    "tr": {
        "title": "APIScout",
        "params": " Parametreler ",
        "provider": "Sağlayıcı:",
        "api_key": "API Key:",
        "scan_btn": "Modelleri Tara",
        "supported_models": " Desteklenen Modeller ",
        "initial_status": "Lütfen API anahtarınızı girip taramayı başlatın.",
        "warning_title": "Uyarı",
        "warning_msg": "Lütfen bir API Key girin.",
        "connecting": "sunucularına bağlanılıyor...",
        "success": "Başarılı! Toplam {count} model bulundu.",
        "error": "Hata oluştu!",
        "err_prefix": "HATA: ",
        "invalid_key": "Geçersiz API Key (Unauthorized)",
        "err_code": "Hata Kodu",
        "conn_err": "Bağlantı hatası",
        "unauthorized_or_invalid": "Geçersiz API Key veya Yetkisiz Erişim",
        "language": "Dil / Language:"
    },
    "en": {
        "title": "APIScout",
        "params": " Parameters ",
        "provider": "Provider:",
        "api_key": "API Key:",
        "scan_btn": "Scan Models",
        "supported_models": " Supported Models ",
        "initial_status": "Please enter your API key and start scanning.",
        "warning_title": "Warning",
        "warning_msg": "Please enter an API Key.",
        "connecting": "connecting to servers...",
        "success": "Success! Found a total of {count} models.",
        "error": "An error occurred!",
        "err_prefix": "ERROR: ",
        "invalid_key": "Invalid API Key (Unauthorized)",
        "err_code": "Error Code",
        "conn_err": "Connection error",
        "unauthorized_or_invalid": "Invalid API Key or Unauthorized Access",
        "language": "Language:"
    },
    "es": {
        "title": "APIScout",
        "params": " Parámetros ",
        "provider": "Proveedor:",
        "api_key": "Clave API:",
        "scan_btn": "Escanear Modelos",
        "supported_models": " Modelos Compatibles ",
        "initial_status": "Ingrese su clave API y comience a escanear.",
        "warning_title": "Advertencia",
        "warning_msg": "Por favor, ingrese una clave API.",
        "connecting": "conectando a los servidores...",
        "success": "¡Éxito! Se encontraron {count} modelos en total.",
        "error": "¡Ocurrió un error!",
        "err_prefix": "ERROR: ",
        "invalid_key": "Clave API no válida (No autorizado)",
        "err_code": "Código de Error",
        "conn_err": "Error de conexión",
        "unauthorized_or_invalid": "Clave API no válida o acceso no autorizado",
        "language": "Idioma:"
    },
    "fr": {
        "title": "APIScout",
        "params": " Paramètres ",
        "provider": "Fournisseur:",
        "api_key": "Clé API:",
        "scan_btn": "Analyser les Modèles",
        "supported_models": " Modèles Pris en Charge ",
        "initial_status": "Veuillez entrer votre clé API et lancer l'analyse.",
        "warning_title": "Avertissement",
        "warning_msg": "Veuillez entrer une clé API.",
        "connecting": "connexion aux serveurs...",
        "success": "Succès ! Total de {count} modèles trouvés.",
        "error": "Une erreur est survenue !",
        "err_prefix": "ERREUR: ",
        "invalid_key": "Clé API invalide (Non autorisé)",
        "err_code": "Code d'erreur",
        "conn_err": "Erreur de connexion",
        "unauthorized_or_invalid": "Clé API invalide ou accès non autorisé",
        "language": "Langue:"
    }
}

# ==================== TARAMA FONKSİYONLARI ====================

def scan_openai(api_key, lang="en"):
    t = TRANSLATIONS[lang]
    url = "https://api.openai.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = sorted([item['id'] for item in data.get('data', [])])
            return True, models
        elif response.status_code == 401:
            return False, t["invalid_key"]
        else:
            return False, f"{t['err_code']} {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"{t['conn_err']}: {str(e)}"

def scan_google_gemini(api_key, lang="en"):
    t = TRANSLATIONS[lang]
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            raw_models = data.get('models', [])
            models = sorted([m['name'].replace('models/', '') for m in raw_models])
            return True, models
        elif response.status_code in (400, 403):
            return False, t["unauthorized_or_invalid"]
        else:
            return False, f"{t['err_code']} {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"{t['conn_err']}: {str(e)}"

def scan_openrouter(api_key, lang="en"):
    t = TRANSLATIONS[lang]
    url = "https://openrouter.ai/api/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = sorted([item['id'] for item in data.get('data', [])])
            return True, models
        elif response.status_code == 401:
            return False, t["invalid_key"]
        else:
            return False, f"{t['err_code']} {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"{t['conn_err']}: {str(e)}"

def scan_groq(api_key, lang="en"):
    t = TRANSLATIONS[lang]
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = sorted([item['id'] for item in data.get('data', [])])
            return True, models
        elif response.status_code == 401:
            return False, t["invalid_key"]
        else:
            return False, f"{t['err_code']} {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"{t['conn_err']}: {str(e)}"

class AIModelScannerApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "en"

        self.root.geometry("620x580")
        self.root.minsize(500, 450)

        icon_path = "app_icon.ico"
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        self.providers = {
            "OpenAI": scan_openai,
            "Google Gemini": scan_google_gemini,
            "OpenRouter": scan_openrouter,
            "Groq": scan_groq
        }

        self.create_widgets()
        self.update_ui_language()

    def create_widgets(self):
        # Dil Seçim Çubuğu
        lang_frame = ttk.Frame(self.root, padding=(15, 10, 15, 0))
        lang_frame.pack(fill="x")
        
        self.lbl_lang = ttk.Label(lang_frame, text="Language:")
        self.lbl_lang.pack(side="left", padx=(0, 5))
        
        self.lang_var = tk.StringVar(value="English")
        lang_map = {"Türkçe": "tr", "English": "en", "Español": "es", "Français": "fr"}
        
        self.lang_dropdown = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=list(lang_map.keys()),
            state="readonly",
            width=12
        )
        self.lang_dropdown.pack(side="left")
        self.lang_dropdown.bind("<<ComboboxSelected>>", self.on_language_change)

        # Üst Form Alanı
        self.form_frame = ttk.LabelFrame(self.root, padding=15)
        self.form_frame.pack(fill="x", padx=15, pady=10)

        self.lbl_provider = ttk.Label(self.form_frame)
        self.lbl_provider.grid(row=0, column=0, sticky="w", pady=5)
        
        self.provider_var = tk.StringVar(value="OpenAI")
        provider_dropdown = ttk.Combobox(
            self.form_frame, 
            textvariable=self.provider_var, 
            values=list(self.providers.keys()), 
            state="readonly",
            width=25
        )
        provider_dropdown.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.lbl_api_key = ttk.Label(self.form_frame)
        self.lbl_api_key.grid(row=1, column=0, sticky="w", pady=5)
        
        self.api_key_entry = ttk.Entry(self.form_frame, width=45, show="*")
        self.api_key_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        self.scan_btn = ttk.Button(self.form_frame, command=self.start_scan)
        self.scan_btn.grid(row=2, column=1, sticky="e", padx=10, pady=10)

        self.form_frame.columnconfigure(1, weight=1)

        # Sonuç Alanı
        self.result_frame = ttk.LabelFrame(self.root, padding=10)
        self.result_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.status_label = ttk.Label(self.result_frame, font=("Arial", 9, "italic"))
        self.status_label.pack(anchor="w", pady=(0, 5))

        self.result_area = scrolledtext.ScrolledText(self.result_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.result_area.pack(fill="both", expand=True)

    def on_language_change(self, event=None):
        lang_map = {"Türkçe": "tr", "English": "en", "Español": "es", "Français": "fr"}
        self.current_lang = lang_map.get(self.lang_var.get(), "en")
        self.update_ui_language()

    def update_ui_language(self):
        t = TRANSLATIONS[self.current_lang]
        self.root.title(t["title"])
        self.lbl_lang.config(text=t["language"])
        self.form_frame.config(text=t["params"])
        self.lbl_provider.config(text=t["provider"])
        self.lbl_api_key.config(text=t["api_key"])
        self.scan_btn.config(text=t["scan_btn"])
        self.result_frame.config(text=t["supported_models"])
        self.status_label.config(text=t["initial_status"])

    def start_scan(self):
        t = TRANSLATIONS[self.current_lang]
        provider = self.provider_var.get()
        api_key = self.api_key_entry.get().strip()

        if not api_key:
            messagebox.showwarning(t["warning_title"], t["warning_msg"])
            return

        self.status_label.config(text=f"{provider} {t['connecting']}", foreground="blue")
        self.result_area.delete("1.0", tk.END)
        self.root.update_idletasks()

        scan_func = self.providers[provider]
        success, result = scan_func(api_key, self.current_lang)

        if success:
            msg = t["success"].format(count=len(result))
            self.status_label.config(text=msg, foreground="green")
            output_text = "\n".join([f"{i:3d}. {model}" for i, model in enumerate(result, 1)])
            self.result_area.insert(tk.END, output_text)
        else:
            self.status_label.config(text=t["error"], foreground="red")
            self.result_area.insert(tk.END, f"{t['err_prefix']}{result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIModelScannerApp(root)
    root.mainloop()