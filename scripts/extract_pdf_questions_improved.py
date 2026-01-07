#!/usr/bin/env python3
"""
Improved extraction script that tracks question numbers and fills gaps with placeholders.

This script ensures that every question has the correct number from the PDF,
and if a question cannot be parsed, a placeholder is inserted at the correct position.

Requirements:
    pip install pdfplumber Pillow

Usage:
    python3 scripts/extract_pdf_questions_improved.py
"""
import pdfplumber
import json
import re
import os
from pathlib import Path

# Expected question counts per chapter (from FEHLENDE_FRAGEN_BERICHT.md)
EXPECTED_COUNTS = {
    "ABC-Gefahrstoffe": 30,
    "Atemschutz": 33,
    "Besondere Gefahren im Zivilschutz": 7,
    "Brandsicherheitsdienst": 7,
    "Brennen": 79,
    "Fahrzeugkunde": 56,
    "Gerätekunde: Geräte für die Technische Hilfeleistung": 9,
    "Gerätekunde: Löschgeräte, Schläuche, Armaturen": 58,
    "Gerätekunde: Persönliche Ausrüstung": 12,
    "Gerätekunde: Rettungsgeräte": 44,
    "Gerätekunde: Sonstige Geräte": 9,
    "Grundlagen des Zivil- und Katastrophenschutzes": 18,
    "Lebensrettende Sofortmaßnahmen (Erste Hilfe)": 24,
    "Löscheinsatz": 88,
    "Löschen": 70,
    "Physische und psychische Belastung": 14,
    "Rechtsgrundlagen": 24,
    "Rettung und Absturzsicherung": 13,
    "Sprechfunk": 12,
    "Technische Hilfeleistung": 16,
    "Unfallverhütungsvorschriften/Unfallversicherung": 29,
    "Verhalten bei Gefahren": 22,
    "Wald- und Vegetationsbrandbekämpfung": 12,
    "Wasserförderung": 10,
}

def normalize_chapter_name(name):
    """Convert chapter name to filename format."""
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        ':': '', '(': '', ')': '', '/': ''
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '-', name)
    name = re.sub(r'-+', '-', name)
    return name.strip('-')

def create_placeholder_question(chapter_name, question_num):
    """Create a placeholder question with correct number."""
    return {
        "question": f"[PLATZHALTER] Frage {question_num} im Kapitel {chapter_name} - Diese Frage muss noch aus dem PDF übernommen werden.",
        "answers": [
            "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort A)",
            "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort B)",
            "[PLATZHALTER] Diese Antwort muss aus dem PDF übernommen werden (Antwort C)"
        ],
        "correctIndex": 0,
        "placeholder": True,
        "note": f"Diese Frage konnte nicht aus dem PDF extrahiert werden und muss manuell ergänzt werden."
    }

