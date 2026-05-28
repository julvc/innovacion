"""
Definicion de secciones de documentacion alineadas al Super Prompt Maestro.

Estructura dual:
  PARTE 1 — Vision Funcional / Negocio  (no tecnico)
  PARTE 2 — Documentacion Tecnica       (tecnico)

Sub-prompts especializados segun tipo: API, UI/Frontend, Mobile.
"""
from __future__ import annotations

# ——— Hints por seccion ————————————————————————————————————————
# Texto guia que aparece en el editor al seleccionar la seccion.
SECTION_HINTS: dict[str, str] = {
    # ── Parte 1: Funcional ──────────────────────────────────────
    "Resumen Ejecutivo": (
        "Que hace este sistema/modulo y que problema de negocio resuelve.\n"
        "Orienta a personas NO tecnicas (Stakeholders, PO, Analistas, Usuarios).\n"
        "NO mencionar lenguajes de programacion, BD o infraestructura."
    ),
    "Glosario de Terminos": (
        "Define 3 a 5 conceptos clave del negocio usados en este modulo.\n"
        "Formato sugerido:\n"
        "- **Termino:** Definicion clara en lenguaje de negocio."
    ),
    "Casos de Uso Principales": (
        "Lista de las acciones principales que un usuario puede realizar.\n"
        "Formato: CU-01, CU-02...\n"
        "Actor | Accion | Resultado esperado"
    ),
    "Flujo Funcional (Diagrama)": (
        "Diagrama Mermaid que muestre el recorrido del usuario.\n"
        "Usa flowchart TD o LR. Ejemplo minimo:\n\n"
        "```mermaid\nflowchart TD\n"
        "    A[Usuario ingresa] --> B{Autenticado?}\n"
        "    B -- Si --> C[Ver Dashboard]\n"
        "    B -- No --> D[Login]\n```"
    ),
    "Reglas de Negocio / Validaciones Clave": (
        "Restricciones importantes del negocio.\n"
        "Ej: 'El usuario debe ser mayor de edad'\n"
        "    'Los documentos no pueden pesar mas de 10MB'\n"
        "    'Solo admins pueden eliminar registros'"
    ),
    # ── Parte 2: Tecnica ────────────────────────────────────────
    "Stack Tecnologico y Dependencias": (
        "Lenguajes, frameworks, librerias principales.\n"
        "Incluir versiones. Formato tabla sugerido:\n\n"
        "| Capa       | Tecnologia | Version |\n"
        "|------------|------------|---------|\n"
        "| Frontend   |            |         |\n"
        "| Backend    |            |         |\n"
        "| Base Datos |            |         |"
    ),
    "Arquitectura del Sistema (Diagrama)": (
        "Diagrama Mermaid tipo C4 o similar.\n"
        "Mostrar Frontend, Backend, APIs externas y BD.\n\n"
        "```mermaid\nC4Context\n"
        "  Person(user, 'Usuario')\n"
        "  System(app, 'Aplicacion', 'Descripcion')\n"
        "  SystemDb(db, 'Base de Datos')\n"
        "  Rel(user, app, 'Usa')\n"
        "  Rel(app, db, 'Lee/Escribe')\n```"
    ),
    "Estructura de Componentes / Patrones": (
        "Como esta organizado el codigo.\n"
        "Patrones: MVC, MVVM, Clean Architecture, Repository, etc.\n"
        "Listar principales modulos, clases, carpetas clave."
    ),
    "Flujo de Datos (Diagrama de Secuencia)": (
        "Diagrama Mermaid sequenceDiagram.\n"
        "Mostrar viaje de los datos: cliente → API → servicio → BD.\n\n"
        "```mermaid\nsequenceDiagram\n"
        "    participant C as Cliente\n"
        "    participant A as API\n"
        "    participant S as Servicio\n"
        "    participant D as Base Datos\n"
        "    C->>A: POST /endpoint\n"
        "    A->>S: procesar()\n"
        "    S->>D: INSERT/UPDATE\n"
        "    D-->>S: OK\n"
        "    S-->>A: resultado\n"
        "    A-->>C: 200 OK\n```"
    ),
    "Modelos de Datos / Entidades Clave": (
        "Estructuras de datos principales: JSON payloads, tablas o esquemas.\n"
        "Incluir campos, tipos y descripcion.\n\n"
        "```json\n{\n"
        "  \"id\": \"string (UUID)\",\n"
        "  \"nombre\": \"string\",\n"
        "  \"fecha_creacion\": \"ISO 8601\"\n"
        "}\n```"
    ),
    "Guia Rapida de Configuracion (Setup)": (
        "Pasos resumidos para levantar este modulo en local.\n"
        "1. Requisitos previos\n"
        "2. Clonar repositorio\n"
        "3. Instalar dependencias\n"
        "4. Variables de entorno (usar .env.example)\n"
        "5. Ejecutar migraciones\n"
        "6. Iniciar servidor"
    ),
    # ── Sub-prompt API ───────────────────────────────────────────
    "Informacion General de la API": (
        "Proposito de la API, URL base, metodo de autenticacion.\n"
        "Ej: Bearer Token, JWT, API Key, OAuth2."
    ),
    "Flujo de Interaccion API (Diagrama)": (
        "Diagrama de secuencia: cliente → API → backend → respuesta.\n"
        "Usa mermaid sequenceDiagram."
    ),
    "Detalle de Endpoints": (
        "Por cada endpoint:\n"
        "- Ruta y Metodo: GET/POST/PUT/DELETE /api/v1/...\n"
        "- Descripcion\n"
        "- Parametros (tabla: Nombre | Tipo | Obligatorio | Descripcion)\n"
        "- Request Body (JSON ejemplo)\n"
        "- Responses: 200, 201, 400, 404, 500 con JSON ejemplo"
    ),
    "Dependencias y Servicios Externos API": (
        "Lista de APIs externas o BD que consume este servicio."
    ),
    # ── Sub-prompt UI/Frontend ───────────────────────────────────
    "Nombre y Proposito del Componente": (
        "Que es este componente y donde se usa en el sistema.\n"
        "> Placeholder: [Insertar captura general del componente]"
    ),
    "Propiedades (Props)": (
        "Tabla: Nombre | Tipo | Valor Default | Requerido | Descripcion"
    ),
    "Eventos (Emits/Outputs)": (
        "Tabla: Nombre Evento | Payload | Cuando se dispara"
    ),
    "Estados Visuales (Variantes)": (
        "Enumerar estados: Loading, Disabled, Success, Error, Empty.\n"
        "Para cada uno: descripcion + placeholder de imagen.\n"
        "> Placeholder: [Insertar captura estado Loading]"
    ),
    "Dependencias y Estado Global": (
        "Stores globales (Pinia/Vuex/Redux/Provider), Composables/Hooks usados."
    ),
    "Ejemplo de Uso (Codigo)": (
        "Bloque de codigo mostrando como instanciar el componente:\n"
        "props pasadas + eventos escuchados."
    ),
    # ── Sub-prompt Mobile ────────────────────────────────────────
    "Nombre y Proposito de la Pantalla": (
        "Que resuelve para el usuario movil.\n"
        "> Placeholder: [Insertar captura de la pantalla en simulador]"
    ),
    "Plataforma y Framework Mobile": (
        "Lenguaje y entorno.\n"
        "Ej: Kotlin/Jetpack Compose, Swift/SwiftUI, Flutter, React Native."
    ),
    "Permisos y Hardware (Device Features)": (
        "Tabla: Permiso | Por que se necesita\n"
        "Ej: Camara, Geolocalizacion, Notificaciones Push, Bluetooth."
    ),
    "Persistencia y Modo Offline": (
        "Almacenamiento local: CoreData, Room, SQLite, SharedPreferences.\n"
        "Comportamiento sin conexion a internet."
    ),
    "Flujo de Navegacion Mobile (Diagrama)": (
        "Mermaid flowchart: pantalla origen → esta pantalla → pantallas destino."
    ),
    "Gestion del Estado / Arquitectura Mobile": (
        "Patron: MVVM, Clean Architecture, BLoC, Provider, etc.\n"
        "Como se conecta la vista con los datos."
    ),
    "Servicios y APIs Consumidas": (
        "Lista de llamadas a red que hace esta vista al cargarse o interactuar."
    ),
}

