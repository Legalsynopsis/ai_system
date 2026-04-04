import os
from PyPDF2 import PdfReader
from docx import Document
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from deep_translator import GoogleTranslator


def read_pdf(path):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if text.strip():
            return text

        # fallback OCR
        images = convert_from_path(path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img, lang="kan+eng")

        return text

    except Exception as e:
        return f"Error reading PDF: {e}"


def read_docx(path):
    try:
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {e}"


def read_image(path):
    try:
        img = Image.open(path)
        return pytesseract.image_to_string(img, lang="kan+eng")
    except Exception as e:
        return f"Error reading Image: {e}"


def translate_text(text, target="en"):
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except:
        return text


def read_document(path):
    if path.endswith(".pdf"):
        return read_pdf(path)

    elif path.endswith(".docx"):
        return read_docx(path)

    elif path.endswith((".png", ".jpg", ".jpeg")):
        return read_image(path)

    else:
        return "Unsupported file format"
