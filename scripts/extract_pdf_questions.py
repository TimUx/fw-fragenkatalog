#!/usr/bin/env python3
"""
Extract questions, answers, and images from the PDF catalog and create JSON files.

This script extracts all questions, answers, correct answers, and images/pictograms 
from the antwortkatalog-hflue-01.26.pdf and creates JSON files for each chapter
that can be used by the web application.

Requirements:
    pip install pdfplumber Pillow

Usage:
    python3 scripts/extract_pdf_questions.py
"""
import pdfplumber
import json
import re
import os
from pathlib import Path

def normalize_chapter_name(name):
    """Convert chapter name to filename format."""
    # Map German characters and normalize
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        ':': '', '(': '', ')': ''
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    # Replace spaces with hyphens, remove special chars
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '-', name)
    # Remove extra hyphens
    name = re.sub(r'-+', '-', name)
    return name.strip('-')

def extract_questions_from_pdf(pdf_path, output_dir, assets_dir):
    """Extract all questions from PDF and save to JSON files."""
    
    with pdfplumber.open(pdf_path) as pdf:
        chapters = {}
        current_chapter = None
        current_question = None
        
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # Skip empty lines
                if not line:
                    i += 1
                    continue
                
                # Detect new chapter - it comes after the "Fragenkatalog..." line
                if i > 0 and 'Fragenkatalog zur Hessischen Feuerwehrleistungsübung' in lines[i-1]:
                    # Skip the "Es ist nur eine..." line
                    if 'Es ist nur eine Antwortmöglichkeit richtig!' not in line:
                        current_chapter = line
                        if current_chapter not in chapters:
                            chapters[current_chapter] = {
                                'title': current_chapter,
                                'questions': []
                            }
                            print(f"Found chapter: {current_chapter}")
                    i += 1
                    continue
                
                # Detect question - starts with number followed by dot and space
                question_match = re.match(r'^(\d+)\.\s+(.+)$', line)
                if question_match and current_chapter:
                    # Save previous question if it's complete
                    if current_question and len(current_question['answers']) == 3:
                        chapters[current_chapter]['questions'].append(current_question)
                    
                    # Start new question
                    question_text = question_match.group(2)
                    
                    # Question might span multiple lines - collect until we hit an answer
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        # Stop if we hit an answer line
                        if next_line.startswith('x ') or next_line.startswith('X '):
                            break
                        # Stop if next question
                        if re.match(r'^\d+\.\s+', next_line):
                            break
                        # Stop if footer
                        if 'Antwortkatalog' in next_line or 'Seite' in next_line:
                            break
                        # Stop if we hit what looks like an answer
                        if next_line and not next_line[0].isdigit() and len(next_line) > 10:
                            if question_text.endswith('?') or question_text.endswith('.'):
                                break
                            question_text += ' ' + next_line
                            j += 1
                        else:
                            break
                    
                    current_question = {
                        'question': question_text.strip(),
                        'answers': [],
                        'correctIndex': -1
                    }
                    i = j
                    continue
                
                # Detect answers - collect exactly 3 answers after each question
                if current_question is not None and len(current_question['answers']) < 3:
                    # Skip footers
                    if 'Antwortkatalog' in line or 'Seite' in line:
                        i += 1
                        continue
                    
                    # Check if this is a marked correct answer
                    if line.startswith('x ') or line.startswith('X '):
                        answer_text = line[2:].strip()
                        current_question['correctIndex'] = len(current_question['answers'])
                        current_question['answers'].append(answer_text)
                        i += 1
                        continue
                    
                    # This is a regular answer
                    if not re.match(r'^\d+\.\s+', line):
                        current_question['answers'].append(line)
                        i += 1
                        continue
                
                i += 1
            
            # Save any pending question at end of page
            if current_question and len(current_question['answers']) == 3 and current_question['correctIndex'] >= 0:
                chapters[current_chapter]['questions'].append(current_question)
                current_question = None
            
            # Check for images on this page
            if page.images and current_chapter and chapters[current_chapter]['questions']:
                last_question = chapters[current_chapter]['questions'][-1]
                
                # Extract and save images
                for img_idx, img_info in enumerate(page.images):
                    try:
                        bbox = (img_info['x0'], img_info['top'], img_info['x1'], img_info['bottom'])
                        cropped_page = page.crop(bbox)
                        img = cropped_page.to_image(resolution=150)
                        
                        chapter_normalized = normalize_chapter_name(current_chapter)
                        img_filename = f"{chapter_normalized}_page{page_num+1}_img{img_idx+1}.png"
                        img_path = os.path.join(assets_dir, img_filename)
                        
                        img.save(img_path)
                        
                        if 'image' not in last_question:
                            last_question['image'] = f"assets/piktos/{img_filename}"
                            print(f"  Saved image: {img_filename}")
                    except Exception as e:
                        print(f"  Error extracting image from page {page_num+1}: {e}")
    
    # Save JSON files for each chapter
    saved_chapters = []
    for chapter_name, chapter_data in chapters.items():
        valid_questions = [q for q in chapter_data['questions'] 
                          if len(q['answers']) == 3 and q['correctIndex'] >= 0 and q['question']]
        
        if valid_questions:
            chapter_data['questions'] = valid_questions
            filename = normalize_chapter_name(chapter_name) + '.json'
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(chapter_data, f, ensure_ascii=False, indent=2)
            
            saved_chapters.append(filename)
            print(f"Saved {filename} with {len(valid_questions)} questions")
    
    return saved_chapters

def update_meta_json(output_dir, chapter_files):
    """Update meta.json with the list of chapter files."""
    meta = {"chapters": sorted(chapter_files)}
    meta_path = os.path.join(output_dir, 'meta.json')
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"\nUpdated meta.json with {len(chapter_files)} chapters")

def main():
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    pdf_path = base_dir / 'data' / 'antwortkatalog-hflue-01.26.pdf'
    output_dir = base_dir / 'data'
    assets_dir = base_dir / 'assets' / 'piktos'
    
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    print("Starting PDF extraction...")
    print(f"PDF: {pdf_path}")
    print(f"Output: {output_dir}")
    print(f"Assets: {assets_dir}\n")
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        return 1
    
    saved_chapters = extract_questions_from_pdf(str(pdf_path), str(output_dir), str(assets_dir))
    update_meta_json(str(output_dir), saved_chapters)
    
    total_q = sum(len(json.load(open(output_dir / ch))['questions']) for ch in saved_chapters)
    print(f"\n✓ Extraction complete!")
    print(f"  Chapters: {len(saved_chapters)}")
    print(f"  Questions: {total_q}")
    
    return 0

if __name__ == '__main__':
    exit(main())
