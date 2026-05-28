"""
Templates de contenido pre-rellenado para cada seccion.

Estructura: { tipo_proyecto: { seccion_id: contenido_markdown } }

Los templates siguen el Super Prompt Maestro:
  PARTE 1 — Vision Funcional / Negocio  (no tecnico)
  PARTE 2 — Documentacion Tecnica        (tecnico)
  Sub-prompts: API, UI/Frontend, Mobile
"""
from __future__ import annotations

# ——— Templates base por seccion ——————————————————————————————
# {seccion_id: template_base} — personalizable segun tipo de proyecto
_TMPL_RESUMEN_WEB = """\
## Resumen Ejecutivo

### ¿Que hace este sistema?
[Descripcion en 2-3 oraciones. Que problema de negocio resuelve. Sin terminos tecnicos.]

### Beneficios Principales
- **[Beneficio 1]:** Descripcion del valor para el negocio.
- **[Beneficio 2]:** Descripcion del valor para el negocio.
- **[Beneficio 3]:** Descripcion del valor para el negocio.

### Usuarios del Sistema
| Tipo de Usuario | Rol en el Sistema |
|-----------------|-------------------|
| Administrador   | [Descripcion]     |
| Usuario Final   | [Descripcion]     |

> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura de la pantalla principal del sistema **]**
"""

_TMPL_RESUMEN_MOBILE = """\
## Resumen Ejecutivo

### ¿Que hace esta aplicacion movil?
[Descripcion en 2-3 oraciones. Problema que resuelve al usuario en su dispositivo movil. Sin terminos tecnicos.]

### Plataformas Disponibles
- [ ] iOS (iPhone / iPad)
- [ ] Android

### Beneficios Principales
- **[Beneficio 1]:** Descripcion del valor para el usuario movil.
- **[Beneficio 2]:** Descripcion del valor para el usuario movil.

> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui capturas de las pantallas principales en iPhone y Android **]**
"""

_TMPL_RESUMEN_QA = """\
## Resumen Ejecutivo

### ¿Que cubre este plan de pruebas?
[Descripcion del sistema bajo prueba. Que modulos, funcionalidades o flujos se van a verificar.]

### Objetivo de Calidad
Garantizar que [nombre del sistema] cumpla con los criterios de aceptacion definidos,
asegurando su correcto funcionamiento en los escenarios de uso mas criticos.

### Metricas Meta
| Metrica                     | Valor Objetivo |
|-----------------------------|----------------|
| Cobertura de casos de prueba| >= 80%         |
| Tasa de defectos criticos   | 0 bugs criticos|
| Casos de prueba exitosos    | >= 95%         |
"""

_TMPL_GLOSARIO = """\
## Glosario de Terminos

| Termino | Definicion en lenguaje de negocio |
|---------|-----------------------------------|
| **[Termino 1]** | [Definicion clara sin tecnicismos] |
| **[Termino 2]** | [Definicion clara sin tecnicismos] |
| **[Termino 3]** | [Definicion clara sin tecnicismos] |
| **[Termino 4]** | [Definicion clara sin tecnicismos] |
| **[Termino 5]** | [Definicion clara sin tecnicismos] |

> Consejo: Usa terminos que el negocio usa en sus conversaciones diarias.
"""

_TMPL_CASOS_USO = """\
## Casos de Uso Principales

| ID    | Actor           | Accion                          | Resultado Esperado              |
|-------|-----------------|---------------------------------|---------------------------------|
| CU-01 | [Actor]         | [El actor puede...]             | [El sistema responde con...]    |
| CU-02 | [Actor]         | [El actor puede...]             | [El sistema responde con...]    |
| CU-03 | [Actor]         | [El actor puede...]             | [El sistema responde con...]    |
| CU-04 | [Actor]         | [El actor puede...]             | [El sistema responde con...]    |
| CU-05 | [Actor]         | [El actor puede...]             | [El sistema responde con...]    |

### Casos de Uso Prioritarios
Los casos de uso mas criticos para el negocio son: **CU-01**, **CU-02**.
"""

