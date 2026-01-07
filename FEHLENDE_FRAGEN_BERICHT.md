# Detaillierter Bericht: Fehlende/Falsche Fragen

**Stand:** 2026-01-07 nach Verbesserung des Extraktionsskripts

## Zusammenfassung

- **Gesamt fehlende Fragen:** 30
- **Gesamt extra Fragen:** 1  
- **Netto-Differenz:** 29 Fragen
- **Kapitel mit Problemen:** 16 von 24

## Status nach Verbesserung des Extraktionsskripts

Das Extraktionsskript wurde verbessert und hat automatisch **22 zusätzliche Fragen** extrahiert:
- **Vorher:** 648/699 Fragen (93%)
- **Nachher:** 670/699 Fragen (96%)

Die verbleibenden 29 Fragen haben komplexe PDF-Formatierungen und benötigen manuelle Überprüfung.

---

## 🔴 PRIORITÄT HOCH (10 fehlende Fragen)

### Brennen
- **Erwartet:** 79 Fragen
- **Gefunden:** 74 Fragen  
- **Fehlen:** 5 Fragen
- **PDF-Seiten:** 21-33
- **Aktion:** PDF-Seiten 21-33 manuell durchgehen und 5 fehlende Fragen identifizieren

### Lebensrettende Sofortmaßnahmen (Erste Hilfe)
- **Erwartet:** 24 Fragen
- **Gefunden:** 19 Fragen
- **Fehlen:** 5 Fragen  
- **PDF-Seiten:** 53-57
- **Aktion:** PDF-Seiten 53-57 manuell durchgehen und 5 fehlende Fragen identifizieren

---

## 🟡 PRIORITÄT MITTEL (12 fehlende Fragen)

### Gerätekunde: Rettungsgeräte
- **Erwartet:** 44 | **Gefunden:** 41 | **Fehlen:** 3
- **PDF-Seiten:** 109-116

### Gerätekunde: Löschgeräte, Schläuche, Armaturen
- **Erwartet:** 58 | **Gefunden:** 56 | **Fehlen:** 2
- **PDF-Seiten:** 85-94

### Sprechfunk
- **Erwartet:** 12 | **Gefunden:** 10 | **Fehlen:** 2
- **PDF-Seiten:** 119-121

### Technische Hilfeleistung
- **Erwartet:** 16 | **Gefunden:** 14 | **Fehlen:** 2
- **PDF-Seiten:** 122-124

### Verhalten bei Gefahren
- **Erwartet:** 22 | **Gefunden:** 20 | **Fehlen:** 2
- **PDF-Seiten:** 131-134

### Wald- und Vegetationsbrandbekämpfung
- **Erwartet:** 12 | **Gefunden:** 10 | **Fehlen:** 2
- **PDF-Seiten:** 138-140

---

## 🟢 PRIORITÄT NIEDRIG (8 fehlende Fragen)

Folgende Kapitel fehlt jeweils **1 Frage:**

| Kapitel | Erwartet | Gefunden | PDF-Seiten |
|---------|----------|----------|------------|
| Atemschutz | 33 | 32 | 9-14 |
| Brandsicherheitsdienst | 7 | 6 | 19 |
| Löschen | 70 | 69 | 73-84 |
| Rechtsgrundlagen | 24 | 23 | 101-105 |
| Rettung und Absturzsicherung | 13 | 12 | 106-108 |
| Unfallverhütungsvorschriften/Unfallversicherung | 29 | 28 | 125-130 |
| Wasserförderung | 10 | 9 | 136-137 |

---

## ⚠️ ZU ÜBERPRÜFEN (1 extra Frage)

### Gerätekunde: Persönliche Ausrüstung
- **Erwartet:** 12 Fragen
- **Gefunden:** 13 Fragen
- **Extra:** 1 Frage
- **PDF-Seiten:** 96-98
- **Aktion:** JSON-Datei überprüfen, ob eine Frage doppelt ist oder nicht zum Kapitel gehört

---

## Mögliche Ursachen für fehlende Fragen

Die verbleibenden Fragen konnten nicht automatisch extrahiert werden aufgrund von:

1. **Fehlende/unklare 'x' Markierung** - Die korrekte Antwort ist nicht klar als 'x' markiert
2. **Mehrzeilige Fragen** - Frage erstreckt sich über mehrere Zeilen mit ungewöhnlichem Layout
3. **Seitenumbrüche** - Frage beginnt auf einer Seite und endet auf der nächsten
4. **Ungewöhnliche Formatierung** - Spezielle Zeichen, Einrückungen oder Abstände
5. **OCR-Artefakte** - Probleme bei der PDF-Texterkennung

---

## Empfohlene Vorgehensweise

### Manuelle Überprüfung:
1. PDF öffnen auf den angegebenen Seiten
2. Fragennummern 1, 2, 3, ... im PDF durchzählen
3. Entsprechende JSON-Datei öffnen und Fragennummern vergleichen
4. Fehlende Fragennummern identifizieren
5. Fehlende Fragen aus PDF manuell extrahieren und zur JSON hinzufügen

### Beispiel für Brennen (74/79):
```bash
# JSON-Datei öffnen
vim data/Brennen.json

# Im PDF durchzählen welche Fragen 1-79 fehlen
# Vermutlich sind es Fragen mit komplexer Formatierung
```

### Validierung:
Nach jeder Korrektur die Gesamtzahl überprüfen:
```bash
python3 -c "import json; print(len(json.load(open('data/Brennen.json'))['questions']))"
```

---

## Nächste Schritte

1. ✅ **Extraktionsskript verbessert** (Commit 209e484)
2. ⏳ **Manuelle Korrekturen für 29 verbleibende Fragen**
3. Priorisierung nach obiger Liste (HOCH → MITTEL → NIEDRIG)
4. Review der extra Frage in Persönliche Ausrüstung

---

**Hinweis:** Das verbesserte Extraktionsskript kann in Zukunft bei PDF-Updates wiederverwendet werden und wird 96% der Fragen automatisch korrekt extrahieren.
