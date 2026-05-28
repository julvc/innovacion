"""
Wizard multi-paso para creacion de nuevo proyecto.

Paso 1 — Tipo de Proyecto   (tarjetas visuales)
Paso 2 — Datos del Proyecto (nombre, stack, descripcion)
Paso 3 — Perfil Target      (tarjetas visuales)
Paso 4 — Resumen            (confirmacion antes de crear)
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

# ——— Paleta (sincronizada con main.py) ———————————————————————
COL = {
    "header":         "#0D47A1",
    "primary":        "#1565C0",
    "primary_active": "#0D47A1",
    "danger":         "#C62828",
    "danger_hover":   "#B71C1C",
    "text":           "#212121",
    "text_secondary": "#607D8B",
    "bg":             "#F0F2F5",
    "card":           "#FFFFFF",
    "sep":            "#CFD8DC",
    "sep_light":      "#ECEFF1",
    "subtitle_blue":  "#BBDEFB",
    "credits_fg":     "#90CAF9",
    "card_title":     "#1565C0",
    "btn_dark":       "#37474F",
    "btn_dark_active":"#263238",
    "help":           "#607D8B",
    "warn":           "#E65100",
    "success":        "#2E7D32",
    "card_selected":  "#E3F2FD",
    "card_sel_border":"#1565C0",
}

F_BODY       = ("Segoe UI", 10)
F_LABEL      = ("Segoe UI", 9)
F_HELP       = ("Segoe UI", 8)
F_CARD_TITLE = ("Segoe UI", 12, "bold")
F_SECTION    = ("Segoe UI", 13, "bold")
F_STEP_NUM   = ("Segoe UI", 20, "bold")
F_STEP_LABEL = ("Segoe UI", 9)
F_CARD_TYPE  = ("Segoe UI", 11, "bold")
F_CARD_DESC  = ("Segoe UI", 8)

# ——— Definicion de opciones de tipo ——————————————————————————
PROJECT_TYPE_DEFS = [
    {
        "id":    "Web",
        "icon":  "🌐",
        "label": "Web",
        "desc":  "Aplicacion o sistema\nweb (frontend + backend)",
        "subs":  "React, Vue, Angular,\nDjango, FastAPI, Laravel...",
    },
    {
        "id":    "Mobile",
        "icon":  "📱",
        "label": "Mobile",
        "desc":  "App movil nativa\no hibrida",
        "subs":  "Flutter, React Native,\nSwift, Kotlin...",
    },
    {
        "id":    "QA",
        "icon":  "✅",
        "label": "QA / Testing",
        "desc":  "Plan de pruebas\ny automatizacion",
        "subs":  "Selenium, Cypress,\nPlaywright, JUnit...",
    },
    {
        "id":    "Web + QA",
        "icon":  "🌐✅",
        "label": "Web + QA",
        "desc":  "Sistema web con\ndocumentacion de QA",
        "subs":  "Documentacion tecnica\n+ plan de pruebas",
    },
    {
        "id":    "Mobile + QA",
        "icon":  "📱✅",
        "label": "Mobile + QA",
        "desc":  "App movil con\ndocumentacion de QA",
        "subs":  "Documentacion mobile\n+ plan de pruebas",
    },
    {
        "id":    "Full Stack",
        "icon":  "⚡",
        "label": "Full Stack",
        "desc":  "Web completo:\nfrontend + backend + mobile",
        "subs":  "Documentacion\ncompleta de sistema",
    },
]

PROFILE_DEFS = [
    {
        "id":    "Tecnico (Lider TI, Devs, QA, Arquitecto)",
        "icon":  "⚙️",
        "label": "Tecnico",
        "desc":  "Para: Lider TI, Desarrolladores,\nQA, Arquitectos",
        "subs":  "Stack, arquitectura, APIs,\ndiagramas, setup, codigo",
    },
    {
        "id":    "No Tecnico (Gerencia, PM)",
        "icon":  "📊",
        "label": "No Tecnico",
        "desc":  "Para: Gerencia, Project Manager,\nStakeholders, Clientes",
        "subs":  "Resumen ejecutivo, alcance,\nbeneficio, estado del proyecto",
    },
    {
        "id":    "Ambos",
        "icon":  "👥",
        "label": "Ambos perfiles",
        "desc":  "Documento completo con\nseccion funcional + tecnica",
        "subs":  "Recomendado: cubre\ntodos los perfiles",
    },
]


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


# ——— Tarjeta de seleccion ————————————————————————————————————
class SelectionCard(tk.Frame):
    """Tarjeta visual clickeable para seleccion de tipo/perfil."""

    def __init__(self, parent, option: dict, on_select, width=160, height=110):
        super().__init__(parent, bg=COL["card"], cursor="hand2",
                         highlightthickness=2,
                         highlightbackground=COL["sep"],
                         width=width, height=height)
        self.pack_propagate(False)
        self.option    = option
        self.on_select = on_select
        self._selected = False

        inner = tk.Frame(self, bg=COL["card"], padx=8, pady=8)
        inner.pack(fill=tk.BOTH, expand=True)

        tk.Label(inner, text=option["icon"],
                 font=("Segoe UI", 18), bg=COL["card"]).pack()
        tk.Label(inner, text=option["label"], font=F_CARD_TYPE,
                 fg=COL["card_title"], bg=COL["card"]).pack()
        tk.Label(inner, text=option["desc"], font=F_CARD_DESC,
                 fg=COL["text_secondary"], bg=COL["card"],
                 justify="center").pack(pady=(2, 0))

        for w in [self, inner] + inner.winfo_children():
            w.bind("<Button-1>", self._on_click)
            w.bind("<Enter>",    self._on_enter)
            w.bind("<Leave>",    self._on_leave)

    def _on_click(self, _evt=None) -> None:
        self.on_select(self.option["id"])

    def _on_enter(self, _evt=None) -> None:
        if not self._selected:
            self.config(highlightbackground=COL["primary"])

    def _on_leave(self, _evt=None) -> None:
        if not self._selected:
            self.config(highlightbackground=COL["sep"])

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        if selected:
            self.config(bg=COL["card_selected"],
                        highlightbackground=COL["card_sel_border"],
                        highlightthickness=2)
            for w in self.winfo_children():
                w.config(bg=COL["card_selected"])
                for ww in w.winfo_children():
                    ww.config(bg=COL["card_selected"])
        else:
            self.config(bg=COL["card"], highlightbackground=COL["sep"],
                        highlightthickness=2)
            for w in self.winfo_children():
                w.config(bg=COL["card"])
                for ww in w.winfo_children():
                    ww.config(bg=COL["card"])


# ——— Wizard principal ————————————————————————————————————————
class NuevoProyectoWizard(tk.Toplevel):
    TOTAL_STEPS = 4

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.title("Nuevo Proyecto — Wizard")
        self.geometry("700x580")
        self.minsize(650, 540)
        self.configure(bg=COL["bg"])
        self.resizable(True, True)
        self.grab_set()

        self.result: dict | None = None
        self._step = 1

        # Datos del proyecto
        self._type    = tk.StringVar()
        self._name    = tk.StringVar()
        self._stack   = tk.StringVar()
        self._profile = tk.StringVar()
        self._desc_content = ""

        # Tarjetas de seleccion (referencias para toggle)
        self._type_cards:    list[SelectionCard] = []
        self._profile_cards: list[SelectionCard] = []

        self._setup_styles()
        self._build()

        self.transient(parent)
        self.wait_window()

    def _setup_styles(self) -> None:
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("TCheckbutton", background=COL["card"],
                    foreground=COL["text"], font=F_BODY)

    # ── Layout fijo ───────────────────────────────────────────────
    def _build(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._build_header()
        self._content_frame = tk.Frame(self, bg=COL["bg"])
        self._content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 8))
        self._content_frame.columnconfigure(0, weight=1)
        self._content_frame.rowconfigure(0, weight=1)
        self._build_footer()
        self._show_step(1)

    def _build_header(self) -> None:
        hdr = tk.Frame(self, bg=COL["header"], height=72, highlightthickness=0)
        hdr.grid(row=0, column=0, sticky="nsew")
        hdr.grid_propagate(False)
        hdr.columnconfigure(0, weight=1)

        inner = tk.Frame(hdr, bg=COL["header"])
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=12)

        self._step_title_var = tk.StringVar(value="Paso 1 de 4")
        self._step_desc_var  = tk.StringVar(value="Selecciona el tipo de proyecto")

        tk.Label(inner, textvariable=self._step_title_var,
                 font=("Segoe UI", 15, "bold"), fg="white",
                 bg=COL["header"], anchor="w").pack(anchor="w")
        tk.Label(inner, textvariable=self._step_desc_var,
                 font=F_BODY, fg=COL["subtitle_blue"],
                 bg=COL["header"], anchor="w").pack(anchor="w")

        # Indicador de pasos (dots)
        dots = tk.Frame(inner, bg=COL["header"])
        dots.pack(anchor="e", side=tk.RIGHT)
        self._step_dots: list[tk.Label] = []
        for i in range(1, self.TOTAL_STEPS + 1):
            d = tk.Label(dots, text="●", font=("Segoe UI", 10),
                         fg=COL["credits_fg"], bg=COL["header"])
            d.pack(side=tk.LEFT, padx=3)
            self._step_dots.append(d)

    def _build_footer(self) -> None:
        foot = tk.Frame(self, bg=COL["sep_light"], height=56, highlightthickness=0)
        foot.grid(row=2, column=0, sticky="ew")
        foot.grid_propagate(False)

        inner = tk.Frame(foot, bg=COL["sep_light"])
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.btn_cancel = _flat_btn(inner, "Cancelar", COL["btn_dark"],
                                     COL["btn_dark_active"],
                                     command=self.destroy)
        self.btn_cancel.pack(side=tk.LEFT)

        self.btn_next = _flat_btn(inner, "Siguiente  →", COL["primary"],
                                   COL["primary_active"],
                                   command=self._on_next)
        self.btn_next.pack(side=tk.RIGHT)

        self.btn_back = _flat_btn(inner, "← Atras", COL["btn_dark"],
                                   COL["btn_dark_active"],
                                   command=self._on_back,
                                   state=tk.DISABLED)
        self.btn_back.pack(side=tk.RIGHT, padx=(0, 8))

    # ── Navegacion ────────────────────────────────────────────────
    def _show_step(self, step: int) -> None:
        self._step = step
        for w in self._content_frame.winfo_children():
            w.destroy()

        self._update_header()
        self._update_nav_buttons()

        builders = {
            1: self._build_step1,
            2: self._build_step2,
            3: self._build_step3,
            4: self._build_step4,
        }
        builders[step]()

    def _update_header(self) -> None:
        titles = {
            1: ("Paso 1 de 4",  "Selecciona el tipo de proyecto"),
            2: ("Paso 2 de 4",  "Datos del proyecto"),
            3: ("Paso 3 de 4",  "Perfil de la documentacion"),
            4: ("Paso 4 de 4",  "Confirmar y crear proyecto"),
        }
        title, desc = titles[self._step]
        self._step_title_var.set(title)
        self._step_desc_var.set(desc)

        for i, dot in enumerate(self._step_dots, 1):
            if i < self._step:
                dot.config(fg="white", text="✓")
            elif i == self._step:
                dot.config(fg="white", text="●", font=("Segoe UI", 13, "bold"))
            else:
                dot.config(fg=COL["credits_fg"], text="●",
                           font=("Segoe UI", 10))

    def _update_nav_buttons(self) -> None:
        self.btn_back.config(state=tk.NORMAL if self._step > 1 else tk.DISABLED)
        if self._step == self.TOTAL_STEPS:
            self.btn_next.config(text="Crear Proyecto  ✓",
                                  bg=COL["success"],
                                  activebackground="#1B5E20")
        else:
            self.btn_next.config(text="Siguiente  →",
                                  bg=COL["primary"],
                                  activebackground=COL["primary_active"])

    def _on_next(self) -> None:
        if not self._validate_current():
            return
        if self._step < self.TOTAL_STEPS:
            self._show_step(self._step + 1)
        else:
            self._on_create()

    def _on_back(self) -> None:
        if self._step > 1:
            self._show_step(self._step - 1)

    def _validate_current(self) -> bool:
        if self._step == 1:
            if not self._type.get():
                messagebox.showwarning("Seleccion requerida",
                                       "Selecciona un tipo de proyecto.",
                                       parent=self)
                return False
        elif self._step == 2:
            if not self._name.get().strip():
                messagebox.showwarning("Campo requerido",
                                       "El nombre del proyecto es obligatorio.",
                                       parent=self)
                return False
        elif self._step == 3:
            if not self._profile.get():
                messagebox.showwarning("Seleccion requerida",
                                       "Selecciona un perfil de documentacion.",
                                       parent=self)
                return False
        return True

    # ── Paso 1: Tipo de proyecto ──────────────────────────────────
    def _build_step1(self) -> None:
        cf = self._content_frame
        cf.rowconfigure(0, weight=1)

        tk.Label(cf, text="¿Que tipo de proyecto vas a documentar?",
                 font=F_SECTION, fg=COL["card_title"], bg=COL["bg"],
                 anchor="w").grid(row=0, column=0, sticky="w", pady=(12, 8))

        grid = tk.Frame(cf, bg=COL["bg"])
        grid.grid(row=1, column=0, sticky="nsew")

        self._type_cards = []
        for i, opt in enumerate(PROJECT_TYPE_DEFS):
            card = SelectionCard(grid, opt, self._on_type_select,
                                 width=190, height=125)
            card.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="nsew")
            grid.columnconfigure(i % 3, weight=1)
            self._type_cards.append(card)

        if self._type.get():
            for c in self._type_cards:
                c.set_selected(c.option["id"] == self._type.get())

    def _on_type_select(self, type_id: str) -> None:
        self._type.set(type_id)
        for c in self._type_cards:
            c.set_selected(c.option["id"] == type_id)

    # ── Paso 2: Datos del proyecto ────────────────────────────────
    def _build_step2(self) -> None:
        cf = self._content_frame
        cf.rowconfigure(2, weight=1)

        outer = tk.Frame(cf, bg=COL["sep"], highlightthickness=0)
        outer.grid(row=0, column=0, sticky="nsew", pady=(10, 0))
        inner = tk.Frame(outer, bg=COL["card"], padx=16, pady=14)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        inner.columnconfigure(0, weight=1)

        # Nombre
        tk.Label(inner, text="Nombre del Proyecto *",
                 font=F_LABEL, fg=COL["text"], bg=COL["card"]).grid(
            row=0, column=0, sticky="w", pady=(0, 3))
        tk.Entry(inner, textvariable=self._name, font=F_BODY,
                 fg=COL["text"], relief=tk.FLAT, highlightthickness=1,
                 highlightbackground=COL["sep"],
                 highlightcolor=COL["primary"]).grid(
            row=1, column=0, sticky="ew", pady=(0, 2))
        tk.Label(inner,
                 text="Ej: Portal de Clientes, App iOS Banca, Suite QA Pagos",
                 font=F_HELP, fg=COL["help"], bg=COL["card"]).grid(
            row=2, column=0, sticky="w", pady=(0, 12))

        # Stack
        tk.Label(inner, text="Stack Tecnologico",
                 font=F_LABEL, fg=COL["text"], bg=COL["card"]).grid(
            row=3, column=0, sticky="w", pady=(0, 3))
        tk.Entry(inner, textvariable=self._stack, font=F_BODY,
                 fg=COL["text"], relief=tk.FLAT, highlightthickness=1,
                 highlightbackground=COL["sep"],
                 highlightcolor=COL["primary"]).grid(
            row=4, column=0, sticky="ew", pady=(0, 2))
        tk.Label(inner, text="Ej: React + FastAPI + PostgreSQL  /  Flutter + Firebase",
                 font=F_HELP, fg=COL["help"], bg=COL["card"]).grid(
            row=5, column=0, sticky="w", pady=(0, 12))

        # Descripcion
        tk.Label(inner, text="Descripcion breve del proyecto",
                 font=F_LABEL, fg=COL["text"], bg=COL["card"]).grid(
            row=6, column=0, sticky="w", pady=(0, 3))

        self._desc_text = tk.Text(
            inner, height=5, font=F_BODY, fg=COL["text"],
            relief=tk.FLAT, highlightthickness=1,
            highlightbackground=COL["sep"],
            highlightcolor=COL["primary"],
            wrap=tk.WORD,
        )
        self._desc_text.grid(row=7, column=0, sticky="ew", pady=(0, 4))
        if self._desc_content:
            self._desc_text.insert(tk.END, self._desc_content)

        tk.Label(inner,
                 text="Esta descripcion se usara como 'Resumen Ejecutivo' inicial.",
                 font=F_HELP, fg=COL["help"], bg=COL["card"]).grid(
            row=8, column=0, sticky="w")

    # ── Paso 3: Perfil target ─────────────────────────────────────
    def _build_step3(self) -> None:
        cf = self._content_frame
        cf.rowconfigure(1, weight=1)

        tk.Label(cf, text="¿Para quienes es la documentacion?",
                 font=F_SECTION, fg=COL["card_title"], bg=COL["bg"],
                 anchor="w").grid(row=0, column=0, sticky="w", pady=(12, 8))

        grid = tk.Frame(cf, bg=COL["bg"])
        grid.grid(row=1, column=0, sticky="n")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        self._profile_cards = []
        for i, opt in enumerate(PROFILE_DEFS):
            card = SelectionCard(grid, opt, self._on_profile_select,
                                 width=195, height=130)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            self._profile_cards.append(card)

        if self._profile.get():
            for c in self._profile_cards:
                c.set_selected(c.option["id"] == self._profile.get())

        # Nota orientativa
        note = tk.Frame(cf, bg=COL["sep_light"], pady=8)
        note.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        tk.Label(note,
                 text="El perfil determina las secciones de documentacion que se generaran.\n"
                      "'Ambos' es la opcion mas completa e incluye seccion ejecutiva + tecnica.",
                 font=F_HELP, fg=COL["text_secondary"], bg=COL["sep_light"],
                 justify="center").pack()

    def _on_profile_select(self, profile_id: str) -> None:
        self._profile.set(profile_id)
        for c in self._profile_cards:
            c.set_selected(c.option["id"] == profile_id)

    # ── Paso 4: Resumen / Confirmacion ────────────────────────────
    def _build_step4(self) -> None:
        # Capturar descripcion antes de destruir widget
        if hasattr(self, "_desc_text"):
            try:
                self._desc_content = self._desc_text.get("1.0", tk.END).strip()
            except tk.TclError:
                pass

        cf = self._content_frame

        outer = tk.Frame(cf, bg=COL["sep"])
        outer.grid(row=0, column=0, sticky="nsew", pady=(10, 0))
        inner = tk.Frame(outer, bg=COL["card"], padx=16, pady=16)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        inner.columnconfigure(1, weight=1)

        tk.Label(inner, text="RESUMEN DEL PROYECTO", font=F_CARD_TITLE,
                 fg=COL["card_title"], bg=COL["card"]).grid(
            row=0, column=0, columnspan=2, sticky="w")
        tk.Frame(inner, height=1, bg=COL["sep_light"]).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(4, 14))

        # Tipo con icono
        type_opt = next((o for o in PROJECT_TYPE_DEFS if o["id"] == self._type.get()), {})
        prof_opt = next((o for o in PROFILE_DEFS if o["id"] == self._profile.get()), {})

        rows = [
            ("Nombre:",     self._name.get()),
            ("Tipo:",       f"{type_opt.get('icon','')} {self._type.get()}  —  {type_opt.get('desc','').replace(chr(10),' ')}"),
            ("Stack:",      self._stack.get() or "(no especificado)"),
            ("Perfil:",     f"{prof_opt.get('icon','')} {prof_opt.get('label','')}  —  {prof_opt.get('desc','').replace(chr(10),' ')}"),
            ("Descripcion:",self._desc_content or "(sin descripcion)"),
        ]

        for r, (label, value) in enumerate(rows, 2):
            tk.Label(inner, text=label, font=("Segoe UI", 9, "bold"),
                     fg=COL["card_title"], bg=COL["card"],
                     anchor="nw").grid(row=r, column=0, sticky="nw",
                                       padx=(0, 12), pady=6)
            tk.Label(inner, text=value, font=F_BODY,
                     fg=COL["text"], bg=COL["card"],
                     anchor="nw", justify="left",
                     wraplength=420).grid(row=r, column=1, sticky="nw", pady=6)

        # Secciones que se generaran
        from project_manager import get_sections_for_type
        sections = get_sections_for_type(self._type.get(), self._profile.get())
        total    = sum(len(v) for v in sections.values())
        sep_row = len(rows) + 2
        tk.Frame(inner, height=1, bg=COL["sep_light"]).grid(
            row=sep_row, column=0, columnspan=2,
            sticky="ew", pady=(8, 6))
        tk.Label(inner,
                 text=f"Se crearan {len(sections)} grupos con {total} secciones de documentacion.",
                 font=F_HELP, fg=COL["help"], bg=COL["card"],
                 justify="left").grid(
            row=sep_row + 1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Opcion: pre-rellenar con templates
        self._use_templates = tk.BooleanVar(value=True)
        tmpl_frame = tk.Frame(inner, bg=COL["card_selected"],
                               highlightthickness=1,
                               highlightbackground=COL["card_sel_border"])
        tmpl_frame.grid(row=sep_row + 2, column=0, columnspan=2,
                        sticky="ew", pady=(4, 0))
        inner_t = tk.Frame(tmpl_frame, bg=COL["card_selected"], padx=10, pady=8)
        inner_t.pack(fill=tk.X)

        s = ttk.Style()
        s.configure("Tmpl.TCheckbutton",
                    background=COL["card_selected"],
                    foreground=COL["card_title"],
                    font=("Segoe UI", 10, "bold"))
        s.map("Tmpl.TCheckbutton", background=[("active", COL["card_selected"])])

        ttk.Checkbutton(inner_t,
                        text="Pre-rellenar secciones con templates de ejemplo",
                        variable=self._use_templates,
                        style="Tmpl.TCheckbutton").pack(anchor="w")
        tk.Label(inner_t,
                 text="Cada seccion incluira estructura, tablas y diagramas Mermaid listos para editar.\n"
                      "Recomendado para empezar rapido. Puedes sobreescribir el contenido despues.",
                 font=F_CARD_DESC, fg=COL["help"],
                 bg=COL["card_selected"], justify="left").pack(anchor="w", pady=(3, 0))

    # ── Crear proyecto ────────────────────────────────────────────
    def _on_create(self) -> None:
        if hasattr(self, "_desc_text"):
            try:
                self._desc_content = self._desc_text.get("1.0", tk.END).strip()
            except tk.TclError:
                pass

        self.result = {
            "name":          self._name.get().strip(),
            "type":          self._type.get(),
            "profile":       self._profile.get(),
            "stack":         self._stack.get().strip(),
            "desc":          self._desc_content,
            "sections":      {},
            "use_templates": getattr(self, "_use_templates", tk.BooleanVar(value=False)).get(),
        }

        if self.result["use_templates"]:
            from section_templates import prefill_project_sections
            prefill_project_sections(self.result)

        self.destroy()
