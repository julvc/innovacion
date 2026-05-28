"""
Conector seguro a proveedores de IA.
La API key NUNCA se loguea ni se imprime.
Soporta: OpenAI, Anthropic, Google Gemini, Ollama (local).
"""
from __future__ import annotations

import json


def test_connection(provider: str, model: str, base_url: str, key: str) -> tuple[bool, str]:
    """Prueba la conexion con el proveedor. Devuelve (ok, mensaje)."""
    try:
        import requests
    except ImportError:
        return False, "requests no instalado. Ejecuta: pip install requests"

    try:
        if "OpenAI" in provider or "Ollama" in provider:
            return _test_openai_compat(model, base_url or "https://api.openai.com/v1", key)
        elif "Anthropic" in provider:
            return _test_anthropic(model, key)
        elif "Google" in provider or "Gemini" in provider:
            return _test_gemini(model, key)
        else:
            return False, f"Proveedor no soportado: {provider}"
    except Exception as e:
        return False, str(e)


def _test_openai_compat(model: str, base_url: str, key: str) -> tuple[bool, str]:
    import requests
    url = f"{base_url.rstrip('/')}/models"
    headers = {"Authorization": f"Bearer {key}"}
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code == 200:
        return True, f"Conexion OK. Modelo: {model}"
    return False, f"HTTP {r.status_code}: {r.text[:200]}"


def _test_anthropic(model: str, key: str) -> tuple[bool, str]:
    import requests
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key":         key,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
    }
    payload = {
        "model": model or "claude-3-5-haiku-20241022",
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "ping"}],
    }
    r = requests.post(url, headers=headers, json=payload, timeout=15)
    if r.status_code == 200:
        return True, f"Conexion OK. Modelo: {model}"
    return False, f"HTTP {r.status_code}: {r.text[:200]}"


def _test_gemini(model: str, key: str) -> tuple[bool, str]:
    import requests
    m = model or "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": "ping"}]}]}
    r = requests.post(url, json=payload, timeout=15)
    if r.status_code == 200:
        return True, f"Conexion OK. Modelo: {m}"
    return False, f"HTTP {r.status_code}: {r.text[:200]}"


def enrich_section(provider: str, model: str, base_url: str, key: str,
                   project_name: str, section_name: str,
                   current_content: str, project_type: str) -> str:
    """
    Llama a la IA para enriquecer el contenido de una seccion.
    Devuelve texto enriquecido o lanza excepcion.
    """
    prompt = (
        f"Eres un Technical Writer Senior y Arquitecto de Software experto en documentacion "
        f"estandarizada. Enriquece la seccion '{section_name}' de la documentacion del proyecto "
        f"'{project_name}' (tipo: {project_type}).\n\n"
        f"ESTRUCTURA REQUERIDA (Super Prompt Maestro):\n"
        f"- Documentacion DUAL: Parte Funcional (no tecnica, para negocio/PM/Gerencia) "
        f"y Parte Tecnica (para devs/QA/arquitectos).\n"
        f"- Diagramas: usar sintaxis Mermaid (flowchart, sequenceDiagram, erDiagram, C4Context).\n"
        f"- Imagenes UI: marcar con placeholder "
        f"`> \U0001f5bc️ **[PLACEHOLDER IMAGEN:** Insertar aqui captura de {{Descripcion}} **]**`\n"
        f"- Tablas Markdown para datos estructurados.\n"
        f"- Glosarios, casos de uso, reglas de negocio cuando aplique.\n\n"
        f"Contenido actual a enriquecer:\n{current_content}\n\n"
        f"Instrucciones: Mantente fiel al contenido existente. Expande con detalles "
        f"tecnicos y ejemplos relevantes. Responde SOLO con el contenido Markdown enriquecido, "
        f"sin explicaciones ni texto fuera del documento."
    )

    if "OpenAI" in provider or "Ollama" in provider:
        return _call_openai_compat(model, base_url or "https://api.openai.com/v1", key, prompt)
    elif "Anthropic" in provider:
        return _call_anthropic(model, key, prompt)
    elif "Google" in provider or "Gemini" in provider:
        return _call_gemini(model, key, prompt)
    raise ValueError(f"Proveedor no soportado: {provider}")


def _call_openai_compat(model: str, base_url: str, key: str, prompt: str) -> str:
    import requests
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def _call_anthropic(model: str, key: str, prompt: str) -> str:
    import requests
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key":         key,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
    }
    payload = {
        "model": model or "claude-3-5-haiku-20241022",
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}],
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["content"][0]["text"]


def _call_gemini(model: str, key: str, prompt: str) -> str:
    import requests
    m = model or "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
