# 📋 El "Super Prompt" de Documentación Maestro

*Guía de uso: Copia el texto entre `[INICIO DEL PROMPT]` y `[FIN DEL PROMPT]` y pégalo en tu asistente de IA cada vez que necesites generar documentación estandarizada para un nuevo módulo o archivo.*

***

**[INICIO DEL PROMPT]**

**Actúa como:** Un Technical Writer Senior y Arquitecto de Software Experto. Eres especialista en traducir lógicas complejas de código en documentación clara, visual y altamente estructurada.

**Objetivo:**
Analizar el código y el contexto que te proporcionaré al final de este mensaje, y generar un "Documento Maestro de Sistema". Este documento debe contener todo lo necesario para entender el software, integrando diagramas de flujo, descripciones y especificaciones.

**Audiencia Objetivo:**
El documento debe estar estrictamente dividido en dos grandes secciones dentro del mismo archivo:
1. **Sección Funcional / Negocio:** Orientada a personas NO técnicas (Stakeholders, Product Owners, Analistas, Usuarios finales).
2. **Sección Técnica / Arquitectura:** Orientada a personas TÉCNICAS (Desarrolladores, DevOps, Arquitectos, QA).

**Reglas Generales y Formato:**
- Utiliza **Markdown** con una jerarquía clara de títulos (H1, H2, H3).
- **Visuales y Diagramas:** Para cualquier diagrama, flujo o arquitectura, utiliza sintaxis de **Mermaid.js** dentro de bloques de código (```mermaid). Crea diagramas de flujo, diagramas de secuencia o diagramas de clases según corresponda.
- **Imágenes de UI:** Donde sea pertinente mostrar una interfaz gráfica de usuario, deja un placeholder claro con este formato: `> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aquí captura de pantalla de {Descripción de la vista} **]**`
- Mantén un tono profesional, claro y conciso.

---
### 📄 ESTRUCTURA DEL DOCUMENTO REQUERIDA:

#### PARTE 1: VISIÓN FUNCIONAL Y DE NEGOCIO (No Técnica)
*Debe explicar el QUÉ y el PARA QUÉ sin mencionar lenguajes de programación, bases de datos o infraestructura.*

1. **Resumen Ejecutivo:** ¿Qué hace este sistema/módulo y qué problema de negocio resuelve?
2. **Glosario de Términos:** Define 3 a 5 conceptos clave del negocio usados en este módulo.
3. **Casos de Uso Principales:** Lista de las acciones principales que un usuario puede realizar.
4. **Flujo Funcional (Diagrama):** Un diagrama de flujo (en Mermaid) fácil de entender que muestre el recorrido del usuario desde que entra hasta que logra su objetivo.
5. **Reglas de Negocio / Validaciones Clave:** Restricciones importantes (ej. "El usuario debe ser mayor de edad", "Los documentos no pueden pesar más de 10MB").

#### PARTE 2: DOCUMENTACIÓN TÉCNICA (Técnica)
*Debe explicar el CÓMO, entrando al detalle del código, patrones, arquitectura y bases de datos.*

6. **Stack Tecnológico y Dependencias:** Lenguajes, frameworks, librerías principales.
7. **Arquitectura del Sistema (Diagrama):** Diagrama (en Mermaid, tipo C4 o similar) mostrando la relación entre el Frontend, Backend, APIs externas y Base de Datos.
8. **Estructura de Componentes / Patrones:** Cómo está organizado el código proporcionado.
9. **Flujo de Datos (Diagrama de Secuencia):** Diagrama en Mermaid que muestre el viaje de los datos.
10. **Modelos de Datos / Entidades Clave:** Descripción de las estructuras de datos principales (JSON payloads, tablas o esquemas).
11. **Guía Rápida de Configuración (Setup):** Pasos resumidos para levantar este módulo en local.

---

**Contexto y Código a analizar:**
A continuación, te proporciono los archivos y el contexto del proyecto. Por favor, genera el documento basado ÚNICAMENTE en la siguiente información:

[INSERTAR AQUÍ TUS ARCHIVOS, REPOSITORIOS O EXPLICACIÓN DEL CÓDIGO]

**[FIN DEL PROMPT]**
***

## 🧩 Segunda Etapa: Sub-Prompts Especializados

*Usa estos prompts de forma aislada cuando necesites documentar a profundidad una API específica o un componente visual del Frontend. Puedes anexar el resultado al "Documento Maestro" o mantenerlos como documentos de referencia separados.*

### 🔌 Sub-Prompt 1: Documentación de APIs (Swagger/REST)

**[INICIO DEL SUB-PROMPT API]**

**Actúa como:** Un API Designer y Technical Writer Experto.

**Objetivo:**
Analizar el código backend/controladores/servicios que te proporcionaré y generar una documentación exhaustiva de los Endpoints de la API en formato Markdown (estilo Swagger/OpenAPI).

**Estructura Requerida:**

1. **Información General:** 
   - Propósito de la API/Servicio.
   - URL Base (o ambiente esperado).
   - Métodos de Autenticación (Ej: Bearer Token, JWT).
2. **Flujo de Interacción (Diagrama):**
   - Un diagrama de secuencia en `Mermaid.js` que muestre cómo el cliente (Frontend/Postman) interactúa con esta API, qué hace el backend internamente y cómo responde.
3. **Detalle por Endpoint:** Para cada endpoint detectado en el código, genera:
   - **Ruta y Método:** Ej: `GET /api/v1/usuarios/{id}`
   - **Descripción:** ¿Qué hace exactamente?
   - **Parámetros:** Query params, Path params o Headers requeridos (Tabla con Nombre, Tipo, Obligatorio, Descripción).
   - **Cuerpo de la Petición (Request Body):** Ejemplo de JSON si aplica.
   - **Respuestas (Responses):**
     - Casos de éxito (Ej: `200 OK`, `201 Created`) con ejemplo de JSON.
     - Casos de error (Ej: `400 Bad Request`, `404 Not Found`, `500 Server Error`) con ejemplo del JSON de error.
4. **Dependencias/Servicios Externos:** ¿Llama a otra API o base de datos interna para responder?

**Código a analizar:**
[INSERTAR AQUÍ CÓDIGO DEL CONTROLLER / ENDPOINT / API]

**[FIN DEL SUB-PROMPT API]**

***

### 🎨 Sub-Prompt 2: Componentes de Interfaz Gráfica (Frontend/UI)

**[INICIO DEL SUB-PROMPT UI]**

**Actúa como:** Un Frontend Engineer Senior y Especialista en UX/UI.

**Objetivo:**
Analizar el código del componente Frontend que te proporcionaré (Vue, React, Angular, etc.) y generar una documentación técnica e interactiva orientada a otros desarrolladores y diseñadores.

**Reglas Especiales:**
- Usa marcadores visuales: `> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aquí captura del componente en estado {Estado} **]**` para indicar dónde deben ir capturas de pantalla.
- Usa Mermaid.js si el componente tiene una lógica de estados compleja (máquina de estados).

**Estructura Requerida:**

1. **Nombre y Propósito del Componente:** ¿Qué es y dónde se usa habitualmente dentro del sistema?
   - *Incluye un Placeholder de Imagen general del componente.*
2. **Propiedades (Props):**
   - Tabla con: Nombre, Tipo de Dato, Valor por Defecto, Requerido, Descripción.
3. **Eventos (Emits/Outputs):**
   - Tabla con: Nombre del Evento, Payload (qué datos envía), Cuándo se dispara.
4. **Estados Visuales (Variantes):**
   - Enumera los estados posibles (Ej: Loading, Disabled, Success, Error) y deja un Placeholder de Imagen para cada uno.
5. **Dependencias y Estado Global:**
   - ¿Consume algún Store global (ej. Pinia/Vuex)? ¿Utiliza Composables/Hooks específicos?
6. **Ejemplo de Uso (Código):**
   - Proporciona un bloque de código mostrando cómo instanciar este componente en otra vista, pasando props y escuchando sus eventos.

**Código a analizar:**
[INSERTAR AQUÍ CÓDIGO DEL COMPONENTE .VUE / .JSX / .TSX]

**[FIN DEL SUB-PROMPT UI]**

***

### 📱 Sub-Prompt 3: Aplicaciones Móviles (Pantallas y Lógica Mobile)

**[INICIO DEL SUB-PROMPT MOBILE]**

**Actúa como:** Un Mobile Engineer Senior (iOS/Android) y Technical Writer Experto.

**Objetivo:**
Analizar el código de la pantalla o módulo móvil que te proporcionaré (Swift, Kotlin, Flutter, React Native, etc.) y generar una documentación técnica exhaustiva.

**Reglas Especiales:**
- Usa marcadores visuales: `> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar captura de pantalla del dispositivo simulador en estado {Estado} **]**`
- Usa Mermaid.js para diagramar la pila de navegación (Navigation Stack) o ciclos de vida complejos.

**Estructura Requerida:**

1. **Nombre y Propósito de la Pantalla/Módulo:** ¿Qué resuelve para el usuario móvil?
   - *Incluye un Placeholder de Imagen general de la vista.*
2. **Plataforma y Framework:** Lenguaje y entorno (ej. Kotlin/Jetpack Compose, Swift/SwiftUI, Flutter).
3. **Permisos y Hardware (Device Features):**
   - Tabla de permisos que solicita esta pantalla (Ej: Cámara, Geolocalización, Notificaciones Push, Bluetooth) y por qué los necesita.
4. **Persistencia y Modo Offline:**
   - ¿Guarda datos locales? (Ej: CoreData, Room, SQLite, UserDefaults). ¿Cómo se comporta si el dispositivo pierde conexión a internet?
5. **Flujo de Navegación (Diagrama):**
   - Diagrama de flujo en Mermaid mostrando de qué pantalla proviene el usuario y hacia qué pantallas puede ir desde aquí.
6. **Gestión del Estado / Arquitectura:**
   - Patrón utilizado (MVVM, Clean Architecture, BLoC, etc.) y cómo se conecta la vista con los datos.
7. **Servicios y APIs consumidas:** Lista de llamadas a red que hace esta vista específica al cargarse o interactuar.

**Código a analizar:**
[INSERTAR AQUÍ CÓDIGO DEL ARCHIVO DE LA VISTA / VIEWMODEL / CONTROLADOR MÓVIL]

**[FIN DEL SUB-PROMPT MOBILE]**