_TMPL_FLUJO_WEB = """\
## Flujo Funcional del Sistema

```mermaid
flowchart TD
    A([Usuario accede al sistema]) --> B{¿Autenticado?}
    B -- No --> C[Pantalla de Login]
    C --> D[Ingresa credenciales]
    D --> E{¿Credenciales validas?}
    E -- No --> F[Mostrar error de autenticacion]
    F --> C
    E -- Si --> G[Dashboard principal]
    B -- Si --> G
    G --> H{¿Que desea hacer?}
    H --> I[Accion 1: ...]
    H --> J[Accion 2: ...]
    H --> K[Accion 3: ...]
    I --> L([Fin del flujo])
    J --> L
    K --> L
```

> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura del flujo navegacional principal **]**
"""

_TMPL_FLUJO_MOBILE = """\
## Flujo Funcional de la Aplicacion

```mermaid
flowchart TD
    A([Usuario abre la app]) --> B{¿Session activa?}
    B -- No --> C[Pantalla de Bienvenida / Login]
    C --> D[Ingresa credenciales o biometria]
    D --> E{¿Autenticacion exitosa?}
    E -- No --> F[Mostrar error]
    F --> C
    E -- Si --> G[Pantalla Principal / Home]
    B -- Si --> G
    G --> H{¿Que desea hacer?}
    H --> I[Funcionalidad 1]
    H --> J[Funcionalidad 2]
    H --> K[Funcionalidad 3]
    I --> L([Fin del flujo])
```

> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui capturas de las pantallas clave del flujo **]**
"""

_TMPL_FLUJO_QA = """\
## Flujo de Proceso de Pruebas

```mermaid
flowchart TD
    A([Inicio del ciclo de pruebas]) --> B[Preparar entorno de pruebas]
    B --> C[Ejecutar casos de prueba]
    C --> D{¿Resultado?}
    D -- Exitoso --> E[Marcar caso como PASS]
    D -- Fallido --> F[Registrar defecto]
    F --> G[Asignar severidad y prioridad]
    G --> H[Desarrollador corrige]
    H --> I[Re-ejecutar caso fallido]
    I --> D
    E --> J{¿Mas casos?}
    J -- Si --> C
    J -- No --> K[Generar reporte de pruebas]
    K --> L([Fin del ciclo])
```
"""

_TMPL_REGLAS_NEGOCIO = """\
## Reglas de Negocio y Validaciones Clave

### Restricciones del Sistema
| # | Regla de Negocio | Impacto si se viola |
|---|------------------|---------------------|
| RN-01 | [Descripcion de la regla] | [Consecuencia] |
| RN-02 | [Descripcion de la regla] | [Consecuencia] |
| RN-03 | [Descripcion de la regla] | [Consecuencia] |

### Validaciones Criticas
- **Formato de datos:** [Ej: El email debe tener formato valido]
- **Limites:** [Ej: Los archivos no pueden superar 10MB]
- **Permisos:** [Ej: Solo administradores pueden eliminar registros]
- **Negocio:** [Ej: No se pueden procesar pedidos con stock < 0]
"""

_TMPL_STACK = """\
## Stack Tecnologico y Dependencias

### Tecnologias Principales
| Capa           | Tecnologia       | Version  | Proposito                    |
|----------------|------------------|----------|------------------------------|
| Frontend       | [Framework]      | [v.x.x]  | [Descripcion]                |
| Backend        | [Framework]      | [v.x.x]  | [Descripcion]                |
| Base de Datos  | [Motor BD]       | [v.x.x]  | [Descripcion]                |
| Autenticacion  | [Libreria/Servicio] | [v.x.x] | [Descripcion]              |
| Deploy         | [Plataforma]     | -        | [Descripcion]                |

### Dependencias Clave (package.json / requirements.txt)
```
[Listar dependencias principales con version]
```

### Servicios Externos
| Servicio | Proposito | Documentacion |
|----------|-----------|---------------|
| [Servicio] | [Para que se usa] | [URL/referencia] |
"""

