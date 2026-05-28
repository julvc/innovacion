"""
Documentador de Proyectos v1.0
Genera documentacion tecnica y no-tecnica para proyectos Web, Mobile y QA.

Autor   : Julio Varas Contreras
Fecha   : Mayo 2026
"""
from __future__ import annotations

import os
import sys
import json
import threading
from pathlib import Path
from tkinter import ttk, filedialog, scrolledtext, messagebox
import tkinter as tk

# ——— Parches Windows ————————————————————————————————————————
class _DummyStream:
    def write(self, *args, **kwargs): pass
    def flush(self, *args, **kwargs): pass
    def isatty(self): return False

if sys.stdout is None: sys.stdout = _DummyStream()
if sys.stderr is None: sys.stderr = _DummyStream()

if sys.platform == "win32":
    import ctypes
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)

base_path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent

# ——— Constantes ———————————————————————————————————————————————
APP_NAME    = "Documentador de Proyectos"
APP_VERSION = "v1.0  -  Mayo 2026"
APP_AUTHOR  = "Julio Varas Contreras"
APP_NOTICE  = (
    "Documentador de Proyectos v1.0\n\n"
    "Genera documentacion estandarizada para proyectos\n"
    "Web, Mobile y QA, adaptada para perfiles tecnicos\n"
    "y no tecnicos.\n\n"
    "© 2026  Julio Varas Contreras — Todos los derechos reservados."
)

PROJECT_TYPES  = ["Web", "Mobile", "QA", "Web + QA", "Mobile + QA", "Full Stack"]
TARGET_PROFILES = ["Tecnico (Lider TI, Devs, QA, Arquitecto)", "No Tecnico (Gerencia, PM)", "Ambos"]
EXPORT_FORMATS  = ["Markdown (.md)", "Word (.docx)", "HTML (.html)", "PDF (.pdf)"]

AI_PROVIDERS = ["OpenAI (GPT-4)", "Anthropic (Claude)", "Google (Gemini)", "Ollama (local)"]

# ——— Paleta corporativa (misma que app referencia) ————————————
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
    "accent":          "#1976D2",
    "tab_active":      "#1565C0",
    "tab_inactive":    "#455A64",
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
F_TREE       = ("Segoe UI", 10)
F_SECTION    = ("Segoe UI", 13, "bold")


# ——— Helpers de recursos ——————————————————————————————————————
def _resource(filename: str) -> str:
    base = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    p = Path(base) / filename
    if not p.exists() and (Path(base) / "assets" / filename).exists():
        return str(Path(base) / "assets" / filename)
    return str(p)


def _set_window_icon(root: tk.Tk) -> None:
    try:
        p = _resource("DF 500X500 BLANCO 1.png")
        if Path(p).is_file():
            img = tk.PhotoImage(file=p)
            root.iconphoto(True, img)
            return
    except Exception:
        pass
    try:
        p = _resource("icon.ico")
        if Path(p).is_file():
            root.iconbitmap(p)
            return
    except Exception:
        pass


# ——— Helpers de UI (identicos a app referencia) ———————————————
_BTN_DISABLED_BG = "#CFD8DC"   # gris azulado claro
_BTN_DISABLED_FG = "#212121"   # texto negro, siempre legible


def _flat_btn(parent, text: str, bg: str, active: str,
              fg: str = "white", command=None,
              state=tk.NORMAL) -> tk.Button:
    is_disabled = (state == tk.DISABLED)
    btn = tk.Button(
        parent, text=text, command=command,
        font=F_BODY,
        bg=_BTN_DISABLED_BG if is_disabled else bg,
        fg=_BTN_DISABLED_FG if is_disabled else fg,
        activebackground=active, activeforeground="white",
        disabledforeground=_BTN_DISABLED_FG,
        relief=tk.FLAT, borderwidth=0,
        cursor="arrow" if is_disabled else "hand2",
        padx=14, pady=8, highlightthickness=0, state=state,
    )
    btn._bg_normal = bg
    btn._fg_normal = fg
    btn._bg_active = active
    return btn


def _set_btn_state(btn: tk.Button, enabled: bool) -> None:
    """Cambia estado con contraste correcto: disabled=negro/gris, normal=blanco/color."""
    if enabled:
        btn.config(
            state=tk.NORMAL,
            bg=getattr(btn, "_bg_normal", COL["primary"]),
            fg=getattr(btn, "_fg_normal", "white"),
            cursor="hand2",
        )
    else:
        btn.config(
            state=tk.DISABLED,
            bg=_BTN_DISABLED_BG,
            fg=_BTN_DISABLED_FG,
            disabledforeground=_BTN_DISABLED_FG,
            cursor="arrow",
        )


def _card(parent, **pack_kw) -> tk.Frame:
    outer = tk.Frame(parent, bg=COL["sep"], highlightthickness=0)
    inner = tk.Frame(outer, bg=COL["card"], padx=14, pady=12, highlightthickness=0)
    inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
    outer.pack(**pack_kw)
    return inner


def _card_title(inner: tk.Frame, text: str) -> None:
    tk.Label(inner, text=text, font=F_CARD_TITLE,
             fg=COL["card_title"], bg=COL["card"],
             anchor="w").pack(fill=tk.X)
    tk.Frame(inner, height=1, bg=COL["sep_light"]).pack(fill=tk.X, pady=(4, 10))


def _labeled_entry(parent: tk.Frame, label: str,
                   var: tk.StringVar, help_text: str = "") -> None:
    tk.Label(parent, text=label, font=F_LABEL,
             fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))
    tk.Entry(
        parent, textvariable=var, font=F_BODY, fg=COL["text"],
        relief=tk.FLAT, highlightthickness=1,
        highlightbackground=COL["sep"],
        highlightcolor=COL["primary"],
    ).pack(fill=tk.X, pady=(0, 2))
    if help_text:
        tk.Label(parent, text=help_text, font=F_HELP,
                 fg=COL["help"], bg=COL["card"]).pack(anchor="w", pady=(0, 8))


def _draw_doc_icon(canvas: tk.Canvas) -> None:
    """Icono de libro abierto para el header."""
    canvas.delete("all")
    # Sombra libro
    canvas.create_rectangle(10, 18, 86, 82, fill="#0A3880", outline="", width=0)
    # Pagina izquierda
    canvas.create_rectangle(8, 14, 48, 80, fill="white", outline="#90CAF9", width=1)
    # Pagina derecha
    canvas.create_rectangle(48, 14, 88, 80, fill="#E3F2FD", outline="#90CAF9", width=1)
    # Lomo central
    canvas.create_rectangle(45, 10, 51, 84, fill="#BBDEFB", outline="#64B5F6", width=1)
    # Lineas texto pagina izquierda
    for y in [26, 33, 40, 47, 54, 61, 68]:
        canvas.create_line(14, y, 42, y, fill="#1565C0", width=1, capstyle=tk.ROUND)
    # Lineas texto pagina derecha
    for y in [26, 33, 40, 47, 54, 61, 68]:
        canvas.create_line(54, y, 82, y, fill="#90A4AE", width=1, capstyle=tk.ROUND)
    # Curva lomo inferior
    canvas.create_arc(38, 70, 58, 90, start=0, extent=180, fill="#90CAF9", outline="#64B5F6")


