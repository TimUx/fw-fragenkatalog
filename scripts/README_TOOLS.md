# Werkzeuge für die Fragenverwaltung

Dieses Verzeichnis enthält mehrere Skripte zur Verwaltung und Pflege des Fragenkatalogs.

## 📋 Verfügbare Werkzeuge

### 1. `analyze_missing_questions.py`
**Zweck:** Analysiert fehlende und zusätzliche Fragen in jedem Kapitel.

**Verwendung:**
```bash
python3 scripts/analyze_missing_questions.py
```

**Ausgabe:**
- Detaillierte Liste der Kapitel mit Problemen
- Anzahl fehlender/zusätzlicher Fragen pro Kapitel
- Priorisierung nach Schweregrad
- Gesamtstatistik

**Beispielausgabe:**
```
Kapitel: Brennen
  Erwartet:   79 Fragen
  Gefunden:   74 Fragen
  Status:     🔴 FEHLEN 5 FRAGEN
```

---

### 2. `fill_missing_questions.py`
**Zweck:** Füllt fehlende Fragen mit Platzhaltern auf.

**Verwendung:**
```bash
# Vorschau (keine Änderungen)
python3 scripts/fill_missing_questions.py --dry-run

# Tatsächliche Ausführung
python3 scripts/fill_missing_questions.py
```

**Was es tut:**
- Fügt Platzhalter-Fragen für alle fehlenden Fragen hinzu
- Markiert Platzhalter deutlich mit `[PLATZHALTER]`
- Speichert aktualisierte JSON-Dateien

**Platzhalter-Format:**
```json
{
  "question": "[PLATZHALTER] Frage 75 im Kapitel Brennen - Diese Frage muss noch aus dem PDF übernommen werden.",
  "answers": [
    "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort A)",
    "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort B)",
    "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort C)"
  ],
  "correctIndex": 0,
  "placeholder": true,
  "note": "Diese Frage wurde automatisch als Platzhalter erstellt und muss manuell korrigiert werden."
}
```

---

### 3. `extract_pdf_questions.py`
**Zweck:** Extrahiert Fragen aus dem PDF-Antwortkatalog.

**Verwendung:**
```bash
python3 scripts/extract_pdf_questions.py
```

**Voraussetzungen:**
```bash
pip install pdfplumber Pillow
```

**Was es tut:**
- Liest `data/antwortkatalog-hflue-01.26.pdf`
- Extrahiert Fragen, Antworten und Bilder
- Erstellt JSON-Dateien für jedes Kapitel
- Aktualisiert `data/meta.json`

---

## 🖥️ GUI-Editor (`editor.html`)

**Zweck:** Benutzerfreundliche Oberfläche zum Bearbeiten von Fragen.

**Verwendung:**
1. Starten Sie einen lokalen Webserver:
   ```bash
   python3 -m http.server 8000
   ```
2. Öffnen Sie im Browser: `http://localhost:8000/editor.html`

**Funktionen:**
- ✅ Kapitel aus Dropdown auswählen
- ✅ Fragen direkt im Browser bearbeiten
- ✅ Richtige Antwort mit Radio-Button markieren
- ✅ Platzhalter-Fragen sind gelb markiert
- ✅ Neue Fragen hinzufügen
- ✅ Fragen löschen
- ✅ Als JSON exportieren
- ✅ Statistiken anzeigen (Gesamt, Platzhalter, Vollständig)

**Workflow:**
1. Kapitel auswählen und laden
2. Fragen bearbeiten
3. Jede Frage einzeln speichern
4. Kapitel als JSON exportieren
5. JSON-Datei in `data/[Kapitelname].json` ersetzen

---

## ⚠️ Wichtiger Hinweis zur Fragenreihenfolge

**Problem:** Aufgrund der automatischen PDF-Extraktion können Fragennummern in den JSON-Dateien von den tatsächlichen Fragennummern im PDF abweichen.

**Beispiel:**
- PDF hat Fragen 1, 2, 3, 4, 5, 6, 7, ...
- Wenn Frage 5 nicht extrahiert wurde:
  - JSON enthält: 1, 2, 3, 4, 6 (als Frage 5), 7 (als Frage 6), ...
  - Die Nummerierung verschiebt sich ab der fehlenden Frage

**Lösung:**
1. Öffnen Sie das PDF auf den angegebenen Seiten
2. Zählen Sie die Fragen im PDF manuell durch (1, 2, 3, ...)
3. Vergleichen Sie mit den Fragen in der JSON-Datei
4. Identifizieren Sie fehlende Fragennummern
5. Fügen Sie fehlende Fragen an der richtigen Position ein

**Tipp:** Verwenden Sie den GUI-Editor, um Fragen einfach hinzuzufügen und neu zu ordnen.

---

## 📊 Workflow zur Vervollständigung

### Schritt 1: Analyse
```bash
python3 scripts/analyze_missing_questions.py
```
→ Zeigt, welche Kapitel Probleme haben

### Schritt 2: Platzhalter füllen
```bash
python3 scripts/fill_missing_questions.py
```
→ Fügt Platzhalter für fehlende Fragen hinzu

### Schritt 3: Manuelle Korrektur
1. Starten Sie den Editor: `python3 -m http.server 8000`
2. Öffnen Sie `http://localhost:8000/editor.html`
3. Für jedes Kapitel mit Platzhaltern:
   - Öffnen Sie das PDF auf den entsprechenden Seiten (siehe `FEHLENDE_FRAGEN_BERICHT.md`)
   - Suchen Sie die fehlenden Fragen im PDF
   - Ersetzen Sie die Platzhalter mit echten Fragen
   - Speichern und exportieren

### Schritt 4: Validierung
```bash
python3 scripts/analyze_missing_questions.py
```
→ Überprüfen Sie, dass alle Fragen vollständig sind

---

## 🔧 Tipps und Tricks

### JSON-Datei validieren
```bash
python3 -m json.tool data/Brennen.json > /dev/null
```
→ Prüft auf Syntaxfehler

### Anzahl der Fragen in einer Datei zählen
```bash
python3 -c "import json; print(len(json.load(open('data/Brennen.json'))['questions']))"
```

### Alle Platzhalter finden
```bash
grep -r "PLATZHALTER" data/*.json
```

### Kapitel mit den meisten Problemen finden
```bash
python3 scripts/analyze_missing_questions.py | grep "🔴 HOCH"
```

---

## 📝 Dateiformat

Jede JSON-Datei hat folgende Struktur:

```json
{
  "title": "Kapitelname",
  "questions": [
    {
      "question": "Fragetext?",
      "answers": [
        "Antwort 1",
        "Antwort 2",
        "Antwort 3"
      ],
      "correctIndex": 0,
      "image": "assets/piktos/bild.png"  // Optional
    }
  ]
}
```

**Platzhalter-Fragen** haben zusätzlich:
```json
{
  "placeholder": true,
  "note": "Diese Frage wurde automatisch erstellt..."
}
```

---

## 🆘 Hilfe und Support

Bei Fragen oder Problemen:
1. Überprüfen Sie die Skriptausgabe auf Fehlermeldungen
2. Validieren Sie JSON-Dateien auf Syntaxfehler
3. Öffnen Sie ein Issue im Repository