_TMPL_ARQUITECTURA = """\
## Arquitectura del Sistema

### Diagrama de Contexto C4

```mermaid
C4Context
  title Arquitectura del Sistema — [Nombre del Proyecto]

  Person(user, "Usuario Final", "Usa el sistema a traves del browser o app movil")
  Person(admin, "Administrador", "Gestiona configuracion y usuarios")

  System(system, "[Nombre del Sistema]", "Descripcion breve del sistema")

  SystemDb_Ext(db, "Base de Datos", "Almacena datos del negocio")
  System_Ext(auth, "Servicio de Autenticacion", "OAuth2 / JWT")
  System_Ext(external, "API Externa", "Integracion con terceros")

  Rel(user,   system,   "Usa",   "HTTPS")
  Rel(admin,  system,   "Administra", "HTTPS")
  Rel(system, db,       "Lee / Escribe", "TCP")
  Rel(system, auth,     "Valida tokens", "HTTPS")
  Rel(system, external, "Consume API",   "HTTPS/REST")
```

> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui diagrama de arquitectura detallado **]**
"""

_TMPL_COMPONENTES_WEB = """\
## Estructura de Componentes

### Patron de Arquitectura
**Patron utilizado:** [MVC / MVVM / Clean Architecture / Hexagonal / etc.]

### Estructura de Carpetas (Frontend)
```
src/
├── components/          # Componentes reutilizables
│   ├── common/          # Botones, inputs, cards
│   └── features/        # Componentes de negocio
├── pages/               # Vistas/pantallas principales
├── services/            # Llamadas a API
├── stores/              # Estado global (Redux/Pinia/Zustand)
├── hooks/               # Custom hooks
└── utils/               # Utilidades comunes
```

### Estructura de Carpetas (Backend)
```
src/
├── controllers/         # Manejo de requests HTTP
├── services/            # Logica de negocio
├── repositories/        # Acceso a datos
├── models/              # Entidades de BD
├── middleware/          # Auth, logging, validacion
└── config/              # Configuracion de la app
```
"""

_TMPL_COMPONENTES_MOBILE = """\
## Estructura de Componentes

### Patron de Arquitectura
**Patron utilizado:** [MVVM / Clean Architecture / BLoC / MVP]

### Estructura de Carpetas
```
lib/ (Flutter) o src/ (React Native)
├── presentation/        # UI: screens, widgets/components
│   ├── screens/         # Pantallas principales
│   └── widgets/         # Componentes reutilizables
├── domain/              # Logica de negocio
│   ├── entities/        # Modelos del dominio
│   └── usecases/        # Casos de uso
├── data/                # Fuentes de datos
│   ├── repositories/    # Implementacion de repos
│   ├── datasources/     # API, local DB
│   └── models/          # DTOs / modelos de datos
└── core/                # Utilidades, DI, constantes
```
"""

_TMPL_FLUJO_DATOS = """\
## Flujo de Datos — Diagrama de Secuencia

### Flujo Principal: [Nombre del Flujo]

```mermaid
sequenceDiagram
    autonumber
    participant U  as Usuario / Cliente
    participant FE as Frontend
    participant API as Backend API
    participant SVC as Servicio
    participant DB  as Base de Datos

    U  ->> FE:  Realiza accion en UI
    FE ->> API: POST /api/v1/[endpoint] + JWT
    API ->> API: Validar token y permisos
    API ->> SVC: Llama a metodo de servicio(params)
    SVC ->> DB:  SELECT / INSERT / UPDATE
    DB  -->> SVC: Resultado de la operacion
    SVC -->> API: Objeto de respuesta
    API -->> FE:  200 OK { data: {...} }
    FE  -->> U:  Actualiza UI con resultado
```

### Flujo de Error

```mermaid
sequenceDiagram
    participant U  as Usuario
    participant FE as Frontend
    participant API as Backend API

    U  ->> FE:  Realiza accion
    FE ->> API: Request con datos invalidos
    API -->> FE: 400 Bad Request { error: "..." }
    FE -->> U:  Muestra mensaje de error
```
"""

