"""
Transcriber — Formateo y exportacion de resultados Whisper.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path

APP_NAME_SHORT = "Transcriptor de Video Pro v1.0"


def _fmt_time(seconds: float) -> str:
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def _fmt_srt_time(seconds: float) -> str:
    ms = int((seconds % 1) * 1000)
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


class VideoTranscriber:

    def save_markdown(self, result: dict, source_file: Path,
                      output_dir: str, options: dict) -> str:
        segments       = result.get("segments", [])
        detected_lang  = result.get("language", "desconocido")
        model_name     = options.get("model", "base")
        use_timestamps = options.get("timestamps", True)
        use_paragraphs = options.get("paragraphs", True)

        stem     = source_file.stem
        out_path = Path(output_dir) / f"{stem}_transcripcion.md"

        duration = _fmt_time(segments[-1]["end"]) if segments else "00:00:00"
        now      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines: list[str] = []
        lines += [
            f"# Transcripcion: {source_file.name}",
            "",
            "| Campo | Valor |",
            "|-------|-------|",
            f"| **Archivo** | `{source_file.name}` |",
            f"| **Modelo Whisper** | `{model_name}` |",
            f"| **Idioma detectado** | `{detected_lang}` |",
            f"| **Duracion** | `{duration}` |",
            f"| **Segmentos** | `{len(segments)}` |",
            f"| **Fecha de transcripcion** | `{now}` |",
            "",
            "---",
            "",
            "## Contenido",
            "",
        ]

        if use_timestamps and segments:
            lines += self._format_with_timestamps(segments, use_paragraphs)
        else:
            full_text = result.get("text", "").strip()
            lines += self._format_plain(full_text, use_paragraphs)

        lines += [
            "",
            "---",
            f"*Generado con {APP_NAME_SHORT} | SONDA | {datetime.now().strftime('%Y-%m-%d')}*",
        ]

        out_path.write_text("\n".join(lines), encoding="utf-8")
        return str(out_path)

    def _format_with_timestamps(self, segments: list[dict],
                                 use_paragraphs: bool) -> list[str]:
        lines: list[str] = []
        para: list[str] = []

        for seg in segments:
            text = seg["text"].strip()
            if not text:
                continue
            ts   = _fmt_time(seg["start"])
            line = f"**[{ts}]** {text}"

            if use_paragraphs:
                para.append(line)
                if text[-1] in ".!?":
                    lines.append("  \n".join(para))
                    lines.append("")
                    para = []
            else:
                lines.append(line)

        if para:
            lines.append("  \n".join(para))
            lines.append("")

        return lines

    def _format_plain(self, full_text: str,
                       use_paragraphs: bool) -> list[str]:
        if not full_text:
            return ["*(sin contenido)*"]

        if not use_paragraphs:
            return [full_text]

        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        lines: list[str] = []
        chunk_size = 4
        for i in range(0, len(sentences), chunk_size):
            chunk = " ".join(sentences[i : i + chunk_size])
            lines.append(chunk)
            lines.append("")
        return lines

    def save_txt(self, result: dict, source_file: Path,
                  output_dir: str) -> str:
        out_path = Path(output_dir) / f"{source_file.stem}_transcripcion.txt"
        text = result.get("text", "").strip()
        out_path.write_text(text, encoding="utf-8")
        return str(out_path)

    def save_srt(self, result: dict, source_file: Path,
                  output_dir: str) -> str:
        out_path = Path(output_dir) / f"{source_file.stem}.srt"
        segments = result.get("segments", [])
        lines: list[str] = []
        for i, seg in enumerate(segments, 1):
            start = _fmt_srt_time(seg["start"])
            end   = _fmt_srt_time(seg["end"])
            text  = seg["text"].strip()
            lines += [str(i), f"{start} --> {end}", text, ""]
        out_path.write_text("\n".join(lines), encoding="utf-8")
        return str(out_path)