# ——— Estructura de secciones por tipo de proyecto ———————————
# Formato: { grupo: [id_seccion, ...] }
# Los IDs deben existir en SECTION_HINTS para mostrar ayuda contextual.

_PARTE1 = "PARTE 1 — Vision Funcional (No Tecnica)"
_PARTE2 = "PARTE 2 — Documentacion Tecnica"

_BASE_WEB = {
    _PARTE1: [
        "Resumen Ejecutivo",
        "Glosario de Terminos",
        "Casos de Uso Principales",
        "Flujo Funcional (Diagrama)",
        "Reglas de Negocio / Validaciones Clave",
    ],
    _PARTE2: [
        "Stack Tecnologico y Dependencias",
        "Arquitectura del Sistema (Diagrama)",
        "Estructura de Componentes / Patrones",
        "Flujo de Datos (Diagrama de Secuencia)",
        "Modelos de Datos / Entidades Clave",
        "Guia Rapida de Configuracion (Setup)",
    ],
    "Sub-Prompt: APIs / Endpoints": [
        "Informacion General de la API",
        "Flujo de Interaccion API (Diagrama)",
        "Detalle de Endpoints",
        "Dependencias y Servicios Externos API",
    ],
    "Sub-Prompt: Componentes UI / Frontend": [
        "Nombre y Proposito del Componente",
        "Propiedades (Props)",
        "Eventos (Emits/Outputs)",
        "Estados Visuales (Variantes)",
        "Dependencias y Estado Global",
        "Ejemplo de Uso (Codigo)",
    ],
}