_TMPL_MODELOS_DATOS = """\
## Modelos de Datos / Entidades Clave

### Entidad Principal: [NombreEntidad]

#### Esquema de Base de Datos
```sql
CREATE TABLE [nombre_tabla] (
    id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre      VARCHAR(255) NOT NULL,
    descripcion TEXT,
    estado      VARCHAR(50)  NOT NULL DEFAULT 'activo',
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);
```

#### JSON Payload (Request)
```json
{
  "nombre":      "string (requerido)",
  "descripcion": "string (opcional)",
  "estado":      "enum: activo | inactivo"
}
```

#### JSON Payload (Response)
```json
{
  "id":          "uuid",
  "nombre":      "string",
  "descripcion": "string | null",
  "estado":      "string",
  "created_at":  "ISO 8601",
  "updated_at":  "ISO 8601"
}
```

### Relaciones Entre Entidades
```mermaid
erDiagram
    ENTIDAD_A {
        uuid id PK
        string nombre
        string estado
    }
    ENTIDAD_B {
        uuid id PK
        uuid entidad_a_id FK
        string valor
    }
    ENTIDAD_A ||--o{ ENTIDAD_B : "tiene"
```
"""

_TMPL_SETUP = """\
## Guia Rapida de Configuracion (Setup Local)

### Requisitos Previos
| Herramienta | Version Minima | Instalacion |
|-------------|----------------|-------------|
| [Runtime]   | [v.x.x]        | [URL]       |
| [BD]        | [v.x.x]        | [URL]       |
| [Otro]      | [v.x.x]        | [URL]       |

### Pasos de Instalacion

```bash
# 1. Clonar el repositorio
git clone [URL_REPOSITORIO]
cd [nombre-proyecto]

# 2. Instalar dependencias
[npm install / pip install -r requirements.txt / flutter pub get]

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores locales

# 4. Inicializar base de datos
[Comando de migraciones]

# 5. Cargar datos de prueba (opcional)
[Comando seed]

# 6. Iniciar servidor de desarrollo
[Comando de inicio]
```

### Variables de Entorno Requeridas
| Variable          | Descripcion                   | Ejemplo          |
|-------------------|-------------------------------|------------------|
| `DATABASE_URL`    | Conexion a base de datos      | `postgres://...` |
| `SECRET_KEY`      | Clave secreta de la app       | `[generada]`     |
| `API_BASE_URL`    | URL base del backend          | `http://localhost:8000` |

### Verificar Instalacion
```bash
# La app debe estar disponible en:
[URL local, ej: http://localhost:3000]
```
"""

# ——— Templates especializados: API ——————————————————————————
_TMPL_API_INFO = """\
## Informacion General de la API

### Descripcion
[Proposito de esta API: que operaciones expone y que problema de negocio resuelve]

### URL Base
```
Desarrollo  : http://localhost:[puerto]/api/v1
Staging     : https://staging.[dominio]/api/v1
Produccion  : https://[dominio]/api/v1
```

### Autenticacion
**Metodo:** Bearer Token (JWT)

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

| Header          | Valor                      | Requerido |
|-----------------|----------------------------|-----------|
| Authorization   | `Bearer {token}`           | Si        |
| Content-Type    | `application/json`         | Si (POST) |
| Accept          | `application/json`         | Si        |
"""

_TMPL_API_FLUJO = """\
## Flujo de Interaccion con la API

```mermaid
sequenceDiagram
    autonumber
    participant C  as Cliente (Frontend/Postman)
    participant GW as API Gateway / Router
    participant MW as Middleware (Auth + Validacion)
    participant SVC as Servicio de Negocio
    participant DB  as Base de Datos

    C  ->> GW:  HTTP Request + Bearer Token
    GW ->> MW:  Verificar token JWT
    MW -->> GW: Token valido | 401 Unauthorized
    GW ->> SVC: Ejecutar logica de negocio
    SVC ->> DB: Operacion CRUD
    DB  -->> SVC: Resultado
    SVC -->> GW: DTO de respuesta
    GW  -->> C:  200 OK / 4xx / 5xx + JSON
```
"""