def extract_questions_from_pdf(pdf_path, output_dir, assets_dir):
    """Extract all questions from PDF with correct numbering."""
    
    with pdfplumber.open(pdf_path) as pdf:
        chapters = {}
        current_chapter = None
        current_question = None
        extracted_questions = {}  # Track question numbers that were extracted
        
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                if not line:
                    i += 1
                    continue
                
                # Detect new chapter
                if i > 0 and 'Fragenkatalog zur Hessischen Feuerwehrleistungsübung' in lines[i-1]:
                    # Save pending question from previous chapter
                    if current_question and len(current_question['answers']) == 3 and current_question['correctIndex'] >= 0:
                        qnum = current_question.get('question_number')
                        if qnum and current_chapter:
                            extracted_questions[current_chapter][qnum] = current_question
                        current_question = None
                    
                    if 'Es ist nur eine Antwortmöglichkeit richtig!' not in line:
                        current_chapter = line
                        if current_chapter not in chapters:
                            chapters[current_chapter] = {
                                'title': current_chapter,
                                'questions_dict': {}
                            }
                            extracted_questions[current_chapter] = {}
                            print(f"Found chapter: {current_chapter}")
                    i += 1
                    continue
                
                # Detect question with number
                question_match = re.match(r'^(\d+)\.\s+(.+)$', line)
                if question_match and current_chapter:
                    # Save previous question
                    if current_question and len(current_question['answers']) == 3:
                        if current_question['correctIndex'] >= 0:
                            qnum = current_question.get('question_number')
                            if qnum:
                                extracted_questions[current_chapter][qnum] = current_question
                    
                    # Start new question
                    question_num = int(question_match.group(1))
                    question_text = question_match.group(2)
                    
                    # Collect multi-line question text
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        if not next_line:
                            j += 1
                            continue
                        if next_line.startswith('x ') or next_line.startswith('X '):
                            break
                        if re.match(r'^\d+\.\s+', next_line):
                            break
                        if 'Antwortkatalog' in next_line or 'Seite' in next_line:
                            j += 1
                            continue
                        if question_text.endswith('?') or question_text.endswith('.'):
                            break
                        if next_line and len(next_line) > 0:
                            question_text += ' ' + next_line
                            j += 1
                        else:
                            break
                    
                    current_question = {
                        'question': question_text.strip(),
                        'answers': [],
                        'correctIndex': -1,
                        'question_number': question_num
                    }
                    i = j
                    continue
                
                # Collect answers
                if current_question is not None and len(current_question['answers']) < 3:
                    if 'Antwortkatalog' in line or 'Seite' in line or 'Hessische' in line:
                        i += 1
                        continue
                    
                    if line.startswith('x ') or line.startswith('X '):
                        answer_text = line[2:].strip()
                        if answer_text:
                            current_question['correctIndex'] = len(current_question['answers'])
                            current_question['answers'].append(answer_text)
                        i += 1
                        continue
                    
                    if not re.match(r'^\d+\.\s+', line) and line:
                        current_question['answers'].append(line)
                        i += 1
                        continue
                
                i += 1
            
            # Save pending question at end of page
            if current_question and len(current_question['answers']) == 3:
                if current_question['correctIndex'] >= 0:
                    qnum = current_question.get('question_number')
                    if qnum and current_chapter:
                        extracted_questions[current_chapter][qnum] = current_question
                current_question = None
        
        # Now fill gaps with placeholders for each chapter
        for chapter_name, questions_dict in extracted_questions.items():
            expected_count = EXPECTED_COUNTS.get(chapter_name, None)
            if not expected_count:
                print(f"⚠️  Warning: No expected count for chapter '{chapter_name}'")
                continue
            
            final_questions = []
            for q_num in range(1, expected_count + 1):
                if q_num in questions_dict:
                    # Remove the question_number field before saving
                    question = questions_dict[q_num].copy()
                    question.pop('question_number', None)
                    final_questions.append(question)
                    print(f"  ✓ Frage {q_num}")
                else:
                    # Create placeholder
                    placeholder = create_placeholder_question(chapter_name, q_num)
                    final_questions.append(placeholder)
                    print(f"  ⚠ Frage {q_num} - PLATZHALTER erstellt")
            
            chapters[chapter_name]['questions'] = final_questions
            print(f"✓ {chapter_name}: {len(final_questions)} Fragen ({expected_count} erwartet)")
    
    # Save JSON files
    saved_chapters = []
    for chapter_name, chapter_data in chapters.items():
        filename = normalize_chapter_name(chapter_name) + '.json'
        filepath = os.path.join(output_dir, filename)
        
        # Prepare final data structure
        output_data = {
            'title': chapter_data['title'],
            'questions': chapter_data['questions']
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        saved_chapters.append(filename)
        placeholders = sum(1 for q in chapter_data['questions'] if q.get('placeholder'))
        print(f"💾 Saved {filename} - {len(chapter_data['questions'])} Fragen ({placeholders} Platzhalter)")
    
    return saved_chapters

def update_meta_json(output_dir, chapter_files):
    """Update meta.json with the list of chapter files."""
    meta = {"chapters": sorted(chapter_files)}
    meta_path = os.path.join(output_dir, 'meta.json')
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Updated meta.json with {len(chapter_files)} chapters")

def main():
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    pdf_path = base_dir / 'data' / 'antwortkatalog-hflue-01.26.pdf'
    output_dir = base_dir / 'data'
    assets_dir = base_dir / 'assets' / 'piktos'
    
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("PDF EXTRAKTION MIT KORREKTER FRAGENNUMMERIERUNG")
    print("=" * 80)
    print(f"PDF: {pdf_path}")
    print(f"Output: {output_dir}\n")
    
    if not pdf_path.exists():
        print(f"❌ Fehler: PDF nicht gefunden: {pdf_path}")
        return 1
    
    saved_chapters = extract_questions_from_pdf(str(pdf_path), str(output_dir), str(assets_dir))
    update_meta_json(str(output_dir), saved_chapters)
    
    # Calculate statistics
    total_q = 0
    total_placeholders = 0
    for ch in saved_chapters:
        with open(output_dir / ch, 'r', encoding='utf-8') as f:
            data = json.load(f)
            total_q += len(data['questions'])
            total_placeholders += sum(1 for q in data['questions'] if q.get('placeholder'))
    
    print("\n" + "=" * 80)
    print("ZUSAMMENFASSUNG")
    print("=" * 80)
    print(f"Kapitel erstellt:        {len(saved_chapters)}")
    print(f"Gesamt Fragen:           {total_q}")
    print(f"Platzhalter:             {total_placeholders}")
    print(f"Vollständige Fragen:     {total_q - total_placeholders}")
    print(f"Erfolgsrate:             {((total_q - total_placeholders) / total_q * 100):.1f}%")
    
    return 0

if __name__ == '__main__':
    exit(main())
