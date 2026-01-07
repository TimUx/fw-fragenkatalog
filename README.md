# FW Willingshausen – Fragenkatalog Hessen

Ein interaktives Quiz-System zur Vorbereitung auf die Leistungsübungen der Feuerwehr Hessen. Diese Anwendung ermöglicht es Feuerwehrleuten, ihr Wissen in verschiedenen Themenbereichen zu testen und zu festigen.

## 📑 Inhaltsverzeichnis

- [🚒 Über das Projekt](#-über-das-projekt)
- [🌐 Live-App nutzen](#-live-app-nutzen)
- [✨ Features](#-features)
- [📸 Screenshots](#-screenshots)
- [🚀 First Steps – Loslegen](#-first-steps--loslegen)
- [🛠️ Technologie-Stack](#️-technologie-stack)
- [📁 Projektstruktur](#-projektstruktur)
- [🚀 Lokale Verwendung](#-lokale-verwendung)
- [📝 Fragen hinzufügen oder bearbeiten](#-fragen-hinzufügen-oder-bearbeiten)
- [📱 Progressive Web App (PWA)](#-progressive-web-app-pwa)
- [🌐 Deployment](#-deployment)
- [📊 Datenstand](#-datenstand)
- [🔗 Links](#-links)

## 🚒 Über das Projekt

Dieses Projekt wurde entwickelt, um Feuerwehrangehörige der Feuerwehr Willingshausen bei der Vorbereitung auf Leistungsprüfungen zu unterstützen. Die Anwendung bietet eine benutzerfreundliche Oberfläche zum Lernen und Üben von Fragen aus dem offiziellen Fragenkatalog der Feuerwehr Hessen.

## 🌐 Live-App nutzen

Die App ist **kostenlos und ohne Installation** online verfügbar:

**🔗 https://fragenkatalog.feuerwehr-willingshausen.de**

Alternativ auch erreichbar unter: [https://timux.github.io/fw-fragenkatalog/](https://timux.github.io/fw-fragenkatalog/)

## ✨ Features

- **Kapiteltraining**: Wählen Sie spezifische Themengebiete aus, um gezielt zu üben
- **Prüfungsmodus**: Simulieren Sie eine echte Prüfung mit 30 zufälligen Fragen
- **Kapitel nachlesen**: Schauen Sie sich alle Fragen und korrekten Antworten eines Kapitels in Ruhe an
- **Sofortiges Feedback**: Erhalten Sie direkt nach jeder Antwort eine Rückmeldung
- **Detaillierte Auswertung**: Am Ende sehen Sie alle falsch beantworteten Fragen mit den richtigen Antworten
- **Responsives Design**: Funktioniert auf Desktop, Tablet und Smartphone
- **Progressive Web App (PWA)**: Installierbar auf Startbildschirm, funktioniert offline
- **Umfangreicher Fragenkatalog**: Über 699 Fragen aus 24 Kapiteln des offiziellen Katalogs der Feuerwehr Hessen

## 📸 Screenshots

### Startseite mit Willkommensbereich
![Startseite](https://github.com/user-attachments/assets/2f139859-6464-4788-8196-8de1a010905b)

### Kapitelauswahl
![Kapitelauswahl](https://github.com/user-attachments/assets/e0116a6f-97b1-4ddf-81c3-30b86a2fbf7a)

## 🚀 First Steps – Loslegen

1. **Öffnen Sie die App:** Besuchen Sie [https://fragenkatalog.feuerwehr-willingshausen.de](https://fragenkatalog.feuerwehr-willingshausen.de)

2. **Wählen Sie einen Modus:**
   - **Kapiteltraining**: Ideal zum gezielten Üben einzelner Themen
   - **Prüfungsmodus**: 30 zufällige Fragen zur Prüfungssimulation
   - **Kapitel nachlesen**: Alle Fragen mit Antworten zum Durchlesen

3. **Optional – Als App installieren:**
   - **Auf Mobilgeräten:** Tippen Sie auf "Zum Startbildschirm hinzufügen"
   - **Auf Desktop:** Klicken Sie auf das Install-Symbol in der Adressleiste
   - Vorteil: Offline-Nutzung und schneller Zugriff

4. **Loslegen und lernen!** 🎓

## 🛠️ Technologie-Stack

- **HTML5**: Struktur der Webanwendung
- **CSS3**: Styling mit modernem, responsivem Design
- **JavaScript (Vanilla)**: Logik und Interaktivität ohne externe Frameworks
- **JSON**: Datenspeicherung für Fragen und Antworten
- **PWA**: Service Worker für Offline-Funktionalität und Installierbarkeit

## 📁 Projektstruktur

```
fw-fragenkatalog/
├── index.html          # Haupt-HTML-Datei mit Willkommensseite
├── editor.html         # GUI-Editor zum Bearbeiten von Fragen
├── app.js              # JavaScript-Logik für die Quiz-Anwendung
├── style.css           # Styling für alle Komponenten
├── manifest.json       # PWA Manifest
├── sw.js               # Service Worker für Offline-Funktionalität
├── assets/
│   ├── wappen.png      # Logo der FW Willingshausen
│   └── icons/          # PWA-Icons in verschiedenen Größen
├── data/
│   ├── meta.json       # Liste aller verfügbaren Kapitel
│   └── *.json          # Fragenkataloge für jedes Kapitel (24 Kapitel)
└── README.md           # Diese Datei
```

## 🚀 Lokale Verwendung

Falls Sie die Anwendung lokal ausführen möchten:

1. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/TimUx/fw-fragenkatalog.git
   cd fw-fragenkatalog
   ```

2. Starten Sie einen lokalen Webserver:
   ```bash
   # Mit Python 3
   python3 -m http.server 8000
   
   # Mit Node.js (http-server)
   npx http-server
   
   # Mit PHP
   php -S localhost:8000
   ```

3. Öffnen Sie `http://localhost:8000` in Ihrem Browser

## 📝 Fragen hinzufügen oder bearbeiten

### 🖥️ GUI-Editor (Empfohlen)

Verwenden Sie den benutzerfreundlichen **Fragen-Editor** für einfaches Bearbeiten:

1. Starten Sie einen lokalen Webserver:
   ```bash
   python3 -m http.server 8000
   ```

2. Öffnen Sie den Editor im Browser:
   ```
   http://localhost:8000/editor.html
   ```

3. **Funktionen:**
   - Kapitel aus Dropdown auswählen
   - Fragen direkt im Browser bearbeiten
   - Richtige Antwort mit Radio-Button markieren
   - Neue Fragen hinzufügen
   - Fragen löschen
   - Als JSON exportieren

### 📄 Manuelles Bearbeiten

Die Fragen werden in einzelnen JSON-Dateien im `data/` Verzeichnis gespeichert. Das Format ist wie folgt:

```json
{
  "questions": [
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

**Feldbeschreibung:**
- **question**: Der Fragetext
- **answers**: Array mit allen Antwortmöglichkeiten (meist 3)
- **correctIndex**: Index der korrekten Antwort (0 = erste Antwort, 1 = zweite, etc.)
- **image**: (Optional) Pfad zu einem Bild oder Piktogramm

### Beispiel:

```json
{
  "questions": [
    {
      "question": "Wie nennt man die Aufnahme von Gefahrstoffen in den Körper?",
      "answers": [
        "Inkorporation",
        "Inkontinenz",
        "Kontamination"
      ],
      "correctIndex": 0
    },
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

- **Service Worker**: Cached alle notwendigen Dateien automatisch
- **Offline-Nutzung**: Die App funktioniert vollständig offline nach dem ersten Laden
- **Schneller Start**: Gecachte Dateien werden sofort geladen

## 🌐 Deployment

### GitHub Pages (Aktuell aktiv)

Die Seite ist unter `https://timux.github.io/fw-fragenkatalog/` verfügbar.

Bei Änderungen:
1. Pushen Sie Ihre Änderungen zum `main` Branch
2. GitHub Pages aktualisiert die Seite automatisch

### Andere Hosting-Optionen

Da es sich um eine statische Website handelt, kann sie auf jedem Webserver oder Hosting-Service bereitgestellt werden:
- Netlify
- Vercel
- AWS S3
- Firebase Hosting

## 📊 Datenstand

**Aktueller Stand:** Januar 2026

- **24 Kapitel** vollständig implementiert
- **699 Fragen** aus dem offiziellen Fragenkatalog
- **96% Abdeckung** des offiziellen Fragenkatalogs Hessen

Die Fragen wurden automatisch aus dem offiziellen PDF-Fragenkatalog der Feuerwehr Hessen (Version 01/26) extrahiert.

## 🎨 Anpassungen

### Farben ändern

Die Hauptfarben können in der `style.css` Datei angepasst werden:

```css
header {
    background: #2c3e50;  /* Header-Farbe */
}
body {
    background: #f5f5f5;  /* Hintergrundfarbe */
}
```

### Logo austauschen

Ersetzen Sie die Datei `assets/wappen.png` mit Ihrem eigenen Logo.

## 🔗 Links

- **Homepage**: [https://www.feuerwehr-willingshausen.de](https://www.feuerwehr-willingshausen.de)
- **Facebook**: [https://www.facebook.com/ffw.willingshausen](https://www.facebook.com/ffw.willingshausen)
- **Instagram**: [https://www.instagram.com/ffw.willingshausen](https://www.instagram.com/ffw.willingshausen)
- **WhatsApp Channel**: [https://whatsapp.com/channel/0029VaaGvZI17EmqYdx03Z2V](https://whatsapp.com/channel/0029VaaGvZI17EmqYdx03Z2V)

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## 🤝 Beitragen

Beiträge sind willkommen! Bitte öffnen Sie ein Issue oder einen Pull Request für Verbesserungen oder neue Features.

## 👨‍🚒 Credits

Entwickelt für die Freiwillige Feuerwehr Willingshausen.

Basierend auf dem offiziellen Fragenkatalog der Feuerwehr Hessen für Leistungsübungen (Version 01/26).

## 📧 Kontakt

Bei Fragen oder Anregungen öffnen Sie bitte ein Issue im Repository oder kontaktieren Sie uns über unsere Social-Media-Kanäle.
