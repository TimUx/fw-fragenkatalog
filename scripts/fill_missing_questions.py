#!/usr/bin/env python3
"""
Fill missing questions with placeholder content.

This script adds placeholder questions for all missing question numbers
in each chapter, allowing the catalog to be complete while flagging
questions that need manual review.

Usage:
    python3 scripts/fill_missing_questions.py [--dry-run]
"""

import json
import os
import sys
from pathlib import Path

# Expected question counts per chapter (from PDF page 2 - official table)
# Total: 699 questions
EXPECTED_COUNTS = {
    "ABC-Gefahrstoffe": 31,
    "Atemschutz": 33,
    "Besondere-Gefahren-im-Zivilschutz": 17,
    "Brandsicherheitsdienst": 7,
    "Brennen": 79,
    "Fahrzeugkunde": 56,
    "Geraetekunde-Geraete-fuer-die-Technische-Hilfeleistung": 14,
    "Geraetekunde-Loeschgeraete-Schlaeuche-Armaturen": 58,
    "Geraetekunde-Persoenliche-Ausruestung": 12,
    "Geraetekunde-Rettungsgeraete": 44,
    "Geraetekunde-Sonstige-Geraete": 6,
    "Grundlagen-des-Zivil-und-Katastrophenschutzes": 18,
    "Lebensrettende-Sofortmassnahmen-Erste-Hilfe": 24,
    "Loescheinsatz": 82,
    "Loeschen": 70,
    "Physische-und-psychische-Belastung": 10,
    "Rechtsgrundlagen": 24,
    "Rettung-und-Absturzsicherung": 13,
    "Sprechfunk": 12,
    "Technische-Hilfeleistung": 16,
    "UnfallverhuetungsvorschriftenUnfallversicherung": 29,
    "Verhalten-bei-Gefahren": 22,
    "Wald-und-Vegetationsbrandbekaempfung": 12,
    "Wasserfoerderung": 10,
}

def create_placeholder_question(chapter_name, question_number):
    """Create a placeholder question object."""
    return {
        "question": f"[PLATZHALTER] Frage {question_number} im Kapitel {chapter_name} - Diese Frage muss noch aus dem PDF übernommen werden.",
        "answers": [
            "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort A)",
            "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort B)",
            "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort C)"
        ],
        "correctIndex": 0,
        "placeholder": True,
        "note": "Diese Frage wurde automatisch als Platzhalter erstellt und muss manuell korrigiert werden."
    }

def fill_missing_questions(data_dir, dry_run=False):
    """Fill missing questions in each chapter with placeholders."""
    
    total_filled = 0
    chapters_updated = []
    
    print("=" * 80)
    print("FEHLENDE FRAGEN MIT PLATZHALTERN FÜLLEN")
    print("=" * 80)
    print()
    
    if dry_run:
        print("🔍 DRY-RUN MODUS: Keine Dateien werden geändert\n")
    
    for chapter_filename, expected_count in sorted(EXPECTED_COUNTS.items()):
        json_file = Path(data_dir) / f"{chapter_filename}.json"
        
        if not json_file.exists():
            print(f"⚠️  Überspringe: {chapter_filename} (Datei nicht gefunden)")
            continue
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        actual_count = len(data['questions'])
        diff = expected_count - actual_count
        
        if diff <= 0:
            # No missing questions or extra questions
            continue
        
        chapter_display = chapter_filename.replace('-', ' ')
        print(f"📝 {chapter_display}")
        print(f"   Aktuell: {actual_count} Fragen")
        print(f"   Soll:    {expected_count} Fragen")
        print(f"   Fehlend: {diff} Fragen")
        
        # Add placeholder questions to reach expected count
        for i in range(diff):
            question_number = actual_count + i + 1
            placeholder = create_placeholder_question(chapter_display, question_number)
            data['questions'].append(placeholder)
            print(f"   ➕ Platzhalter-Frage {question_number} hinzugefügt")
        
        total_filled += diff
        chapters_updated.append(chapter_filename)
        
        # Save updated JSON
        if not dry_run:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"   ✅ Datei aktualisiert: {json_file.name}")
        
        print()
    
    # Summary
    print("=" * 80)
    print("ZUSAMMENFASSUNG")
    print("=" * 80)
    print(f"Kapitel aktualisiert:       {len(chapters_updated)}")
    print(f"Platzhalter hinzugefügt:    {total_filled}")
    
    if dry_run:
        print("\n💡 Führen Sie das Skript ohne --dry-run aus, um die Änderungen zu speichern.")
    else:
        print("\n✅ Alle Platzhalter wurden erfolgreich hinzugefügt!")
        print("⚠️  WICHTIG: Überprüfen Sie die Platzhalter-Fragen und ersetzen Sie sie mit den")
        print("   korrekten Fragen aus dem PDF.")
    
    return total_filled

def main():
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    
    if not data_dir.exists():
        print(f"❌ Fehler: Datenverzeichnis nicht gefunden: {data_dir}")
        return 1
    
    dry_run = '--dry-run' in sys.argv
    
    fill_missing_questions(data_dir, dry_run=dry_run)
    
    return 0

if __name__ == '__main__':
    exit(main())
