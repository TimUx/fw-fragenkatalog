# FFW Willingshausen – Fragenkatalog Hessen

Ein interaktives Quiz-System zur Vorbereitung auf die Leistungsübungen der Feuerwehr Hessen. Diese Anwendung ermöglicht es Feuerwehrleuten, ihr Wissen in verschiedenen Themenbereichen zu testen und zu festigen.

## 🚒 Über das Projekt

Dieses Projekt wurde entwickelt, um Feuerwehrangehörige bei der Vorbereitung auf Leistungsprüfungen zu unterstützen. Die Anwendung bietet eine benutzerfreundliche Oberfläche zum Lernen und Üben von Fragen aus dem offiziellen Fragenkatalog der Feuerwehr Hessen.

## ✨ Features

- **Kapiteltraining**: Wählen Sie spezifische Themengebiete aus, um gezielt zu üben (mit Fragenanzahl)
- **Prüfungsmodus**: Simulieren Sie eine echte Prüfung mit 30 zufälligen Fragen
- **Sofortiges Feedback**: Erhalten Sie direkt nach jeder Antwort eine Rückmeldung
- **Responsives Design**: Funktioniert auf Desktop, Tablet und Smartphone
- **Progressive Web App (PWA)**: Installierbar auf Startbildschirm, funktioniert offline
- **Bildunterstützung**: Fragen können mit Piktogrammen oder Bildern versehen werden

## 🛠️ Technologie-Stack

- **HTML5**: Struktur der Webanwendung
- **CSS3**: Styling mit modernem, responsivem Design
- **JavaScript (Vanilla)**: Logik und Interaktivität
- **JSON**: Datenspeicherung für Fragen und Antworten
- **PWA**: Service Worker für Offline-Funktionalität und Installierbarkeit

## 📁 Projektstruktur

```
fw-fragenkatalog/
├── index.html          # Haupt-HTML-Datei
├── app.js              # JavaScript-Logik
├── manifest.json       # PWA Manifest
├── sw.js               # Service Worker für Offline-Funktionalität
├── style.css           # Styling
├── assets/
│   └── wappen.png      # Logo der FFW Willingshausen
├── data/
│   └── questions.json  # Fragenkatalog
└── README.md           # Diese Datei
```

## 🚀 Verwendung

### Lokale Verwendung

1. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/TimUx/fw-fragenkatalog.git
   cd fw-fragenkatalog
   ```

2. Öffnen Sie die `index.html` Datei in einem modernen Webbrowser:
   ```bash
   open index.html
   # oder
   firefox index.html
   # oder
   google-chrome index.html
   ```

3. Wählen Sie einen Modus:
   - **Kapiteltraining**: Üben Sie gezielt einzelne Themen
   - **Prüfungsmodus**: Testen Sie Ihr Wissen mit 30 zufälligen Fragen

### Web-Server

Für optimale Funktionalität empfiehlt sich die Verwendung eines lokalen Webservers:

```bash
# Mit Python
python -m http.server 8000

# Mit Node.js (http-server)
npx http-server

# Mit PHP
php -S localhost:8000
```

Öffnen Sie dann `http://localhost:8000` in Ihrem Browser.

## 📝 Fragen hinzufügen oder bearbeiten

Die Fragen werden in der Datei `data/questions.json` gespeichert. Das Format ist wie folgt:

```json
{
  "Kapitelname": [
    {
      "question": "Ihre Frage hier?",
      "answers": [
        "Antwort 1",
        "Antwort 2",
        "Antwort 3"
      ],
      "correctIndex": 0,
      "image": "assets/bild.png"
    }
  ]
}
```

### Feldbeschreibung:
- **question**: Der Fragetext
- **answers**: Array mit allen Antwortmöglichkeiten
- **correctIndex**: Index der korrekten Antwort (0 = erste Antwort, 1 = zweite, etc.)
- **image**: (Optional) Pfad zu einem Bild oder Piktogramm

### Beispiel:

```json
{
  "ABC-Gefahrstoffe": [
    {
      "question": "Wie nennt man die Aufnahme von Gefahrstoffen in den Körper?",
      "answers": [
        "Inkorporation",
        "Inkontinenz",
        "Kontamination"
      ],
      "correctIndex": 0
    }
  ],
  "Atemschutz": [
    {
      "question": "Welche Atemschutzgeräte sind umluftunabhängig?",
      "answers": [
        "Behältergeräte",
        "Brandfluchthauben",
        "Filtergeräte"
      ],
      "correctIndex": 0
    }
  ]
}
```

## 🌐 Deployment

### GitHub Pages

1. Pushen Sie Ihre Änderungen zu GitHub
2. Gehen Sie zu den Repository-Einstellungen
3. Navigieren Sie zu "Pages"
4. Wählen Sie den `main` Branch als Quelle
5. Die Seite wird unter `https://username.github.io/fw-fragenkatalog/` verfügbar sein

### Andere Hosting-Optionen

Da es sich um eine statische Website handelt, kann sie auf jedem Webserver oder Hosting-Service bereitgestellt werden:
- Netlify
- Vercel
- AWS S3
- Firebase Hosting

## 📱 Progressive Web App (PWA)

Diese Anwendung ist als Progressive Web App (PWA) konzipiert und bietet folgende Vorteile:

### Installation

**Auf Mobilgeräten (iOS/Android):**
1. Öffnen Sie die App im Browser
2. Wählen Sie "Zum Startbildschirm hinzufügen" (iOS) oder "App installieren" (Android)
3. Die App wird wie eine native App auf Ihrem Gerät installiert

**Auf Desktop (Chrome/Edge):**
1. Klicken Sie auf das Install-Symbol in der Adressleiste
2. Bestätigen Sie die Installation
3. Die App wird als eigenständige Anwendung installiert

### Offline-Funktionalität

- **Service Worker**: Cachet alle notwendigen Dateien automatisch
- **Offline-Nutzung**: Die App funktioniert vollständig offline nach dem ersten Laden
- **Schneller Start**: Gecachte Dateien werden sofort geladen

### PWA-Dateien

- `manifest.json`: Definiert App-Metadaten, Icons und Verhalten
- `sw.js`: Service Worker für Caching und Offline-Funktionalität
- `assets/icons/`: App-Icons in verschiedenen Größen (72x72 bis 512x512)

## 🎨 Anpassungen

### Farben ändern

Die Hauptfarben können in der `style.css` Datei angepasst werden:

```css
header {
    background: #b30000;  /* Rot der Feuerwehr */
}
body {
    background: #101820;  /* Dunkler Hintergrund */
}
```

### Logo austauschen

Ersetzen Sie die Datei `assets/wappen.png` mit Ihrem eigenen Logo.

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die LICENSE-Datei für Details (falls vorhanden).

## 🤝 Beitragen

Beiträge sind willkommen! Bitte öffnen Sie ein Issue oder einen Pull Request für Verbesserungen oder neue Features.

## 👨‍🚒 Credits

Entwickelt für die Freiwillige Feuerwehr Willingshausen.

Basierend auf dem Fragenkatalog der Feuerwehr Hessen für Leistungsübungen.

## 📧 Kontakt

Bei Fragen oder Anregungen öffnen Sie bitte ein Issue im Repository.
