import os
from pdfminer.high_level import extract_text as extract_pdf_text
import docx
import pytesseract
from PIL import Image

def extract_text_from_pdf(filepath):
    return extract_pdf_text(filepath)

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return '\n'.join(para.text for para in doc.paragraphs)

def extract_text_from_txt(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

def extract_text_with_ocr(filepath):
    return pytesseract.image_to_string(Image.open(filepath))

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.pdf':
            try:
                return extract_text_from_pdf(filepath)
            except Exception:
                return extract_text_with_ocr(filepath)
        elif ext == '.docx':
            return extract_text_from_docx(filepath)
        elif ext == '.txt':
            return extract_text_from_txt(filepath)
        else:
            return extract_text_with_ocr(filepath)
    except Exception as e:
        return f"Error extracting text: {str(e)}"
