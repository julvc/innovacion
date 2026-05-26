# Guia de Uso — Transcriptor de Video Pro v1.0

**Autor:** Julio Varas Contreras | **Empresa:** SONDA | **Fecha:** Mayo 2026

---

## Descripcion

Transcriptor de Video Pro convierte videos y archivos de audio a documentos
Markdown estructurados usando OpenAI Whisper, un motor de reconocimiento de
voz de alta precision que funciona completamente offline (sin enviar datos a
internet durante la transcripcion).

---

## Requisitos del Sistema

| Componente | Requerimiento |
|-----------|--------------|
| Sistema operativo | Windows 10/11 (64-bit) |
| Python | 3.9 o superior |
| RAM | 4 GB minimo (8 GB recomendado para modelos medium/large) |
| Disco | 500 MB libre + espacio para modelos |
| ffmpeg | Instalado y en PATH del sistema |

---

## Instalacion

### Paso 1 — Instalar ffmpeg

1. Descargar desde: https://ffmpeg.org/download.html  
   (Seleccionar "Windows builds" → gyan.dev o BtbN)
2. Extraer el archivo ZIP en `C:\ffmpeg\`
3. Agregar `C:\ffmpeg\bin` al PATH del sistema:
   - Buscar "Variables de entorno" en el menu de inicio
   - Editar la variable `Path` del sistema
   - Agregar `C:\ffmpeg\bin`
4. Reiniciar la consola y verificar: `ffmpeg -version`

### Paso 2 — Instalar dependencias Python

Ejecutar el script de setup incluido:

```
setup_dependencias.bat
```

*Nota: Este proceso puede tardar varios minutos y descargara aproximadamente 1.5 GB de datos en tu equipo local.*

### Paso 3 — Ejecutar la aplicacion

Una vez finalizada la configuracion, simplemente usa el siguiente archivo
para iniciar la aplicacion cada vez que lo necesites:

```
Iniciar_Transcriptor.bat
```


## Interfaz de Usuario

### Seccion: Archivo de Video / Audio

| Elemento | Descripcion |
|---------|-------------|
| Campo de archivo | Ruta del archivo seleccionado |
| Seleccionar | Abre dialogo para elegir un archivo |
| Cola de archivos | Lista de archivos pendientes de transcribir |
| Agregar Multiples | Selecciona varios archivos a la vez |
| Quitar Seleccionado | Elimina el archivo marcado de la cola |
| Limpiar Lista | Vacia toda la cola |
| Carpeta de Salida | Directorio donde se guardan los archivos generados |

### Seccion: Configuracion

| Elemento | Descripcion |
|---------|-------------|
| Modelo Whisper | Tamano del modelo de IA (ver tabla abajo) |
| Idioma | Idioma del audio (Auto-detectar recomendado) |
| Marcas de tiempo | Agrega [HH:MM:SS] al inicio de cada segmento |
| Agrupar en parrafos | Une frases en bloques de texto coherentes |
| Exportar .txt | Genera copia en texto plano sin formato |
| Exportar .srt | Genera archivo de subtitulos compatible con reproductores |

### Modelos Whisper disponibles

| Modelo | Tamano | Velocidad | Precision | Uso recomendado |
|--------|--------|-----------|-----------|-----------------|
| tiny | ~39 MB | Muy rapido | Basica | Pruebas rapidas |
| base | ~74 MB | Rapido | Buena | **Uso general** |
| small | ~244 MB | Moderado | Alta | Contenido tecnico |
| medium | ~769 MB | Lento | Muy alta | Precision critica |
| large | ~1.5 GB | Muy lento | Maxima | Maxima calidad |

> Los modelos se descargan automaticamente al primer uso en:
> `C:\Users\<usuario>\.cache\whisper\`

---

## Uso Paso a Paso

1. **Seleccionar archivo(s):**
   - Click en "Seleccionar" para un archivo
   - Click en "Agregar Multiples" para procesar varios en secuencia

2. **Configurar opciones:**
   - Seleccionar el modelo (recomendado: `base` para inicio)
   - Seleccionar idioma (dejar en Auto-detectar si hay dudas)
   - Marcar opciones de exportacion deseadas

3. **Seleccionar carpeta de salida** (por defecto: `Documentos/Transcripciones`)

4. **Click en "Transcribir":**
   - Primera vez: el modelo se descarga automaticamente
   - El log muestra el progreso en tiempo real
   - La barra de progreso indica que el proceso esta activo

5. **Al finalizar:**
   - Click en "Abrir Carpeta de Salida" para ver los archivos
   - O navegar manualmente a la carpeta configurada

---

## Formato del Markdown Generado

Cada transcripcion genera un archivo `<nombre_video>_transcripcion.md`:

```markdown
# Transcripcion: mi_video.mp4

