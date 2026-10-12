#!/usr/bin/env python3
"""Erzeugt den providers-Block der promptfooconfig.yaml aus ollama list.

Verwendung:
    python3 generate_promptfoo_config.py [--output DATEI] [--keep-alive WERT] [--dry-run]
"""

import argparse
import subprocess
import sys
from pathlib import Path

DEFAULT_OUTPUT = "promptfooconfig.yaml"
DEFAULT_PROMPT = "prompts/software-engineer.txt"


def ollama_models():
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "unbekannter Fehler")
    models = []
    header = True
    for line in result.stdout.splitlines():
        tokens = line.split()
        if not tokens:
            continue
        if tokens[0].upper() == "NAME":
            header = False
            continue
        models.append(tokens[0])
    return models


def select_checkbox(models):
    from simple_term_menu import TerminalMenu

    menu = TerminalMenu(
        models,
        multi_select=True,
        show_multi_select_hint=True,
        title="Modelle wählen (Pfeiltasten, Leertaste = auswählen, Enter = OK, q = Abbruch):",
    )
    indices = menu.show()
    if not indices:
        return None
    return [models[i] for i in indices]


def select_numbered(models):
    print("Verfügbare Modelle:")
    for i, model in enumerate(models, 1):
        print(f"  {i:>2}. {model}")
    while True:
        raw = input("Auswahl (z. B. 1,3-5, leer = Abbruch): ").strip()
        if not raw:
            return None
        indices = set()
        valid = True
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                start, _, finish = part.partition("-")
                try:
                    start, finish = int(start), int(finish)
                    if start < 1 or finish > len(models) or start > finish:
                        valid = False
                        break
                    indices.update(range(start, finish + 1))
                except ValueError:
                    valid = False
                    break
            else:
                try:
                    n = int(part)
                    if not 1 <= n <= len(models):
                        valid = False
                        break
                    indices.add(n)
                except ValueError:
                    valid = False
                    break
        if valid and indices:
            return [models[i - 1] for i in sorted(indices)]
        print("  Ungültige Eingabe, bitte erneut versuchen.")


def select_models(models):
    try:
        selected = select_checkbox(models)
    except ImportError:
        selected = select_numbered(models)
    return selected


def confirm(models):
    print("\nAusgewählte Modelle:")
    for model in models:
        print(f"  - {model}")
    answer = input("\nÜbernehmen? [j/N]: ").strip().lower()
    return answer in ("j", "ja", "y", "yes")


def provider_block(models, keep_alive):
    parts = ["providers:"]
    for model in models:
        parts.append(f"  - id: ollama:chat:{model}")
        parts.append(f"    label: {model}")
        parts.append("    config:")
        parts.append(f'      keep_alive: "{keep_alive}"')
    parts.append("")
    return "\n".join(parts) + "\n"


def replace_providers(text, block):
    lines = text.splitlines(keepends=True)
    prov = None
    for i, line in enumerate(lines):
        if line.rstrip("\r\n") == "providers:":
            prov = i
            break
    if prov is None:
        insert = len(lines)
        for i, line in enumerate(lines):
            stripped = line.rstrip("\r\n")
            if stripped and not stripped[0].isspace():
                insert = i
                break
        lines.insert(insert, block)
        return "".join(lines)
    end = len(lines)
    for j in range(prov + 1, len(lines)):
        stripped = lines[j].rstrip("\r\n")
        if stripped and not stripped[0].isspace() and ":" in stripped:
            end = j
            break
    return "".join(lines[:prov] + [block] + lines[end:])


def fresh_config(models, keep_alive):
    parts = [
        "description: Lokaler Ollama Benchmark für Java Spring Boot, React und Fullstack Aufgaben",
        "",
        provider_block(models, keep_alive).rstrip("\n"),
        "",
    ]
    if Path(DEFAULT_PROMPT).exists():
        parts.append("prompts:")
        parts.append(f"  - file://{DEFAULT_PROMPT}")
        parts.append("")
    return "\n".join(parts)


def write_safely(path, text):
    if path.exists():
        backup = path.with_suffix(path.suffix + ".bak")
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Backup: {backup}")
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Erzeugt den providers-Block der promptfooconfig.yaml aus ollama list."
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Zieldatei (Default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--keep-alive",
        default="0s",
        help='keep_alive-Wert für Ollama (Default: "0s")',
    )
    parser.add_argument("--dry-run", action="store_true", help="Nur Vorschau, nichts schreiben")
    args = parser.parse_args()

    try:
        models = ollama_models()
    except RuntimeError as exc:
        print(f"Fehler beim Aufruf von 'ollama list': {exc}", file=sys.stderr)
        print("Stelle sicher, dass Ollama installiert und gestartet ist.", file=sys.stderr)
        sys.exit(1)

    if not models:
        print(
            "Keine Modelle gefunden. Lade zuerst eines herunter, z. B. 'ollama pull <modell>'.",
            file=sys.stderr,
        )
        sys.exit(1)

    selected = select_models(models)
    if not selected:
        print("Keine Modelle ausgewählt – Abbruch.")
        sys.exit(0)

    if not confirm(selected):
        print("Abgebrochen.")
        sys.exit(0)

    block = provider_block(selected, args.keep_alive)
    output = Path(args.output)

    if output.exists():
        new_text = replace_providers(output.read_text(encoding="utf-8"), block)
    else:
        new_text = fresh_config(selected, args.keep_alive)

    if args.dry_run:
        print("\nVorschau (dry-run):")
        print("-" * 40)
        print(new_text, end="")
        return

    write_safely(output, new_text)
    print(f"Geschrieben: {output}")


if __name__ == "__main__":
    main()