_TMPL_API_ENDPOINTS = """\
## Detalle de Endpoints

---

### `GET /api/v1/[recurso]`
**Descripcion:** Lista todos los recursos con paginacion.

**Query Parameters:**
| Parametro | Tipo    | Requerido | Descripcion                    |
|-----------|---------|-----------|--------------------------------|
| `page`    | integer | No        | Numero de pagina (default: 1)  |
| `limit`   | integer | No        | Items por pagina (default: 20) |
| `search`  | string  | No        | Filtro de busqueda             |

**Response 200 OK:**
```json
{
  "data": [
    {
      "id":   "uuid",
      "nombre": "string",
      "estado": "string"
    }
  ],
  "pagination": {
    "page":       1,
    "limit":     20,
    "total":    100,
    "pages":      5
  }
}
```

---

### `POST /api/v1/[recurso]`
**Descripcion:** Crea un nuevo recurso.

**Request Body:**
```json
{
  "nombre":      "string (requerido)",
  "descripcion": "string (opcional)"
}
```

**Response 201 Created:**
```json
{
  "id":          "uuid",
  "nombre":      "string",
  "created_at":  "ISO 8601"
}
```

**Errores:**
| Codigo | Descripcion              | Body                                    |
|--------|--------------------------|-----------------------------------------|
| 400    | Datos invalidos          | `{"error": "nombre es requerido"}`      |
| 401    | No autenticado           | `{"error": "Token invalido o expirado"}`|
| 409    | Conflicto / duplicado    | `{"error": "El recurso ya existe"}`     |
| 500    | Error interno del servidor | `{"error": "Internal Server Error"}`  |

---

### `GET /api/v1/[recurso]/{id}`
**Descripcion:** Obtiene un recurso por su ID.

**Path Parameters:**
| Parametro | Tipo   | Requerido | Descripcion        |
|-----------|--------|-----------|--------------------|
| `id`      | uuid   | Si        | ID del recurso     |

**Response 200 OK:**
```json
{
  "id":          "uuid",
  "nombre":      "string",
  "descripcion": "string",
  "created_at":  "ISO 8601"
}
```

**Response 404 Not Found:**
```json
{
  "error": "Recurso no encontrado"
}
```
"""

_TMPL_API_DEPS = """\
## Dependencias y Servicios Externos

| Servicio / BD         | Tipo              | Proposito                              | URL/Host              |
|-----------------------|-------------------|----------------------------------------|-----------------------|
| [Base de Datos]       | PostgreSQL / MySQL | Persistencia principal de datos       | `localhost:[puerto]`  |
| [Cache]               | Redis              | Cache de sesiones / resultados         | `localhost:6379`      |
| [Servicio externo]    | REST API           | [Descripcion del proposito]            | `https://[url]`       |
| [Mensajeria]          | RabbitMQ / Kafka   | Procesamiento asincrono                | `localhost:[puerto]`  |
"""

# ——— Templates especializados: UI/Frontend ——————————————————
_TMPL_UI_COMP_NOMBRE = """\
## Nombre y Proposito del Componente

### Identificacion
**Nombre del componente:** `[NombreComponente]`
**Ubicacion en el proyecto:** `src/components/[ruta/NombreComponente]`
**Tipo:** [ ] Componente de presentacion  [ ] Componente contenedor  [ ] Componente mixto

### Proposito
[Descripcion de que hace este componente y donde se usa dentro del sistema.
Mencionar en que pantallas o flujos aparece.]

> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura general del componente en estado normal **]**
"""

_TMPL_UI_PROPS = """\
## Propiedades (Props)

| Nombre     | Tipo de Dato   | Valor Default | Requerido | Descripcion                    |
|------------|----------------|---------------|-----------|--------------------------------|
| `prop1`    | `string`       | `''`          | Si        | [Descripcion de la prop]       |
| `prop2`    | `boolean`      | `false`       | No        | [Descripcion de la prop]       |
| `prop3`    | `() => void`   | `-`           | No        | Callback al hacer click        |
| `prop4`    | `string[]`     | `[]`          | No        | Lista de elementos a mostrar   |
"""