# ——— Tooltip simple ——————————————————————————————————————————
class Tooltip:
    """Muestra ventana flotante con texto al hacer hover sobre widget."""
    def __init__(self, widget: tk.Widget, text: str) -> None:
        self._widget = widget
        self._text   = text
        self._tip: tk.Toplevel | None = None
        widget.bind("<Enter>", self._show, add="+")
        widget.bind("<Leave>", self._hide, add="+")

    def _show(self, _evt=None) -> None:
        if self._tip:
            return
        x = self._widget.winfo_rootx() + 10
        y = self._widget.winfo_rooty() + self._widget.winfo_height() + 4
        self._tip = tk.Toplevel(self._widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(self._tip, text=self._text, font=("Segoe UI", 8),
                       bg="#263238", fg="white", padx=8, pady=4,
                       relief=tk.FLAT, justify="left")
        lbl.pack()

    def _hide(self, _evt=None) -> None:
        if self._tip:
            self._tip.destroy()
            self._tip = None


def _action_group(parent: tk.Frame, label: str) -> tk.Frame:
    """Crea grupo visual con label inferior para la barra de acciones."""
    grp = tk.Frame(parent, bg=COL["card"])
    grp.pack(side=tk.LEFT, padx=(0, 2))
    inner = tk.Frame(grp, bg=COL["card"])
    inner.pack(fill=tk.X)
    tk.Frame(grp, height=1, bg=COL["sep_light"]).pack(fill=tk.X, pady=(4, 0))
    tk.Label(grp, text=label, font=("Segoe UI", 7),
             fg=COL["help"], bg=COL["card"]).pack()
    return inner


def _vsep(parent: tk.Frame) -> None:
    """Separador vertical entre grupos de acciones."""
    tk.Frame(parent, width=1, bg=COL["sep"]).pack(side=tk.LEFT, fill=tk.Y,
                                                    padx=10, pady=2)


# NuevoProyectoDialog — alias al wizard multi-paso
from wizard import NuevoProyectoWizard as NuevoProyectoDialog


# ——— Aplicacion Principal —————————————————————————————————————
class DocumentadorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{APP_NAME}  -  Documentador")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 720)
        self.root.configure(bg=COL["bg"])

        _set_window_icon(self.root)

        self.status       = tk.StringVar(value="Listo. Cree o abra un proyecto para comenzar.")
        self.current_project: dict | None = None
        self.project_path: Path | None = None
        self._ai_configured = tk.BooleanVar(value=False)

        self._setup_styles()
        self._build()

    # ── Estilos ttk ───────────────────────────────────────────────
    def _setup_styles(self) -> None:
        s = ttk.Style(self.root)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass

        s.configure("TCheckbutton", background=COL["card"],
                    foreground=COL["text"], font=F_BODY)
        s.map("TCheckbutton", background=[("active", COL["card"])])

        s.configure("Prog.Horizontal.TProgressbar",
                    troughcolor=COL["sep_light"],
                    background=COL["primary"],
                    bordercolor=COL["sep_light"],
                    lightcolor=COL["primary"],
                    darkcolor=COL["primary"],
                    thickness=14)

        s.configure("Doc.TNotebook", background=COL["bg"],
                    borderwidth=0, tabmargins=[0, 0, 0, 0])
        s.configure("Doc.TNotebook.Tab",
                    background=COL["btn_dark"],
                    foreground="#90A4AE",
                    font=("Segoe UI", 9),
                    padding=[14, 5])
        s.map("Doc.TNotebook.Tab",
              background=[("selected", COL["primary"]),
                          ("active",   COL["accent"])],
              foreground=[("selected", "white"),
                          ("active",   "white")],
              font=[("selected", ("Segoe UI", 11, "bold"))],
              padding=[("selected", [22, 10])])

        s.configure("Treeview",
                    background=COL["card"],
                    foreground=COL["text"],
                    fieldbackground=COL["card"],
                    font=F_TREE, rowheight=26)
        s.map("Treeview",
              background=[("selected", COL["primary"])],
              foreground=[("selected", "white")])
        s.configure("Treeview.Heading",
                    background=COL["sep_light"],
                    foreground=COL["card_title"],
                    font=("Segoe UI", 9, "bold"))

    # ── Build principal ────────────────────────────────────────────
    def _build(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        self._build_header()
        tk.Frame(self.root, bg=COL["sep"], height=1).grid(row=1, column=0, sticky="ew")
        self._build_notebook()
        self._build_actions()
        self._build_footer()

    # ── Header (identico a app referencia) ────────────────────────
    def _build_header(self) -> None:
        hdr = tk.Frame(self.root, bg=COL["header"], height=118, highlightthickness=0)
        hdr.grid(row=0, column=0, sticky="nsew")
        hdr.grid_propagate(False)

        hc = tk.Frame(hdr, bg=COL["header"])
        hc.pack(fill=tk.BOTH, expand=True, padx=18, pady=(14, 12))

        iw = tk.Frame(hc, bg=COL["header"], width=96, height=96, highlightthickness=0)
        iw.pack(side=tk.LEFT, padx=(0, 16))
        iw.pack_propagate(False)

        cv = tk.Canvas(iw, width=96, height=96, bg=COL["header"], highlightthickness=0)
        cv.pack()
        _draw_doc_icon(cv)

        titles = tk.Frame(hc, bg=COL["header"])
        titles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(titles, text=APP_NAME, font=F_HEADER,
                 fg="white", bg=COL["header"], anchor="w").pack(anchor="w")
        tk.Label(titles,
                 text="Genera documentacion estandarizada para proyectos Web, Mobile y QA",
                 font=F_SUBHEADER, fg=COL["subtitle_blue"],
                 bg=COL["header"], anchor="w").pack(anchor="w", pady=(2, 0))
        tk.Label(titles, text=f"{APP_VERSION}  |  {APP_AUTHOR}",
                 font=("Segoe UI", 8), fg=COL["credits_fg"],
                 bg=COL["header"], anchor="w").pack(anchor="w", pady=(2, 0))

        right_frame = tk.Frame(hc, bg=COL["header"])
        right_frame.pack(side=tk.RIGHT, anchor="ne")

        cred = tk.Label(right_frame, text="Acerca de",
                        font=F_CREDITS, fg=COL["credits_fg"],
                        bg=COL["header"], cursor="hand2")
        cred.pack(anchor="e", pady=(0, 6))
        cred.bind("<Button-1>", self._on_about)

        try:
            df_logo_path = _resource("DF 500X500 BLANCO 1.png")
            if Path(df_logo_path).is_file():
                img_df = tk.PhotoImage(file=df_logo_path).subsample(8, 8)
                lbl_df = tk.Label(right_frame, image=img_df, bg=COL["header"])
                lbl_df.image = img_df
                lbl_df.pack(anchor="e")
        except Exception:
            pass

    # ── Notebook con 4 tabs ───────────────────────────────────────
    def _build_notebook(self) -> None:
        nb_frame = tk.Frame(self.root, bg=COL["bg"])
        nb_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=(12, 4))
        nb_frame.rowconfigure(0, weight=1)
        nb_frame.columnconfigure(0, weight=1)

        self.nb = ttk.Notebook(nb_frame, style="Doc.TNotebook")
        self.nb.grid(row=0, column=0, sticky="nsew")

        self._tab_proyectos = tk.Frame(self.nb, bg=COL["bg"])
        self._tab_editor    = tk.Frame(self.nb, bg=COL["bg"])
        self._tab_ia        = tk.Frame(self.nb, bg=COL["bg"])
        self._tab_preview   = tk.Frame(self.nb, bg=COL["bg"])

        self.nb.add(self._tab_proyectos, text="  Proyectos  ")
        self.nb.add(self._tab_editor,    text="  Editor  ")
        self.nb.add(self._tab_ia,        text="  Config. IA  ")
        self.nb.add(self._tab_preview,   text="  Vista Previa  ")

        self._build_tab_proyectos()
        self._build_tab_editor()
        self._build_tab_ia()
        self._build_tab_preview()

    # ── Tab 1: Proyectos ──────────────────────────────────────────
    def _build_tab_proyectos(self) -> None:
        tab = self._tab_proyectos
        tab.columnconfigure(0, weight=2)
        tab.columnconfigure(1, weight=3)
        tab.rowconfigure(0, weight=1)

        # Panel izquierdo — lista de proyectos
        left = tk.Frame(tab, bg=COL["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)
        left.rowconfigure(1, weight=1)

        cl = _card(left, fill=tk.X)
        _card_title(cl, "PROYECTOS")

        btn_row = tk.Frame(cl, bg=COL["card"])
        btn_row.pack(fill=tk.X, pady=(0, 10))
        _flat_btn(btn_row, "Nuevo Proyecto", COL["primary"], COL["primary_active"],
                  command=self._on_nuevo_proyecto).pack(side=tk.LEFT, padx=(0, 6))
        _flat_btn(btn_row, "Abrir", COL["btn_dark"], COL["btn_dark_active"],
                  command=self._on_abrir_proyecto).pack(side=tk.LEFT)

        tk.Label(cl, text="Proyectos recientes:", font=F_LABEL,
                 fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 4))

        list_outer = tk.Frame(cl, bg=COL["sep"])
        list_outer.pack(fill=tk.BOTH, expand=True)
        sb = tk.Scrollbar(list_outer, orient=tk.VERTICAL)
        self.projects_listbox = tk.Listbox(
            list_outer, font=F_BODY, height=12,
            bg="#F8F9FA", fg=COL["text"],
            relief=tk.FLAT, borderwidth=0,
            selectbackground=COL["primary"],
            selectforeground="white",
            activestyle="none",
            yscrollcommand=sb.set,
        )
        sb.config(command=self.projects_listbox.yview)
        self.projects_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y, pady=1)
        self.projects_listbox.bind("<<ListboxSelect>>", self._on_project_select)

        _flat_btn(cl, "Eliminar Proyecto", COL["danger"], COL["danger_hover"],
                  command=self._on_eliminar_proyecto).pack(anchor="w", pady=(8, 0))

        # Panel derecho — info del proyecto seleccionado
        right = tk.Frame(tab, bg=COL["bg"])
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=8)

        cr = _card(right, fill=tk.BOTH, expand=True)
        _card_title(cr, "INFORMACION DEL PROYECTO")

        self.proj_info_text = scrolledtext.ScrolledText(
            cr, font=F_BODY, wrap=tk.WORD,
            bg="#F8F9FA", fg=COL["text"],
            relief=tk.FLAT, borderwidth=0, height=18,
            state=tk.DISABLED,
        )
        self.proj_info_text.pack(fill=tk.BOTH, expand=True)

        self._refresh_projects_list()

    # ── Tab 2: Editor ─────────────────────────────────────────────
    def _build_tab_editor(self) -> None:
        tab = self._tab_editor
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=3)
        tab.rowconfigure(0, weight=1)

        self._section_modified = False
        self._current_section_id: str | None = None

        # ── Panel izquierdo: arbol de secciones ──────────────────
        left = tk.Frame(tab, bg=COL["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)

        cl = _card(left, fill=tk.BOTH, expand=True)
        _card_title(cl, "SECCIONES")

        tree_frame = tk.Frame(cl, bg=COL["sep"])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        sb_tree = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.sections_tree = ttk.Treeview(
            tree_frame, selectmode="browse",
            yscrollcommand=sb_tree.set, show="tree",
        )
        sb_tree.config(command=self.sections_tree.yview)
        self.sections_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
        sb_tree.pack(side=tk.RIGHT, fill=tk.Y, pady=1)
        self.sections_tree.bind("<<TreeviewSelect>>", self._on_section_select)

        # Progreso del proyecto
        self._proj_progress_var = tk.StringVar(value="")
        tk.Label(cl, textvariable=self._proj_progress_var,
                 font=F_HELP, fg=COL["help"], bg=COL["card"],
                 anchor="w").pack(fill=tk.X, pady=(8, 0))

        # ── Panel derecho: editor ─────────────────────────────────
        right = tk.Frame(tab, bg=COL["bg"])
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=8)
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        # Cabecera de seccion
        hdr_card_outer = tk.Frame(right, bg=COL["sep"])
        hdr_card_outer.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        hdr_card = tk.Frame(hdr_card_outer, bg=COL["card"], padx=14, pady=8)
        hdr_card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        hdr_card.columnconfigure(0, weight=1)

        self.section_title_lbl = tk.Label(
            hdr_card, text="Seleccione una seccion del arbol",
            font=F_SECTION, fg=COL["card_title"], bg=COL["card"], anchor="w")
        self.section_title_lbl.grid(row=0, column=0, sticky="w")

        self.section_help_lbl = tk.Label(
            hdr_card, text="Abra o cree un proyecto para habilitar el editor.",
            font=F_HELP, fg=COL["help"], bg=COL["card"], anchor="w", wraplength=650)
        self.section_help_lbl.grid(row=1, column=0, sticky="w", pady=(2, 6))

        # Toolbar de estado + estadisticas
        toolbar = tk.Frame(hdr_card, bg=COL["card"])
        toolbar.grid(row=2, column=0, sticky="ew")

        # Estado de la seccion
        tk.Label(toolbar, text="Estado:", font=F_HELP,
                 fg=COL["text_secondary"], bg=COL["card"]).pack(side=tk.LEFT, padx=(0, 4))
        self._sec_status_var = tk.StringVar(value="pendiente")
        for status, color in [("pendiente", COL["text_secondary"]),
                               ("borrador",  COL["warn"]),
                               ("revision",  COL["accent"]),
                               ("listo",     COL["success"])]:
            tk.Radiobutton(
                toolbar, text=status, variable=self._sec_status_var,
                value=status, font=("Segoe UI", 8),
                bg=COL["card"], fg=color,
                selectcolor=COL["card"],
                activebackground=COL["card"],
                command=self._on_status_change,
            ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Frame(toolbar, width=1, bg=COL["sep"]).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=1)

        self._wordcount_var = tk.StringVar(value="0 palabras")
        tk.Label(toolbar, textvariable=self._wordcount_var,
                 font=F_HELP, fg=COL["text_secondary"],
                 bg=COL["card"]).pack(side=tk.LEFT)

        self._modified_lbl = tk.Label(toolbar, text="",
                                       font=("Segoe UI", 8, "bold"),
                                       fg=COL["warn"], bg=COL["card"])
        self._modified_lbl.pack(side=tk.LEFT, padx=(8, 0))

        # Toolbar Markdown
        md_card_outer = tk.Frame(right, bg=COL["sep_light"])
        md_card_outer.grid(row=1, column=0, sticky="nsew")
        md_card = tk.Frame(md_card_outer, bg=COL["card"], padx=8, pady=6)
        md_card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        md_card.rowconfigure(1, weight=1)
        md_card.columnconfigure(0, weight=1)

        # Fila de botones Markdown
        md_toolbar = tk.Frame(md_card, bg=COL["card"])
        md_toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        md_btns = [
            ("H1",       lambda: self._md_insert("# ")),
            ("H2",       lambda: self._md_insert("## ")),
            ("H3",       lambda: self._md_insert("### ")),
            ("|",        None),
            ("**B**",    lambda: self._md_wrap("**", "**")),
            ("*I*",      lambda: self._md_wrap("*", "*")),
            ("`Code`",   lambda: self._md_wrap("`", "`")),
            ("|",        None),
            ("Tabla",    lambda: self._md_insert_table()),
            ("Mermaid",  lambda: self._md_insert_mermaid()),
            ("🖼️ IMG",   lambda: self._md_insert_placeholder()),
            ("---",      lambda: self._md_insert("\n---\n")),
            ("|",        None),
            ("Ctrl+S = Guardar", None),
        ]
        for item in md_btns:
            label, cmd = item
            if label == "|":
                tk.Frame(md_toolbar, width=1, bg=COL["sep"]).pack(
                    side=tk.LEFT, fill=tk.Y, padx=4, pady=2)
            elif cmd is None:
                tk.Label(md_toolbar, text=label, font=("Segoe UI", 7),
                         fg=COL["help"], bg=COL["card"]).pack(side=tk.LEFT, padx=4)
            else:
                btn = tk.Button(
                    md_toolbar, text=label, command=cmd,
                    font=("Segoe UI", 8), bg=COL["sep_light"],
                    fg=COL["text"], activebackground=COL["primary"],
                    activeforeground="white",
                    relief=tk.FLAT, borderwidth=0, cursor="hand2",
                    padx=6, pady=3, highlightthickness=0,
                )
                btn.pack(side=tk.LEFT, padx=2)

        # Editor principal
        self.section_editor = scrolledtext.ScrolledText(
            md_card, font=F_BODY, wrap=tk.WORD,
            bg="#F8F9FA", fg=COL["text"],
            relief=tk.FLAT, borderwidth=0,
            insertbackground=COL["primary"],
        )
        self.section_editor.grid(row=1, column=0, sticky="nsew")
        self.section_editor.bind("<Key>",     self._on_editor_key)
        self.section_editor.bind("<KeyRelease>", self._on_editor_keyrelease)
        self.section_editor.bind("<Control-s>", lambda e: self._on_save_section())

        # Barra inferior del editor
        ed_foot = tk.Frame(md_card, bg=COL["card"])
        ed_foot.grid(row=2, column=0, sticky="ew", pady=(6, 0))

        _flat_btn(ed_foot, "  Guardar Sección  (Ctrl+S)  ",
                  COL["primary"], COL["primary_active"],
                  command=self._on_save_section).pack(side=tk.LEFT, padx=(0, 8))
        _flat_btn(ed_foot, "Limpiar",
                  COL["btn_dark"], COL["btn_dark_active"],
                  command=self._on_clear_section).pack(side=tk.LEFT, padx=(0, 8))
        _flat_btn(ed_foot, "Restaurar Template",
                  COL["btn_dark"], COL["btn_dark_active"],
                  command=self._on_restore_template).pack(side=tk.LEFT)

        self.btn_ai_section = _flat_btn(
            ed_foot, "  ✦ Enriquecer con IA  ",
            COL["success"], "#1B5E20",
            command=self._on_ai_section,
            state=tk.DISABLED)
        self.btn_ai_section.pack(side=tk.RIGHT)

    # ── Tab 3: Config IA ──────────────────────────────────────────
    def _build_tab_ia(self) -> None:
        tab = self._tab_ia
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)

        left = tk.Frame(tab, bg=COL["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)

        cl = _card(left, fill=tk.X)
        _card_title(cl, "CONFIGURACION DE IA")

        tk.Label(cl, text="Proveedor de IA", font=F_LABEL,
                 fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))
        self.ai_provider_var = tk.StringVar(value=AI_PROVIDERS[0])
        ttk.Combobox(cl, textvariable=self.ai_provider_var,
                     values=AI_PROVIDERS, state="readonly",
                     font=F_BODY).pack(fill=tk.X, pady=(0, 10))

        tk.Label(cl, text="Modelo", font=F_LABEL,
                 fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))
        self.ai_model_var = tk.StringVar(value="gpt-4o")
        tk.Entry(cl, textvariable=self.ai_model_var, font=F_BODY, fg=COL["text"],
                 relief=tk.FLAT, highlightthickness=1,
                 highlightbackground=COL["sep"],
                 highlightcolor=COL["primary"]).pack(fill=tk.X, pady=(0, 10))

        tk.Label(cl,
                 text="URL Base (solo para Ollama u OpenAI-compatible)",
                 font=F_LABEL, fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))
        self.ai_base_url_var = tk.StringVar(value="")
        tk.Entry(cl, textvariable=self.ai_base_url_var, font=F_BODY, fg=COL["text"],
                 relief=tk.FLAT, highlightthickness=1,
                 highlightbackground=COL["sep"],
                 highlightcolor=COL["primary"]).pack(fill=tk.X, pady=(0, 2))
        tk.Label(cl, text="Ej: http://localhost:11434/v1  (dejar vacio si usa proveedor oficial)",
                 font=F_HELP, fg=COL["help"], bg=COL["card"]).pack(anchor="w", pady=(0, 10))

        tk.Frame(cl, height=1, bg=COL["sep_light"]).pack(fill=tk.X, pady=(4, 8))

        tk.Label(cl, text="API Key", font=F_LABEL,
                 fg=COL["text"], bg=COL["card"]).pack(anchor="w", pady=(0, 3))
        self.ai_key_var = tk.StringVar()
        key_row = tk.Frame(cl, bg=COL["card"])
        key_row.pack(fill=tk.X, pady=(0, 4))
        self.key_entry = tk.Entry(key_row, textvariable=self.ai_key_var,
                                   show="*", font=F_BODY, fg=COL["text"],
                                   relief=tk.FLAT, highlightthickness=1,
                                   highlightbackground=COL["sep"],
                                   highlightcolor=COL["primary"])
        self.key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self._show_key = False
        self.btn_show_key = _flat_btn(key_row, "Mostrar", COL["btn_dark"],
                                       COL["btn_dark_active"],
                                       command=self._toggle_key_visibility)
        self.btn_show_key.pack(side=tk.RIGHT)

        tk.Label(cl,
                 text="La clave se almacena de forma segura en el llavero del sistema (keyring).\nNunca se guarda en texto plano.",
                 font=F_HELP, fg=COL["help"], bg=COL["card"],
                 justify="left").pack(anchor="w", pady=(0, 10))

        btn_ia_row = tk.Frame(cl, bg=COL["card"])
        btn_ia_row.pack(fill=tk.X)
        _flat_btn(btn_ia_row, "Guardar y Probar Conexion",
                  COL["primary"], COL["primary_active"],
                  command=self._on_save_ai_config).pack(side=tk.LEFT, padx=(0, 8))
        _flat_btn(btn_ia_row, "Limpiar Clave", COL["danger"], COL["danger_hover"],
                  command=self._on_clear_ai_key).pack(side=tk.LEFT)

        # Panel derecho — estado + log IA
        right = tk.Frame(tab, bg=COL["bg"])
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=8)
        right.rowconfigure(0, weight=1)

        cr = _card(right, fill=tk.BOTH, expand=True)
        _card_title(cr, "ESTADO DE CONEXION IA")

        self.ai_status_var = tk.StringVar(value="Sin configurar")
        tk.Label(cr, textvariable=self.ai_status_var,
                 font=F_STATUS, fg=COL["warn"], bg=COL["card"],
                 anchor="w").pack(fill=tk.X, pady=(0, 10))

        self.ai_log = scrolledtext.ScrolledText(
            cr, font=F_LOG, wrap=tk.WORD,
            bg="#F8F9FA", fg=COL["text"],
            relief=tk.FLAT, borderwidth=0, height=12,
            state=tk.DISABLED,
        )
        self.ai_log.pack(fill=tk.BOTH, expand=True)

        tk.Frame(cr, height=1, bg=COL["sep_light"]).pack(fill=tk.X, pady=(8, 6))
        tk.Label(cr,
                 text="Proveedores soportados: OpenAI, Anthropic, Google Gemini, Ollama (local)\n"
                      "La IA solo se usa cuando el usuario lo solicita explicitamente.",
                 font=F_HELP, fg=COL["help"], bg=COL["card"],
                 justify="left").pack(anchor="w")

        self._load_ai_config()

    # ── Tab 4: Vista Previa ───────────────────────────────────────
    def _build_tab_preview(self) -> None:
        tab = self._tab_preview
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=0)
        tab.rowconfigure(1, weight=1)

        ctrl = tk.Frame(tab, bg=COL["bg"])
        ctrl.grid(row=0, column=0, sticky="ew", pady=(8, 0))

        cp = _card(ctrl, fill=tk.X)
        btn_row = tk.Frame(cp, bg=COL["card"])
        btn_row.pack(fill=tk.X)

        self.preview_mode_var = tk.StringVar(value="Markdown")
        for mode in ["Markdown", "Tecnico", "No Tecnico"]:
            tk.Radiobutton(btn_row, text=mode, variable=self.preview_mode_var,
                           value=mode, font=F_BODY,
                           bg=COL["card"], fg=COL["text"],
                           selectcolor=COL["card"],
                           activebackground=COL["card"],
                           command=self._refresh_preview).pack(side=tk.LEFT, padx=(0, 16))

        _flat_btn(btn_row, "Refrescar", COL["btn_dark"], COL["btn_dark_active"],
                  command=self._refresh_preview).pack(side=tk.RIGHT, padx=(8, 0))
        _flat_btn(btn_row, "Copiar al Portapapeles", COL["primary"], COL["primary_active"],
                  command=self._copy_preview).pack(side=tk.RIGHT)

        pv = tk.Frame(tab, bg=COL["bg"])
        pv.grid(row=1, column=0, sticky="nsew", pady=(8, 8))
        pv.rowconfigure(0, weight=1)
        pv.columnconfigure(0, weight=1)

        cp2 = _card(pv, fill=tk.BOTH, expand=True)
        self.preview_text = scrolledtext.ScrolledText(
            cp2, font=F_LOG, wrap=tk.WORD,
            bg="#F8F9FA", fg=COL["text"],
            relief=tk.FLAT, borderwidth=0,
            state=tk.DISABLED,
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)

    # ── Barra de acciones ─────────────────────────────────────────
    def _build_actions(self) -> None:
        acts = tk.Frame(self.root, bg=COL["bg"])
        acts.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 8))

        outer = tk.Frame(acts, bg=COL["sep"])
        outer.pack(fill=tk.X)
        inner = tk.Frame(outer, bg=COL["card"], padx=14, pady=10)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # ── Fila 1: grupos de botones ──────────────────────────
        btn_row = tk.Frame(inner, bg=COL["card"])
        btn_row.pack(fill=tk.X, pady=(0, 6))

        # Grupo 1 — Documentacion
        grp1 = _action_group(btn_row, "Documentacion")
        self.btn_generate = _flat_btn(
            grp1, "  Generar Documento  ",
            COL["primary"], COL["primary_active"],
            command=self._on_generate, state=tk.DISABLED)
        self.btn_generate.pack(side=tk.LEFT, padx=(0, 6))
        Tooltip(self.btn_generate,
                "Genera el borrador del documento\n"
                "con el contenido de todas las secciones.\n"
                "Requiere proyecto abierto.")

        self.btn_enrich_ai = _flat_btn(
            grp1, "  Enriquecer con IA  ",
            COL["success"], "#1B5E20",
            command=self._on_enrich_ai, state=tk.DISABLED)
        self.btn_enrich_ai.pack(side=tk.LEFT)
        Tooltip(self.btn_enrich_ai,
                "Usa IA para mejorar y expandir\n"
                "el contenido de todas las secciones.\n"
                "Requiere configurar proveedor de IA.")

        _vsep(btn_row)

        # Grupo 2 — Exportar
        grp2 = _action_group(btn_row, "Exportar como")
        self.export_var = tk.StringVar(value=EXPORT_FORMATS[0])
        self._export_combo = ttk.Combobox(
            grp2, textvariable=self.export_var,
            values=EXPORT_FORMATS, state="readonly",
            font=F_BODY, width=16)
        self._export_combo.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_export = _flat_btn(
            grp2, "  Exportar  ",
            COL["btn_dark"], COL["btn_dark_active"],
            command=self._on_export, state=tk.DISABLED)
        self.btn_export.pack(side=tk.LEFT)
        Tooltip(self.btn_export,
                "Exporta el documento al formato seleccionado.\n"
                "MD = GitHub/Confluence\n"
                "DOCX = Word (gerencia)\n"
                "HTML = intranet\n"
                "PDF = distribucion formal")

        _vsep(btn_row)

        # Grupo 3 — Proyecto
        grp3 = _action_group(btn_row, "Proyecto")
        self.btn_save = _flat_btn(
            grp3, "  Guardar  ",
            COL["accent"], "#0D47A1",
            command=self._on_save_project, state=tk.DISABLED)
        self.btn_save.pack(side=tk.LEFT)
        Tooltip(self.btn_save,
                "Guarda el estado actual del proyecto\n"
                "en formato JSON en la carpeta 'projects/'.")

        # ── Fila 2: progreso + status ──────────────────────────
        self.progress = ttk.Progressbar(
            inner, mode="indeterminate",
            style="Prog.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(2, 4))

        status_row = tk.Frame(inner, bg=COL["card"])
        status_row.pack(fill=tk.X)

        self._status_icon = tk.Label(
            status_row, text="●", font=("Segoe UI", 10),
            fg=COL["text_secondary"], bg=COL["card"])
        self._status_icon.pack(side=tk.LEFT, padx=(0, 6))

        tk.Label(status_row, textvariable=self.status,
                 font=F_STATUS, fg=COL["text"], bg=COL["card"],
                 anchor="w", wraplength=950, justify="left").pack(
            side=tk.LEFT, fill=tk.X, expand=True)

    # ── Footer ────────────────────────────────────────────────────
    def _build_footer(self) -> None:
        foot = tk.Frame(self.root, bg=COL["sep_light"], height=36, highlightthickness=0)
        foot.grid(row=4, column=0, sticky="ew")
        foot.grid_propagate(False)

        fl = tk.Frame(foot, bg=COL["sep_light"])
        fl.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        self.footer_deps = tk.StringVar(value="Verificando dependencias...")
        tk.Label(fl, textvariable=self.footer_deps, font=F_FOOTER,
                 fg=COL["text_secondary"], bg=COL["sep_light"], anchor="w").pack(side=tk.LEFT)
        tk.Label(fl, text="Documentador de Proyectos  -  uso interno",
                 font=("Segoe UI", 8, "italic"),
                 fg=COL["text_secondary"], bg=COL["sep_light"]).pack(side=tk.RIGHT)

        self.root.after(400, self._check_deps)

    # ── Verificacion de dependencias ──────────────────────────────
    def _check_deps(self) -> None:
        deps = {"jinja2": False, "docx": False, "markdown": False,
                "fpdf":   False, "keyring": False}
        try: import jinja2;   deps["jinja2"]   = True
        except ImportError: pass
        try: import docx;     deps["docx"]     = True
        except ImportError: pass
        try: import markdown; deps["markdown"] = True
        except ImportError: pass
        try: import fpdf;     deps["fpdf"]     = True
        except ImportError: pass
        try: import keyring;  deps["keyring"]  = True
        except ImportError: pass

        ok    = [k for k, v in deps.items() if v]
        miss  = [k for k, v in deps.items() if not v]
        parts = []
        if ok:   parts.append("OK: " + ", ".join(ok))
        if miss: parts.append("Falta: " + ", ".join(miss))
        self.footer_deps.set("  |  ".join(parts) if parts else "Todas las dependencias OK")

        if miss:
            self._log_ai(f"AVISO: Faltan dependencias: {', '.join(miss)}")
            self._log_ai("  Ejecuta: pip install -r requirements.txt")

    # ── Gestion de proyectos ──────────────────────────────────────
    def _projects_dir(self) -> Path:
        d = base_path / "projects"
        d.mkdir(exist_ok=True)
        return d

    def _refresh_projects_list(self) -> None:
        self.projects_listbox.delete(0, tk.END)
        for p in sorted(self._projects_dir().glob("*.json")):
            self.projects_listbox.insert(tk.END, p.stem)

    def _on_nuevo_proyecto(self) -> None:
        dlg = NuevoProyectoDialog(self.root)
        if dlg.result:
            self._load_project(dlg.result)
            path = self._projects_dir() / f"{dlg.result['name']}.json"
            self.project_path = path
            self._save_project_file()
            self._refresh_projects_list()
            self.set_status(f"Proyecto '{dlg.result['name']}' creado. Empiece a editar las secciones.", 'success')

    def _on_abrir_proyecto(self) -> None:
        f = filedialog.askopenfilename(
            title="Abrir Proyecto",
            initialdir=str(self._projects_dir()),
            filetypes=[("Proyectos JSON", "*.json"), ("Todos", "*.*")],
        )
        if f:
            try:
                with open(f, encoding="utf-8") as fh:
                    data = json.load(fh)
                self.project_path = Path(f)
                self._load_project(data)
                self.set_status(f"Proyecto '{data.get('name', f)}' cargado.", 'success')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el proyecto:\n{e}", parent=self.root)

    def _on_project_select(self, _evt=None) -> None:
        sel = self.projects_listbox.curselection()
        if not sel:
            return
        name = self.projects_listbox.get(sel[0])
        path = self._projects_dir() / f"{name}.json"
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            self.project_path = path
            self._load_project(data)
            self.set_status(f"Proyecto '{name}' cargado.", 'success')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar '{name}':\n{e}", parent=self.root)

    def _on_eliminar_proyecto(self) -> None:
        sel = self.projects_listbox.curselection()
        if not sel:
            messagebox.showwarning("Seleccionar", "Seleccione un proyecto para eliminar.", parent=self.root)
            return
        name = self.projects_listbox.get(sel[0])
        if messagebox.askyesno("Confirmar", f"Eliminar proyecto '{name}'?\nEsta accion no se puede deshacer.", parent=self.root):
            path = self._projects_dir() / f"{name}.json"
            try:
                path.unlink()
            except Exception:
                pass
            self._refresh_projects_list()
            if self.current_project and self.current_project.get("name") == name:
                self.current_project = None
                self.project_path = None
                self._disable_editing()
            self.set_status(f"Proyecto '{name}' eliminado.", 'warn')

    def _load_project(self, data: dict) -> None:
        self.current_project = data
        self._current_section_id = None
        self._section_modified   = False
        self._populate_project_info()
        self._populate_sections_tree()
        self._update_project_progress()
        self._enable_editing()

    def _populate_project_info(self) -> None:
        if not self.current_project:
            return
        p = self.current_project
        lines = [
            f"Nombre   : {p.get('name', '')}",
            f"Tipo     : {p.get('type', '')}",
            f"Perfil   : {p.get('profile', '')}",
            f"Stack    : {p.get('stack', '')}",
            "",
            "Descripcion:",
            p.get("desc", "(sin descripcion)"),
            "",
            f"Secciones completadas: {len([v for v in p.get('sections', {}).values() if v.strip()])} / {len(p.get('sections', {}))}",
        ]
        self.proj_info_text.config(state=tk.NORMAL)
        self.proj_info_text.delete(1.0, tk.END)
        self.proj_info_text.insert(tk.END, "\n".join(lines))
        self.proj_info_text.config(state=tk.DISABLED)

    def _populate_sections_tree(self) -> None:
        from project_manager import get_sections_for_type
        self.sections_tree.delete(*self.sections_tree.get_children())
        if not self.current_project:
            return
        ptype   = self.current_project.get("type", "Web")
        profile = self.current_project.get("profile", "Ambos")
        sections_def = get_sections_for_type(ptype, profile)

        for group, items in sections_def.items():
            node = self.sections_tree.insert("", tk.END, text=f"  {group}",
                                              open=True, tags=("group",))
            for item in items:
                filled = bool(self.current_project.get("sections", {}).get(item, "").strip())
                tag = "done" if filled else "pending"
                self.sections_tree.insert(node, tk.END, text=f"    {'✓' if filled else '○'} {item}",
                                           iid=item, tags=(tag,))

        self.sections_tree.tag_configure("group",   foreground=COL["card_title"], font=("Segoe UI", 9, "bold"))
        self.sections_tree.tag_configure("done",    foreground=COL["success"])
        self.sections_tree.tag_configure("pending", foreground=COL["text_secondary"])

    def _on_section_select(self, _evt=None) -> None:
        sel = self.sections_tree.selection()
        if not sel or not self.current_project:
            return
        section_id = sel[0]
        if not self.sections_tree.parent(section_id):
            return  # es un grupo, no una seccion

        # Advertir si hay cambios sin guardar
        if self._section_modified and self._current_section_id:
            if not messagebox.askyesno(
                "Cambios sin guardar",
                f"La seccion '{self._current_section_id}' tiene cambios sin guardar.\n"
                "¿Descartar y cambiar de seccion?",
                parent=self.root,
            ):
                # Revertir seleccion al item anterior
                if self._current_section_id:
                    self.sections_tree.selection_set(self._current_section_id)
                return

        self._current_section_id = section_id
        self._clear_modified()

        from project_manager import get_section_hint
        self.section_title_lbl.config(text=section_id)
        content = self.current_project.get("sections", {}).get(section_id, "")
        self.section_editor.delete(1.0, tk.END)
        if content.strip():
            self.section_editor.insert(tk.END, content)
        else:
            hint = get_section_hint(section_id)
            self.section_editor.insert(tk.END, hint)
            self.section_editor.tag_add("hint", "1.0", tk.END)
            self.section_editor.tag_configure("hint", foreground=COL["help"])

        # Restaurar estado de la seccion
        status = self.current_project.get("section_status", {}).get(section_id, "pendiente")
        self._sec_status_var.set(status)

        # Word count inicial
        words = len([w for w in content.split() if w])
        self._wordcount_var.set(f"{words} palabras  ·  {len(content)} chars")

        self.section_help_lbl.config(
            text=f"Proyecto: {self.current_project.get('name', '')}  |  {section_id}")

    def _on_save_section(self) -> None:
        section_id = self._current_section_id
        if not section_id or not self.current_project:
            return
        if not self.sections_tree.parent(section_id):
            return
        content = self.section_editor.get("1.0", tk.END).strip()
        if "sections" not in self.current_project:
            self.current_project["sections"] = {}
        self.current_project["sections"][section_id] = content

        # Guardar estado de la seccion
        if "section_status" not in self.current_project:
            self.current_project["section_status"] = {}
        self.current_project["section_status"][section_id] = self._sec_status_var.get()

        self._clear_modified()
        self._save_project_file()        # auto-save JSON
        self._populate_sections_tree()
        self._populate_project_info()
        self._update_project_progress()
        self.set_status(f"Seccion '{section_id}' guardada.", 'success')

    def _on_clear_section(self) -> None:
        self.section_editor.delete(1.0, tk.END)

    def _on_editor_key(self, event) -> None:
        if event.keysym in ("Control_L", "Control_R", "s") and event.state & 0x4:
            return  # ignorar Ctrl+S (lo maneja el binding separado)
        if self.section_editor.tag_ranges("hint"):
            if event.char and not event.state & 0x4:
                self.section_editor.delete(1.0, tk.END)
                self.section_editor.tag_delete("hint")
        if event.char or event.keysym in ("BackSpace", "Delete", "Return"):
            self._mark_modified()

    def _on_ai_section(self) -> None:
        messagebox.showinfo("IA", "Funcion de IA por secciones disponible en Paso 8.", parent=self.root)

    # ── Toolbar Markdown ──────────────────────────────────────────
    def _md_insert(self, text: str) -> None:
        try:
            idx = self.section_editor.index(tk.INSERT)
            self.section_editor.insert(idx, text)
        except Exception:
            pass

    def _md_wrap(self, prefix: str, suffix: str) -> None:
        try:
            sel = self.section_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.section_editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.section_editor.insert(tk.INSERT, f"{prefix}{sel}{suffix}")
        except tk.TclError:
            self.section_editor.insert(tk.INSERT, f"{prefix}texto{suffix}")

    def _md_insert_table(self) -> None:
        table = (
            "\n| Columna 1 | Columna 2 | Columna 3 |\n"
            "|-----------|-----------|------------|\n"
            "| Valor 1   | Valor 2   | Valor 3    |\n"
            "| Valor 4   | Valor 5   | Valor 6    |\n"
        )
        self._md_insert(table)

    def _md_insert_mermaid(self) -> None:
        block = (
            "\n```mermaid\nflowchart TD\n"
            "    A[Inicio] --> B{Decision}\n"
            "    B -- Si --> C[Accion]\n"
            "    B -- No --> D[Fin]\n```\n"
        )
        self._md_insert(block)

    def _md_insert_placeholder(self) -> None:
        self._md_insert(
            "\n> 🖼️ **[PLACEHOLDER IMAGEN:** "
            "Insertar aqui captura de pantalla de {Descripcion} **]**\n"
        )

    def _on_restore_template(self) -> None:
        if not self._current_section_id or not self.current_project:
            return
        from section_templates import get_template
        tmpl = get_template(self._current_section_id,
                            self.current_project.get("type", "Web"))
        if not tmpl:
            messagebox.showinfo("Sin template",
                                f"No hay template disponible para '{self._current_section_id}'.",
                                parent=self.root)
            return
        if messagebox.askyesno("Restaurar template",
                               f"Sobreescribir contenido de '{self._current_section_id}' "
                               f"con el template de ejemplo?",
                               parent=self.root):
            self.section_editor.delete(1.0, tk.END)
            self.section_editor.insert(tk.END, tmpl)
            self._mark_modified()

    # ── Tracking cambios ──────────────────────────────────────────
    def _on_editor_keyrelease(self, _evt=None) -> None:
        content = self.section_editor.get("1.0", tk.END)
        words = len([w for w in content.split() if w])
        self._wordcount_var.set(f"{words} palabras  ·  {len(content)} chars")

    def _mark_modified(self) -> None:
        self._section_modified = True
        self._modified_lbl.config(text="● Sin guardar")

    def _clear_modified(self) -> None:
        self._section_modified = False
        self._modified_lbl.config(text="")

    def _update_project_progress(self) -> None:
        if not self.current_project or not hasattr(self, "_proj_progress_var"):
            return
        from project_manager import get_sections_for_type
        sections_def = get_sections_for_type(
            self.current_project.get("type", "Web"),
            self.current_project.get("profile", "Ambos"),
        )
        total  = sum(len(v) for v in sections_def.values())
        filled = sum(
            1 for grp in sections_def.values()
            for sid in grp
            if self.current_project.get("sections", {}).get(sid, "").strip()
        )
        pct = int(filled / total * 100) if total else 0
        self._proj_progress_var.set(f"Progreso: {filled}/{total} secciones ({pct}%)")

    def _on_status_change(self) -> None:
        if not self._current_section_id or not self.current_project:
            return
        if "section_status" not in self.current_project:
            self.current_project["section_status"] = {}
        self.current_project["section_status"][self._current_section_id] = \
            self._sec_status_var.get()

    # ── Config IA ─────────────────────────────────────────────────
    def _load_ai_config(self) -> None:
        cfg_path = base_path / ".ai_config.json"
        if cfg_path.is_file():
            try:
                with open(cfg_path, encoding="utf-8") as fh:
                    cfg = json.load(fh)
                self.ai_provider_var.set(cfg.get("provider", AI_PROVIDERS[0]))
                self.ai_model_var.set(cfg.get("model", "gpt-4o"))
                self.ai_base_url_var.set(cfg.get("base_url", ""))
            except Exception:
                pass

        try:
            import keyring
            provider = self.ai_provider_var.get()
            key = keyring.get_password("documentador_ia", provider)
            if key:
                self.ai_key_var.set(key)
                self.ai_status_var.set(f"Clave cargada desde llavero: {provider}")
                self._ai_configured.set(True)
                self._enable_ai_buttons()
        except ImportError:
            self._log_ai("AVISO: keyring no instalado. La clave se guardara solo en memoria.")
        except Exception:
            pass

    def _on_save_ai_config(self) -> None:
        provider = self.ai_provider_var.get()
        model    = self.ai_model_var.get().strip()
        base_url = self.ai_base_url_var.get().strip()
        key      = self.ai_key_var.get().strip()

        if not key:
            messagebox.showwarning("API Key", "Ingrese una API Key.", parent=self.root)
            return

        cfg_path = base_path / ".ai_config.json"
        with open(cfg_path, "w", encoding="utf-8") as fh:
            json.dump({"provider": provider, "model": model, "base_url": base_url}, fh)

        try:
            import keyring
            keyring.set_password("documentador_ia", provider, key)
            self._log_ai(f"Clave guardada en llavero del sistema para: {provider}")
        except ImportError:
            self._log_ai("AVISO: keyring no disponible. Clave solo en memoria de sesion.")
        except Exception as e:
            self._log_ai(f"Error al guardar en llavero: {e}")

        self._log_ai(f"Probando conexion con {provider} / {model}...")
        self.root.after(100, lambda: self._test_ai_connection(provider, model, base_url, key))

    def _test_ai_connection(self, provider: str, model: str, base_url: str, key: str) -> None:
        from ai_connector import test_connection
        ok, msg = test_connection(provider, model, base_url, key)
        if ok:
            self.ai_status_var.set(f"Conectado: {provider} / {model}")
            self._log_ai(f"OK — Conexion exitosa: {msg}")
            self._ai_configured.set(True)
            self._enable_ai_buttons()
        else:
            self.ai_status_var.set(f"Error de conexion: {provider}")
            self._log_ai(f"ERROR — {msg}")

    def _on_clear_ai_key(self) -> None:
        if not messagebox.askyesno("Limpiar", "Eliminar la clave API guardada?", parent=self.root):
            return
        provider = self.ai_provider_var.get()
        try:
            import keyring
            keyring.delete_password("documentador_ia", provider)
        except Exception:
            pass
        self.ai_key_var.set("")
        self.ai_status_var.set("Clave eliminada.")
        self._ai_configured.set(False)
        self._disable_ai_buttons()
        self._log_ai(f"Clave eliminada para: {provider}")

    def _toggle_key_visibility(self) -> None:
        self._show_key = not self._show_key
        self.key_entry.config(show="" if self._show_key else "*")
        self.btn_show_key.config(text="Ocultar" if self._show_key else "Mostrar")

    def _log_ai(self, msg: str) -> None:
        self.ai_log.config(state=tk.NORMAL)
        self.ai_log.insert(tk.END, f"{msg}\n")
        self.ai_log.see(tk.END)
        self.ai_log.config(state=tk.DISABLED)

    # ── Vista Previa ──────────────────────────────────────────────
    def _refresh_preview(self) -> None:
        if not self.current_project:
            return
        from doc_generator import render_preview
        mode = self.preview_mode_var.get()
        text = render_preview(self.current_project, mode)
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, text)
        self.preview_text.config(state=tk.DISABLED)
        self.set_status(f"Vista previa actualizada — modo: {mode}", 'info')

    def _copy_preview(self) -> None:
        content = self.preview_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.set_status('Contenido copiado al portapapeles.', 'success')

    # ── Generar + Exportar ────────────────────────────────────────
    def _on_generate(self) -> None:
        if not self.current_project:
            return
        self.progress.start(10)
        self.set_status('Generando documentacion...', 'info')
        self.root.update_idletasks()
        threading.Thread(target=self._generate_thread, daemon=True).start()

    def _generate_thread(self) -> None:
        try:
            from doc_generator import generate_all
            generate_all(self.current_project)
            self.root.after(0, lambda: self.set_status('Documentacion generada. Revise Vista Previa.', 'success'))
            self.root.after(0, self._refresh_preview)
        except Exception as e:
            self.root.after(0, lambda: self.set_status(f'Error: {e}', 'error'))
        finally:
            self.root.after(0, self.progress.stop)

    def _on_enrich_ai(self) -> None:
        messagebox.showinfo("IA", "Enriquecimiento IA disponible en Paso 8.", parent=self.root)

    def _on_export(self) -> None:
        if not self.current_project:
            return
        fmt = self.export_var.get()
        ext_map = {
            "Markdown (.md)": ".md",
            "Word (.docx)":   ".docx",
            "HTML (.html)":   ".html",
            "PDF (.pdf)":     ".pdf",
        }
        ext = ext_map.get(fmt, ".md")
        out_dir = base_path / "exports"
        out_dir.mkdir(exist_ok=True)
        default_name = f"{self.current_project.get('name', 'proyecto')}{ext}"

        path = filedialog.asksaveasfilename(
            title="Exportar Documento",
            initialdir=str(out_dir),
            initialfile=default_name,
            defaultextension=ext,
            filetypes=[(fmt, f"*{ext}"), ("Todos", "*.*")],
        )
        if not path:
            return

        self.progress.start(10)
        self.set_status(f'Exportando {fmt}...', 'info')
        self.root.update_idletasks()
        threading.Thread(
            target=self._export_thread,
            args=(path, fmt),
            daemon=True,
        ).start()

    def _export_thread(self, path: str, fmt: str) -> None:
        try:
            from doc_generator import export_document
            export_document(self.current_project, path, fmt)
            self.root.after(0, lambda: self.set_status(f'Exportado: {Path(path).name}', 'success'))
            self.root.after(0, lambda: self._open_file(path))
        except Exception as e:
            self.root.after(0, lambda: self.set_status(f'Error al exportar: {e}', 'error'))
        finally:
            self.root.after(0, self.progress.stop)

    def _open_file(self, path: str) -> None:
        if sys.platform == "win32":
            os.startfile(path)

    # ── Guardar proyecto ──────────────────────────────────────────
    def _on_save_project(self) -> None:
        if not self.current_project:
            return
        if not self.project_path:
            name = self.current_project.get("name", "proyecto")
            self.project_path = self._projects_dir() / f"{name}.json"
        self._save_project_file()
        self.set_status(f'Proyecto guardado: {self.project_path.name}', 'success')

    def _save_project_file(self) -> None:
        if self.project_path and self.current_project:
            with open(self.project_path, "w", encoding="utf-8") as fh:
                json.dump(self.current_project, fh, ensure_ascii=False, indent=2)

    # ── Habilitar / deshabilitar controles ────────────────────────
    def _enable_editing(self) -> None:
        _set_btn_state(self.btn_generate, True)
        _set_btn_state(self.btn_save,     True)
        _set_btn_state(self.btn_export,   True)
        if self._ai_configured.get():
            self._enable_ai_buttons()

    def _disable_editing(self) -> None:
        _set_btn_state(self.btn_generate, False)
        _set_btn_state(self.btn_save,     False)
        _set_btn_state(self.btn_export,   False)
        self._disable_ai_buttons()

    def _enable_ai_buttons(self) -> None:
        _set_btn_state(self.btn_enrich_ai,  True)
        _set_btn_state(self.btn_ai_section, True)

    def _disable_ai_buttons(self) -> None:
        _set_btn_state(self.btn_enrich_ai,  False)
        _set_btn_state(self.btn_ai_section, False)

    # ── Status coloreado ──────────────────────────────────────────
    def set_status(self, msg: str, kind: str = "info") -> None:
        """kind: 'info' | 'success' | 'error' | 'warn'"""
        colors = {
            "info":    (COL["text_secondary"], "●"),
            "success": (COL["success"],        "✓"),
            "error":   (COL["danger"],         "✗"),
            "warn":    (COL["warn"],            "⚠"),
        }
        fg, icon = colors.get(kind, colors["info"])
        self.status.set(msg)
        if hasattr(self, "_status_icon"):
            self._status_icon.config(text=icon, fg=fg)

    # ── Acerca de ─────────────────────────────────────────────────
    def _on_about(self, _evt=None) -> None:
        messagebox.showinfo(f"{APP_NAME}  {APP_VERSION}", APP_NOTICE, parent=self.root)


# ——— Entry point ——————————————————————————————————————————————
def main() -> None:
    if sys.platform == "win32" and sys.prefix != sys.base_prefix:
        base_tcl = Path(sys.base_prefix) / "tcl"
        if base_tcl.is_dir():
            for d in base_tcl.iterdir():
                if d.is_dir() and d.name.startswith("tcl") and "TCL_LIBRARY" not in os.environ:
                    os.environ["TCL_LIBRARY"] = str(d)
                elif d.is_dir() and d.name.startswith("tk") and "TK_LIBRARY" not in os.environ:
                    os.environ["TK_LIBRARY"] = str(d)

    if sys.platform == "win32":
        import ctypes
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "documentador.proyectos.1.0")
        except Exception:
            pass

    root = tk.Tk()
    DocumentadorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