| Campo | Valor |
|-------|-------|
| Archivo | `mi_video.mp4` |
| Modelo Whisper | `base` |
| Idioma detectado | `es` |
| Duracion | `01:23:45` |
| Segmentos | `312` |
| Fecha de transcripcion | `2026-05-20 10:30:00` |

---

## Contenido

**[00:00:00]** Bienvenidos a esta sesion de capacitacion...

**[00:01:15]** El objetivo de hoy es revisar los procesos de QA...

---
*Generado con Transcriptor de Video Pro v1.0 | SONDA | 2026-05-20*
```

---

## Exportaciones Disponibles

| Formato | Extension | Contenido |
|---------|-----------|-----------|
| Markdown | `.md` | Siempre generado. Metadatos + contenido formateado |
| Texto plano | `.txt` | Solo el texto sin formato ni marcas de tiempo |
| Subtitulos | `.srt` | Compatible con VLC, YouTube, Premiere Pro, etc. |

---

## Cancelar una Transcripcion

Click en el boton "Cancelar" durante el proceso. El archivo que se esta
procesando en ese momento finalizara su segmento actual antes de detenerse.

---

## Compilar como Ejecutable (.exe)

Para distribuir sin necesidad de Python instalado:

```
build_exe.bat
```

El ejecutable resultante estara en `dist\Transcriptor.exe`.

> **Nota:** El ejecutable ahora esta diseñado para ser **ligero** (oculta el codigo fuente 
> sin incluir las librerias pesadas de Inteligencia Artificial). 
> Para distribuirlo, debes empaquetar unicamente `Transcriptor.exe` y `setup_dependencias.bat`.
> El usuario final ejecutara el setup para descargar las dependencias.


## Problemas Frecuentes

### "ffmpeg no encontrado en PATH"
- Instalar ffmpeg y agregar `bin/` al PATH del sistema
- Reiniciar la consola o la aplicacion
- Si usas el ejecutable (`.exe`), este error no debería aparecer ya que incluye ffmpeg.

### "openai-whisper no instalado"
- Ejecutar `setup_dependencias.bat`
- O: `pip install openai-whisper`

### El audio es largo y tarda mucho
- Usar modelo `tiny` o `base` para archivos muy largos
- Los modelos `medium` y `large` pueden tardar el doble del tiempo real del video

### Error de memoria (RAM insuficiente)
- Usar modelo mas pequeno (`tiny` o `base`)
- Cerrar otras aplicaciones antes de transcribir

### El idioma no se detecta correctamente
- Seleccionar el idioma manualmente en el desplegable
- Verificar que el audio tenga buena calidad de grabacion

### Los subtitulos .srt no sincronizan bien
- Verificar que el video original no este cortado o tenga gaps
- Usar modelo `small` o superior para mejor precision temporal

---

## Formatos de Archivo Soportados

**Video:** `.mp4` `.mkv` `.avi` `.mov` `.wmv` `.flv` `.webm`  
**Audio:** `.mp3` `.wav` `.m4a` `.ogg` `.flac` `.aac`

---

## Informacion de Licencia

Este software ha sido creado para uso exclusivo de SONDA.  
Queda estrictamente prohibida su distribucion, copia, modificacion o
divulgacion a terceros sin autorizacion expresa del autor.

**© 2026 Julio Varas Contreras — Todos los derechos reservados.**