_TMPL_UI_EVENTOS = """\
## Eventos (Emits / Outputs)

| Nombre del Evento | Payload                         | Cuando se Dispara                    |
|-------------------|---------------------------------|--------------------------------------|
| `on-click`        | `{ id: string, data: object }`  | Al hacer click en el elemento        |
| `on-change`       | `{ value: string }`             | Al cambiar el valor del input        |
| `on-close`        | `void`                          | Al cerrar el componente              |
| `on-submit`       | `FormData`                      | Al enviar el formulario              |
"""

_TMPL_UI_ESTADOS = """\
## Estados Visuales (Variantes)

### Default
Estado normal del componente con datos cargados.
> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura del componente en estado Default **]**

### Loading
Mientras se cargan los datos o se procesa una accion.
> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura del componente en estado Loading **]**

### Error
Cuando ocurre un error al cargar datos o al procesar.
> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura del componente en estado Error **]**

### Empty
Cuando no hay datos que mostrar.
> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura del componente en estado Empty **]**

### Disabled
Cuando el componente esta deshabilitado.
> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura del componente en estado Disabled **]**
"""

_TMPL_UI_DEPS = """\
## Dependencias y Estado Global

### Stores / Estado Global
| Store      | Estado Utilizado     | Accion Ejecutada          |
|------------|----------------------|---------------------------|
| `[Store]`  | `[nombre_estado]`    | `[nombre_accion]()`       |

### Composables / Hooks Utilizados
| Hook / Composable   | Proposito                              |
|---------------------|----------------------------------------|
| `use[NombreHook]()` | [Para que se usa en este componente]   |

### Dependencias Externas
| Libreria    | Version | Uso en el componente       |
|-------------|---------|----------------------------|
| [Libreria]  | v.x.x   | [Para que se usa]          |
"""

_TMPL_UI_EJEMPLO = """\
## Ejemplo de Uso (Codigo)

### Uso Basico
```tsx
import { NombreComponente } from '@/components/[ruta]'

function MiPantalla() {
  const handleClick = (data) => {
    console.log('Click recibido:', data)
  }

  return (
    <NombreComponente
      prop1="valor"
      prop2={true}
      onAction={handleClick}
    />
  )
}
```

### Uso con Estado
```tsx
import { useState }          from 'react'
import { NombreComponente } from '@/components/[ruta]'

function MiPantalla() {
  const [items, setItems] = useState([])

  return (
    <NombreComponente
      prop1="valor"
      items={items}
      onSubmit={(data) => setItems(prev => [...prev, data])}
      onClose={() => console.log('cerrado')}
    />
  )
}
```
"""

# ——— Templates especializados: Mobile ————————————————————————
_TMPL_MOB_NOMBRE = """\
## Nombre y Proposito de la Pantalla

**Nombre de la pantalla:** `[NombrePantalla]Screen`
**Ruta de navegacion:** `[ruta en el navigator]`
**Archivo:** `[ruta/NombrePantalla.swift|kt|dart|tsx]`

### Proposito
[Que resuelve esta pantalla para el usuario movil. Que tarea completa aqui.]

> 🖼️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura de la pantalla en simulador iPhone / Android **]**
"""

_TMPL_MOB_PLATAFORMA = """\
## Plataforma y Framework

| Aspecto           | Detalle                                        |
|-------------------|------------------------------------------------|
| Plataforma        | [ ] iOS  [ ] Android  [ ] Cross-platform       |
| Lenguaje          | [Swift / Kotlin / Dart / TypeScript]           |
| Framework UI      | [SwiftUI / Jetpack Compose / Flutter / RN]     |
| Version minima OS | iOS [v.x]  /  Android API [nivel]              |
| Version actual    | [v.x.x del proyecto]                           |
"""

_TMPL_MOB_PERMISOS = """\
## Permisos y Hardware (Device Features)

| Permiso               | Plataforma     | Por que se necesita                    |
|-----------------------|----------------|----------------------------------------|
| Camara                | iOS / Android  | [Descripcion del uso]                  |
| Geolocalizacion       | iOS / Android  | [Descripcion del uso]                  |
| Notificaciones Push   | iOS / Android  | [Descripcion del uso]                  |
| Almacenamiento        | iOS / Android  | [Descripcion del uso]                  |
| [Otro permiso]        | [Plataforma]   | [Descripcion del uso]                  |

### Solicitud de Permisos
Los permisos se solicitan en: [momento en que se piden, ej: primer uso, al abrir camara]

```
iOS (Info.plist):
NSCameraUsageDescription: "[Texto explicativo para el usuario]"

Android (AndroidManifest.xml):
<uses-permission android:name="android.permission.CAMERA" />
```
"""

