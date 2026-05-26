"""
Transcriptor de Video Pro v1.0  —  SONDA
Transcribe videos y audio a documentos Markdown usando OpenAI Whisper (offline).

Autor   : Julio Varas Contreras
Empresa : SONDA
Fecha   : Mayo 2026
"""
from __future__ import annotations

import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, scrolledtext, messagebox

# Parche para pythonw.exe (sin consola) para evitar errores de IO con torch/tqdm
class _DummyStream:
    def write(self, *args, **kwargs): pass
    def flush(self, *args, **kwargs): pass
    def isatty(self): return False
if sys.stdout is None: sys.stdout = _DummyStream()
if sys.stderr is None: sys.stderr = _DummyStream()

# Ocultar consola (evita WinError 6 de PyTorch que falla sin consola real)
if sys.platform == "win32":
    import ctypes
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0

# Ajustar PATH si se ejecuta desde PyInstaller para encontrar ffmpeg empaquetado
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.environ["PATH"] = sys._MEIPASS + os.pathsep + os.environ.get("PATH", "")

# Ajuste para entorno portable: buscar ffmpeg en la carpeta 'bin' local
base_path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
local_bin = base_path / "bin"
if local_bin.is_dir():
    os.environ["PATH"] = str(local_bin.resolve()) + os.pathsep + os.environ.get("PATH", "")

# Inyectar librerias del entorno virtual al ejecutable compilado
if getattr(sys, 'frozen', False):
    import site
    venv_lib = base_path / "env" / "Lib" / "site-packages"
    if venv_lib.is_dir():
        site.addsitedir(str(venv_lib))
        if str(venv_lib) not in sys.path:
            sys.path.insert(0, str(venv_lib))

APP_NAME    = "Transcriptor de Video Pro"
APP_VERSION = "v1.0  -  Mayo 2026"
APP_AUTHOR  = "Julio Varas Contreras"
APP_COMPANY = "SONDA"
APP_NOTICE  = (
    "Este software ha sido creado para uso exclusivo de SONDA.\n\n"
    "Queda estrictamente prohibida su distribucion, copia,\n"
    "modificacion o divulgacion a terceros sin autorizacion\n"
    "expresa del autor.\n\n"
    "© 2026  Julio Varas Contreras — Todos los derechos reservados."
)

SUPPORTED_EXTENSIONS = (
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
    ".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac",
)

# ——— Paleta corporativa SONDA ————————————————————————————————————
COL = {
    "header":          "#0D47A1",
    "primary":         "#1565C0",
    "primary_active":  "#0D47A1",
    "danger":          "#C62828",
    "danger_hover":    "#B71C1C",
    "text":            "#212121",
    "text_secondary":  "#607D8B",
    "bg":              "#F0F2F5",
    "card":            "#FFFFFF",
    "sep":             "#CFD8DC",
    "sep_light":       "#ECEFF1",
    "subtitle_blue":   "#BBDEFB",
    "credits_fg":      "#90CAF9",
    "card_title":      "#1565C0",
    "btn_dark":        "#37474F",
    "btn_dark_active": "#263238",
    "help":            "#607D8B",
    "warn":            "#E65100",
    "success":         "#2E7D32",
}

F_BODY       = ("Segoe UI", 10)
F_LABEL      = ("Segoe UI", 9)
F_HELP       = ("Segoe UI", 8)
F_CARD_TITLE = ("Segoe UI", 12, "bold")
F_HEADER     = ("Segoe UI", 22, "bold")
F_SUBHEADER  = ("Segoe UI", 11)
F_CREDITS    = ("Segoe UI", 9)
F_FOOTER     = ("Segoe UI", 8)
F_STATUS     = ("Segoe UI", 10, "bold")
F_LOG        = ("Consolas", 11)

