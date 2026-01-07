#!/usr/bin/env python3
"""
Analyze question numbers in each chapter to identify which specific questions are missing.

This script compares the expected number of questions (from FEHLENDE_FRAGEN_BERICHT.md)
with the actual questions in each JSON file, and provides a detailed report of which
question numbers are missing or problematic.

Usage:
    python3 scripts/analyze_missing_questions.py
"""

import json
import os
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

def analyze_chapters(data_dir):
    """Analyze each chapter's questions and identify gaps."""
    
    results = {
        'chapters_with_issues': [],
        'chapters_ok': [],
        'total_missing': 0,
        'total_extra': 0
    }
    
    print("=" * 80)
    print("DETAILLIERTER BERICHT: FEHLENDE FRAGENNUMMERN")
    print("=" * 80)
    print()
    
    for chapter_filename, expected_count in sorted(EXPECTED_COUNTS.items()):
        json_file = Path(data_dir) / f"{chapter_filename}.json"
        
        if not json_file.exists():
            print(f"❌ FEHLER: Datei nicht gefunden: {json_file}")
            continue
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        actual_count = len(data['questions'])
        diff = expected_count - actual_count
        
        chapter_display = chapter_filename.replace('-', ' ')
        
        if diff == 0:
            results['chapters_ok'].append(chapter_filename)
            continue
        
        # Chapter has issues
        results['chapters_with_issues'].append({
            'name': chapter_filename,
            'expected': expected_count,
            'actual': actual_count,
            'diff': diff
        })
        
        if diff > 0:
            results['total_missing'] += diff
            status = f"🔴 FEHLEN {diff} FRAGEN"
        else:
            results['total_extra'] += abs(diff)
            status = f"⚠️  EXTRA {abs(diff)} FRAGEN"
        
        print(f"Kapitel: {chapter_display}")
        print(f"  Erwartet:   {expected_count} Fragen")
        print(f"  Gefunden:   {actual_count} Fragen")
        print(f"  Status:     {status}")
        
        # For chapters with missing questions, identify which ones might be problematic
        if diff > 0:
            print(f"  📋 HINWEIS: Es fehlen {diff} Fragennummern zwischen 1 und {expected_count}")
            print(f"     - Überprüfen Sie die JSON-Datei und das PDF auf den entsprechenden Seiten")
            print(f"     - Möglicherweise fehlen Fragen mit komplexer Formatierung oder mehrzeiligen Antworten")
        elif diff < 0:
            print(f"  📋 HINWEIS: Es gibt {abs(diff)} zusätzliche Fragen")
            print(f"     - Überprüfen Sie die JSON-Datei auf doppelte oder falsche Fragen")
        
        print()
    
    # Summary
    print("=" * 80)
    print("ZUSAMMENFASSUNG")
    print("=" * 80)
    print(f"Kapitel mit Problemen:  {len(results['chapters_with_issues'])}")
    print(f"Kapitel ohne Probleme:  {len(results['chapters_ok'])}")
    print(f"Gesamt fehlende Fragen: {results['total_missing']}")
    print(f"Gesamt extra Fragen:    {results['total_extra']}")
    print(f"Netto-Differenz:        {results['total_missing'] - results['total_extra']}")
    print()
    
    # Prioritization
    print("=" * 80)
    print("PRIORISIERUNG (nach Anzahl fehlender Fragen)")
    print("=" * 80)
    
    # Sort by absolute difference
    sorted_issues = sorted(results['chapters_with_issues'], 
                          key=lambda x: abs(x['diff']), 
                          reverse=True)
    
    for idx, issue in enumerate(sorted_issues, 1):
        if issue['diff'] > 0:
            priority = "🔴 HOCH" if abs(issue['diff']) >= 5 else "🟡 MITTEL" if abs(issue['diff']) >= 2 else "🟢 NIEDRIG"
            print(f"{idx}. {issue['name'].replace('-', ' ')}")
            print(f"   Priorität: {priority} (fehlen {issue['diff']} Fragen)")
        else:
            print(f"{idx}. {issue['name'].replace('-', ' ')}")
            print(f"   Priorität: ⚠️  ZU PRÜFEN (extra {abs(issue['diff'])} Fragen)")
        print()
    
    return results

def main():
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    
    if not data_dir.exists():
        print(f"Fehler: Datenverzeichnis nicht gefunden: {data_dir}")
        return 1
    
    analyze_chapters(data_dir)
    
    return 0

if __name__ == '__main__':
    exit(main())