_TMPL_MOB_OFFLINE = """\
## Persistencia y Modo Offline

### Almacenamiento Local
| Tecnologia           | Uso                                        |
|----------------------|--------------------------------------------|
| [CoreData/Room/Hive] | [Datos que se guardan localmente]          |
| [UserDefaults/Prefs] | [Preferencias del usuario]                 |
| [Keychain/Keystore]  | [Datos sensibles: tokens, credenciales]    |

### Comportamiento Sin Conexion
- **Con conexion:** [Comportamiento normal]
- **Sin conexion:** [Que funciona en modo offline, que se deshabilita]
- **Al recuperar conexion:** [Como se sincronizan los datos]

### Estrategia de Cache
```
Cache-First: [datos que se leen primero del cache]
Network-First: [datos que siempre requieren conexion]
```
"""

_TMPL_MOB_NAVEGACION = """\
## Flujo de Navegacion

```mermaid
flowchart TD
    A[Pantalla Anterior] --> B[**Esta Pantalla**]
    B --> C{Accion del usuario}
    C -- Accion 1 --> D[Pantalla Destino 1]
    C -- Accion 2 --> E[Pantalla Destino 2]
    C -- Volver --> A
    D --> F([Fin del flujo])
    E --> F
```

### Parametros de Navegacion
| Parametro    | Tipo     | Requerido | Descripcion                    |
|--------------|----------|-----------|--------------------------------|
| `[param1]`   | `string` | Si        | [Para que se usa]              |
| `[param2]`   | `object` | No        | [Para que se usa]              |
"""

_TMPL_MOB_ESTADO = """\
## Gestion del Estado / Arquitectura

### Patron Utilizado
**Patron:** [MVVM / Clean Architecture / BLoC / Provider / Redux]

### Capas de la Pantalla
```
View (UI)
  └── [NombrePantalla]Screen
       ↕ binding / observe
ViewModel / Controller / BLoC
  └── [NombrePantalla]ViewModel
       ↕ llama
Repository
  └── [Nombre]Repository
       ↕ datasource
DataSource (Remote + Local)
  └── [Nombre]RemoteDataSource
  └── [Nombre]LocalDataSource
```

### Estado de la Pantalla
```dart // o Swift / Kotlin
enum [NombrePantalla]State {
  initial,
  loading,
  success,
  error,
}
```
"""

_TMPL_MOB_APIS = """\
## Servicios y APIs Consumidas

| Endpoint                   | Metodo | Cuando se llama                        | Response esperado      |
|----------------------------|--------|----------------------------------------|------------------------|
| `/api/v1/[recurso]`        | GET    | Al cargar la pantalla                  | Lista de recursos      |
| `/api/v1/[recurso]/{id}`   | GET    | Al seleccionar un item                 | Detalle del recurso    |
| `/api/v1/[recurso]`        | POST   | Al enviar el formulario                | Recurso creado         |

### Manejo de Errores de Red
- **Timeout (> 30s):** Mostrar alerta con opcion de reintentar
- **Sin conexion:** Usar cache local si disponible, sino mostrar banner offline
- **500 Server Error:** Mostrar mensaje de error generico con codigo
"""

