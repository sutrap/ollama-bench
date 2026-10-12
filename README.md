# 🦙 Ollama Promptfoo Benchmark

![promptfoo](https://img.shields.io/badge/promptfoo-0.124.1-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![platform](https://img.shields.io/badge/platform-linux-lightgrey)

Lokaler Benchmark für Ollama-Modelle — komplett **lokal**, ohne Cloud-Kosten
und ohne API-Keys. Fokus: Java Spring Boot, React, TypeScript und Fullstack.

## ✨ Features

- 🆓 100 % lokal (Ollama + promptfoo), keine Cloud-Kosten, keine API-Keys
- 🧠 Modell-Auswahl per Checkbox direkt aus `ollama list`
- 🧪 8 codierte Benchmarks: Spring CRUD/Validation/Exceptions/Tests, React Form/Hook/Bugfix, Fullstack-Flow
- 📊 Ergebnisse als JSON/CSV exportierbar, Auswertung im Browser

## 📦 Voraussetzungen

- Node.js ≥ 18 (inkl. npm)
- Ollama installiert und gestartet
- Mindestens ein Modell heruntergeladen

## 🚀 Schnellstart

```bash
ollama list            # 1. Ollama-Kontrolle
npm install            # 2. Abhängigkeiten
npm run generate       # 3. Modelle auswählen (Checkbox)
npm run eval           # 4. Benchmark starten
npm run view           # 5. Ergebnisse ansehen
```

> **Linux-Hinweis:** promptfoo ist nur als lokale Dev-Dependency installiert.
> Direkt auf der Kommandozeile lautet der Aufruf immer `npx promptfoo ...`
> (z. B. `npx promptfoo --version`). Bitte niemals global installieren —
> Details in [INSTALL.md](INSTALL.md).

## 🧰 Verwendung

| Aufgabe | Befehl |
| --- | --- |
| Config erzeugen | `npm run generate` |
| Benchmark ausführen | `npm run eval` |
| Ergebnis als JSON | `npm run eval:json` → `results/benchmark.json` |
| Ergebnis als CSV | `npm run eval:csv` → `results/benchmark.csv` |
| Ergebnisse ansehen | `npm run view` |
| Cache zurücksetzen | `npm run clear` |

Alle Skripte sind in [`package.json`](package.json) definiert und nutzen
`--max-concurrency 1`, damit sich die Modelle lokal nicht gegenseitig
verlangsamen.

## 🛠️ Modell-Auswahl generieren

Das Python-Skript [`generate_promptfoo_config.py`](generate_promptfoo_config.py)
liest alle Modelle aus `ollama list`, zeigt sie zur Mehrfachauswahl an und
schreibt nur die ausgewählten Modelle in den `providers`-Block der
`promptfooconfig.yaml`. `prompts` und `tests` bleiben dabei unverändert,
vor dem Überschreiben wird eine Sicherung `promptfooconfig.yaml.bak` angelegt.

```bash
python3 generate_promptfoo_config.py [--output DATEI] [--keep-alive WERT] [--dry-run]
```

Für die Checkbox-Auswahl wird `simple-term-menu` empfohlen
(`pip install simple-term-menu`); ohne die Bibliothek fällt das Skript auf eine
nummerierte Mehrfachauswahl zurück.

## 💻 Installation

Schritt-für-Schritt-Anleitung für Linux (inkl. der `npx`-Besonderheit) in
[INSTALL.md](INSTALL.md).

## 📁 Projektstruktur

```
benchmarking/
├── INSTALL.md                   # Schritt-für-Schritt-Installation (Linux)
├── README.md                    # diese Datei
├── package.json                 # npm-Skripte + Dev-Dependency promptfoo
├── promptfooconfig.yaml         # Benchmark-Config (providers, prompts, tests)
├── generate_promptfoo_config.py # erzeugt providers-Block aus ollama list
├── prompts/
│   └── software-engineer.txt    # System-Prompt mit {{task}}-Variable
└── results/                     # Evaluationsergebnisse
```

## 📄 Lizenz

[MIT](LICENSE) — Copyright (c) 2026 sutrap