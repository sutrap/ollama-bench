# Installation (Linux)

## Voraussetzungen

- [Node.js](https://nodejs.org) >= 18 (inkl. npm)
- [Ollama](https://ollama.com) installiert und gestartet
- Mindestens ein Modell heruntergeladen (`ollama pull <modell>`)

Kontrolle:

```bash
node --version
ollama list
```

## Schritt 1 – Abhängigkeiten installieren

Im Projektverzeichnis:

```bash
npm install
```

Installiert `promptfoo` als lokale Dev-Dependency (in `node_modules/`).

## Schritt 2 – promptfoo aufrufen (Wichtig unter Linux)

Promptfoo wird **nicht global** installiert. Unter Linux funktioniert der
Aufruf nur über `npx`:

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
- Eine globale Installation (`npm install -g promptfoo`) ist unter Linux
  fehleranfällig und wird nicht unterstützt.

## Schritt 3 – Optional: Modell-Generator

Der Generator zeigt eine Checkbox-Auswahl aller per `ollama list` verfügbaren
Modelle. Für die TUI wird eine kleine Python-Bibliothek empfohlen:

```bash
pip install simple-term-menu
```

Ohne diese Bibliothek fällt das Skript auf eine einfache nummerierte
Mehrfachauswahl zurück.

## Schritt 4 – Config erzeugen

```bash
python3 generate_promptfoo_config.py
```

oder über npm:

```bash
npm run generate
```

Es werden nur die ausgewählten Modelle in den `providers`-Block der
`promptfooconfig.yaml` geschrieben. Vor dem Überschreiben wird automatisch
ein Backup als `promptfooconfig.yaml.bak` angelegt.

## Schritt 5 – Benchmark starten

```bash
npm run eval
```

oder explizit:

```bash
npx promptfoo eval --max-concurrency 1
```

Die Ergebnisse landen standardmäßig in `./results/`.

## Schritt 6 – Ergebnisse ansehen

```bash
npm run view
```

öffnet die interaktive Ergebnisansicht im Browser (`npx promptfoo view`).

## Cache zurücksetzen (bei Bedarf)

```bash
npm run clear
```