# ——— Diccionario principal: tipo → { seccion_id: template } ——
_BASE_SECTIONS: dict[str, str] = {
    "Resumen Ejecutivo":                  _TMPL_RESUMEN_WEB,
    "Glosario de Terminos":               _TMPL_GLOSARIO,
    "Casos de Uso Principales":           _TMPL_CASOS_USO,
    "Flujo Funcional (Diagrama)":         _TMPL_FLUJO_WEB,
    "Reglas de Negocio / Validaciones Clave": _TMPL_REGLAS_NEGOCIO,
    "Stack Tecnologico y Dependencias":   _TMPL_STACK,
    "Arquitectura del Sistema (Diagrama)": _TMPL_ARQUITECTURA,
    "Estructura de Componentes / Patrones": _TMPL_COMPONENTES_WEB,
    "Flujo de Datos (Diagrama de Secuencia)": _TMPL_FLUJO_DATOS,
    "Modelos de Datos / Entidades Clave": _TMPL_MODELOS_DATOS,
    "Guia Rapida de Configuracion (Setup)": _TMPL_SETUP,
    # API sub-prompt
    "Informacion General de la API":       _TMPL_API_INFO,
    "Flujo de Interaccion API (Diagrama)": _TMPL_API_FLUJO,
    "Detalle de Endpoints":                _TMPL_API_ENDPOINTS,
    "Dependencias y Servicios Externos API": _TMPL_API_DEPS,
    # UI sub-prompt
    "Nombre y Proposito del Componente":   _TMPL_UI_COMP_NOMBRE,
    "Propiedades (Props)":                 _TMPL_UI_PROPS,
    "Eventos (Emits/Outputs)":             _TMPL_UI_EVENTOS,
    "Estados Visuales (Variantes)":        _TMPL_UI_ESTADOS,
    "Dependencias y Estado Global":        _TMPL_UI_DEPS,
    "Ejemplo de Uso (Codigo)":             _TMPL_UI_EJEMPLO,
    # Mobile sub-prompt
    "Nombre y Proposito de la Pantalla":   _TMPL_MOB_NOMBRE,
    "Plataforma y Framework Mobile":       _TMPL_MOB_PLATAFORMA,
    "Permisos y Hardware (Device Features)": _TMPL_MOB_PERMISOS,
    "Persistencia y Modo Offline":         _TMPL_MOB_OFFLINE,
    "Flujo de Navegacion Mobile (Diagrama)": _TMPL_MOB_NAVEGACION,
    "Gestion del Estado / Arquitectura Mobile": _TMPL_MOB_ESTADO,
    "Servicios y APIs Consumidas":         _TMPL_MOB_APIS,
}

_OVERRIDES: dict[str, dict[str, str]] = {
    "Mobile": {
        "Resumen Ejecutivo":        _TMPL_RESUMEN_MOBILE,
        "Flujo Funcional (Diagrama)": _TMPL_FLUJO_MOBILE,
        "Estructura de Componentes / Patrones": _TMPL_COMPONENTES_MOBILE,
    },
    "QA": {
        "Resumen Ejecutivo":        _TMPL_RESUMEN_QA,
        "Flujo Funcional (Diagrama)": _TMPL_FLUJO_QA,
        "Estructura de Componentes / Patrones": _TMPL_COMPONENTES_WEB,
    },
}

# Los tipos compuestos heredan overrides del tipo base
_TYPE_ALIAS = {
    "Web":         "Web",
    "Mobile":      "Mobile",
    "QA":          "QA",
    "Web + QA":    "Web",
    "Mobile + QA": "Mobile",
    "Full Stack":  "Web",
}


def get_template(section_id: str, project_type: str = "Web") -> str:
    """
    Devuelve el template pre-rellenado para una seccion y tipo de proyecto.
    Primero busca override por tipo, luego base general.
    """
    base_type = _TYPE_ALIAS.get(project_type, "Web")
    override  = _OVERRIDES.get(base_type, {})
    return override.get(section_id) or _BASE_SECTIONS.get(section_id, "")


def prefill_project_sections(project: dict) -> dict:
    """
    Rellena project['sections'] con templates para todas las secciones vacias.
    Retorna el proyecto modificado.
    """
    from project_manager import get_sections_for_type
    ptype   = project.get("type",    "Web")
    profile = project.get("profile", "Ambos")

    sections_def = get_sections_for_type(ptype, profile)
    if "sections" not in project:
        project["sections"] = {}

    for group, items in sections_def.items():
        for section_id in items:
            if not project["sections"].get(section_id, "").strip():
                tmpl = get_template(section_id, ptype)
                if tmpl:
                    project["sections"][section_id] = tmpl

    return project