WHISPER_MODELS    = ["tiny", "base", "small", "medium", "large"]
LANGUAGES         = ["auto", "es", "en", "pt", "fr", "de", "it", "ja", "zh", "ar"]
LANGUAGE_LABELS   = {
    "auto": "Auto-detectar",
    "es":   "Español",
    "en":   "English",
    "pt":   "Português",
    "fr":   "Français",
    "de":   "Deutsch",
    "it":   "Italiano",
    "ja":   "日本語",
    "zh":   "中文",
    "ar":   "العربية",
}
MODEL_INFO = {
    "tiny":   "~39 MB  · muy rapido · baja precision",
    "base":   "~74 MB  · rapido     · buena precision  (recomendado)",
    "small":  "~244 MB · equilibrado · mayor precision",
    "medium": "~769 MB · lento      · alta precision",
    "large":  "~1.5 GB · muy lento  · maxima precision",
}


# ——— Utilidades de recursos ————————————————————————————————————
def _resource(filename: str) -> str:
    base = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return str(Path(base) / filename)


def _set_window_icon(root: tk.Tk) -> None:
    try:
        df_logo = _resource("DF 500X500 BLANCO 1.png")
        if Path(df_logo).is_file():
            img = tk.PhotoImage(file=df_logo)
            root.iconphoto(True, img)
            return
    except Exception:
        pass

    try:
        ico = _resource("icon.ico")
        if Path(ico).is_file():
            root.iconbitmap(ico)
            return
    except Exception:
        pass
    for sz in (64, 128, 32, 256, 16):
        try:
            png = _resource(f"icon_{sz}x{sz}.png")
            if Path(png).is_file():
                img = tk.PhotoImage(file=png)
                root.iconphoto(True, img)
                return
        except Exception:
            pass


def _check_tool(name: str) -> bool:
    import shutil
    return shutil.which(name) is not None


# ——— Helpers de UI ——————————————————————————————————————————————
def _flat_btn(parent, text: str, bg: str, active: str,
              fg: str = "white", command=None,
              state=tk.NORMAL) -> tk.Button:
    return tk.Button(
        parent, text=text, command=command,
        font=F_BODY, bg=bg, fg=fg,
        activebackground=active, activeforeground=fg,
        relief=tk.FLAT, borderwidth=0, cursor="hand2",
        padx=14, pady=8, highlightthickness=0, state=state,
    )


def _card(parent, **pack_kw) -> tk.Frame:
    outer = tk.Frame(parent, bg=COL["sep"], highlightthickness=0)
    inner = tk.Frame(outer, bg=COL["card"], padx=14, pady=12,
                     highlightthickness=0)
    inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
    outer.pack(**pack_kw)
    return inner


def _card_title(inner: tk.Frame, text: str) -> None:
    tk.Label(inner, text=text, font=F_CARD_TITLE,
             fg=COL["card_title"], bg=COL["card"],
             anchor="w").pack(fill=tk.X)
    tk.Frame(inner, height=1, bg=COL["sep_light"]).pack(
        fill=tk.X, pady=(4, 10))


