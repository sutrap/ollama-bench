# Installation

Gilt für Linux und Windows. Plattformspezifische Unterschiede sind markiert.

## Voraussetzungen

- [Node.js](https://nodejs.org) >= 18 (inkl. npm)
- Python 3.9+ (für den Modell-Generator)
  - Windows: beim Installieren die Option **„Add python.exe to PATH“** aktivieren
- [Ollama](https://ollama.com) installiert und gestartet
- Mindestens ein Modell heruntergeladen (`ollama pull <modell>`)

Kontrolle:

```bash
node --version
ollama list
```

## Schritt 1 – Projekt herunterladen

```bash
git clone git@github.com:sutrap/ollama-bench.git
cd ollama-bench
```

## Schritt 2 – Abhängigkeiten installieren

```bash
npm install
```

Installiert `promptfoo` als lokale Dev-Dependency (in `node_modules/`).

## Schritt 3 – promptfoo aufrufen (Wichtig auf beiden Plattformen)

Promptfoo wird **nicht global** installiert. Der Aufruf funktioniert über
`npx`, auf **Linux und Windows gleichermaßen**:

```bash
npx promptfoo --version
```

`npx` nutzt dabei automatisch die lokal installierte Version aus
`node_modules/`.

Hinweise:

- Die npm-Skripte (`npm run eval`, `npm run view`, ...) funktionieren ohne
  `npx`, da npm das lokale `node_modules/.bin/` in den PATH legt.
- Nur direkt auf der Kommandozeile, außerhalb von npm-Skripten, immer die
  `npx`-Form verwenden: `npx promptfoo <befehl>`.
- Eine globale Installation (`npm install -g promptfoo`) ist fehleranfällig
  und wird nicht unterstützt.

## Schritt 4 – Optional: Modell-Generator

Der Generator zeigt eine Checkbox-Auswahl aller per `ollama list` verfügbaren
Modelle. Für die TUI wird eine kleine Python-Bibliothek empfohlen:

```bash
pip install simple-term-menu
```

Windows, falls `pip` direkt nicht gefunden wird:

```powershell
py -m pip install simple-term-menu
```

Ohne diese Bibliothek fällt das Skript auf eine einfache nummerierte
Mehrfachauswahl zurück.

## Schritt 5 – Config erzeugen

Am einfachsten (plattformübergreifend) über npm:

```bash
npm run generate
```

oder direkt per Python:

```bash
# Linux
python3 generate_promptfoo_config.py

# Windows
python generate_promptfoo_config.py
```

>`npm run generate` startet den Generator über einen Node-Wrapper, der
>automatisch den passenden Python-Launcher findet (`py`/`python`/`python3`).

Es werden nur die ausgewählten Modelle in den `providers`-Block der
`promptfooconfig.yaml` geschrieben. Vor dem Überschreiben wird automatisch
ein Backup als `promptfooconfig.yaml.bak` angelegt.

## Schritt 6 – Benchmark starten

```bash
npm run eval
```

oder explizit:

```bash
npx promptfoo eval --max-concurrency 1
```

Die Ergebnisse landen standardmäßig in `./results/`.

## Schritt 7 – Ergebnisse ansehen

```bash
npm run view
```

öffnet die interaktive Ergebnisansicht im Browser (`npx promptfoo view`).

## Cache zurücksetzen (bei Bedarf)

```bash
npm run clear
```

## Plattform-Hinweise

| | Linux | Windows |
| --- | --- | --- |
| Ollama installieren | `curl -fsSL https://ollama.com/install.sh \| sh` oder Paketmanager | Installer von [ollama.com](https://ollama.com) |
| Python-Aufruf | `python3` | `python` (oder `py -3`) |
| Shell | Bash | PowerShell / CMD (Befehle identisch) |