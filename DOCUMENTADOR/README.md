# Documentador de Proyectos v1.0

Herramienta de escritorio para generar documentacion estandarizada para proyectos Web, Mobile y QA. Produce documentos duales (Funcional + Tecnico) siguiendo el **Super Prompt Maestro** de documentacion.

---

## Indice

1. [Requisitos](#requisitos)
2. [Instalacion y primer uso (desde codigo fuente)](#instalacion-desde-codigo-fuente)
3. [Distribucion como ejecutable](#distribucion-como-ejecutable)
4. [Manual de uso de la aplicacion](#manual-de-uso)
5. [Estructura del proyecto (para desarrolladores)](#estructura-del-proyecto)
6. [Preguntas frecuentes](#preguntas-frecuentes)

---

## Requisitos

### Para ejecutar el `.exe` (usuario final)
- Windows 10 / Windows 11 (64-bit)
- Sin instalaciones adicionales — todo incluido en el ejecutable

### Para ejecutar desde codigo fuente (desarrollador)
- Python 3.10 o superior ([descargar aqui](https://www.python.org/downloads/))
  - Marcar **"Add Python to PATH"** durante la instalacion
- Conexion a internet (solo para instalar dependencias la primera vez)

---

## Instalacion desde codigo fuente

### Paso 1 — Clonar o descomprimir el proyecto

```
innova_df_chile\
    DOCUMENTADOR\
        main.py
        requirements.txt
        setup_dependencias.bat
        run.bat
        ...
```

### Paso 2 — Instalar dependencias

Ejecutar haciendo **doble clic** en:

```
setup_dependencias.bat
```

Este script:
- Verifica que Python este instalado
- Crea el entorno virtual `env\` si no existe
- Instala todas las librerias desde `requirements.txt`
- Crea las carpetas `projects\`, `exports\`, `assets\`, `templates\`

### Paso 3 — Ejecutar la aplicacion

```
run.bat
```

O directamente desde terminal con el venv activado:

```cmd
env\Scripts\activate.bat
python main.py
```

---

## Distribucion como ejecutable

Para generar el ejecutable `.exe` para distribucion (sin Python instalado):

```
build_exe.bat
```

El ejecutable se genera en:

```
dist\DocumentadorProyectos\DocumentadorProyectos.exe
```

Para distribuir: copiar la carpeta completa `dist\DocumentadorProyectos\` — contiene el `.exe` y todas las DLLs necesarias. El usuario final **no necesita instalar nada**.

---

## Manual de uso

### Pantalla principal

La aplicacion tiene 4 pestanas:

| Pestana | Funcion |
|---------|---------|
| **Proyectos** | Crear, abrir, y gestionar proyectos de documentacion |
| **Editor** | Escribir y editar el contenido de cada seccion |
| **Config. IA** | Configurar proveedor de IA (opcional) |
| **Vista Previa** | Ver el documento generado en tiempo real |

---

### 1. Crear un proyecto nuevo

1. Ir a la pestana **Proyectos**
2. Clic en **"Nuevo Proyecto"**
3. Seguir el wizard de 4 pasos:
   - **Paso 1:** Tipo de proyecto (Web, Mobile, QA, Full Stack, etc.)
   - **Paso 2:** Nombre, stack tecnologico y descripcion
   - **Paso 3:** Perfil del documento (Tecnico / No Tecnico / Ambos)
   - **Paso 4:** Confirmacion — opcion de pre-rellenar con templates
4. Clic en **"Crear Proyecto ✓"**

> El proyecto se guarda automaticamente en la carpeta `projects\` como archivo `.json`.

---

### 2. Editar secciones

1. Ir a la pestana **Editor**
2. En el arbol izquierdo, expandir un grupo y seleccionar una seccion
3. Escribir el contenido en el editor Markdown derecho
   - La toolbar ofrece atajos: H1/H2/H3, **negrita**, *italica*, `codigo`, tablas, diagramas Mermaid, placeholders de imagen
4. Clic en **"Guardar Seccion (Ctrl+S)"** o presionar `Ctrl+S`

#### Estados de las secciones

| Estado | Significado |
|--------|-------------|
| pendiente | Sin contenido aun |
| borrador | En proceso de escritura |
| revision | Listo para revisar |
| listo | Aprobado y completo |

#### Restaurar template

Si quieres volver al template de ejemplo para una seccion:
- Clic en **"Restaurar Template"** en la barra inferior del editor

---

### 3. Estructura del documento (Super Prompt Maestro)

El documento sigue la estructura del **Super Prompt Maestro** con documentacion dual:

#### PARTE 1 — Vision Funcional (No Tecnica)
Para: Gerencia, Project Manager, Stakeholders, Clientes.

| Seccion | Que incluye |
|---------|-------------|
| Resumen Ejecutivo | Que hace el sistema y que problema resuelve |
| Glosario de Terminos | 3-5 conceptos clave del negocio |
| Casos de Uso Principales | Tabla CU-01, CU-02... con actor/accion/resultado |
| Flujo Funcional (Diagrama) | Diagrama Mermaid del recorrido del usuario |
| Reglas de Negocio | Restricciones y validaciones criticas |

#### PARTE 2 — Documentacion Tecnica
Para: Lider TI, Desarrolladores, QA, Arquitectos.

| Seccion | Que incluye |
|---------|-------------|
| Stack Tecnologico | Tabla con capas, tecnologias y versiones |
| Arquitectura del Sistema | Diagrama C4/Mermaid del sistema completo |
| Estructura de Componentes | Patrones y organizacion del codigo |
| Flujo de Datos | Diagrama de secuencia cliente → API → BD |
| Modelos de Datos | Esquemas SQL, JSON payloads, relaciones |
| Guia de Configuracion | Pasos para levantar el proyecto localmente |

#### Sub-prompts especializados (segun tipo de proyecto)
- **Web:** APIs/Endpoints y Componentes UI/Frontend
- **Mobile:** Pantallas, permisos, navegacion, modo offline
- **QA:** Plan de pruebas y automatizacion

---

### 4. Generar y exportar documentacion

> **No se necesita IA para generar documentacion.** La IA es un complemento opcional.

#### Generar borrador

En la barra de acciones inferior:
- Clic en **"Generar Documento"** → crea `exports\[nombre-proyecto].md` y `.html` automaticamente

#### Exportar en distintos formatos

1. Seleccionar formato en el combo "Exportar como"
2. Clic en **"Exportar"**

| Formato | Uso recomendado |
|---------|-----------------|
| Markdown (.md) | GitHub, Confluence, Notion |
| Word (.docx) | Gerencia, clientes, distribucion formal |
| HTML (.html) | Intranet, portales internos |
| PDF (.pdf) | Distribucion formal sin edicion |

Los archivos se guardan en la carpeta `exports\`.

---

### 5. Vista Previa

Ir a la pestana **Vista Previa**:
- **Markdown:** Ver todo el contenido sin filtros
- **Tecnico:** Solo las secciones tecnicas (Parte 2)
- **No Tecnico:** Solo la vision funcional (Parte 1)
- Toggle **Formateado / Texto:** Render visual con estilos vs texto plano
- Boton **"Copiar al Portapapeles"** para pegar en otra herramienta

---

### 6. Configuracion de IA (opcional)

La IA se usa para enriquecer el contenido de secciones. Es completamente opcional.

#### Proveedores soportados

| Proveedor | Modelo por defecto | Requiere API Key |
|-----------|-------------------|-----------------|
| OpenAI (GPT-4) | gpt-4o | Si (paga) |
| Anthropic (Claude) | claude-3-5-haiku-20241022 | Si (paga) |
| Google (Gemini) | gemini-1.5-flash | Si (paga) |
| Ollama (local) | llama3 | No (local) |

#### Configurar IA

1. Ir a la pestana **Config. IA**
2. Seleccionar proveedor
3. Ingresar API Key (se guarda cifrada en el llavero del sistema, nunca en texto plano)
4. Clic en **"Guardar y Probar Conexion"**
5. Esperar confirmacion "Conectado: proveedor / modelo"

#### Usar IA para enriquecer

**Por seccion** (en el Editor):
- Escribir contenido base en la seccion
- Clic en **"✦ Enriquecer con IA"** (boton verde derecho)

**Todo el proyecto a la vez** (en la barra de acciones):
- Clic en **"Enriquecer con IA"** → enriquece TODAS las secciones con contenido

> El prompt IA sigue el Super Prompt Maestro: genera documentacion dual Funcional/Tecnica con diagramas Mermaid y placeholders de imagenes.

---

## Estructura del proyecto

```
DOCUMENTADOR\
├── main.py                  # Aplicacion principal (UI tkinter)
├── wizard.py                # Wizard multi-paso de nuevo proyecto
├── project_manager.py       # Definicion de secciones por tipo/perfil
├── section_templates.py     # Templates pre-rellenados por seccion
├── doc_generator.py         # Generacion y exportacion (MD/DOCX/HTML/PDF)
├── ai_connector.py          # Conector IA (OpenAI/Anthropic/Gemini/Ollama)
│
├── requirements.txt         # Dependencias pip
├── run.bat                  # Ejecutar desde fuente
├── setup_dependencias.bat   # Setup inicial (venv + pip install)
├── build_exe.bat            # Compilar .exe con PyInstaller
├── documentador.spec        # Config PyInstaller
│
├── SUPER_PROMPT_DOCUMENTACION.md  # Referencia: estructura de documentacion
├── README.md                # Este archivo
│
├── projects\                # Proyectos guardados (.json)
├── exports\                 # Documentos exportados
├── assets\                  # Recursos (icon.ico, logos)
├── templates\               # Templates por tipo (web/mobile/qa)
└── env\                     # Entorno virtual Python (no se versiona)
```

### Dependencias principales

| Libreria | Version | Uso |
|----------|---------|-----|
| `python-docx` | >=1.1.0 | Exportacion Word |
| `markdown` | >=3.5.0 | Conversion MD a HTML |
| `fpdf2` | >=2.7.0 | Exportacion PDF |
| `keyring` | >=24.0.0 | Almacenamiento seguro de API Keys |
| `requests` | >=2.31.0 | Llamadas a APIs de IA |
| `Pillow` | >=10.0.0 | Manejo de imagenes/icono |
| `jinja2` | >=3.1.0 | Motor de plantillas (fpdf2) |

> **Nota:** El Markdown (.md) se genera sin ninguna dependencia externa — solo stdlib de Python.

---

## Preguntas frecuentes

**¿Puedo generar documentacion sin configurar la IA?**
Si. La IA es completamente opcional. Los botones "Generar Documento" y "Exportar" funcionan sin ningun proveedor de IA configurado.

**¿Donde se guardan los proyectos?**
En la carpeta `projects\` dentro del directorio del ejecutable (o del script `.py`).

**¿Donde se guardan los documentos exportados?**
En la carpeta `exports\` en el mismo directorio.

**¿La API Key se guarda de forma segura?**
Si. Se almacena en el llavero cifrado del sistema operativo (Windows Credential Manager) usando la libreria `keyring`. Nunca se escribe en texto plano en ningun archivo.

**¿Que pasa si quiero usar Ollama (IA local)?**
Instalar Ollama desde [ollama.ai](https://ollama.ai), ejecutar `ollama pull llama3` y dejar la URL Base como `http://localhost:11434/v1`. No requiere API Key.

**¿Como genero el ejecutable?**
Ejecutar `build_exe.bat`. Requiere haber hecho `setup_dependencias.bat` primero.

**¿El ejecutable funciona en una maquina sin Python?**
Si. El `.exe` generado con PyInstaller incluye Python y todas las librerias. No requiere instalacion.

**¿Que es el Super Prompt Maestro?**
Es la metodologia de documentacion implementada en la app. Genera documentacion dual: una seccion funcional para perfiles no tecnicos (gerencia, PO) y una seccion tecnica para devs/QA/arquitectos. El archivo `SUPER_PROMPT_DOCUMENTACION.md` contiene la especificacion completa que puedes usar directamente en cualquier LLM para generar documentacion manualmente.

---

*Documentador de Proyectos v1.0 — Julio Varas Contreras — Mayo 2026*
