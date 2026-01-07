# PDF Extraction Script

This directory contains a script to extract questions, answers, and images from the PDF catalog.

## extract_pdf_questions.py

Extracts all questions, answers, correct answers, and images/pictograms from `data/antwortkatalog-hflue-01.26.pdf` and creates JSON files for each chapter.

### Requirements

```bash
pip install pdfplumber Pillow
```

### Usage

From the repository root:

```bash
python3 scripts/extract_pdf_questions.py
```

### What it does

1. Parses the PDF to identify all chapters
2. Extracts questions with their three answer options
3. Identifies the correct answer (marked with 'x' in the PDF)
4. Extracts and saves any images/pictograms associated with questions
5. Creates a JSON file for each chapter in `data/`
6. Updates `data/meta.json` with the list of all chapters

### Output Format

Each chapter JSON file contains:

```json
{
  "title": "Chapter Name",
  "questions": [
    {
      "question": "Question text?",
      "answers": [
        "Answer 1",
        "Answer 2",
        "Answer 3"
      ],
      "correctIndex": 0,
      "image": "assets/piktos/image.png"  // Optional
    }
  ]
}
```

### Notes

- Images are saved to `assets/piktos/` with descriptive filenames
- The script maintains the exact question order from the PDF
- Questions without exactly 3 answers are skipped (validation)
- Old manual data files are preserved in `data/old_manual_data/`