def _path_row(parent: tk.Frame, label: str,
              var: tk.StringVar, cmd,
              btn_text: str = "Seleccionar") -> None:
    tk.Label(parent, text=label, font=F_LABEL,
             fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))
    row = tk.Frame(parent, bg=COL["card"])
    row.pack(fill=tk.X, pady=(0, 10))
    tk.Entry(
        row, textvariable=var, font=F_BODY, fg=COL["text"],
        relief=tk.FLAT, highlightthickness=1,
        highlightbackground=COL["sep"],
        highlightcolor=COL["primary"],
    ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    _flat_btn(row, btn_text, COL["primary"],
              COL["primary_active"], command=cmd).pack(side=tk.RIGHT)


def _draw_header_icon(canvas: tk.Canvas) -> None:
    canvas.delete("all")
    # Cuerpo de camara
    canvas.create_rectangle(6, 24, 62, 72,
                             fill="white", outline="white", width=0)
    canvas.create_rectangle(6, 24, 62, 72,
                             fill="white", outline="#90CAF9", width=2)
    # Lente
    canvas.create_oval(16, 30, 52, 66,
                       fill="#1565C0", outline="white", width=2)
    canvas.create_oval(24, 38, 44, 58,
                       fill="#90CAF9", outline="white", width=1)
    # Visor triangular
    canvas.create_polygon(64, 30, 88, 40, 88, 56, 64, 66,
                          fill="white", outline="white")
    # Forma de onda (audio) — parte inferior
    for i, h in enumerate([8, 14, 20, 26, 20, 14, 8, 12, 18, 12, 8]):
        x = 8 + i * 8
        yc = 86
        canvas.create_line(x, yc - h // 2, x, yc + h // 2,
                           fill="#90CAF9", width=3, capstyle=tk.ROUND)


# ——— Aplicacion principal ——————————————————————————————————————
class TranscriptorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{APP_NAME}  -  {APP_COMPANY}")
        self.root.geometry("1024x900")
        self.root.minsize(900, 760)
        self.root.configure(bg=COL["bg"])

        _set_window_icon(self.root)

        self.video_path  = tk.StringVar()
        self.output_path = tk.StringVar(
            value=str(Path.home() / "Documents" / "Transcripciones"))
        self.model_var   = tk.StringVar(value="base")
        self.lang_var    = tk.StringVar(value="auto")
        self.timestamps  = tk.BooleanVar(value=True)
        self.paragraphs  = tk.BooleanVar(value=True)
        self.export_txt  = tk.BooleanVar(value=False)
        self.export_srt  = tk.BooleanVar(value=False)
        self.status      = tk.StringVar(
            value="Listo. Seleccione un archivo y pulse Transcribir.")

        self._selected_files: list[str] = []
        self._cancel_flag = threading.Event()

        self._setup_styles()
        self._build()
        self.root.after(300, self._refresh_footer)

    # ── Estilos ttk ─────────────────────────────────────────────
    def _setup_styles(self) -> None:
        s = ttk.Style(self.root)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("TCheckbutton",
                    background=COL["card"],
                    foreground=COL["text"],
                    font=F_BODY)
        s.map("TCheckbutton", background=[("active", COL["card"])])
        s.configure(
            "Prog.Horizontal.TProgressbar",
            troughcolor=COL["sep_light"],
            background=COL["primary"],
            bordercolor=COL["sep_light"],
            lightcolor=COL["primary"],
            darkcolor=COL["primary"],
            thickness=14,
        )

    # ── Construccion de ventana ──────────────────────────────────
    def _build(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=1)

        self._build_header()
        tk.Frame(self.root, bg=COL["sep"],
                 height=1).grid(row=1, column=0, sticky="ew")
        self._build_body()
        self._build_actions()
        self._build_log()
        self._build_footer()

    def _build_header(self) -> None:
        hdr = tk.Frame(self.root, bg=COL["header"],
                       height=118, highlightthickness=0)
        hdr.grid(row=0, column=0, sticky="nsew")
        hdr.grid_propagate(False)

        hc = tk.Frame(hdr, bg=COL["header"])
        hc.pack(fill=tk.BOTH, expand=True, padx=18, pady=(14, 12))

        iw = tk.Frame(hc, bg=COL["header"], width=96, height=96,
                      highlightthickness=0)
        iw.pack(side=tk.LEFT, padx=(0, 16))
        iw.pack_propagate(False)

        cv = tk.Canvas(iw, width=96, height=96,
                       bg=COL["header"], highlightthickness=0)
        cv.pack()
        loaded = False
        for sz in (64, 128, 32):
            try:
                png = _resource(f"icon_{sz}x{sz}.png")
                if Path(png).is_file():
                    img = tk.PhotoImage(file=png)
                    cv.create_image(48, 48, image=img, anchor="center")
                    cv._icon_img = img
                    loaded = True
                    break
            except Exception:
                pass
        if not loaded:
            _draw_header_icon(cv)

        titles = tk.Frame(hc, bg=COL["header"])
        titles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(titles, text=APP_NAME,
                 font=F_HEADER, fg="white",
                 bg=COL["header"], anchor="w").pack(anchor="w")
        tk.Label(titles,
                 text="Transcribe videos y audio a documentos Markdown usando IA offline (Whisper)",
                 font=F_SUBHEADER, fg=COL["subtitle_blue"],
                 bg=COL["header"], anchor="w").pack(anchor="w", pady=(2, 0))
        tk.Label(titles,
                 text=f"{APP_VERSION}  |  {APP_COMPANY}",
                 font=("Segoe UI", 8), fg=COL["credits_fg"],
                 bg=COL["header"], anchor="w").pack(anchor="w", pady=(2, 0))

        right_frame = tk.Frame(hc, bg=COL["header"])
        right_frame.pack(side=tk.RIGHT, anchor="ne")

        cred = tk.Label(right_frame, text="Creditos",
                        font=F_CREDITS, fg=COL["credits_fg"],
                        bg=COL["header"], cursor="hand2")
        cred.pack(anchor="e", pady=(0, 6))
        cred.bind("<Button-1>", self._on_credits)

        try:
            df_logo_path = _resource("DF 500X500 BLANCO 1.png")
            if Path(df_logo_path).is_file():
                # Reducir imagen de 500x500 a ~62x62 para el header
                img_df = tk.PhotoImage(file=df_logo_path).subsample(8, 8)
                lbl_df = tk.Label(right_frame, image=img_df, bg=COL["header"])
                lbl_df.image = img_df  # Prevenir recoleccion de basura
                lbl_df.pack(anchor="e")
        except Exception:
            pass

    def _build_body(self) -> None:
        body = tk.Frame(self.root, bg=COL["bg"])
        body.grid(row=2, column=0, sticky="nsew", padx=16, pady=14)
        body.columnconfigure(0, weight=3, uniform="cols")
        body.columnconfigure(1, weight=2, uniform="cols")

        left  = tk.Frame(body, bg=COL["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        right = tk.Frame(body, bg=COL["bg"])
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        # — Tarjeta ARCHIVO DE VIDEO —
        ci = _card(left, fill=tk.X)
        _card_title(ci, "ARCHIVO DE VIDEO / AUDIO")

        _path_row(ci, "Archivo de Video / Audio:",
                  self.video_path, self._browse_video)

        # Lista de archivos seleccionados
        tk.Label(ci, text="Cola de archivos:", font=F_LABEL,
                 fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))
        list_outer = tk.Frame(ci, bg=COL["sep"])
        list_outer.pack(fill=tk.X, pady=(0, 6))
        sb = tk.Scrollbar(list_outer, orient=tk.VERTICAL)
        self.files_listbox = tk.Listbox(
            list_outer, font=F_LOG, height=5,
            bg="#F8F9FA", fg=COL["text"],
            relief=tk.FLAT, borderwidth=0,
            selectbackground=COL["primary"],
            selectforeground="white",
            activestyle="none",
            yscrollcommand=sb.set,
        )
        sb.config(command=self.files_listbox.yview)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.X,
                                expand=True, padx=1, pady=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=1)

        btn_files_row = tk.Frame(ci, bg=COL["card"])
        btn_files_row.pack(fill=tk.X, pady=(0, 10))
        _flat_btn(btn_files_row, "Agregar Multiples",
                  COL["primary"], COL["primary_active"],
                  command=self._browse_multiple).pack(side=tk.LEFT, padx=(0, 6))
        _flat_btn(btn_files_row, "Quitar Seleccionado",
                  COL["btn_dark"], COL["btn_dark_active"],
                  command=self._remove_selected).pack(side=tk.LEFT, padx=(0, 6))
        _flat_btn(btn_files_row, "Limpiar Lista",
                  COL["btn_dark"], COL["btn_dark_active"],
                  command=self._clear_files).pack(side=tk.LEFT)

        _path_row(ci, "Carpeta de Salida:",
                  self.output_path, self._browse_output)

        # — Tarjeta CONFIGURACION —
        co = _card(right, fill=tk.X)
        _card_title(co, "CONFIGURACION")

        tk.Label(co, text="Modelo Whisper:", font=F_LABEL,
                 fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))

        model_cb = ttk.Combobox(
            co, textvariable=self.model_var,
            values=WHISPER_MODELS, state="readonly", font=F_BODY)
        model_cb.pack(fill=tk.X, pady=(0, 2))
        model_cb.bind("<<ComboboxSelected>>", self._on_model_change)

        self.model_info_lbl = tk.Label(
            co, text=MODEL_INFO["base"],
            font=F_HELP, fg=COL["help"], bg=COL["card"], justify="left")
        self.model_info_lbl.pack(anchor="w", pady=(0, 10))

        tk.Label(co, text="Idioma:", font=F_LABEL,
                 fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))
        lang_display = [LANGUAGE_LABELS[l] for l in LANGUAGES]
        self.lang_combo = ttk.Combobox(
            co, values=lang_display, state="readonly", font=F_BODY)
        self.lang_combo.current(0)
        self.lang_combo.pack(fill=tk.X, pady=(0, 10))

        tk.Frame(co, height=1, bg=COL["sep_light"]).pack(fill=tk.X, pady=(4, 8))

        tk.Label(co, text="Opciones de salida:", font=F_LABEL,
                 fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 6))

        for var, txt in [
            (self.timestamps, "Incluir marcas de tiempo [HH:MM:SS]"),
            (self.paragraphs, "Agrupar texto en parrafos"),
            (self.export_txt, "Exportar copia en .txt"),
            (self.export_srt, "Exportar subtitulos .srt"),
        ]:
            ttk.Checkbutton(co, text=txt, variable=var).pack(anchor="w", pady=2)

        tk.Frame(co, height=1, bg=COL["sep_light"]).pack(fill=tk.X, pady=(8, 6))

        tk.Label(co,
                 text="Requiere ffmpeg en PATH.\n"
                      "Modelos se descargan al primer uso.\n"
                      "Procesamiento 100% offline.",
                 font=F_HELP, fg=COL["help"], bg=COL["card"],
                 justify="left").pack(anchor="w")

    def _build_actions(self) -> None:
        acts = tk.Frame(self.root, bg=COL["bg"])
        acts.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 10))

        outer = tk.Frame(acts, bg=COL["sep"])
        outer.pack(fill=tk.X)
        inner = tk.Frame(outer, bg=COL["card"], padx=14, pady=12)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        btn_row = tk.Frame(inner, bg=COL["card"])
        btn_row.pack(fill=tk.X, pady=(0, 10))

        self.btn_transcribe = _flat_btn(
            btn_row, "Transcribir",
            COL["primary"], COL["primary_active"],
            command=self._on_transcribe)
        self.btn_transcribe.pack(side=tk.LEFT, fill=tk.X,
                                 expand=True, padx=(0, 8))

        self.btn_cancel = _flat_btn(
            btn_row, "Cancelar",
            COL["danger"], COL["danger_hover"],
            command=self._on_cancel,
            state=tk.DISABLED)
        self.btn_cancel.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_open = _flat_btn(
            btn_row, "Abrir Carpeta de Salida",
            COL["btn_dark"], COL["btn_dark_active"],
            command=self._open_folder,
            state=tk.DISABLED)
        self.btn_open.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(
            inner, mode="indeterminate",
            style="Prog.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(0, 4))

        tk.Label(
            inner, textvariable=self.status,
            font=F_STATUS, fg=COL["text"], bg=COL["card"],
            anchor="w", wraplength=900, justify="left",
        ).pack(fill=tk.X)

    def _build_log(self) -> None:
        outer = tk.Frame(self.root, bg=COL["sep"])
        outer.grid(row=4, column=0, sticky="nsew", padx=16, pady=(0, 8))
        inner = tk.Frame(outer, bg=COL["card"], padx=14, pady=12)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        inner.rowconfigure(1, weight=1)
        inner.columnconfigure(0, weight=1)

        hdr_row = tk.Frame(inner, bg=COL["card"])
        hdr_row.pack(fill=tk.X)
        tk.Label(hdr_row, text="LOG DE EJECUCION", font=F_CARD_TITLE,
                 fg=COL["card_title"], bg=COL["card"],
                 anchor="w").pack(side=tk.LEFT)
        _flat_btn(hdr_row, "Limpiar Log",
                  COL["btn_dark"], COL["btn_dark_active"],
                  command=self._clear_log).pack(side=tk.RIGHT, pady=0)
        tk.Frame(inner, height=1, bg=COL["sep_light"]).pack(
            fill=tk.X, pady=(4, 10))

        self.log_text = scrolledtext.ScrolledText(
            inner, font=F_LOG, wrap=tk.WORD,
            bg="#F8F9FA", fg=COL["text"],
            relief=tk.FLAT, borderwidth=0, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _build_footer(self) -> None:
        foot = tk.Frame(self.root, bg=COL["sep_light"],
                        height=36, highlightthickness=0)
        foot.grid(row=5, column=0, sticky="ew")
        foot.grid_propagate(False)

        fl = tk.Frame(foot, bg=COL["sep_light"])
        fl.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        self.footer_diag = tk.StringVar(
            value="ffmpeg: comprobando...  |  whisper: comprobando...")
        tk.Label(fl, textvariable=self.footer_diag, font=F_FOOTER,
                 fg=COL["text_secondary"],
                 bg=COL["sep_light"], anchor="w").pack(side=tk.LEFT)
        tk.Label(fl,
                 text=f"{APP_COMPANY}  -  uso interno",
                 font=("Segoe UI", 8, "italic"),
                 fg=COL["text_secondary"],
                 bg=COL["sep_light"]).pack(side=tk.RIGHT)

    # ── Diagnostico ───────────────────────────────────────────────
    def _refresh_footer(self) -> None:
        ffmpeg_ok = _check_tool("ffmpeg")
        try:
            import whisper  # noqa: F401
            whisper_ok = True
        except Exception as e:
            whisper_ok = False
            self.log(f"DEBUG - Error al cargar whisper: {e}")

        f = "detectado" if ffmpeg_ok  else "NO en PATH"
        w = "detectado" if whisper_ok else "NO instalado"
        self.footer_diag.set(
            f"ffmpeg: {f}  |  openai-whisper: {w}")

        if not ffmpeg_ok:
            self.log("AVISO: ffmpeg no encontrado en PATH.")
            self.log("  Descargar desde: https://ffmpeg.org/download.html")
            self.log("  Agregar la carpeta bin/ al PATH del sistema.")
            self.log("")
        if not whisper_ok:
            self.log("AVISO: openai-whisper no instalado.")
            self.log("  Ejecutar: pip install openai-whisper")
            self.log("")

    # ── Eventos de modelo ─────────────────────────────────────────
    def _on_model_change(self, _evt=None) -> None:
        m = self.model_var.get()
        self.model_info_lbl.config(text=MODEL_INFO.get(m, ""))

    # ── Navegacion de archivos ────────────────────────────────────
    def _browse_video(self) -> None:
        exts = " ".join(f"*{e}" for e in SUPPORTED_EXTENSIONS)
        f = filedialog.askopenfilename(
            title="Seleccionar Video o Audio",
            filetypes=[("Multimedia", exts), ("Todos", "*.*")],
        )
        if f and f not in self._selected_files:
            self._selected_files.append(f)
            self.files_listbox.insert(tk.END, Path(f).name)
            self.video_path.set(f)
            self.log(f"Archivo agregado: {f}")

    def _browse_multiple(self) -> None:
        exts = " ".join(f"*{e}" for e in SUPPORTED_EXTENSIONS)
        files = filedialog.askopenfilenames(
            title="Seleccionar Multiples Archivos",
            filetypes=[("Multimedia", exts), ("Todos", "*.*")],
        )
        added = 0
        for f in files:
            if f not in self._selected_files:
                self._selected_files.append(f)
                self.files_listbox.insert(tk.END, Path(f).name)
                added += 1
        if added:
            self.video_path.set(self._selected_files[0])
            self.log(f"{added} archivo(s) agregados a la cola.")

    def _remove_selected(self) -> None:
        sel = self.files_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.files_listbox.delete(idx)
        del self._selected_files[idx]
        if self._selected_files:
            self.video_path.set(self._selected_files[0])
        else:
            self.video_path.set("")

    def _clear_files(self) -> None:
        self._selected_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.video_path.set("")
        self.log("Lista de archivos limpiada.")

    def _browse_output(self) -> None:
        f = filedialog.askdirectory(title="Seleccionar Carpeta de Salida")
        if f:
            self.output_path.set(f)
            self.log(f"Carpeta de salida: {f}")

    # ── Creditos ──────────────────────────────────────────────────
    def _on_credits(self, _evt=None) -> None:
        messagebox.showinfo(
            f"{APP_NAME}  {APP_VERSION}",
            APP_NOTICE,
            parent=self.root,
        )

    # ── Log ───────────────────────────────────────────────────────
    def log(self, msg: str) -> None:
        self.log_text.insert(tk.END, f"{msg}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def _clear_log(self) -> None:
        self.log_text.delete(1.0, tk.END)

    def update_status(self, msg: str) -> None:
        self.status.set(msg)
        self.root.update_idletasks()

    # ── Abrir carpeta ─────────────────────────────────────────────
    def _open_folder(self) -> None:
        out = self.output_path.get()
        if os.path.isdir(out):
            if sys.platform == "win32":
                os.startfile(out)
            elif sys.platform == "darwin":
                os.system(f'open "{out}"')
            else:
                os.system(f'xdg-open "{out}"')

    # ── Cancelar ──────────────────────────────────────────────────
    def _on_cancel(self) -> None:
        self._cancel_flag.set()
        self.log("Cancelacion solicitada. El archivo actual terminara antes de detenerse.")
        self.update_status("Cancelando...")

    # ── Transcribir ───────────────────────────────────────────────
    def _on_transcribe(self) -> None:
        files = self._selected_files.copy()
        if not files:
            f = self.video_path.get().strip()
            if f:
                files = [f]
        if not files:
            messagebox.showwarning(
                "Sin archivo",
                "Seleccione al menos un archivo de video o audio.",
                parent=self.root)
            return

        output = self.output_path.get().strip()
        if not output:
            messagebox.showwarning(
                "Sin carpeta",
                "Seleccione una carpeta de salida.",
                parent=self.root)
            return

        self.btn_transcribe.config(state=tk.DISABLED)
        self.btn_cancel.config(state=tk.NORMAL)
        self.btn_open.config(state=tk.DISABLED)
        self.progress.start(10)
        self._cancel_flag.clear()
        self.log_text.delete(1.0, tk.END)

        lang_idx = self.lang_combo.current()
        lang = LANGUAGES[lang_idx] if lang_idx >= 0 else "auto"

        options = {
            "model":      self.model_var.get(),
            "language":   lang,
            "timestamps": self.timestamps.get(),
            "paragraphs": self.paragraphs.get(),
            "export_txt": self.export_txt.get(),
            "export_srt": self.export_srt.get(),
        }

        threading.Thread(
            target=self._transcribe_thread,
            args=(files, output, options),
            daemon=True,
        ).start()

    def _transcribe_thread(self, files: list[str],
                           output: str, options: dict) -> None:
        from transcriber import VideoTranscriber
        try:
            self.log("=" * 62)
            self.log(f"  {APP_NAME}  {APP_VERSION}")
            self.log(f"  {APP_COMPANY}  -  {APP_AUTHOR}")
            self.log("=" * 62)
            self.log("")

            os.makedirs(output, exist_ok=True)

            self.log(f"Cargando modelo Whisper '{options['model']}'...")
            self.log("(Primera vez puede tardar: descarga el modelo de internet)")
            self.update_status(f"Cargando modelo '{options['model']}'...")

            try:
                import whisper
            except Exception as e:
                self.log("ERROR: openai-whisper no instalado.")
                self.log("  Ejecuta: pip install openai-whisper")
                self.log(f"  Detalle del error: {e}")
                return

            model = whisper.load_model(options["model"])
            self.log(f"Modelo '{options['model']}' listo.")
            self.log("")

            transcriber = VideoTranscriber()
            generated: list[str] = []
            total = len(files)

            for idx, filepath in enumerate(files, 1):
                if self._cancel_flag.is_set():
                    self.log("\nTranscripcion cancelada por el usuario.")
                    break

                fp = Path(filepath)
                if not fp.is_file():
                    self.log(f"[{idx}/{total}] ERROR: Archivo no encontrado: {filepath}")
                    continue

                self.log(f"[{idx}/{total}] Transcribiendo: {fp.name}")
                self.update_status(
                    f"Transcribiendo {idx}/{total}: {fp.name}")

                lang = options["language"] if options["language"] != "auto" else None
                result = model.transcribe(
                    str(fp),
                    language=lang,
                    verbose=False,
                )

                detected_lang = result.get("language", "desconocido")
                seg_count = len(result.get("segments", []))
                self.log(f"  Idioma detectado : {detected_lang}")
                self.log(f"  Segmentos        : {seg_count}")

                md_path = transcriber.save_markdown(result, fp, output, options)
                generated.append(md_path)
                self.log(f"  [MD]  {Path(md_path).name}")

                if options["export_txt"]:
                    txt_path = transcriber.save_txt(result, fp, output)
                    generated.append(txt_path)
                    self.log(f"  [TXT] {Path(txt_path).name}")

                if options["export_srt"]:
                    srt_path = transcriber.save_srt(result, fp, output)
                    generated.append(srt_path)
                    self.log(f"  [SRT] {Path(srt_path).name}")

                self.log("")

            if not self._cancel_flag.is_set():
                self.log("=" * 62)
                self.log("PROCESO COMPLETADO")
                self.log("=" * 62)
                self.log(f"\n  Archivos en: {output}")
                for g in generated:
                    ext = Path(g).suffix.upper().replace(".", "")
                    self.log(f"  [{ext:<3}] {Path(g).name}")
                self.update_status("Transcripcion completada correctamente.")
                self.root.after(0, lambda: self.btn_open.config(state=tk.NORMAL))
            else:
                self.update_status("Transcripcion cancelada.")

        except Exception as exc:
            self.log(f"\nERROR: {exc}")
            self.update_status(f"Error: {exc}")
            import traceback
            self.log(traceback.format_exc())
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.btn_transcribe.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_cancel.config(state=tk.DISABLED))


def main() -> None:
    # Parche para bug de Tkinter en entornos virtuales (TclError) en Windows
    if sys.platform == "win32" and sys.prefix != sys.base_prefix:
        base_tcl = Path(sys.base_prefix) / "tcl"
        if base_tcl.is_dir():
            for d in base_tcl.iterdir():
                if d.is_dir() and d.name.startswith("tcl") and "TCL_LIBRARY" not in os.environ:
                    os.environ["TCL_LIBRARY"] = str(d)
                elif d.is_dir() and d.name.startswith("tk") and "TK_LIBRARY" not in os.environ:
                    os.environ["TK_LIBRARY"] = str(d)

    # Solucionar icono de la barra de tareas en Windows
    if sys.platform == "win32":
        import ctypes
        try:
            app_id = f"sonda.{APP_NAME.replace(' ', '').lower()}.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception:
            pass

    root = tk.Tk()

    # Verificar si falta el entorno portable al correr como .exe
    env_dir = base_path / "env"
    if getattr(sys, 'frozen', False) and not env_dir.is_dir():
        messagebox.showerror(
            "Entorno no encontrado",
            "Faltan las dependencias de Inteligencia Artificial.\n\n"
            "Por favor, ejecuta primero el archivo 'setup_dependencias.bat' "
            "para descargar e instalar los componentes necesarios.",
        )
        sys.exit(1)

    TranscriptorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