_BASE_MOBILE = {
    _PARTE1: [
        "Resumen Ejecutivo",
        "Glosario de Terminos",
        "Casos de Uso Principales",
        "Flujo Funcional (Diagrama)",
        "Reglas de Negocio / Validaciones Clave",
    ],
    _PARTE2: [
        "Stack Tecnologico y Dependencias",
        "Arquitectura del Sistema (Diagrama)",
        "Estructura de Componentes / Patrones",
        "Flujo de Datos (Diagrama de Secuencia)",
        "Modelos de Datos / Entidades Clave",
        "Guia Rapida de Configuracion (Setup)",
    ],
    "Sub-Prompt: Pantallas Mobile": [
        "Nombre y Proposito de la Pantalla",
        "Plataforma y Framework Mobile",
        "Permisos y Hardware (Device Features)",
        "Persistencia y Modo Offline",
        "Flujo de Navegacion Mobile (Diagrama)",
        "Gestion del Estado / Arquitectura Mobile",
        "Servicios y APIs Consumidas",
    ],
}

_BASE_QA = {
    _PARTE1: [
        "Resumen Ejecutivo",
        "Glosario de Terminos",
        "Casos de Uso Principales",
        "Flujo Funcional (Diagrama)",
        "Reglas de Negocio / Validaciones Clave",
    ],
    _PARTE2: [
        "Stack Tecnologico y Dependencias",
        "Arquitectura del Sistema (Diagrama)",
        "Estructura de Componentes / Patrones",
        "Flujo de Datos (Diagrama de Secuencia)",
        "Modelos de Datos / Entidades Clave",
        "Guia Rapida de Configuracion (Setup)",
    ],
    "Sub-Prompt: Plan de Pruebas y Automatizacion": [
        "Informacion General de la API",
        "Flujo de Interaccion API (Diagrama)",
        "Detalle de Endpoints",
        "Dependencias y Servicios Externos API",
    ],
}

_SECTIONS_BY_TYPE: dict[str, dict] = {
    "Web":         _BASE_WEB,
    "Mobile":      _BASE_MOBILE,
    "QA":          _BASE_QA,
    "Web + QA":    {**_BASE_WEB, **{f"[QA] {k}": v for k, v in _BASE_QA.items()
                    if k not in (_PARTE1, _PARTE2)}},
    "Mobile + QA": {**_BASE_MOBILE, **{f"[QA] {k}": v for k, v in _BASE_QA.items()
                    if k not in (_PARTE1, _PARTE2)}},
    "Full Stack":  {**_BASE_WEB, "Sub-Prompt: Pantallas Mobile": _BASE_MOBILE["Sub-Prompt: Pantallas Mobile"]},
}


def get_sections_for_type(ptype: str, profile: str) -> dict[str, list[str]]:
    """Devuelve {grupo: [id_seccion, ...]} segun tipo de proyecto."""
    base = _SECTIONS_BY_TYPE.get(ptype, _BASE_WEB)

    if "No Tecnico" in profile:
        return {_PARTE1: base[_PARTE1]}

    if "Tecnico" in profile and "No Tecnico" not in profile:
        return {k: v for k, v in base.items() if k != _PARTE1}

    # Ambos — estructura completa
    return base


def get_section_hint(section_id: str) -> str:
    """Texto guia para mostrar al usuario al seleccionar una seccion."""
    return SECTION_HINTS.get(section_id, "Complete esta seccion con el contenido correspondiente.")
